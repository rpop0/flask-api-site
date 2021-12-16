from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Income(Resource):
    def get(self, income_type):
        return {'status': income_type}

    def post(self):
        print(request.get_json())
        return {'status': 'success'}, 200


class Expense(Resource):
    def get(self):
        return {'status': 'Gotten expense.'}

    def post(self, expense_type):
        print(expense_type)
        print(request.form)
        return {'status': 'success'}, 200


api.add_resource(Income, '/income/<string:income_type>')
api.add_resource(Expense, '/expense/<string:expense_type>')

if __name__ == '__main__':
    app.run(debug=True)
