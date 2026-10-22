#!/usr/bin/env python3
"""Exact finite challenges for the written measure/ordinal derivations.

This program imports no submitted checker and proves no infinite-measure theorem.
It tracks every coordinate through formal convergent blocks, including finite
prefixes and tails, and tests exact half-density chain coefficients.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json


STREAMS = {}
FINITES = {}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Atom:
    tag: str
    index: int


@dataclass(frozen=True)
class Tail:
    tag: str
    offset: int


@dataclass(frozen=True)
class Block:
    prefix: tuple
    tail: Tail


@dataclass(frozen=True)
class Word:
    blocks: tuple = ()
    suffix: tuple = ()


def atom_value(atom):
    if atom.tag in FINITES:
        return FINITES[atom.tag][atom.index]
    a, delta, pattern = STREAMS[atom.tag]
    return a + delta * Q(pattern[atom.index % len(pattern)], 2 ** atom.index)


def normalized(block):
    prefix = list(block.prefix)
    tail = block.tail
    while prefix and tail.offset > 0 and prefix[-1] == Atom(tail.tag, tail.offset - 1):
        prefix.pop()
        tail = Tail(tail.tag, tail.offset - 1)
    return Block(tuple(prefix), tail)


def concatenate(left, right):
    if right.blocks:
        first = right.blocks[0]
        absorbed = normalized(Block(left.suffix + first.prefix, first.tail))
        return Word(left.blocks + (absorbed,) + right.blocks[1:], right.suffix)
    return Word(left.blocks, left.suffix + right.suffix)


def grade(word):
    return len(word.blocks), len(word.suffix)


def ordinal_add(left, right):
    n, m = left
    p, q = right
    return (n + p, q) if p else (n, m + q)


def take_tail(block, k):
    if k < len(block.prefix):
        return normalized(Block(block.prefix[k:], block.tail))
    return normalized(Block((), Tail(block.tail.tag, block.tail.offset + k - len(block.prefix))))


def parameters(block):
    a, delta, _ = STREAMS[block.tail.tag]
    power = len(block.prefix) - block.tail.offset
    recovered = delta * (Q(2 ** power) if power >= 0 else Q(1, 2 ** (-power)))
    return a, recovered


def one_letter(atom):
    return Word((), (atom,))


def color(value, cuts):
    require(value not in cuts, "Coordinate equals a fixed cut in this control")
    return sum(value > c for c in cuts)


def color_runs(word, cuts):
    """Exact run factorization for our bounded periodic-z convergent blocks.

    A finite prefix is inspected literally; beyond a certified index the
    absolute tail displacement is smaller than every distance from limit to cut.
    """
    pieces = []
    for block in word.blocks:
        for atom in block.prefix:
            pieces.append((color(atom_value(atom), cuts), one_letter(atom)))
        a, delta, pattern = STREAMS[block.tail.tag]
        require(a not in cuts, "Block limit equals a fixed cut in this control")
        bound = min(abs(a - c) for c in cuts)
        i = block.tail.offset
        max_z = max(abs(z) for z in pattern)
        while delta * Q(max_z, 2 ** i) >= bound:
            atom = Atom(block.tail.tag, i)
            pieces.append((color(atom_value(atom), cuts), one_letter(atom)))
            i += 1
        pieces.append((color(a, cuts), Word((Block((), Tail(block.tail.tag, i)),), ())))
    for atom in word.suffix:
        pieces.append((color(atom_value(atom), cuts), one_letter(atom)))
    runs = []
    for c, piece in pieces:
        if runs and runs[-1][0] == c:
            runs[-1] = (c, concatenate(runs[-1][1], piece))
        else:
            runs.append((c, piece))
    return tuple(runs)


def flatten(runs):
    result = Word()
    for _, word in runs:
        result = concatenate(result, word)
    return result


def make_word(n, m, tag, a_values=(Q(1, 3), Q(5, 3), Q(7, 3))):
    blocks = []
    for i in range(n):
        stream = tag + ":B" + str(i)
        STREAMS[stream] = (a_values[i % len(a_values)], Q(5 + i, 8), (1, -1, -1, 1))
        prefix_tag = tag + ":P" + str(i)
        FINITES[prefix_tag] = (Q(1, 7), Q(17, 7), Q(10, 7))
        p = i % 3
        blocks.append(Block(tuple(Atom(prefix_tag, j) for j in range(p)), Tail(stream, i % 2)))
    suffix_tag = tag + ":S"
    FINITES[suffix_tag] = tuple(Q(3 + 4 * j, 13) for j in range(m))
    return Word(tuple(blocks), tuple(Atom(suffix_tag, j) for j in range(m)))


def density_form(names, scale=Q(1)):
    """Gaussian q as (number of (2pi)^(-1/2) factors, rational prefactor,
    exact coefficient of each -(name-a)^2 in the exponent).
    """
    k = len(names)
    prefactor = Q(1)
    exponent = {}
    for j, name in enumerate(names):
        width = scale * 2 ** (k - j)
        prefactor /= width
        exponent[name] = Q(1, 2) / (width * width)
    return k, prefactor, exponent


def multiply_forms(left, right):
    exponent = dict(left[2])
    for name, value in right[2].items():
        exponent[name] = exponent.get(name, Q(0)) + value
    return left[0] + right[0], left[1] * right[1], exponent


def calculate():
    checks = 0
    association_cases = 0
    run_cases = 0
    prefix_cases = 0
    density_cases = 0
    negative_controls = []
    grades = list(product(range(3), range(4)))
    for a, b, c in product(grades, repeat=3):
        wa, wb, wc = [make_word(*g, "assoc:" + str(i)) for i, g in enumerate((a, b, c))]
        left = concatenate(concatenate(wa, wb), wc)
        right = concatenate(wa, concatenate(wb, wc))
        require(left == right, "Associativity loses or reorders coordinates")
        require(grade(left) == ordinal_add(ordinal_add(a, b), c), "Grade arithmetic differs")
        require(concatenate(Word(), wa) == wa and concatenate(wa, Word()) == wa, "Vacuum not an identity")
        checks += 3
        association_cases += 1
    for n, m, variant in product(range(4), range(5), range(5)):
        # Limits avoid integer cuts; finite and tail coordinates are rational.
        word = make_word(n, m, "runs:" + str((n, m, variant)),
                         tuple(Q(1 + 4 * ((i + variant) % 3), 3) for i in range(3)))
        for cuts in ((Q(1),), (Q(2),), (Q(1), Q(2)), (Q(-1), Q(1), Q(2), Q(4))):
            runs = color_runs(word, cuts)
            require(flatten(runs) == word, "Run extraction loses a coordinate at an ordinal boundary")
            require(all(runs[i][0] != runs[i + 1][0] for i in range(len(runs) - 1)), "Runs are not maximal")
            require(all(grade(piece) != (0, 0) for _, piece in runs), "An empty centered run was admitted")
            for c, piece in runs:
                again = color_runs(piece, cuts)
                require(again == ((c, piece),), "A monochromatic run is not monochromatic or unique")
                checks += 1
            checks += 3
            run_cases += 1
        # Compare the two binary-cut parenthesizations with the direct three-color chart.
        direct = color_runs(word, (Q(1), Q(2)))
        upper_first = []
        for outer_color, piece in color_runs(word, (Q(2),)):
            if outer_color == 0:
                upper_first.extend(color_runs(piece, (Q(1),)))
            else:
                upper_first.append((2, piece))
        lower_first = []
        for outer_color, piece in color_runs(word, (Q(1),)):
            if outer_color == 1:
                lower_first.extend((c + 1, w) for c, w in color_runs(piece, (Q(2),)))
            else:
                lower_first.append((0, piece))
        require(tuple(upper_first) == direct, "Upper grouping changes the color-run chart")
        require(tuple(lower_first) == direct, "Lower grouping changes the color-run chart")
        checks += 2
        for block in word.blocks:
            a, delta = parameters(block)
            for k in range(13):
                tail = take_tail(block, k)
                require(parameters(tail) == (a, delta / (2 ** k)), "Recoverable tail scale is wrong")
                checks += 1
                prefix_cases += 1
    for k, l, scale in product(range(9), range(9), (Q(1, 3), Q(1), Q(7, 2))):
        v = tuple("v" + str(j) for j in range(k))
        w = tuple("w" + str(j) for j in range(l))
        left = density_form(v + w, scale)
        right = multiply_forms(density_form(v, scale * 2 ** l), density_form(w, scale))
        require(left == right, "Exact Gaussian normalizer/quadratic chain identity fails")
        checks += 1
        density_cases += 1
        if k and l:
            wrong = multiply_forms(density_form(v, scale), density_form(w, scale))
            require(left != wrong, "Control failed to detect omitted tail-scale change")
            checks += 1
    # Pointwise coordinate-loss controls; these are invalid changes to the construction.
    wa = make_word(1, 2, "negative:left")
    wb = make_word(1, 1, "negative:right")
    correct = concatenate(wa, wb)
    dropped = Word(wa.blocks + wb.blocks, wb.suffix)
    require(correct != dropped, "Control did not detect a suffix discarded by ordinal absorption")
    negative_controls.append("Discarded finite suffix before an infinite right block is detected")
    reversed_blocks = Word(tuple(reversed(correct.blocks)), correct.suffix)
    require(correct != reversed_blocks, "Control did not detect reversed infinite blocks")
    negative_controls.append("Reordered infinite blocks are detected")
    # General RN norm identity on a finite exact measure model (not Gaussian integration).
    density = (Q(2), Q(3))
    input_norm_squared = Q(2)
    correct_norm_squared = sum(q / q for q in density)
    wrong_norm_squared = sum(q * q for q in density)
    require(correct_norm_squared == input_norm_squared and wrong_norm_squared != input_norm_squared,
            "RN sign control failed")
    negative_controls.append("Opposite RN half-density direction violates the exact norm identity")
    # A block limit at the cut must be rejected by this deterministic chart control.
    special = make_word(1, 0, "negative:cutlimit", (Q(1),))
    caught = False
    try:
        color_runs(special, (Q(1),))
    except RuntimeError:
        caught = True
    require(caught, "Control incorrectly certified an excluded limit-at-cut block")
    negative_controls.append("A limit exactly at the cut is excluded rather than silently factorized")
    checks += 4
    return {"status": "PASS", "exact_finite_checks": checks,
            "formal_association_cases": association_cases,
            "exact_convergent_block_color_run_cases": run_cases,
            "tail_scale_cases": prefix_cases,
            "exact_gaussian_density_form_cases": density_cases,
            "negative_controls": negative_controls,
            "density_wrong_scale_cases_rejected": 8 * 8 * 3,
            "scope": "Finite symbolic/rational controls of coordinate retention, fixed-cut charts and Gaussian coefficients; the written sigma-finite and infinite-dimensional proof remains essential"}


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2, sort_keys=True))
