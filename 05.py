with open('05.input') as f:
    seenIDs = {
        int(line.rstrip().translate(str.maketrans('FBLR', '0101')), 2)
        for line in f
    }

# part 1
print(max(seenIDs))

# part 2
print((set(range(min(seenIDs), max(seenIDs) + 1)) - seenIDs).pop())
