# Adversarial gate review: all-`n` theta sharpness theorem

Date: 2026-08-09  
Scope: standalone mathematical sharpness result only  
Implementation: Python standard library, exact arithmetic, no imported
historical graph/Fourier code  
Manuscript sources edited: none

## Gate verdict — PROVED

**PROVED.** Under the standard semi-directed convention stated below, the
proposed sharpness theorem is mathematically valid as a standalone result:
for every integer `n >= 4` there are two nonisomorphic, non-ordinary-`T`
equivalent binary level-2 standard semi-directed networks

```text
N_n, N'_n in W_TC \ S_TC
```

whose open Jukes--Cantor model images share a regular region of full dimension
`2n`.

The four-leaf base pair was reconstructed from primitive arcs.  Its rooted and
mixed topology, five admissible rootings, blobs, level, cycles, exact physical
point, all 256 Fourier coordinates, all 256 inverse-Fourier pattern
coordinates, six full-model polynomial identities, and two nonzero
rank-eight Jacobian certificates were independently checked.  The all-`n`
claim then follows from a quantified cherry-substitution proof with an
explicit positive analytic inverse; it is not an extrapolation from a finite
regression.

No theorem-bearing item required for this sharpness conclusion remains
`FALSE` or `UNRESOLVED`.  Two convention blind spots were found and are
recorded in this review.  Neither invalidates the theorem once the standard
conventions are pinned.

## Claim ledger

| Label | Claim | Gate result |
|---|---|---|
| **EXACTLY COMPUTED** | Both supplied four-leaf graphs are binary rooted DAGs, their roots are LSAs, and the supplied rootings are tree-child. | Pass |
| **EXACTLY COMPUTED** | Each standard reduction has one level-2 blob, cycle rank two, three simple cycles of lengths `3,5,6`, and one triangle. | Pass |
| **EXACTLY COMPUTED** | Exhausting all root sites and all orientations gives five admissible rootings for each mixed graph; all five pass the LSA filter, exactly two are tree-child, and three are not. | Pass |
| **PROVED** | Both topologies lie in `R_TC` and `W_TC \ S_TC`. | Pass |
| **PROVED** | The pair is leaf-labelled nonisomorphic and is not equivalent under ordinary triangle redirection `T`. | Pass |
| **PROVED** | Every source and target edge multiplier and inheritance probability is strictly in `(0,1)`. | Pass by exact rational intervals |
| **EXACTLY COMPUTED** | The full displayed-tree sums agree in all 256 four-leaf Fourier coordinates in `Q(beta)`. | Pass, zero mismatches |
| **EXACTLY COMPUTED** | The inverse Klein-four transform agrees in all 256 pattern coordinates; the common pattern point is strictly positive. | Pass, zero mismatches |
| **EXACTLY COMPUTED** | Six common polynomial identities vanish identically on each full parameterization. | Pass by sparse-polynomial expansion |
| **EXACTLY COMPUTED** | Independent source and target `8 x 8` Jacobian determinants are nonzero. | Pass by two exact determinant algorithms |
| **PROVED** | Each four-leaf JC model has exact dimension eight and the same irreducible localized closure. | Pass |
| **PROVED** | The two physical images share a regular eight-dimensional relatively open germ. | Pass by inverse-function argument |
| **PROVED** | One cherry substitution is a positive analytic embedding with positive analytic inverse and raises image dimension by exactly two. | Pass |
| **PROVED** | Repeated substitution preserves equality, regular full-dimensional overlap, `R_TC`, `W_TC \ S_TC`, level two, nonisomorphism, and non-`T` separation for every `n >= 4`. | Pass |
| **PROVED** | The all-`n` model dimension is `8+2(n-4)=2n`. | Pass |
| **FALSE** | “The collision calculation by itself detects a mistaken use of `Z4` addition in place of Klein-four XOR.” | False: this collision also survives that mutation |
| **FALSE** | “Tree-child witnesses remain if admissible roots are artificially restricted to undirected edges.” | False: both witnesses use compatible retained-arrow edges |
| **UNRESOLVED** | Priority, novelty, and completeness of the external literature search. | Outside this mathematical gate |
| **UNRESOLVED** | The quarantined broader positive `S_TC` identifiability theorem. | Independent of this standalone sharpness theorem |

