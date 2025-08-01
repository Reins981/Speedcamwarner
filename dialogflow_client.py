import os
import uuid
from google.cloud import dialogflow_v2 as dialogflow


class DialogflowClient:
    def __init__(self, project_id, language_code="en"):
        self.project_id = project_id
        self.language_code = language_code
        self.session_client = dialogflow.SessionsClient()

    def detect_intent(self, text):
        session_id = str(uuid.uuid4())
        session = self.session_client.session_path(self.project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code=self.language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        try:
            response = self.session_client.detect_intent(request={"session": session, "query_input": query_input})
            return response.query_result.fulfillment_text
        except Exception as e:
            print(f"Error during Dialogflow request: {e}")
            return "Sorry, I couldn't process your request."

# Example usage (replace 'your-project-id' with your Dialogflow project ID):
# client = DialogflowClient(project_id='your-project-id')
# response = client.detect_intent(text='Hello')
# print(response)
