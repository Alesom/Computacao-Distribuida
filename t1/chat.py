from bottle import run, get, post, view, request, redirect, route
import json
from threading import Thread
import requests
import time
from urllib3.exceptions import MaxRetryError
import sys


messages = set([("Nobody", "Hello!")])
nick = "Nobody"
PS = set( ['localhost:8080', 'localhost:8081', 'localhost:8082'])

@get('/')
@view('index')
def index():
    return {'messages': messages, 'nick': nick}

@route('/<nick>')
@view('index')
def index(nick='Nobody'):
    return {'messages': messages, 'nick': nick}

@post('/send')
def sendMessage():
	nick = ""
	m = request.forms.get('message')
	n = request.forms.get('nick')
	messages.add((n, m))

	nick = n
	redirect('/'+nick)


@get('/peers')# get peers retorna a quem pedir a lista de conhecidos em formato json
def getPeers(): 
	jason_data=json.dumps(list(PS))
	return jason_data

def getPeersFrom(host):
	link = "http://"+ host + "/peers"
	try:
		r = requests.get(link)
		if r.status_code == 200:
			obj=json.loads(r.text)
			#print(host + " oi "+ str(set(obj)))
			return set(obj)
	except MaxRetryError:
		print ("Conection Error, número maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print ("Conection Error!")

	return set([])


def mainloopP():
	while True:
		time.sleep(1)
		N = set([])
		global PS
		for p in PS:
			PS2 = getPeersFrom(p)
			if PS2.difference(PS):
				N = N.union(PS2.difference(PS))
		PS = PS.union(N)



@get('/messages')# get peers retorna a quem pedir a lista de conhecidos em formato json
def getPeers(): 
	jason_data=json.dumps(list(messages))
	return jason_data

def getMessagesFrom(host):
	link = "http://"+ host + "/messages"
	try:
		r = requests.get(link)
		if r.status_code == 200:
			obj=json.loads(r.text)
			setT = set((a, b) for [a,b] in obj)
				
			#print(host + " MSG "+ str(obj))
			return setT
	except MaxRetryError:
		print ("Conection Error, número maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print ("Conection Error!")

	return set([])


def mainloopM():
	while True:
		time.sleep(1)
		N = set([])
		global messages
		for p in PS:
			MS2 = getMessagesFrom(p)
			if MS2.difference(messages):
				N = N.union(MS2.difference(messages))
		messages = messages.union(N)


thGetPeers=Thread(None, mainloopP, (), {}, None)
thGetPeers.start()
thGetMsgs=Thread(None, mainloopM, (), {}, None)
thGetMsgs.start()


run(host='localhost', port=int(sys.argv[1]))
