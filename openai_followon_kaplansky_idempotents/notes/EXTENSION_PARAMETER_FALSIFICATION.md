# Independent falsification audit: the q=32 Fano-extra construction

Reviewer: internal parameter-falsification subagent, 2026-10-07 05:56 UTC
(2026-10-06 22:56 PDT). This is an automated mathematical audit, not human
peer review or formal verification. Checkpoint estimates: 100% of this
parameter-sensitive mathematical audit; 0% of a new publication package
reviewed by this agent.

## Exact claim and verdict

The claim audited is that the October 4 family-197 construction, pinned at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, works with q=32 instead of
q=128, using the same seven Fano-complement extras, the same matching
model, and the same topology and parity mechanism. Its alphabet then has
1064 signed letters and its rose has 532 geometric edges. Some sufficiently
large finite matching outcome gives a torsion-free finitely presented
group with a finite two-dimensional classifying complex and scalar
a,b,c over F_2 satisfying ab=1, ac=0, c≠0. The core idempotent and
projective-module consequences follow by the already audited classical
ring argument.

**Verdict: no substantive parameter-sensitive obstruction found.** I read
the original user request and all seven source sections, 2079 lines in
total, before comparing my reconstruction with the earlier source audits.
The changed proof needs an explicit replacement of the source's numeric
degree and expansion constants; merely replacing the first occurrence of
128 would leave incorrect statements. With those replacements, each step
survives. Independent exact code also checks the full signed-alphabet
matrix, not just the proposed three-by-three formula.

An additional claim passes: q=32 is the least dyadic q for which the
**unchanged prescribed type model and unchanged turn weights** have the
squared-word decay used in the source. This is a statement about the
model's decay criterion. It does not establish that no different matching
model, different weights, different argument, or different group can work
with fewer letters. It gives no lower bound of 532 on the minimum number
of generators of a group with the desired ring-theoretic properties.

This report does not certify priority or publication novelty. Indeed the
source's original crude contraction vector already works at q=32. The
three-class calculation sharpens the contraction constant and certifies
failure at smaller dyadic q; it is not a repair of an invalid source proof.

## Reviewed sources and reproducible finite checks

All section-and-line references below are relative to
`sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/`.
I read `introduction.tex`, `random.tex`, `patterns.tex`, `planar.tex`,
`algebra.tex`, `topology.tex`, and `assembly.tex` in full. After forming
the independent parameter analysis, I compared it with
`reviews/source_combinatorics.md` and the topology source audit. The
earlier audits were corroborating evidence, not premises for the finite
matrix calculation or the degree replacements.

Independent checking artifacts:

- `notes/extensions_attack/check_parameter32.py`: Python standard-library
  script; uses exact `Fraction` arithmetic for every matrix certificate.
- `notes/extensions_attack/parameter32_checks.json`: successful run,
  including hashes of all seven actual source sections reviewed.

Reproduce from the project directory with:

```text
python3 notes/extensions_attack/check_parameter32.py
```

The script verifies the proposed quotient against every row of the full
matrix on 1064 letters at q=32, and likewise against every full row at
q=4,8,16. It constructs F_32 as
F_2[X]/(X^5+X^2+1), checks irreducibility by all monic degree-one and
degree-two divisors, enumerates all 1057 projective points and lines,
checks all 558096 pairs of points and all 558096 pairs of lines, and
checks the seven Fano complements. It has no random matching outcome,
finite relator list, reduced group-ring supports, or multiplication
certificate. Its m=13 check is only a type-capacity illustration, not an
assertion that the later probabilistic construction works at m=13.

## 1. Type construction, integrality, and parity

`random.tex:14–112` depends on q through the finite projective plane,
line size, incidence probabilities, and assignment capacity. With q=32:

    v=32^2+32+1=1057,  p=33/1057,  |T|=1057+7=1064.