## Locked conventions

**PROVED.** The result uses the following operational definitions, all of
which are implemented rather than inferred from status prose.

1. A rooted binary network has root bidegree `(0,2)`, ordinary tree-vertex
   bidegree `(1,2)`, reticulation bidegree `(2,1)`, and leaf bidegree `(1,0)`.
   It is acyclic and every vertex is root-reachable.
2. The standard semi-directed reduction retains arrowheads precisely on
   edges entering reticulations, makes ordinary edges undirected, and
   suppresses the binary root once.  It performs no further degree-two
   cleanup or broad deletion of reticulation artifacts.
3. An admissible rooting may insert its root on an undirected edge or on a
   compatible retained edge entering a reticulation.  Every orientation must
   have the required rooted binary bidegrees, be acyclic, and reduce exactly
   back to the starting mixed graph.
4. `R_TC` means that the supplied rooted DAG is tree-child.  `W_TC` means that
   at least one admissible rooting is tree-child.  `S_TC` means that every
   admissible rooting is tree-child.
5. Mixed-graph isomorphism preserves every leaf label, every retained
   arrowhead, and vertex roles.  Ordinary `T` equivalence erases
   reticulation status and arrowheads only within the unique triangle; all
   exterior marks and labels remain fixed.
6. The state group is `Z2 x Z2`, encoded by bitwise XOR.  The four-state JC
   edge multiplier is `x_e=1-4q_e`, with physical open domain `0<x_e<1`, and
   reticulation choices are mixed with inheritance probabilities in `(0,1)`.

**PROVED.** The base-pair conclusions survive the stricter convention that
the inserted root must be the lowest stable ancestor of all leaves: all five
admissible rootings pass that filter.  Thus the known disagreement between
broad root-artifact elimination and unrestricted rooted preimages elsewhere
does not affect this pair.

## Independent implementation boundary

**EXACTLY COMPUTED.** The verifier imports only Python standard-library
modules.  It reconstructs the following from first principles:

- rooted bidegrees, reachability, acyclicity, tree-childness, and LSA status;
- standard semi-directed reduction;
- labelled mixed-graph isomorphism and the ordinary-`T` quotient;
- simple cycles and Tarjan biconnected components;
- exhaustive admissible root sites and orientations;
- displayed trees and JC Fourier edge-split monomials;
- sparse multivariate polynomials over `Q`;
- the quadratic field `Q(beta)` as pairs `a+b beta`;
- exact rational interval arithmetic;
- forward-mode exact differentiation;
- determinant calculation both by elimination and by cofactor recursion;
- the Klein-four character transform and inverse transform;
- cherry substitution on graphs, parameters, and full tensors.

No historical verifier was imported or executed.  Historical status strings
were ignored.  The downloaded verifier files were read only for provenance
hashing and were not used as code dependencies.

## Four-leaf topology gate

### Rooted DAGs and standard reductions — EXACTLY COMPUTED

The common internal arcs are

```text
rho->A, rho->C, A->B, B->C, C->D, D->E, A->F, E->F.
```

`C` and `F` are the reticulations.  The pendant arcs are

```text
N:       B->L1, D->L2, F->L3, E->L4,
N_prime: E->L1, D->L2, F->L3, B->L4.
```

Every rooted bidegree is correct, both graphs are acyclic and root-reachable,
both roots are LSAs, and every internal vertex has a tree or leaf child.  Thus
the supplied representatives lie in `R_TC`.

Suppressing `rho` combines `rho->A` and `rho->C` into the retained edge
`A->C`.  The retained edges are exactly

