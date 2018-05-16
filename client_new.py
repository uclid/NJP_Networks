##Client

import socket
import sys
import json

#vars
connected = False
state = 0
SM_NEW_GAME = {}
player_id = 0

#connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost',8888))
connected = True
#subscribing state
print('Network Jeopardy Game')
name = input('Your name: ')
CM_SUBSCRIBE = {'name': name}
message = json.dumps(CM_SUBSCRIBE)
client_socket.send(message.encode())

while connected == True:
    if(state == 0):#game in progress
        #wait for server commands to do things, now we will just display things
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        SM_NEW_GAME = cmd
        
        player_id = (SM_NEW_GAME['player_names']).index(name) + 1 
        print ('Your Player ID is {}'.format(player_id))

        state = 1
    elif(state == 1):#round in progress
        #wait for server commands to do things, now we will just display things
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        print("The available categories are {}".format(SM_NEW_GAME["categories"]))
        print("Each categories have {} questions".format(SM_NEW_GAME["ques_in_categories"]))
        if(cmd["selected_player"] == player_id):
            print("You are selected!!")
            category = int(input('Please select a category (0,1,2..) in order they are displayed: '))
            SM_CATEGORY = {'player_id': player_id,'category': category}
            message = json.dumps(SM_CATEGORY)
            client_socket.send(message.encode())            
        else:
            print("Player {} is selecting a category...".format(cmd["selected_player"]))
        state = 2
    elif(state == 2): #select category
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        print("Category selected is {}.".format(SM_NEW_GAME["categories"][cmd["category"]]))
        state = 3
    elif(state == 3): #display question and ring
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        print("Your question is {}.".format([cmd["question"]]))
        ring = int(input("Please press 1 and enter to ring..."))
        if(ring == 1):
            SM_RING = {'ring_player_id': player_id}
            message = json.dumps(SM_RING)
            client_socket.send(message.encode())
        else:
            print("Wrong buzzer press, you missed out")
        state = 4
    elif(state == 4):
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        if('player_id' in cmd.keys()):
            if(cmd["player_id"] == player_id):
                print("You can answer!!")
                category = input('Please enter your answer: ')
                #SM_CATEGORY = {'player_id': player_id,'category': category}
                #message = json.dumps(SM_CATEGORY)
                #client_socket.send(message.encode())            
            else:
                print("Player {} is answering...".format(cmd["player_id"]))
                xyz = input("answering...")
        elif('timeout' in cmd.keys()):
            print("Timeout, you cannot answer anymore!")
        state = 5
