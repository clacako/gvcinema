import string
import random
import secrets

def generate_alphanum(model=None, *args, **kwargs):
    length  = 9
    chars   = string.digits
    result  = ''.join(random.choice(chars) for _ in range(length))
    if model is not None and model.objects.filter(external_id=result).exists(): generate_alphanum(model=model, *args, **kwargs)
    
    return result

def token_urlsafe(length=10):
    return secrets.token_urlsafe(length)

def roman_month(month):
    roman_months    = {
        1   : "I",
        2   : "II",
        3   : "III",
        4   : "IV",
        5   : "V",
        6   : "VI",
        7   : "VII",
        8   : "VIII",
        9   : "IX",
        10  : "X",
        11  : "XI",
        12  : "XII"
    }

    return roman_months.get(month)
