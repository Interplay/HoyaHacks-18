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
def check_bal(idn):
    os.system('sh accounts+'idn'+.sh > output.json')
    data = json.load(open('output.json'))
    return ('your current available balance is: ' + say_money(data['account_balances'][0]['available']))

# most recent transaction
def most_recent_transaction(idn):
    os.system('sh transactions+'idn'+.sh > output.json')
    data = json.load(open('output.json'))
    val = data['transactions'][0]['amount']
    
    return ('Your most recent transaction was: ' + say_money(val))

# how much did i spend total
def total_yr_spend_value(idn):
    os.system('sh transactions+'idn'+.sh > output.json')
    data = json.load(open('output.json'))
    arr = data['transactions']
    total = 0
    for x in arr:
        total = total + x['amount']
    print('Your total spending over the last year was: ' + say_money(total))
    return total

def total_yr_spend(idn):
    os.system('sh transactions'+idn+'.sh > output.json')
    data = json.load(open('output.json'))
    arr = data['transactions']
    total = 0
    for x in arr:
        total = total + x['amount']
    return ('Your total spending over the last year was: ' + say_money(total))


# how much did i spend last week
def week_spend(idn):
    os.system('sh transactions+'idn'+.sh > output.json')
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
    past_year = total_yr_spend_value()

    ret_str = ret_str + ('The percentage from the past two weeks is ' + str(round(past_two*100/past_year, 2)) + ' percent of your spending over the past year')

    return ret_str



@ask.launch
def launch():
    speech_text = 'Welcome to EchoDog, your loyal fincancial companion.'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

# ELLEN's
#
#
@ask.intent('BiWeeklyPercentage')
def BiWeekPercent():
    speech_text = week_spend(1) + 'That is pretty good, keep it up'
    return statement(speech_text).simple_card('BiWeeklyPercentage', speech_text)

@ask.intent('YearTotal')
def year_total():
    speech_text = total_yr_spend(1) + 'That is a lot of money.'
    return statement(speech_text).simple_card('YearTotal', speech_text)

@ask.intent('CheckBalance')
def chk_bal():
    speech_text = check_bal(1) + ' You are doing pretty well for yourself'
    return statement(speech_text).simple_card('CheckBalance', speech_text)

@ask.intent('MostRecent')
def most_recent():
    speech_text = most_recent_transaction(1) 
    return statement(speech_text).simple_card('MostRecent', speech_text)

# JACOB's
#
#
@ask.intent('BiWeeklyPercentage2')
def BiWeekPercent2():
    speech_text = week_spend(2)
    return statement(speech_text).simple_card('BiWeeklyPercentage', speech_text)

@ask.intent('YearTotal2')
def year_total2():
    speech_text = total_yr_spend(2)
    return statement(speech_text).simple_card('YearTotal', speech_text)

@ask.intent('CheckBalance2')
def chk_bal2():
    speech_text = check_bal(2)
    return statement(speech_text).simple_card('CheckBalance', speech_text)

@ask.intent('MostRecent2')
def most_recent2():
    speech_text = most_recent_transaction(2)
    return statement(speech_text).simple_card('MostRecent', speech_text)


# MIKE
#
#
@ask.intent('BiWeeklyPercentage3')
def BiWeekPercent3():
    speech_text = 'The percentage over the past two weeks that you have' 
                  'spent is 50 percent of your spending over the past year'
                  'Boy you need to save more and stop being so yolo swag. Dabs'
    return statement(speech_text).simple_card('BiWeeklyPercentage', speech_text)

@ask.intent('YearTotal3')
def year_total3():
    speech_text = 'You did alright this year but you could use a while lot of improvement. Your killing me Mike'
    return statement(speech_text).simple_card('YearTotal', speech_text)

@ask.intent('CheckBalance3')
def chk_bal():
    speech_text = 'I am not sure if you want to know your balance, but you have 5 dollars and 37 cents in your account,'
    return statement(speech_text).simple_card('CheckBalance', speech_text)

@ask.intent('MostRecent3')
def most_recent():
    speech_text = 'You spent 50 dollars on garlic bread maybe you need to rethink your life choices'
    return statement(speech_text).simple_card('MostRecent', speech_text)




############################

@ask.intent('Unhandled')
def unhandled():
    unhandled_response="Sorry, I did not understand that command. Say help for assitance"
    return question().reprompt(unhandled_response)

@ask.intent('HelpFunc')
def help_func():
    helplist="You are able to ask for most recent transaction, check your balance, spending stats for two weeks, and weekly total spending"
    return question(helplist).simple_card('HelpFunc', helplist)

@ask.intent('AMAZON.HelpIntent')
def help():
    unhandled_response="Sorry, I did not understand that command. Say help for assitance."
    return question().reprompt(unhandled_response)


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