```text
A->C, B->C, A->F, E->F,
```

and the internal undirected edges are `A--B`, `C--D`, and `D--E`.  The
underlying nontrivial blob has vertex set `{A,B,C,D,E,F}`, seven edges, cycle
rank `7-6+1=2`, and reticulations `{C,F}`.  Its three simple cycles are

```text
A-B-C-A                 length 3,
A-C-D-E-F-A             length 5,
A-B-C-D-E-F-A           length 6.
```

Therefore each topology is binary, level two, and has exactly one triangle.

### Exhaustive admissible rootings — EXACTLY COMPUTED

There are seven undirected and four retained edges in each standard mixed
graph.  The search checked

```text
7 * 2^6 + 4 * 2^7 = 960
```

root-site/orientation candidates per topology.  It rejected any candidate
with a wrong bidegree, directed cycle, failed exact reduction, or failed LSA
condition.  Exactly five rootings survive:

| Root site in `N` | Root site in `N_prime` | LSA | Tree-child | Failure if not tree-child |
|---|---|---:|---:|---|
| `A->F` | `A->F` | yes | yes | — |
| `A->C` | `A->C` | yes | yes | — |
| `B--L1` | `B--L4` | yes | no | `A` has children `C,F` |
| `B->C` | `B->C` | yes | no | `A` has children `C,F` |
| `A--B` | `A--B` | yes | no | `A` has children `C,F` |

The full arc set and SHA-256 hash of every surviving rooting are in
`certificate.json`.

**PROVED.** Two tree-child witnesses prove `W_TC`; any one of the other three
proves not-`S_TC`.  Together with the supplied tree-child rooting, both
networks lie in `R_TC` and their standard reductions lie in
`W_TC \ S_TC`.

### Labelled separation and ordinary `T` — PROVED

The verifier exhausted color-preserving internal-vertex permutations.  The
graphs are isomorphic only after forgetting leaf labels; the explicit
label-blind witness fixes every internal vertex and swaps `L1` with `L4`.

With labels retained, `L1` is adjacent to `B`, a vertex of the unique
triangle, in `N`.  In `N_prime`, `L1` is adjacent to `E`, which is not on any
triangle.  Labelled graph isomorphisms preserve this property.  Ordinary
triangle redirection also preserves it because that operation changes marks
within the triangle but does not move leaves or change the underlying graph.
Thus the pair is neither isomorphic nor ordinary-`T` equivalent.

## Exact physical point

### Quadratic root isolation — PROVED

Let

```text
p(beta)=43337075 beta^2-36083110 beta+7336259.
```

The verifier works in the two-basis field `Q(beta)` and proves that `p` is
irreducible over `Q`: its discriminant is the positive nonsquare integer

```text
30262801262400.
```

For

```text
l=441/1250,  u=3529/10000,
```

exact substitution gives

```text
p(l)=13119323/62500 > 0,
p(u)=-1360417797/4000000 < 0.
```

The derivative is negative throughout `[l,u]`, and `u` lies below the axis
`10339/24835`.  Hence the interval contains exactly the smaller real root.

### Every open parameter inequality — PROVED

The source multipliers are

| Source arc | Multiplier |
|---|---:|
| `rho->A`, `rho->C` | `2/3`, `3/4` |
| `A->B`, `B->C` | `3/5`, `1/2` |
| `C->D`, `D->E` | `9/20`, `2/5` |
| `A->F`, `E->F` | `1/2`, `1/3` |
| `B->L1`, `D->L2`, `F->L3`, `E->L4` | `1/5`, `1/2`, `1/2`, `3/8` |
| `lambda_C`, `lambda_F` | `1/2`, `1/2` |

Every listed rational is strictly between zero and one.

The target's rational multipliers are

