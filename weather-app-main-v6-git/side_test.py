import calendar
from datetime import date, timedelta, datetime

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=2)


print("Yesterday = ", calendar.day_name[yesterday.weekday()], yesterday.strftime('%d-%m-%Y'))
print("Today = ", calendar.day_name[today.weekday()], today.strftime('%d-%m-%Y'))
print("Tomorrow = ", calendar.day_name[tomorrow.weekday()], tomorrow.strftime('%d-%m-%Y'))
now = datetime.now()

current_time = int(now.strftime("%H"))
one_hour = now + timedelta(hours=1)
int_one_hour = int(one_hour.strftime("%H"))

if int_one_hour > 12:
    print(int_one_hour - 12)
else:
    print(int_one_hour)

print("Current Time =", current_time)
print(int_one_hour)

