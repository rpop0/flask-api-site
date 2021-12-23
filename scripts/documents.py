import datetime
import mongoengine

mongo_host = "mongodb+srv://monthly-spending:monthly-spending@cluster0.itj78.mongodb.net/myFirstDatabase?retryWrites" \
             "=true&w=majority "


class Spending(mongoengine.Document):
    month = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    spending_text = mongoengine.StringField(required=True)
    amount = mongoengine.FloatField(required=True)
    category = mongoengine.StringField(required=True)
