# Independent exact-byte audit of the all-feasible two-active AA identity

**Audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The audited certificate and test are

~~~text
src/remaining_18496_all_feasible_two_active_aa_certificate.py
25e5c2fce812d2e3d3f02c0c9377533cf16c68313b77bc0d1e7a485052bd68ee
187 lines / 6480 bytes

tests/test_remaining_18496_all_feasible_two_active_aa_certificate.py
2445edcbcf66ff2204c821baec455b4f8a416180360a39a6d757712af5fc22e0
49 lines / 1744 bytes
~~~

The verdict on these exact bytes is **STRICT PASS AS A FINITE GEOMETRIC
IDENTITY**.

For every weight-flag-feasible two-active descriptor of every pair in the
frozen 18,496-pair remainder, each linkage is classified Q, U, or C by the
frozen ordered classifier.  Equivalently, every such row is AA.  The
certificate enumerates no orientations, rates, populations, stochastic
histories, or communicating classes and proves no recurrence theorem.

## 2. Exact universe and dependency pins

The certificate begins with the frozen remainder rather than constructing a
new pair universe.  Its dependency hashes replay exactly:

~~~text
src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63

src/global_tier_interface.py
b8feae08c2eecf21b6e4e387eeaa6f5b15f32d862fca5324d4523c38872494ab

src/s_tier_superlevel_interface.py
1a4e27fcf40af76cac6281f8830b7644bf086b3c05d97a963ce9f5bac736ad57

src/stoichiometric_gate_feasibility.py
4602e7d31af02c26cc9785ed056c876e3e571e428ad974e861e4940b9edba9a1
~~~

The remainder fingerprint is

~~~text
eb7db151e42eb9562b1a1d519ea7dad212df52c6df368ffa08edbf79410db4ad
~~~

and the code asserts the literal cardinality 18,496 before accepting the
identity.

The feasibility test is the exact rational level-by-level affine flag test
for the pair's stoichiometric subspace.  It deliberately does not impose a
particular integral fixed-class base or an exact realization of a cap value.
Consequently the streamed set is at least as large as the descriptors that
can occur in a fixed class.  Proving AA on this larger flag-feasible set is
safe for the intended necessity implication.

## 3. Ordered classifier replay

For each linkage the program applies the classifier in its load-bearing
order:

1. whole linkage top gives S;
2. a top complex with two active particles gives Q;
3. the active-carrier flat test gives S;
4. a top unary gives U;
5. bounded cofactor both at top and below gives C;
6. otherwise S.

This is the literal classifier of the frozen bridge

~~~text
research_notes/proof_first_quc_classifier_bridge_and_raw_trichotomy.md
014a317602b60c765dc9a9eb98f0921ba3fd8f779221e271e0dd7f53e245f54c
~~~

The finite certificate tests the two linkages independently and records an
unavailable row whenever either output is outside Q/U/C.  The exact count is
zero.  The variable name `unavailable_linkage_rows` means rows with at least
one unavailable linkage; because its value is zero, no multiplicity
ambiguity affects the conclusion.

## 4. Exact streamed identity

The independent replay produced

~~~text
feasible two-active incidences       1,140,984
corrected-cut passes                 1,137,900
corrected-cut failures                   3,084
rows with an unavailable linkage             0
pairs represented                       18,322
~~~

The active-coordinate masks occur symmetrically:

~~~text
AB active    380,328
AC active    380,328
BC active    380,328
~~~

The unordered Q/U/C histogram is

~~~text
C/C       216
C/Q   165,870
C/U     9,360
Q/Q   639,468
Q/U   321,858
U/U     4,212
~~~

These six cells sum to 1,140,984.  There is no S cell.  The 3,084
corrected-cut failures agree with the failure count in the frozen 18,496
certificate; the new result is stronger because it also checks all
1,137,900 passing two-active rows.

The canonical streamed-incidence and summary fingerprints are

~~~text
a4c4aa42dadabe7e73d46a690f29fe1d457bf57c5bece422b8c0a3fafe72eb99
bc9195d09dc8717381486ae114fcd59e22786c729d957fe209ceac432deaaac8
~~~

The five dedicated tests pass:

~~~text
Ran 5 tests in 92.312s
OK
~~~

## 5. What the identity does and does not discharge

The identity discharges the classifier bridge for every possible
two-active terminal descriptor in this remainder.  Thus a proof may always
choose the available-target paths furnished by the Q/U/C bridge from the
current actual mark.

It does **not** by itself prove an unconditional population-Foster episode.
In particular, it does not show that a cap or tier exit is charged, that an
exit graph is Markov, that an exit-only cycle has negative average reward,
or that a local drift-or-exit alternative tiles globally.  Those are
stochastic composition statements absent from the finite calculation.

The exact safe conclusion is therefore:

> Every flag-feasible two-active descriptor of the 18,496-pair remainder is
> AA.  Any remaining two-active obstruction is analytic composition, not a
> missing support-classifier case.

This identity may be used in an unconditional killed-completion theorem that
continues through bounded-cap and tier changes.  It may not be used as a
terminal-chart-exit shortcut.
