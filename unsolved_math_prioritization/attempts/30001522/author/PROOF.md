# A fixed Wu-manifold witness for the free-rank question

Problem 30001522 / OWR-4413-005. Author-prepared proof, 6 October 2026.
This note uses classical facts and claims no priority for the example.

## 1. Target and answer

Here rk_T(X) means the largest rank of a torus acting **freely and continuously on X itself**, and rk_p(X) means the largest rank of an elementary abelian p-group acting freely and continuously on X itself. The question in Bernhard Hanke's contribution to Oberwolfach Report 32/2010, printed p. 1912 [1], asks whether a fixed finite connected complex with abelian fundamental group, trivial fundamental-group action on higher homotopy, and finite-dimensional total rational homotopy can satisfy rk_p(X) > rk_T(X) for infinitely many primes.

**Theorem.** Let W = SU(3)/SO(3), with SO(3) embedded as the real orthogonal matrices. This single compact smooth five-manifold is a finite connected complex satisfying all those homotopy hypotheses. It has

\[
\operatorname{rk}_T(W)=\operatorname{rk}_2(W)=0,
\qquad
\operatorname{rk}_p(W)=1\quad\text{for every odd prime }p.
\]

In fact, W admits a free smooth cyclic action of every odd order. The strict inequality therefore holds for every odd prime. No asymptotic extrapolation from computations is involved.

The proof separates an explicit odd-order construction from a topological obstruction to a free involution. That obstruction excludes every free torus action, not merely homogeneous, isometric, smooth, or locally linear ones.

## 2. The space and its homotopy hypotheses

The closed subgroup SO(3) of SU(3) gives a smooth principal bundle

\[
SO(3)\longrightarrow SU(3)\longrightarrow W.
\]

Thus W is closed, connected and smooth, of dimension 8 - 3 = 5. A compact smooth manifold admits a finite triangulation; choose one once and for all. This realizes W itself as a finite complex, rather than replacing it by some other space of finite homotopy type.

The homotopy exact sequence, using pi_1(SU(3)) = pi_2(SU(3)) = 0 and pi_1(SO(3)) = Z/2, gives

\[
\pi_1(W)=0,\qquad \pi_2(W)=\mathbb Z/2.
\]

These facts are also recorded, with their proof, in [2, Lemma 4.41]. In particular, the fundamental-group hypotheses hold, and H_2(W;Z) = Z/2 by Hurewicz.

For completeness, finite-dimensional total rational homotopy follows directly from the same fibration: SU(3) has rational homotopy Q in degrees 3 and 5 only, while SO(3) has rational homotopy Q in degree 3 only. These are the usual rational homotopy computations for compact Lie groups. Rationalizing the homotopy exact sequence shows that W can have rational homotopy only in degrees 3, 4 and 5, with finite dimensions in each. This suffices for the question.

One can sharpen this to W_Q equivalent to S^5_Q. Indeed, W is orientable because it is simply connected. Integral Poincare duality and the universal coefficient theorem give its integral homology, in degrees 0 through 5, as

\[
(\mathbb Z,0,\mathbb Z/2,0,0,\mathbb Z).
\]

For example, H_4 = H^1 = 0 and H_3 = H^2 = 0. Hence W is a simply connected rational homology five-sphere. Rational Hurewicz followed by rational Whitehead identifies its rational homotopy type with that of S^5. Equivalently, a map S^5 to W representing a nonzero rational Hurewicz class is a rational homology equivalence, hence a rational homotopy equivalence between simply connected spaces. Thus pi_5(W) tensor Q = Q and the other positive-degree rational homotopy groups vanish. In particular, chi^pi(W) = -1.

## 3. An explicit free action for every odd order

For z in S^1 define

\[
D(z)=\operatorname{diag}(z,z,z^{-2})\in SU(3),
\qquad z\cdot[g]=[D(z)g].
\]

This is a well-defined smooth action on right cosets. If z fixes [g], then g^{-1}D(z)g belongs to SO(3). Every real orthogonal 3-by-3 matrix of determinant 1 has eigenvalue 1: nonreal eigenvalues occur in conjugate pairs, and the determinant forces the unpaired real eigenvalue to be 1. Consequently, D(z) can fix a coset only if z = 1 or z^{-2} = 1. Thus every stabilizer is contained in {1,-1}.

Let n be any odd positive integer and let C_n be the n-th roots of unity in this fixed circle. Its intersection with {1,-1} is {1}. Restricting the displayed action gives a free C_n action on W. In particular rk_p(W) >= 1 for every odd prime p.

This construction does not assert that the circle action is free. It is not: D(-1) = diag(-1,-1,1) is in SO(3), so -1 fixes the identity coset. The classical orbifold calculation [3, Proposition 4.2], specialized to weights (1,1,-2), provides compatible published context for these stabilizers, but the eigenvalue argument above proves all the freeness needed here independently.

## 4. No free topological involution

We first record a general covering obstruction.

**Lemma.** If a closed topological d-manifold M has a nonzero Stiefel-Whitney number, then M admits no free continuous action by a group of order two.

**Proof.** Suppose an involution acts freely. Its orbit map q:M -> N is an ordinary two-sheeted covering. Indeed, a small neighborhood of each point can be chosen disjoint from its translate. Therefore N is a closed topological d-manifold and q is a local homeomorphism. No smoothness or local-linearity assumption on the involution is required.

The topological tangent microbundle is natural under local homeomorphisms, so tau_M is isomorphic to q^*(tau_N). This can also be seen directly from the diagonal definition of the tangent microbundle: near the diagonal the map (x,y) -> (x,q(y)) identifies M x M with the pullback of a neighborhood of the diagonal in N x N. The Thom definition of Stiefel-Whitney classes, by Steenrod squares of the mod-2 Thom class, is natural under this identification. It agrees with ordinary tangent-bundle classes when a smooth structure is available. Hence w_i(M) = q^*w_i(N).

