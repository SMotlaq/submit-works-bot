import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import jdatetime
import myDateTime as mdt
import DataBase as db
import signal
import messages as ms
import buttons as bt
import tokens
import os

my_token = tokens.my_token

myPath     = os.getcwd()
database   = os.path.join(myPath, "DB.db")
conn       = db.create_connection(database)

log_chan   = -1001391934746
salman     = 95374546
bot        = telegram.Bot(token=my_token)
updater    = Updater(my_token)
db.create_table(conn)

#----------------------- FSM FUNCTIONS -----------------------#

def _start_timer(inCome_uid):
    try:
        with conn:
            NewTime_RowNumber = db.add_times(conn, inCome_uid, start_time = str(jdatetime.datetime.now()))
            db.edit_user(conn, inCome_uid, state = 'working', has_open_time_range = '1', last_time_row = str(NewTime_RowNumber))
        send_text(inCome_uid, ms.timer_started, keyboard = bt.working)
    except Exception as e:
        pritn('error in _start_timer()')
        print(e)

def _cheghadr_shod(inCome_uid):
    try:
        with conn:
            all_times = db.query_user_times(conn, inCome_uid)
            if all_times==[0]:
                db.edit_user(conn, inCome_uid, state = 'home')
                send_text(inCome_uid, ms.no_work_yet, keyboard = bt.home)
            else:
                db.edit_user(conn, inCome_uid, state = 'enter_period')
                send_text(inCome_uid, ms.enter_period, keyboard = bt.time_domain)
    except Exception as e:
        pritn('error in _cheghadr_shod()')
        print(e)

def _working_done(inCome_uid):
    try:
        with conn:
            LastTime_RowNumber = int(db.query_user(conn, inCome_uid)[6]) #last_time_row
            start_time = db.query_time(conn, LastTime_RowNumber)[2]    #start_time
            converted_start_time = mdt.str2dt(start_time)
            stop_time  = str(jdatetime.datetime.now())
            converted_stop_time = mdt.str2dt(stop_time)
            section_length = (converted_stop_time - converted_start_time).total_seconds()
            db.edit_user(conn, inCome_uid, state = 'home', has_open_time_range = '0')
            db.edit_times_byID(conn, LastTime_RowNumber, inCome_uid, stop_time, str(int(section_length)))
        send_text(inCome_uid, ms.timer_stoped.replace('%', str(int(section_length/60))), keyboard = bt.home)
    except Exception as e:
        pritn('error in _working_done()')
        print(e)

def _today(inCome_uid):
    try:
        with conn:
            all_times = db.query_user_times(conn, inCome_uid)
            sum_of_today = 0
            for _time in all_times:
                stop_time  = _time[1]
                sum_of_row = _time[2]
                if mdt.isInToday(stop_time)==1:
                    sum_of_today = sum_of_today + int(sum_of_row)
            db.edit_user(conn, inCome_uid, state = 'enter_period')
        total_minutes = int((sum_of_today%3600)/60)
        total_hours   = int(sum_of_today/3600)
        if sum_of_today<60:
            send_text(inCome_uid, ms.no_today, keyboard = bt.time_domain)
        else:
            if total_hours==0:
                send_text(inCome_uid, ms.today_all_onlyMinute.replace('%', str(total_minutes)), keyboard = bt.time_domain)
            else:
                if total_minutes==0:
                    send_text(inCome_uid, ms.today_all_noMinute.replace('%', str(total_hours)), keyboard = bt.time_domain)
                else:
                    send_text(inCome_uid, ms.today_all_withMinute.replace('%', str(total_hours)).replace('$', str(total_minutes)), keyboard = bt.time_domain)
    except Exception as e:
        pritn('error in _today()')
        print(e)

def _this_month(inCome_uid):
    try:
        with conn:
            all_times = db.query_user_times(conn, inCome_uid)
            sum_of_this_month = 0
            for _time in all_times:
                stop_time  = _time[1]
                sum_of_row = _time[2]
                if mdt.isInThisMonth(stop_time)==1:
                    sum_of_this_month = sum_of_this_month + int(sum_of_row)
            db.edit_user(conn, inCome_uid, state = 'enter_period')
        total_minutes = int((sum_of_this_month%3600)/60)
        total_hours   = int(sum_of_this_month/3600)
        if sum_of_this_month<60:
            send_text(inCome_uid, ms.no_this_month, keyboard = bt.time_domain)
        else:
            if total_hours==0:
                send_text(inCome_uid, ms.month_all_onlyMinute.replace('%', str(total_minutes)), keyboard = bt.time_domain)
            else:
                if total_minutes==0:
                    send_text(inCome_uid, ms.month_all_noMinute.replace('%', str(total_hours)), keyboard = bt.time_domain)
                else:
                    send_text(inCome_uid, ms.month_all_withMinute.replace('%', str(total_hours)).replace('$', str(total_minutes)), keyboard = bt.time_domain)
    except Exception as e:
        pritn('error in _this_month()')
        print(e)

