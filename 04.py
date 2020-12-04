import re


def parse_passports(f):
    for passport in f.read().split('\n\n'):
        yield dict(field.split(':', 1) for field in passport.split())


def has_valid_fields(passport):
    fields = set(passport.keys())
    fields.discard('cid')
    return fields == {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}


def has_valid_values(passport, check_fields=None):

    def check_height(v):
        if v.endswith('cm'):
            return 150 <= float(v[:-2]) <= 193
        elif v.endswith('in'):
            return 59 <= float(v[:-2]) <= 76
        else:
            return False

    checks = {
        'byr': lambda v: len(v) == 4 and 1920 <= int(v) <= 2002,
        'iyr': lambda v: len(v) == 4 and 2010 <= int(v) <= 2020,
        'eyr': lambda v: len(v) == 4 and 2020 <= int(v) <= 2030,
        'hgt': check_height,
        'hcl': lambda v: bool(re.compile(r'#[0-9a-f]{6}').fullmatch(v)),
        'ecl': lambda v: v in set('amb blu brn gry grn hzl oth'.split()),
        'pid': lambda v: bool(re.compile(r'[0-9]{9}').fullmatch(v)),
        'cid': lambda v: True,
    }

    if check_fields is None:
        check_fields = checks.keys()
    return all(checks[f](passport.get(f, '')) for f in check_fields)


with open('04.input') as f:
    passports = list(parse_passports(f))

# part 1
print(len([pp for pp in passports if has_valid_fields(pp)]))

# part 2
print(len([pp for pp in passports if has_valid_values(pp)]))
