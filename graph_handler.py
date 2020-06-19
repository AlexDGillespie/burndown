#!/usr/bin/env python

import base64

from matplotlib import pyplot as plt

def plot_sprint(sprint):
    # Sorting the dict of entries by key (i.e. date)
    keys_sorted_list = sorted([*sprint['daily_sp_remaining']], reverse=False)

    # Setting up x-axis
    x_values = ['Mon1', 'Tue1', 'Wed1', 'Thu1', 'Fri1', 'Mon2', 'Tue2', 'Wed2', 'Thu2', 'Fri2']
    
    # Setting up y-axis for values
    y_values = []
    for key in keys_sorted_list:
        y_values.append(float(sprint['daily_sp_remaining'][key]))

    # Setting up y-axis fro target
    y_linear = []
    for i in reversed(range(10)):
        y_linear.append(int(sprint['sp_total']) * (i + ((i + 1) / 10)) / 10)

    # Very Important: Setting pretty colors depending on whether we are above or below the target
    # Warning, this will crash if run while there are no values in the sprint. This should never happen though. 
    if y_values[-1] <= y_linear[len(y_values) - 1]:
        line_color = '#66c2a5'
    else:
        line_color = '#fc8d62'
    
    # Style
    plt.xkcd()

    # Ploting
    plt.plot(x_values, y_linear, color='#8da0cb' ,label='Target')
    plt.plot(x_values[:len(y_values)], y_values, color=line_color, label='Actual')

    # Extras
    plt.xlabel('Date')
    plt.ylabel('Story Points Remaining')
    plt.title('Sprint Burndown Chart for\n{} through {}'.format(sprint['start_date'], sprint['end_date']))
    plt.tight_layout()
    plt.legend()

    # Saving the graph as plot.png
    plt.savefig('plot.png')

def encode_64(file):
    with open(file, 'rb') as f:
        return base64.b64encode(f.read())