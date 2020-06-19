#!/usr/bin/env python

import json
import requests

def get_token():
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    
    return token

def setup_headers(token):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/vnd.github.inertia-preview+json'}

    return headers

def setup_payload(token, content, sha):
    payload = {
        'message': 'Sent from code!',
        'content': content,
        'sha': sha}

    return payload

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
    # Getting a list of all cards in the column
    response = api_request('https://api.github.com/projects/columns/{}/cards'.format(column_id), headers)
    response_list = json.loads(response.decode('utf8'))

    # Setting up list of Issue URLs
    content_urls = []

    # Filling the list of Issue URLs from the cards
    for card in response_list:
        try:
            content_urls.append(card['content_url'])
        except:
            # Card has no attached issue.
            pass

    return content_urls

def api_request(api_url, headers, payload=False):
    if not payload:
        response = requests.get(api_url, headers=headers)
    else:
        response = requests.put(url=api_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return (response.content)
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))

def get_sha(headers):
    response = api_request('https://api.github.com/repos/AlexDGillespie/burndown/contents/plot.png', headers)
    plot_json = json.loads(response)
    
    return plot_json['sha']