| Target arc | Multiplier |
|---|---:|
| `rho->A`, `rho->C` | `2/3`, `3/4` |
| `B->C`, `E->F`, `D->L2` | `1/2`, `1/2`, `1/2` |
| `C->D`, `D->E` | `9934/12215`, `171/775` |
| `F->L3`, `E->L1` | `1767/4832`, `31/190` |
| `lambda_C`, `lambda_F` | `1/2`, `1/2` |

The three beta-dependent target multipliers have exact interval enclosures

| Target arc | Expression | Exact enclosure |
|---|---|---|
| `A->B` | `24835 beta/(20678-24835 beta)` | `[44703/60797, 17528543/23827457]` |
| `A->F` | `10339/(53010 beta)` | `[10339000/18707229, 26375/47709]` |
| `B->L4` | `3/(20 beta)` | `[1500/3529, 125/294]` |

Every lower endpoint is positive and every upper endpoint is below one.  The
effective suppressed-root multiplier is exactly

```text
x_AC=(2/3)(3/4)=1/2.
```

Consequently every corresponding JC substitution probability
`q_e=(1-x_e)/4` lies strictly in `(0,1/4)`.  The other quadratic root is not a
physical alternative: it forces the `A->B` multiplier into

```text
[23827457/17528543, 60797/44703] subset (1,infinity).
```

## Exact Fourier equality

### Formula reconstructed from displayed trees — PROVED

For a displayed tree and leaf characters `g=(g_1,...,g_4)` in `Z2 x Z2`, the
verifier computes

```text
qhat_T(g) = product over edges e of x_e^[ XOR_{i in A_e} g_i != 0 ]
```

when the total XOR is zero, and zero otherwise.  At each of `C` and `F` it
deletes the unchosen incoming edge, uses the selected parent, and multiplies
by the selected inheritance weight.  Summing the four parent-choice products
gives the full network coordinate.  Degree-two suppression is unnecessary in
this calculation: consecutive edges with the same split contribute their
product automatically.

The sparse symbolic maps also prove that `x_(rho,A)` and `x_(rho,C)` occur
with equal exponents in every monomial, so they enter only through their
product.  This checks rather than assumes the root-split convention.

### State-group and orbit lock — EXACTLY COMPUTED

The verifier checks all six automorphisms of the Klein four-group for the
homomorphism identity, partitions all 64 zero-total four-tuples, and obtains
15 JC orbits: normalization plus the fourteen supplied nonconstant
representatives.  It independently constructs the `4 x 4` character table
and verifies

```text
H H^T = 4 I.
```

Thus the inverse scale is `1/4` per leaf.  This explicit check is necessary
because the collision itself is accidentally insensitive to replacing XOR by
addition modulo four.

### Coordinate comparison — EXACTLY COMPUTED

At the exact source and target points:

- all 192 assignments with nonzero total character vanish on both sides;
- all 64 zero-total assignments are nonzero and agree in `Q(beta)`;
- the fourteen derived orbit values exactly equal the claimed rational
  vector;
- all 256 inverse-Fourier pattern coordinates agree;
- the pattern probabilities sum to one and the smallest is
  `40819/12288000 > 0`.

The common Fourier tensor SHA-256 is

```text
880f9afdfc9ab7c241983e718042e861e2052d921fd3ebc79ddb081825796199
```

This is an equality of the full tensor, not only of fourteen manually entered
values.

## Dimension and regular overlap

### Common upper bound — PROVED

**EXACTLY COMPUTED.** Direct expansion of the full displayed-tree maps, with
independent edge variables and independent `lambda_C,lambda_F`, gives the
following six identities for both topologies:

```text
J-K-M+N = 0,
J-AH-BF+CE = 0,
GL-EN = 0,
L^2-BEH = 0,
BM-DL-B^2F+BCE = 0,
BEO-BGH-CEL+DEH = 0.
```

The symbolic parameterization hashes are

```text
N:       52139d2f62130176033f0afbf30175d950549c2785b48bb1e41df92725998906
N_prime: 60c518f35a280f87b5e81f95369cfce71ac77957f388b7ef52fd5be644634190
```

