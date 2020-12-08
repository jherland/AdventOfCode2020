def parse_instructions(f):
    for line in f:
        instr, arg = line.rstrip().split(' ')
        assert instr in {'acc', 'jmp', 'nop'}
        yield instr, int(arg)


def execute(program, pc=0, acc=0):
    while 0 <= pc < len(program):
        jmp = +1  # jump to next instruction by default
        instr, arg = program[pc]
        if instr == 'acc':
            acc += arg
        elif instr == 'jmp':
            jmp = arg
        elif instr == 'nop':
            pass
        else:
            raise ValueError(instr)
        pc += jmp
        yield acc, pc


def execute_until_repeat(program):
    seen = {0}
    for acc, pc in execute(program):
        if pc in seen:
            return True, acc
        seen.add(pc)
    return False, acc


def mutate(program):
    for addr, (instr, arg) in enumerate(program):
        if instr in {'jmp', 'nop'}:
            clone = list(program)
            clone[addr] = ('nop' if instr == 'jmp' else 'jmp', arg)
            yield clone


with open('08.input') as f:
    program = list(parse_instructions(f))

# part 1
repeat, acc = execute_until_repeat(program)
assert repeat is True
print(acc)

# part 2
for mutation in mutate(program):
    repeat, acc = execute_until_repeat(mutation)
    if not repeat:
        print(acc)
        break
