import secrets
import string
"""module: models/generators/generate_password
used to generate passwords for platforms
"""


def password_generator():
    """generate a strong password
     Return:
        password (str) - a password containing a combination of
                         special character, numbers and letters
    """
    # collect a list of ascii chars, int and special characters
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    selection_list = letters + digits + special_chars

    # set password length
    password_len = 10

    '''
    loop until the password has a minimum of 1 special character and a
    minimum of 2 digits
    ''' 
    while True:
        password = ''
        for i in range(password_len):
            password += ''.join(secrets.choice(selection_list))

        if (any(char in special_chars for char in password) and
                sum(char in digits for char in password) >= 2):
            break

    return password
