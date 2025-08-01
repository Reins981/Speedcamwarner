import json, os
from google.cloud import dialogflow_v2 as dialogflow
from openai import OpenAI
from ServiceAccount import SERVICE_ACCOUNT, load_service_account

# Refactored user_phrases to include all possible voice prompt strings from AccustWarnerThread

user_phrases = [
    # EXIT / STOP
    "Exit the app",
    "Close the application",
    "Stop running",
    "Shut down the speed camera app",
    "Quit",
    "Terminate",
    "End application",

    # ADD POLICE
    "I saw a police car",
    "Add a police warning",
    "There’s a police checkpoint",
    "Mark police location",
    "Report police",
    "Police ahead",
    "Police trap",
    "Add police marker",

    # POLICE ADD FAIL
    "Adding police didn't work",
    "Police marker failed",
    "Couldn't report police",
    "Failed to add police",
    "Police not added",

    # GPS
    "GPS is off",
    "Turn on GPS",
    "I lost GPS signal",
    "GPS is weak",
    "GPS is back online",
    "No GPS",
    "GPS unavailable",
    "GPS signal lost",

    # INTERNET / OSM DATA
    "No internet connection",
    "The map isn’t loading",
    "Can't download data",
    "Why is there no data from the server?",
    "No map data",
    "Offline mode",
    "No connection",
    "Server not reachable",

    # HAZARD
    "There’s a hazard ahead",
    "Danger on the road",
    "I see something dangerous",
    "Hazard detected",
    "Road hazard",
    "Obstacle ahead",

    # SPEED CAMERA WARNINGS

    # Fixed camera distance prompts
    "Fixed camera 100 meters ahead",
    "Fixed camera ahead in 100 meters",
    "There is a fixed camera 100 meters away",
    "Fixed speed camera 100 meters ahead",
    "Fixed camera coming up in 100 meters",
    "Fixed camera 300 meters ahead",
    "Fixed camera ahead in 300 meters",
    "There is a fixed camera 300 meters away",
    "Fixed speed camera 300 meters ahead",
    "Fixed camera coming up in 300 meters",
    "Fixed camera 500 meters ahead",
    "Fixed camera ahead in 500 meters",
    "There is a fixed camera 500 meters away",
    "Fixed speed camera 500 meters ahead",
    "Fixed camera coming up in 500 meters",
    "Fixed camera 1000 meters ahead",
    "Fixed camera ahead in 1000 meters",
    "There is a fixed camera 1000 meters away",
    "Fixed speed camera 1000 meters ahead",
    "Fixed camera coming up in 1000 meters",

    # Traffic camera distance prompts
    "Traffic camera 100 meters ahead",
    "Traffic camera ahead in 100 meters",
    "There is a traffic camera 100 meters away",
    "Traffic enforcement camera 100 meters ahead",
    "Traffic camera coming up in 100 meters",
    "Traffic camera 300 meters ahead",
    "Traffic camera ahead in 300 meters",
    "There is a traffic camera 300 meters away",
    "Traffic enforcement camera 300 meters ahead",
    "Traffic camera coming up in 300 meters",
    "Traffic camera 500 meters ahead",
    "Traffic camera ahead in 500 meters",
    "There is a traffic camera 500 meters away",
    "Traffic enforcement camera 500 meters ahead",
    "Traffic camera coming up in 500 meters",
    "Traffic camera 1000 meters ahead",
    "Traffic camera ahead in 1000 meters",
    "There is a traffic camera 1000 meters away",
    "Traffic enforcement camera 1000 meters ahead",
    "Traffic camera coming up in 1000 meters",

    # Mobile speed trap distance prompts
    "Mobile speed trap 100 meters ahead",
    "Mobile speed trap ahead in 100 meters",
    "There is a mobile speed trap 100 meters away",
    "Mobile speed camera 100 meters ahead",
    "Mobile speed trap coming up in 100 meters",
    "Mobile speed trap 300 meters ahead",
    "Mobile speed trap ahead in 300 meters",
    "There is a mobile speed trap 300 meters away",
    "Mobile speed camera 300 meters ahead",
    "Mobile speed trap coming up in 300 meters",
    "Mobile speed trap 500 meters ahead",
    "Mobile speed trap ahead in 500 meters",
    "There is a mobile speed trap 500 meters away",
    "Mobile speed camera 500 meters ahead",
    "Mobile speed trap coming up in 500 meters",
    "Mobile speed trap 1000 meters ahead",
    "Mobile speed trap ahead in 1000 meters",
    "There is a mobile speed trap 1000 meters away",
    "Mobile speed camera 1000 meters ahead",
    "Mobile speed trap coming up in 1000 meters",

    # General camera warnings
    "Speed camera nearby",
    "Camera just ahead",
    "Speed trap ahead",

    # DISTANCE-BASED CAMERA ALERTS
    "Camera right ahead",
    "Camera within proximity range",

    # POI
    "I reached my destination",
    "Add this point of interest",
    "POI failed to save",
    "Stop the route",
    "No route available",
    "Save this location",
    "Destination reached",
    "Route ended",

    # MISC
    "There's water on the road",
    "What's the access control status?",
    "Something’s wrong with direction",
    "There’s a person on the road",
    "Pedestrian detected",
    "Access control error",
    "Wrong direction",
    "Unexpected object on road"
]

