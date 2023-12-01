# yourappname/views.py
from django.http import JsonResponse
from django.shortcuts import render
# from rasa.shared.nlu.interpreter import Interpreter
# from rasa.nlu.model import Interpreter

# def chat_with_rasa(request):
#     message = request.GET.get('message', '')
    
#     # Initialize Rasa interpreter
#     interpreter = Interpreter.load("path/to/your/model")

#     # Get Rasa response
#     response = interpreter.parse(message)

#     # Return Rasa response as JSON
#     return JsonResponse(response)
# yourappname/views.py

def index(request):
    return render(request, 'index.html')


