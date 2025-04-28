def draw_triangle(canvas, x, y, size, orientation):
    half_size = size / 2
    narrow= .95  # Adjust this factor to make the triangle narrower

    if orientation == 'up':
        points = [(x-half_size*narrow, y+half_size),
                  (x, y-half_size),
                  (x + half_size*narrow, y+half_size)]
    elif orientation == 'right':
        points = [(x-half_size, y+half_size*narrow),
                  (x-half_size, y-half_size*narrow),
                  (x+half_size,y)]

    elif orientation == 'down':
        points = [(x-half_size*narrow, y-half_size),
                  (x, y+half_size),
                  (x + half_size*narrow, y-half_size)]

            
    elif orientation == 'left':
        points = [(x+half_size, y+half_size*narrow),
                  (x+half_size, y-half_size*narrow),
                  (x-half_size,y)]

    # so the canvas item can be stored and deleted if needbe
    return canvas.create_polygon(points, fill="orange", outline="orange")
