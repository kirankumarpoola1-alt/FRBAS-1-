prev_x = None

def detect_head_movement(box):
    global prev_x
    _, right, _, left = box
    cx = (left + right) // 2

    if prev_x is None:
        prev_x = cx
        return False

    moved = abs(cx - prev_x) > 15
    prev_x = cx
    return moved
