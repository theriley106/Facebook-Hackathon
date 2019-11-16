from flask import Flask, request, Response
import requests, json, random, os
try:
	from keys import *
	verify_token = FB_VERIFY_TOKEN
	access_token = FB_ACCESS_TOKEN
	account_sid = TWILIO_ID
	auth_token = TWILIO_AUTH
except:
	verify_token = os.getenv('VERIFY_TOKEN', None)
	access_token = os.getenv('ACCESS_TOKEN', None)
	account_sid = os.getenv('TWILIO_ID', None)
	auth_token = os.getenv('TWILIO_AUTH', None)

from flask import Flask, request, redirect
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import re

app = Flask(__name__)

def cleanNumber(number):
	return "+1" + ''.join(re.findall("\d+", number.replace("+1", "")))

def send_sms(number, body):
	client = Client(account_sid, auth_token)

	message = client.messages.create(
      body=body,
      from_='+12054311920',
      to=cleanNumber(number)
  )

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
	number = request.form['From']
	message_body = request.form['Body']

	resp = MessagingResponse()
	response_message = 'Hello {}, You said:{}'.format(number, message_body)
	resp.message(response_message)

	return str(resp)

@app.route('/webhook', methods=['GET'])
def webhook_verify():
	if request.args.get('hub.verify_token') == verify_token:
		return request.args.get('hub.challenge')
	return "Wrong verify token"

@app.route('/webhook', methods=['POST'])
def webhook_action():
	data = json.loads(request.data.decode('utf-8'))
	for entry in data['entry']:
		user_message = entry['messaging'][0]['message']['text']
		send_sms('8645674106', user_message)
		user_id = entry['messaging'][0]['sender']['id']
		response = {
			'recipient': {'id': user_id},
			'message': {}
		}
		response['message']['text'] = handle_message(user_id, user_message)
		r = requests.post(
			'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
	return Response(response="EVENT RECEIVED",status=200)

@app.route('/webhook_dev', methods=['POST'])
def webhook_dev():
	# custom route for local development
	data = json.loads(request.data.decode('utf-8'))
	user_message = data['entry'][0]['messaging'][0]['message']['text']
	user_id = data['entry'][0]['messaging'][0]['sender']['id']
	response = {
		'recipient': {'id': user_id},
		'message': {'text': handle_message(user_id, user_message)}
	}
	return Response(
		response=json.dumps(response),
		status=200,
		mimetype='application/json'
	)

def handle_message(user_id, user_message):
	return "Hello "+user_id+" ! You just sent me : " + user_message

@app.route('/privacy', methods=['GET'])
def privacy():
	# needed route if you need to make your bot public
	return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."

@app.route('/', methods=['GET'])
def index():
	return "Hello there, I'm a facebook messenger bot."

if __name__ == '__main__':
	send_sms("", "")
	app.run(debug=True, host='0.0.0.0')
