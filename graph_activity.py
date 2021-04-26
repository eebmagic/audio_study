from ast import literal_eval
import matplotlib.pyplot as plt

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

if __name__ == '__main__':
    from tqdm import tqdm

    with open('outputs/jayjay.txt') as file:
        content = file.read()

    # Parse data
    parsed = parse_data(content, verbose=False)

    # Plot mouse positions
    times, positions = zip(*parsed['positions'])
    plt.plot(times, positions)
    top = max(positions)

    # Plot button presses
    times, positions = zip(*parsed['buttons'])
    adjusted = [x*top for x in positions]
    plt.plot(times, adjusted)

    plt.show()
