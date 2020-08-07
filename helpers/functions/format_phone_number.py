import re

def format_phone_number(phone_number):
    phone_number = phone_number.replace('+1','')
    return re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', phone_number)