The plane exists because 32 is a prime power. In the independent finite
enumeration, points are the normalized triples
(1,a,b), (0,1,a), (0,0,1), and lines are kernels of normalized nonzero
linear forms on F_32^3. Each line has 33 points, each point lies on 33
lines, and every pair of distinct points lies on exactly one line.
Every pair of distinct lines intersects at exactly one point. The
enumeration verifies all of these claims; the linear-algebra proof is
also identical to the source's proof over F_128.

The 7 extras can be paired with 7 distinct ordinary letters, and the
remaining 1050 ordinary letters can be paired with each other. Thus the
involution is fixed-point-free. The source requires no compatibility
between this arbitrary inverse pairing and projective-plane incidence.

With m≡1 (mod 4), the complement counts become

    a_m=(33m−1)/4,   b_m=33(m−1)/4.

They are integers and satisfy 4a_m+1=33m and 4b_m=33(m−1).
Distribute each complement as evenly as possible among the 1057 line
classes and allocate disjoint vertices for the seven complements. The
source's per-class capacity bounds now have coefficient

    7·33/(4·1057)=231/4228<1.

Consequently `7 ceil(a_m/1057)+1` and `7 ceil(b_m/1057)` are less
than m−1 for all sufficiently large admissible m. In fact the crude
ceiling bound already suffices for admissible m≥13; the proof needs
only eventual capacity. This preserves the distinguished full-extra
vertex and the prescribed root on the B side.

Ordinary intersections have size 33 on equal lines and 1 otherwise,
both odd. Extra intersections are 0,2,4 except for the distinguished
full set intersecting itself in 7. Hence the exceptional self-pair has
even size 33+7=40, and every other required intersection is odd. The
possible degrees are 33,37,40. Label balance remains exact on each
side, so each inverse-label bijection has |Y|p pairs. The parity proof
has not changed.

`random.tex:133–161` continues to give the three turn frequencies:

    ordinary–ordinary: 1/33;
    ordinary–extra:    p=33/1057;
    extra–extra:       1/2.

The formula is `np w(t,u)+O(1)` on either side. The B-side difference
from np is constant because v is fixed. Even distribution among line
classes gives a constant O(1) error when summed over 33 incident lines.
All positive turn weights remain less than one and bounded below by
1/33. These are the only weight properties used in the later bin
estimates beyond squared-word decay.

## 2. Exact squared-turn matrix and contraction

Let E be the 7 extra letters, S the 7 ordinary letters paired with
extras, and O the other v−7 ordinary letters. Inverse maps E↔S and
O↔O. For M_{t,u}=w(t,u)^2, a vector constant on these classes is taken
to another such vector. The exact row-sum quotient, in order E,S,O, is

    Q = [ 7p²,  6/(q+1)²,  (v−7)/(q+1)² ]
        [ 6/4,  7p²,         (v−7)p²       ]
        [ 7p²,  7/(q+1)²,  (v−8)/(q+1)² ].

This follows directly from the excluded inverse successor. A row in E
has ordinary inverse in S, so it excludes one S letter; a row in S has
extra inverse, so it excludes one E letter; a row in O excludes one O
letter. This is sensitive to row class, not merely to whether the row
letter itself is ordinary. The independent script counts all allowed
successors and all three squared turn categories for every actual row,
then compares to Q. No quotient formula is used in that enumeration.

At q=32, use the lifted positive vector with class values

    f=(1,13/5,1).

The exact coordinate ratios of Qf to f are respectively

    95146189/96562235,
    579417/592826,
    857592557/869060115.

Each is strictly less than λ=987/1000. Thus Mf<λf coordinatewise.
Since 1≤f≤(13/5)1, the total squared-word mass satisfies

    sum_{W∈T^h} P(W)^2
      = 1^T M^(h−1)1
      ≤ (13/5)|T| λ^(h−1).

For δ=−log(λ)/4>0, the right side is at most exp(−2δh) for all
sufficiently large h. The assertion is eventual, as in the source;
it is not supposed to hold for h=1.

As an attribution and necessity check, the source's original class
vector (1,4,1) also works at q=32. Its original crude row bounds are

    32/33 + 7p² + 21/33² = 57694220/57937341 < 1,
    6/4 + (1057+21)p²    = 116319/45602 < 4.

