import jdatetime

names = {
    '01' : 'فروردین',
    '02' : 'اردیبهشت',
    '03' : 'خرداد',
    '04' : 'تیر',
    '05' : 'مرداد',
    '06' : 'شهریور',
    '07' : 'مهر',
    '08' : 'آبان',
    '09' : 'آذر',
    '10' : 'دی',
    '11' : 'بهمن',
    '12' : 'اسفند'
}

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

def get_this_year():
    return get_year(str(jdatetime.datetime.now()))

def get_this_month():
    return get_month(str(jdatetime.datetime.now()))

def get_this_month_name():
    return names[get_month(str(jdatetime.datetime.now()))]

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

def isInPrevMonth(_input):
    first_day_of_current_month = jdatetime.date.today().replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - jdatetime.timedelta(days=1)

    input_year  = get_year(_input)
    input_month = get_month(_input)
    return 1 if (int(input_year)==last_day_of_previous_month.year and int(input_month)==last_day_of_previous_month.month) else 0

def minutes_to_now(_input):
    today = jdatetime.datetime.now()
    converted_input = str2dt(_input)
    return (today - converted_input).total_seconds()/60
