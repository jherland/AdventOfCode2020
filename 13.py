import math

with open('13.input') as f:
    t_now = int(next(f))
    schedule = list(enumerate(next(f).split(',')))

# part 1
buses = [int(b) for _, b in schedule if b != 'x']
t_dep, bus = min((b * math.ceil(t_now / b), b) for b in buses)
print(bus * (t_dep - t_now))


# part 2
def crt(congruences):
    '''Chinese remainder theorem.

    For a system of linear congruences (given as [(n_1, a_1), ..., (n_k, a_k)])
        x ≡ a_1 (mod n_1)
        ...
        x ≡ a_k (mod n_k)
    where all n_i are pairwise coprime, find x mod N, where N is the product
    of all n_i.
    '''
    def ext_euclid(a, b):
        assert a > b
        r, s, t = [a, b], [1, 0], [0, 1]
        while True:
            q = r[-2] // r[-1]
            r.append(r[-2] - q * r[-1])
            s.append(s[-2] - q * s[-1])
            t.append(t[-2] - q * t[-1])
            if r[-1] == 0:
                assert s[-2] * a + t[-2] * b == r[-2]
                return r[-2], s[-2], t[-2]

    N = math.prod(n for n, a in congruences)
    x = 0
    for n_i, a_i in congruences:
        a_i = (N + a_i) % n_i  # 0 <= a_i < n_i
        N_i = N // n_i
        gcd, r_i, s_i = ext_euclid(N_i, n_i)  # r_i * N_i + s_i * n_i = 1
        assert gcd == 1
        x += a_i * r_i * N_i
    return N, x % N


congruences = [(int(mod), -offset) for offset, mod in schedule if mod != 'x']
N, x = crt(congruences)
print(x)
