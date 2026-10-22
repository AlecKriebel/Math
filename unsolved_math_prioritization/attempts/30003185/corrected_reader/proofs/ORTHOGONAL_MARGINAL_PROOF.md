**Integrated reader status.** Accepted orthogonal marginal stage. Original candidate-stage wording is retained; the later generation obligation is discharged by the generation bridge and replacement theorem. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# A uniform marginal bound for natural orthogonal groups

## Status and scope

Authored proof candidate, 13 October 2026, submitted for independent audit. It proves a proposed even-branch probability bound, not a generation theorem or the whole algorithmic claim. No novelty certificate is asserted.

The previously published linear and unitary probability theorems remain credited literature. The distinguished factor of uniquely largest eigenvalue-order 2-part follows the mechanism of Dixon–Praeger–Seress, *Strong involutions in finite special linear groups of odd characteristic*, J. Algebra 498 (2018), 413–447, DOI https://doi.org/10.1016/j.jalgebra.2017.11.047, author PDF https://people.math.carleton.ca/~jdixon/Strong%20Involutions.pdf . The present orthogonal count is derived independently; neither linear nor symplectic orbit weights are substituted for orthogonal weights.

## Theorem

Let q be an odd prime power, let V be a nondegenerate quadratic space over F_q of natural dimension n≥98304, and let G be one of the following exact matrix groups:

- O(V), the full isometry group;
- SO(V), the determinant-one isometry group;
- Ω(V), the subgroup of SO(V) with trivial spinor norm.

Let t∈G be an involution whose two eigenspaces each have dimension in [n/3,2n/3]. For uniform g∈G put y=t t^g. Define inv(y)=1 if |y| is odd, and inv(y)=y^{|y|/2} otherwise. For either fixed ε∈{+1,−1},

P(inv(y) restricted to E_ε(t) is strong) > 1/(5,000,000 log n).

Here log is natural. An involution on a space of dimension e is strong when its two eigenspaces have dimensions in [e/3,2e/3]. The theorem gives two marginal bounds separately; it does not claim simultaneous balance.

This includes both split and nonsplit even-dimensional quadratic spaces and both discriminant classes of odd-dimensional quadratic spaces. Odd-dimensional groups are often isomorphic after scaling the form, but the proof keeps the given space and its actual restricted discriminants. There is no passage to a projective quotient, no treatment of similitudes, and no assertion about involutions in a quotient whose matrix lifts have order four.

## 1. Conventions and conjugacy under O, SO, and Ω

Use a nondegenerate symmetric bilinear form β, and set Q(v)=β(v,v)/2. Write disc(U) for det(β|_U), modulo squares, on any nondegenerate subspace U. In each fixed dimension, nondegenerate symmetric forms over F_q are isometric exactly when these discriminants agree. For even dimension 2m the split type has χ(disc(U))=χ((-1)^m); the other type is nonsplit. In odd dimension both determinant classes are retained, even though scaling identifies the abstract isometry groups. Here χ is the quadratic character on F_q^×.

The spinor norm θ is normalized by θ(r_v)=Q(v) modulo squares for a reflection r_v. Its restriction to SO is unchanged if β(v,v), rather than Q(v), is used in the normalization. Thus Ω is unambiguously ker(det)∩ker(θ). These conventions match the finite-field formulation in Pellegrini–Tamburini Bellani, *The (2,3)-generation of the finite simple odd-dimensional orthogonal groups*, Section 2, https://www.cambridge.org/core/journals/journal-of-the-australian-mathematical-society/article/boldsymbol-23generation-of-the-finite-simple-odddimensional-orthogonal-groups/6E62763349A734703229266CFED37F7E .

For any involution t, its ±1 eigenspaces are perpendicular and nondegenerate, so

C_{O(V)}(t)=O(E_−(t))×O(E_+(t)).

Each eigenspace here has dimension at least three. A nondegenerate quadratic space of dimension at least three over F_q has a hyperbolic plane and consequently represents every nonzero element of F_q. Reflections supported in E_−(t) therefore realize both pairs

(det,θ)=(-1,square), (-1,nonsquare).