# 1. Send user phrases to OpenAI API to get intents + training phrases
"""client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You group user phrases into Dialogflow intents with intent names and training phrases."
        },
        {
            "role": "user",
            "content": json.dumps(user_phrases)
        }
    ]
)

# 2. Extract and parse the response
response_text = response.choices[0].message.content
intents = json.loads(response_text)"""

# 3. For each intent, create Dialogflow intent via Dialogflow API
client = dialogflow.IntentsClient()
json_data = load_service_account()
project_id = json_data["project_id"]
parent = dialogflow.AgentsClient.agent_path(project_id)

intents = [
    {
        "intent": "EXIT_APPLICATION",
        "training_phrases": [
            "Exit the app", "Close the application", "Stop running",
            "Please exit", "End the program", "Leave the app", "Exit now", "Close speedcamwarner", "I want to quit", "Stop the software", "Terminate the process", "End this session", "Shut down now"
        ]
    },
    {
        "intent": "ADDED_POLICE",
        "training_phrases": [
            "I saw a police car", "Add a police warning", "There’s a police checkpoint",
            "Police spotted", "Mark police here", "Police location ahead", "Warn about police", "Add police alert", "Police presence", "Police on the road", "Report police car", "Police detected", "Mark police checkpoint"
        ]
    },
    {
        "intent": "ADDING_POLICE_FAILED",
        "training_phrases": [
            "Adding police didn't work", "Police marker failed", "Couldn't report police",
            "Police warning not added", "Failed to mark police", "Police alert failed", "Police not reported", "Error adding police", "Police marker error", "Unable to add police", "Police report unsuccessful", "Police warning error", "Could not mark police"
        ]
    },
    {
        "intent": "STOP_APPLICATION",
        "training_phrases": [
            "Shut down the speed camera app", "Quit", "Terminate", "End application",
            "Stop the app", "Close speed camera app", "Exit speedcamwarner", "Stop speedcamwarner", "End the speedcamwarner app", "Terminate speedcamwarner", "Quit the application", "Close the program", "Stop this application"
        ]
    },
    {
        "intent": "GPS_OFF",
        "training_phrases": [
            "GPS is off", "Turn on GPS", "I lost GPS signal", "GPS is weak",
            "GPS disconnected", "No GPS signal", "GPS turned off", "GPS unavailable", "GPS not working", "GPS not detected", "GPS is disabled", "GPS is not active", "GPS is not on"
        ]
    },
    {
        "intent": "GPS_LOW",
        "training_phrases": [
            "Low GPS signal", "Weak GPS signal", "GPS is not accurate",
            "GPS accuracy is low", "GPS signal is poor", "Unstable GPS", "GPS is unreliable", "GPS signal weak", "GPS not precise", "GPS is fluctuating", "GPS is inconsistent", "GPS is not strong", "GPS is not stable"
        ]
    },  
    {
        "intent": "GPS_ON",
        "training_phrases": [
            "GPS is back online", "GPS signal restored", "GPS is now active",
            "GPS reconnected", "GPS is working again", "GPS is available", "GPS is enabled", "GPS is functioning", "GPS is online", "GPS is operational", "GPS is up", "GPS is active again", "GPS is back"
        ]
    },
    {
        "intent": "SPEEDCAM_BACKUP",
        "training_phrases": [
            "Speed camera backup", "Backup speed camera data", "Save speed camera locations",
            "Backup cameras", "Store speed camera info", "Backup all speed cameras", "Save camera data", "Backup speedcamwarner data", "Create speed camera backup", "Backup speedcam data", "Save all camera locations", "Backup speedcam info", "Backup speed camera points"
        ]
    },
    {
        "intent": "SPEEDCAM_REINSERT",
        "training_phrases": [
            "Reinsert speed camera data", "Restore speed camera locations", "Speed camera data reinserted",
            "Reload speed camera data", "Re-add speed cameras", "Restore camera info", "Reinstate speed camera data", "Import speed camera backup", "Reinsert all cameras", "Restore speedcamwarner data", "Reimport speed camera points", "Reinsert camera locations", "Restore speedcam data"
        ]
    },
    {
        "intent": "INTERNET_CONN_FAILED",
        "training_phrases": [
            "No internet connection", "The map isn’t loading", "Can't download data",
            "Internet is down", "No connection", "Offline mode", "No network", "Internet unavailable", "No data connection", "Internet not working", "No access to internet", "Network error", "Internet failure"
        ]
    },
    {
        "intent": "HAZARD",
        "training_phrases": [
            "There’s a hazard ahead", "Danger on the road", "I see something dangerous",
            "Hazard detected", "Road hazard", "Obstacle ahead", "Dangerous situation", "Hazard on route", "Warning: hazard", "Potential hazard", "Hazard in the way", "Danger detected", "Obstacle on the road"
        ]
    },
    {
        "intent": "FIX_100",    
        "training_phrases": [
            "Fixed camera 100 meters ahead", "Fixed camera ahead in 100 meters", "There is a fixed camera 100 meters away",
            "Speed camera 100 meters ahead", "Fixed speed camera in 100 meters", "Camera ahead 100 meters", "Fixed camera coming up in 100 meters", "Fixed camera at 100 meters", "Fixed camera nearby", "Fixed camera close", "Fixed camera soon", "Camera in 100 meters", "Fixed camera up ahead"
        ]
    },
    {
        "intent": "FIX_300",    
        "training_phrases": [
            "Fixed camera 300 meters ahead", "Fixed camera ahead in 300 meters", "There is a fixed camera 300 meters away",
            "Speed camera 300 meters ahead", "Fixed speed camera in 300 meters", "Camera ahead 300 meters", "Fixed camera coming up in 300 meters", "Fixed camera at 300 meters", "Fixed camera nearby", "Fixed camera close", "Fixed camera soon", "Camera in 300 meters", "Fixed camera up ahead"
        ]
    },
    {   "intent": "FIX_500",    
        "training_phrases": [
            "Fixed camera 500 meters ahead", "Fixed camera ahead in 500 meters", "There is a fixed camera 500 meters away",
            "Speed camera 500 meters ahead", "Fixed speed camera in 500 meters", "Camera ahead 500 meters", "Fixed camera coming up in 500 meters", "Fixed camera at 500 meters", "Fixed camera nearby", "Fixed camera close", "Fixed camera soon", "Camera in 500 meters", "Fixed camera up ahead"
        ]
    },
    {   "intent": "FIX_1000",    
        "training_phrases": [
            "Fixed camera 1000 meters ahead", "Fixed camera ahead in 1000 meters", "There is a fixed camera 1000 meters away",
            "Speed camera 1000 meters ahead", "Fixed speed camera in 1000 meters", "Camera ahead 1000 meters", "Fixed camera coming up in 1000 meters", "Fixed camera at 1000 meters", "Fixed camera nearby", "Fixed camera close", "Fixed camera soon", "Camera in 1000 meters", "Fixed camera up ahead"
        ]
    },  
    {   "intent": "TRAFFIC_100",
        "training_phrases": [
            "Traffic camera 100 meters ahead", "Traffic camera ahead in 100 meters", "There is a traffic camera 100 meters away",
            "Traffic enforcement camera 100 meters ahead", "Traffic camera coming up in 100 meters", "Traffic camera at 100 meters", "Traffic camera nearby", "Traffic camera close", "Traffic camera soon", "Camera in 100 meters", "Traffic camera up ahead", "Traffic camera in 100 meters", "Traffic camera just ahead"
        ]
    },      
    {   "intent": "TRAFFIC_300",
        "training_phrases": [
            "Traffic camera 300 meters ahead", "Traffic camera ahead in 300 meters", "There is a traffic camera 300 meters away",
            "Traffic enforcement camera 300 meters ahead", "Traffic camera coming up in 300 meters", "Traffic camera at 300 meters", "Traffic camera nearby", "Traffic camera close", "Traffic camera soon", "Camera in 300 meters", "Traffic camera up ahead", "Traffic camera in 300 meters", "Traffic camera just ahead"
        ]
    },  
    {   "intent": "TRAFFIC_500",
        "training_phrases": [
            "Traffic camera 500 meters ahead", "Traffic camera ahead in 500 meters", "There is a traffic camera 500 meters away",
            "Traffic enforcement camera 500 meters ahead", "Traffic camera coming up in 500 meters", "Traffic camera at 500 meters", "Traffic camera nearby", "Traffic camera close", "Traffic camera soon", "Camera in 500 meters", "Traffic camera up ahead", "Traffic camera in 500 meters", "Traffic camera just ahead"
        ]
    },
    {   "intent": "TRAFFIC_1000",
        "training_phrases": [
            "Traffic camera 1000 meters ahead", "Traffic camera ahead in 1000 meters", "There is a traffic camera 1000 meters away",
            "Traffic enforcement camera 1000 meters ahead", "Traffic camera coming up in 1000 meters", "Traffic camera at 1000 meters", "Traffic camera nearby", "Traffic camera close", "Traffic camera soon", "Camera in 1000 meters", "Traffic camera up ahead", "Traffic camera in 1000 meters", "Traffic camera just ahead"
        ]
    },
    {   "intent": "MOBILE_100",
        "training_phrases": [
            "Mobile speed trap 100 meters ahead", "Mobile speed trap ahead in 100 meters", "There is a mobile speed trap 100 meters away",
            "Mobile speed camera 100 meters ahead", "Mobile speed trap coming up in 100 meters", "Mobile speed trap at 100 meters", "Mobile trap nearby", "Mobile trap close", "Mobile trap soon", "Trap in 100 meters", "Mobile trap up ahead", "Mobile trap in 100 meters", "Mobile trap just ahead"
        ]
    },
    {   "intent": "MOBILE_300",
        "training_phrases": [
            "Mobile speed trap 300 meters ahead", "Mobile speed trap ahead in 300 meters", "There is a mobile speed trap 300 meters away",
            "Mobile speed camera 300 meters ahead", "Mobile speed trap coming up in 300 meters", "Mobile speed trap at 300 meters", "Mobile trap nearby", "Mobile trap close", "Mobile trap soon", "Trap in 300 meters", "Mobile trap up ahead", "Mobile trap in 300 meters", "Mobile trap just ahead"
        ]
    },
    {   "intent": "MOBILE_500",
        "training_phrases": [
            "Mobile speed trap 500 meters ahead", "Mobile speed trap ahead in 500 meters", "There is a mobile speed trap 500 meters away",
            "Mobile speed camera 500 meters ahead", "Mobile speed trap coming up in 500 meters", "Mobile speed trap at 500 meters", "Mobile trap nearby", "Mobile trap close", "Mobile trap soon", "Trap in 500 meters", "Mobile trap up ahead", "Mobile trap in 500 meters", "Mobile trap just ahead"
        ]
    },
    {   "intent": "MOBILE_1000",
        "training_phrases": [
            "Mobile speed trap 1000 meters ahead", "Mobile speed trap ahead in 1000 meters", "There is a mobile speed trap 1000 meters away",
            "Mobile speed camera 1000 meters ahead", "Mobile speed trap coming up in 1000 meters", "Mobile speed trap at 1000 meters", "Mobile trap nearby", "Mobile trap close", "Mobile trap soon", "Trap in 1000 meters", "Mobile trap up ahead", "Mobile trap in 1000 meters", "Mobile trap just ahead"
        ]
    },
    {   "intent": "DISTANCE_100",
        "training_phrases": [
            "Distance 100 meters ahead", "Distance ahead in 100 meters", "There is a distance marker 100 meters away",
            "Distance marker 100 meters ahead", "Distance marker in 100 meters", "Marker ahead 100 meters", "Distance coming up in 100 meters", "Distance at 100 meters", "Distance marker nearby", "Distance marker close", "Distance marker soon", "Marker in 100 meters", "Distance marker up ahead"
        ]
    },
    {   "intent": "DISTANCE_300",
        "training_phrases": [
            "Distance 300 meters ahead", "Distance ahead in 300 meters", "There is a distance marker 300 meters away",
            "Distance marker 300 meters ahead", "Distance marker in 300 meters", "Marker ahead 300 meters", "Distance coming up in 300 meters", "Distance at 300 meters", "Distance marker nearby", "Distance marker close", "Distance marker soon", "Marker in 300 meters", "Distance marker up ahead"
        ]
    },
    {   "intent": "DISTANCE_500",
        "training_phrases": [
            "Distance 500 meters ahead", "Distance ahead in 500 meters", "There is a distance marker 500 meters away",
            "Distance marker 500 meters ahead", "Distance marker in 500 meters", "Marker ahead 500 meters", "Distance coming up in 500 meters", "Distance at 500 meters", "Distance marker nearby", "Distance marker close", "Distance marker soon", "Marker in 500 meters", "Distance marker up ahead"
        ]
    },
    {   "intent": "DISTANCE_1000",
        "training_phrases": [
            "Distance 1000 meters ahead", "Distance ahead in 1000 meters", "There is a distance marker 1000 meters away",
            "Distance marker 1000 meters ahead", "Distance marker in 1000 meters", "Marker ahead 1000 meters", "Distance coming up in 1000 meters", "Distance at 1000 meters", "Distance marker nearby", "Distance marker close", "Distance marker soon", "Marker in 1000 meters", "Distance marker up ahead"
        ]
    },
    {   "intent": "FIX_NOW",
        "training_phrases": [
            "Fix camera right ahead", "Fix camera just ahead", "Fix camera inf front of you",
            "Fixed camera immediately ahead", "Fixed camera in front", "Fixed camera now", "Fixed camera directly ahead", "Fixed camera close by", "Fixed camera at your location", "Fixed camera here", "Fixed camera present", "Fixed camera on your path", "Fixed camera in your lane"
        ]
    },
    {   "intent": "TRAFFIC_NOW",
        "training_phrases": [
            "Traffic camera right ahead", "Traffic camera just ahead", "Traffic camera in front of you",
            "Traffic camera immediately ahead", "Traffic camera in front", "Traffic camera now", "Traffic camera directly ahead", "Traffic camera close by", "Traffic camera at your location", "Traffic camera here", "Traffic camera present", "Traffic camera on your path", "Traffic camera in your lane"
        ]
    },
    {   "intent": "MOBILE_NOW",
        "training_phrases": [
            "Mobile speed trap right ahead", "Mobile speed trap just ahead", "Mobile speed trap in front of you",
            "Mobile trap immediately ahead", "Mobile trap in front", "Mobile trap now", "Mobile trap directly ahead", "Mobile trap close by", "Mobile trap at your location", "Mobile trap here", "Mobile trap present", "Mobile trap on your path", "Mobile trap in your lane"
        ]
    },
    {   "intent": "DISTANCE_NOW",
        "training_phrases": [
            "Distance camera right ahead", "Distance camera just ahead", "Distance camera in front of you",
            "Distance marker immediately ahead", "Distance marker in front", "Distance marker now", "Distance marker directly ahead", "Distance marker close by", "Distance marker at your location", "Distance marker here", "Distance marker present", "Distance marker on your path", "Distance marker in your lane"
        ]
    },
    {   "intent": "WATER",
        "training_phrases": [
            "There's water on the road", "Water hazard just ahead", "Water on the roadway",
            "Flooded road", "Water detected", "Wet road ahead", "Water spill", "Water on route", "Water in the way", "Water on my path", "Water on the street", "Standing water", "Puddle ahead"
        ]
    },
    {   "intent": "ACCESS_CONTROL",
        "training_phrases": [
            "Access control right ahead", "Access control just ahead", "Access control in front of you",
            "Access control immediately ahead", "Access control in front", "Access control now", "Access control directly ahead", "Access control close by", "Access control at your location", "Access control here", "Access control present", "Access control on your path", "Access control in your lane"
        ]
    },
    {   "intent": "POI_SUCCESS",
        "training_phrases": [
            "Point of interest added", "POI saved successfully", "Location marked as POI",
            "POI created", "POI stored", "POI registered", "POI marked", "POI added", "POI location saved", "POI set", "POI point added", "POI successfully created", "POI successfully marked"
        ]
    },
    {   "intent": "POI_FAILED",
        "training_phrases": [
            "Failed to save POI", "POI not saved", "Could not add point of interest",
            "POI save error", "POI creation failed", "POI not created", "POI not marked", "POI add failed", "POI not registered", "POI not stored", "POI not set", "POI could not be added", "POI could not be saved"
        ]
    },
    {   "intent": "ANGLE_MISMATCH",
        "training_phrases": [
            "Wrong direction, Camera discarded", "Unexpected camera angle detected", "Direction mismatch detected",
            "Camera angle error", "Camera discarded due to angle", "Angle mismatch", "Camera not aligned", "Camera facing wrong way", "Camera orientation error", "Camera not in correct direction", "Camera angle mismatch", "Camera not facing road", "Camera direction error"
        ]
    },
    {    "intent": "LOW_DOWNLOAD_DATA_RATE",
        "training_phrases": [
            "Low download data rate", "Slow data download", "Data download is slow",
            "Slow internet speed", "Download speed is low", "Data coming in slowly", "Slow connection", "Slow data transfer", "Low bandwidth", "Download is slow", "Data rate is low", "Internet is slow", "Slow download detected"
        ]
    },
]

