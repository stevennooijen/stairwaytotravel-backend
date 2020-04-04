
def create_interests_query(user_interests):
    interest_mapping = {
        'flights': '4fdc15b644',
        'local_transport': '7ceb4a1b29',
        'activities': '621cff108a',
        'accommodation': '14af682816',
        'none': '5ebcfd6d93',
    }

    return {interest_mapping[key]:value for (key,value) in user_interests.items()}
