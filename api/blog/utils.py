from datetime import datetime
# 2020-08-12


def validate_date_query_params(date_from, date_to):
    errors = []
    date_from_date = datetime.strptime(date_from, '%Y-%m-%d')
    date_to_date = datetime.strptime(date_to, '%Y-%m-%d')

    if date_from_date > date_to_date:
        errors.append('The start date of the interval cannot be greater than the end date')

    is_valid = True if not errors else False

    result = {'is_valid': is_valid}

    if not is_valid:
        result['errors'] = errors

    return result
