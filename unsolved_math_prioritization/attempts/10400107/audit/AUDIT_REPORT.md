# Independent adversarial audit: 10400107 / AMR-103-0107

Date: 2026-10-04 UTC. Queue rank: 605.

## Verdict

**PASS. Recommend `already_solved`, `1/5`, as verification of a known affirmative answer.**
No blocking mathematical, attribution, scope, or reproducibility defect was found.
This is not a new-solution or priority claim. No remote write was performed and
no file in the frozen attempt was edited.

The exact audited input is the six-file public manifest with SHA-256
`b13203cb599712d5877e5bd58bdafcdbc6ef248f39c58f07a1fa2043773d82e1`.
All six checksums verified before and after the audit. The original control
output was reproduced byte-for-byte.

The natural realization covers arbitrary discrete quandles, arbitrary constant
abelian coefficient groups, all positive degrees, and degree zero with the
explicit unaugmented convention. Non-injective homomorphisms are included.

## 1. Target and primary-source check

The original target is Ohtsuki, *Problems on invariants of knots and 3-manifolds*,
Problem 5.11, printed p.465, PDF page 93. It asks for a natural space realizing
quandle cohomology. Its neighboring warning concerns the failure of collapsing
a rack-space subcomplex. Section 5.3, printed p.459, defines ordinary cochains
with values in an abelian group and the adjacent-equality vanishing condition.
No restriction to finite or connected quandles is attached to Problem 5.11.
The neighboring Conjecture 5.12 and the earlier local-coefficient problem are
separate targets. [Original publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

I inspected the actual definition and cell statement in Ishikawa–Tanaka,
arXiv:1912.12917v2, §6.1, printed pp.17–18, including a local visual rendering
of both pages. I also checked Remark 2.1 for the quandle specialization and
Remark 6.1 for the historical correction. This was not an abstract-only check.
The source specifies all dimensions, nondegenerate tuple cells, and the cellular
map from the rack space; no finiteness assumption enters this construction.
[Inspected version](https://arxiv.org/pdf/1912.12917v2).

The arXiv record dates v2 to March 26, 2020; the manuscript itself is dated
March 5, 2020. Publisher metadata independently confirms *Topology and its
Applications* 345 (2024), 108832, DOI 10.1016/j.topol.2024.108832. The publisher
introduction still points to §6.1 and Remark 6.1. The page references in the
attempt explicitly refer to the inspected preprint, so they do not confuse
preprint and version-of-record pagination.
[Version record](https://arxiv.org/abs/1912.12917v2),
[publisher record](https://www.sciencedirect.com/science/article/pii/S0166864124000178).

The primary text supports the construction and cellular quotient. The all-A,
all-degree, natural cohomology conclusion is correctly derived in the attempt
from that cellular information; it is not falsely presented as a quoted theorem
about arbitrary coefficients from the article.

## 2. Independent algebraic and geometric challenge

### Degenerate chains and signs

For an adjacent equal pair, faces outside the pair preserve an adjacent equal
pair. The two exceptional deletion faces cancel, and the two exceptional action
faces cancel by idempotence. Thus the subgroup on degenerate tuples really is a
subcomplex. The quotient is free on nondegenerate tuples in every degree.
The sign sum `(-1)^i(d_i^0-d_i^1)` equals the usual oriented cube boundary
`(-1)^(i-1)(d_i^1-d_i^0)`. In degree two it gives `(x)-(x*y)`, matching the
source's first coboundary. No sign correction is needed.

### Termination and all local overlaps

Each submitted shortening strictly decreases word length. Right translation
is an automorphism, with

    S R_a^k = R_{S(a)}^k S.

For two erasures at coordinate 1, the order change is exactly
`R_(a*b) R_b = R_b R_a`. An erasure or merge to the right transforms every label
of a disjoint left operation by the same automorphism; the displayed identity
therefore resolves the fork. The same reasoning handles two disjoint merges,
including carries of two. Erasing a zero commutes, apart from its immediate
merge overlap, where the two reductions have the same further reduction.
For an overlapping triple with equal label a, both parenthesizations have
carry `floor(s+t+u)`, residual fractional part, and the same prefix action by a.
Idempotence ensures that retained a's do not change under these carries.

These are all overlaps of length-one erasures and length-two merges. New
adjacencies formed by deleting a block are handled by further reductions;
local confluence does not require terminal results after just one additional
step. Termination and local confluence therefore imply a unique normal form.
Each generating equal-sum relation has the same immediately merged result,
so it preserves normal form even when used in reverse. Consequently there are
no hidden identifications between distinct nondegenerate interior points
arising through larger degenerate cubes.

### A fully explicit CW weak-topology justification

The argument in submitted §3.3 is correct. A useful way to make its continuity
claim completely transparent is to avoid treating the canonical floor-normal
form as a continuous map into a disjoint union. It is generally not such a map.
Instead, use the following closed-piece contraction for an equal pair:

    (P,(s,a),(t,a),S) -> (P,(s+t,a),S)             if s+t <= 1,
    (P,(s,a),(t,a),S) -> (R_a P,(s+t-1,a),S)       if s+t >= 1.

Here R_a acts only on the labels of P, and coordinates 0 and 1 are deliberately
retained until their existing face identifications are applied. Both outputs
have length one less. At s+t=1, the low output has an a-coordinate 1 and the
high output has an a-coordinate 0. Deleting these endpoints gives precisely
the same word. At s+t=2 the high output still has a coordinate 1, whose later
erasure provides the second carry. Thus both branches are continuous into the
already constructed lower skeleton and agree on their closed overlap.

More formally, induct simultaneously on dimension:

1. Assume all cubes of length below n have continuous maps to the corresponding
   inductively constructed CW skeleta, realizing the normal-form equivalence.
2. A degenerate n-cube maps into the (n-1)-skeleton by the two closed branches
   above and the induction hypothesis. This proves continuity by finite gluing.
3. For a nondegenerate n-tuple, every boundary face reduces to a cube of length
   n-1. The already continuous face maps agree on face intersections by
   confluence. Attach that closed n-cube along this continuous boundary map.
4. Every such boundary meets finitely many cells: its reduction tree is finite,
   because each step decreases length, each step has finitely many choices,
   and only finitely many labels arise from a fixed finite starting word.
5. Confluence identifies the resulting underlying set with the quotient by the
   three submitted relations. Every original cube has a continuous map into
   this CW complex, and every surviving characteristic cube maps continuously
   to the original quotient. The two mutually inverse maps are continuous by
   the respective final topologies.

This proves the claimed topology, rather than only a set bijection. It also
proves that the surviving cube interiors are homeomorphic open cells, that
degenerate n-cubes land below dimension n, and that the CW closure-finiteness
condition holds. No countability, finite cardinality, or quandle connectivity
is used. This is an exposition strengthening, not a missing additional theorem
required to rescue the construction.

## 3. Exact cochains, arbitrary coefficients, and naturality

The rack quotient is cellular. In degree n its cellular map has coefficient
+1 on a surviving nondegenerate cell and zero on a degenerate cell. Surjectivity
forces the target cellular differential to be precisely the algebraic quotient
differential. Hence the actual integral cellular chain complex, not merely its
homology, is `C_*^R(X)/D_*`.

Applying `Hom_Z(-,A)` gives exactly the ordinary quandle cochain group and its
differential for every abelian A. Infinite bases produce products, not direct
sums, in the cochain groups. Thus torsion coefficients and infinite quandles
introduce no UCT splitting or finite-support issue. Cellular cohomology agrees
naturally with singular cohomology for CW complexes and cellular maps.

A quandle map f respects every defining relation by equality preservation and
`f(a*b)=f(a)*f(b)`. The coordinatewise map on the disjoint union is continuous,
so the descended map is continuous by the quotient topology. A formerly
nondegenerate tuple may become degenerate, but then its image lies in a lower
skeleton. Thus the map remains cellular. Its cellular chain map is exactly the
usual coordinatewise quandle map modulo degeneracies. This proves the required
contravariant naturality in X, including non-injective maps, and covariant
naturality in coefficient homomorphisms. Identities and composition hold on
representatives, without auxiliary choices.

There is one vertex, so the constructed space is connected, even for an empty
quandle if that convention is admitted. The unaugmented `C_0=Z` convention gives
`H^0=A`. A convention with `C_0=0` instead matches reduced degree-zero
cohomology; positive degrees are unaffected. The normalized chain quotient
here is precisely ordinary quandle cohomology, not an alternative cohomology
theory inadvertently substituted for the target.

## 4. Falsification controls and history

For the one-element quandle, the surviving cells are exactly one vertex and
one edge, giving a circle. Its higher quandle cochains vanish. This rejects both
of the tempting incorrect constructions:

- The cellular subcomplex generated by all degenerate cells is the whole rack
  space for a nonempty quandle: every tuple is a deletion face of the tuple
  obtained by repeating its last entry. Collapsing it gives a point.
- The literal Nosaka Definition 2.1 takes a mapping cone from disjoint cubes.
  That domain has no positive homology, so its cofiber leaves rack homology
  unchanged in degrees at least two. For the singleton, rack H_2 is Z, whereas
  ordinary quandle H_2 is zero.

I inspected Nosaka's actual Definition 2.1 in the locally retained primary PDF;
it has exactly this disjoint-cube domain. The later correction is therefore
substantive. This criticism is confined to the literal all-degree definition:
Remark 6.1 also explains that the additional-cell low-skeleton discussion has
the desired homotopy type. The 2011 low-dimensional construction alone cannot
certify the original all-degree question. The submitted historical attribution
correctly distinguishes these points.

For a trivial quandle of size m, all boundaries vanish and the cell count is
`m(m-1)^(n-1)` in positive degree, consistent with the quotient complex. A
natural realization need not turn disconnected quandles into disconnected
spaces; orbit information appears in H^1 rather than H^0.

## 5. Reproducible computational audit

The frozen script was run unchanged in a separate output location and its
output matched `controls/CONTROL_RESULTS.json` byte-for-byte. Its limits are
accurately disclosed: five finite quandles, chain degree at most five,
naturality degree at most four, and half-grid geometry through length four.
The negative-control strings in that JSON are analytic assertions supported
by the written cofiber calculation, not numerical homology computations.

The independent `check_supplement.py` uses elementary contractions on the two
closed branches above, not the submitted combined floor-and-carry rewrite.
It adds the missing non-involutive geometric model A5 with operation 2x-y
modulo 5, whose right translations have order four, and exact thirds:

- 168,421 A5 words through length four
- 273,020 equal-sum fiber comparisons
- 128,000 prefixed disjoint-merge inputs of length five
- 78,326 geometric naturality cases for R4 -> T2 parity and A5 -> singleton
- 18,224 instances in which those maps lower normal-form dimension
- 400 closed-branch seam checks

All passed. Neither this supplement nor the original finite tests is used as
proof of the arbitrary-quandle/all-degree topological assertion.

## 6. Corrections and release boundary

Required corrections: **none**.

Optional exposition improvement: insert the two closed-branch formulas from
§2 of this report into submitted §3.3. This makes the seam argument explicit
and prevents a reader from mistaking discontinuous floor-normalization for a
continuous normal-form selector. The frozen proof already states the correct
piecewise/final-topology argument and cites the exact published cell statement.

The original public publication allowlist is exactly:

1. `public/README.md`
2. `public/PROOF.md`
3. `public/SOURCE_STATUS.md`
4. `public/APPROACH_LOG.md`
5. `controls/check_controls.py`
6. `controls/CONTROL_RESULTS.json`

Do not publish the original `private/` tree, imported corpora, source PDFs or
renders, `AUDIT_REQUEST.json`, or `FREEZE.json`. The current two root checksum
files happen to list only these six safe files, but they are not themselves
in the supplied publication allowlist; generate release checksums from the
explicitly selected files rather than copying arbitrary root metadata.

This separate audit's safe files are listed in `VERDICT.json` and hashed in
`AUDIT_SHA256SUMS`. Its `private/` source renders are excluded. The mathematical
verdict does not authorize queue edits or other remote changes. Repository
head/status and integration gates should be rechecked by the parent at release;
this audit is tied to the stated immutable artifact, not a live branch claim.
