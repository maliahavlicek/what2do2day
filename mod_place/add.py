from app import db_issue, mongo


def load_place_to_db(form):
    try:
        new_place = {
            'name': form.name.lower(),
            'description': form.description,
            'activity': [form.activity],
            'phone': form.phone,
            'website': form.website,
            'image_url': form.image_url,
            'address': form.address,

        }
        places = mongo.db.places.insert_one(new_place)
    except Exception as e:
        db_issue(e)

