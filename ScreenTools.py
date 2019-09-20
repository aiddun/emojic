def render_array_in_array(original_array, input_array, startx, starty):
    # print(len(input_array))
    # print(len(input_array[0]))


    for y in range(len(input_array)):
        # print(f'outlen + {len(original_array[0])}')

        # print(f'inlen + {len(input_array[0])}')

        for x in range(len(input_array[0])):

            # print(starty + y, startx + x)
            original_array[starty + y][startx + x] = input_array[y][x]

    # print("card done")

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