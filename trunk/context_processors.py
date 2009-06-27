from utils.activity import *

# grab number of 'good question' and 'good answer' for request.user

def avatar_meta(request):
    try:
        user_score = get_user_score_for_user(request.user)
    except:
        user_score = 'N/A'
        
    return locals()