for intent in intents:
    intent_name = intent['intent'].upper()
    training_phrases = [
        dialogflow.Intent.TrainingPhrase(parts=[dialogflow.Intent.TrainingPhrase.Part(text=intent_name)])
    ]
    responses = intent['training_phrases']
    new_intent = dialogflow.Intent(
        display_name=intent['intent'],
        training_phrases=training_phrases,
        messages=[
            dialogflow.Intent.Message(
                text=dialogflow.Intent.Message.Text(text=responses)
            )
        ]
    )
    # Uncomment and set parent to enable actual creation
    # response = client.create_intent(request={"parent": parent, "intent": new_intent})
    print(f"Prepared intent {intent['intent']} with training phrase '{intent_name}' and responses {responses}")
    response = client.create_intent(request={"parent": parent, "intent": new_intent})
    print(f"Created intent {intent['intent']} with training phrase '{intent_name}' and responses {responses}")


'''for intent in intents:
    training_phrases = [
        dialogflow.Intent.TrainingPhrase(parts=[dialogflow.Intent.TrainingPhrase.Part(text=phrase)])
        for phrase in intent['training_phrases']
    ]
    new_intent = dialogflow.Intent(
        display_name=intent['intent'],
        training_phrases=training_phrases,
        # You can add responses or parameters here too
    )
    response = client.create_intent(request={"parent": parent, "intent": new_intent})
    print(f"Created intent {intent['intent']}")'''
