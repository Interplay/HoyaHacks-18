import logging
import os
import json
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import datetime as DT

os.system('sh transactions.sh > output.json')
data = json.load(open('output.json'))

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# function that converts the amount of money to an string
# that can be said
def say_money(value):
    neg = ''
    startv = 0
    if value < 0:
        neg = 'negative'
        startv = startv + 1
    value = str(value)
    cents = value[-2:]
    if cents == '.0':
        cents = '0'
    dollars = value[startv:-2]
    return neg + ' ' + dollars + ' dollars and ' + cents + ' cents'


# check balance
def check_bal():
    os.system('sh accounts.sh > output.json')
    data = json.load(open('output.json'))
    print('your current available balance is: ' + str(data['account_balances'][0]['available']))

# most recent transaction
def most_recent_transaction():
    os.system('sh transactions.sh > output.json')
    data = json.load(open('output.json'))
    val = data['transactions'][0]['amount']
    
    print('Your most recent transaction was: ' + say_money(val))

# how much did i spend total
def total_yr_spend():
    os.system('sh transactions.sh > output.json')
    data = json.load(open('output.json'))
    arr = data['transactions']
    total = 0
    for x in arr:
        total = total + x['amount']
    print('Your total spending over the last year was: ' + say_money(total))
    return total


# how much did i spend last week
def week_spend():
    os.system('sh transactions.sh > output.json')
    data = json.load(open('output.json'))
    total = 0
    today = DT.date.today()
    week_ago = today - DT.timedelta(days=14)
    arr = data['transactions']
    for x in arr:
        strdate = str(x['settled_at'])
        strdate = strdate[0:10]
        print(strdate)
        curr_day = DT.datetime.strptime(strdate, '%Y-%m-%d').date()
        if curr_day >= week_ago:
            total = total + x['amount']

    ret_str = ''
    ret_str = ret_str + ('Your total spending over the past two weeks was: ' + say_money(total) + '. ')

    past_two = total
    past_year = total_yr_spend()

    ret_str = ret_str + ('The percentage of total transactions is ' + str(round(past_two*100/past_year, 2)) + ' percent')

    return ret_str



@ask.launch
def launch():
    speech_text = 'suh dude'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('HelloWorldIntent')
def hello_world():
    speech_text = week_spend()
    return statement(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = week_spend()
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)


# how much did i spend last week
# how much did i spend last week compared to the entire