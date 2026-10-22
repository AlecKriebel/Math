# Independent acceptance of the metric threshold counterexample

13 October 2026. Problem 30003527 / OWR-15575-006, queue row 1767. Independent audit within shared substantive pass 3. This audit is not an additional research pass.

## Verdict and scope

**Accepted.** The frozen report proves both of the following construction obstructions for the bounded globally Lipschitz vertical-slowing flow determined by a compact stationary set.

1. For every prescribed radius r>0, some movable stationary compactum C has nonmovable maximal invariant metric fill M_r(C).
2. A single movable stationary compactum C_∞ has nonmovable M_(r_n)(C_∞) for a sequence r_n decreasing to zero.

The exact distance and metric-fill formulas for the original stretched-book compactum also pass the audit. No mathematical correction to the frozen construction is required. This report supplies explicit uniform separation bounds, separating tail radii, and the full quantifiers for the clopen-subcompactum argument.

Two minor wording clarifications do not affect the proof. The opening phrase “compact planar graphs” means graphs of continuous functions over compact subsets of the plane. It does not mean finite graphs in the graph-theoretic sense, or that the displayed graphs themselves lie in affine planes. “Two disjoint compact graphs over planar compacta” would be unambiguous. In the scaled-copy section, the assertion that every bounded orbit belongs to one copy's vertical hull means every bounded nonstationary orbit; the stationary singleton at 0 is the explicitly included exception. The formulas and proof already handle it correctly.

**The invariant movable enlargement question remains unresolved.** The new stationary sets C and C_∞ are themselves movable, so choosing B=C or B=C_∞ satisfies their own enlargement instances in every neighborhood. This conclusion does not apply to the original nonmovable stretched-book A. The report neither obstructs every invariant enlargement nor proves or refutes the existence of arbitrarily small good metric radii for every compact stationary set.

## Frozen artifacts and inherited input

The following authored files were read in full:

- METRIC_THRESHOLD_COUNTEREXAMPLE.md: 12,733 bytes; SHA-256 602b36eff65bd1fa9ea966ecfffeb1a26853b8cbbd40315528616b1b210aafa1.
- VERTICAL_GAP_COUNTEREXAMPLE.md: 11,970 bytes; SHA-256 85ab6a5e1b948ebc8f83f6506cb04a1d9e8fa644826261fcc40247567b695403.
- VERTICAL_GAP_ACCEPTANCE.md: 14,943 bytes; SHA-256 ef81f2296048ec77a5b8175bb838cd66c6cb6b5d61482f210e14ec04df26d1c8.

The imported topological input is the accepted nonmovable compactum

A = (P₀×{0}) ∪ (P₁×{1}) ∪ (S×[0,1]),

where P₀,P₁ are compact planar sets and S is a nonempty compact subset of P₀∩P₁. The pass-2 proof obtains it from a dyadic solenoid K embedded in an arc times a triod and proves nonmovability by explicit near-homeomorphisms and neighborhood homotopies. The accepted argument fixes its domain neighborhood before the arbitrary target neighborhood; it does not need a general cell-like-map assertion.

The displayed definitions of P₀,P₁,S in the frozen metric report reproduce that same A. In particular, each binding point contributes both endpoints and the full column. If S were empty, connectedness of K would put K in one component of the three-page book with its common edge removed. Each such component lies in a single planar page. Planar movability would contradict nonmovability of K. Thus the use of dist(p,S) is legitimate.

Bing's Theorem 8 and its proof on printed pp.121–122 were re-inspected in the existing primary-source page images. Borsuk's neighborhood-homotopy definition, shape invariance, and planar movability were rechecked in existing primary-source text and page images. The existing primary PDFs were hash-verified. These checks reuse the accepted source collection and introduce no additional literature-search pass.

## Full flow and the metric invariant part

For nonempty compact C, the function dist(·,C) is 1-Lipschitz. Taking its minimum with 1 preserves that property. Consequently

F_C(p,z) = min(1,dist((p,z),C))e₃

is globally Lipschitz and bounded. Existence and uniqueness therefore give a continuous full flow for all real times. Its stationary set is exactly C, and each horizontal coordinate p is constant along an orbit.

Within an open complementary interval of C_p, the scalar velocity is strictly positive. A nonstationary orbit cannot have a finite limiting height in the interior of that interval, since the velocity would then remain bounded below by a positive number nearby. It cannot reach a finite endpoint in finite time, since the endpoint is a stationary solution and uniqueness would fail. Thus the orbit image is the whole open complementary interval. An unbounded interval gives a full orbit unbounded in at least one time direction.

Let N_r(C) be the closed Euclidean r-neighborhood. It is compact, and

M_r(C) = ⋂_(t∈R) φ_C(t,·)⁻¹(N_r(C)).

The t=0 term ensures that this is a closed subset of N_r(C). The group law makes it invariant under all real time maps. The orbit classification proves that it consists exactly of C together with the bounded complementary fiber intervals whose entire closed segments are in N_r(C). Using closed segments causes no mismatch, because their endpoints already belong to C and N_r(C) is closed.

