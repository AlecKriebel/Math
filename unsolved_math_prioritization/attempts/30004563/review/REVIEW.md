# Independent adversarial review: five alpha=16 cube-move centers

**Verdict: PASS for the stated complete counterexample.** The frozen candidate proves that an admissible incoming alpha=16 realization has at least five distinct allowed outgoing centers. This contradicts the proposed upper bound of three in the crossing-allowed realization/immersion setting. I found no mandatory mathematical correction. The proof does not establish the actual maximum, a result about proper embeddings, or historical priority.

The review was performed separately from the author. Its arithmetic checker was independently written and uses a different interval representation, a different eighth-root algorithm, and fresh root brackets. This is an independent AI-assisted mathematical review, not human peer review or formal proof-assistant verification.

## Frozen material reviewed

| Artifact | SHA-256 |
|---|---|
| CANDIDATE.md | 293f5ad9475b4a8d045121b2eccecbcf0d4937df3077e9bb430c7f9056e12f51 |
| certify_five_centers.py | 09b5db2b625b00e2c20f9c41ea1922733b1b6ab04f404c2e37ba8f0e6ef1e585 |
| turn2_exact_certificate.json | 393f41d9cafb49f8b60f6950b54150b5ed3d395076d99fb8c6507a0bbc7ced5e |

The full candidate and full author checker were read. Running an isolated copy of the author checker reproduced the frozen receipt byte-for-byte: **6,987 checks**. The separate `independent_check.py` passes **13,948 exact checks**, including **3,444 certified eighth-root evaluations**. Its full rational receipt is `INDEPENDENT_CERTIFICATE.json`.

## 1. The source question and its hypotheses

