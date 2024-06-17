from email.message import EmailMessage
from email.utils import make_msgid
import ssl
import smtplib
import os
from dotenv import load_dotenv
from weather import get_current_weather
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import calendar
from datetime import date

load_dotenv()

def email_notifications(email_dict):
    email_sender = 'weatherappgmu@gmail.com'
    email_password = os.getenv('EMAIL_PASSWORD')
    
    for email_receiver, zipcode in email_dict.items():
        weather_data, city, alert_headline, air_pollutant_response = get_current_weather(zipcode)
        subject = 'Daily Weather Report'
        em = MIMEMultipart('related')
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject

        aqi=air_pollutant_response['list'][0]['main']['aqi']
        status=weather_data['current']['weather'][0]['description']
        temp=weather_data["current"]["temp"]
        feels_like=weather_data["current"]["feels_like"]
        humidity=weather_data['current']['humidity']
        wind_speed = weather_data['current']['wind_speed']
        uv_index=weather_data['current']['uvi']
        
        today = date.today()
        today_day = calendar.day_name[today.weekday()]
        today_status=weather_data['daily'][0]['summary']
        today_max_temp=weather_data['daily'][0]['temp']['max']
        today_min_temp=weather_data['daily'][0]['temp']['min']
        today_hum=weather_data['daily'][0]['humidity']
        today_uvi=weather_data['daily'][0]['uvi']
        today_wind_speed=weather_data['daily'][0]['wind_speed']
        
        message = '''
                <!DOCTYPE html>
                    <html>
                        <head>
                            <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Poppins">
                            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <style type="text/css">
                                h1{font-size:56px;background-color:#000000}
                                h2{font-size:28px;font-weight:900; text-align:center}
                                p{font-weight:100}
                                td{vertical-align:top}
                                #email{margin:auto;width:600px;background-color:#fff}
                            </style>
                        </head>
                        <body bgcolor="#F5F8FA" style="width: 100%; font-family:Poppins, sans-serif; font-size:18px;">
                        <div id="email">
                            <table role="presentation" width="100%">
                            <tr>
                            <td align="center" style="color: white;">
                ''' + f'''
                            <h1>
                            <br>
                            <img src="cid:image1" alt="Logo" style="width:124px;height:124px;"><br>
                            Hello, {email_receiver}!<br><br>
                            </h1>

                ''' + '''
                    
                            </td>
                            </table>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
                            <tr>
                            <td>

                ''' + f'''
                    
                            <h2>Happy {today_day}! This is your weather report!</h2>
                            <b>Location:</b> {city}<br><br>
                            
                            <p style="color: red"; font-weight: "bold"><b>Current weather alerts:</b></p>
                            {alert_headline}
                            <br><br>

                            <b>Currently:</b><br>
                            Description: {status}<br>
                            Temperature: {temp}&deg;F<br>
                            Feels like: {feels_like}&deg;F<br>
                            Humidity: {humidity}%<br>
                            Wind speed: {wind_speed}<br>
                            UV index: {uv_index}<br>
                            Air Quality Index: {aqi}<br>
                            <br>
                            <b>Later today:</b><br>
                            Today's weather description: {today_status}.<br>
                            Today's high: {today_max_temp}&deg;F<br>
                            Today's low: {today_min_temp}&deg;F<br>
                            Expected humidity: {today_hum}%<br>
                            Expected wind speed: {today_wind_speed} MPH<br>
                            UV index: {today_uvi}<br>
                            </td>
                            </tr>
                            </table>
                            </div>
                            </body>
                            </html>
                    '''
        


        part2 = MIMEText(message, 'html')
        em.attach(part2)
        fp = open('./static/photos/email_photo.png', 'rb')
        email_img = MIMEImage(fp.read())
        fp.close()
        email_img.add_header('Content-ID', '<image1>')
        em.attach(email_img)

       

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        print('Sent to:', email_receiver)

def new_user_email(email):
    email_sender = 'weatherappgmu@gmail.com'
    email_password = os.getenv('EMAIL_PASSWORD')
    
    email_receiver = email
    subject = 'GMU Weather App Signup!'
    em = MIMEMultipart('related')
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    message = '''
                <!DOCTYPE html>
                    <html>
                        <head>
                            <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Poppins">
                            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <style type="text/css">
                                h1{font-size:56px;background-color:#000000}
                                h2{font-size:28px;font-weight:900; text-align:center}
                                p{font-weight:100}
                                td{vertical-align:top}
                                #email{margin:auto;width:600px;background-color:#fff}
                            </style>
                        </head>
                        <body bgcolor="#F5F8FA" style="width: 100%; font-family:Poppins, sans-serif; font-size:18px;">
                        <div id="email">
                            <table role="presentation" width="100%">
                            <tr>
                            <td align="center" style="color: white;">
                ''' + f'''
        
                            <h1><img src="cid:image1" alt="Logo" style="width:124px;height:124px;"><br>
                            Welcome, {email_receiver}!<br></h1>

                ''' + '''
                    
                            </td>
                            </table>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
                            <tr>
                            <td>

                ''' + f'''
                    
                            <h2>Thank you for signing up for the GMU Weather Application!</h2>
                            <p>
                            Every day at 8am a notification will be sent to your email provided that details what the current weather is,
                            and what the weather will be for the remainder of the day. For more real time updates check out our website at
                            (LINK_PLACEHOLDER)! <br><br>
                            Have a wonderful day!<br>
                            With any questions or concerns email us weatherappgmu@gmail.com!
                            </p>
                
                ''' + '''
                
                            </td>
                            </tr>
                            </table>
                            </div>
                            </body>
                            </html>
                    '''
        
    part2 = MIMEText(message, 'html')
    em.attach(part2)
    fp = open('./static/photos/email_photo.png', 'rb')
    email_img = MIMEImage(fp.read())
    fp.close()
    email_img.add_header('Content-ID', '<image1>')
    em.attach(email_img)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
