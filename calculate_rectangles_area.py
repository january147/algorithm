
def calculate_interval_union(intervals):

    if len(intervals) == 0:
        return 0
    
    intervals.sort(key=lambda x: x[0])
    current_start, current_end = intervals[0]
    total_length = 0

    for start, end in intervals[1:]:
        if start > current_end:
            total_length += current_end - current_start
            current_start, current_end = start, end
        else:
            current_end = max(current_end, end)    
    total_length += current_end - current_start

    return total_length


def calcualte_union_area(rects):

    events = []
    for left, top, right, bottom in rects:
        events.append((top, 1, left, right))
        events.append((bottom, -1, left, right))

    events.sort()
    active_intervals = []
    total_area = 0

    scan_start = events[0][0]
    for scan_pos, event, left, right in events:
        interval_length = calculate_interval_union(intervals=active_intervals)
        total_area += (scan_pos - scan_start) * interval_length
        print("scan_start: {}, scan_pos: {}, interval_length: {}, total_area: {}".format(scan_start, scan_pos, interval_length, total_area))
        if event == 1:
            active_intervals.append((left, right))
        else:
            active_intervals.remove((left, right))
        scan_start = scan_pos

    return total_area


test = [
    [1, 1, 5, 5],
    [2, 2, 3, 3],
    [3, 3, 4, 4],
    [2, 2, 6, 6],
    [5, 1, 11, 5],
]


print(calcualte_union_area(rects=test))
