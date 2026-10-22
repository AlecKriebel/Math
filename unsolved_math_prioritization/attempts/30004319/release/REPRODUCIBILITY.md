# Reproduction and limits

All programs use Python 3's standard library. No installation, network access,
random seed, symbolic-algebra package, group solver, or source PDF is required.
From this directory:

    python3 finite_algebra_controls.py > /tmp/rank602-finite.json
    cmp finite_algebra_results.json /tmp/rank602-finite.json
    python3 symbolic_controls.py > /tmp/rank602-symbolic.json
    cmp symbolic_results.json /tmp/rank602-symbolic.json
    python3 verify_small_witnesses.py > /tmp/rank602-witness.json
    cmp witness_results.json /tmp/rank602-witness.json
    sha256sum -c MANIFEST.sha256

The programs terminate by fixed finite loops. The author's combined rerun
took about two seconds on the available machine; runtime is not a proof claim.

## Exact finite domain

The additive group is F2³, encoded as integers 0..7 with addition by XOR.
The fixed ordered basis is 1=1, e=2, f=4. Unitality fixes five basis products;
each of e², ef, fe, f² can be any of the eight vectors. Consequently the 4,096
tables are an exhaustive labelled family, with no isomorphism reduction.

The strong-inverse test exhausts every proposed inverse and every element z.
The three unit-Moufang equations are checked on every y,z for each strong unit.
Both alternative laws are checked on every a,b. Associativity is checked on
basis triples, which is sufficient because the associator is trilinear.
The implication (Z) is checked on all a,b,c,t, rather than only basis tuples.

Expected principal counts:

- 4,096 total tables
- 76 alternative and 76 associative tables
- 3,976 unit-Moufang tables, including 3,900 nonalternative tables
- 3,324 of those 3,900 rejected by (Z)
- 576 nonalternative tables remaining after both necessary filters

The retained JSON gives all 576 final tables, examples and witnesses, plus a
hash of the ordered 3,900-table intermediate list. The integer-translate
coverage count is 24; every covered ring passing unit-Moufang is alternative,
as predicted by Proposition 2. This extra check is not a claim that every
coordinate ring satisfies that sufficient condition.

The positive-root model over R0 has 512 elements. The program checks all
512 two-sided inverses, all 4,096 instances of the four-coordinate cocycle
identity on which associativity depends, and all 64 displayed root commutators.
This is supplemented by the uniform proof, not represented as a 512³
brute-force associativity run.

## Independent witness and symbolic controls

`verify_small_witnesses.py` builds products from explicit coordinate formulas
for R0 and R1 and imports nothing from the main enumeration. It checks the
strong units, unit-Moufang identities, nonalternativity witnesses, and (Z).
Its ordering differs from the integer-bit enumeration, so the first reported
R0 obstruction witness is allowed to differ.

`symbolic_controls.py` expands formal unital, nonassociative binary trees over
Z[n]. It does not impose associativity. It verifies invariance of the repeated
associator under a+n1, the matrix Jacobi identity's exact defect, and the finite
A2/A3 positive-root chain comparison.

## What these controls do not establish

- They do not formalise the literature's unit-Moufang theorem.
- They do not establish injectivity or nondegeneracy in S(R) for any survivor.
- They do not construct a full A2-graded group with nonalternative parameters.
- They do not classify higher-dimensional algebras, rings of other
  characteristics, or isomorphism classes even in the finite tested family.
- Passing necessary algebraic tests is not evidence of a full counterexample.
- The written group proofs and their assumptions require mathematical review;
  a successful Python run is not an independent proof of every theorem here.

No claimed full solution is available for a 1/5 candidate disposition.