The [original Oberwolfach report](https://ems.press/content/serial-article-files/46871), printed p.1785, introduces alpha-immersions, explicitly permits intersecting edges, and proposes three as the maximum possible number of central points when alpha is greater than one. The corresponding [published Melotti-Ramassamy-Thevenin paper](https://ems.press/content/serial-article-files/39488), DOI [10.4171/AIHPD/163](https://doi.org/10.4171/AIHPD/163), supplies precise definitions:

- Definition 2.1, p.788: the alternating sum of alpha-powers of side lengths vanishes; quads need not be proper or convex
- Definition 2.4, p.789: a realization is a vertex map with the quad conditions; it is distinct from an embedding
- Definition 2.5, p.790: six boundary vertices are distinct and the two alternating triples are noncollinear
- Remark 2.8, pp.792-793: outer balance makes the third construction-curve equation dependent
- Remark 4.8, p.811: the proposed three-intersection bound is retained for two construction curves sharing a focus

The definition and conjecture pages were also visually inspected in the published PDF. The candidate addresses these hypotheses. No convexity, cyclic order in the geometric plane, common face orientation, or noncrossing condition may be imported from the separate proper-embedding problem.

Independently fetched PDF hashes:

- Original OWR: `2a70b32e89e824135a1a5f62f0fbc79765d92136ff3172b5ceb0f268bba37a2c`
- Published paper: `42f93be598b2550859d56c3112fc8ebb30482ee5545cb031353b23ef2c2c2a44`

This is a source-target validation, not an exhaustive novelty search.

## 2. Radius reduction: no extraneous roots

Set A=(0,0), B=(b,0), C=(c,d) with the candidate's exact rational b,c,d, and positive levels lambda and mu. For a genuine solution let s=|X-A|^16. The squared distances are respectively u=s^(1/8), v=(s+lambda)^(1/8), w=(s+mu)^(1/8). Subtracting the squared-distance equations gives

2bx=b^2+u-v,

2cx+2dy=c^2+d^2+u-w.

Because b and d are nonzero, these determine exactly the candidate's x(s), y(s). Conversely, if its residual G(s)=x(s)^2+y(s)^2-u vanishes, these equations recover all three squared distances, and raising them to the eighth power recovers the original sixteenth-power differences. The radicands used in the example are positive. No sign choice or squaring step creates an extraneous solution.

G is continuous on the positive parameter interval. Distinct values of s at roots yield distinct points because the recovered point satisfies |X-A|^16=s. Thus five disjoint intervals with sign changes suffice; neither monotonicity nor uniqueness in any interval is required.

## 3. Independent exact sign certificate

The separate checker represents intervals as pairs of Fractions and bounds each eighth root by **binary integer search at scale 2^256**. It verifies the two bounding eighth-power inequalities exactly. This differs from the author's 2^200 scale and three nested integer square roots.

It independently establishes all six displayed coarse residual bounds:

| s | Strict enclosure for G(s) |
|---|---|
| 9/10000 | (0.38,0.39) |
| 11/10000 | (-0.28,-0.27) |
| 13/10000 | (0.51,0.52) |
| 1/2 | (-0.91,-0.90) |
| 1 | (9,10) |
| 10^17 | (-39,-38) |

All decimals in this table denote exact rational numbers. In particular, the last, large-radius sign is certified by rational arithmetic rather than floating-point cancellation. The five successive open gaps are disjoint and each contains a root by the intermediate value theorem.

The checker then performs **110 fresh exact sign-preserving bisections** within each gap. It validates both retained endpoint signs, computes coordinate boxes, and checks all five boxes pairwise disjoint. No recorded decimal approximation or author-computed sign is an input to these decisions.

## 4. Algebraic boundary construction and nondegeneracy

The boundary parameter equation has the form

|q|^16 [( (t-1)^2+h^2 )^8 - ( t^2+h^2 )^8] = level.

For g(t)=(t^2+h^2)^8, g''(t)=16(t^2+h^2)^6(15t^2+h^2), which is positive for the nonzero h used here. Hence g' is strictly increasing and g(t-1)-g(t) strictly decreasing. The polynomial has leading term -16t^15, up to the positive factor |q|^16, and therefore has opposite infinite limits. Each boundary parameter exists and is unique. This supplies exact algebraic vertices, rather than merely small residuals at numerical vertices.

The independent checker starts from its own rational brackets and performs **180 bisections** for each of t1,t3,t5. The final polynomial signs are checked exactly. It recovers every coarse coordinate enclosure stated in the candidate, the exact even determinant 0.00132672, and the odd determinant in (6.37,6.39).

It also verifies:

- All six boundary vertices are pairwise distinct
- All 20 boundary triples are noncollinear, stronger than the two alternating-triple requirement
- Every one of the five outgoing center boxes is disjoint from every boundary box
- Every outgoing center is off every line through two boundary vertices
- The stated A3 exclusion residual belongs to (0.98,0.99)

The analytical x<b/2 exclusion and the exclusions of the even foci are valid, though the independent box tests also establish the required distinctness directly.

## 5. All three outgoing quad identities

Write Eij=|Ai-Aj|^16. The exact boundary definitions give

E61-E12=mu, E34-E23=lambda, E56-E45=mu-lambda.

Every outgoing point has

|X-A4|^16-|X-A2|^16=lambda,

|X-A6|^16-|X-A2|^16=mu.

The difference of these two equations gives the third difference mu-lambda. These are exactly the alternating side-power identities for A2 A3 A4 X, A4 A5 A6 X, and A6 A1 A2 X, respectively. Their signs and vertex ordering agree with the source definition. All the required edge lengths are positive by the distinctness tests.

## 6. Direct incoming realization

The construction does not rely on assuming the flip theorem. With common focus A3, other foci A5,A1, and exact algebraic levels

L=E45-E43, M=E21-E23,

the candidate solves the two squared-distance differences by an invertible 2-by-2 linear system and imposes its remaining radius equation H(s)=0. The same converse argument as for G proves exact equivalence. Positivity of L and M, and nonvanishing of the determinant, are independently certified.

The interval evaluation retains dependence conservatively: every occurrence of a boundary coordinate encloses the same actual algebraic point, while interval operations may enlarge rather than shrink the set of possible values. The resulting endpoint signs therefore hold for the actual fixed boundary configuration. Independently computed bounds are

H(1/100) in (0.00037,0.00038),

H(11/1000) in (-0.00081,-0.00080).

Continuity gives an incoming center Z. Its box lies within the candidate's stated x and y ranges. It is disjoint from all six boundaries, from all five outgoing center boxes, and from every boundary-pair line.

The L and M equations give the old quads A3 A4 A5 Z and A1 A2 A3 Z. For the remaining one,

M-L-(E61-E65)=E12+E34+E56-E23-E45-E61=0.

The last equality follows by adding the three exact boundary identities, with the first reversed. Thus A5 A6 A1 Z also satisfies its exact quad equation. This verifies an actual admissible incoming instance, not just five intersections detached from the original move.

## 7. Arithmetic audit and scope

The author's interval addition, subtraction, multiplication, square, and division are outward enclosures with exact rational endpoints. Division rejects intervals meeting zero. The author's nested integer-square-root calculation indeed returns the floor of the eighth root of the scaled integer; its final power test independently checks each bracket. Floating-point conversion is used only for explanatory output. Bisection decisions and geometric tests use exact comparisons.

The separate checker uses different root arithmetic and fresh isolations, and reproduces every substantive inequality needed for the proof. Its receipt records full rational enclosures. A separate symbolic coefficient check confirms the outer balance and third incoming quad identity; the proof above supplies the mathematical interpretation of those coefficients.

**Publication disposition:** this reviewed proof supports `claimed_solved` for the proposed upper bound of three, with the conclusion stated as **at least five**. It does not support `already_solved`, a claim that five is maximal, a claim about proper embeddings, or a claim that the result is historically new. Those distinctions should remain explicit in any PR.
