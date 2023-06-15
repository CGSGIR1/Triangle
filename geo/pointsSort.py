import random
def _quick_sort(a, first, last):
    if last - first <= 1:
        return
    i, j = partion(a, first, last)
    _quick_sort(a, first, i)
    _quick_sort(a, j, last)
    return


def partion(a, first, last):
    x = a[random.randrange(first, last)].x
    i = first
    for k in range(first, last):
        if a[k].x < x:
            a[i], a[k] = a[k], a[i]
            i += 1
    j = i
    for k in range(first, last):
        if a[k].x == x:
            a[j], a[k] = a[k], a[j]
            j += 1
    return i, j

def quick_sort_point(a):
    _quick_sort(a, 0, len(a))