This verifies full invariance rather than merely forward invariance. Compactness of C also gives M_r(C)⊂U for every open U⊃C and all sufficiently small r. None of these general facts implies movability.

## The prescribed radius construction

Fix r>0 and put g(p)=r+dist(p,S). The sets

C⁻ = {(p,−g(p)):p∈P₀},
C⁺ = {(p, g(p)):p∈P₁}

are compact and homeomorphic to P₀,P₁ respectively. One can also flatten each graph by an ambient shear. Planar movability and homeomorphism invariance imply their movability. The two graphs are separated by the open slab −r<z<r. Finite disjoint unions preserve movability: for a given outer neighborhood, choose disjoint outer neighborhoods of the two compact pieces, choose each piece's movability neighborhood, and combine the homotopies on those disjoint domains. No theorem about arbitrary finite gluing is being used.

A bounded gap exists precisely over p∈P₀∩P₁, with endpoints ±g(p). For p∈S those endpoints are ±r; every point between them is within r of an endpoint. The whole gap is therefore selected by M_r(C).

For p∉S, every graph point (q,±g(q)) satisfies

|(p,0)−(q,±g(q))|² = |p−q|²+g(q)² ≥ r².

Equality would require both p=q and g(q)=r, hence p∈S. Compactness of C ensures that the distance minimum is attained, so the absence of equality gives the strict inequality dist((p,0),C)>r. This is the required strict exclusion; pointwise strict inequalities alone, without attainment, would not suffice. The orbit classification now gives exactly

M_r(C) = C ∪ (S×[−r,r]).

The map H(p,z)=(p,(z+g(p))/(2g(p))) is an ambient homeomorphism, with inverse H⁻¹(p,t)=(p,2g(p)t−g(p)). Continuity and invertibility hold globally because g≥r>0. It carries the two graphs to the two endpoint pieces of A and the selected columns to S×[0,1]. Thus H(M_r(C))=A, proving nonmovability.

For 0<s<r, every bounded gap has a midpoint at distance at least r, including the gaps over S. Therefore M_s(C)=C. This also verifies the claimed failure of monotonic preservation of movability as the radius increases. No uniqueness of the bad radius is claimed or needed.

## The scaled copies and their separation

Let C₀ be the construction for r=1, with full vertical hull V₀. In the displayed coordinate normalization, every horizontal base has norm at most √2, and its distance from the nonempty binding set S is at most √2. Heights in V₀ satisfy |z|≤1+√2. Consequently V₀ is contained even in a ball of radius √(5+2√2)<3, so the report's radius-4 bound is valid.

Write d_n=2⁻ⁿ, c_n=(d_n,0,0), and a_n=2⁻⁴ⁿ⁻¹⁰. Then C_n=c_n+a_n C₀ and its full vertical hull V_n=c_n+a_n V₀ are contained in the closed ball of radius 4a_n about c_n. The union C_∞={0}∪⋃_n C_n is compact: a sequence either has a subsequence in one of finitely many compact copies or has copy indices tending to infinity and converges to 0.

For k≥1,

a_k ≤ d_k/8192.

If m≠n and k=min(m,n), then |c_m−c_n|≥d_k/2 and 4a_m+4a_n≤8a_k. Hence the distance between the two corresponding radius-4 balls is at least

d_k/2−8a_k ≥ (511/1024)d_k ≥ (511/1024)d_n > a_n.

Also the distance from V_n to 0 is at least

d_n−4a_n ≥ (2047/2048)d_n > a_n.

These estimates prove the claimed uniform inequality

dist(V_n,C_∞\C_n)>a_n

for each fixed n. They hold equally for horizontal projection disks, since their centers have the same separation and their radii have the same upper bounds. The disks are disjoint and avoid the origin. Thus a vertical fiber meets at most one copy, or consists solely of the stationary point 0 on the origin fiber. No bounded gap can bridge different copies. Every bounded nonstationary orbit belongs to one V_n.

For x∈V_n, the preceding strict bound shows

dist(x,C_∞)≤a_n if and only if dist(x,C_n)≤a_n.

The exact full-gap selection within this block is therefore the isolated-copy selection. Euclidean distance scales by a_n, so

M_(a_n)(C_∞)∩V_n = c_n+a_n M₁(C₀).

A conjugacy with the same time parameter is neither asserted nor required; the orbit classification and metric scaling prove this equality directly.

## The nonmovable block is clopen

An explicit isolating cylinder is the product of the open horizontal disk of radius 5a_n centered at (d_n,0) with the vertical line R. It contains all of V_n. The strict separation bound above excludes every other V_m and the origin from that cylinder. Since M_(a_n)(C_∞) lies in {0}∪⋃_m V_m, intersecting it with the cylinder gives precisely c_n+a_n M₁(C₀). This block is relatively open, and it is relatively closed because it is compact.