These generate the full quotient of O(V) by Ω(V). Hence

O(V)=Ω(V) C_{O(V)}(t).

The O(V)-conjugacy class of t is consequently a single Ω(V)-orbit and a single SO(V)-orbit. A uniform element of any of O(V), SO(V), or Ω(V) gives the same uniform distribution on that class. This is the explicit nonsplitting argument; no blanket nonsplitting claim for other classes is needed.

It is therefore sufficient to do the probability count in O(V). Replacing t by −t does not change t t^g. Arrange

V=A⊥B,  t=−I_A⊕I_B,  a=dim A≤b=dim B,

with a≤b≤2a, n=a+b and a≥n/3≥32768. This replacement is made only after the orbit reduction; it does not assume −I belongs to the original G.

## 2. The graph chart and its orthogonal constraints

For F:A→B let F*:B→A be its adjoint and set K=F*F. Then K is self-adjoint on A. If K and I+K are invertible, F is injective and F(A) is nondegenerate. The graph

W={(u,Fu):u∈A}

has induced form β_A(u,(I+K)v). Hence W is nondegenerate and isometric to A if and only if χ(det(I+K))=+1. In that case the involution s_W acting as −I on W and +I on W^⊥ is O(V)-conjugate to t. Conversely the graph determines F uniquely. The cardinality of the conjugacy class is

N=|O(V)|/(|O(A)| |O(B)|).                                           (1)

For fixed invertible self-adjoint K, the condition F*F=K says exactly that F is an isometric embedding of

A_K=(A, (u,v)↦β_A(u,Kv))

into B. Its discriminant is disc(A) det(K). Put c=b−a.

- If c>0, a nondegenerate c-dimensional space C exists with discriminant disc(B)/(disc(A)det K). The classification by dimension and discriminant gives A_K⊥C≅B.
- If c=0, an embedding exists if and only if χ(det K)=χ(disc(B)/disc(A)); then C is the zero space.

The isometry group O(B) acts transitively on the embeddings: choose an isometry of the images and of their orthogonal complements and take their orthogonal direct sum. The pointwise stabilizer of an embedding is O(C), including |O(0)|=1. Therefore there are exactly

|O(B)|/|O(C)|                                                     (2)

maps F for each admissible K. This retains the codimension-zero discriminant constraint, rather than treating it as an automatic embedding.

Fix once and for all a sign α: take α=χ(disc(B)/disc(A)) if c=0, and α=+1 if c>0. We will count only K satisfying

χ(det K)=α,  χ(det(I+K))=+1.                                      (3)

In particular the isometry type of C in (2) is fixed throughout this count.

## 3. Squarefree orthogonal self-adjoint operators and exact probability mass

Let f be monic squarefree of degree a, coprime to X(X+1), and let its distinct irreducible factors have degrees d_1,...,d_s. Consider self-adjoint operators K on A with characteristic polynomial f. The primary spaces are mutually perpendicular because their projection operators are polynomials in K and are self-adjoint. For each primary factor, L_i=F_{q^{d_i}} acts on a one-dimensional L_i-space. Every compatible symmetric F_q-bilinear form is

(u,v)↦Tr_{L_i/F_q}(c_i uv),  c_i∈L_i^×.

To justify this description, self-adjointness makes the form balanced over F_q[K]=L_i. Every F_q-linear functional on L_i is uniquely Tr(c_i·), since the trace pairing of a finite separable field extension is nondegenerate. The form is nondegenerate exactly when c_i≠0.

Changing the L_i-basis changes c_i by a square. There are two classes for each primary factor, and their centralizers within the isometry group both have order two, namely multiplication by ±1. Multiplying c_i by u_i∈L_i^× changes its F_q-discriminant by Norm_{L_i/F_q}(u_i). In particular a nonsquare multiplier changes the discriminant square class, since

χ_q(Norm x)=χ_{q^{d_i}}(x).

Thus exactly 2^{s−1} of the 2^s choices have total discriminant disc(A). All of these choices are realizable on the fixed space A, and they give distinct O(A)-conjugacy classes of K. Each has centralizer of order 2^s. Consequently the total number of K on A with characteristic polynomial f is exactly

