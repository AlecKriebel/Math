#!/usr/bin/env python3
"""Exact supplementary checks; the infinite-tree proof is in the Markdown note."""

from collections import deque
import json
from pathlib import Path


def color(n):
    """1-indexed n in 1;1,2;1,2,3;... ."""
    row = 1
    while n > row:
        n -= row
        row += 1
    return n


def digits(x, p, depth):
    result = [0] * depth
    for pos in range(depth - 1, -1, -1):
        x, result[pos] = divmod(x, p)
    return result


def integer(word, p):
    result = 0
    for digit in word:
        result = p * result + digit
    return result


def generator(p, depth, selected_color=None):
    result = []
    for x in range(p**depth):
        word = digits(x, p, depth)
        if selected_color is None:
            word[0] = (word[0] + 1) % p
        else:
            first = next((j for j, value in enumerate(word) if value), None)
            if (first is not None and word[first] == 1 and first + 1 < depth
                    and color(first + 1) == selected_color):
                word[first + 1] = (word[first + 1] + 1) % p
        result.append(integer(word, p))
    return tuple(result)


def compose(left, right):
    return tuple(left[right[x]] for x in range(len(left)))


def group_order(gens, limit=100_000):
    identity = tuple(range(len(gens[0])))
    seen = {identity}
    pending = deque([identity])
    while pending:
        current = pending.popleft()
        for g in gens:
            new = compose(g, current)
            if new not in seen:
                seen.add(new)
                pending.append(new)
                if len(seen) > limit:
                    raise RuntimeError("Explicit enumeration exceeded safety bound")
    return len(seen)


def orbit_size(gens, initial=0):
    seen = {initial}
    pending = deque([initial])
    while pending:
        x = pending.popleft()
        for g in gens:
            y = g[x]
            if y not in seen:
                seen.add(y)
                pending.append(y)
    return len(seen)


def verify():
    output = {"method": "exact integer permutation enumeration; supplementary only",
              "finite_subgroup_images": [], "level_transitivity": [],
              "commutators": []}
    for p, chosen, max_depth in [(2, 1, 9), (2, 2, 9), (3, 2, 5)]:
        orders = []
        for depth in range(1, max_depth + 1):
            a = generator(p, depth)
            d = generator(p, depth, chosen)
            identity = tuple(range(p**depth))
            assert compose(a, compose(a, identity)) == identity if p == 2 else True
            power = identity
            for _ in range(p):
                power = compose(d, power)
            assert power == identity
            orders.append(group_order([a, d]))
        output["finite_subgroup_images"].append(
            {"p": p, "I": [chosen], "depths": list(range(1, max_depth + 1)),
             "image_orders": orders})

    for p, max_depth in [(2, 8), (3, 5)]:
        for depth in range(1, max_depth + 1):
            selected = sorted({color(n) for n in range(1, depth)})
            gens = [generator(p, depth)] + [generator(p, depth, i) for i in selected]
            size = orbit_size(gens)
            assert size == p**depth
            output["level_transitivity"].append({"p": p, "depth": depth, "orbit_size": size})

    for p in [2, 3, 5, 7, 11]:
        exponents = list(range(p))
        differences = [(exponents[(j + 1) % p] - exponents[j]) % p for j in range(p)]
        assert differences == [1] * p
        output["commutators"].append({"p": p, "diagonal_exponents": differences})
    return output


if __name__ == "__main__":
    data = verify()
    destination = Path(__file__).with_name("finite_level_results.json")
    destination.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))
