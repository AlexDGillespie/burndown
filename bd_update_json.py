#!/usr/bin/env python

import json
import requests
import datetime

API_URL_BASE = 'https://api.github.com/'
BACKLOG_COLUMN_ID = '7446636'
PROGRESS_COLUMN_ID = '5014072'
DONE_COLUMN_ID = '9573102'

def get_sp_total(column_id, headers):
    # Finds a list of all issues in the column
    content_urls = get_content_urls(column_id, headers)

    total_sp = 0

    # Runs for each issue in the column
    for content_url in content_urls:
        response = json.loads(api_request(content_url, headers))

        labels = response['labels']

        # Searches for a 'sp: #' label on the issue
        for label in labels:
            if 'sp: ' in label['name']:
                total_sp += int(label['name'][3:])
        
    return total_sp

def get_content_urls(column_id, headers):
    response = api_request('{}projects/columns/{}/cards'.format(API_URL_BASE, column_id), headers)

    response_list = json.loads(response.decode('utf8'))

    content_urls = []

    for card in response_list:
        try:
            content_urls.append(card['content_url'])
        except:
            # Card has no attached issue.
            pass

    return content_urls

def api_request(api_url, headers):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return (response.content)
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

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

def main():
    with open('token.txt', 'r') as f:
        token = f.read().strip()

    headers = {
            'Authorization': 'Token {}'.format(token),
            'Accept': 'application/vnd.github.inertia-preview+json'}

    backlog_sp_total = get_sp_total(BACKLOG_COLUMN_ID, headers)
    progress_sp_total = get_sp_total(PROGRESS_COLUMN_ID, headers)
    done_sp_total = get_sp_total(DONE_COLUMN_ID, headers)

    total_sp = backlog_sp_total + progress_sp_total + done_sp_total
    remaining_sp = total_sp - done_sp_total

    update_json(total_sp, remaining_sp)

if __name__ == '__main__':
    main()