2^{s−1}|O(A)|/2^s=|O(A)|/2.                                      (4)

The determinant signs depend only on f:

χ(det K)=χ((-1)^a f(0)),
χ(det(I+K))=χ((-1)^a f(−1)).                                     (5)

Whenever f satisfies (3) through (5), all the operators in (4) are admissible. Combining (1), (2), and (4), the disjoint graph-chart contribution of this f to the uniform-conjugate probability is exactly

P_f=|O(A)|² |O(B)|² / [2 |O(V)| |O(C)|].                          (6)

This is unconditional probability mass. We have neither conditioned on being in the chart nor asserted that a uniform conjugate gives a uniform K.

For a nonzero orthogonal space U of dimension m write |O(U)|=q^{m(m−1)/2} η(U). The standard order formulas, with ε=+1 for split and −1 for nonsplit, are

η(O(2r+1,q))=2∏_{j=1}^r(1−q^{−2j}),
η(O^ε(2r,q))=2(1−ε q^{−r})∏_{j=1}^{r−1}(1−q^{−2j}).

Since ∏_{j≥1}(1−q^{−2j})≥1−∑_{j≥1}q^{−2j}≥7/8, these give, uniformly in every positive dimension and every form type,

7/6≤η(U)≤8/3.

Set η(0)=1. The power of q in (6) is q^{−a}, including c=0. Since A and B have positive dimension,

P_f≥q^{−a}(7/6)^4/[2(8/3)^2]
   =q^{−a}·2401/18432
   >q^{−a}/8.                                                     (7)

The familiar order formulas are used for each actual quadratic space, not with an implicit common split sign. They are stated in D. E. Taylor, *The Geometry of the Classical Groups*, Chapter 11, printed p.141, author-hosted corrected text https://www.maths.usyd.edu.au/u/don/papers/gcg.pdf . The same chapter, pp.138–139 and Theorems 11.50–11.51 on pp.164–165, supplies the finite-field form classification and the spinor-kernel characterization used in Section 1. The order formulas on p.141 were checked both in extracted text and visually.

## 4. The spectrum of t s_W and the negative dimensions

Let C=F(A)^⊥∩B. Relative to A⊕F(A), identifying F(A) with A by F, the projection onto W gives

y=t s_W=
[[ (I−K)(I+K)^{−1},  2K(I+K)^{−1} ],
 [ −2(I+K)^{−1},     (I−K)(I+K)^{−1} ]].                           (8)

On C, y=I. For a root κ of f the two eigenvalues of the corresponding block satisfy

λ+λ^{−1}=2(1−κ)/(1+κ),
κ=−(λ−1)^2/(λ+1)^2.                                              (9)

Because κ≠0,−1 these eigenvalues are distinct and neither is ±1. The block belonging to a degree-j factor has dimension 2j in V and dimension j on each of A and F(A). It is semisimple, and all its eigenvalues have the same order 2-part, because inversion and Frobenius preserve order.

Suppose one factor f_* of degree k has eigenvalue-order 2-part strictly larger than that on all other blocks, and this 2-part exceeds one. Then |y| is even and z=inv(y) is −I on that entire 2k-dimensional block and +I on every other block and C. It follows that

dim(E_−(z)∩A)=dim(E_−(z)∩B)=k.                                  (10)

In particular the fixed complement in B has not been omitted from the positive eigenspace dimension.

## 5. Distinguished factors with controlled determinant characters

Fix a power of two d=2^h with h≥2 and take k=d times an odd positive integer. There are at least q^k/(8k) monic irreducible degree-k polynomials f_* for which the eigenvalues in (9) have order 2-part (q^k−1)_2 and for which

χ(det K_*)=+1,  χ(det(I+K_*))=−1.                                (11)

Indeed exactly (q^k−1)/2 elements λ of F_{q^k}^× have the maximal order 2-part. Elements in proper subfields belong to the union of fields F_{q^j} for j≤k/2, so their number is less than

∑_{j=1}^{k/2}q^j < q^{k/2+1}/(q−1) ≤(3/2)q^{k/2}.

