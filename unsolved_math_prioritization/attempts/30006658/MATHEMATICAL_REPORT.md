# Vanishing of the cellularization map for non-p-nilpotent component groups

Problem 30006658 / OWR-14299915-021. Accepted proof-only edition, 10 October 2026.

## Result and scope

**Theorem.** Let (p) be a prime, (k) a field of characteristic (p), and (G) a compact Lie group. Write
\[
 X=(BG)^\wedge_p,\qquad R=C_*(\Omega X;k).
\]
If the finite group \(\pi_0G\) is not (p)-nilpotent, the canonical (k)-cellularization map
\[
 \nu:\Gamma_kR\longrightarrow R
\]
induces the zero map in every homotopy degree.

In particular this answers the literal positive-dimensional question of J. P. C. Greenlees, Question 2.2 in Oberwolfach Report 9/2026, printed p. 594, affirmatively. The argument does not require orientability of the adjoint representation, nilpotent component-group action, or collapse of a spectral sequence. It proves zero on homotopy; it does not assert that \(\nu\) is null in the derived category.

**Review status.** The complete authored proof was accepted for its full stated scope by the accompanying independent mathematical audit, with no required correction. The constituent Hopf-algebra and proxy-smallness theorems are established prior mathematics, credited below. This AI-assisted manuscript and audit are unrefereed; acceptance does not mean external human peer review, journal acceptance, or formal proof-assistant certification. No claim of literature novelty or exhaustive current-openness verification is made.

## 1. A finite-ideal fact, including graded signs

**Lemma 1.** An infinite-dimensional graded Hopf algebra over a field has no nonzero finite-dimensional graded left or right ideal. Here the Hopf structure uses the Koszul sign symmetry.

