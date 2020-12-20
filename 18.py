import ast


def replace_ast_binops(root, tweaks):
    ast_ops = {'+': 'Add', '*': 'Mult', '-': 'Sub', '/': 'Div'}
    tweaks = {ast_ops[a]: getattr(ast, ast_ops[b])() for a, b in tweaks}
    for node in ast.walk(root):
        if isinstance(node, ast.BinOp):
            node.op = tweaks.get(node.op.__class__.__name__, node.op)


def tweaked_evaluator(*tweaks):
    def inner(line):
        for a, b in tweaks:
            line = line.replace(a, b)
        node = ast.parse(line, mode='eval')
        replace_ast_binops(node, [(b, a) for a, b in tweaks])
        return eval(compile(node, '<string>', mode='eval'))

    return inner


with open('18.input') as f:
    lines = f.read().split('\n')

# part 1
# evaluate multiplication and addition at same order of precedence
my_eval = tweaked_evaluator(('*', '-'))  # evaluate '*' at precedence of '-'
print(sum(my_eval(line) for line in lines))

# part 2
# evaluate additions before multiplication
my_eval = tweaked_evaluator(('*', '-'), ('+', '/'))  # flip order of precedence
print(sum(my_eval(line) for line in lines))
