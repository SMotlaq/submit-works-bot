import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import jdatetime
import xlsxwriter
import myDateTime as mdt
import DataBase as db
import signal
import messages as ms
import buttons as bt
import excell_prop as ex
import tokens
import os

my_token = tokens.my_token

myPath     = os.getcwd()
database   = os.path.join(myPath, "DB.db")
report     = os.path.join(myPath, "reports")
conn       = db.create_connection(database)

log_chan   = -1001391934746
salman     = 95374546
milad      = 675104932
bot        = telegram.Bot(token=my_token)
updater    = Updater(my_token)
db.create_table(conn)

#----------------------- FSM FUNCTIONS -----------------------#

def _start_timer(inCome_uid, inCome_name, inCome_user_id):
    try:
        with conn:
            NewTime_RowNumber = db.add_times(conn, inCome_uid, start_time = str(jdatetime.datetime.now()))
            db.edit_user(conn, inCome_uid, state = 'working', has_open_time_range = '1', last_time_row = str(NewTime_RowNumber))
        send_text(inCome_uid, ms.timer_started, keyboard = bt.working)
        send_text(log_chan, ms.new_start.replace('%', '[NO USER ID]' if inCome_user_id=='None' else ('@' + inCome_user_id)))
        if int(inCome_uid)==salman:
            send_text(milad, ms.oomadam)
            send_text(salman, ms.oomadam)
    except Exception as e:
        print('error in _start_timer()')
        print(e)

def _cheghadr_shod(inCome_uid, inCome_name, inCome_user_id):
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
        print('error in _cheghadr_shod()')
        print(e)

def _working_done(inCome_uid, inCome_name, inCome_user_id):
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
        send_text(log_chan, ms.end_of_working.replace('%',  '[NO USER ID]' if inCome_user_id=='None' else ('@' + inCome_user_id)).replace('$', str(int(section_length/60))))
        if int(inCome_uid)==salman:
            send_text(milad, ms.raftam)
            send_text(salman, ms.raftam)
    except Exception as e:
        print('error in _working_done()')
        print(e)

def _today(inCome_uid, inCome_name, inCome_user_id):
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
        print('error in _today()')
        print(e)

def _this_month(inCome_uid, inCome_name, inCome_user_id):
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
        print('error in _this_month()')
        print(e)

def _back_to_home(inCome_uid, inCome_name, inCome_user_id):
    try:
        with conn:
            db.edit_user(conn, inCome_uid, state = 'home')
        send_text(inCome_uid, ms.what_to_do, keyboard = bt.home)
    except Exception as e:
        print('error in _back_to_home()')
        print(e)

def _back_to_enter_period(inCome_uid, inCome_name, inCome_user_id):
    try:
        with conn:
            db.edit_user(conn, inCome_uid, state = 'enter_period')
        send_text(inCome_uid, ms.enter_period, keyboard = bt.time_domain)
    except Exception as e:
        print('error in _back_to_enter_period()')
        print(e)

def _enter_month(inCome_uid, inCome_name, inCome_user_id):
    try:
        with conn:
            db.edit_user(conn, inCome_uid, state = 'enter_month')
        send_text(inCome_uid, ms.which_month, keyboard = bt.monthes)
    except Exception as e:
        print('error in _enter_month()')
        print(e)

def _export_selector_prev(inCome_uid, inCome_name, inCome_user_id):
    __export_excell(inCome_uid, inCome_name, inCome_user_id, previous=True)

def _export_selector_now(inCome_uid, inCome_name, inCome_user_id):
    __export_excell(inCome_uid, inCome_name, inCome_user_id, previous=False)

