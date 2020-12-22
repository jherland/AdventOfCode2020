def parse_deck(f):
    for line in f:
        if not line.rstrip():
            break
        yield int(line.rstrip())


def simple_round(c1, c2):
    loot = sorted([c1, c2], reverse=True)
    return (loot, []) if c1 > c2 else ([], loot)


def combat(p1, p2):
    while p1 and p2:
        loot1, loot2 = simple_round(p1.pop(0), p2.pop(0))
        p1 += loot1
        p2 += loot2
    return p1, p2, (0 if p1 else 1)


def recursive_combat(p1, p2):
    seen = set()
    while p1 and p2:
        state = '|'.join([','.join(map(str, p1)), ','.join(map(str, p2))])
        if state in seen:
            return p1, p2, 0  # player 1 wins on repeated game state
        seen.add(state)

        c1, c2 = p1.pop(0), p2.pop(0)  # deal cards
        if len(p1) >= c1 and len(p2) >= c2:  # recursive combat
            sub1, sub2, winner = recursive_combat(p1[:c1], p2[:c2])
            loot1 = [c1, c2] if winner == 0 else []
            loot2 = [c2, c1] if winner == 1 else []
        else:  # non-recursive/simple round
            loot1, loot2 = simple_round(c1, c2)

        p1 += loot1
        p2 += loot2
    return p1, p2, (0 if p1 else 1)


def score(p):
    return sum(m * c for m, c in enumerate(reversed(p), start=1))


with open('22.input') as f:
    assert next(f) == 'Player 1:\n'
    p1 = list(parse_deck(f))
    assert next(f) == 'Player 2:\n'
    p2 = list(parse_deck(f))

# part 1
*players, winner = combat(list(p1), list(p2))
print(score(players[winner]))

# part 2
*players, winner = recursive_combat(list(p1), list(p2))
print(score(players[winner]))
