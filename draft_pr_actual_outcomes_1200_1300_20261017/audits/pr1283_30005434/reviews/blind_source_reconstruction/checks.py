#!/usr/bin/env python3
"""Bounded consistency checks; universal validity is proved in PROOF.md.

No assertions are used, so all diagnostics remain active under -O and -OO.
"""

from itertools import product


class CheckFailure(Exception):
    pass


def require(predicate, message):
    if not predicate:
        raise CheckFailure(message)


def labelled_semilattices(n):
    """Enumerate relations, retain partial orders with all binary meets."""
    off_diagonal = [(a, b) for a in range(n) for b in range(n) if a != b]
    for mask in range(1 << len(off_diagonal)):
        le = [[a == b for b in range(n)] for a in range(n)]
        for bit, (a, b) in enumerate(off_diagonal):
            if mask & (1 << bit):
                le[a][b] = True
        if any(le[a][b] and le[b][a] for a in range(n) for b in range(a)):
            continue
        if any(le[a][b] and le[b][c] and not le[a][c]
               for a, b, c in product(range(n), repeat=3)):
            continue
        meet = [[None for _ in range(n)] for _ in range(n)]
        valid = True
        for a, b in product(range(n), repeat=2):
            lower = [c for c in range(n) if le[c][a] and le[c][b]]
            greatest = [c for c in lower if all(le[d][c] for d in lower)]
            if len(greatest) != 1:
                valid = False
                break
            meet[a][b] = greatest[0]
        if valid:
            yield le, meet


def validate_semilattice(meet):
    n = len(meet)
    for x in range(n):
        require(meet[x][x] == x, f"meet idempotence at {x}")
    for x, y in product(range(n), repeat=2):
        require(meet[x][y] == meet[y][x], f"meet commutativity at {x,y}")
    for x, y, z in product(range(n), repeat=3):
        require(meet[meet[x][y]][z] == meet[x][meet[y][z]],
                f"meet associativity at {x,y,z}")


def validate_semibrace(meet, op, e):
    n = len(meet)
    require(0 <= e < n, "distinguished point is absent")
    for x in range(n):
        require(op[e][x] == x, f"left unit at {x}")
        require(op[x][e] == e, f"right absorption at {x}")
    for x, y, z in product(range(n), repeat=3):
        require(op[x][meet[y][z]] == meet[op[x][y]][op[x][z]],
                f"meet preservation at {x,y,z}")
        require(op[meet[x][y]][z] == op[op[x][y]][op[x][z]],
                f"mixed identity at {x,y,z}")


def validate_lalgebra(op, e):
    n = len(op)
    require(0 <= e < n, "distinguished point is absent")
    for x in range(n):
        require(op[e][x] == x, f"L left unit at {x}")
        require(op[x][x] == e, f"L diagonal at {x}")
        require(op[x][e] == e, f"L right absorption at {x}")
    for x, y in product(range(n), repeat=2):
        require((op[x][y] == e and op[y][x] == e) == (x == y),
                f"L separation at {x,y}")
    for x, y, z in product(range(n), repeat=3):
        require(op[op[x][y]][op[x][z]] == op[op[y][x]][op[y][z]],
                f"cycloid at {x,y,z}")


def validate_order_coincidence(le, op, e):
    n = len(op)
    for x, y in product(range(n), repeat=2):
        require((op[x][y] == e) == le[x][y], f"order mismatch at {x,y}")


def expected_rejection(check, expected_fragment):
    try:
        check()
    except CheckFailure as error:
        require(expected_fragment in str(error),
                f"unexpected rejection reason: {error}")
        return str(error)
    raise CheckFailure("injected false predicate was accepted")


def main():
    print("All finite checks are consistency evidence, not the universal proof.")
    totals = []
    for n in range(1, 5):
        semilattices = points = greatest_points = 0
        for le, meet in labelled_semilattices(n):
            validate_semilattice(meet)
            semilattices += 1
            for e in range(n):
                projection = [[y for y in range(n)] for x in range(n)]
                validate_semibrace(meet, projection, e)
                points += 1
                if all(le[x][e] for x in range(n)):
                    constructed = [[e if le[x][y] else meet[x][y]
                                    for y in range(n)] for x in range(n)]
                    validate_semibrace(meet, constructed, e)
                    validate_lalgebra(constructed, e)
                    validate_order_coincidence(le, constructed, e)
                    greatest_points += 1
        totals.append((semilattices, greatest_points))
        print(f"n={n}: labelled semilattices={semilattices}; "
              f"projection pointed checks={points}; "
              f"greatest-point L constructions={greatest_points}: PASS")

    require(totals == [(1, 1), (2, 2), (9, 6), (76, 36)],
            f"unexpected enumeration totals: {totals}")

    # All 16 binary operations on a two-element chain: a prescribed
    # distinguished bottom must not support the simultaneous axioms.
    meet2 = [[0, 0], [0, 1]]
    accepted = 0
    for entries in product(range(2), repeat=4):
        op = [list(entries[:2]), list(entries[2:])]
        try:
            validate_semibrace(meet2, op, 0)
            validate_lalgebra(op, 0)
        except CheckFailure:
            continue
        accepted += 1
    require(accepted == 0, f"non-top prescribed point accepted {accepted} times")
    print("Two-element chain, prescribed bottom: 0 of 16 operations accepted: PASS")

    # M3: 0 bottom, 1/2/3 atoms, 4 top. This is nondistributive.
    meet_m3 = [[x if x == y else (y if x == 4 else (x if y == 4 else 0))
                for y in range(5)] for x in range(5)]
    validate_semilattice(meet_m3)
    op_m3 = [[4 if meet_m3[x][y] == x else meet_m3[x][y]
              for y in range(5)] for x in range(5)]
    validate_semibrace(meet_m3, op_m3, 4)
    validate_lalgebra(op_m3, 4)
    print("M3 nondistributive five-element lattice: PASS")
    print("M3 operation rows (0 bottom, 1/2/3 atoms, 4 top):")
    for row in op_m3:
        print(" ".join(map(str, row)))

    # A real operation table is corrupted to falsify the left-unit predicate.
    corrupted = [row[:] for row in op_m3]
    corrupted[4][0] = 4
    rejection = expected_rejection(
        lambda: validate_semibrace(meet_m3, corrupted, 4), "left unit at 0")
    print(f"Injected false left-unit predicate rejected: {rejection}")

    # Projection is valid for the first question but must fail L's diagonal.
    projection2 = [[y for y in range(2)] for x in range(2)]
    validate_semibrace(meet2, projection2, 1)
    rejection = expected_rejection(
        lambda: validate_lalgebra(projection2, 1), "L diagonal at 0")
    print(f"Injected false L-algebra predicate rejected: {rejection}")

    rejection = expected_rejection(
        lambda: validate_semibrace([], [], 0), "distinguished point is absent")
    print(f"Empty distinguished-set predicate rejected: {rejection}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
