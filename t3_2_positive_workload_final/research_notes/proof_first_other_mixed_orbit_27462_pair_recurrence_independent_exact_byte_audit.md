# Second independent exact-byte audit of the 27,462-pair mixed orbit

**Audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The audited theorem and finite inputs are

~~~text
research_notes/proof_first_other_mixed_orbit_27462_pair_recurrence_theorem.md
a91e8c31f35312ef4b9063e8f5a48af534861145db2236e662ea6cc1eff8e30e
200 lines / 7856 bytes

src/other_mixed_orbit_27462_certificate.py
57d8904dd86cd0bf626e344dbfd7b7f248b239cdeaace48489796058c6875f08

tests/test_other_mixed_orbit_27462_certificate.py
e708c52f6cbc1bbc4dabf33f246d72379dff58c74cc97a38fdd8076ac3ae7d13
~~~

The verdict is **STRICT PASS** at these exact bytes.  The theorem proves
nonexplosion and positive recurrence on every closed irreducible class for
exactly the 27,462 ordered support pairs obtained from the completed seed
branches.  It does not use the invalid active-only-invariant inference and
does not claim the exclusive 432-pair gap.

## 2. Independent seed-partition replay

I rebuilt the seed sets directly from the inherited positive-shield and
signed-shield tables, rather than reading the certificate's summary payload.
The union has 5,169 ordered seeds.  Exactly 110 have first applicable branch
`common_active_invariant`; removing them before any symmetry operation leaves
5,059 eligible seeds.

The five completed predicates give the pairwise-disjoint cardinalities

\[
                   187,\qquad 974,\qquad 9,\qquad 1378,\qquad 2511,
\]

and their union is exactly the 5,059-seed eligible set.  Their fingerprints,
in the same order as the theorem, are

~~~text
e760b14784236fe097aec28fa775553bcda4516fcc81e858b478a70eefd0bd6a
4e79e97328e35796ba4ff903708f1ccc341db564bd89463ccb47e1fa349a8fc1
7a8d67d09a4d76923df5c36879f53bbaf301f2f666e6282a8e36f729aa48f2b1
9d70b04459dc110a1f7451d63c36e7e21d874eca3afec284268cac8cba942ba7
0c57f530eb44a688520cc1706f830afa18063f4d08d24e5006f47a5666edd0b3
~~~

The eligible-set and branch-manifest fingerprints are respectively

~~~text
c45f67990ff841e1ba7b7d5d8a2795539f495f2434d68135ad3b2483d2fda44f
22f10cf6ea09a7b36650df174a866fd15470c770b3da6079728cfe5301f61c76
~~~

All five focused certificate tests pass.  No orientation, rate, population,
history, or class is present in this finite calculation.

## 3. Analytic sufficiency of the five branches

The first two branches are self-contained.  A strictly positive common
invariant makes every nonnegative integer class finite.  A weakly reversible
full-deficiency-zero network is complex balanced for every positive rate
vector; its stochastic product form is normalizable after restriction to
each closed class because it is dominated by the full product-Poisson sum.

The nine physical-seam seeds are exact-support invocations.  They consist of
six new seven-support pairs, two new signed-service pairs, and one residual
pair.  The theorem pins all three arbitrary-orientation physical-time proofs
and their exact-scope audit

~~~text
e7e76b76cd1371f98d19da0a1f5362ab4a0696548fba62028b29ccd2950617c9.
~~~

In particular, the signed-service theorem is never extended to a support
superset.

For each of the 1,378 tier-pass seeds, every one of the 259 exact descriptors
satisfies the corrected S-tier-superlevel cut.  In a strong linkage graph,
the first edge leaving the nonempty proper D-superlevel is sourced in the
top S-tier and is D-descending.  Thus every escaping class-contained tier
sequence satisfies the Anderson--Kim hypothesis.  The standard bad-sequence
argument gives statewise entropy drift outside a finite classwise set; no
chart-exit composition is being inferred.

For the last 2,511 seeds, I independently ran the publication-safe union
certificate at SHA

~~~text
501d96c4cea2de33ed34db2c31702d3104e8ed80c1abb8cf15e895c56201593f.
~~~

Its fourteen branch sizes are

\[
151,14,51,141,92,36,4,15,1212,26,416,13,7,333,
\]

which sum to 2,511.  They are pairwise disjoint, their union has fingerprint
`0c57f530...`, and the five union tests pass.  Its dependency verifier
rehashes the theorem and independent-audit bytes for every branch.  Each
dependency concludes recurrence for its fixed support pair under arbitrary
strong orientations and positive rates.  Consequently this is a finite
union of pair theorems, not a switch among local potentials on one path.

## 4. Independent orbit and conjugacy replay

I independently applied all six coordinate permutations and linkage
reversal to the eligible set.  The result has 27,462 distinct ordered pairs
and fingerprint

~~~text
1bf337cf143c6eb4cee5088827bb9e9b9cec704f01a1b1f57bde6aed856d2812.
~~~

The active-only-invariant seed orbit has 714 points.  Exactly 282 also lie in
the eligible orbit, while the remaining 432 form the exclusive gap; the
27,462-pair set is disjoint from that gap.  An overlap point is valid because
membership in the eligible orbit supplies a completed eligible seed
preimage.  Its active-only-invariant representation is irrelevant.

A coordinate permutation is a bijection of population lattices and closed
irreducible classes.  Pulling an image orientation and its positive labelled
rates back through that permutation gives an arbitrary seed orientation with
the same falling-factorial propensities, so the two generators are
conjugate.  Linkage reversal changes only the order in which the same two
linkages are listed.  Nonexplosion and positive recurrence therefore
transfer to every orbit image with no extra analytic hypothesis.

## 5. Nonexplosion and publication check

A degree-two source in the binary universe cannot increase total molecular
population.  Every population-increasing rate is therefore at most affine
in total population, while jumps are bounded.  Linear pure-birth comparison
prevents population escape in finite time, and neutral quadratic clocks
cannot accumulate inside a finite population sublevel.

The exact theorem was independently converted with Pandoc's
single-backslash TeX-math reader and compiled with Tectonic.  The resulting
three-page letter PDF has zero diagnostics; all pages were visually checked,
and control-byte and placeholder scans are clean.

Thus the exact theorem at SHA `a91e8c31...` is publication-ready at its
stated 27,462-pair scope.
