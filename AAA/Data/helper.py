import os
import hashlib
import json
import smtplib

from email.mime.text import MIMEText

# TODO: replace it with proper way
os.chdir('..')

INIT_TEST_ID = 103271
DEFAULT_DB_PATH = os.getcwd() + '/db/'


class DataHelper:

    def __init__(self, api_instance):
        self._api = api_instance

    def _calc_score(self, questions):
        scores = map(lambda q: q['score'], filter(lambda q: q['answered'], questions))
        return list(scores)

    def collect_data_from_test(self, test_id):
        test_all_data = self._api.get_test_candidates(test_id=test_id)
        test_data = [{'id': hashlib.sha256(str(test['email']).encode('utf-8')).hexdigest()[:16],
                      'scores': self._calc_score(test['questions']),
                      'plagiarism': test['plagiarism']} for test in test_all_data]
        return test_data

    @staticmethod
    def write_data(data, filename):
        with open(DEFAULT_DB_PATH + filename, 'w') as file:
            json.dump(data, file, sort_keys=True, indent=4)

    @staticmethod
    def read_data(filename):
        with open(DEFAULT_DB_PATH + filename, 'r') as file:
            data = json.load(file)
        return data

    def map_students(self):
        test_all_data = self._api.get_test_candidates(test_id=INIT_TEST_ID)
        mapping = [{'id': hashlib.sha256(str(test['email']).encode('utf-8')).hexdigest()[:16],
                    'full_name': test['candidate_details'][1]['value'],
                    'email': test['email'], } for test in test_all_data]
        return mapping


class EmailDelivery:

    def __init__(self, username, host='smtp.yandex.ru', port='465'):
        self._username = username
        self._port = port
        self._host = host

    def send_email_to(self, password, to, subject, content):
        """
        Send Email for one destination with given text data
        :param password: password to access email account
        :param to: email
        :param subject: email subject
        :param content: text
        :return: status as string
        """
        status = "Message sent!"
        try:
            msg = MIMEText(content, 'plain')
            msg['Subject'] = subject
            msg['From'] = self._username
            connection = smtplib.SMTP_SSL(host=self._host, port=self._port)
            connection.login(self._username, password)

            try:
                connection.sendmail(from_addr=self._username, to_addrs=to, msg=msg.as_string())
            finally:
                connection.quit()

        except Exception as e:
            status = str(e)

        return status

    def send_email_by_map(self, password, subject, mapping):
        """
        Send email by dict object which represents mapping between email destination and content
        :param password: password to access email account
        :param subject: email subject
        :param mapping: dict
        :return: status as string
        """
        status = "Messages sent!"

        try:
            connection = smtplib.SMTP_SSL(host=self._host, port=self._port)
            connection.login(self._username, password)

            try:
                for item in mapping:
                    msg = MIMEText(item['content'], 'plain')
                    msg['Subject'] = subject
                    msg['From'] = self._username

                    connection.sendmail(from_addr=self._username, to_addrs=item['to'], msg=msg.as_string())
            finally:
                connection.quit()

        except Exception as e:
            status = str(e)

        return status
