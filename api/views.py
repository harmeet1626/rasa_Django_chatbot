# yourappname/views.py
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response 
import requests, json, secrets, string, random
from api.models import Tickets, Chatroom, Chats
from decouple import config
from api.serializers import *
from api.pagination import paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token






def generate_random_alphanumeric_string(length):
        alphanumeric_characters = string.ascii_letters + string.digits
        return "T-"+''.join(secrets.choice(alphanumeric_characters) for _ in range(length))


class index(APIView):
    authentication_classes =[SessionAuthentication,]
    permission_classes = [IsAuthenticated,]
    login_url = ""

    def get(self,request):
        token = Token.objects.get_or_create(user=request.user)
        return render(request, 'sampleIndex.html',{"token":token[0].key})




class Login(APIView):
    def get(self,request):
        return render(request,"login.html")
    
    def post(self,request):
        username,password = request.data["username"],request.data["password"]
        data = {"username":username,"password":password}
        existing_user = request.data["existing_user"]
        print(existing_user)
        if existing_user == 'True':
            user = authenticate(self, username=username, password=password)
            print(user,"is authenticated")
            if not user:
                data['error_message'] = "User not authenticated"
                return render(request,"login.html",{"data":data})   
        else:
            if not  User.objects.filter(username = username):
                user = User.objects.create_user(username = username,password = password)
            else:
                data['error_message'] = "User already exists"
                return render(request,"login.html",{"data":data})   
        login(request, user)
        print("getting token",user)
        token = Token.objects.get_or_create(user=user)
        print("got token")
        return redirect('/index')  




class Chatbot(APIView):
    authentication_classes =[TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    login_url = ""

    def get_headers(self):
        headers = {"Content-Type": "application/json"}
        return headers

    def post(self,request):
        try:
            status,message,response_array=200,"Success",[]
            user=request.user
            data = request.data
            if request.data["type"]=="buttons":
                user_message = data["payload"]["title"]
                chatbot_data = {
                    "message" :data["payload"]["payload"],
                    "sender": user.id,
                }
            else:
                print("in the else part")
                user_message = data["message"]
                chatbot_data = {
                    "message" :data['message'],
                    "sender": user.id,
                }
            print("request data=========>",request.data)
            chatroom= Chatroom.objects.get_or_create(user=user)[0]
            chat = Chats.objects.create(chatroom = chatroom)
            print("user_message=============>",user_message)
            if 'help_me' in user_message.lower():
                response_array = [{"text":"You can ask me about categories, products, or anything else. Feel free to explore!"}]
            elif 'raise_ticket-' in user_message.lower():
                ticket_number = generate_random_alphanumeric_string(5)
                response_array = [{"text":f'Thankyou for sharing your problem, We have created a ticket for your issue. Please note down the ticket number {ticket_number} '},{"text":"Do you want to share any related documents?"}]
                user_message =user_message.replace("raise_ticket-","")
                chat.question = user_message
                Tickets.objects.create(ext_id=ticket_number,document="", chat_id = chat.id,status ="Initiated",text=user_message)
            elif 'track_ticket-' in user_message.lower():
                ext_id = user_message.lower().replace("track_ticket-","")
                try:
                    ticket_details = get_object_or_404(Tickets,ext_id=ext_id)
                    response_array = [{"text":f'Current status of your ticket {ext_id} is marked as "{ticket_details.status}"'}]
                except:
                    response_array = [{"text":f'Sorry, We were not able to fetch the details of this ticket. Please enter the correct ticket number'}]
                user_message =user_message.replace("track_ticket-","")
                chat.question = user_message
                
            else:
                url =  config('RASA_URL')

               

                chatbot_response = requests.post(url,data=json.dumps(chatbot_data),headers=self.get_headers())
                print("chatbot_response======================>",chatbot_response)
                if chatbot_response.status_code == 200 :
                    chatbot_response = json.loads(chatbot_response.content)
                    print(chatbot_response,"-=------------")
                    response_array = chatbot_response
                    if response_array ==[]:
                        response_array =[{"text":"I'm sorry. I dont have the answer to that."}]
                    if not response_array[0].get('text'):
                        response_array[0]['text']='Select an order for refund'

                    # return Response({"status":200, "response":response_array})
                else:
                    status = 400
                    message ="Rasa Error"
                chat.question = user_message
            
            chat.response = response_array[0]["text"]
            chat.save()
            try:
                for i in range(1,len(response_array)):
                    Chats.objects.create(chatroom = chatroom,response=response_array[i]["text"])
            except:
                pass
            print("final_response")
            return Response({"status":status,"message":message,"response":response_array})
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "message":str(E)})


class UploadDocumentTicket(UpdateAPIView):
    authentication_classes =[TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    queryset = Tickets.objects.all()
    serializer_class = UploadDocumentsSerializer
    def put(self, request):
        try:
            print(request.data,"==========")
            print(request.FILES,"=========")
            ticket_obj = Tickets.objects.filter(chat__chatroom__user_id = request.user).last()
            if not ticket_obj:
                return Response({"status":400, "error":"Ticket doesn't exist"})
            serializer = UploadDocumentsSerializer(ticket_obj,request.data)
            if serializer.is_valid():
                print("serializer is validated")
                serializer.save()
                print("serializer  saved")
                Chats.objects.create(chatroom=ticket_obj.chat.chatroom, document = serializer.data["document"],type = "file")
                response_array = [{"text":"Your Document has uploaded Successfully"}]
            else:
                return Response({"status":400, "error":serializer.errors})
            return Response({"status":200,"response":response_array,"document":serializer.data["document"]})
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "error":str(E)})

    
class ChatsListing(ListAPIView):
    queryset = Chats.objects.all()
    serializer_class = ChatsListingSerializer
    pagination_class = paginator
    authentication_classes =[TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        try:
            chats = Chats.objects.filter(chatroom__user = self.request.user).order_by("-id")
            return chats
        except Exception as E:
            print("internal server error===",str(E))
            return Response({"status":500, "error":str(E)})
        