Writing all fundamental classes with F_2 coefficients, q_*[M] = 2[N] = 0. For any partition i_1 + ... + i_k = d, naturality of the cohomology-homology pairing gives

\[
\langle w_{i_1}(M)\cdots w_{i_k}(M),[M]\rangle
=\langle w_{i_1}(N)\cdots w_{i_k}(N),q_*[M]\rangle=0.
\]

This contradicts a nonzero Stiefel-Whitney number. QED.

For the Wu manifold, the classical computation is

\[
H^*(W;\mathbb F_2)=\mathbb F_2[x,y]/(x^2,y^2),
\quad |x|=2,\ |y|=3,\qquad w(W)=1+x+y.
\]

See [2, Corollary 4.44 and Proposition 4.45], which credit Barden, Landweber-Stong and Calabi for the classical ingredients. Since xy generates H^5(W;F_2),

\[
\langle w_2(W)w_3(W),[W]\rangle=\langle xy,[W]\rangle=1.
\]

The lemma proves that W has no free continuous involution. Therefore rk_2(W)=0. Every positive-dimensional torus contains an involution, and restricting a free action to a subgroup preserves freeness. Thus rk_T(W)=0.

This argument deliberately uses the quotient by a finite group. It does not assume that an arbitrary free topological circle action on a manifold has a manifold orbit space. It also does not substitute a theorem about isometric circle actions for one about all continuous actions.

## 5. Optional sharpening: the exact odd-primary rank

Sections 2-4 already answer the question affirmatively. Here is a standard cohomological argument for the asserted equality rk_p(W)=1, independent of a large-prime threshold.

For odd p, the homology calculation in Section 2 and the universal coefficient theorem show that W is an F_p-homology five-sphere. Suppose E=(Z/p)^2 acted freely and continuously. The action on H^*(W;F_p) is trivial: the only nonzero degrees are 0 and 5, and a p-group has no nontrivial homomorphism to F_p^*, whose order is p-1.

The Borel fibration W -> W_E -> BE has multiplicative cohomological Serre spectral sequence

\[
E_2^{i,j}=H^i(BE;\mathbb F_p)\otimes H^j(W;\mathbb F_p),
\quad H^*(BE;\mathbb F_p)=R=\mathbb F_p[t_1,t_2]\otimes\Lambda(s_1,s_2),
\]

with degrees |t_i|=2 and |s_i|=1. There are only two rows, j=0 and j=5. The sole possible nonzero differential is d_6, and multiplicativity makes its image in the bottom row the principal ideal (f), where f=d_6(u) has degree 6 and u generates H^5(W;F_p). Consequently E_infinity^{*,0}=R/(f).

Set s_1=s_2=0. This gives a graded surjection

\[
R/(f)\longrightarrow\mathbb F_p[t_1,t_2]/(\bar f).
\]

The target is infinite-dimensional. If bar f is zero this is immediate. Otherwise bar f is a homogeneous polynomial of ordinary degree 3. In polynomial degree m >= 3 the quotient dimension equals (m+1)-(m-2)=3, because multiplication by a nonzero polynomial is injective in a polynomial ring over a field. Thus the bottom spectral-sequence row survives in arbitrarily large degrees.

Freeness identifies W_E up to homotopy with W/E. The latter is a closed topological five-manifold by the same local covering argument used above, so its cohomology vanishes above dimension 5. This is a contradiction. It follows that no rank-two elementary abelian p-group acts freely. A free higher-rank action would restrict to rank two, so rk_p(W)<=1. Combined with Section 3, this proves equality for every odd prime.

## 6. Scope and the integral obstruction

The witness W is fixed once, and only the finite subgroup varies with p. Its smooth actions are genuine free actions on that fixed finite complex. The nonexistence assertion covers every continuous free torus action.

The finite-prime support of torsion is compatible with the persistent gap. The obstruction here lives at the single prime 2. A torus contains 2-torsion and therefore cannot act freely, while its odd-order subgroups avoid the stabilizers of the explicit almost-free circle action. Discarding finitely many torsion primes in a rational or large-prime argument does not remove the obstruction to a globally free torus action.

W does have an almost-free circle action, and its rationalization has the rational type of S^5. Thus this note does not produce a gap against an almost-free toral rank or a rational-homotopy toral rank. It addresses the actual free-action definitions printed in [1]. Hanke's asymptotic bound rk_p(W)<=-chi^pi(W)=1 is satisfied; it does not assert equality with rk_T(W).

No computational check proves the infinite-prime or topological claims. Those follow from the arguments above. The accompanying computations are finite diagnostics of the weight congruences and the small mod-2 algebra only.

## References

[1] B. Hanke, "Homotopy Euler characteristic and the stable free rank of symmetry," in *Cohomology of Finite Groups: Interactions and Applications*, Oberwolfach Reports 7 (2010), 1912-1915. Report DOI: https://doi.org/10.4171/OWR/2010/32 . Official report: https://ems.press/content/serial-article-files/46287 .

[2] A. Debray and M. Yu, "What Bordism-Theoretic Anomaly Cancellation Can Do for U," *Communications in Mathematical Physics* 405, article 154 (2024), especially Lemma 4.41, Corollary 4.44, Proposition 4.45, and Lemma 5.20. https://doi.org/10.1007/s00220-024-04937-4 .

[3] D. Yeroshkin, "Orbifold biquotients of SU(3)," *Differential Geometry and its Applications* 42 (2015), 54-76, Proposition 4.2. https://doi.org/10.1016/j.difgeo.2015.07.003 ; author preprint https://arxiv.org/abs/1401.7565 .
