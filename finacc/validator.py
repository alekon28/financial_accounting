class Validator(object):
    def __init__(self):
        self.expected_types = ['regular', 'random', 'savings']

    def validate_new_income(self, income_type=None, value=None, name=None, comment=None):

        if income_type is None or value is None or name is None or comment is None:
            return False
        if income_type == '' or name == '' or value == '':
            return False
        if income_type not in self.expected_types:
            return False
        if not value.isdigit():
            return False
        return True