**PROVED.** On `BE != 0`, five equations reconstruct

```text
J=AH+BF-CE,
N=GL/E,
M=(DL+B^2F-BCE)/B,
K=J+N-M,
O=(BGH+CEL-DEH)/(BE).
```

The remaining equation is `L^2=BEH`.  Equivalently, because `BE` is
invertible, it reconstructs `H=L^2/(BE)`.  The localized locus is therefore
irreducible and eight-dimensional.  It is smooth because the derivative with
respect to `H` is `-BE`, which is nonzero throughout the physical locus.
Every physical `B` and `E` is a positive sum of positive monomials, so no open
model point is lost by this localization.  Hence both model dimensions are at
most eight.

### Two rank-eight certificates — EXACTLY COMPUTED

The Jacobians were obtained by differentiating the independently enumerated
displayed-tree sums with exact forward-mode arithmetic.  Each determinant was
computed twice, once by field elimination and once by recursive cofactor
expansion; the results agree.

For `N`, the rows are `(A,...,H)` and the columns are

```text
(x_D2,x_DE,x_E4,x_EF,x_F3,x_CD,x_AB,x_B1).
```

The exact determinant is

```text
531441/16384000000000000000 != 0,
```

and the matrix SHA-256 is

```text
1a7592eaf697eea79c757e27981dc2293e5865a037bb97ac8501eb1dbca7f472.
```

For `N_prime`, the columns are

```text
(x_D2,x_DE,x_AF,x_AB,x_F3,x_CD,x_E1,x_B4).
```

The determinant is

```text
97608431685933/382537302016000000000000000
- (46892453833449/76507460403200000000000000) beta.
```

It is nonzero because `beta` is irrational and its beta coefficient is
nonzero; independently, its entered factorization consists entirely of
strictly nonzero physical factors.  The matrix SHA-256 is

```text
f653e653c8bbc46933836b29a6fbe7e357d248a551e4abf957234069e3b6f5b9.
```

The rank lower bound eight and invariant upper bound eight prove exact model
dimension eight for each topology.  Since each model closure is irreducible,
is contained in the common irreducible eight-fold, and has the same dimension,
both closures equal that eight-fold.

### Full-dimensional stochastic overlap — PROVED

Closure equality or one matching point would not be enough.  The required
physical overlap follows as follows.

1. Restrict each parameterization to its displayed eight-variable gauge
   slice.  All fixed and free parameters are interior physical values.
2. The corresponding map to `(A,...,H)` has a nonzero determinant at the
   matching point.  The analytic inverse-function theorem therefore gives an
   open neighborhood of the same `(A,...,H)` point in each projected image.
3. Intersect those two neighborhoods.  For every first-eight vector in the
   intersection, both network tensors satisfy the six common identities.
4. On a sufficiently small physical neighborhood, `B,E,H,L` remain positive.
   Thus `L^2=BEH` selects the same positive value of `L` in both images, and
   the five rational reconstruction formulas force the same `J,K,M,N,O`.
5. The fourteen orbit coordinates determine the full Fourier tensor and the
   pattern distribution.

The intersection is therefore a relatively open eight-dimensional region in
each model image, and the rank certificates make it regular on both sides.

## All-`n` cherry-substitution theorem

### Explicit family — PROVED

For definiteness, retain labels `1,2,3,4` in the base pair.  At step `n`,
replace labelled leaf `2` in both networks by a cherry whose children are the
retained leaf `2` and the new leaf `n`.  Repeating this operation gives a
specific pair `N_n,N'_n` on `[n]` for every `n >= 4`.

### Exact tensor transform and inverse — PROVED

Write the old tensor as `P(g_X,k)`, where `k` is the character at the selected
leaf.  Preserve the old pendant multiplier on the new stem and give the two
new arms multipliers `u,v in (0,1)`.  Direct displayed-tree propagation gives