def _back_to_home(inCome_uid):
    try:
        with conn:
            db.edit_user(conn, inCome_uid, state = 'home')
        send_text(inCome_uid, ms.what_to_do, keyboard = bt.home)
    except Exception as e:
        pritn('error in _back_to_home()')
        print(e)

FSM_Array = {
            'home'          : { bt.home[0][1]: _start_timer,
                                bt.home[0][0]: _cheghadr_shod },

            'working'       : { bt.working[0][0]: _working_done },

            'enter_period'  : { bt.time_domain[0][0]: _today,
                                bt.time_domain[0][1]: _this_month,
                                bt.time_domain[1][0]: _back_to_home }
            }

def FSM_handler(bot, update):
    inCome_uid, inCome_name, inCome_user_id = exctract_info(update.message.from_user)
    input_message = update.message.text
    with conn:
        query_result = db.query_user(conn, inCome_uid)
    if query_result!=0 and query_result!='Fail':
        with conn:
            db.edit_user(conn, inCome_uid, name = inCome_name, user_id = inCome_user_id)
            current_state = db.query_user(conn, inCome_uid)[4]
        try:
            FSM_Array[current_state][input_message](inCome_uid)
        except Exception as e:
            pritn('error in FSM_handler()')
            print(e)
    else:
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id = int(inCome_uid),text = ms.hit_start, reply_markup=reply_markup)

def start(bot, update, args):
    inCome_uid, inCome_name, inCome_user_id = exctract_info(update.message.from_user)
    with conn:
        isThere = db.query_user(conn, inCome_uid)
        if isThere==0:
            db.add_user(conn, inCome_uid, inCome_name, inCome_user_id, 'home')
            if inCome_user_id=='None':
                inCome_user_id = '[NO USER ID]'
            else:
                inCome_user_id = '@' + inCome_user_id
            send_text(log_chan, ms.new_member_log + '\n' + inCome_user_id + '\n' + inCome_name + '\n#uid_' + inCome_uid)
        else:
            db.edit_user(conn, inCome_uid, name = inCome_name, user_id = inCome_user_id)
    send_text(int(inCome_uid),ms.start,keyboard=bt.home)

#----------------------- OTHER FUNCTIONS -----------------------#

def exctract_info(chat_id):
    inCome_uid = str(chat_id['id'])
    inCome_user_id = chat_id['username']
    if inCome_user_id==None:
        inCome_user_id='None'
    first_name = chat_id['first_name']
    last_name = chat_id['last_name']
    if first_name==None:
        first_name = ''
    if last_name==None:
        last_name = ''
    else:
        last_name = ' ' + last_name
    inCome_name = first_name + last_name
    return inCome_uid, inCome_name, inCome_user_id
def send_photo(uid,msg,adrs):
    try:
        bot.sendChatAction(uid, 'UPLOAD_PHOTO')
        bot.sendPhoto(chat_id=uid, photo=open(adrs, 'rb'), caption=msg)
    except Exception as e:
        print(e)
def send_text(uid, msg, keyboard=None):
    try:
        #bot.sendChatAction(uid, 'TYPING')
        if keyboard==None:
            bot.send_message(chat_id=uid, text=msg)
        else:
            reply_markup = telegram.ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
            bot.send_message(chat_id=uid, text=msg, reply_markup=reply_markup)
    except Exception as e:
        pritn('error in sen_text()')
        print(e)
def send2all(payam):
    with conn:
        users = db.query_all_users(conn)
    if users!=[]:
        for user in users:
            send_text(int(user[0]),payam[user[1]])
def send2all_pic(payam):
    with conn:
        users = db.query_all_users(conn)
    if users!=[]:
        for user in users:
            try:
                bot.sendPhoto(chat_id=int(user[0]), photo=open('nor1.jpg', 'rb'), caption=payam)
            except:
                print("No chat with " + user[2])
def keyboard_handler(keyboard_buttons):
    return telegram.ReplyKeyboardMarkup(keyboard_buttons,resize_keyboard=True)
def handler(signum, frame):
    print('idle point')
    updater.idle()

#----------------------- EVENT HANDLERS -----------------------#

signal.signal(signal.SIGINT, handler)
start_command = CommandHandler('start', start, pass_args=True)
updater.dispatcher.add_handler(start_command)
state_handler = MessageHandler(Filters.text & (~Filters.command), FSM_handler)
updater.dispatcher.add_handler(state_handler)
updater.start_polling()

#send2all(ms.repair)
#send2all(ms.ready)
#send2all(ms.temp_message)

#send_text(salman, 'Bot started')
send_text(log_chan, 'Bot started')

# send2all_pic(ms.nowruz)
#
# print("DONE")
#
# while True:
#     pass

while True:
    clear = lambda: os.system('cls')
    clear()

    print('Submit')
    time.sleep(3)
    print('Works')
    time.sleep(3)
    print('is UP!')
    time.sleep(3)