Here is the full neighborhood argument that a clopen subcompactum D of a movable compactum X is movable. The empty-complement case is immediate. Otherwise put E=X\D, and fix any open O_D⊃D. Compactness and disjointness permit disjoint open O₁,O₂ with D⊂O₁⊂O_D and E⊂O₂. Apply movability of X in O₁∪O₂ to choose a fixed neighborhood V⊂O₁∪O₂. Set V_D=V∩O₁.

For any later open target W_D⊃D, use movability of X with the target (W_D∩O₁)∪O₂. For x∈V_D, the homotopy path begins in O₁ and stays in O₁∪O₂. Its connected image cannot switch between the disjoint relatively clopen parts O₁ and O₂. The restricted homotopy therefore stays in O₁⊂O_D and ends in W_D. The domain V_D was chosen before W_D, exactly as required.

The isolated block is homeomorphic to the accepted nonmovable A. Therefore M_(a_n)(C_∞) cannot be movable for any n.

## Movability of the original disconnected compactum

The tail argument is valid with a neighborhood fixed independently of every subsequent target. Explicit separating radii can be chosen as

t_N=(3/2)2⁻ᴺ, for N≥2.

For n≥N, the whole copy C_n has norm at most (2049/2048)d_n≤(2049/2048)d_N<t_N. For n<N, every point of C_n has norm at least (2047/2048)d_n≥(2047/1024)d_N>t_N. Thus the closed ball of radius t_N separates the entire tail from the finite head, and t_N tends to zero.

Given open O⊃C_∞, take N large enough that the closed ball of radius t_N is contained in O. Choose pairwise disjoint open O_n around C_n, n<N, inside O and outside that closed ball. Their existence follows from the positive separation of the finitely many compact sets. Each C_n is movable, so choose its movability neighborhood U_n⊂O_n. The fixed open neighborhood

V=B(0,t_N) ∪ ⋃_(n<N) U_n

contains all of C_∞. For any target W⊃C_∞, contract the ball linearly to 0, entirely within O. Its endpoint lies in W because 0∈C_∞. On U_n use movability with target W∩O_n and outer neighborhood O_n. These finitely many disjoint open domains carry continuous homotopies that combine into one continuous homotopy of V in O, ending in W.

The definition of movability does not require the stationary compactum to remain pointwise fixed during this neighborhood homotopy. Thus contracting the ball, including its tail copies, is permitted. This proves movability of C_∞ without a countable-union assertion. The flow fixes C_∞ pointwise, while r_n=a_n decreases to zero and each M_(r_n)(C_∞) is nonmovable.

## Exact distance formula for the original stretched book

For p∈P₀∩P₁ and 0≤z≤1, the distance from (p,z) to P₀×{0} is exactly z and its distance to P₁×{1} is exactly 1−z, because the point with the same base p is present in each endpoint piece. Its distance to S×[0,1] is exactly dist(p,S), since height z is available in every binding column. Therefore

dist((p,z),A)=min(z,1−z,dist(p,S)).

The maximum in z is min(1/2,dist(p,S)); it is attained at z=1/2. Bounded gaps outside the binding are the unit gaps over P₀∩P₁. The full-gap rule consequently yields, for 0<r<1/2,

M_r(A)=A ∪ ((P₀∩P₁∩N_r^(2)(S))×[0,1]),

with the planar neighborhood closed, including the equality case dist(p,S)=r. At r≥1/2 all remaining unit gaps are selected. The equations are geometric identities and imply no unproved assertion about movability of small fills of this A.

## Sources and final verification

- R. H. Bing, *Embedding Circle-Like Continua in the Plane*, Canadian Journal of Mathematics 14 (1962), 113–128, Theorem 8, printed pp.121–122. [DOI](https://doi.org/10.4153/CJM-1962-009-3). Existing primary PDF: 1,695,552 bytes; SHA-256 694b7217d647f0731926a034e0189815048a2ed82ae4c7f39721fd56565058ac. The theorem and its complete short proof were re-inspected in the existing page images.
- K. Borsuk, *On movable compacta*, Fundamenta Mathematicae 66 (1969/1970), 137–146. [DOI](https://doi.org/10.4064/fm-66-1-137-146). Existing primary PDF: 1,353,266 bytes; SHA-256 9ec781740ccb5c5c66bd7a1ac9a712f1e3246c48cea9e01a407ba8fb0fcf94d1. The definition on p.137, Corollary (3.11) on p.142, and Corollary (5.5) on p.145 were rechecked in the existing primary text and rendered images. The solenoid argument was also read in the existing primary text and the accepted authored audit.

The new midpoint threshold test, ambient homeomorphism, full-flow classification, uniform scaled-copy bounds, clopen inheritance, fixed-neighborhood tail contraction, and exact metric formula were independently checked. The original files and primary PDFs remain unchanged. No remote mutation, fresh source retrieval, source-body publication, or external outreach was performed.

The accepted outcome is a counterexample to arbitrary-radius and eventual uniform small-radius movability of this metric-fill construction. It leaves the existential good-radius statement and the full invariant movable enlargement problem open.
