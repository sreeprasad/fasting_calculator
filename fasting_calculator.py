import os
import json
from datetime import datetime, timedelta

def get_user_input():
    start_time = input("Enter fasting start time (HH:MM): ")
    end_time = input("Enter fasting end time (HH:MM): ")
    goal_hours = int(input("Enter fasting goal in hours: "))
    return start_time, end_time, goal_hours

def calculate_fasting_hours(input_start_time: str, input_end_time: str, goal_hours: int):
    start_time = datetime.strptime(input_start_time, "%H:%M")
    end_time = datetime.strptime(input_end_time, "%H:%M")
    
    if end_time < start_time:
        end_time += timedelta(days=1)  
    fasting_duration = end_time - start_time
    fasting_hours = fasting_duration.total_seconds() / 3600  
    
    result = {
        "start_time": input_start_time,
        "end_time": input_end_time,
        "fasting_hours": fasting_hours,
        "goal_hours": goal_hours,
        "completed": fasting_hours >= goal_hours
    }
    return result

def save_to_file(data, filename="fasting_data.json"):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_from_file(filename="fasting_data.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    return None

def save_completed_fast(data, filename="completed_fast.json"):
    completed_data = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            completed_data = json.load(file)

    completed_data.append(data)
    
    with open(filename, 'w') as file:
        json.dump(completed_data, file)

def main():
    filename = "fasting_data.json"
    existing_data = load_from_file(filename)
    
    if existing_data:
        overwrite = input("Already fasting in progress. Do you want to start new (yes/no): ")
        overwrite = overwrite.strip().lower()
        if overwrite != 'yes':
            print("Continuing existing fast.")
            data = existing_data
        else:
            start_time, end_time, goal_hours = get_user_input()
            data = calculate_fasting_hours(start_time, end_time, goal_hours)
            save_to_file(data, filename)
    else:
        start_time, end_time, goal_hours = get_user_input()
        data = calculate_fasting_hours(start_time, end_time, goal_hours)
        save_to_file(data, filename)

    print(f"Fasting Hours: {data['fasting_hours']:.2f}")
    print(f"Fasting Goal: {data['goal_hours']} hours")
    
    if data['goal_hours'] > data['fasting_hours']:
        print(f"Hours Left to Reach Goal: {data['goal_hours'] - data['fasting_hours']:.2f}")
    else:
        print("You have met or exceeded your fasting goal!")
        save_completed_fast(data)
        os.remove(filename)
        print("Fast completed and saved to 'completed_fast.json'.")

if __name__ == "__main__":
    main()

