import jdatetime

def get_year(_input):
    return _input.split('-')[0]

def get_month(_input):
    return _input.split('-')[1]

def get_day(_input):
    return _input.split('-')[2].split(' ')[0]

def get_hour(_input):
    return _input.split(' ')[1].split(':')[0]

def get_minute(_input):
    return _input.split(':')[1]

def get_second(_input):
    return _input.split(':')[2].split('.')[0]

def get_date(_input):
    return _input.split(' ')[0]

def get_time(_input):
    return _input.split(' ')[1].split('.')[0]

def str2dt(_input):
    return jdatetime.datetime.strptime(_input.split('.')[0], "%Y-%m-%d %H:%M:%S")

def isInToday(_input):
    today = str(jdatetime.datetime.now())
    today_date = get_date(today)

    start_of_today = today_date + " 00:00:00.0"

    length = (str2dt(_input) - str2dt(start_of_today)).total_seconds()

    if 0 < length and length < 24*3600:
        return 1
    else:
        return 0