Therefore q=32 does not require a qualitatively new contraction
mechanism. The sharper certificate above and the exclusions below
are the added exact information.

## 3. What the smaller dyadic exclusions prove

For q=4,8,16, lift the positive class vector

    g=(193/500,1,97/250).

The exact ratios Qg/g are:

| q | E | S | O |
|---|---|---|---|
| 4 | 480733/303975 | 26959/21000 | 500011/305550 |
| 8 | 10342603/9256473 | 5726739/5329000 | 10523789/9304434 |
| 16 | 35146373/34932807 | 3571543/3549000 | 2078707/2065518 |

All nine ratios are strictly greater than β=503/500>1. For each
corresponding full matrix, Mg>βg. Since max g=1, one has 1≥g and

    1^T M^(h−1)1 ≥ β^(h−1) sum_t g(t).

The total squared-word mass grows exponentially, contradicting any
eventual bound exp(−2δh) with δ>0. Thus the source's precise
word-decay lemma is false for these q with unchanged turn weights.
This is stronger than failure of one trial upper-bound vector and
does not rely on numerical eigenvalue estimates or Perron root
rounding. It does not say the final group-ring theorem is false for
every conceivable construction at these alphabet sizes.

q=2 is already inadmissible for the unchanged balanced-extra scheme.
Its two balance equations would be 4a+1=3m and 4b=3(m−1);
subtracting gives 4(a−b)+1=3, an impossibility modulo 4. More
generally this balance scheme requires q≡0 (mod 4). Since q=1 is
not a field order, these checks cover every dyadic field order below
32. The exact conclusion is the minimum dyadic **decay-admissible
parameter in this fixed model**, not a universal optimality theorem.

## 4. Conditioning on large girth and switch counts

`random.tex:223–360` uses only finite fixed |T|, p>0, a fixed maximum
degree d_*, and a sufficiently small positive c_0. Set d_*=40 and,
for an explicit admissible choice, c_0=1/100. Then

    c_0 log(2|T|/p)<1,   2c_0 log d_*<1.

These can be certified without floating-point arithmetic:
2|T|/p=2249296/33<2^17<exp(17), and 40<2^6<exp(6).
The respective left sides are less than 17/100 and 3/25.
Let L=floor(c_0 log n) as in the source. The expected number of
edges on cycles shorter than L is o(n). A radius-2L endpoint
neighborhood excludes O(40^(2L+2))=o(n) edges. The smallest relevant
bijection has np−vp=np−33 pairs, a positive linear number.

Thus the distant good edge needed to remove any bad edge is still
available for large n. A target-transposition switch preserves all
types and creates no cycle shorter than L. Its geometric argument
uses distance and girth, not a minimum degree of 129. The same
reasoning includes old loops. Repetition removes bad edges until
the conditioning event is nonempty.

For conditioned prescriptions, the one-to-many injection remains
valid: from the switched output and requested pair x→y, recover
z=φ′(x) and u=(φ′)⁻¹(y), even with overlapping domain and codomain
vertex sets. The changed exclusion term is

    r_n=33+O(40^(2L+2))=o(n).

After s existing prescriptions, the additional-edge upper bound is
(np−s−r_n)^−1 when positive. For E=O(L), its accumulated exponent
error E(E+r_n)/n is o(L), exactly as in the source. No lower bound
for the probability of the girth event and no independence after
conditioning are assumed. All changes here are changes of fixed
constants.

## 5. Expansion and diameter: all changed numbers

`random.tex:375–447` is the place where the minimum degree matters.
A nonexpanding set S of size k sits inside a set Z of size 2k
containing at least

    r=ceil(33k/2) distinct edges,   16.5k≤r≤17k.

An edge contributes at most two to the degree sum, including the
loop convention; this bound is unaffected. The number of possible
labeled prescriptions with endpoints in Z is still at most
4|T|k², so the prescription-set count is at most (C_2 k)^r
for a fixed C_2. Choose ρ<1/4 and 17ρ<p/4. Since r_n=o(n),
the denominator for every exposure is at least np/2 eventually.

