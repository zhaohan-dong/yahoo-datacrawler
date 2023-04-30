"""
WebullClient class to inherit the webull package

Added functions:
- load opengpg encrypted login credentials from local file
- override login with device id and name to bypass image captcha, and with retry upon failure

"""

from webull import paper_webull, webull
import gnupg
import json
import os

ENVIRONMENT = paper_webull

class WebullClient(ENVIRONMENT):

    def __init__(self, credential_path,
                 gnupghome=f"{os.path.expanduser('~')}/.gnupg"):
        self.__credential_path = credential_path
        self.__gnupghome = gnupghome
        # Set know device ID to bypass image captcha
        self._set_did(self.__get_cred(credential_path=self.__credential_path,
                                      gnupghome=self.__gnupghome)["did"], path="./")
        super().__init__()

    def __get_cred(self, credential_path, gnupghome):
        """
        Read credentials from gpg encrypted login json file

        :return: dictionary of username, password, did(deviceID), device_name
        """
        try:
            with open(credential_path, 'rb') as f:
                # Decrypt the credentials
                gpg = gnupg.GPG(gnupghome=gnupghome)

                # Store credentials as byte object
                credentials = gpg.decrypt(f.read()).data

                # Convert credentials to dictionary
                cred_dict = json.loads(credentials)
            return cred_dict
        except Exception as e:
            print(e)
            raise

    def login(self, username='', password='', device_name='', mfa='', question_id='', question_answer='',
              save_token=False, token_path=None):
        """
        Login with gpg encrypted credentials

        :param username:
        :param password:
        :param device_name:
        :param mfa:
        :param question_id:
        :param question_answer:
        :param save_token:
        :param token_path:
        :return:
        """

        # Retry login for three times
        login_retry_count = 0
        while login_retry_count < 3:
            res = super().login(username=self.__get_cred(credential_path=self.__credential_path,
                                                         gnupghome=self.__gnupghome)["username"],
                                password=self.__get_cred(credential_path=self.__credential_path,
                                                         gnupghome=self.__gnupghome)["password"],
                                device_name=self.__get_cred(credential_path=self.__credential_path,
                                                            gnupghome=self.__gnupghome)["device_name"])

            # Return dict if login successful
            if "accessToken" in res:
                print("Login successful")
                print(f"Token expiring at: {res['tokenExpireTime']}")
                return res

            # Print response message if login failed
            print("Login failed. Retrying...")
            print(f"Server response: {res}")
            login_retry_count += 1

    def place_order(self, stock=None, tId=None, price=0, action='BUY', orderType='LMT', enforce='GTC', quant=0, outsideRegularTradingHour=True, stpPrice=None, trial_value=0, trial_type='DOLLAR'):
        strategy.buy(self)
