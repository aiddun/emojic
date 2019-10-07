def render_array_in_array(original_array, input_array, startx, starty):

    for y in range(len(input_array)):

        if starty + y > len(original_array):
            continue

        for x in range(len(input_array[0])):
            # print(starty + y, startx + x)
            if startx + x > len(original_array[0]):
                continue

            original_array[starty + y][startx + x] = input_array[y][x]

    return original_array


def render_text(array, text, x, y):
    # x, y - start coordinates of text
    # Assuming horizontal test
    return render_array_in_array(array, [list(text)], x, y)


def generate_screen_buffer(height, width):
    #   Using native lists to minimise dependencies
    screenbuffer = []
    # Row
    for i in range(height):
        screenbuffer.append([])
        # Column
        for j in range(width):
            screenbuffer[i].append(" ")

    return screenbuffer
