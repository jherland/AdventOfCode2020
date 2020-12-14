import re
from typing import Iterable, Iterator, TextIO, Tuple, Union

mask_pattern = re.compile(r'mask = ([10X]{36})')
mem_pattern = re.compile(r'mem\[(\d+)\] = (\d+)')


class Mask:
    Bits = 36

    def __init__(self, s: str):
        assert len(s) == self.Bits
        assert all(c in set('01X') for c in s)
        self.mask = s
        self.ones = int(s.replace('X', '0'), 2)
        self.zeroes = ~int(s.replace('X', '1'), 2)
        self.xes = int(s.replace('1', '0').replace('X', '1'), 2)

    def __repr__(self) -> str:
        return f'Mask({self.mask})'

    def mask_num(self, num: int) -> int:
        assert num.bit_length() <= self.Bits
        return (num | self.ones) & ~self.zeroes

    def tweaked_nums(self, num: int) -> Iterator[int]:
        def expand_xes():
            num_xbits = self.mask.count('X')
            for n in range(pow(2, num_xbits)):
                bits = iter(f'{n:0{num_xbits}b}')
                s = ''.join(next(bits) if c == 'X' else '0' for c in self.mask)
                yield int(s, 2)

        num = (num & self.zeroes) | self.ones
        for xbits in expand_xes():
            yield num | xbits


Assignment = Tuple[int, int]
Instruction = Union[Mask, Assignment]


def parse(f: TextIO) -> Iterator[Instruction]:
    for line in f:
        m = mask_pattern.fullmatch(line.rstrip())
        if m:
            yield Mask(m.group(1))
        else:
            m = mem_pattern.fullmatch(line.rstrip())
            if m:
                yield int(m.group(1)), int(m.group(2))
            else:
                raise NotImplementedError(f'invalid line {line}')


def mask_values(
    stream: Iterable[Instruction], init_mask: Mask = Mask('X' * 36)
) -> Iterator[Assignment]:
    mask = init_mask
    for m in stream:
        if isinstance(m, Mask):
            mask = m
        else:
            address, value = m
            yield address, mask.mask_num(value)


def tweak_addresses(
    stream: Iterable[Instruction], init_mask: Mask = Mask('0' * 36)
) -> Iterator[Assignment]:
    mask = init_mask
    for m in stream:
        if isinstance(m, Mask):
            mask = m
        else:
            address, value = m
            for a in mask.tweaked_nums(address):
                yield a, value


with open('14.input') as f:
    instructions = list(parse(f))

# part 1
assignments = dict(mask_values(instructions))
print(sum(assignments.values()))

# part 2
assignments = dict(tweak_addresses(instructions))
print(sum(assignments.values()))
