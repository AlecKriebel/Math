# Reproducibility and limits

From this directory, with Python 3 and no third-party packages:

    python3 -B controls.py --full-lattice --output /tmp/twisted-wreath-control-results.json
    cmp CONTROL_RESULTS.json /tmp/twisted-wreath-control-results.json
    sha256sum -c SHA256SUMS

The JSON result is deterministic. The script prints elapsed time to stdout only; it is not placed in the hashed result. The optional --full-lattice switch is required to reproduce the supplied result exactly. Without that switch, the proof-independent witness and Burnside controls still run, but the lattice field is null.

Checks:

1. Construct A6 from its 360 even permutations and Q=A5 as the point stabilizer of 6.
2. Compute all component centralizers: orders 3, 4, 5, hence minimum component class size 12.
3. Construct the even three-pair partition stabilizer R of order 24, its intersection with Q of order four, and the equivariant function f_{R,t}. Check its equivariance on every pair (x,q) in P x Q and its full stabilizer on every p in P. The stabilizer is R, giving orbit size 15.
4. Check every A6 involution has two fixed letters and the 5-cycle centralizer normalizer has order ten inside Q.
5. Use the double-coset formula to compute fixed-function counts for every element of A6; verify consistency by cycle type and integral Burnside orbit count.
6. Enumerate all A6 subgroups by starting with the identity and adjoining each possible new generator, skipping elements in the same left coset of the current subgroup. Completeness follows because every finite subgroup has a generating sequence; adjoining h g for h in H gives the same overgroup as adjoining g. Each generated subgroup is stored as its full set of permutation indices. Find 501 subgroups, 432 admissible, maximum admissible order 24, and maximum order five when the value is a fixed 5-cycle.
7. Independently enumerate integer partitions for 5 <= n <= 30, compute alternating-group centralizer orders including split classes, and check that the resulting class sizes add to |A_n|-1. Verify the A8 minimum 105 and the A9 witness bound 168 < 945.
8. Factor |A20| exactly and check that every Sylow order is smaller than the explicit 3-cycle centralizer in A19, showing the Sylow criterion is not universally applicable.

Hard limits:

- largest explicitly enumerated permutation group: order 360;
- full subgroup enumeration: A6 only;
- subgroup-enumeration wall-clock guard: 120 seconds;
- largest partition degree: 30;
- number of socle points enumerated: zero;
- no random trials, floating-point arithmetic, internet access, package installation, or large exhaustive search;
- neither all primitive groups nor all twists phi are enumerated.

The mathematical proofs of Propositions 7 and 8 do not rely on treating these finite controls as evidence of a universal statement. The elementary lower bound in Proposition 7 also does not depend on the completeness of the computed subgroup lattice.
