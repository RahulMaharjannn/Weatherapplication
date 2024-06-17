from flask import Flask, render_template, request, make_response
from weather import get_current_weather, get_time
from gpt import get_gpt_text
from datetime import date, timedelta, datetime
import calendar
import json
import gpt
from database.account import create_user, get_user_info
from database.emailLoop import emailLoop
from email_notifications import email_notifications, new_user_email
from flask_apscheduler import APScheduler

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)

#@scheduler.task('cron', id='do_email_job', minute='*', day_of_week='*')
#def email_job():
    #email_dict, user_list = emailLoop()
    #email_notifications(email_dict)

scheduler.start()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', warning_message='')

@app.route('/weather', methods=['POST', 'GET'])
def get_weather():
    if request.method=='POST':

        #Get Create Account information from index.html
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        userZip = request.form.get('userZip', '')
        tempPref = request.form.get('tempPref', 'N')
        precipitationPref = request.form.get('precipPref', 'N')
        windPref = request.form.get('windPref', 'N')
        uvPref = request.form.get('uvPref', 'N')
        humidityPref = request.form.get('humidityPref', 'N')

        output = ''
        resp = make_response(output) 
        resp.set_cookie('username', username) 

        #Original Zipcode variable
        zipcode = request.form['zipcode']
        templateFront = gpt.userTemplateFront
        templateBack = gpt.userTemplateBack
        userMode=False

        if len(zipcode) == 0:

            # If the username field is left empty
            if len(username) == 0 and len(email) != 0 and len(userZip)!= 0:
                return render_template('index.html', warning_message ='No username entered!')
            
            # If the email field is empty
            elif len(username) != 0 and len(email) == 0 and len(userZip)!= 0:
                return render_template('index.html', warning_message ='No email entered!')
            
            # If the zipcode field is empty
            elif len(username) != 0 and len(email) != 0 and len(userZip) == 0:
                return render_template('index.html', warning_message ='No zipcode entered!')
            
            # If the username and the email field are empty
            elif len(username) == 0 and len(email) == 0 and len(userZip) != 0:
                return render_template('index.html', warning_message ='No username or email entered!')
            
            elif len(username) != 0 and len(email) == 0 and len(userZip) == 0:
                return render_template('index.html', warning_message ='No email or zipcode entered!')
            
            elif len(username) == 0 and len(email) != 0 and len(userZip) == 0:
                return render_template('index.html', warning_message ='No username or zipcode entered!')
            
            elif len(username) == 0 and len(email) == 0 and len(userZip) == 0:
                return render_template('index.html', warning_message ='No fields filled out!')
            
            else:
                pass

        #Create User txt.file if info is not Null
        if ((username != '') and (tempPref != '')):
            create_user(username, email, userZip, tempPref, precipitationPref, windPref, uvPref, humidityPref)
            new_user_email(email)
        

        email_dict, user_list = emailLoop()
        if not zipcode.isdigit() and len(zipcode) > 1 and zipcode not in user_list:
            return render_template('index.html', warning_message ='Username not found in database!')
        #If value is a username, unpack user values and grab user zipcode
        if not zipcode.isdigit() and zipcode != '':
            u_name,u_email,u_zipcode,u_temp_pref,u_precip_pref,u_windspeed_pref,u_uv_pref,u_humidity_pref = get_user_info(zipcode)
            

            #TEMP PREF
            if u_temp_pref == 'Y':
                templateFront=templateFront+'Temperature, '
            else:
                templateBack=templateBack+'Temperature, '
            #PRECIP PREF
            if u_precip_pref == 'Y':
                templateFront=templateFront+'Precipitation, '
            else:
                templateBack=templateBack+'Precipitation, '
            #WIND SPEED PREF
            if u_windspeed_pref == 'Y':
                templateFront=templateFront+'Wind Speed, '
            else:
                templateBack=templateBack+'Wind Speed, '
            #UV PREF
            if u_uv_pref == 'Y':
                templateFront=templateFront+'UV Index, '
            else:
                templateBack=templateBack+'UV Index, '
            #HUMIDITY PREF
            if u_humidity_pref == 'Y':
                templateFront=templateFront+'Humidity, '
            else:
                templateBack=templateBack+'Humidity, '
                      
            userMode=True          
            zipcode=u_zipcode
            
        #If zipcode is null, user zip is used
        if zipcode == '':
            zipcode = userZip        
            
        weather_data, city, alert_headline, air_pollutant_response = get_current_weather(zipcode)

        #GPT Process
        json_string=json.dumps(weather_data)
        if userMode:
           print(templateFront+templateBack+". Here is the JSON Data: ")
           message = get_gpt_text(templateFront+templateBack+". Here is the JSON Data: "+json_string)
        else:
           message = get_gpt_text(gpt.template+json_string)


        today = date.today()
        day_one = today + timedelta(days=1)
        day_two = today + timedelta(days=2)
        day_three = today + timedelta(days=3)
        day_four = today + timedelta(days=4)
        day_five = today + timedelta(days=5)
        day_six = today + timedelta(days=6)
        day_seven = today + timedelta(days=7)
        now = datetime.now()
        
        one_hour = now + timedelta(hours=1)
        one_hour_int = int(one_hour.strftime("%H"))
        
        two_hours = now + timedelta(hours=2)
        two_hours_int = int(two_hours.strftime("%H"))
        
        three_hours = now + timedelta(hours=3)
        three_hours_int = int(three_hours.strftime("%H"))

        four_hours = now + timedelta(hours=4)
        four_hours_int = int(four_hours.strftime("%H"))

        five_hours = now + timedelta(hours=5)
        five_hours_int = int(five_hours.strftime("%H"))

        six_hours = now + timedelta(hours=6)
        six_hours_int = int(six_hours.strftime("%H"))
        
        seven_hours = now + timedelta(hours=7)
        seven_hours_int = int(seven_hours.strftime("%H"))
        
        eight_hours = now + timedelta(hours=8)
        eight_hours_int = int(eight_hours.strftime("%H"))
 
        return render_template(
            "weather.html",

            aqi=air_pollutant_response['list'][0]['main']['aqi'],
            co=air_pollutant_response['list'][0]['components']['co'],
            no=air_pollutant_response['list'][0]['components']['no'],
            no2=air_pollutant_response['list'][0]['components']['no2'],
            o3=air_pollutant_response['list'][0]['components']['o3'],
            so2=air_pollutant_response['list'][0]['components']['so2'],
            pm25=air_pollutant_response['list'][0]['components']['pm2_5'],
            pm10=air_pollutant_response['list'][0]['components']['pm10'],
            nh3=air_pollutant_response['list'][0]['components']['nh3'],

            status=weather_data['current']['weather'][0]['description'],
            temp=weather_data["current"]["temp"],
            feels_like=weather_data["current"]["feels_like"],
            humidity=weather_data['current']['humidity'],
            wind_speed = weather_data['current']['wind_speed'],
            air_pressure =weather_data['current']['pressure'],
            uv_index=weather_data['current']['uvi'],
            dew_point=weather_data['current']['dew_point'],
            location=city,

            day_one = calendar.day_name[day_one.weekday()],
            day_one_status=weather_data['daily'][1]['summary'],
            day_one_max_temp=weather_data['daily'][1]['temp']['max'],
            day_one_min_temp=weather_data['daily'][1]['temp']['min'],
            day_one_hum=weather_data['daily'][1]['humidity'],
            day_one_uvi=weather_data['daily'][1]['uvi'],
            day_one_wind_speed=weather_data['daily'][1]['wind_speed'],

            day_two = calendar.day_name[day_two.weekday()],
            day_two_status=weather_data['daily'][2]['summary'],
            day_two_max_temp=weather_data['daily'][2]['temp']['max'],
            day_two_min_temp=weather_data['daily'][2]['temp']['min'],
            day_two_hum=weather_data['daily'][2]['humidity'],
            day_two_uvi=weather_data['daily'][2]['uvi'],
            day_two_wind_speed=weather_data['daily'][2]['wind_speed'],

            day_three =calendar.day_name[day_three.weekday()],
            day_three_status = weather_data['daily'][3]['summary'],
            day_three_max_temp=weather_data['daily'][3]['temp']['max'],
            day_three_min_temp=weather_data['daily'][3]['temp']['min'],
            day_three_hum=weather_data['daily'][3]['humidity'],
            day_three_uvi=weather_data['daily'][3]['uvi'],
            day_three_wind_speed=weather_data['daily'][3]['wind_speed'],

            day_four =calendar.day_name[day_four.weekday()],
            day_four_status= weather_data['daily'][4]['summary'],
            day_four_max_temp=weather_data['daily'][4]['temp']['max'],
            day_four_min_temp=weather_data['daily'][4]['temp']['min'],
            day_four_hum=weather_data['daily'][4]['humidity'],
            day_four_uvi=weather_data['daily'][4]['uvi'],
            day_four_wind_speed=weather_data['daily'][4]['wind_speed'],
            
            day_five =calendar.day_name[day_five.weekday()],
            day_five_status= weather_data['daily'][5]['summary'],
            day_five_max_temp=weather_data['daily'][5]['temp']['max'],
            day_five_min_temp=weather_data['daily'][5]['temp']['min'],
            day_five_hum=weather_data['daily'][5]['humidity'],
            day_five_uvi=weather_data['daily'][5]['uvi'],
            day_five_wind_speed=weather_data['daily'][5]['wind_speed'],
            
            day_six = calendar.day_name[day_six.weekday()],
            day_six_status= weather_data['daily'][6]['summary'],
            day_six_max_temp=weather_data['daily'][6]['temp']['max'],
            day_six_min_temp=weather_data['daily'][6]['temp']['min'],
            day_six_hum=weather_data['daily'][6]['humidity'],
            day_six_uvi=weather_data['daily'][6]['uvi'],
            day_six_wind_speed=weather_data['daily'][6]['wind_speed'],
            
            day_seven = calendar.day_name[day_seven.weekday()],
            day_seven_status= weather_data['daily'][7]['summary'],
            day_seven_max_temp=weather_data['daily'][7]['temp']['max'],
            day_seven_min_temp=weather_data['daily'][7]['temp']['min'],
            day_seven_hum=weather_data['daily'][7]['humidity'],
            day_seven_uvi=weather_data['daily'][7]['uvi'],
            day_seven_wind_speed=weather_data['daily'][7]['wind_speed'],

            one_hour = get_time(one_hour_int),
            one_hour_temp=weather_data['hourly'][1]['temp'],
            one_hour_humidity = weather_data['hourly'][1]['humidity'],
            one_hour_uvi = weather_data['hourly'][1]['uvi'],
            one_hour_wind_speed = weather_data['hourly'][1]['wind_speed'],
            one_hour_description = weather_data['hourly'][1]['weather'][0]['main'],

            two_hours=get_time(two_hours_int),
            two_hours_temp=weather_data['hourly'][2]['temp'],
            two_hours_humidity = weather_data['hourly'][2]['humidity'],
            two_hours_uvi = weather_data['hourly'][2]['uvi'],
            two_hours_wind_speed = weather_data['hourly'][2]['wind_speed'],
            two_hours_description = weather_data['hourly'][2]['weather'][0]['main'],

            three_hours=get_time(three_hours_int),
            three_hours_temp=weather_data['hourly'][3]['temp'],
            three_hours_humidity = weather_data['hourly'][3]['humidity'],
            three_hours_uvi = weather_data['hourly'][3]['uvi'],
            three_hours_wind_speed = weather_data['hourly'][3]['wind_speed'],
            three_hours_description = weather_data['hourly'][3]['weather'][0]['main'],

            four_hours=get_time(four_hours_int),
            four_hours_temp=weather_data['hourly'][4]['temp'],
            four_hours_humidity = weather_data['hourly'][4]['humidity'],
            four_hours_uvi = weather_data['hourly'][4]['uvi'],
            four_hours_wind_speed = weather_data['hourly'][4]['wind_speed'],
            four_hours_description = weather_data['hourly'][4]['weather'][0]['main'],

            five_hours=get_time(five_hours_int),
            five_hours_temp=weather_data['hourly'][5]['temp'],
            five_hours_humidity = weather_data['hourly'][5]['humidity'],
            five_hours_uvi = weather_data['hourly'][5]['uvi'],
            five_hours_wind_speed = weather_data['hourly'][5]['wind_speed'],
            five_hours_description = weather_data['hourly'][5]['weather'][0]['main'],

            six_hours=get_time(six_hours_int),
            six_hours_temp=weather_data['hourly'][6]['temp'],
            six_hours_humidity = weather_data['hourly'][6]['humidity'],
            six_hours_uvi = weather_data['hourly'][6]['uvi'],
            six_hours_wind_speed = weather_data['hourly'][6]['wind_speed'],
            six_hours_description = weather_data['hourly'][6]['weather'][0]['main'],
            
            seven_hours=get_time(seven_hours_int),
            seven_hours_temp=weather_data['hourly'][7]['temp'],
            seven_hours_humidity = weather_data['hourly'][7]['humidity'],
            seven_hours_uvi = weather_data['hourly'][7]['uvi'],
            seven_hours_wind_speed = weather_data['hourly'][7]['wind_speed'],
            seven_hours_description = weather_data['hourly'][7]['weather'][0]['main'],

            eight_hours = get_time(eight_hours_int),
            eight_hours_temp = weather_data['hourly'][8]['temp'],
            eight_hours_humidity = weather_data['hourly'][8]['humidity'],
            eight_hours_uvi = weather_data['hourly'][8]['uvi'],
            eight_hours_wind_speed = weather_data['hourly'][8]['wind_speed'],
            eight_hours_description = weather_data['hourly'][8]['weather'][0]['main'],


            alert=alert_headline,
            #Ryan vars
            message=message
        )
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)