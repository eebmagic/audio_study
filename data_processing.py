from ast import literal_eval
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as ticker
import numpy as np


def rolling_average(times, data, depth):
    assert len(times)==len(data), "times and data must match in length"

    out = [0] * depth
    for i in range(depth, len(data)):
        sub = data[i-depth:i]
        avg = sum(sub) / len(sub)
        out.append(avg)

    return out


def parse_data(dataString, verbose=False):
    mouse_positions = []
    mouse_buttons = []

    lines = dataString.strip().split('\n')
    for line in lines:
        event, time = line.split('|')
        time = float(time)

        if verbose:
            print(line)
            print(event, time)

        if len(mouse_buttons) == 0:
            mouse_buttons.append((time, 0))

        if 'mouse at' in event:
            position = literal_eval(event[event.index('('):event.index(')')+1])
            x, y = position
            if verbose:
                print(f'position: {x, y}')
            mouse_positions.append((time, x))

        elif 'mouse pressed' in event:
            last_position = mouse_buttons[-1][1]

            if 'left' in event.lower():
                new_position = last_position + 1
                # new_position = 1
            elif 'right' in event.lower():
                new_position = last_position - 1
                # new_position = -1

            mouse_buttons.append((time, new_position))
            if verbose:
                print(f'{last_position=}, {new_position=}')

        elif 'mouse released' in event:
            last_position = mouse_buttons[-1][1]

            if 'left' in event.lower():
                new_position = last_position - 1
                # new_position = 0
            elif 'right' in event.lower():
                new_position = last_position + 1
                # new_position = 0

            mouse_buttons.append((time, new_position))
            if verbose:
                print(f'{last_position=}, {new_position=}')

        if verbose:
            print('')

    outs = {
        'positions': mouse_positions,
        'buttons': mouse_buttons
    }

    return outs


def graph(filename, chart=False):
    with open(filename) as file:
        content = file.read()

    # Parse data
    parsed = parse_data(content, verbose=False)
    print(parsed.keys())
    # print(parsed['positions'])

    points = parsed['positions']
    speeds = []
    times = []
    for i in range(1, len(points)):
        a = points[i-1]
        b = points[i]
        dist_diff = abs(a[1] - b[1])
        time_diff = b[0] - a[0]
        speed = dist_diff / time_diff

        speeds.append(speed)
        times.append(a[0])

    # depth = 1_000
    # averages = rolling_average(times, speeds, depth)

    parts = []
    for i in range(4):
        start = i * (len(speeds) // 4)
        end = (i+1) * (len(speeds) // 4)
        sub = speeds[start:end]
        avg = sum(sub) / len(sub)
        parts.append(avg)
    print(f'{filename} => {parts}')
    return parts


    if chart:
        # plt.plot(times, speeds)
        # plt.plot(times, averages)

        secs = mdate.epoch2num(times)
        fig, ax = plt.subplots()
        # ax.plot_date(secs, speeds)
        ax.plot_date(secs, averages, 'b-')

        # apply formatting
        # date_fmt = '%d-%m-%y %H:%M:%S'
        date_fmt = '%H:%M:%S'
        date_formatter = mdate.DateFormatter(date_fmt)
        ax.xaxis.set_major_formatter(date_formatter)
        fig.autofmt_xdate(rotation=45)

        # start, end = ax.get_xlim()
        # ax.xaxis_date()
        # plt.xticks(np.arange(0, len(secs)+1, 5))

        plt.show()


        # Plot mouse positions
        # times, positions = zip(*parsed['positions'])
        # plt.plot(times, positions)
        # top = max(positions)

        # # Plot button presses
        # times, positions = zip(*parsed['buttons'])
        # adjusted = [x*top for x in positions]
        # plt.plot(times, adjusted)

        # plt.show()

if __name__ == '__main__':
    # graph('outputs/jayjay.txt')
    # graph('outputs/sarah.txt')
    # graph('outputs/matthew.txt')

    files = ['outputs/jayjay.txt', 'outputs/sarah.txt', 'outputs/matthew.txt']
    for file in files:
        out = graph(file)
        plt.plot(list(range(1, 5)), out)

    plt.show()


