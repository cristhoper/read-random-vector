from datetime import datetime
from flask_restful import Resource


class DatetimeHandler(Resource):
    def get(self):
        result = datetime.now()
        if result is not None:
            return f"{result.year},{result.month},{result.day},{result.hour},{result.minute},{result.second},{result.microsecond},0"

        return 0
