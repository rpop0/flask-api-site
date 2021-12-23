from flask import Flask
from flask_restful import Resource, Api, reqparse
from scripts.sheet_adder import SheetInterface

app = Flask(__name__)
api = Api(app)


class Income(Resource):
    @staticmethod
    def post():
        """
        Parses the request, checking all of the arguments and the key. It then uses the add_to_sheet script to
        add the specific income on the sheet.
        :return: Json response depending on the status of the addition.
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('key', required=True)
        parser.add_argument('income_text', required=True)
        parser.add_argument('amount', type=int, required=True)
        parser.add_argument('type', required=True)
        args = parser.parse_args()
        if args['key'] != "key_test":
            return {'unauthorized': 401}, 401
        sheet_interface = SheetInterface()
        status = sheet_interface.add_income(args['amount'], args['income_text'], args['type'])
        if status == 1:
            return {'found': False}, 204
        return {'ok': True}, 200


class Expense(Resource):
    @staticmethod
    def post():
        """
        Parses the request, checking all of the arguments and the key. It then uses the add_to_sheet script to
        add the specific expense on the sheet.
        :return: Json response depending on the status of the addition.
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('key', required=True)
        parser.add_argument('expense_text', required=True)
        parser.add_argument('amount', type=float, required=True)
        parser.add_argument('type', required=True)
        args = parser.parse_args()
        if args['key'] != "key_test":
            return {'unauthorized': 401}, 401
        sheet_interface = SheetInterface()
        status = sheet_interface.add_expense(args['amount'], args['expense_text'], args['type'])
        if status == 1:
            return {'found': False}, 204
        return {'ok': True}, 200


class Value(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('key', required=True)
        args = parser.parse_args()
        if args['key'] != "key_test":
            return {'unauthorized': 401}, 401
        sheet_interface = SheetInterface()
        current_value = sheet_interface.get_current_month_value()
        return {'current_value': current_value}, 200


api.add_resource(Income, '/api/income/')
api.add_resource(Expense, '/api/expense/')
api.add_resource(Value, '/api/value/')

if __name__ == '__main__':
    app.run(debug=True)
