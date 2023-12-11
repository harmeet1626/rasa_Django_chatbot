# yourappname/views.py
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response 
import requests, json, secrets, string, random
from rasa_chat_app.models import Tickets, Chatroom, Chats
from decouple import config
from rasa_chat_app.serializers import *
from rasa_chat_app.pagination import paginator


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
            user=1
            chatroom= Chatroom.objects.get_or_create(user=user)[0]
            chat = Chats.objects.create(chatroom = chatroom, question = user_message)

            if 'help_me' in user_message.lower():
                response_array = [{"text":"You can ask me about categories, products, or anything else. Feel free to explore!"}]
                status=200
                message="Success"

            elif 'raise_ticket' in user_message.lower() and '-'  in user_message.lower():
                ticket_number = generate_random_alphanumeric_string(5)
                response_array = [{"text":f'Thankyou for sharing your problem, We have created a ticket for your issue. Please note down the ticket number T-{ticket_number} \n Do you want to share any related documents?'}]
                Tickets.objects.create(ext_id=ticket_number,document="", chat_id = chat.id,status ="Initiated")
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
            chat.response = response_array[0]["text"]
            return Response({"status":status,"message":message,"response":response_array})
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "message":str(E)})


class UploadDocumentTicket(UpdateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = UploadDocumentsSerializer
    def put(self, request):
        try:
            ext_id = request.data["ext_id"]
            # ticket_obj = Tickets.objects.filter(ext_id = ext_id).last()
            ticket_obj = Tickets.objects.filter(chat__chatroom__user_id = 1).last()

            print("ticket_obj =", ticket_obj)
            serializer = UploadDocumentsSerializer(ticket_obj,request.data)
            if serializer.is_valid():
                serializer.save()
                response_array = [{"text":"Your Document has uploaded Successfully"}]
                print(serializer.data)
            else:
                return Response({"status":500, "error":serializer.errors})
            return Response({"status":200,"response":response_array,"document":serializer.data["document"]})
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "error":str(E)})

    
class ChatsListing(ListAPIView):
    queryset = Chats.objects.all()
    serializer_class = ChatsListingSerializer
    pagination_class = paginator

    def get_queryset(self):
        try:
            chats = Chats.objects.filter(chatroom__user = 1).order_by("-id")
            return chats
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "error":str(E)})






