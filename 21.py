from dataclasses import dataclass
from typing import Dict, Set


@dataclass
class Food:
    ingredients: Set[str]
    allergens: Set[str]

    @classmethod
    def parse(cls, line: str) -> 'Food':
        left, right = line.rstrip().split('(', 1)
        assert right.startswith('contains ') and right.endswith(')')
        return cls(set(left.split()), set(right[9:-1].split(', ')))


def deduce_mapping(possibles: Dict[str, Set[str]]) -> Dict[str, str]:
    possibles = possibles.copy()
    deduced: Dict[str, str] = {}
    while len(deduced) < len(possibles):
        d = {a: bs.pop() for a, bs in possibles.items() if len(bs) == 1}
        for b in d.values():  # eliminate deduced value from other possibles
            for cs in possibles.values():
                cs.discard(b)
        if not d:  # no progress
            break
        deduced.update(d)
    return deduced


with open('21.input') as f:
    foods = list(Food.parse(line) for line in f)

# Map allergens to set of possible corresponding ingredients
allergens: Dict[str, Set[str]] = {}
all_ingredients: Set[str] = set()

for food in foods:
    all_ingredients |= food.ingredients
    for a in food.allergens:
        if a not in allergens:
            allergens[a] = set(food.ingredients)
        else:
            allergens[a] &= food.ingredients

known_allergens = deduce_mapping(allergens)

# part 1
allergen_free = all_ingredients - set(known_allergens.values())
allergen_free_uses = []
for food in foods:
    allergen_free_uses.extend(list(food.ingredients & allergen_free))
print(len(allergen_free_uses))

# part 2
print(','.join(ingr for _, ingr in sorted(known_allergens.items())))
