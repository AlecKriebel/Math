# Exact-byte audit of the 18,496-pair remainder certificate

**Independent proof-first audit, 2026-08-12 PDT.** The frozen targets are

~~~text
src/outside_mixed_remaining_18496_certificate.py
SHA-256 314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63
451 lines / 15,178 bytes

tests/test_outside_mixed_remaining_18496_certificate.py
SHA-256 28d3cf0087bcd77e24d6dbfa280b226b34d3d026c35e743bc10487c829667769
61 lines / 1,993 bytes
~~~

The verdict is **STRICT PASS** for the literal finite support/descriptor
claim. The code makes no recurrence claim and enumerates no orientation,
rate vector, population state, reaction history, or communicating class.

## 1. Universe subtraction

The audit rehashed every declared dependency. The frozen all-active
certificate supplies 18,832 ordered disjoint pairs outside the inherited
mixed-atlas orbit and the strictly-positive-invariant branch. It also
supplies 336 distinct level-set pairs: its selected incidence count equals
its projected-pair count. Literal set subtraction gives

\[
 18{,}496=18{,}832-336,                               \tag{1.1}
\]

with disjoint union back to the 18,832-pair universe. The canonical
remainder fingerprint independently replays as

~~~text
eb7db151e42eb9562b1a1d519ea7dad212df52c6df368ffa08edbf79410db4ad
~~~

No quotient by species permutations or linkage reversal is taken in this
count: these are the literal ordered pairs entering the analytic theorem.

## 2. Failure predicate and exact counts

For each remainder pair, the program scans the frozen complete set of 259
tier/cap descriptors. A row is retained precisely when

1. the exact rational affine-feasibility predicate is true; and
2. the corrected S-tier-superlevel universal strong-orientation predicate
   is false.

These are the same frozen predicates used in the separately audited
corrected-cut and level-set certificates. There is no orientation witness
construction in this derivative.

The independent replay gives

\[
 \begin{array}{c|r}
 \text{object}&\text{count}\\ \hline
 \text{feasible corrected-cut failure rows}&21{,}906\\
 \text{pairs with at least one failure}&6{,}654\\
 \text{pairs with no failure}&11{,}842.
 \end{array}                                          \tag{2.1}
\]

The two pair fingerprints are

~~~text
failed 6,654
036f9cb8f00f99f78be9cb6c2303208a8ca8b25be8c1bd350b8fac6b35582eed
no failure 11,842
b425db9040d0836462f4240a4a3acf51d067d356eb4f2bfe4ce2cf648e42db26
~~~

They are disjoint and their union is the remainder in (1.1).

## 3. Independent classifier replay

The one-active classifier was reimplemented directly from its symbolic
definition. For the unique active coordinate X it applies, in order:

\[
 \mathrm Q,\quad \mathrm{F0},\quad \mathrm{F1},\quad
 \mathrm B,\quad \mathrm D.
\]

Here B means that a degree-one complex \(q\) and a degree-zero complex \(c\)
satisfy \(q_i\le c_i\) in both inactive coordinates. The clean-room
implementation and the target agree on every nontrivial support and every
one-active exact descriptor: zero mismatches.

The two-active Q/U/C/S classifier was likewise reimplemented from the frozen
bridge, preserving its ordered tests: flat-top S, quadratic-active Q,
active-support flat S, unary-top U, bounded-carrier C, and residual S. Every
two-active descriptor has positive weights exactly on its two active
coordinates. The clean-room implementation agrees with the target on every
support/descriptor input: zero mismatches.

The resulting failure-row histogram is exactly

\[
 21{,}906
 =15{,}204\ [\mathrm{B/F0}]
  +3{,}618\ [\mathrm{B/B}]
  +3{,}084\ [\mathrm{AA}].                           \tag{3.1}
\]

There are 18,822 one-active rows and 3,084 two-active rows. Every two-active
row is available/available. Its unordered classifier split is

\[
 \begin{array}{c|rrrrr}
 &\mathrm{Q/U}&\mathrm{U/U}&\mathrm{C/U}&\mathrm{C/Q}&\mathrm{C/C}\\ \hline
 \text{rows}&1200&996&660&156&72.
 \end{array}                                          \tag{3.2}
\]

Thus no unlisted F1, D, mixed, SS, or all-active failure remains after the
stated subtraction. This is a finite classification statement only.

## 4. Pair-level signature pins

The failed pairs split by their set of incident profiles as

\[
 \begin{array}{c|r}
 \mathrm{B/B}&2874\\
 \mathrm{B/F0}&1818\\
 \mathrm{AA+B/F0}&1428\\
 \mathrm{B/B+B/F0}&366\\
 \mathrm{AA+B/B+B/F0}&156\\
 \mathrm{AA}&12.
 \end{array}                                          \tag{4.1}
\]

The canonical signature records the ordered pair, exact partition, active
mask, caps, weight, aggregate profile, and both ordered linkage kinds for
every failure row. Its sorted-key and insertion-order encodings rehash as

~~~text
d3adaf3aa0c6f3957162d1b1538dc6bf1797caa6bb4bc5c5812b53263851000b
0d106ccdbd0701664aa451dead00230863abbcb88e19eb34f44fd1e12fe5fe22
~~~

All five focused tests pass.

## 5. Verdict boundary

The exact pair subtraction, affine/cut predicate, classifiers, counts, and
fingerprints are **STRICT PASS**. This certificate proves only that the
remaining analytic failures have the three profiles in (3.1). It does not
prove that their local drift-or-exit statements compose, that a common
potential exists, or that any of the 18,496 pairs is recurrent. Those are
separate load-bearing analytic obligations.