```text
P_tilde(g_X,g_1,g_2)
  = P(g_X,g_1 XOR g_2) u^[g_1!=0] v^[g_2!=0].
```

The verifier compared this formula with a fresh five-leaf displayed-tree
enumeration on all `4^5=1024` coordinates for both networks and found zero
mismatches.  Both routes give the same extended tensor hash

```text
e55a5752c0d1505c6733f89237ceb6130bb5c22b583a2f9f12027a1665e6e004.
```

For any nonzero `h`, exact positive coordinates recover

```text
uv  = P_tilde(0,h,h),
u/v = P_tilde(g_X,h,0)/P_tilde(g_X,0,h),  XOR g_X=h.
```

The common base factor in the ratio is strictly positive.  Hence

```text
u=sqrt((uv)(u/v)),  v=sqrt((uv)/(u/v))
```

with the unique positive roots, and then

```text
P(g_X,k)=P_tilde(g_X,k,0)/u^[k!=0].
```

This is a positive analytic inverse.  Thus the substituted model image is
analytically equivalent to the old image times `(0,1)^2`, not merely mapped
onto it non-injectively.

### Dimension and common germ — PROVED

The exact analytic product implies

```text
dim M_(n+1) = dim M_n + 2.
```

Starting at dimension eight gives

```text
dim M_(N_n) = dim M_(N'_n) = 8+2(n-4)=2n.
```

If `O` is the common regular germ at one stage, applying the same cherry map
to `O x (0,1)^2` puts a relatively open regular germ of dimension two larger
in both next-stage images.  Induction preserves equality and
full-dimensional regular overlap for every `n`.

### Class and level preservation — PROVED

- Replacing a leaf child by a tree child with two leaf children preserves the
  supplied rooted tree-child property, so `R_TC` persists.
- Applying the same operation to either base tree-child admissible rooting
  gives a tree-child admissible rooting of the substituted mixed graph, so
  `W_TC` persists.
- Applying it to any base non-tree-child rooting leaves vertex `A` with the
  two reticulation children `C,F`; that rooting still reduces exactly to the
  substituted mixed graph.  Therefore not-`S_TC` persists.
- The inserted tree and its two arms are attached through bridges.  No blob,
  cycle, retained arrow, or reticulation is added.  Binary degree and level
  two are preserved.
- LSA validity persists: no new vertex can dominate all old leaves, and every
  old nonroot failed to dominate all old leaves already.

The verifier extended all five base rooting witnesses and checked these facts
for each `4 <= n <= 12`.  Those finite checks are regression tests only.  The
preceding local argument quantifies over every substitution step and is the
proof for all `n`.

### Nonisomorphism and non-`T` preservation — PROVED

The construction substitutes only at leaf `2`; it never changes leaf `1` or
the unique theta blob.  Therefore leaf `1` remains adjacent to a triangle
vertex only in `N_n`.  This labelled property is invariant under graph
isomorphism and under every redirection confined to the triangle.  Hence the
two networks remain nonisomorphic and non-ordinary-`T` equivalent for every
`n`.

## Adversarial convention findings

### Retained-edge root sites are load-bearing — FALSE if omitted

**FALSE.** It is not safe to enumerate roots only on undirected edges.  Under
that nonstandard restriction, each graph has two admissible rootings and zero
tree-child rootings.  Both actual tree-child witnesses insert the root on a
compatible retained edge, `A->C` or `A->F`.  A standalone paper must state
this permission in its definition of admissible rooting; the present theorem
then passes exactly.

### The collision is state-group-blind — FALSE as a convention test

**FALSE.** Equality at this point does not distinguish Klein-four XOR from
cyclic addition modulo four: the mutated source and target still have zero
coordinate mismatches.  This does not alter the JC proof because the verifier
separately checks the Klein-four automorphisms, orbit representatives,
character table, and inverse transform.  A standalone presentation should not
claim that the collision itself validates the group convention.

