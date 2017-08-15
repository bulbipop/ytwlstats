import pygal
from datetime import timedelta

import db

def makeChart():
    dates, stats = [], []
    records = db.getRecords()
    if records:
        for record in records:
            dates.append(record[1])
            stats.append(dict(label=str(record[2]), value=record[3]))

        minimum = min(stats, key=lambda x: x['value'])
        minimum = max(0, minimum['value'] - 10000)
    else:
        minimum = 0
    formatter = lambda x: str(timedelta(seconds=x))
    chart = pygal.Line(show_legend=False,
                        x_label_rotation=35,
                        fill=True,
                        show_y_guides=False,
                        zero=minimum,
                        print_labels=True,
                        value_formatter=formatter)
    chart.x_labels = list(map(lambda x: x[5:-3], dates))
    chart.add('Total length', stats)
    return chart.render()
