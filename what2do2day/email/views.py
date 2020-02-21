import json


def email_event(event, user_email):
    email_body = '<div style="background:#00d1b2; color:"#a2a2a2; font-size:18px; margin:10px; padding:0: font-family:\'Raleway\', arial; font-weight:normal;">'
    email_body += '<h1 style="font-size:2.6rem; color:#FFF; margin: 20px;">You\'ve joined ' + event[
        'event_name'] + '</h1>'
    email_json = event_json_ld(event, user_email)
    email_body += '<script type="application/ld+json">' + json.dumps(email_json) + '</script>'
    return email_body


def event_json_ld(event, user_email):
    startDate = event['date_time_range'][0:10]
    startTime = event['date_time_range'][11:16]
    endDate = event['date_time_range'][19:29]
    endTime = event['date_time_range'][30:35]

    event_json = [{
        "@context": "http://schema.org",
        "@type": "EventReservation",
        "reservationNumber": "E123456789",
        "reservationStatus": "http://schema.org/Confirmed",
        "underName": {
            "@type": "Person",
            "name": user_email
        },
        "reservationFor": {
            "@type": "Event",
            "name": event['event_name'],
            "startDate": startDate + 'T-7' + startTime,
            "endDate": endDate + 'T-7' + endTime,
            "details": event['details']

        }
    }]
    streetAddress = ''
    if 'event_address' in event.keys() and event['event_address'] != '' and 'address_line_1' in event[
        'event_address'].keys() and event['event_address']['address_line_1'] != "":
        streetAddress = event['event_address']['address_line_1']
        if 'address_line_2' in event['event_address'].keys() and event['event_address']['address_line_2'] != "":
            streetAddress += ", " + event['event_address']['address_line_2']

        if streetAddress != '':
            address = {
                "@type": "PostalAddress",
                "streetAddress": streetAddress,
                "addressLocality": event['event_address']['city'],
                "addressRegion": event['event_address']['state'],
                "addressCountry": event['event_address']['country']
            }
            if 'postal_code' in event['event_address'].keys() and event['event_address']['postal_code'] != '':
                postal_code = {'postal_code': event['event_address']['postal_code']}
                address['postal_code'] = postal_code
            event_json[0]['reservationFor']['location'] = { 'address': address}

    return event_json
