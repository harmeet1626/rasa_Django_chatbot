# yourappname/views.py
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
import requests, json
from decouple import config




def index(request):
    return render(request, 'index.html')


class Chatbot(APIView):

    def get_headers(self):
        headers = {"Content-Type": "application/json"}
        return headers

    def post(self,request):
        try:
            url =  config('RASA_URL')
            data = request.data
            chatbot_data = {
                "message" :data['message'],
                "sender": "Ranjeet",
            }
            chatbot_response = requests.post(url,data=json.dumps(chatbot_data),headers=self.get_headers())
            if chatbot_response.status_code == 200 :
                chatbot_response = json.loads(chatbot_response.content)
                response_array = chatbot_response
                print("response:================>", response_array)
                if response_array ==[]:
                    response_array =[{"text":"I'm sorry. I dont have the answer to that."}]
                return Response({"status":200, "response":response_array})
            else:
                print("chatbot_response.content",chatbot_response.content)
                return Response({"status":400, "message":"Something went wrong"})
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "message":str(E)})



