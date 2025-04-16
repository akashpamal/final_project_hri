import time
import json
import requests

def main():
    file_name = input("Enter the name of the file: ")
    url = "http://127.0.0.1:5001/receive_json"

    try:
        with open(file_name, 'r') as file:
            movements = []
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # Split into elapsed time and JSON data
                time_str, json_str = line.split(',', 1)
                elapsed_time = float(time_str)
                movement_data = json.loads(json_str)
                movements.append((elapsed_time, movement_data))

            print(movements)
            # Sort by elapsed time (assuming chronological order)
            movements.sort(key=lambda x: x[0]) # Should already be sorted in chronological order
            print(movements)

            # Execute movements with precise timing
            start_time = time.time()
            for elapsed, data in movements:
                # Calculate remaining wait time
                current_elapsed = time.time() - start_time
                delay = elapsed - current_elapsed
                if delay > 0:
                    time.sleep(delay)
                else: # Don't send a ton of requests at once
                    continue
                
                # Send HTTP request
                try:
                    response = requests.post(
                        url,
                        json=data,
                        timeout=0.5
                    )
                    print(f"Sent {data['movementType']} to {data['chainName']} "
                          f"at {elapsed}s (Status: {response.status_code})")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {str(e)}")

    except FileNotFoundError:
        print("Error: File not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in file")
    except ValueError as e:
        print(f"Error parsing data: {str(e)}")

if __name__ == "__main__":
    main()
