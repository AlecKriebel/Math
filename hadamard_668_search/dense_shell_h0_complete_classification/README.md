# Complete dense-shell \(h=0\) profile classification

## Result

The strict \(729\)-shard census contains exactly **18 canonical exact
compressed-profile orbits** in the dense \(h=0\) shell.

Under the exact 24-element action

\[
C_6\times C_{2,A}^{*}\times C_{2,B}^{*},
\]

12 representatives have trivial stabilizer and orbit size 24, while six
have stabilizer order two and orbit size 12.  Thus

\[
12\cdot24+6\cdot12=360,
\]

exactly matching the production counter `weighted_exact_zero_hits = 360`.
All \(\binom{18}{2}=153\) pairwise orbit intersections are empty.

This is a complete classification **inside the dense \(h=0\)
compressed-profile search scope**.  It is not a labelled \(LP(333)\), a
Legendre pair, or a Hadamard matrix of order 668.

## Independent certificate

`certificate.json` freezes the 18 representatives and the final strict
aggregate's global census metadata.  It does not contain or require the
ignored production output.

`verify_h0_complete_classification.py` uses only the Python standard
library.  It independently:

1. reconstructs the 12 order-three cyclotomic classes of
   \(\mathbb F_{37}^{*}\);
2. expands each compressed representative to two physical length-37 words
   over \(\mathbb Z[\omega]\);
3. evaluates all 37 correlations for each representative in exact integer
   Eisenstein arithmetic—666 correlations in total;
4. checks zero lag \((167,0)\) and all 36 nonzero lags \((0,0)\);
5. recomputes the shell counts \((n_9,n_3,n_0)=(0,18,6)\);
6. reconstructs and verifies closure, identity, inverses, associativity,
   and faithfulness of the exact 24-element action;
7. recomputes canonicality, stabilizers, orbit sizes, all production
   digests, orbit hashes, and physical replay hashes;
8. proves the 18 reconstructed orbits pairwise disjoint; and
9. ties their total size 360 to the frozen Burnside-weighted exact-hit
   count.

Run:

```text
python3 verify_h0_complete_classification.py
```

The replay takes about 0.1 seconds and 22 MB RSS on the research machine.

## Census provenance and completeness boundary

The frozen strict aggregate reports:

- 729 of 729 prefix shards complete;
- 47,730,304 raw decorations;
- 1,999,128 canonical decorations, all processed;
- 25,368,365,895,696 weighted primitive-flag phase leaves;
- 19,986 characteristic-two/mod-9 intersections;
- 64 post-mod-9 lambda hits;
- 18 canonical exact-zero hits;
- 360 weighted exact-zero hits; and
- 18 distinct retained canonical exact-profile orbits.

The verifier pins the SHA-256 digests of the final aggregate, production
manifest, classifier source, and binary, and checks the complete counter
vector.  It deliberately does **not** rerun the enormous enumeration.
Accordingly, the mathematical validity and inequivalence of the 18 frozen
orbits are independently replayed, while exhaustion of the search space is
certified by the hashed strict production provenance.

The production aggregate labels its exact upper scope
`char2_mod9_intersection`.  No claim is made beyond that structured dense
\(h=0\) search family.
