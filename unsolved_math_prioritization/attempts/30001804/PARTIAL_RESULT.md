# Surface Steinberg presentations: a certificate reduction, with the explicit-relations gap retained

**Unsolved original target; scoped algebraic result; independent review pending.** Record 30001804 / OWR-5158-001. This package does not give the requested general-genus list of relations on the designated surface generator.

## 1. Source and scope

The [2011 Oberwolfach report](https://oa.tib.eu/renate/server/api/core/bitstreams/b5c4c1c3-353d-4cd9-b9fc-9915ad312a53/content), p.1649, asks separately for understanding the module structure and for a presentation on Broaddus's single generator. Here Σ_g^1 is a genus-g surface with **one marked point**, not a surface with a boundary circle fixed pointwise. The module is reduced integral curve-complex homology in degree 2g−2.

[Broaddus, arXiv:0711.0011v3](https://arxiv.org/abs/0711.0011v3), Proposition 3.6, provides a finite presentation using oriented filling-arc orbit representatives, both boundary relations and signed stabilizer relations. Theorem 4.2 proves cyclicity. Remark 4.7 explicitly notes the theoretical calculability of a finite generating set for the annihilator ideal and asks for more geometric understanding. The report's Proposition 3.5 reference uses older numbering. Thus abstract finite presentability on one generator is already implied by known work and is not a resolution here.

[Irmer's 2026 paper](https://www.ms.u-tokyo.ac.jp/journal/c4403d3f4e9f2de5b1eca004b17daed0cf0807b1.pdf) concerns explicit generating spheres for **closed** surfaces. Its Corollary 1.2 states faithfulness after quotienting by the center, a qualification not visible in the shorter abstract. Its stated generator and faithfulness results do not themselves supply the requested marked-surface relation list. A braid-group single-generator presentation is likewise a different target. This is a scoped literature check, not a claim that every current paper has been exhausted.

## 2. A noncommutative certificate lemma

Let R be any unital ring. All modules are left R-modules. Set
\[
F=\bigoplus_{i=0}^{s-1}Re_i,\quad
N=\sum_{j=1}^t Rr_j,\quad
r_j=\sum_i b_{ji}e_i,\quad M=F/N.
\]
Suppose the class of e₀ generates M. Choose a₀=1 and a_i∈R such that
\[
e_i-a_i e_0\in N\quad (0\leq i<s).
\tag{1}
\]
Then the annihilator of [e₀] is the left ideal
\[
J=\sum_{j=1}^t R\left(\sum_i b_{ji}a_i\right),
\quad M\cong R/J.
\tag{2}
\]

**Proof.** Define the left-linear map T:F→R by T(e_i)=a_i, so T(Σx_i e_i)=Σx_i a_i. By (1), x−T(x)e₀∈N for every x∈F. In particular T(r_j)e₀∈N, so the displayed ideal is contained in the annihilator. Conversely if re₀∈N, write re₀=Σ_j c_j r_j. Applying T and using a₀=1 gives r=Σ_j c_j T(r_j), proving the reverse inclusion. The map R→M sending r to r[e₀] is surjective by cyclicity and has kernel J. □

The order b_{ji}a_i matters. R is the noncommutative group ring in the application, and one cannot commute substitution coefficients through relation coefficients. No Noetherian assumption or two-sided ideal claim is used.

A finite, independently checkable input certificate consists of the a_i and coefficients c_{ij} with
\[
e_i-a_i e_0=\sum_j c_{ij}r_j
\tag{3}
\]
as literal equalities in the finite free module. Once these are supplied, (2) proves both sufficiency and completeness of the resulting relators. Merely verifying that some proposed relators annihilate [e₀] proves only one inclusion and is insufficient.

## 3. Arbitrary representative and a necessary consistency relation

If the desired cyclic generator is represented instead by c=Σ_i c_i e_i, choose a_i with e_i−a_i c∈N and again T(e_i)=a_i. Then
\[
\operatorname{Ann}_R([c])
=\sum_j RT(r_j)+R\bigl(1-T(c)\bigr).
\tag{4}
\]
To prove inclusion from right to left, use x≡T(x)c modulo N, first for r_j and then for c. Conversely rc∈N implies rT(c)∈T(N); writing r=r(1−T(c))+rT(c) proves the other inclusion. This also gives a finite presentation on any selected cyclic generator.

The consistency term cannot be discarded in general. For R=Z, F=Ze, N=2Ze, choose c=3e and a=3. Then e−ac=−8e∈N, T(2e)=6, and 1−T(c)=−8. The correct annihilator is (6,−8)=2Z. Keeping only the substituted old relator would incorrectly give Z/6Z in place of Z/2Z.

## 4. Application to the arc-system presentation

Take R=Z[Mod(Σ_g^1)] and choose the finite oriented 0-filling orbit representatives so that e₀ is Broaddus's designated generator. Include **all** signed stabilizer relations from Proposition 3.6 together with the boundaries of the 1-filling representatives. They form the r_j above.

Cyclicity implies the existence of a_i satisfying (1). For a boundary relation r_j=Σ_i b_{ji}e_i the transferred relator is Σ_i b_{ji}a_i. For the signed stabilizer relation (1−ε_i h_i)e_i it is (1−ε_i h_i)a_i, in that order. If every equation (3) is supplied, these relations present the original Steinberg module, not just a quotient or a surjection onto it.

This is a certificate format and a proof of what the certificates would establish. It does not supply the required a_i, mapping-class words, or coefficients c_{ij} in general genus. The existential implication “finite presentation plus cyclicity yields finite annihilator generators” was already available, as Broaddus's remark confirms.

For completeness, there is a conditional exhaustive-search procedure. If R has an effective encoding with computable addition, multiplication, and additive inverse, its elements are effectively enumerable, and equality of its elements is recursively enumerable, enumerate tuples (a_i,c_{ij}) and dovetail searches verifying all equalities (3), fixing a₀=1. Cyclicity and the finite presentation guarantee that a successful finite tuple exists, so the search eventually returns one; formula (2) then gives a presentation. Negative equality decisions are unnecessary. This statement is conditional on an effective encoding and verification of the input presentation. No running-time bound, practical surface implementation, or explicit uniform relation family is claimed.

## 5. Exact controls and remaining gap

The verifier checks noncommutative substitution over M₂(F₂), including all choices of the second generator's coefficient and every vector in the two-generator free module. It compares the generated relation submodule with the direct action kernel, checks left-linearity, and detects the erroneous reversed product order. Integer controls verify the consistency-term example. These finite-ring controls support the algebraic lemma; they do not test or construct mapping-class-group relations.

Two substantive approaches were explored: certificate/Tietze elimination and source-driven geometric presentation reduction. The former yields the fully proved algebraic lemma; the latter stalls at explicit general-genus arc-reduction certificates and their relation simplification. The original broad structure and requested explicit-relations problem remain **unsolved**, proposed status 2/5. No new finite-generation, finite-presentation, or first-discovery claim is made. Actual model metadata: inherited runtime, exact model identifier not exposed; no model/reasoning switch made.
