# Independent finite checks

The two programs in this packet were written for this verification. They do not copy or execute programs from the source paper's archive.

## Minimal witness: Python standard library

Run `python3 verify_witness.py` and compare the JSON with `witness_results.json`.

The field models use polynomial bit representations, with modulus integers 7 and 11. A point of V is encoded by x+4y+16z, with x,y∈{0,1,2,3} and z∈{0,...,7}; vector addition is XOR. The program verifies the operator's order, its fixed space, every vector-pair linearity identity, all twelve orbits, the explicit 64-point support of a fixed element, and the zero trace of the induced representation. It also counts the twenty orbit-unions of size 64. The proof supplies irreducibility and the exhaustive invariant-character count; these are not inferred from the finite data alone.

## Complete count: integer C++

Compile and run:

    c++ -O2 -std=c++17 verify_exact_count.cpp -o /tmp/verify_2609_count
    /tmp/verify_2609_count

Compare the JSON with `exact_count_results.json`. The program uses only the compiler's standard library and exact integers.

The character parameter u and fixed element c are each a 12-bit assignment to the twelve operator orbits. From §4 of the certificate,

    |V_u| χ_u(c) = Σ_(t∈V) (-1)^(Σ_(x∈V) u(x+t)c(x)).

For fixed u and t, the exponent is a linear functional of the 12 bits of c. Its signature is recorded as a 12-bit mask. The histogram of 128 signatures has an integer Walsh transform whose 4096 entries are exactly the sums in the displayed formula. Each value is checked divisible by |V_u|, calculated independently from translation stabilizers. Vanishing is equivalent before and after this nonzero divisor. Five entire rows, including u=δ_0, are also checked using the literal double character sum, bypassing the signature histogram and transform.

The scan covers all 4096²=16,777,216 character/element pairs. This is an exhaustive check of the small parameter space, not an enumeration of the 2^135-element group. It gives:

- 1728 characters with zero zeros on C;
- 2048 characters with exactly 20 zeros on C;
- 320 characters with exactly 128 zeros on C;
- 81,920 zero character/element pairs in total.

Every character with a zero has degree 128. The degree histogram is 2 of degree 1, 10 of degree 4, 2 of degree 8, 52 of degree 16, 50 of degree 32, and 3980 of degree 128. Among the last group 1612 are nowhere zero. These extra data are internal consistency checks and do not assert any minimality of the construction.

## Limits

The numerical equality 1728 is a reproducible exact computation based on the complete character parameterization proved in the certificate. The simpler written proof of strict inequality requires only the single explicit witness and the total count, and remains valid independently of the complete enumeration. Neither program certifies the paper's unrelated theorems or historical priority.
