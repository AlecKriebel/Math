"""Exact, deliberately small-scale monomial-quotient regularity calculator.

Only standard product gradings are supported. No nonmonomial degeneration is
performed. Characteristic 0 uses rational arithmetic; prime p uses F_p. The
proof of termination and completeness is in PROOF.md, not inferred from tests.
"""
from fractions import Fraction
from itertools import combinations, product


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, length - 1):
                yield (first,) + rest


def is_prime(p):
    if p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True


def matrix_rank(matrix, characteristic=0):
    if not matrix or not matrix[0]:
        return 0
    if characteristic:
        a = [[v % characteristic for v in row] for row in matrix]
    else:
        a = [[Fraction(v) for v in row] for row in matrix]
    pivot_row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        inverse = (pow(a[pivot_row][col], -1, characteristic)
                   if characteristic else 1 / a[pivot_row][col])
        a[pivot_row] = [v * inverse for v in a[pivot_row]]
        if characteristic:
            a[pivot_row] = [v % characteristic for v in a[pivot_row]]
        for i in range(pivot_row + 1, len(a)):
            factor = a[i][col]
            if factor:
                a[i] = [v - factor * w for v, w in zip(a[i], a[pivot_row])]
                if characteristic:
                    a[i] = [v % characteristic for v in a[i]]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


