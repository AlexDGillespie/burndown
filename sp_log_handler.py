#!/usr/bin/env python

import json
import datetime

def update_json(total_sp, remaining_sp, recursive_call=False):
    # Handling datetime
    today_date = datetime.date.today()
    is_weekday = today_date.weekday() < 5
    today = str(today_date)

    # Pulling sp_log.json into memory
    # Note: if this starts taking up too much memory then just trim old sprints off this file.
    with open('sp_log.json', 'r') as f:
        sp_log = json.loads(f.read())

    # Turns False if today is inside a sprint's date range
    is_outside_sprint = True

    # Updates sp_log with todays data if we are in a sprint and it's a weekday
    for sprint in sp_log:
        if today <= sprint['end_date'] and today >= sprint['start_date']:
            is_outside_sprint = False

            if is_weekday:
                sprint['sp_total'] = str(total_sp)
                sprint['daily_sp_remaining'][today] = str(remaining_sp)
    
    # Creates a new sprint in sp_log on the first monday of the sprint.
    # sp_total will be set to None until the next time this script runs.
    if is_outside_sprint and is_weekday:
        new_sprint = {
            'start_date': today,
            'end_date': str(today_date + datetime.timedelta(days=11)),
            'sp_total': 'None',
            'daily_sp_remaining': {}
        }

        sp_log.append(new_sprint)
    
    # Updates sp_log.json with sp_log storred in memory.
    with open('sp_log.json', 'w') as f:
        f.write(json.dumps(sp_log, indent=4))

    # Maybe not the best solution I could come up with, but this makes sure that the first datapoint is always 
    # collected
    if is_outside_sprint and not recursive_call:
        update_json(total_sp, remaining_sp, True)

def get_current_sprint():
    # Handling datetime
    today_date = datetime.date.today()
    is_weekday = today_date.weekday() < 5
    today = str(today_date)

    # Loading sp_log.json
    with open('sp_log.json', 'r') as f:
        sp_log = json.loads(f.read())

    # Running function to plot the current sprint if one exists
    for sprint in sp_log:
        if today <= sprint['end_date'] and today >= sprint['start_date']:
            if is_weekday:
                return sprint
    
    return False