The union-bound exponent becomes

    33/2−2 = 14.5,

and the failure probability for this k is at most

    (C_3 (k/n)^14.5)^k.

Constants C_2,C_3 are allowed to change with the now-fixed
alphabet. For k≤sqrt(n), this is at most
(C_3 n^−7.25)^k; for sqrt(n)<k≤ρn, choose ρ smaller so
C_3ρ^14.5<1/2 and bound it by 2^−k. Both sums tend to zero.
Thus small-set expansion still holds on both sides under the
conditioned law. The exact substitutions are 129→33,
64.5→16.5, 65→17, 62.5→14.5, and 31.25→7.25.

The subsequent diameter argument needs only that expansion and
that each side has at most n vertices. Closed balls double until
they exceed ρn; balls with geodesic centers spaced 2R+1 are
disjoint, where R=ceil(log_2 n)+1. This gives a fixed d with
component diameter at most dL. It never assumes either graph is
connected. A potentially much larger fixed d is harmless for
the later order of quantifiers.

## 6. Bounded path systems and every weight-dependent interface

I reread all 594 lines of `patterns.tex`. None of its structural
arguments uses a degree of 129. Its parameter-dependent hypotheses
are exactly: fixed finite signed alphabet; fixed-point-free inverse;
positive reduced turn weights with a positive minimum and maximum
at most one; inverse-word symmetry; the eventual squared-word
decay; and the conditioned short-prescription bound. All hold
at q=32 by Sections 1,2,4 above.

The image-rank bound uses girth and O(L) total edges, not ambient
degree. The stationary nonbacktracking walk is on the suppressed
image multigraph, where minimum degree three is structural. Leaves
of the image can only be endpoints of the one exceptional interval.
Multiplicity is bounded by 2(C+K_0), because repeated traversal of
one oriented edge is separated by a reduced closed walk of length
at least L. Chains and unlabelled patterns remain bounded in number
for fixed K_0,C,I. The stage-incidence inequality retains its exact
root correction and no positive total power of n is introduced.

The common-grid construction and self-link count need only fixed
alphabet size and inverse-word symmetry. At q=32, the entropy
factor |T|^(κs+O(1)) is still exp(o(s)). Translation self-links
have nonzero shifts because paired positions use distinct underlying
edges. Reflection self-links still force a fixed inverse letter or
an inverse adjacent pair, so reduced words rule them out.

For the word bins, the minimum positive weight is 1/33. One may
choose a_0=2 log 33 for all sufficiently large block scales s;
then δs/2≤d_i≤a_0s. The lower bound and bin count come from
the new δ=−log(987/1000)/4. The fixed-stage expectation has
the same formula: internal turns supply npw(t,u)+O(1), marked
vertices supply at most n choices, and injective image embeddings
use E_j distinct prescriptions. O(1) frequency errors stay uniform
because all positive weights are fixed away from zero. Chain-junction
and fragment losses remain exp(o(L)).

Multiplying the deterministic stage bounds, with no independence
assumption, yields the unchanged inequality

    log product_j B_j ≤ −δH/2 + a_0 b_0 + o(L).

Choose ε=min{1/4, δ/[16(1+a_0)]}>0 before K_0,C,I. This gives
the same exp(−δL/(4M)+o(L)) probability bound. The new value of
ε may force enormous later constants, but they are fixed before
n tends to infinity. There is no numerical-size claim here.

## 7. Short closures and the full planar extraction

`planar.tex:66–119` has two explicit degree substitutions: 129
becomes 33 and 127 becomes 31. After deleting at most two edges
incident to a chosen base vertex, every remaining vertex still
has degree at least 31, hence at least three. It still has at
least 3·2^(k−1)>n nonbacktracking k-edge walks starting there,
with k=ceil(log_2 n)+1. Two ending at the same vertex give a
nonempty linearly immersed based loop avoiding the deleted edges.
This is enough to close the original segment without canceling
any original occurrence, even though the auxiliary loop need not
be cyclically immersed at its base.