For q≥3, k≥4 this leaves at least q^k/4 elements λ of full degree. Define κ by (9). Its degree can only be k or k/2, since λ is quadratic over F_q(κ). If it were k/2, Frobenius q^{k/2} would send λ to λ^{−1}, so |λ| would divide q^{k/2}+1. Since k/2 is even this latter number has 2-part two, whereas (q^k−1)_2≥8, a contradiction. Thus κ has degree k. The map λ↦κ has exactly two preimages, λ and λ^{−1}; dividing by k-element Frobenius orbits gives q^k/(8k) factors.

Moreover k is even, so −1 is a square in F_{q^k}, and (9) makes κ a nonzero square. Also

1+κ=4λ/(λ+1)^2.

Maximal order 2-part makes λ a nonsquare in F_{q^k}^×. Taking norms proves (11).

Put e=v_2(q²−1). For a factor of degree j the eigenvalues in (9) lie either in F_{q^j}^× or in its quadratic extension's norm-one subgroup. Their order 2-part is at most max((q^j−1)_2,(q^j+1)_2), which is

2^{e−1} if j is odd,
2^{e+v_2(j)−1} if j is even.

The distinguished factor has 2-part 2^{e+h−1}. Thus every other factor whose degree is not divisible by d has strictly smaller 2-part. It suffices to forbid factor degrees divisible by d in the remainder.

## 6. Squarefree remainder counts in all four determinant sectors

For every r≥8 and every prescribed pair (σ,τ)∈{±1}², at least q^r/16 monic squarefree degree-r polynomials f_0 coprime to X(X+1) satisfy

χ((-1)^r f_0(0))=σ,  χ((-1)^r f_0(−1))=τ.                        (12)

Here is an elementary proof retaining the uniformity at q=3. Let T_r count all monic squarefree degree-r polynomials coprime to X(X+1). We have T_r≥q^r/3. For q≥5 and r≥2, subtract the q^{r−1} nonsquarefree polynomials and at most 2q^{r−1} polynomials with either forbidden root, leaving at least (2/5)q^r. For q=3 the normalized counts have generating function

∑_{r≥0}(T_r/3^r)u^r=(1−u²/3)/[(1−u)(1+u/3)^2],

whose coefficients are

T_r/3^r=3/8+(−1)^r3^{−r}(10−8r)/16≥1/3.

For the three nontrivial sign characters, define ξ on monic polynomials coprime to X(X+1) by one of

ξ(f)=χ(f(0)), χ(f(−1)), χ(f(0)f(−1)),

and set ξ(f)=0 when f is not coprime. For degree r≥2, the map f↦(f(0),f(−1)) has every pair in F_q² equally often, because the two evaluations impose independent linear conditions on the coefficients of a monic polynomial. Thus the sum of each nontrivial ξ over monic degree-r polynomials is zero. In degree one the respective sums are −1, −χ(−1), −1. The last identity is the elementary quadratic-character sum ∑_c χ(c(c−1))=−1. For example it follows by counting solutions of z²=c(c−1), or equivalently (2c−1−2z)(2c−1+2z)=1, which gives q−1 solutions and hence character sum −1.

Consequently each Dirichlet generating function has the form

L(u,ξ)=∑_{f monic}ξ(f)u^{deg f}=1+s u,  s∈{±1}.

The principal character on polynomials coprime to X(X+1) has generating function (1−u)^2/(1−qu). Euler products, valid as formal power series, therefore give the squarefree character sum series

S_ξ(u)=∏_{P irreducible}(1+ξ(P)u^{deg P})
      =L(u,ξ)/L(u²,ξ²)
      =(1+s u)(1−qu²)/(1−u²)^2.                                  (13)

The coefficient of u^{2j} in (1−qu²)/(1−u²)^2 is 1−(q−1)j, and its odd coefficients vanish. For r≥1 the absolute value of the coefficient of u^r in (13) is at most qr/2. Fourier inversion over the four sign pairs now shows that each raw-evaluation sector has at least

(T_r−3qr/2)/4 ≥ q^r/12−3qr/8
                  ≥ q^r/16                                    (14)

