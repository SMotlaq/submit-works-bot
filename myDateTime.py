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
    today_year  = get_year(today)
    today_month = get_month(today)
    today_day   = get_day(today)

    input_year  = get_year(_input)
    input_month = get_month(_input)
    input_day   = get_day(_input)

    return 1 if (input_year==today_year and input_month==today_month and input_day==today_day) else 0

def isInThisMonth(_input):
    today = str(jdatetime.datetime.now())
    today_year  = get_year(today)
    today_month = get_month(today)

    input_year  = get_year(_input)
    input_month = get_month(_input)

    return 1 if (input_year==today_year and input_month==today_month) else 0

def minutes_to_now(_input):
    today = jdatetime.datetime.now()
    converted_input = str2dt(_input)
    return (today - converted_input).total_seconds()/60
