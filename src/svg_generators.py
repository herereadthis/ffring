import math

def draw_line(angle, unit_size):
    # Convert negative angles to their positive equivalent
    while angle < 0:
        angle += 360

    print('angle')
    print(angle)

    # Calculate the center point of the square
    center_x, center_y = 0,0

    # Calculate the endpoint of the line based on the given angle
    end_x = math.sin(math.radians(angle))
    end_y = 0 - math.cos(math.radians(angle))

    # Scale the coordinates by the unit size
    center_x += unit_size
    center_y += unit_size
    end_x = end_x * unit_size + unit_size
    end_y = end_y * unit_size + unit_size

    # Build the SVG code as a string
    svg_code = '<svg viewBox="0 0 ' + str(2*unit_size) + ' ' +  str(2*unit_size) +'" xmlns="http://www.w3.org/2000/svg">'
    svg_code += f'<circle cx="{unit_size}" cy="{unit_size}" r="{0.05 * unit_size}" fill="red" />'
    svg_code += '<line x1="' + str(center_x) + '" y1="' + str(center_y) + '" x2="' + str(end_x) + '" y2="' + str(end_y) + '" stroke="red" stroke-width="2" />'
    svg_code += '</svg>'

    # Return the SVG code as a string
    return svg_code