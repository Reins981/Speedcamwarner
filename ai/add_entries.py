import json
import random

# File path to the training.json file
file_path = "training.json"

# Load the existing JSON data
with open(file_path, "r") as file:
    data = json.load(file)

# Generate 1000 new simulated camera entries
new_cameras = []
for i in range(11, 1011):
    new_camera = {
        "name": f"Simulated Camera {i}",
        "coordinates": [
            {
                "latitude": round(random.uniform(-90, 90), 6),
                "longitude": round(random.uniform(-180, 180), 6)
            }
        ]
    }
    new_cameras.append(new_camera)

# Append the new cameras to the existing data
data["cameras"].extend(new_cameras)

# Save the updated JSON data back to the file
with open(file_path, "w") as file:
    json.dump(data, file, indent=4)

print("Added 1000 new entries to training.json.")
