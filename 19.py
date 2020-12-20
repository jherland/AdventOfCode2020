from contextlib import suppress
from dataclasses import dataclass
from typing import Dict, List, Union

rules: Dict[int, Union['Atom', 'Disjunction']] = {}


@dataclass(frozen=True)
class Atom:
    letter: str

    def __str__(self):
        return f'{self.letter!r}'

    def check(self, msg, start):
        with suppress(IndexError):
            if msg[start] == self.letter:
                yield start + 1


@dataclass(frozen=True)
class Conjunction:
    terms: List[int]

    def __str__(self):
        return ' '.join(map(str, self.terms))

    def check_recursive(self, terms, msg, start):
        if start > len(msg):
            return
        if not terms:
            yield start
            return

        rule = rules[terms[0]]
        for consumed in rule.check(msg, start):
            yield from self.check_recursive(terms[1:], msg, consumed)

    def check(self, msg, start):
        yield from self.check_recursive(self.terms, msg, start)


@dataclass(frozen=True)
class Disjunction:
    terms: List[Conjunction]

    def __str__(self):
        return ' | '.join(map(str, self.terms))

    def check(self, msg, start):
        for term in self.terms:
            yield from term.check(msg, start)


def parse_rule(s):
    if s.startswith('"') and s.endswith('"') and len(s) == 3:  # Atom
        return Atom(s[1])

    alternatives = []
    for alt in s.split('|'):
        alternatives.append(
            Conjunction([int(num) for num in alt.strip().split(' ')]))
    return Disjunction(alternatives)


def parse_rules(f):
    for line in f:
        if not line.rstrip():
            break
        num, rulestr = line.split(':', 1)
        yield int(num), parse_rule(rulestr.strip())


def check(msg, rule):
    return any(consumed == len(msg) for consumed in rule.check(msg, 0))


with open('19.input') as f:
    rules.update(parse_rules(f))
    messages = list(line.rstrip() for line in f)

# part 1
print(sum(check(msg, rules[0]) for msg in messages))

# part 2
rules[8] = parse_rule('42 | 42 8')
rules[11] = parse_rule('42 31 | 42 11 31')
print(sum(check(msg, rules[0]) for msg in messages))
