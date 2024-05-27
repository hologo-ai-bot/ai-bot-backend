import requests

class OpenAIRepository:
    def createThread(self,apiToken):
        url = 'https://api.openai.com/v1/threads'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}'
        }

        response = requests.post(url,headers=headers)
        return response.json
    
    def sendMessageThread(self,apiToken,threadID,message):
        url = f'https://api.openai.com/v1/threads/{threadID}/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}'
        }

        data = {
        "role": "user",
        "content": f"{message}"
        }

        response = requests.post(url,headers=headers,json=data)
        return response.json

    def runThread(self,apiToken,threadID,assistant_ID):
        url = f'https://api.openai.com/v1/threads/{threadID}/runs'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}'
        }

        data={"assistant_id": f"{assistant_ID}"}

        response = requests.post(url,headers=headers,json=data)
        return response.json
    


    def checkRunStatus(self,apiToken,threadID,runID):
        url = f'https://api.openai.com/v1/threads/{threadID}/runs/{runID}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}'
        }
        response = requests.post(url,headers=headers)
        return response.json
    


    def retriveMessage(self,apiToken,threadID):
        url = f'https://api.openai.com/v1/threads/{threadID}/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiToken}'
        }


        response = requests.get(url,headers=headers)
        return response.data[0].content[0].text.value