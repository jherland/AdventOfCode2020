DEF CUPS_LEN = 1_000_000
cdef int cups[CUPS_LEN]
cdef int triple[3]


cdef void read_triple(int i):
    triple[0] = cups[i + 0]
    triple[1] = cups[i + 1]
    triple[2] = cups[i + 2]


cdef void write_triple(int i):
    cups[i + 0] = triple[0]
    cups[i + 1] = triple[1]
    cups[i + 2] = triple[2]


cdef void move_section(int src, int dst, int len):
    cdef int i
    if dst < src:  # move left
        for i in range(len):
            cups[dst + i] = cups[src + i]
    else:  # move right
        for i in range(len):
            cups[dst + (len - 1) - i] = cups[src + (len - 1) - i]


cdef int search(int needle, int start, int end):
    cdef int i
    for i in range(start, end):
        if cups[i] == needle:
            return i
    return -1


cdef int day23_move(int cur):
    cdef int i, needle, dest
    # Rotate cur to start if near end
    if CUPS_LEN - cur <= 3:
        read_triple(CUPS_LEN - 3)
        move_section(0, 3, CUPS_LEN - 3)
        write_triple(0)
        cur -= CUPS_LEN - 3

    read_triple(cur + 1)
    needle = cups[cur] - 1
    while True:
        dest = search(needle, 0, cur)  # search left side
        if dest >= 0:  # found it, shift cups[dest+1:cur+1] right
            move_section(dest + 1, dest + 4, cur - dest)
            write_triple(dest + 1)
            return (cur + 4) % CUPS_LEN
        else:
            dest = search(needle, cur + 4, CUPS_LEN)  # search right side
            if dest >= 0:  # found it shift cups[cur+4:dest+1] left
                move_section(cur + 4, cur + 1, dest - (cur + 3))
                write_triple(dest + 1 - 3)
                return (cur + 1) % CUPS_LEN
            else:
                needle -= 1
                if needle <= 0:
                    needle = CUPS_LEN


cpdef long day23_part2(start):
    cdef int current = 0
    cdef int i
    cdef long i1, i2
    for i in range(9):
        cups[i] = start[i]
    for i in range(9, CUPS_LEN):
        cups[i] = i + 1
    for i in range(10_000_000):
        current = day23_move(current)
    i = search(1, 0, CUPS_LEN)
    i1 = cups[i + 1]
    i2 = cups[i + 2]
    return i1 * i2
