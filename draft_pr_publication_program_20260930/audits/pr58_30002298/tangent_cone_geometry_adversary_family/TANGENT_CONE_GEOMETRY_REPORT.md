# Independent tangent-cone geometry/valuation audit: PR58

The exact characterization passes this family's universal mathematical audit.
For compact finite unions of convex polytopes in R^d with unit ambient
Lebesgue density, the reduced Fantappiè denominator is the squarefree product
of the nonzero algebraic-vertex factors. Consequently the source's product
over V(P) is exact if and only if every nonzero point of V(P) is algebraic.
This is a complete local geometric characterization, including a finite signed
chamber test. It does not transfer the central difficulty to an unsupported
geometric-realization claim. The appropriate disposition is already_solved,
with the prior result credited to Akopyan–Bárány–Robins; no novelty is claimed.

Pinned original head: `465d771ec1ddc91877e8d9db51ed59aea1b0d97d`.
The candidate is `../original_preparation_family/original/SOURCE_STATUS.md`,
152 lines, 10960 bytes, SHA256
`fc9b927d0755ca48a61e4d2e90f5189c9d896e00a417ff8f1c10ec880bc8ec3e`.
All candidate line references below are to that exact body.

## Independence, exact question and primary access

This agent previously audited PR56 and PR57. PR58 began afresh by reading the
literal source_record.json and full candidate before historical reviewer or
checker bodies, or other fresh-family findings. The initial geometric route
was recorded in INITIAL_SCOPE_AND_GEOMETRY.md at 15:05:07 UTC, before the
source preparer's authentication/accounting was inspected. No historical
checker was read or replayed, and no other fresh family's findings were used.