class MonomialQuotient:
    def __init__(self, block_sizes, generators, characteristic=0):
        self.block_sizes = tuple(block_sizes)
        if not self.block_sizes or any(type(v) is not int or v < 2 for v in self.block_sizes):
            raise ValueError('Each block must have at least two variables (P^n, n >= 1).')
        if type(characteristic) is not int or (characteristic != 0 and not is_prime(characteristic)):
            raise ValueError('Characteristic must be 0 or a positive prime.')
        self.characteristic = characteristic
        self.nvars = sum(self.block_sizes)
        self.generators = tuple(sorted(set(tuple(g) for g in generators)))
        if any(len(g) != self.nvars or any(type(v) is not int or v < 0 for v in g)
               for g in self.generators):
            raise ValueError('Generators must be nonnegative integer exponent vectors.')
        self.blocks = []
        offset = 0
        for size in self.block_sizes:
            self.blocks.append(tuple(range(offset, offset + size)))
            offset += size
        # Minimal monomial generators of the irrelevant ideal B.
        self.b_supports = tuple(frozenset(v) for v in product(*self.blocks))
        q = len(self.b_supports)
        self.cech_subsets = [tuple(combinations(range(q), i)) for i in range(q + 1)]
        self.inverted = {s: frozenset().union(*(self.b_supports[j] for j in s))
                         for row in self.cech_subsets for s in row}

    def survives(self, degree, inverted):
        outside = [j for j in range(self.nvars) if j not in inverted]
        if any(degree[j] < 0 for j in outside):
            return False
        return not any(all(g[j] <= degree[j] for j in outside) for g in self.generators)

    def fine_cohomology(self, degree, check_complex=False):
        """Dimensions of every fine-degree Cech cohomology group."""
        if len(degree) != self.nvars:
            raise ValueError('Wrong fine degree length.')
        bases = [[s for s in row if self.survives(degree, self.inverted[s])]
                 for row in self.cech_subsets]
        matrices = []
        ranks = [0]
        for i in range(len(bases) - 1):
            source_index = {s: j for j, s in enumerate(bases[i])}
            a = [[0] * len(bases[i]) for _ in bases[i + 1]]
            for row, target in enumerate(bases[i + 1]):
                for pos in range(len(target)):
                    source = target[:pos] + target[pos + 1:]
                    if source in source_index:
                        a[row][source_index[source]] = (-1) ** pos
            matrices.append(a)
            ranks.append(matrix_rank(a, self.characteristic))
        ranks.append(0)
        if check_complex:
            for i in range(len(matrices) - 1):
                a, b = matrices[i], matrices[i + 1]
                for row in b:
                    for col in range(len(bases[i])):
                        assert sum(row[k] * a[k][col] for k in range(len(a))) == 0
        dims = tuple(len(bases[i]) - ranks[i] - ranks[i + 1] for i in range(len(bases)))
        assert all(v >= 0 for v in dims)
        return dims

    def cells(self):
        """(representative, coordinate upper bounds); None denotes +infinity."""
        caps = [max((g[j] for g in self.generators), default=0) for j in range(self.nvars)]
        coordinate_cells = [[(-1, -1)] + [(a, a) for a in range(cap)] + [(cap, None)]
                            for cap in caps]
        for cell in product(*coordinate_cells):
            yield tuple(c[0] for c in cell), tuple(c[1] for c in cell)

    def regularity(self, check_complex=False, kind='module'):
        """Return exact CNF and every minimal point, including degenerate cases.

        Each clause is a disjunction of (coordinate, inclusive lower threshold).
        The full region is the conjunction of all clauses. An empty conjunction
        is all Z^r; an empty clause makes the region empty. Minimal points need
        not generate the region when the quotient has zero associated sheaf.
        """
        if kind not in ('module', 'sheaf'):
            raise ValueError('kind must be module or sheaf.')
        r = len(self.blocks)
        support_uppers = set()
        cell_count = 0
        for a, upper in self.cells():
            cell_count += 1
            h = self.fine_cohomology(a, check_complex=check_complex)
            coarse_upper = tuple(None if any(upper[j] is None for j in block)
                                 else sum(upper[j] for j in block) for block in self.blocks)
            for i, dimension in enumerate(h):
                if dimension and (kind == 'module' or i >= 2):
                    support_uppers.add((i, coarse_upper))
        clauses = set()
        for i, upper in support_uppers:
            shifts = (compositions(i - 1, r) if i > 0
                      else (tuple(-int(j == k) for j in range(r)) for k in range(r)))
            for shift in shifts:
                clauses.add(tuple((j, upper[j] + shift[j] + 1)
                                  for j in range(r) if upper[j] is not None))
        clauses = tuple(sorted(clauses))
        thresholds = tuple(tuple(sorted({v for clause in clauses for k, v in clause if k == j}))
                           for j in range(r))
        minima = []
        for d in product(*thresholds):
            if satisfies(clauses, d) and all(not satisfies(clauses, tuple(v - int(k == j)
                            for k, v in enumerate(d))) for j in range(r)):
                minima.append(d)
        # Produce a finite union of generalized orthants as a complete region
        # description, even when some lower endpoints are -infinity (None).
        orthants = {tuple(None for _ in range(r))}
        for clause in clauses:
            next_orthants = set()
            for a in orthants:
                for j, t in clause:
                    b = list(a)
                    b[j] = t if b[j] is None else max(t, b[j])
                    next_orthants.add(tuple(b))
            orthants = {a for a in next_orthants if not any(
                b != a and generalized_le(b, a) for b in next_orthants)}
        return {'kind': kind, 'block_sizes': self.block_sizes, 'generators': self.generators,
                'characteristic': self.characteristic, 'cells_checked': cell_count,
                'support_profiles': len(support_uppers), 'clauses': clauses,
                'candidate_thresholds': thresholds, 'minimal_elements': tuple(sorted(minima)),
                'generalized_orthants': tuple(sorted(orthants, key=repr))}


def generalized_le(a, b):
    return all(x is None or (y is not None and x <= y) for x, y in zip(a, b))


def satisfies(clauses, degree):
    return all(any(degree[j] >= bound for j, bound in clause) for clause in clauses)


def complete_intersection_frontier(degrees):
    """Known BHS formula; caller must certify saturation, CI, and I subset B."""
    if not degrees or any(len(d) != len(degrees[0]) or any(x < 1 for x in d) for d in degrees):
        raise ValueError('Need nonempty positive multidegrees of a certified saturated CI.')
    a = tuple(map(sum, zip(*degrees)))
    return tuple(sorted(tuple(x - 1 - v for x, v in zip(a, u))
                        for u in compositions(len(degrees) - 1, len(a))))
