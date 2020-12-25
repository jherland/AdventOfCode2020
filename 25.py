from itertools import islice

def loop(subject_number):
    value = 1
    while True:
        yield value
        value = (value * subject_number) % 20201227


def nth(iterable, n, default=None):
    return next(islice(iterable, n, None), default)


with open('25.input') as f:
    pubkeys = {int(line.rstrip()) for line in f}

loop_size, pubkey = next((i, n) for i, n in enumerate(loop(7)) if n in pubkeys)
other_pubkey = (pubkeys - {pubkey}).pop()
encryption_key = nth(loop(other_pubkey), loop_size)
print(encryption_key)
