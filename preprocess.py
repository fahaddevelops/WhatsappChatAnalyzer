import re
import pandas as pd
def preprocessor(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s[APapMm]{2}\s-\s)(.*)'
    msgs = re.findall(pattern, data)
    user_msg = []
    msg_date = []

    for date, msg in msgs:
        user_msg.append(msg)
        msg_date.append(date.strip())

    df = pd.DataFrame({'user_msg': user_msg, 'msg_date': msg_date})
    df['msg_date'] = pd.to_datetime(df['msg_date'], format='%d/%m/%Y, %I:%M %p -')

    df.rename(columns = {'msg_date': 'date'}, inplace = True)
    users = []
    messages = []

    for msg in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_msg'], inplace=True)
    df['month'] = df['date'].dt.month_name()
    df['day_n'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.strftime('%I %p')
    df['minute'] = df['date'].dt.minute
    df['year'] = df['date'].dt.year
    df['only_date']=df['date'].dt.date
    df['num_month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        period.append(hour)
    df['period'] = period
    
    return df

