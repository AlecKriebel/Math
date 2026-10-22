# Independent acceptance: isolated-flow structural results

Date: 13 October 2026 UTC. Target: row 1767 / 30003527 / OWR-15575-006.

This is verification within substantive pass 1, not a new proof-search pass. The satellite-circle construction and its separate acceptance are outside this audit.

## Verdict

**Accepted, with the source dependencies and scope limits below.** The authored arguments establish:

1. An isolated invariant compactum of a continuous full flow on R³ has free integral first Čech cohomology. The argument imposes no finite-rank hypothesis and proves no uniform rank bound.
2. If its Čech H⁰ and H¹ over F₂ are finite-dimensional, it is movable in the exact ambient neighborhood-homotopy sense. The permissible enlargement is the set itself.
3. The all-enlargements retraction obstruction, uniform trapping sufficiency criterion, and compatible-core-circle sufficiency criterion have the stated quantifiers.

No substantive gap was found in these deductions. They do not establish an infinite-rank isolated realization, movability of every isolated invariant compactum, or the unrestricted invariant-enlargement result. The empty invariant set should be disposed of directly rather than passed through a theorem whose connected-block proof uses nonemptiness.

## 1. Primary-source dependencies

I independently inspected [Sánchez-Gabites, arXiv:2403.18805v1](https://arxiv.org/html/2403.18805v1), including the relevant statements and surrounding arguments. Its setting includes continuous flows and orientable boundaryless 3-manifolds. Definition 6 gives tame manifold blocks with compact entry/exit surfaces; closed entry sets provide the continuous entry-time hypothesis of Proposition 5. That proposition's relative-cohomology identification is obtained through flow homotopies, continuity, and compact-pair constructions, so the same proof works over Z and F₂. Section 5.4 supplies a block basis without a finite-cohomology assumption. Theorem 10 assumes a connected block and finite generation in degrees 0 and 1; Theorem 16 gives the product-collar complement of a regular block.

These are imported results, not consequences inferred from a bare cohomology isomorphism. I have not re-proved all classical results underlying the source's block-existence and tameness arguments. I did not independently recheck the historical 2016 abstract attribution, which is not needed for correctness here. No primary-source body is included in this report.

## 2. Surface algebra and coefficient bridge

For compact L in a finite union S of closed orientable surfaces, Alexander–Lefschetz duality and the relative homology sequence give

H₁(S;G) → Čech H¹(L;G) → H₀(S\L;G) → H₀(S;G).

The first term may equivalently be written H¹(S;G), using orientation and Poincaré duality. Thus the two presentations in the audited files are compatible. Compact subsets meeting the boundary of an entry surface cause no difficulty: place that surface in its double, or simply use the closed ambient boundary surface ∂N.

Finite-dimensional Čech H⁰(L;F₂) implies finitely many connected components. In a compact Hausdorff space, distinct components can be separated by clopen partitions; arbitrarily many components would give arbitrarily many independent characteristic functions. Once their number is finite, the components are clopen and Čech H⁰(L;Z) is finite free.

The displayed sequence over F₂ shows that H₀(S\L;F₂) is finite-dimensional whenever Čech H¹(L;F₂) is. The complement is an open surface, so its connected and path components coincide. Consequently H₀(S\L;Z) is finite free. The sequence over Z then proves finite generation of Čech H¹(L;Z). This remains valid for L=∅, L=S, empty complementary components, and disconnected S.

For the isolated-set bridge, the degree bookkeeping is correct:

- H⁰(K;F₂) controls H¹(N,K;F₂), using finite-type N.
- H¹(K;F₂) controls H²(N,K;F₂).
- Proposition 5(iii) transfers these relative groups to (P,L)=(Nⁱ,n⁺).
- The pair sequence transfers finiteness to H⁰(L;F₂) and H¹(L;F₂).
- The surface bridge changes coefficients for those two groups.
- The integral pair sequence gives finite generation of H¹(P,L;Z) and H²(P,L;Z).
- Transfer back to (N,K), then use its pair sequence to obtain H⁰(K;Z) and H¹(K;Z).

Every finite-generation step uses subgroups, quotients, or extensions of finitely generated abelian groups. No H²(K;F₂) hypothesis is required. No universal-coefficient assertion for arbitrary compacta is being substituted for the surface argument.

A compact manifold has only finitely many components. For a block N, the invariant pieces K∩N_a form a finite clopen partition of K. Full trajectories staying in N cannot switch its components. Each nonempty piece therefore has connected block N_a and inherits finite generation as a direct summand. Applying Theorem 10 separately and taking the finite union is legitimate. Beginning with N inside a prescribed open O gives arbitrarily small regular blocks. This does not require K itself to be connected.

## 3. Freeness without a finite-rank assumption

First, Čech H¹(X;Z) is torsion-free for every compact metric X. Use a finite-polyhedral expansion: ordinary H¹ at each stage is torsion-free by the universal coefficient theorem, and filtered direct limits preserve torsion-freeness. Explicitly, if a multiple of a represented element dies in the limit, it dies at a later stage; torsion-freeness there makes the element itself die. Injective bonding maps are unnecessary.

For L⊂S as above, the image of H₁(S;Z) in Čech H¹(L;Z) is finitely generated and torsion-free, hence free. Its quotient in Čech H¹(L;Z) embeds in the free group H₀(S\L;Z), so is free. The extension splits. Thus Čech H¹(L;Z) is free, even with infinitely many complementary components.

If F is free and J is finitely generated, J is contained in a finite-rank direct summand of F. The structure theorem in that summand proves F/J is free plus finite torsion. Every subgroup of such a group is again free plus finite torsion: project to the free factor and split over the free image. These claims hold for infinite-rank F; they do not mistake arbitrary torsion-free groups for free groups.

Now H²(P;Z) is finite free because P is a compact orientable surface. From

H¹(P) → H¹(L) → H²(P,L) → H²(P)

the quotient of H¹(L) by the preceding image is free plus finite torsion, and the remaining image in H²(P) is free. Splitting shows H²(P,L), and hence H²(N,K), is free plus finite torsion.

Finally let C be the image of H¹(N) in H¹(K), and D the image of H¹(K) in H²(N,K). Then C is finite free, D=F⊕T with F free and T finite, and

0 → C → H¹(K) → F⊕T → 0.

Lifting a basis splits off F. The preimage of T is finitely generated, since it is an extension of the finite group T by finitely generated C. It is also torsion-free, being a subgroup of H¹(K), and hence finite free. This proves the asserted freeness. None of these steps needs finite Čech H⁰(K) or H¹(K).

For a genuine generalized solenoid with infinitely many nontrivial covering degrees, H¹ is rank-one noncyclic and therefore not free. Isolation is excluded. A retraction from an isolated invariant compactum onto such a solenoid is also excluded, because its induced H¹ injection would realize this nonfree group as a subgroup of a free group. These conclusions concern isolation or retractions; they say nothing by themselves about other invariant enlargements.

## 4. Collar homotopy and exact movability

Write h:Q\K→∂Q×[0,∞) for the imported spine homeomorphism. The tails

Q_r = K ∪ h⁻¹(∂Q×[r,∞))

are compact: their complements are relatively open in Q. They are neighborhoods of K because h⁻¹(∂Q×[0,r]) is compact and disjoint from K. They are cofinal: for any open W⊃K, the compact set Q\W has bounded h-coordinate.

The authored piecewise function f_t is continuous at s=r+1, since both formulas there equal r+1. It equals s at t=0, is nonnegative, has f₁(s)≥r, and fixes every s≥r+1 for every t. The resulting F_t on Q\K therefore extends jointly continuously by the identity on K: it is already the identity on a single neighborhood Q_{r+1} throughout the homotopy.

Choose Q⊂O first and put V=int Q. This V is an ambient open neighborhood of K, contained in O, and is independent of W. Only afterward choose r for W. The homotopy stays in Q⊂O and ends in Q_r⊂W. It need not follow the flow. Thus the exact order “for every O, some V, for every W, some H” is satisfied.

For K=∅, take V=∅ and the empty homotopy, under the usual neighborhood convention. This avoids any unnecessary invocation of connected nonempty block machinery. Empty entry surfaces are harmless in the pair sequences. When the finite-dimensional H⁰ group is zero, K is empty; zero H¹ poses no special problem.

## 5. Other structural criteria

### Retractions and all allowed enlargements

The coordinatewise extension of r:B→A to R³ exists by the Tietze theorem. Given O⊃A, choose P⊃B with r̃(P)⊂O, and obtain Q from movability of B. There is a fixed open V⊃A in Q on which every segment from x to r̃(x) lies in O, because r̃ fixes A and A is compact. This V is chosen before the target neighborhood T.

For T⊃A, use a neighborhood W⊃B contained in r̃⁻¹(T). Compose the movable homotopy in P with r̃, and prepend the segment homotopy on V. Its endpoint lies in T. This proves retract preservation with the required quantifiers.

If A is a nonmovable retract of M=Inv(N) and A⊂int N, every compact invariant B between A and int N lies in M; the retraction restricts to B. This excludes every allowed movable B, including disconnected ones and B=A. It is a sufficient counterexample criterion, not a realized counterexample.

### Trapping criterion

The stated property supplies V for O before choosing W, and then a uniform T for all x∈cl V. The map H(x,s)=φ(sT,x) has the required initial value, range in O, and endpoint in W. Take T≥0. Uniform attraction is essential; neither invariance nor one-sided stability alone supplies it.

### Compatible cores

For the nested-torus construction, compactness of the decreasing intersection makes the T_j cofinal at A. Choose j from O and k>j. Every early core D_m,…,D_{k−1} is compact and disjoint from T_k; pairwise disjoint tubular neighborhoods avoiding T_k exist. The finite union of those tubes with int T_k is an open neighborhood of B inside O.

The core hypothesis provides a homotopy of T_j to D_j. Restrict it to int T_k, and use tube retractions on the other, disjoint domains. These finitely many domain pieces are clopen in their union, so the assembled homotopy is continuous. Its image stays in O and its endpoint lies in B itself. Thus it works for every W⊃B without changing V. Hausdorff convergence supplies compactness of B but is not being used as a substitute for the core homotopy.

The elementary maximal-invariant-core compactness and finite-time nested-intersection facts are also correct. They yield no movable homotopy by themselves. Likewise, making a wild set stationary does not exclude invariant finite-polyhedral enlargements when the flow is stationary on a neighborhood.

## 6. Acceptance boundary

This report verifies the authored deductions conditional on the explicitly imported primary theorems. It does not independently establish any additional realization theorem, component-sensitive obstruction beyond these arguments, historical priority claim, or satellite-source correction. “Free, with rank possibly infinite” records the absence of a rank restriction in the proof; it is not evidence that the proposed infinite-rank candidate is dynamically realizable.

The unrestricted target must remain partial/unresolved on the strength of these results alone.
