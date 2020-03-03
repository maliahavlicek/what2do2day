import json

from bson import ObjectId

import filters
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from what2do2day import app, mongo


def email_event(event, user_email_list, update=False, add_attendee=False):
    message = MIMEMultipart("alternative")
    message["From"] = app.config['EMAIL']
    password = app.config['EMAIL_PASS']  # Your SMTP password for Gmail
    message["Subject"] = "What2do2day Event- " + event['event_name'].title()
    email_body = "<div style='color:#363636; font-size:18px;'>It's your friends with What2do2day. Here are the details about an event you wanted to attend:</div>"
    text = "Hello,\nIt's your friends with What2do2day. Here are the details about an event you wanted to attend:"
    if update:
        message["Subject"] = "Updated: " + message["Subject"]
        email_body = "<div style='color:#363636; font-size:18px;'>It's your friends with What2do2day. An event you wanted to attend has been updated:</div>"
        text = "Hello,\nIt's your friends with What2do2day. An event you wanted to attend has been updated:"

    email_body += '<div style="color:#363636; font-size:18px;">'
    if update:
        email_body += '<h1 style="font-size:22px; margin: 20px;">' + event[
            'event_name'].title() + '<span style="font-size:20px; margin-left:20px;">Sponsored By: ' + event[
                          'place-name'] + '</span>' + ' has been updated!</h1>'
        text += "\n" + event['event_name'].title() + ' has been updated!'
        text += "\n\tSponsored By: " + event['place-name']
    else:
        email_body += '<h1 style="font-size:22px margin: 20px;">' + event['event_name'].title()
        email_body += '<span style="font-size:20px; margin-left:20px;">Sponsored By: ' + event[
            'place_name'] + '</span></h1>'
        text += "\n" + event['event_name'].title()
        text += "\n\tSponsored By: " + event['place_name']
    email_body += '<div class="columns"><div class="is-bold column">When:</div><div class="column">'

    startDate = event['date_time_range'][0:10]
    startTime = event['date_time_range'][11:16]
    endDate = event['date_time_range'][19:29]
    endTime = event['date_time_range'][30:35]

    email_body += startDate + " " + filters.time_only(
        event['date_time_range']) + '</div></div><div style="clear:both"></div>'
    text += "\nWhen: " + event['date_time_range']

    event_json = {
        "@context": "http://schema.org",
        "@type": "EventReservation",
        "reservationNumber": str(event['_id']),
        "reservationStatus": "http://schema.org/Confirmed",

        "reservationFor": {
            "@type": "Event",
            "name": event['event_name'],
            "startDate": startDate + 'T-7' + startTime,
            "endDate": endDate + 'T-7' + endTime,
            "details": event['details']

        }
    }
    streetAddress = ''
    if 'event_address' in event.keys() and event['event_address'] != '' and event[
        'event_address'] != []:
        if isinstance(event['event_address'], list):
            address = event['event_address'][0]
        else:
            address = event['event_address']
        text += "\nWhere: "
        streetAddress = address['address_line_1'].title()
        displayAddress = streetAddress.title()
        text += "\n" + streetAddress
        if 'address_line_2' in address.keys() and address['address_line_2'] != "":
            streetAddress += ", " + address['address_line_2'].title()
            displayAddress += '<br>' + address['address_line_2'].title()
            text += "\n" + address['address_line_2'].title()

        displayAddress += '<br>' + address['city'].title() + ", " + address['state'].title()
        text += "\n" + address['city'].title() + ", " + address['state'].title()

        if streetAddress != '':
            if isinstance(address['country'], str):
                country = address['country'].title()
            else:
                country = mongo.db.countries.find_one({'_id': ObjectId(address['country'])})
                country = country['country'].title()
            address = {
                "@type": "PostalAddress",
                "streetAddress": streetAddress,
                "addressLocality": address['city'].title(),
                "addressRegion": address['state'].title(),
                "addressCountry": country
            }
            if 'postal_code' in address.keys() and address['postal_code'] != '':
                postal_code = {'postal_code': address['postal_code'].title()}
                address['postal_code'] = postal_code
                displayAddress += '<br>' + address['postal_code'].title() + ' ' + country
                text += "\n" + address['postal_code'].title() + ' ' + country
            else:
                displayAddress += '<br>' + country
                text += "\n" + country

            event_json['reservationFor']['location'] = {'address': address}
            email_body += '<div class="columns"><div class="is-bold column">Where:</div><div class="column">'
            email_body += displayAddress + '</div></div><div style="clear:both"></div>'
    email_body += '<div class="columns"><div class="is-bold column">Details:</div><div class="column">'
    email_body += event['details'] + '</div></div><div style="clear:both"></div>'

    email_body += '<div class="columns"><div class="is-bold column">Price:</div><div class="column">'
    if 'price_for_non_members' in event.keys() and event['price_for_non_members'] != "":
        email_body += event['price_for_non_members'] + '</div></div><div style="clear:both"></div>'
        text += "\nPrice: " + event['price_for_non_members']
    else:
        email_body += "Free </div></div><div style='clear:both'></div>"
        text += "\nPrice: Free"
    email_body += '<div class="columns"><div class="is-bold column">Ages:</div><div class="column">'
    text += "\nAges: "
    if 'age_limit' in event.keys() and len(event['age_limit']) > 0:
        for index, age in enumerate(event['age_limit']):
            email_body += age
            text += age
            if index != len(event['age_limit']) - 1:
                email_body += ", "
                text += ", "

        email_body += "</div></div><div style='clear:both'></div>"
    else:
        email_body += "No Limit </div></div><div style='clear:both'></div>"
        text += "No Limit"

    email_body = email_body.replace('class="columns"', 'style="line-height:1.8rem; margin:5px;"')
    email_body = email_body.replace('class="is-bold column"', 'style="float:left; font-weight:700; width: 90px;"')
    email_body = email_body.replace('class="column"', 'style="float:left; width: auto;"')

    for user in user_email_list:
        user_email = user['email']
        event_json["underName"] = {
            "@type": "Person",
            "name": user_email
        }
        send_email_body = email_body + '</div><script type="application/ld+json">' + json.dumps(event_json) + '</script>'
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(send_email_body, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        message["To"] = user_email

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(app.config['EMAIL'], password)
                server.sendmail(
                    app.config['EMAIL'], user_email, message.as_string()
                )
            if app.config['DEBUG']:
                print('Email update to attendee: ', user_email, " status: success")

        except smtplib.SMTPAuthenticationError as e:
            if add_attendee:
                return False
            else:
                # not the end of the world if email fails, Ideally would log system and let system admin know there is an issue
                if app.config['DEBUG']:
                    print('Email update to attendee: ', user_email, " status: failure")
                pass

    return True