The [official OWR 11/2013](https://ems.press/content/serial-article-files/46446),
printed pp.637–638 (private layout lines 2841–2910), specifies the normalized
unit-density transform on compact unions of convex polytopes. Its V(P) is the
intersection of all triangulation vertex sets. Question 1 follows a genuine
factor-cancellation example, so the reduced-denominator reading is justified.
Candidate lines 7–21 accurately retain those conventions.

The complete [ABR author manuscript v2](https://arxiv.org/pdf/1508.07594v2)
was acquired. The selected definitions, a.e. algebra, tangent construction,
full Lemmas 5–6 proof and Remark 10 were read; their relevant rendered pages
were inspected. Definition 1, Lemma 6 and Remark 10 are respectively at
printed pp.1,9–10,12 (layout lines 36–38,470–520,642–648). The last explicitly
identifies denominator vertices with algebraic vertices without a genericity
restriction. This is the prior result used by candidate lines 25–54.

[Publisher metadata](https://www.sciencedirect.com/science/article/pii/S0001870815302425)
and an actual [Crossref metadata receipt](https://api.crossref.org/works/10.1016/j.aim.2016.12.026)
confirm Advances in Mathematics 308 (2017), 627–644, DOI
10.1016/j.aim.2016.12.026. The publisher PDF request returned HTTP 403, with
the genuine failed response privately retained. This family has not asserted
byte identity of the author manuscript with the published article or
independently inspected the publisher's full typeset proof.

[Gravin–Pasechnik–Shapiro–Shapiro v2](https://arxiv.org/pdf/1210.3193v2),
printed p.3 (layout lines 137–165), supplies the simplex and partial-fraction
identities cited in candidate line 81. The theorem there is restricted to
simple convex polytopes; applying it separately to simplices avoids imposing
that restriction on P. The independent derivation below checks that extension
directly. The manuscript's general-density assertions are not needed here.

Whole source PDFs, bulk extracted text, selected page PNGs, Crossref body and
the publisher failure body are privately retained outside this fixed handoff.
Only authored deductions, URL/byte/hash receipts, selected locators and
genuine actual-run sources/streams are in the lean public packet. This is a
selected-source audit, not a comprehensive current-literature search.

## 1. Geometry and measure conventions

Let P be an actual set, not a multiset of its defining convex pieces. A
hyperplane arrangement of all piece facets partitions it into convex cells;
compatible subdivision gives a finite simplicial complex with union P.
Its full-dimensional simplex indicators sum to 1_P almost everywhere.
This construction allows overlapping original pieces, nonconvexity,
disconnected components, holes, nonsimple corners and added subdivision
vertices. No assumption that P admits a triangulation using only V(P) is
necessary. Candidate lines 12,21,50,60 and 98 pass this scope check.

Null-dimensional pieces are retained in the literal set P and its source
triangulations, but contribute zero ambient d-dimensional mass. Their tangent
indicators are also zero in the a.e. cone algebra. Thus there is no substitution
of atomic or surface measure. V(P) is finite, since it is contained in the
finite vertex set of any one triangulation. Empty P and ambient-null P have
F=0 and reduced denominator 1. The main proof uses d≥1; for d=0 all affine
factors are units and the denominator assertion is immediate.

At v, the translated local tangent C_v(P) is the finite union of the tangent
cones of those convex pieces containing v. A signed indicator identity for
P induces the corresponding tangent identity a.e.: on a sufficiently small
ball the finitely many local polyhedral membership tests are conical. Boundary
exceptions remain null. In particular overlapping original convex pieces
must first be partitioned or treated by inclusion-exclusion; their raw
indicators cannot simply be summed.

A line-cone is invariant under translation in one nonzero direction. Different
summands may have different directions, and the coefficients may be signed.
The condition is not that C_v itself be a line-cone, nor that it can be
partitioned into line-cones. This distinction is essential to the criterion.

## 2. Triangulation-forced versus algebraic vertices

Fix any source triangulation T and a point v absent from its vertex set. For
a simplex S not containing v, its tangent is empty. If v belongs to S, it is
in the relative interior of a face of positive dimension. The tangent is
invariant along every direction parallel to that face, so it is a line-cone
(or ambient-null, hence zero). Summing over full-dimensional simplices shows
1_{C_v(P)} is a finite signed sum of line-cone indicators. Therefore v is not
algebraic. This proves

    A(P) ⊆ Vert(T) for every T, and hence A(P) ⊆ V(P).

The argument works for the source's face-to-face triangulations without
equating them to another author's non-face-to-face dissection convention.
It also proves algebraic vertices cannot arise away from a finite vertex set.
This independently establishes the key inclusion in candidate line 98.
The reverse inclusion is false in general and is not assumed anywhere.

## 3. Complete local signed-cone test

Use the standard a.e. polyhedral Fourier–Laplace valuation, which is additive,
kills line-cones, and for a full-dimensional simplicial cone with independent
generators q_j has rational value

    Φ(K)(u)=(-1)^d |det(q_1,...,q_d)| / ∏_j <q_j,u>.

The sign here is fixed by directly integrating exp(<u,x>) on a convergence
domain, where each one-dimensional integral is -1/<q_j,u>. A global
dimension-dependent sign convention does not change any kernel or vertex
test. The standard valuation extension, rather than an integral over an
arbitrary nonpointed cone, is needed: opposite orthants can have no common
integral convergence domain. ABR's a.e. algebra and Section 4 provide that
framework; Lemma 6 provides exactly its kernel statement.

Here is an independent verification of the decisive geometric kernel step.
Partition C_v a.e. into full-dimensional simplicial cones K_i, or use a signed
cone decomposition. Choose η nonorthogonal to every generator. For independent
q_1,...,q_d, flipping q_1 gives

    [pos(q_1,...,q_d)] + [pos(-q_1,q_2,...,q_d)]
      = [pos(q_1,-q_1,q_2,...,q_d)]  a.e.

The right cone is invariant along q_1. Iterating gives

    [K_i] ≡ ε_i[K_i^+] modulo finite signed line-cones,
    ε_i=∏_j sign<η,q_ij>,   q_ij^+=sign<η,q_ij> q_ij.

Thus g^+=Σ_i ε_i[K_i^+] is congruent to the original tangent indicator.
All its generators lie strictly on the η-positive side. For their common
cone K, finiteness gives c>0 with η·x≥c|x| on K: each generator satisfies
this with one common lower bound, and the triangle inequality preserves it
under nonnegative linear combination. Hence K is pointed and
e^{-η·x}g^+(x) is an L1 function.

On Re u=-η its genuine Laplace integral equals the rational cone valuation.
If the original valuation is zero, the congruence makes Φ(g^+)=0. Evaluating
at -η+it for every real t now gives the zero Fourier transform of the L1
function e^{-η·x}g^+. Fourier uniqueness forces g^+=0 a.e. The finite flip
identities then explicitly express the original tangent indicator as a finite
signed sum of line-cones. Conversely any such sum has zero valuation. Thus

    Φ(C_v(P)) ≠ 0  iff  v∈A(P).

This closes the local geometric test. It uses a convergent integral only after
flipping, so it makes no unjustified common-convergence assumption about the
original cone union. Overlaying the finitely many flipped facet hyperplanes
makes g^+ constant on each full-dimensional chamber. It is nonzero a.e. iff
one such chamber has a nonzero signed count. This is a finite geometric
certificate, not an appeal to a rational-transform calculation or numerical
sampling. Different subdivisions and admissible η give the same verdict
because each is equivalent to the original class modulo line-cones.
Candidate lines 102–121 therefore supply a complete characterization.

## 4. Exact reduced denominator, including nonsimple and nonconvex sets

For a simplex Δ with vertices w_0,...,w_d and barycentric coordinates t_i,
direct integration gives

    ∫_Δ ∏ t_i^{α_i} dx = d!Vol(Δ) ∏α_i!/(d+|α|)!.

Expanding the source's kernel near u=0 and integrating each term gives

    F_Δ(u)=d!Vol(Δ) / ∏_i (1-<w_i,u>).

This can be justified by absolute uniform convergence on a sufficiently small
u-neighborhood, since Δ is compact. Add this identity over the actual
interior-disjoint triangulation. Every denominator divides the squarefree
product over its full finite vertex set W minus 0. Thus the reduced
denominator has no higher multiplicities, no extra irreducible factors and
no homogeneous edge factors. This verifies candidate lines 60–66 without
any simplicity or generic-position hypothesis on P.

The elementary partial-fraction identity for ∏_i(λ-a_i)^{-1}, evaluated at
λ=1 with a_i=<w_i,u>, yields

    F_P(u)=Σ_{w∈W} c_w(u)/(1-<w,u>),
    c_w(u)=(-1)^d Σ_{Δ containing w as a vertex}
             d!Vol(Δ)/∏_{z vertex of Δ, z≠w}<z-w,u>.

It first holds where the projected a_i are distinct, then everywhere as a
rational identity. The coefficient is homogeneous of degree -d. It is exactly
the valuation of the local tangent indicator: simplices with w as a vertex
have the displayed cone, while simplices containing w only on a
positive-dimensional face give a line-cone and zero valuation. The tangent
indicator identity is additive a.e., so artificial vertices and subdivisions
are correctly handled. This checks candidate lines 68–90.

Fix a nonzero v∈W and H_v={u:<v,u>=1}. No homogeneous edge-denominator
hyperplane equals H_v, since the former contains 0 and H_v does not. No other
vertex affine hyperplane equals H_v: their affine equations are normalized
with constant 1, so equality would imply the vertices are equal. At a generic
point of H_v all these other denominators are regular. Multiplying by
L_v=1-<v,u> and restricting the partial fractions to H_v leaves precisely
c_v restricted to H_v. Therefore L_v survives iff that restriction is nonzero.

If a homogeneous rational function c_v vanished identically on H_v, then
for generic u with <v,u>≠0, its value at u/<v,u> is zero and homogeneity
forces its value at u to be zero. It would vanish on a nonempty real open
set and hence identically as a rational function. Thus the restriction is
nonzero exactly when c_v is nonzero. Combined with the complete local cone
test and squarefree divisibility,

    Ω_P(u)=∏_{v∈A(P)\{0}} (1-<v,u>).

The normalization Ω(0)=1 fixes the unit. Real-coordinate degeneracies,
collinear vertices and coincidences among edge hyperplanes do not affect the
argument; only distinct affine vertex hyperplanes are separated, and they
always are. The d=1 hyperplane is a single nonzero point, with the same
scaling argument. Candidate lines 94–98 pass these boundary checks.

Finally A(P)⊆V(P), and distinct nonzero vertex factors are distinct irreducible
linear polynomials. Equality with the product over V(P) is therefore equivalent
to V(P)\{0}⊆A(P). This proves the precise requested iff criterion, not just a
necessary condition or denominator reduction.

## 5. Adversarial geometric controls and limiting cases

The eight executed exact control families supplement the universal proof.
They do not certify a universal theorem by finite examples, nor do they
replay the original 284/6463-check programs.

* **Overlapping pieces.** In R, [1,3]∪[2,4]=[1,4]. Unit union mass is 3;
  summing original interval masses gives 4. Inclusion-exclusion gives the exact
  transform identity F_13+F_24-F_23=F_14, checked by polynomial clearing.
  It removes the artificial interior endpoints 2 and 3. Naive component sums
  would silently change density and the geometric object.
* **Null pieces.** For P=[1,2]∪{4} in R, the isolated point 4 occurs in every
  triangulation, but its tangent is ambient-null and its mass is zero.
  A(P)={1,2}, V(P)={1,2,4}, and Ω=(1-u)(1-2u). The target product includes
  1-4u, so equality fails exactly as the criterion predicts. Replacing {4}
  by {0} makes the extra factor a unit and equality holds. For a pure
  nonzero singleton in R, F=0, Ω=1 and the target equality fails. Thus a.e.
  measure equivalence of P does not require literal equality of its source V.
* **Artificial boundary vertex.** At a subdivided straight square edge,
  the tangent is a halfplane, invariant in the edge direction. Its two
  quadrant coefficients cancel, so it contributes no denominator factor.
  An added interior vertex similarly has whole-space tangent. Such additions
  to one triangulation are not automatically members of source V(P).
* **Holes and reentrant corners.** Let P be the closed frame [0,3]^2 minus
  the open square (1,2)^2. It is a finite union of four closed rectangular
  bars with interior-disjoint subdivision. At inner corner (1,1), the tangent
  indicator is whole-space minus the positive quadrant. Its valuation is
  -1/(u_1u_2), nonzero. It is algebraic and forced in every triangulation.
  The convex hull's vertices miss it; the actual union criterion retains it.
  This also models a reentrant polygon corner and shows why convexity is
  unnecessary.
* **Opposite cones and signed cancellation.** For C=O_+∪O_- in R^d,
  its cone valuation is [(-1)^d+1]/(u_1...u_d). The exact Boolean expansion
  of ∏h_i+∏(1-h_i) has top coefficient 1+(-1)^d. For odd d that coefficient
  vanishes and all remaining monomials omit a coordinate, hence each is a
  line-cone indicator. For even d the valuation is nonzero. Dimensions 2,3,4
  were checked exactly. For d≥2, C itself is not a line-cone: any putative
  invariant nonzero direction can be tested on an interior positive point
  with unequal component ratios, producing mixed signs upon translation.
  Thus merely requiring C not to be a line-cone would give a false result
  already in dimension 3.
* **A bounded realization of that distinction.** The two opposite standard
  d-simplices meeting only at their apex have tangent C. The apex belongs to
  every triangulation for d≥2: a full-dimensional simplex inside their union
  has connected interior contained in one of its two separated interior
  components, and the apex is extreme in that component. Hence no full
  simplex covering the apex neighborhood can avoid using it as a vertex.
  In d=3 this is a genuine nonalgebraic source vertex. When the apex is 0
  its missing factor is a unit; after translation to a nonzero point its
  factor is genuinely missing. This verifies the necessity of the origin
  exception in candidate lines 125–146.
* **Skew flip.** For generators (1,1),(-1,2) and η=(1,0), flipping the second
  generator changes the cone valuation's sign and gives a line-cone identity
  invariant along (-1,2). All four facet-coordinate sign chambers were
  checked exactly; they exhaust the full-dimensional cells, rather than
  sampling arbitrary Euclidean points.
* **Admissible η and affine-factor normalization.** A zero dot product with
  a generator is rejected. Collinear distinct vertices still give distinct
  factors 1-u and 1-2u; the origin gives 1. The general conclusions are
  proved above, with these computations acting only as assumption controls.

No control provides a counterexample to the candidate. They do falsify
stronger shortcuts: convex-hull-only vertices, unsigned partition criteria,
non-line-cone-only criteria, naive overlap summation, and omission of the
literal origin exception.

## Evidence accounting, custody limits and conclusion

Primary acquisition was owned child PID 22956 of collector 22948,
15:10:16.419597–15:10:22.078039 UTC, exit 0. Eleven owned Poppler children
all exited 0. Three full primary PDFs were acquired; the separate publisher
PDF attempt failed with 403 and its 832806-byte response is privately retained.
Crossref acquisition succeeded. Complete primary-run stdout was 4121 bytes,
stderr empty. Exact controls were owned child 25257 of collector 25249,
15:13:35.296884–15:13:35.331265 UTC, exit 0, stdout 3015 bytes, stderr empty.
Prelaunch operator/collector sources, actual PID/UTC/argv, complete streams
and byte hashes are preserved. No mathematical-control run failed; the
publisher access failure is separately qualified rather than called success.

The source preparer records 17 original science files and 18 changed files.
Its actual merge base is 60292bed09f59236aa192cb17aa138f7b4750e1a,
distinct from GitHub's reported c6975ca76f9f667f1250ba403d0e6da2aafe14d0.
This family binds that preparer evidence; it did not authenticate Git itself
and does not infer ROOT custody, native acceptance or publication authority.
Current measured full modes are recorded separately from historical Git
100644/source-read mode observations. Later freezing is a filesystem-mode
change, not a scientific-body change.

Original turns.jsonl is genuinely empty. The original disposition is
already_solved 0/5, with no substantive new proof-attempt turn; this audit adds
zero. The preparer's raw prior report key is ABSENT, SQL report is non-NULL
TEXT "{}", and the archived wrapper's research_result_for_code field is
present with literal null. These are separate typed facts. This family directly
checks the wrapper/empty turn file and binds the preparer's raw/SQL account,
without copying or rereading the giant corpora. Native queued 0/5 at the
preparer's dated selection is not the original draft's status and is not
mutated here.

High confidence: the full denominator formula and exact iff geometric
characterization follow universally in the stated measure/triangulation
scope. No remaining mathematical gap was found. Published-version access is
qualified above, and the review remains AI-authored/unrefereed. ROOT custody,
human review and downstream acceptance are separate pending actions.
No external individual, native, branch/index, remote/ref, paper, DOI or
publication action occurred. No discovery or novelty credit is claimed.
