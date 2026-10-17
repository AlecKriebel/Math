**Integrated reader status.** Accepted symplectic marginal stage. Its original candidate-stage scope and final future-work paragraph are retained as historical statements; the later generation and orthogonal obligations are discharged by the other proofs in this reader. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# A uniform marginal bound for natural symplectic groups

## Status and scope

This is an authored proof candidate for independent audit, 13 October 2026. It addresses only the even-branch probability statement in the exact natural symplectic group. It does not assert the all-classical result, projective variants, or a generation theorem.

The linear/unitary logarithmic probability results are prior literature. In particular, the use of a distinguished factor whose eigenvalues have strictly largest 2-part follows the mechanism of Dixon–Praeger–Seress, *Strong involutions in finite special linear groups of odd characteristic*, J. Algebra 498 (2018), 413–447, DOI 10.1016/j.jalgebra.2017.11.047, https://people.math.carleton.ca/~jdixon/Strong%20Involutions.pdf . Their regular-semisimple pair count is not used as a symplectic count. The symplectic graph-chart count below is proved explicitly.

## Theorem

Let q be an odd prime power and G=Sp(V)=Sp(2m,q), with natural dimension n=2m≥49152. Let t∈G be an involution such that each of its two eigenspaces has dimension in [n/3,2n/3]. For a uniform g∈G put y=t t^g, and put z=inv(y), where inv(y)=1 if y has odd order and inv(y)=y^{|y|/2} otherwise. For either fixed ε∈{+1,−1},

P(z restricted to E_ε(t) is strong) > 1/(40000 log n).

Here log denotes the natural logarithm, and strong on a space of dimension e means that both eigenspaces have dimensions in [e/3,2e/3]. These are two separate marginal statements. No simultaneous-event bound is asserted. No assertion is made below the stated dimension threshold.

## 1. Symplectic graph chart and its exact measure

Replacing t by −t leaves t t^g unchanged, so arrange V=A⊥B with t=−I on A and +I on B, dim A=2a≤2b=dim B. Strongness says a≤b≤2a, and n=2(a+b). In particular a≥n/6≥8192.

For a linear map F:A→B write F*:B→A for its adjoint with respect to the alternating forms, and let K=F*F. Then K is self-adjoint on A. Suppose K and I+K are invertible. The map F is injective, its image is nondegenerate, and its graph W={(u,Fu):u∈A} is nondegenerate: the form induced on the graph is (u,v)↦⟨u,(I+K)v⟩. The involution s_W that is −I on W and +I on W⊥ is conjugate to t in G.

Every such W is counted once by its graph map F. Uniform g makes t^g uniform on its conjugacy class, whose cardinality is

N=|Sp(2(a+b),q)|/(|Sp(2a,q)| |Sp(2b,q)|).

Fix a monic squarefree polynomial f∈F_q[X] of degree a, coprime to X(X+1). There is exactly one Sp(A)-conjugacy class of semisimple self-adjoint K with characteristic polynomial f² and minimal polynomial f. If the distinct irreducible factors of f have degrees d_1,...,d_s, its centralizer in Sp(A) is the product of Sp(2,q^{d_i}). Consequently the number of such K is

|Sp(2a,q)| / ∏_i |Sp(2,q^{d_i})|.                                      (1)

For completeness, on the primary space for an irreducible factor of degree d, F_q[K] is F_{q^d} and the space has dimension two over this field. Self-adjointness makes the original form the trace of a unique nondegenerate F_{q^d}-bilinear alternating form. All such two-dimensional forms are isometric. Its isometry group is Sp(2,q^d). Orthogonal primary decomposition proves both uniqueness and (1).

For fixed invertible self-adjoint K, the equation F*F=K asks for isometric embeddings of the symplectic space (A,(u,v)↦⟨u,Kv⟩) into B. The symplectic group of B acts transitively on them, with pointwise stabilizer Sp(2(b−a),q). Hence the number of F is exactly

|Sp(2b,q)|/|Sp(2(b−a),q)|.                                            (2)

Combining (1), (2), and N, the probability mass associated with this f is exactly

P_f=|Sp(2a,q)|² |Sp(2b,q)|² /
    (|Sp(2(a+b),q)| |Sp(2(b−a),q)| ∏_i |Sp(2,q^{d_i})|).              (3)

