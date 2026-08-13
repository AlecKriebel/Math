# Exact-byte audit of the 18,496-pair globally-nonmixed bridge

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes the
finite bridge

~~~text
src/remaining_18496_globally_nonmixed_certificate.py
SHA-256 54e0a5c96c2fe5e0e54c48bbb91f0f2eccbd140d62bce39ed55df54dd5a486fb
167 lines, 4801 bytes

tests/test_remaining_18496_globally_nonmixed_certificate.py
SHA-256 9228597561617ef92b93f6387a43cd954f534796e7de1b51f542613bfce06060
29 lines, 947 bytes
~~~

The verdict is **STRICT PASS** at these exact bytes.  The certificate proves
only a support/classifier identity: every pair in the exact 18,496-pair
outside-mixed remainder satisfies the literal globally-nonmixed hypothesis
of the frozen one-active symbolic theorem.  It enumerates no orientations,
rates, population states, reaction paths, or stochastic histories.

## 1. Exact theorem predicate

The analytic target is frozen at

~~~text
research_notes/proof_first_one_active_no_mixed_exhaustion_repaired.md
SHA-256 9fb1828f5660ffae83e6e1a08a0cb33ce8bd2813d7394a90187d9bccc64895c4
~~~

Its definition fixes each of the three active-coordinate pairs and evaluates
the available/shielded classifier on the seven ordered workload cells

\[
 (1,1),(2,3),(3,2),(1,2),(2,1),(1,3),(3,1).             \qquad (1.1)
\]

A linkage pair is globally nonmixed precisely when the two linkage supports
have identical Boolean outputs in all twenty-one cells.  The audited source
implements exactly this equality of twenty-one-entry support signatures.
It does not replace the predicate by membership in a named atlas or by a
single presently active chart.

## 2. Independent classifier replay

I independently compared every audited classifier call with the frozen raw
classifier in

~~~text
src/exact_shielded_seam.py
SHA-256 74cdc338c992e6a3ae27b86b35bb5fa496ac6048b39ded26777135514eb6f3e5
~~~

For an arbitrary active pair \((i,j)\), I permuted coordinates
\((i,j,k)\) to the raw classifier's displayed \((A,B,C)\) convention and
permuted the support mask accordingly.  The replay covered all 1,013 binary
supports of size at least two, all three active pairs, and all seven cells:

\[
                 1{,}013\cdot3\cdot7=21{,}273
                 \quad\hbox{comparisons}.              \qquad (2.1)
\]

There were zero mismatches.  In particular, the order of the branches is
literal: flat top, active-quadratic top, one-active-particle-flat
obstruction, unary top, shared bounded cofactor, and otherwise shielded.
The audited use of ``at least two'' in the active-quadratic branch is
equivalent to the raw equality test because every complex is binary.

## 3. Exact remainder and result

The pair universe is imported without re-selection from

~~~text
src/outside_mixed_remaining_18496_certificate.py
SHA-256 314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63
~~~

and the shared support encoding is pinned by

~~~text
src/global_atlas_interface_closure.py
SHA-256 293a63711f6da152edd72615d27fad5bbb859aa33a4b7eb150673b27ae3cb5bd
~~~

The exact replay returned

\[
\begin{array}{c|r}
\text{remainder pairs}&18{,}496\\
\text{globally nonmixed pairs}&18{,}496\\
\text{violations}&0.
\end{array}                                             \qquad (3.1)
\]

The complete sorted pair manifest and the support-signature dictionary have
the respective compact-JSON fingerprints

~~~text
eb7db151e42eb9562b1a1d519ea7dad212df52c6df368ffa08edbf79410db4ad
216a07ec3265cd9c072ff6975235198b839ab44b9dfd832c51ff70dd304459c1
~~~

The pair fingerprint agrees with the independently frozen 18,496-pair
certificate.  Thus the bridge neither drops nor adds a support pair.

## 4. Test and scope verdict

The four dedicated tests pass.  They pin the exact remainder size, zero
violations, all three active-coordinate pairs, all seven workload cells,
and the non-recurrence claim boundary.

The exact implication certified here is therefore

\[
 p\in\mathcal R_{18{,}496}
 \quad\Longrightarrow\quad
 p\text{ is globally nonmixed in the literal hypothesis of SHA }9fb1828f\ldots.
                                                               \qquad (4.1)
\]

This is sufficient to invoke the symbolic Q/flat/B/D exhaustion on every
one-active subsequence of every pair in the remainder.  It does not by
itself prove the stochastic estimates required inside those analytic
categories, and it does not claim recurrence of any pair.
