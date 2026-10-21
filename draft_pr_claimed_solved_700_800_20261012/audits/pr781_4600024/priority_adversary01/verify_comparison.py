#!/usr/bin/env python3
"""Finite controls for the written comparisons; no finite test proves universality."""
import itertools
import json

class ComparisonError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise ComparisonError(message)

def local_union(word):
    return "a" not in word or "c" not in word

def even_word(word):
    zeros = [i for i, symbol in enumerate(word) if symbol == "0"]
    return all((j - i - 1) % 2 == 0 for i, j in zip(zeros, zeros[1:]))

def main():
    for n in range(1, 65):
        word = "a" + "b" * n + "c"
        require(not local_union(word), "union word unexpectedly allowed")
        require(all(local_union(word[i:i+n]) for i in range(len(word)-n+1)),
                "union local-factor control failed")
        word = "0" + "1" * (2*n+1) + "0"
        require(not even_word(word), "even-shift bad word unexpectedly allowed")
        require(all(even_word(word[i:i+n]) for i in range(len(word)-n+1)),
                "even local-factor control failed")
    require("010" not in "01110" and not even_word("01110"),
            "density versus exactness control failed")
    fixed_images = {str(bit): str(bit ^ bit) for bit in (0, 1)}
    require("1" not in fixed_images.values(), "XOR fixed-point obstruction failed")
    local_blocks = 0
    for length in range(1, 9):
        for y in itertools.product((0, 1), repeat=length):
            x = [0]
            for symbol in y:
                x.append(x[-1] ^ symbol)
            require(tuple(x[i] ^ x[i+1] for i in range(length)) == y,
                    "XOR finite-block preimage control failed")
            local_blocks += 1
    print(json.dumps({
        "result": "PASS",
        "lt_non_sft_factor_controls": 64,
        "even_shift_local_controls": 64,
        "density_exactness_control": True,
        "xor_fixed_point_images": fixed_images,
        "xor_local_blocks_checked": local_blocks,
        "universal_arguments": ["COMPARISON.md", "PEER_CHALLENGE.md"],
        "finite_checks_are_not_a_new_theorem_proof": True
    }, sort_keys=True))

if __name__ == "__main__":
    main()