Put ψ_r(q)=∏_{j=1}^r(1−q^{−2j}), with ψ_0=1. Using |Sp(2r,q)|=q^{2r²+r}ψ_r(q), equation (3) becomes

P_f=q^{−a} [ψ_a² ψ_b²/(ψ_{a+b} ψ_{b−a})] ∏_i(1−q^{−2d_i})^{−1}.

Since ψ_r≥1−∑_{j≥1}q^{−2j}≥7/8 for all q≥3, while ψ_r≤1,

P_f ≥ (7/8)^4 q^{−a} > (1/2)q^{−a}.                                (4)

This is an unconditional lower bound under uniform g. There is no assumption that a uniformly sampled conjugate gives uniformly distributed K, nor any omission of graph-chart probability.

## 2. The spectral meaning of the polynomial

Let C=F(A)⊥∩B. Then V=A⊕F(A)⊕C, dim C=2(b−a), and both t and s_W are +I on C. Thus y=t s_W and z are I on C.

Relative to A⊕F(A), writing a vector as (u,Fv), a direct projection calculation gives

y = [[(I−K)(I+K)^{−1}, 2K(I+K)^{−1}],
     [−2(I+K)^{−1},     (I−K)(I+K)^{−1}]].                          (5)

For a root κ of an irreducible factor of f, the corresponding y-eigenvalues λ,λ^{−1} satisfy

λ+λ^{−1}=2(1−κ)/(1+κ),
κ=−(λ−1)²/(λ+1)².                                                   (6)

Since κ≠0,−1, these roots are distinct and neither is ±1. The block for a degree-j factor has dimension 4j in V and dimension 2j in each of A and F(A). The two reciprocal eigenvalues have the same multiplicative order, and Frobenius conjugates preserve that order. The entire block therefore has a single 2-part of eigenvalue order. Formula (5) also shows that y is semisimple on every block.

If exactly one factor f_* of degree k yields the strictly largest 2-part, and this 2-part is >1, then y has even order and z is −I on the whole 4k-dimensional block for f_* and +I on every other block and on C. Therefore

dim(E_−(z)∩A)=dim(E_−(z)∩B)=2k.                                    (7)

The equality in (7) concerns negative dimensions; the fixed complement C remains in the positive eigenspace on B.

## 3. Many factors with a distinguished 2-part

Fix a power of two d=2^h with h≥2, and let k=d times an odd positive integer, k≥4. There are at least q^k/(8k) monic irreducible polynomials f_* of degree k for which the eigenvalues in (6) have 2-part exactly (q^k−1)_2.

Proof. Among F_{q^k}^× exactly (q^k−1)/2 elements have this maximal 2-part. Elements lying in any proper subfield belong to the union of F_{q^j} over 1≤j≤k/2, so there are fewer than q^{k/2+1}/(q−1)≤(3/2)q^{k/2} of them. For q≥3 and k≥4,

(q^k−1)/2 − (3/2)q^{k/2} ≥ q^k/4.

For each remaining λ define κ by (6). The denominator is nonzero, and κ≠0,−1. Its degree is either k or k/2, since λ satisfies a quadratic over F_q(κ). If the degree were k/2, Frobenius q^{k/2} would interchange λ and λ^{−1}; hence λ would have order dividing q^{k/2}+1. But k/2 is even, so (q^{k/2}+1)_2=2, whereas (q^k−1)_2≥8. Thus κ has degree k. The map λ↦κ is exactly two-to-one on these elements, identifying only λ with λ^{−1}. Dividing further by the k-element Frobenius orbit yields at least q^k/(8k) distinct f_*.

For a factor of degree j, its λ lies either in F_{q^j}^× or in the norm-one subgroup of F_{q^{2j}}^×. Its 2-part is therefore bounded by max((q^j−1)_2,(q^j+1)_2). Put e=v_2(q²−1). The elementary 2-adic identities are:

- For j odd, this maximum is 2^{e−1}.
- For j even, this maximum is 2^{e+v_2(j)−1}.

For k=d times odd the distinguished 2-part is 2^{e+h−1}. If d does not divide j, the 2-part associated with degree j is strictly smaller. Therefore it suffices to forbid factor degrees divisible by d in the remainder polynomial.

## 4. Enough squarefree remainder polynomials

