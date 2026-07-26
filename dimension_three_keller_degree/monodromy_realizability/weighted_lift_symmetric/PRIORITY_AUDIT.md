# Priority audit: symmetric monodromy realizations

**Initial sweep (UTC):** 2026-07-25T19:47:04Z.
**Hostile-audit correction (UTC):** 2026-07-25T20:08:55Z.

This is source-specific evidence, not a guarantee of worldwide priority.
No person was contacted.

## Candidate claim

Every admissible degree-\((d-1)\) seed in Gallagher's weighted-lift
construction has geometric monodromy \(S_d\).  In particular, for every
\(d\ge3\), the full symmetric group \(S_d\) occurs as the geometric
monodromy group of a dimension-three Keller counterexample.

## Sources checked

- Alexis Gallagher, *An infinite family of counterexamples to the
  Jacobian Conjecture in dimension three: every generic fiber degree
  \(n\ge3\) occurs*, Zenodo DOI
  [10.5281/zenodo.21479195](https://doi.org/10.5281/zenodo.21479195),
  and the associated
  [research record](https://github.com/algal/jacobianfun/blob/main/RESEARCH.md).
  Gallagher proves the all-degree weighted-lift construction.  Searches
  of the full public research record for “monodromy” and “Galois”
  returned no calculation of its monodromy groups.
- Gallagher's
  [public explainer](https://jacobianfun.org/jacobian-explained),
  including the all-degree seed construction and exact atlas.  It states
  generic degrees but does not state monodromy groups.
- The live
  [Secret Blogging Seminar thread](https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/),
  including its discussion of Gallagher's tangent-sweep construction.
  It contains no occurrence of “monodromy.”  A separate odd-degree
  family discussed in Tao's comments has both symmetric and alternating
  groups; it is not the present all-\(d\) realization.
- The current
  [MathOverflow question on the announced map's \(S_3\)
  monodromy](https://mathoverflow.net/questions/513387/galois-structure-of-the-new-counterexample-to-the-jacobian-conjecture-an-explic).
  It asks whether constraints beyond non-normality are known and contains
  no all-degree symmetric realization.
- The MathOverflow answer
  [*Geometric degrees of counterexamples to the Jacobian conjecture in
  dimension three*](https://mathoverflow.net/a/513470) and its linked
  [Note 19](https://github.com/dasjoms/jacobian-conjecture-counterexample-exploration/blob/main/jacobian_pin_transposition.md).
  This is a direct predecessor: it proves \(S_d\) for Gallagher's
  canonical tower for \(3\le d\le13\).  Public commit
  `ad47e9cea792` records the note on 21 July 2026.  It reports further
  finite checks but expressly leaves the all-degree argument open.
- Terence Tao's
  [digestion post and current comments](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/).
  The post has no Gallagher monodromy calculation.  One comment describes
  a different odd-degree family with \(S_{2m-1}\) for even \(m\) and
  \(A_{2m-1}\) for odd \(m\).
- arXiv searches in math.AG/math.AC for July 2026 combinations of
  “Jacobian,” “Keller,” “counterexample,” “monodromy,” “Galois,” and
  “symmetric group,” including arXiv:2607.20210 and arXiv:2607.21572.
  The former records \(S_3\) for the announced map; the latter concerns
  real generic degrees.  No collision with the all-\(d\) statement was
  found.
- Exact web searches for `T^d-T^2+UT+V`, the weighted-lift inverse
  polynomial, and Keller/symmetric-monodromy combinations.  This located
  David Brink, *On Alternating and Symmetric Groups as Galois Groups*,
  Israel J. Math. 142 (2004), 47--60,
  [doi:10.1007/BF02771527](https://doi.org/10.1007/BF02771527).
  Brink's Theorem 13 directly proves that every monic polynomial with fixed
  higher coefficients and independent linear and constant coefficients has
  Galois group \(S_d\) in characteristic zero.  Thus the Galois lemma used
  here is prior art in exactly the needed generality.
- Search-engine sweeps of X/Twitter-indexed pages and the current Tao,
  MathOverflow, and Secret Blogging Seminar discussions.  No matching
  all-\(d\) Keller realization was found.

## Corrected verdict

Gallagher has clear priority for the counterexample family and its all-degree
generic-fibre theorem.  Brink has clear priority for the two-parameter
symmetric Galois theorem.  The MathOverflow/Note 19 authors have priority
for the finite \(3\le d\le13\) symmetric-monodromy computation in
Gallagher's canonical tower.  Their family-wide combination through the
exact weighted-lift root-field recovery--full symmetric monodromy for every
admissible seed and every \(d\ge3\)--was not found in the checked public
record and passed the independent mathematical audit.  It should be
presented as a new attributed Brink--Gallagher corollary, not as a new
Galois theorem.

The absence of a hit is not proof of novelty.

## 2026-07-26T03:49Z — source-and-scope re-audit

A second hostile audit read Gallagher's full PDF and the full text around
Brink's Theorem 13.  Gallagher's Theorem 1 is uniform over exactly the
displayed admissible seeds, and Proposition 1 proves generic degree
\(\deg p+1\).  Brink's theorem applies verbatim to the normalized inverse
pencil over \(\mathbb C(P,Q)\).  No correctness or scope defect was found.

Two newly visible records were checked:

- *Exact Fibers, Image, and Geometry at Infinity of the Marked-Root Keller
  Family*, GitLab snippet 6012790, studies a different
  \(\mathbb C^n\)-family of generic degree \(n(n-2)\);
- F. Santibañez-Leal, *The Jacobian counterexample, validated and
  extended*, Zenodo record 21579022, contains no monodromy or Galois
  calculation.

Neither collides with the all-seed Brink--Gallagher corollary.  Fresh
site-restricted searches again found the already credited finite
\(3\le d\le13\) computation, but no public all-degree, all-admissible-seed
statement.  This remains source-specific evidence, not a guarantee of
worldwide priority.