def __export_excell(inCome_uid, inCome_name, inCome_user_id, previous=False):
    try:
        month_times = (ex.titles,);
        with conn:
            all_times = db.query_user_times(conn, inCome_uid)
            sum_of_this_month = 0
            for _time in all_times:
                start_time  = _time[0]
                stop_time   = _time[1]
                sum_of_row  = _time[2]
                if previous==False:
                    if mdt.isInThisMonth(stop_time)==1:
                        month_times += ([str(int(mdt.get_day(stop_time))),mdt.get_time(start_time),mdt.get_time(stop_time),int(sum_of_row)/3600],)
                else:
                    if mdt.isInPrevMonth(stop_time)==1:
                        month_times += ([str(int(mdt.get_day(stop_time))),mdt.get_time(start_time),mdt.get_time(stop_time),int(sum_of_row)/3600],)

        THIS_YEAR  = mdt.get_this_year()
        THIS_MONTH = mdt.get_this_month()
        if previous==True:
            if THIS_MONTH=='01':
                THIS_MONTH = '12'
                THIS_YEAR = str(int(THIS_YEAR)-1)
            else:
                THIS_MONTH = int(THIS_MONTH)-1
                THIS_MONTH = "%02d"%THIS_MONTH
        THIS_MONTH_NAME = mdt.names[THIS_MONTH]

        file_name = os.path.join(report, THIS_YEAR + '-' + THIS_MONTH + '__' + inCome_uid + ".xlsx")
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        #worksheet.write(1, 1, ex.header, workbook.add_format(ex.header_format))
        worksheet.merge_range(1, 1, 1, 4, ex.header.replace('%',THIS_MONTH_NAME).replace('&',THIS_YEAR), workbook.add_format(ex.header_format))

        # Start from the first cell. Rows and columns are zero indexed.
        row = 2
        col = 1

        # Iterate over the data and write it out row by row.
        for _day, _start_time, _stop_time, _sum in (month_times):
            worksheet.write(row, col + 0, _day,        workbook.add_format(ex.regular_format))
            worksheet.write(row, col + 1, _start_time, workbook.add_format(ex.regular_format))
            worksheet.write(row, col + 2, _stop_time,  workbook.add_format(ex.regular_format))
            worksheet.write(row, col + 3, _sum,        workbook.add_format(ex.sum_of_day_format))
            row += 1

        # Merging duplicate cells.
        start_row = 0
        stop_row = 1
        month_times += (['','','',''],)
        prev_day = ''

        for i in range(1,len(month_times)):
            if prev_day!=month_times[i][0]:
                stop_row = i
                if start_row!=(stop_row-1):
                    worksheet.merge_range(start_row+2, 1, stop_row+1, 1, prev_day, workbook.add_format(ex.regular_format))
                start_row = i
            prev_day = month_times[i][0]

        # Write the sum of month
        worksheet.write(row, 3, ex.sum_all, workbook.add_format(ex.sum_all_format))
        worksheet.write(row, 4, '=SUM(E3:E' + str(len(month_times)+1) + ')', workbook.add_format(ex.sum_all_format))

        workbook.close()

        send_document(inCome_uid,file_name,ms.send_report.replace('%',inCome_name).replace('&',THIS_MONTH_NAME).replace('*',THIS_YEAR))
        send_document(log_chan,file_name,ms.send_report.replace('%',inCome_name).replace('&',THIS_MONTH_NAME).replace('*',THIS_YEAR))

    except Exception as e:
        print('error in _export_excell()')
        print(e)

FSM_Array = {
            'home'          : { bt.home[0][1]: _start_timer,
                                bt.home[0][0]: _cheghadr_shod },

            'working'       : { bt.working[0][0]: _working_done },

            'enter_period'  : { bt.time_domain[0][0]: _today,
                                bt.time_domain[0][1]: _this_month,
                                bt.time_domain[0][2]: _enter_month,
                                bt.time_domain[1][0]: _back_to_home },

            'enter_month'   :{  bt.monthes[0][0]: _export_selector_prev,
                                bt.monthes[0][1]: _export_selector_now,
                                bt.monthes[1][0]: _back_to_enter_period,}
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
            FSM_Array[current_state][input_message](inCome_uid, inCome_name, inCome_user_id)
        except Exception as e:
            print('error in FSM_handler()')
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
def send_document(uid,file_name,caption):
    try:
        document = open(file_name, 'rb')
        bot.sendChatAction(uid, 'UPLOAD_DOCUMENT')
        bot.send_document(uid, document, caption=caption)
        document.close()
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
        print('error in sen_text()')
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

send_text(log_chan, 'Bot started')

# send2all_pic(ms.nowruz)
# print("DONE")
# while True:
#     pass

while True:
    with conn:
        all_times = db.query_all_times(conn)
        if all_times!=0:
            for _time in all_times:
                if (5 < mdt.minutes_to_now(_time[2])) and (mdt.minutes_to_now(_time[2]) % (2*60) <= 1) and (_time[3]=='0') and (_time[4]=='0'):
                    if int(_time[1])!=117771663:
                        send_text(_time[1], ms.pasho_pasho)
    time.sleep(60)
