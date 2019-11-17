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
	FB_RECIPIENT = os.getenv('FB_RECIPIENT', None)

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

def encode_text(string):
	return string
	return string.encode('ascii').encode('zlib_codec')

def decode_text(zlibText):
	return zlibText
	return zlibText.decode('zlib_codec').decode('ascii')

# def process_everything

# This is the route belonging to FB that encodes the text string
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
	number = request.form['From']
	message_body = request.form['Body']
	textBody = {'n': number, 'b': message_body}
	textBody['t'] = 'm'
	# This shortens the text string
	text_string = encode_text(json.dumps(textBody))
	print("Sending: {}".format(text_string))
	send_sms("8706399053", text_string)
	print("Sent encoded text string to another twilio number")

# This is the route belonging to FB that decodes the text string
# This route determines if the message should be sent to messenger or text
@app.route("/smsRoute2", methods=['GET', 'POST'])
def sms_reply2():
	number = request.form['From']
	message_body = json.load(request.form['Body'])
	# This specifies where the message is posted


def process_message(message_body):
	if message_body.get('t') == 'm':
		# M means the message is intented for fb messenger
		print(request.form)
		print("Trying to decode ^")
		message_body = gen_fb_message(decode_text(message_body))
		r = requests.post(
				'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=message_body)
	else:
		send_sms('4153080453', message_body['text'])


@app.route("/smsRoute3", methods=['GET', 'POST'])
def sms_reply3():
	number = request.form['From']
	message_body = request.form['Body']
	message_body = gen_fb_message(message_body)
	r = requests.post(
			'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=message_body)
	# This is sendign the message via messenger
	print("SENDING MESSAGE")

def gen_fb_message(text):
	return {'message': {'text': text}, 'recipient': {'id': FB_RECIPIENT}}

@app.route('/webhook', methods=['GET'])
def webhook_verify():
	if request.args.get('hub.verify_token') == verify_token:
		return request.args.get('hub.challenge')
	return "Wrong verify token"

@app.route('/webhook', methods=['POST'])
def webhook_action():
	data = json.loads(request.data.decode('utf-8'))
	for entry in data['entry']:
		user_message = entry['messaging'][0]['message']
		process_message(user_message)
		
		'''
								user_id = entry['messaging'][0]['sender']['id']
								response = {
									'recipient': {'id': user_id},
									'message': {}
								}
								response['message']['text'] = handle_message(user_id, user_message)
								r = requests.post(
									'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
								print("URL + {}".format('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token))
								print(response)'''
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
	# send_sms("", "")
	app.run(debug=True, host='0.0.0.0')
