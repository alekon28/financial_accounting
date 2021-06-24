class Validator(object):
    def __init__(self):
        self.expected_freq_types = ['regular', 'random', 'savings']
        self.expected_transaction_type = ['income', 'expense']
        self.expected_transaction_keys = ['project_id', 'freq_type', 'value', 'name', 'comment', 'trans_type']

    def validate_new_transaction(self, data):
        for k in self.expected_transaction_keys:
            if data.get(k) is None:
                return False
            elif data.get(k) == '' and k != 'comment':
                return False
        if not data[self.expected_transaction_keys[2]].isdigit():
            return False
        if not data[self.expected_transaction_keys[0]].isdigit():
            return False
        if not data[self.expected_transaction_keys[1]] in self.expected_freq_types:
            return False
        if not data[self.expected_transaction_keys[5]] in self.expected_transaction_type:
            return False
        return True
