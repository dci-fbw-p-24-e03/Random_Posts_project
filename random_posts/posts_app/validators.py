from django.core.exceptions import ValidationError



def validate_email(value):
    if value.endswith('.mars') or value.endswith('.jp'):
        raise ValidationError("We do not accept emails from other planets")
    
def validate_username(value):
    if len(value)<5:
        raise ValidationError("Username must be at least 5 characters long")
    

def validate_no_bad_words(value):
    BAD_WORDS = ['dog','cat','fish','popcorn']
    if any([word in value.lower() for word in BAD_WORDS]):
        raise ValidationError('Content contains bad words')
    

def validate_age(value):
    if value < 14 or value > 100:
        raise ValidationError("Users should be between 14 and 100")
    
def validate_post_length(value):
    if len(value) < 20:
        raise ValidationError("Post must be longer than 20 chars")