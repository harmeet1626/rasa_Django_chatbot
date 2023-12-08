# yourappname/views.py
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
import requests, json, secrets, string, random
from rasa_chat_app.models import Tickets, Chatroom
from decouple import config


def generate_random_alphanumeric_string(length):
        alphanumeric_characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphanumeric_characters) for _ in range(length))


def index(request):
    return render(request, 'sampleIndex.html')
    # return render(request, 'index.html')


class Chatbot(APIView):

    def get_headers(self):
        headers = {"Content-Type": "application/json"}
        return headers
    

    def post(self,request):
        try:
            status,message,response_array=200,"",[]
            user_message = request.data["message"]
            print(user_message)
            chatroom = Chatroom.objects.filter(user=request.user.id).first()
            
            if 'help_me' in user_message.lower():
                response_array = [{"text":"You can ask me about categories, products, or anything else. Feel free to explore!"}]
                status=200
                message="Success"

            elif 'raise_ticket' in user_message.lower() and '-'  in user_message.lower():
                ticket_number = generate_random_alphanumeric_string(5)
                response_array = [{"text":f'Thankyou for sharing your problem, We have created a ticket for your issue. Please note down the ticket number T-{ticket_number} \n Do you want to share any related documents?'}]
                Tickets.objects.create(ext_id=ticket_number,document_url="", chatroom_id=1,status ="Initiated")
                status=200
                message="Success"
    
    
            else:
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
                    status=200
                    # return Response({"status":200, "response":response_array})
                else:
                    print("chatbot_response.content",chatbot_response.content)
                    status = 400
                    message ="Rasa Error"

            return Response({"status":status,"message":message,"response":response_array})
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "message":str(E)})



