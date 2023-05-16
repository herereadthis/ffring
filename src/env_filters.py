import math

def render_or_unknown(dict_to_check, key, unknown = 'unknown'):
    result = unknown
    print('dict_to_check')
    print(dict_to_check)
    if dict_to_check is None or len(dict_to_check) == 0:
        result = unknown
    elif key not in dict_to_check or dict_to_check[key] is None or len(dict_to_check[key]) == 0:
        result = unknown
    else:
        result = dict_to_check[key]
    return result

def render_climb(baro_rate, altitude):
    result = f'Flying at {altitude} ft'
    if baro_rate is None:
        result = f'Unknown climb rate, flying at {altitude} ft'
    if baro_rate > 10:
        result = f'Climbing {baro_rate} ft/min from {altitude} ft'
    elif baro_rate < -10:
        result = f'Descending {abs(baro_rate)} ft/min from {altitude} ft'
    return result


def render_schedule_diff(x):
    if x is None:
        result = 'unknown scheduling'
    else:
        diff = round(abs(x))
        result = ''
        if diff == 0:
            result = 'On time'
        else:
            if diff == 1:
                result = "1 minute"
            elif diff < 90:
                result = f"{diff} minutes"
            else:
                hours = diff // 60
                minutes = diff % 60
                if hours == 1:
                    hour_str = "1 hr."
                else:
                    hour_str = f"{hours} hrs."
                if minutes == 1:
                    minute_str = "1 min."
                else:
                    minute_str = f"{minutes} mins."
                result = f"{hour_str}, {minute_str}"
            if x > 0:
                result = f'<span class="schedule_delayed">{result} delayed</span>'
            else:
                result = f'<span class="schedule_early">{result} early</span>'
    
    return result