### Inheritance-parent order is point-blind

**EXACTLY COMPUTED.** Both inheritance probabilities equal `1/2`, so swapping
the named first and second parent is invisible at the certified point.  This
is harmless for existence and rank at this point, but it would be poor
convention evidence.  The symbolic invariant checks therefore retain
independent `lambda_C` and `lambda_F` variables and the primitive data records
the parent order explicitly.

### Mutations that were detected — EXACTLY COMPUTED

- undirecting the suppressed `A->C` edge makes reticulation `C` invalid;
- retaining only one displayed tree causes 63 source-target mismatches;
- swapping leaf axes `1` and `4` causes 36 tensor mismatches;
- selecting the larger quadratic root forces an edge multiplier above one;
- changing a sign in the first common invariant leaves seven nonzero sparse
  terms;
- ignoring leaf labels collapses the pair, as expected, which confirms that
  labelled isomorphism is essential.

## Standalone-submission assessment

**PROVED.** The sharpness theorem is self-contained mathematically and does
not depend on the unresolved positive identifiability theorem, finite atlas,
bridge factorization, or global gluing program.  It can serve as the central
result of a standalone submission if the submission includes:

1. the six locked conventions above, especially compatible retained-edge root
   insertion;
2. the explicit four-leaf arc lists and the labelled triangle-adjacency
   separation;
3. the displayed-tree Fourier formula and exact quadratic point;
4. the six common identities, the localized dimension argument, and both
   rank-eight certificates;
5. the inverse-function proof of physical overlap, not only closure equality;
6. the positive cherry inverse and explicit all-`n` construction.

**UNRESOLVED.** This gate does not certify bibliographic novelty, priority,
journal fit, exposition quality of any existing manuscript, or consistency of
the quarantined positive-theorem manuscript.  Those are separate review
obligations.  No manuscript source was changed during this audit.

## Reproduction and hashes

Run from the release root:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 reproducibility/independent/verify_sharpness.py --instance reproducibility/independent/instance.json --output /tmp/stc-jc-sharpness-certificate.json
```

Expected result:

```text
PASS final_verdict=PROVED
certificate_sha256=38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7
```

The run was repeated under `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654`; both produced byte-identical certificates with the
same hash.

Core audit artifacts:

| File | SHA-256 |
|---|---|
| `verify_sharpness.py` | `93a29ea6fdd1eba1671cf720a3929c2e2cab6ef5882c89a355d7cef04406c639` |
| `instance.json` | `cca38c3928c7eb768f5dabf480d8eae16ef5a08b7576ffe2780e6a7deaeb337b` |
| `certificate.json` | `38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7` |

The active hashes above were reissued after the final manuscript referee
identified an inert post-root degree-two cleanup loop.  Removing that loop
makes the implementation literally match the manuscript's narrow `sd_0`
definition; it changes only the implementation hash recorded inside the
certificate.  The corrected artifacts are independently re-audited in
`repair/reviews/MANUSCRIPT_FINAL_REREVIEW.md`.

Raw input provenance:

| Read-only input | SHA-256 |
|---|---|
| downloaded `networks.json` | `80b07f82641bf7d9e7a96abdbaae1c36cba7fc070cc3163214eee639fc43e9af` |
| downloaded counterexample `manuscript.tex` | `4b3001444c29fa7926f14793e0fe4082834fc13e02e9096f76fc996d06badaa4` |
| untrusted closure status certificate | `d0bca08bd6df796655b2a7b9d0fa44b013dfb689042505bc6e522a3f7939d7de` |
| closure verifier not imported | `1df20e19ab9cb7c4f52518cfe402cc5ed9f79453f094a8e8e824cdb803fa38d4` |
| counterexample verifier not imported | `c790585c83515141d3dfff20084548a8372c132205cba01f934f017009c6bbb9` |

`repair/independent/sharpness/MANIFEST.sha256` records the remaining final
artifact hashes, including this review.