For every r≥0 and odd q≥3, at least q^r/3 monic degree-r polynomials are squarefree and coprime to X(X+1).

One elementary verification is as follows. For q≥5 and r≥2, there are q^{r−1} nonsquarefree monic polynomials and at most 2q^{r−1} polynomials with one of the two forbidden roots, leaving at least (1−3/q)q^r≥(2/5)q^r. The cases r=0,1 are direct. For q=3 the generating function for the normalized counts c_r is

Σ_{r≥0}c_r u^r=(1−u²/3)/((1−u)(1+u/3)²),

so c_r=3/8+(−1)^r 3^{−r}(10−8r)/16. This gives c_0=1, c_1=c_2=1/3; odd r≥3 give c_r>3/8, and for even r≥2 the correction has largest absolute value at r=2. Hence c_r≥1/3.

The number of degree-r monic polynomials having an irreducible factor of degree divisible by d is at most

Σ_{1≤j≤r/d} N(q,jd) q^{r−jd}
 ≤ q^r Σ_{1≤j≤r/d}1/(jd)
 ≤ q^r(1+log r)/d,                                                   (8)

where N(q,l)≤q^l/l is the elementary irreducible-polynomial bound. If r<d, the sum is zero. In particular, if 0≤r≤a and d≥12(1+log a), at least q^r/4 monic degree-r polynomials are squarefree, coprime to X(X+1), and have no irreducible factor of degree divisible by d. The assertion for r=0 is immediate.

## 5. Separate balance intervals and the final bound

Choose the least power of two d satisfying d≥12(1+log a). Then

12(1+log a)≤d<24(1+log a).

Since a≥8192, we have a≥576(1+log a)>24d. For the target A use the interval

[L,U]=[a/3,2a/3].

For the target B use instead

[L,U]=[b/3,min(2b/3,5a/6)].

In either case L≥a/3, U≤5a/6, and U−L≥a/6. Every k in the relevant interval makes the negative dimension 2k in (7) lie between one third and two thirds of the target dimension. Thus it gives a strong restriction to the selected eigenspace.

The integers k=d times odd have spacing 2d, so the interval contains at least

(U−L)/(2d)−1 ≥ a/(12d)−1 ≥ a/(24d)

such integers. For each k, Section 3 gives at least q^k/(8k) choices for f_*. Section 4 gives at least q^{a−k}/4 choices for a remainder f_0. The product f=f_*f_0 is squarefree, avoids 0,−1, and has exactly one irreducible factor whose degree is divisible by d. Therefore different choices of k, f_*, f_0 give different f; there is no overcount.

The number of good f is at least

Σ_k q^a/(32k) ≥ q^a/(768d).

Using their disjoint graph-chart masses from (4) gives

P(strong restriction to the selected eigenspace)
 > 1/(1536d)
 > 1/[36864(1+log a)]
 > 1/(36864 log n)
 > 1/(40000 log n).

The penultimate inequality uses n=2(a+b)≥4a>ea. This proves the theorem for either fixed eigenspace.

## 6. Why the linear regular-semisimple count cannot be copied

In fact every eigenvalue of a product y=t s of two symplectic involutions in odd characteristic has even algebraic multiplicity. For λ≠±1, t maps the generalized λ-space to the generalized λ^{−1}-space, and (u,v)↦⟨u,tv⟩ is a nondegenerate alternating form on the generalized λ-space. Its dimension is even. The ±1 primary spaces are themselves nondegenerate symplectic spaces and also have even dimension. Thus the characteristic polynomial of y is a square. This explains the failure of the natural-representation separable-characteristic-polynomial stratum used in the linear/unitary analyses.

The proof above uses semisimple blocks with eigenvalue multiplicity two instead. It counts their actual symplectic stabilizers, which are Sp(2,q^d), rather than linear torus stabilizers.

## Remaining algorithmic work

The theorem is a probability statement, not a complete generation analysis. Turning it into a logarithmic centralizer-generation algorithm still requires a correctly scoped class-random generation theorem and an argument that handles the product factors without an unjustified subdirect-product shortcut. In the large dimensions used here C_G(t)=Sp(2a,q)×Sp(2b,q) has perfect factors, so the distinction between C_G(t)'' and its last derived subgroup disappears for this exact family; nevertheless, that observation alone does not prove generation. Orthogonal families and small-dimensional exceptions remain outside this proof.
