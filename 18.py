from operator import add, mul
import tokenize


def tokenize_line(line):
    for token in tokenize.generate_tokens(iter([line]).__next__):
        if token.type == tokenize.NUMBER:
            yield int(token.string)
        elif token.type == tokenize.OP:
            yield token.string
        elif token.type in {tokenize.NEWLINE, tokenize.ENDMARKER}:
            continue


def parse_parentheses(tokens):
    result = []
    for token in tokens:
        if token == '(':
            result.append(parse_parentheses(tokens))
        elif token == ')':
            break
        else:
            result.append(token)

    assert result
    return result


def parse_op(operand, ops):
    # print(f'  parse_op({operand=}, {ops=})')
    if isinstance(operand, list):
        return parse_ops(operand, ops)
    elif isinstance(operand, tuple):
        op, a, b = operand
        assert callable(op)
        return (op, parse_op(a, ops), parse_op(b, ops))
    return operand


def parse_ops(operands, ops):
    # print(f'  parse_ops({operands=}, {ops=})')
    if isinstance(operands, tuple):  # already parsed
        return parse_op(operands, ops)

    assert isinstance(operands, list) and len(operands)
    a = parse_op(operands.pop(0), ops)
    if not len(operands):
        return a

    op = operands.pop(0)
    assert isinstance(op, str) and len(operands)

    if op in ops:  # parse [a, op, b, ...] -> [(ops[op], a, b), ...]
        b = parse_op(operands.pop(0), ops)
        result = (ops[op], a, b)
        if operands:
            return parse_ops([result] + operands, ops)
        else:
            return result
    else:  # leave [a, op, ...] for the next parse step
        return [a, op, parse_ops(operands, ops)]


def evaluate(value):
    if isinstance(value, list):
        assert len(value) == 1
        value = value.pop()
    if isinstance(value, tuple):
        assert len(value) == 3 and callable(value[0])
        op, a, b = value
        value = op(evaluate(a), evaluate(b))
    assert isinstance(value, int)
    return value


with open('18.input') as f:
    lines = f.read().split('\n')

# part 1
print(
    sum(
        evaluate(
            parse_ops(
                parse_parentheses(tokenize_line(line)),
                {'+': add, '*': mul},
            )
        )
        for line in lines
    )
)

# part 2
print(
    sum(
        evaluate(
            parse_ops(
                parse_ops(
                    parse_parentheses(tokenize_line(line)),
                    {'+': add},
                ),
                {'*': mul},
            )
        )
        for line in lines
    )
)
