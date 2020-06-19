#!/usr/bin/env python

# TODO: Remove json
import json
import sys

import github_handler as gith
import sp_log_handler as logh
import graph_handler as graphh

BACKLOG_COLUMN_ID = '7446636'
PROGRESS_COLUMN_ID = '5014072'
DONE_COLUMN_ID = '9573102'

def main():
    token = gith.get_token()
    headers = gith.setup_headers(token)

    backlog_sp_total = gith.get_sp_total(BACKLOG_COLUMN_ID, headers)
    progress_sp_total = gith.get_sp_total(PROGRESS_COLUMN_ID, headers)
    done_sp_total = gith.get_sp_total(DONE_COLUMN_ID, headers)

    total_sp = backlog_sp_total + progress_sp_total + done_sp_total
    remaining_sp = total_sp - done_sp_total

    logh.update_json(total_sp, remaining_sp)

    sprint = logh.get_current_sprint()

    if sprint:
        graphh.plot_sprint(sprint)
    else:
        # It is between sprints right now
        sys.exit()

    # Build the payload
    graph_64 = str(graphh.encode_64('plot.png'))[2:-1]
    old_sha = gith.get_sha(headers)
    payload = gith.setup_payload(token, graph_64, old_sha)

    # Update GitHub
    gith.api_request('https://api.github.com/repos/AlexDGillespie/burndown/contents/plot.png', headers, payload)

if __name__ == '__main__':
    main()
