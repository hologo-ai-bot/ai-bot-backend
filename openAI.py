import requests
import time
import os
# from dotenv import load_dotenv 

# load_dotenv()
class OpenAIRepository:
    def createThread(self,apiToken):
        url = 'https://api.openai.com/v1/threads'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta' : 'assistants=v2'
        }

        response = requests.post(url,headers=headers)
        # print(response.json()['id'])
        return response.json()['id']

    
    def sendMessageThread(self,apiToken,threadID,message):
        url = f'https://api.openai.com/v1/threads/{threadID}/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta' : 'assistants=v2'
        }

        data = {
        "role": "user",
        "content": f"{message}"
        }

        response = requests.post(url,headers=headers,json=data)
        return response.json()

    def runThread(self,apiToken,threadID,assistant_ID):
        url = f'https://api.openai.com/v1/threads/{threadID}/runs'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta' : 'assistants=v2'
        }

        data={"assistant_id": f"{assistant_ID}"}

        response = requests.post(url,headers=headers,json=data)
        return response.json()['id']
    


    def checkRunStatus(self,apiToken,threadID,runID):
        url = f'https://api.openai.com/v1/threads/{threadID}/runs/{runID}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta' : 'assistants=v2'
        }
        response = requests.get(url,headers=headers)
        return response.json()['status']
    


    def retriveMessage(self,apiToken,threadID):
        url = f'https://api.openai.com/v1/threads/{threadID}/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}',
            'OpenAI-Beta' : 'assistants=v2'
        }
        response = requests.get(url,headers=headers)
        return response.json()['data'][0]['content'][0]['text']['value']
    

    def connectAi(self, apiToken, message, assistant_ID):
        threadID = self.createThread(apiToken)
        if threadID:
            self.sendMessageThread(apiToken, threadID, message)
            runID = self.runThread(apiToken, threadID, assistant_ID)
            if runID:
                status = ''
                while status != "completed":
                    print(f"Current status: {status}. Checking again in 5 seconds...")
                    time.sleep(5)  # Wait for 5 seconds before checking the status again
                    status = self.checkRunStatus(apiToken, threadID, runID)
                if status == "completed":
                    final_message = self.retriveMessage(apiToken, threadID)
                    return final_message




apiToken = os.getenv("OPENAI_API_TOKEN")
message = os.getenv("ASSISTANT_ID")
assistant_ID = 'asst_jm8jRCaQ9S6WKelXbSJgfvDs'

repository = OpenAIRepository()
response_message = repository.connectAi(apiToken, message, assistant_ID)
print(f'Response message: {response_message}')