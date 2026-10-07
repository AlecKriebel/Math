"""Conditional deterministic factorization reduction over represented finite fields.

This module implements the established Berlekamp fixed-algebra and trace-coordinate
reduction.  Its missing uniform ingredient is supplied through ``prime_oracle``:
an algorithm returning all roots of a monic, squarefree, completely split polynomial
over F_p.  The included exhaustive oracle is FOR SMALL EXAMPLES ONLY; its O(p)
enumeration is not polynomial in log(p).  Nothing in this file certifies an
unconditional bit-polynomial prime-field algorithm or a new mathematical result.

Representations: p is promised prime, h is an explicitly supplied monic polynomial
of degree m >= 1, and K = F_p[t]/h.  Coefficients are m-tuples in the power basis.
The constructor verifies irreducibility of h without factoring m or p-1.
Polynomials in x are little-endian tuples of K elements, with () denoting zero.
Only Python's standard library is used.  Operation counters describe this
reference implementation, not an optimized or practical complexity claim.
"""

from dataclasses import dataclass, field as dataclass_field
from typing import Callable, Iterable, Sequence

Element = tuple[int, ...]
Polynomial = tuple[Element, ...]
PrimeOracle = Callable[[int, tuple[int, ...]], Iterable[int]]


@dataclass
class Statistics:
    """Checkable dimensions, degree bounds, oracle calls and arithmetic counts."""

    counters: dict[str, int] = dataclass_field(default_factory=dict)
    matrices: list[dict[str, int | str]] = dataclass_field(default_factory=list)
    squarefree_runs: list[dict[str, int]] = dataclass_field(default_factory=list)
    oracle_queries: list[dict[str, int | list[int]]] = dataclass_field(default_factory=list)
    trace_coordinates: list[dict[str, int]] = dataclass_field(default_factory=list)

    def count(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount

    def matrix(self, name: str, rows: int, columns: int) -> None:
        self.matrices.append({"name": name, "rows": rows, "columns": columns})

    def as_dict(self) -> dict:
        return {"counters": self.counters, "matrices": self.matrices,
                "squarefree_runs": self.squarefree_runs,
                "oracle_queries": self.oracle_queries,
                "trace_coordinates": self.trace_coordinates}


def _itrim(a: Sequence[int], p: int) -> tuple[int, ...]:
    b = [x % p for x in a]
    while b and b[-1] == 0:
        b.pop()
    return tuple(b)


def _iadd(a: Sequence[int], b: Sequence[int], p: int, sign: int = 1) -> tuple[int, ...]:
    return _itrim([(a[i] if i < len(a) else 0) + sign * (b[i] if i < len(b) else 0)
                   for i in range(max(len(a), len(b)))], p)


def _imul(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    if not a or not b:
        return ()
    c = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] = (c[i + j] + ai * bj) % p
    return _itrim(c, p)


def _idiv(a: Sequence[int], b: Sequence[int], p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    a, b = list(_itrim(a, p)), _itrim(b, p)
    if not b:
        raise ZeroDivisionError("zero polynomial divisor")
    q = [0] * max(0, len(a) - len(b) + 1)
    inv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        shift = len(a) - len(b)
        coefficient = a[-1] * inv % p
        q[shift] = coefficient
        for j, bj in enumerate(b):
            a[shift + j] = (a[shift + j] - coefficient * bj) % p
        while a and a[-1] == 0:
            a.pop()
    return _itrim(q, p), tuple(a)


def _igcd(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    a, b = _itrim(a, p), _itrim(b, p)
    while b:
        a, b = b, _idiv(a, b, p)[1]
    if not a:
        return ()
    inv = pow(a[-1], -1, p)
    return tuple(ai * inv % p for ai in a)


def _ipowmod(a: Sequence[int], exponent: int, h: Sequence[int], p: int) -> tuple[int, ...]:
    r, a = (1,), _idiv(a, h, p)[1]
    while exponent:
        if exponent & 1:
            r = _idiv(_imul(r, a, p), h, p)[1]
        exponent >>= 1
        if exponent:
            a = _idiv(_imul(a, a, p), h, p)[1]
    return r


def prime_polynomial_irreducible(p: int, h: Sequence[int]) -> bool:
    """Frobenius criterion, checking every j <= m/2 instead of factoring m.

    The argument p is promised prime.  This function is not a primality test.
    """
    h = _itrim(h, p)
    m = len(h) - 1
    if m < 1:
        return False
    x = _idiv((0, 1), h, p)[1]
    xp = x
    for j in range(1, m + 1):
        xp = _ipowmod(xp, p, h, p)
        if j <= m // 2 and _igcd(_iadd(xp, x, p, -1), h, p) != (1,):
            return False
    return xp == x


class FiniteField:
    """Power-basis field with promised prime characteristic and checked modulus."""

    def __init__(self, p: int, modulus: Sequence[int], statistics: Statistics | None = None):
        if not isinstance(p, int) or p < 2:
            raise ValueError("p must be a promised prime integer >= 2")
        self.p = p
        self.h = _itrim(modulus, p)
        self.m = len(self.h) - 1
        if self.m < 1 or self.h[-1] != 1:
            raise ValueError("the field modulus must be monic of positive degree")
        if not prime_polynomial_irreducible(p, self.h):
            raise ValueError("the field modulus is reducible")
        self.stats = statistics if statistics is not None else Statistics()
        self.stats.count("representation_irreducibility_frobenius_steps", self.m)
        self.q = p ** self.m
        self.zero = (0,) * self.m
        self.one = (1,) + (0,) * (self.m - 1)

    def element(self, a: int | Sequence[int]) -> Element:
        if isinstance(a, int):
            return (a % self.p,) + (0,) * (self.m - 1)
        if len(a) > self.m:
            raise ValueError("a field element must have at most m power-basis coefficients")
        return tuple(x % self.p for x in a) + (0,) * (self.m - len(a))

    def poly(self, coefficients: Iterable[int | Sequence[int]]) -> Polynomial:
        return trim(self, tuple(self.element(a) for a in coefficients))

    def add(self, a: Element, b: Element) -> Element:
        self.stats.count("field_additions")
        return tuple((ai + bi) % self.p for ai, bi in zip(a, b))

    def neg(self, a: Element) -> Element:
        self.stats.count("field_negations")
        return tuple(-ai % self.p for ai in a)

    def sub(self, a: Element, b: Element) -> Element:
        return self.add(a, self.neg(b))

    def mul(self, a: Element, b: Element) -> Element:
        self.stats.count("field_multiplications")
        c = [0] * (2 * self.m - 1)
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                c[i + j] = (c[i + j] + ai * bj) % self.p
        for k in range(2 * self.m - 2, self.m - 1, -1):
            coefficient = c[k]
            for j in range(self.m):
                c[k - self.m + j] = (c[k - self.m + j] - coefficient * self.h[j]) % self.p
        return tuple(c[:self.m])

    def pow(self, a: Element, exponent: int) -> Element:
        if exponent < 0:
            return self.pow(self.inv(a), -exponent)
        r = self.one
        while exponent:
            if exponent & 1:
                r = self.mul(r, a)
            exponent >>= 1
            if exponent:
                a = self.mul(a, a)
        return r

    def inv(self, a: Element) -> Element:
        if a == self.zero:
            raise ZeroDivisionError("zero field element")
        self.stats.count("field_inversions")
        return self.pow(a, self.q - 2)

    def basis(self) -> tuple[Element, ...]:
        return tuple(tuple(int(i == j) for i in range(self.m)) for j in range(self.m))

    def elements_for_testing(self) -> Iterable[Element]:
        """Enumeration has q steps and is explicitly restricted to test code."""
        from itertools import product
        return product(range(self.p), repeat=self.m)


def trim(K: FiniteField, a: Sequence[Element]) -> Polynomial:
    n = len(a)
    while n and a[n - 1] == K.zero:
        n -= 1
    return tuple(a[:n])


def add(K: FiniteField, a: Polynomial, b: Polynomial) -> Polynomial:
    return trim(K, [K.add(a[i] if i < len(a) else K.zero,
                          b[i] if i < len(b) else K.zero)
                    for i in range(max(len(a), len(b)))])


def neg(K: FiniteField, a: Polynomial) -> Polynomial:
    return trim(K, [K.neg(ai) for ai in a])


def sub(K: FiniteField, a: Polynomial, b: Polynomial) -> Polynomial:
    return add(K, a, neg(K, b))


def scale(K: FiniteField, a: Polynomial, c: Element) -> Polynomial:
    return trim(K, [K.mul(ai, c) for ai in a])


def mul(K: FiniteField, a: Polynomial, b: Polynomial) -> Polynomial:
    if not a or not b:
        return ()
    c = [K.zero] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] = K.add(c[i + j], K.mul(ai, bj))
    return trim(K, c)


def divmod_poly(K: FiniteField, a: Polynomial, b: Polynomial) -> tuple[Polynomial, Polynomial]:
    a, b = list(trim(K, a)), trim(K, b)
    if not b:
        raise ZeroDivisionError("zero polynomial divisor")
    q = [K.zero] * max(0, len(a) - len(b) + 1)
    inv = K.inv(b[-1])
    while len(a) >= len(b):
        shift = len(a) - len(b)
        coefficient = K.mul(a[-1], inv)
        q[shift] = coefficient
        for j, bj in enumerate(b):
            a[shift + j] = K.sub(a[shift + j], K.mul(coefficient, bj))
        while a and a[-1] == K.zero:
            a.pop()
    return trim(K, q), tuple(a)


def exact_div(K: FiniteField, a: Polynomial, b: Polynomial) -> Polynomial:
    q, r = divmod_poly(K, a, b)
    if r:
        raise ArithmeticError("nonexact polynomial division")
    return q


def monic(K: FiniteField, a: Polynomial) -> Polynomial:
    a = trim(K, a)
    return scale(K, a, K.inv(a[-1])) if a else ()


def gcd(K: FiniteField, a: Polynomial, b: Polynomial) -> Polynomial:
    K.stats.count("polynomial_gcds")
    while b:
        a, b = b, divmod_poly(K, a, b)[1]
    return monic(K, a)


def powmod(K: FiniteField, a: Polynomial, exponent: int, f: Polynomial) -> Polynomial:
    if exponent < 0:
        raise ValueError("polynomial modular exponent must be nonnegative")
    r = divmod_poly(K, (K.one,), f)[1]
    a = divmod_poly(K, a, f)[1]
    while exponent:
        if exponent & 1:
            r = divmod_poly(K, mul(K, r, a), f)[1]
        exponent >>= 1
        if exponent:
            a = divmod_poly(K, mul(K, a, a), f)[1]
    return r


def derivative(K: FiniteField, f: Polynomial) -> Polynomial:
    return trim(K, [K.mul(K.element(i), f[i]) for i in range(1, len(f))])


def polynomial_pth_root(K: FiniteField, f: Polynomial) -> Polynomial:
    """Inverse coefficient Frobenius: a^(p^(m-1)); not a^(1/p) in integers."""
    if any(ai != K.zero and i % K.p for i, ai in enumerate(f)):
        raise ValueError("polynomial is not a pth power")
    return trim(K, [K.pow(f[i], K.p ** (K.m - 1)) for i in range(0, len(f), K.p)])


def squarefree_decomposition(K: FiniteField, f: Polynomial) -> list[tuple[Polynomial, int]]:
    """Monic nonconstant input; return squarefree factors with multiplicities."""
    f = monic(K, f)
    if len(f) <= 1:
        return []
    one = (K.one,)
    c = gcd(K, f, derivative(K, f))
    w = exact_div(K, f, c)
    result: list[tuple[Polynomial, int]] = []
    i = 1
    while w != one:
        y = gcd(K, w, c)
        z = exact_div(K, w, y)
        if len(z) > 1:
            result.append((z, i))
        w = y
        c = exact_div(K, c, y)
        i += 1
    if c != one:
        for g, multiplicity in squarefree_decomposition(K, polynomial_pth_root(K, c)):
            result.append((g, K.p * multiplicity))
    return result


def rref(K: FiniteField, matrix: Sequence[Sequence[Element]], pivot_columns: int | None = None
         ) -> tuple[list[list[Element]], list[int]]:
    a = [list(row) for row in matrix]
    if not a:
        return a, []
    columns = len(a[0]) if pivot_columns is None else pivot_columns
    pivot_row, pivots = 0, []
    for column in range(columns):
        selected = next((i for i in range(pivot_row, len(a)) if a[i][column] != K.zero), None)
        if selected is None:
            continue
        a[pivot_row], a[selected] = a[selected], a[pivot_row]
        inv = K.inv(a[pivot_row][column])
        a[pivot_row] = [K.mul(value, inv) for value in a[pivot_row]]
        for i in range(len(a)):
            if i != pivot_row and a[i][column] != K.zero:
                coefficient = a[i][column]
                a[i] = [K.sub(ai, K.mul(coefficient, bi))
                        for ai, bi in zip(a[i], a[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(a):
            break
    return a, pivots


def kernel(K: FiniteField, matrix: Sequence[Sequence[Element]], columns: int) -> list[list[Element]]:
    K.stats.matrix("kernel", len(matrix), columns)
    a, pivots = rref(K, matrix)
    result = []
    for free in (i for i in range(columns) if i not in pivots):
        vector = [K.zero] * columns
        vector[free] = K.one
        for row, pivot in enumerate(pivots):
            vector[pivot] = K.neg(a[row][free])
        result.append(vector)
    return result


def solve_columns(K: FiniteField, columns: Sequence[Sequence[Element]], target: Sequence[Element]
                  ) -> list[Element] | None:
    """Solve sum columns[j]*a[j] = target by exact field Gaussian elimination."""
    d, n = len(columns), len(target)
    K.stats.matrix("minimal_polynomial_augmented", n, d + 1)
    matrix = [[columns[j][i] for j in range(d)] + [target[i]] for i in range(n)]
    a, pivots = rref(K, matrix, d)
    if any(all(value == K.zero for value in row[:d]) and row[d] != K.zero for row in a):
        return None
    answer = [K.zero] * d
    for row, pivot in enumerate(pivots):
        answer[pivot] = a[row][d]
    return answer


def berlekamp_basis(K: FiniteField, f: Polynomial) -> list[Polynomial]:
    """Kernel of a -> a^q-a on the n-dimensional K quotient algebra."""
    n = len(f) - 1
    if n < 1 or gcd(K, f, derivative(K, f)) != (K.one,):
        raise ValueError("Berlekamp input must be monic, nonconstant and squarefree")
    xq = powmod(K, (K.zero, K.one), K.q, f)
    column = (K.one,)
    columns = []
    for _ in range(n):
        columns.append(column + (K.zero,) * (n - len(column)))
        column = divmod_poly(K, mul(K, column, xq), f)[1]
    matrix = [[K.sub(columns[j][i], K.one if i == j else K.zero)
               for j in range(n)] for i in range(n)]
    basis = [trim(K, b) for b in kernel(K, matrix, n)]
    if not basis:
        raise ArithmeticError("the fixed algebra must contain constants")
    if any(powmod(K, b, K.q, f) != b for b in basis):
        raise ArithmeticError("computed Berlekamp basis fails Frobenius check")
    return basis


def trace_coordinate(K: FiniteField, b: Polynomial, alpha: Element, f: Polynomial) -> Polynomial:
    value = scale(K, b, alpha)
    answer: Polynomial = ()
    for i in range(K.m):
        answer = add(K, answer, value)
        if i + 1 < K.m:
            value = powmod(K, value, K.p, f)
    if powmod(K, answer, K.p, f) != answer:
        raise ArithmeticError("trace coordinate is not p-Frobenius fixed")
    return answer


def minimal_polynomial_in_quotient(K: FiniteField, c: Polynomial, f: Polynomial) -> tuple[int, ...]:
    """First linear dependence of 1,c,... over K; verify F_p coefficients."""
    n = len(f) - 1
    powers = [(K.one,) + (K.zero,) * (n - 1)]
    value = (K.one,)
    for d in range(1, n + 1):
        value = divmod_poly(K, mul(K, value, c), f)[1]
        vector = value + (K.zero,) * (n - len(value))
        coefficients = solve_columns(K, powers, [K.neg(v) for v in vector])
        if coefficients is not None:
            if any(any(a[j] for j in range(1, K.m)) for a in coefficients):
                raise ArithmeticError("p-fixed coordinate has a non-prime-field minimal polynomial")
            result = tuple(a[0] for a in coefficients) + (1,)
            check: Polynomial = ()
            for a, power in zip(coefficients, powers):
                check = add(K, check, scale(K, trim(K, power), a))
            if add(K, check, value):
                raise ArithmeticError("minimal-polynomial relation does not evaluate to zero")
            return result
        powers.append(vector)
    raise ArithmeticError("quotient dimension bound failed")


def exhaustive_prime_split_oracle(p: int, f: tuple[int, ...], max_prime: int = 4096) -> list[int]:
    """Toy oracle: O(p*deg(f)) modular work; never claimed polynomial in log p."""
    if p > max_prime:
        raise ValueError("toy oracle prime-size limit; supply a separately justified prime oracle")
    roots = []
    for a in range(p):
        value = 0
        for coefficient in reversed(f):
            value = (value * a + coefficient) % p
        if value == 0:
            roots.append(a)
    return roots


def checked_prime_roots(p: int, f: tuple[int, ...], oracle: PrimeOracle) -> tuple[int, ...]:
    roots = tuple(oracle(p, f))
    if any(not isinstance(a, int) or not 0 <= a < p for a in roots):
        raise ArithmeticError("oracle returned a noncanonical prime-field root")
    if len(set(roots)) != len(roots):
        raise ArithmeticError("oracle returned duplicate roots")
    product = (1,)
    for a in roots:
        product = _imul(product, (-a % p, 1), p)
    if product != f:
        raise ArithmeticError("oracle roots do not completely factor the queried polynomial")
    return roots


def squarefree_factor(K: FiniteField, f: Polynomial, prime_oracle: PrimeOracle) -> list[Polynomial]:
    """At most m*s prime-oracle calls of degree at most s, s=#factors <= n."""
    f = monic(K, f)
    n = len(f) - 1
    basis = berlekamp_basis(K, f)
    s = len(basis)
    K.stats.squarefree_runs.append({"degree": n, "fixed_algebra_dimension": s,
                                   "trace_coordinate_bound": K.m * s,
                                   "prime_oracle_call_bound": K.m * s,
                                   "prime_oracle_degree_bound": s})
    factors = [f]
    for b_index, b in enumerate(basis):
        for alpha_index, alpha in enumerate(K.basis()):
            if len(factors) == s:
                return factors
            c = trace_coordinate(K, b, alpha, f)
            minimum = minimal_polynomial_in_quotient(K, c, f)
            d = len(minimum) - 1
            if d > s:
                raise ArithmeticError("minimal-polynomial degree exceeds the fixed-algebra dimension")
            K.stats.trace_coordinates.append({"input_degree": n, "basis_index": b_index,
                                             "alpha_index": alpha_index, "minimal_degree": d})
            K.stats.count("prime_oracle_calls")
            K.stats.oracle_queries.append({"p_bits": K.p.bit_length(), "degree": d,
                                           "polynomial": list(minimum)})
            roots = checked_prime_roots(K.p, minimum, prime_oracle)
            refined = []
            for factor in factors:
                remaining = factor
                for a in roots:
                    divisor = gcd(K, remaining, sub(K, c, (K.element(a),)))
                    if len(divisor) > 1:
                        refined.append(divisor)
                        remaining = exact_div(K, remaining, divisor)
                    if remaining == (K.one,):
                        break
                if remaining != (K.one,):
                    raise ArithmeticError("coordinate roots did not partition a component")
            factors = refined
    if len(factors) != s:
        raise ArithmeticError("trace coordinates did not separate all components")
    return factors


def irreducible(K: FiniteField, f: Polynomial) -> bool:
    """Deterministic Frobenius irreducibility criterion, no degree factorization."""
    f = monic(K, f)
    n = len(f) - 1
    if n < 1:
        return False
    x = divmod_poly(K, (K.zero, K.one), f)[1]
    value = x
    for j in range(1, n + 1):
        value = powmod(K, value, K.q, f)
        if j <= n // 2 and gcd(K, sub(K, value, x), f) != (K.one,):
            return False
    return value == x


@dataclass(frozen=True)
class Factorization:
    unit: Element
    factors: tuple[tuple[Polynomial, int], ...]

    def reconstruct(self, K: FiniteField) -> Polynomial:
        answer = (self.unit,)
        for f, multiplicity in self.factors:
            for _ in range(multiplicity):
                answer = mul(K, answer, f)
        return trim(K, answer)

    def verify(self, K: FiniteField, original: Polynomial) -> bool:
        return (self.reconstruct(K) == trim(K, original)
                and len({f for f, _ in self.factors}) == len(self.factors)
                and all(e >= 1 and f[-1] == K.one and irreducible(K, f)
                        for f, e in self.factors))


def factor(K: FiniteField, f: Polynomial, prime_oracle: PrimeOracle,
           verify_output: bool = True) -> Factorization:
    """Complete factorization conditional on the prime oracle; zero is rejected."""
    f = trim(K, f)
    if not f:
        raise ValueError("zero polynomial has no finite complete factorization")
    unit = f[-1]
    terms = []
    for squarefree, multiplicity in squarefree_decomposition(K, monic(K, f)):
        terms.extend((g, multiplicity) for g in squarefree_factor(K, squarefree, prime_oracle))
    result = Factorization(unit, tuple(sorted(terms)))
    if verify_output and not result.verify(K, f):
        raise ArithmeticError("factorization failed independent Frobenius/reconstruction checks")
    return result