First recall the ordinary, ungraded result (Sweedler's finite-ideal theorem; see Lomp, §2.4). A short proof is included to specify the required version.

Let (B) be an ordinary Hopf algebra and (I\ne0) a finite-dimensional right ideal. Set
\[
 J=\operatorname{span}\{(1\otimes f)\Delta(i):i\in I,\ f\in B^*\}\subset B.
\]
The subspace (J) is finite-dimensional: choose a finite basis of (I), write the coproduct of each basis element as a finite sum, and take the span of all first tensor factors. Also (I\subset J), by using the counit. Coassociativity gives \(\Delta(J)\subset J\otimes B\).

The subspace (J) is a right ideal. Indeed, with \(i\in I\), \(b\in B\), and \(f\in B^*\), the antipode identity gives
\[
 ((1\otimes f)\Delta(i))b
 =\sum (1\otimes f_{b_{(2)}})\Delta(i b_{(1)}),\qquad
 f_c(z)=f(zS(c)).
\]
For verification, the expression on the right is
\(\sum i_{(1)}b_{(1)} f(i_{(2)}b_{(2)}S(b_{(3)}))
=\sum i_{(1)}b f(i_{(2)})\).
Every \(ib_{(1)}\) belongs to (I), proving the assertion.

Consequently (J), with multiplication and restricted coproduct, is a right Hopf submodule of (B). The fundamental theorem of Hopf modules gives
\[
 J\cong J^{\operatorname{co}B}\otimes B.
\]
Inside the regular comodule (B), an element (x) satisfying \(\Delta x=x\otimes1\) is \(\epsilon(x)1\). Thus \(J^{\operatorname{co}B}\subset k1\). Since (J\ne0), its coinvariants are nonzero, so (B) is finite-dimensional. The left-ideal version follows by applying this argument to \(B^{\mathrm{op},\mathrm{cop}}\), which is a Hopf algebra with the same antipode. This argument uses no assumption that the original antipode is bijective.

For a graded Hopf algebra (H), characteristic two presents no sign issue, and forgetting the grading gives an ordinary Hopf algebra. In other characteristics reduce the grading modulo two and form the standard parity bosonization
\[
 B=H\mathbin{\#} kC_2.
\]
For homogeneous (h,a\in H), with (g^2=1) and (i,j\in\{0,1\}\), its formulas are
\[
 (h\#g^i)(a\#g^j)=(-1)^{i|a|}ha\#g^{i+j},
\]
\[
 \Delta_B(h\#g^i)=\sum
 (h_{(1)}\#g^{|h_{(2)}|+i})\otimes(h_{(2)}\#g^i),
 \qquad \epsilon_B(h\#g^i)=\epsilon_H(h),
\]
\[
 S_B(h\#g^i)=(1\#g^{i+|h|})(S_H(h)\#1).
\]
The graded Hopf identities verify the ordinary Hopf identities for these formulas. If (I\subset H) is a graded one-sided ideal, (I\# kC_2\) is a one-sided ideal of (B). Its dimension is (2\dim_k I), while \(\dim_k B=2\dim_k H\). The ordinary result therefore proves Lemma 1. In particular, the proof does not mistakenly treat an odd-characteristic graded Hopf algebra as an ungraded Hopf algebra. ∎

## 2. Compact approximation of cellular objects

Work in the derived category, or the stable category, of modules over an augmented differential graded (k)-algebra (A\to k). The same argument applies to the corresponding (Hk)-algebra. Write \(\operatorname{thick}(K)\) for finite construction from (K), allowing suspensions, finite sums, cones and retracts; write \(\operatorname{Loc}(K)\) when arbitrary coproducts are also allowed.

Recall that (k) is **proxy-small** over (A) if there is an (A)-module (K) such that
\[
 K\in\operatorname{thick}(A)\cap\operatorname{thick}(k),
 \qquad k\in\operatorname{Loc}(K).
\]
In particular (K) is compact and \(\operatorname{Loc}(K)=\operatorname{Loc}(k)\). This is Dwyer–Greenlees–Iyengar (DGI), Definition 4.6 and Remark 4.8.

**Lemma 2.** If (k) is proxy-small over (A), any (k)-cellular (A)-module (M) is a filtered homotopy colimit of modules in \(\operatorname{thick}(K)\). Each such module has finite-dimensional total homotopy over (k). Consequently, every homogeneous class in \(\pi_*M\) comes from the homotopy of one such finite-dimensional module.

**Proof.** Put (E=\operatorname{End}_A(K)). Compact Morita equivalence identifies \(\operatorname{Loc}(K)\) with right (E)-modules; its inverse is
\[
 T(N)=N\otimes_E^{\mathbf L}K.
\]
This is precisely DGI Theorem 4.9 applied to the compact object (K). Every derived (E)-module is a filtered homotopy colimit of perfect (E)-modules. One can see this directly in a differential graded model: choose a semi-free resolution with a well-ordered basis whose differential involves only earlier basis elements. Each differential is a finite sum. The dependency closure of a finite set of basis elements is finite: its finitely branching dependency tree has no infinite path, because the indices strictly decrease. The finite dependency-closed subsets form a filtered system of finite semi-free submodules with union the resolution. The inclusions are semi-free cofibrations, so this union represents the homotopy colimit.

The functor (T) preserves these colimits and sends each perfect (E)-module to \(\operatorname{thick}(K)\). Since \(K\in\operatorname{thick}(k)\), every object of \(\operatorname{thick}(K)\) is finitely built from (k); its total homotopy is therefore finite-dimensional over (k). Finally homotopy commutes with filtered homotopy colimits of module spectra (equivalently, filtered colimits are exact for complexes of vector spaces). ∎

The argument does not assume that the cellular generator (k) itself is compact. Replacing it by the compact proxy (K) is essential.

## 3. A general vanishing criterion

**Proposition 3.** Suppose (A\to k) is an augmented differential graded (k)-algebra such that:

1. (k) is proxy-small as an (A)-module;
2. \(H=\pi_*A\), with its multiplication, admits a graded Hopf algebra structure over (k);
3. \(\dim_k H=\infty\).

Then every (A)-linear map \(f:M\to A\) from a (k)-cellular module induces zero on every homotopy group. In particular \(\pi_*(\Gamma_kA\to A)=0\).

**Proof.** Let (x\in\pi_n M\). By Lemma 2 there is \(P\in\operatorname{thick}(K)\), a map \(u:P\to M\), and \(y\in\pi_nP\) with \(u_*(y)=x\). The image
\[
 I=\operatorname{im}\bigl(\pi_*(f u):\pi_*P\longrightarrow H\bigr)
\]
is a graded left ideal of (H), because (fu) is (A)-linear and the target is the regular left module. It is finite-dimensional because \(\pi_*P\) is finite-dimensional. Lemma 1 gives (I=0). Hence \(f_*(x)=0\). This works in every integer degree. ∎

Notice the distinction from a global boundedness argument: even if \(\Gamma_kA\) has homotopy in arbitrarily high positive degrees, each individual class is tested through a finite-dimensional approximation. No untwisted duality identification is needed.

## 4. Verification of the hypotheses for completed loop chains

Let \(X=(BG)^\wedge_p\) and \(R_0=C_*(\Omega X;\mathbb F_p)\).

### Proxy-smallness

DGI §5.7 proves for every compact Lie group (G) that the augmentations of both \(C^*(X;\mathbb F_p)\) and \(C_*(\Omega X;\mathbb F_p)\) are proxy-small. No adjoint-orientability condition occurs in that argument. It uses a faithful embedding \(G\hookrightarrow SU(n)\), the finite homogeneous space \(SU(n)/G\), and the cochain fibration construction. DGI §4.22 and Proposition 4.17 transfer proxy-smallness across the double-centralizer equivalence. Greenlees 2504.03050v3, §2.C, restates this fact for the rings at issue here.

For an arbitrary field (k) of characteristic (p), scalar extension gives
\[
 R\simeq R_0\otimes_{\mathbb F_p}k.
\]
If (K_0) is a compact proxy for \(\mathbb F_p\) over (R_0), then
\(K=K_0\otimes_{\mathbb F_p}k\) is finitely built from (R), finitely built from (k), and builds (k): derived scalar extension preserves finite constructions and arbitrary colimits. Thus (k) is proxy-small over (R). This also avoids any unjustified interchange of an infinite cochain dual with extension of scalars.

### Hopf structure

The loop space \(\Omega X\) is a grouplike (H)-space and may be replaced by a homotopy-equivalent simplicial/topological group. Pontryagin multiplication, diagonal, unit, augmentation and loop inverse give
\[
 H_*(\Omega X;k)=\pi_*R
\]
a graded Hopf algebra. The diagonal satisfies the graded bialgebra identity, and the Künneth isomorphism over the field (k) identifies homology of a product with the tensor product. This argument does not require \(\Omega X\) to be connected; in this case its component group is finite and is a (p)-group, but Lemma 1 does not need that extra fact.

### Infinite dimension

A classifying space (BG) is called (p)-compact when \(H_*(\Omega(BG)^\wedge_p;\mathbb F_p)\) has finite total dimension. Ishiguro, *Classifying spaces of compact Lie groups that are p-compact for all prime numbers*, Proposition 1.3(a), printed p. 199, states the necessary condition
\[
 BG\text{ is }p\text{-compact}\quad\Longrightarrow\quad\pi_0G\text{ is }p\text{-nilpotent}.
\]
It cites his earlier *Toral groups and classifying spaces of p-compact groups*, Proposition 3.1. Taking the contrapositive under the present hypothesis proves \(\dim_{\mathbb F_p}\pi_*R_0=\infty\). Extension to the field (k) preserves infinite dimension, so \(\dim_k\pi_*R=\infty\).

All three hypotheses of Proposition 3 hold. Taking (M=\Gamma_kR) and (f=\nu) proves the theorem. ∎

## 5. Scope and prior-work controls

- The coefficient (k) is a field. The finite-ideal theorem can fail over coefficient rings; no ring-coefficient generalization is claimed.
- Completion is applied to (BG) before looping. Neither (C_*(G;k)) nor an ordinary group algebra is substituted for (R).
- The conclusion is all-graded homotopy vanishing of the canonical cellularization map. A nontrivial map may induce zero on all homotopy groups.
- The proof applies in characteristic two and odd characteristic, including nonorientable adjoint actions. It never uses \(\Gamma_kR\simeq\Sigma^{\dim G}R^\vee\).
- Greenlees's finite-group dichotomy (Lemma 6.2) and nilpotent-action/projected-image/tensor-collapse statements (Lemma 6.5 and Remark 6.6) remain credited prior results. They are not being relabeled as this argument.
- The originating question is credited to J. P. C. Greenlees.

## References

1. J. P. C. Greenlees, *The singularity category and duality for complete intersection groups*, Oberwolfach Report 9/2026, pp. 592–595; Question 2.2 on p. 594. DOI: https://doi.org/10.4171/owr/2026/9 . Official PDF: https://ems.press/content/serial-article-files/53607?nt=1 .
2. J. P. C. Greenlees, *The singularity category and duality for complete intersection groups*, arXiv:2504.03050v3, 27 April 2026, especially §§2.C, 5.B–5.C and 6. https://arxiv.org/abs/2504.03050v3 .
3. W. G. Dwyer, J. P. C. Greenlees and S. Iyengar, *Duality in algebra and topology*, Advances in Mathematics 200 (2006), 357–402, especially Definition 4.6, Remark 4.8, Theorem 4.9, Proposition 4.17, §4.22 and §5.7. DOI: https://doi.org/10.1016/j.aim.2005.11.004 . Publisher-version PDF: https://www.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf .
4. C. Lomp, *Integrals in Hopf algebras over rings*, §2.4, arXiv:math/0307046. https://arxiv.org/abs/math/0307046 . The field finite-ideal theorem is credited there to Sweedler.
5. K. Ishiguro, *Classifying spaces of compact Lie groups that are p-compact for all prime numbers*, Geometry & Topology Monographs 10 (2007), 195–211, Proposition 1.3. DOI: https://doi.org/10.2140/gtm.2007.10.195 . Official PDF: https://msp.org/gtm/2007/10/gtm-2007-10-011p.pdf .
6. K. Ishiguro, *Toral groups and classifying spaces of p-compact groups*, Contemporary Mathematics 271 (2001), 155–167, Proposition 3.1. This earlier result was verified through the author's explicit restatement in Reference 5; the original article was not separately inspected for this attempt.

## Supplementary bibliography and published-version limit

A separate bibliographic check on 10 October 2026 identified the published
version of Greenlees's manuscript: *Bulletin of the London Mathematical
Society* 58(6) (2026), e70405, DOI https://doi.org/10.1112/blms.70405 .
Publisher-deposited [Crossref metadata](https://api.crossref.org/works/10.1112/blms.70405)
records acceptance on 3 May 2026 and online publication on 1 June 2026.
Initial direct HTML and PDF requests returned HTTP 403, but a subsequent
browser visit successfully displayed the [published HTML](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.70405).
The full published §6 was read on 10 October 2026 at 06:23 UTC. It retains
the finite-group dichotomy in Lemma 6.2, nilpotent-action and partial-vanishing
scope in §6.5/Lemma 6.5, and the tensor-collapse hypothesis in Remark 6.6.
Section 6.1 assumes adjoint k-orientability. The unrestricted theorem of
this report was not found in that inspected section. The published PDF was
not downloaded or hashed, and byte equivalence with arXiv v3 is not asserted.
This targeted section check does not establish priority, exhaustive current
openness or absence of a resolution elsewhere.

The compact-proxy and filtered-colimit machinery also has an explicit prior
presentation in Benjamin Briggs, Srikanth B. Iyengar and Greg Stevenson,
*Proxy-small objects present compactly generated categories*, New York Journal
of Mathematics 31 (2025), 701–721. The inspected primary manuscript is
https://arxiv.org/abs/2411.07328v2 (18 December 2024): §2, Definition 2.1
and its following Ind-completion discussion, Remarks 2.3 and 2.6, and Lemma
4.1. The [published PDF](https://sunsite3.icm.edu.pl/packages/EMIS/journals/NYJM/j/2025/31-26p.pdf)
was subsequently obtained and inspected: Definition 2.1, its following
Ind-completion discussion and Remark 2.3 are on printed p. 703; Lemma 4.1
and its filtered-perfect-colimit proof are on printed p. 709. The lemma
represents an E-module as a filtered homotopy colimit of objects in thick(E)
and tensors to thick(P). This reinforces prior-work credit for the machinery
used in Lemma 2; the report retains its self-contained argument and makes
no novelty claim for that mechanism.