members, because 18r≤q^{r−1} for q≥3 and r≥8. Multiplying each target sign by χ((-1)^r) gives (12).

Now suppose r≤a and d≥32(1+log a). The number of monic degree-r polynomials having any irreducible factor of degree divisible by d is at most

∑_{1≤j≤r/d} N(q,jd)q^{r−jd}
 ≤q^r∑_{1≤j≤r/d}1/(jd)
 ≤q^r(1+log a)/d
 ≤q^r/32,                                                       (15)

where N(q,l)≤q^l/l. Subtracting this bound from a prescribed sector in (14) leaves at least q^r/32 squarefree polynomials with that sector and with no factor degree divisible by d. This subtraction is global and thus does not assume independence of the signs and the factor degrees.

## 7. Balance intervals and the uniform bound

Choose the least power of two d with d≥32(1+log a). Then

32(1+log a)≤d<64(1+log a).

For a≥32768, a≥1536(1+log a)>24d. To obtain strength on A, use

[L,U]=[a/3,2a/3].

To obtain strength on B, use instead

[L,U]=[b/3,min(2b/3,5a/6)].

In both cases L≥a/3, U≤5a/6, U−L≥a/6. Every k in the applicable interval makes the negative dimension in (10) lie between one third and two thirds of the selected target's dimension. The integers k=d times odd have spacing 2d, so their number in either interval is at least

(U−L)/(2d)−1 ≥ a/(12d)−1 ≥ a/(24d).                              (16)

For each such k choose a distinguished factor f_* as in Section 5. Set r=a−k≥a/6>8, and choose a remainder f_0 from Section 6 with signs (σ,τ)=(α,−1) and no factor degree divisible by d. Then f=f_* f_0 is squarefree, coprime to X(X+1), and has determinant signs (α,+1), as required by (3). It has exactly one factor of degree divisible by d. Thus distinct choices of k, f_*, and f_0 produce distinct polynomials f, with no overcount.

There are at least q^k/(8k) choices for f_* and q^{a−k}/32 for f_0. Using (16) and k≤a, the number of admissible f is at least

∑_k q^a/(256k) ≥ q^a/(6144d).

Their graph-chart masses are disjoint, and (7) gives

P(strong on the selected eigenspace)
 >1/(49152d)
 >1/[3,145,728(1+log a)].                                         (17)

Since n=a+b≥2a and a≥32768, 1+log a<(4/3)log n. Therefore (17) is greater than

1/(4,194,304 log n)>1/(5,000,000 log n),

as asserted. By Section 1 the same measure applies separately to the originally specified G=O(V), SO(V), or Ω(V).

## 8. What this does and does not establish

The proof addresses the precise marginal even-branch problem in the natural orthogonal representation, with explicit constants and threshold. The small numerical constant is deliberately conservative. It is uniform in q, in the dimensions and discriminants of both t-eigenspaces, in both even-dimensional Witt types, and in odd ambient dimension. It does not transfer a symplectic centralizer formula, suppress determinant sectors, or assume arbitrary O-classes remain intact in Ω.

It does not by itself prove that the generated subgroup contains C_G(t)'', even though the source identifies marginal balance as the main sufficient problem. Such a conclusion still needs a correctly scoped application of class-random generation and a direct-product/subdirect-product argument. Neither all of C_G(t), its second derived subgroup, and its last derived subgroup are being identified without further proof. The source formulation is Cheryl E. Praeger, *Finding strong involutions in finite classical groups in odd characteristic*, OWR 37/2016, printed pp.2160–2161, DOI https://doi.org/10.4171/OWR/2016/37, report https://ems.press/journals/owr/articles/14745 .

The unitary literature is Glasby–Praeger–Roney-Dougal, *Involution centralisers in finite unitary groups of odd characteristic*, J. Algebra 545 (2020), 245–299, DOI https://doi.org/10.1016/j.jalgebra.2019.09.009, inspected preprint https://arxiv.org/abs/1812.01362v2 . Its GL/GU generation theorems are credited, not asserted for orthogonal groups by analogy.