The added length bound remains dL+4k, so any integer
D_0≥d+8/(c_0 log 2)+8 works. The original segment remains
unchanged. No hidden requirement of degree 127 is used.

I reread all remaining planar estimates, `planar.tex:130–440`.
The ribbon-neighborhood Euler identity, treatment of disconnected
regions, monogon exception at one break, same-band digons, and
paired-interval bound 6N′ are combinatorial and independent of q.
Recursive Lipton–Tarjan separation is also independent of q; this
audit treats that published separator theorem as the same external
input as the source, rather than claiming a new proof of it.

The needed order of constants is still

    (types,c_0,δ); (ε,d); D_0; U; η; K_0; (C,I); n.

In particular ε is fixed before the separator-derived K_0,C,I.
The source's choices U≥96D_0/ε, η≤ε/(64U), and
K_0≥(C_sep/η)^2 remain possible. All original-loss bounds
are unchanged: added closures cost at most εH_0/32;
deleted occurrences at most εH_0/32; total surviving length
is at least 15H_0/16; discarded high-loss and high-comparison
clusters cost at most H_0/16 each. An intact exceptional path
shorter than L costs less than H_0/2 because an ordinary boundary
is present. A bounded system remains with positive total length,
and it uses one fixed triple K_0,C,I for arrangements of every
finite size.

The possible new closures can revisit underlying edges. Their
positions are left unpaired, exactly as allowed by the bounded-path
theorem. The changes of δ,d,D_0,ε do not alter this interface.

## 8. Cone criterion, finite presentation, and ring consequences

The cone criterion in all 335 lines of `topology.tex` is stated
for any finite immersed graph and contains no q-dependent numeric
hypothesis. Its cone-picture replacements, minimal-length
arguments, all four band surgeries, the preservation of root
endpoints, and the lifted homology identity are unchanged. The
finite two-dimensional contractible-cover resolution still rules
out prime-order torsion. This report found no new issue in those
arguments, but does not label the construction formally verified.

The parity criterion in all 125 lines of `algebra.tex` uses
looplessness, the prescribed intersection parities, and root
protection. Large girth supplies looplessness; Sections 1 and 7
supply the other hypotheses. Restriction to the root components
preserves parity. The coefficient of 1 in c is one because no
other vertex in its root component has identity label. It does
not require that all root-to-vertex labels be pairwise distinct.

After one good matching is chosen, the rose has exactly 532
geometric edges. Its fundamental group surjects onto the cone
group. Choosing a maximal tree in every graph component yields
relators from its non-tree edges, all expressed in these 532 rose
generators. The cone's relative replacement by basis-loop disks
gives a finite presentation complex homotopy equivalent relative
to the rose; it is aspherical by the cone criterion. Thus this
construction gives a group generated by at most 532 elements,
with a finite two-dimensional K(G,1). It does not prove the group
needs 532 generators.

The source's `assembly.tex` then selects an eventual good finite
matching outcome, not a listed outcome. The witnesses remain
finite path-label sums a,b,c over F_2 with ab=1, ac=0, c≠0.
The already audited ring argument produces e=1−ba and P=eR;
it remains a scalar nontrivial idempotent over every field of
characteristic two, and P≠0 with R≅R⊕P and [P]=0. No
characteristic-zero, odd-characteristic, nonzero K_0 class, or
reduced C*-algebra projection claim is justified by the change.

## Findings and remaining gaps

No mathematical repair is required beyond explicitly propagating
the changed constants listed above. The strict model-minimum
claim has exact rational certificates and does not rely on a
floating-point eigenvalue calculation. A full publication review
must still examine the actual new manuscript and metadata; this
source-extension audit cannot substitute for that process.

The remaining issues are priority/novelty and package-specific
verification, assigned elsewhere. The correct attribution is to
the OpenAI construction and its full proof mechanism, with a
verified parameter refinement and a model-specific threshold
calculation. No numerical matching witness or new independent
solution of the underlying conjecture has been produced here.
