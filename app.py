from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import random

app = Flask(__name__)


@app.route("/")
def hello():
    return "Testing of Twilio WhatsApp Bot is going on. Please come back later!"


@app.route("/sms", methods=["POST"])
def sms_reply():

    # Fetch details of the user
    ph_no = request.form.get("From")

    conn = sqlite3.connect('customers.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, number VARCHAR)')
    cur.execute('SELECT number FROM contacts WHERE number=(?)', (ph_no,))
    number_exist = cur.fetchall()
    if not number_exist:
        cur.execute('INSERT INTO contacts (number) values (?)', (ph_no,))
    conn.commit()
    conn.close()

    # Fetch the message sent by the user
    msg_in = request.form.get("Body").lower()

    # # INTELLIGENT BOT # #
    # # Reply to the message
    responded = False
    msg_out = MessagingResponse()
    if 'hello' in msg_in:
        # msg_out.message("Hello to you too. How are you?")
        msg_out.message().body("Hello to you too. How are you?")
        responded = True
    if 'random number' in msg_in:
        # we can't use 'elif' here since it only checks if first condition isn't satisfied
        msg_out.message().body("A random number for you is " + str(random.randint(0, 100)) + ".")
        msg_out.message().media('https://bit.ly/3hf3oEx')
        responded = True
    if not responded:
        msg_out.message().body("You have asked me to do something which is beyond my capabilities at the moment.")

    # # ECHO BOT # #
    # # Reply to the message
    # msg_out = MessagingResponse()
    # msg_out.message().body("You said: {}".format(msg_in))

    return str(msg_out)


if __name__ == "__main__":
    app.run(debug=True)
