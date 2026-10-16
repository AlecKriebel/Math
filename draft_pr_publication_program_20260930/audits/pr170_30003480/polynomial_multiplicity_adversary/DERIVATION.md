# Independent derivation: the determinant-involution multiplicity obstruction

This derivation was reconstructed in the algebraic-multiplicity audit family. Its substantive first version was sealed before scientific comparison. It treats the target conclusion as a hypothesis and derives a contradiction from a proposed defining polynomial. The finite checker is supplementary; the statements quantified over all polynomials and all integers n are proved below.

## Claim, assumptions, and success criterion

For a real tensor T in (R^2)^{tensor n}, write M_i(T) for its mode-i flattening and d_i(T)=det(M_i(T)M_i(T)^T). Let G_n be the determinant image of all tensors with Frobenius norm at most one. Define

C_n=[0,1/4]^n,

H_n={d in C_n: d_i <= sum_{j != i} d_j for every i}.

The claim is that, for each integer n>=3 and each B_n in {C_n,H_n}, no real polynomial P in the determinant variables satisfies

G_n={d in B_n:P(d)>=0}.

The polynomial is arbitrary in degree and coefficients. There are no auxiliary variables or quantifiers in this proposed description. The domains include their determinant-zero faces. Establishing local sign obstructions for every polynomial and an exact higher-dimensional slice meets the success criterion. None of this establishes historical novelty.

The primary source's Definition 1.2 specifies the closed norm ball, Theorem 1.3 gives H_n, and Conjecture 1.5 uses C_n. These interpretations were independently checked in Seigal's published paper, printed pages 352–354, and in the OWR report, printed page 1226. The normalized polygon inequality and real three-mode realization are prior results of Higuchi–Sudbery–Szulc; their relevant proof and construction appear on PDF pages 2–3. We give the needed deductions explicitly.

## 1. The normalized eigenvalue constraint

For a normalized nonzero real tensor, every one-mode Gram matrix has trace one. Let lambda_i in [0,1/2] be its smaller eigenvalue. Fix mode 1 and let a=lambda_1. If a=0 there is nothing to prove. Otherwise a real Schmidt decomposition gives

psi=sqrt(a)|0>u+sqrt(1-a)|1>v,

where u and v are orthonormal vectors on the other factors. Real symmetric Gram matrices have orthonormal real eigenbases, including at repeated eigenvalues. On each remaining factor choose the projection P_j onto a smaller-eigenvalue vector. Let N=sum_{j=2}^n P_j on the tensor product, and let w be the product of the complementary eigenvectors. In this product eigenbasis, N is diagonal with integer eigenvalues: zero at w and at least one elsewhere. Thus N>=I-|w><w| as a quadratic-form inequality.

Set p=|<w,u>|^2 and q=|<w,v>|^2. Orthonormality gives p+q<=1. Then

sum_{j=2}^n lambda_j
= a<u,Nu>+(1-a)<v,Nv>
>= a(1-p)+(1-a)(1-q)
= a(2-p-q)+(1-2a)(1-q)
>= a(2-p-q)
>= a.

The inequalities use a<=1/2 and q<=1. Permuting the factors yields lambda_i<=sum_{j != i}lambda_j. This proof handles a=1/2 and all other eigenvalue ties. It applies to real tensors without invoking complex-real sufficiency.

## 2. From a norm ball to trace one in determinant coordinates

Let s=||T||_F^2. For T!=0, 0<s<=1, all mode Gram matrices have trace s, and 0<=d_i<=s^2/4. Their unnormalized smaller eigenvalues are

a_s(d)=(s-sqrt(s^2-4d))/2.

After normalizing T by sqrt(s), the smaller eigenvalues are a_s(d_i)/s. The preceding polygon inequality therefore implies

a_s(d_i)<=sum_{j != i}a_s(d_j).

Define lambda(d)=a_1(d). We prove the necessary determinant-coordinate condition

lambda(d_i)<=sum_{j != i}lambda(d_j).                         (A)

If (A) failed at mode i, monotonicity of lambda on [0,1/4] would force d_i>d_j for every j!=i, and d_i>0. For 0<d_j<d_i and s>2sqrt(d_i), rationalization gives

a_s(d)=2d/(s+sqrt(s^2-4d)),

d/ds log(a_s(d_j)/a_s(d_i))
=1/sqrt(s^2-4d_i)-1/sqrt(s^2-4d_j)>0.

Consequently the ratio sum at any permissible s<=1 is at most the ratio sum at 1, which is less than one by the supposed failure of (A). This contradicts the necessary polygon inequality at s. Terms with d_j=0 are identically zero. At the lower trace endpoint s=2sqrt(d_i), the ratio denominator remains positive and continuity applies. If d_i=1/4, the only permissible trace is s=1, where the contradiction is immediate. The zero tensor has all determinants zero and satisfies (A).

This step is essential: substituting trace one directly for an arbitrary tensor in the ball would be an unjustified normalization. The ratio argument supplies the missing implication. Trace scales quadratically and determinant quartically under tensor scaling, consistently with the formula for a_s.

## 3. Exact real three-mode locus

For t_i in [0,1/2] satisfying the three triangle inequalities, set

w_0=1-(t_1+t_2+t_3)/2,
w_1=(-t_1+t_2+t_3)/2,
w_2=(t_1-t_2+t_3)/2,
w_3=(t_1+t_2-t_3)/2.

The weights are nonnegative and sum to one; w_0>=1/4. The real tensor with amplitudes sqrt(w_0),sqrt(w_1),sqrt(w_2),sqrt(w_3) at 000,011,101,110 and zero elsewhere has norm one. No two support indices differ in exactly one bit, so every mode Gram matrix is diagonal. The probabilities of bit one in the three modes are, respectively,

w_2+w_3=t_1, w_1+w_3=t_2, w_1+w_2=t_3.

Thus the mode eigenvalues are t_i and 1-t_i, and d_i=t_i(1-t_i). The endpoints with zero weights or t_i=1/2 cause no exception. Combined with (A), this proves

G_3={d in C_3:lambda(d_i)<=lambda(d_j)+lambda(d_k) for all i}.

In particular, with D=(0,1/2)^3 and phi(t)_i=t_i(1-t_i), the inverse image of G_3 in D is exactly the closed triangle region intersected with D. The map phi is a diffeomorphism from D onto (0,1/4)^3: each derivative 1-2t_i is strictly positive. The proof only uses this interior inverse, never a diffeomorphism at t_i=1/2.

## 4. Exact multiplicity lemma

Let F be a nonzero real polynomial and L a nonconstant real linear polynomial. If F vanishes on a relatively open subset of the plane L=0, then L divides F. To see this, make an invertible affine coordinate change with first coordinate x=L. The coefficient of x^0 is a polynomial in the plane coordinates; it vanishes on an open set and hence is identically zero.

Because F!=0, there is a finite exact integer multiplicity m>=1 with F=L^m Q and L not dividing Q. The restriction Q|_{L=0} is therefore a nonzero polynomial. It cannot vanish on any relatively open plane patch, so each such patch contains a point p with Q(p)!=0. In a sufficiently small neighborhood of p, Q has a fixed nonzero sign. A transverse line with x=L consequently exhibits the sign behavior of x^m times a nonzero constant.

It follows that a genuine crossing from F>=0 to F<0 requires m odd. Nonnegativity of F on both sides in a full open neighborhood requires m even. Merely knowing that some power of L divides F would not justify either inference: underdividing leaves a residual factor which vanishes on the whole plane.

## 5. The true boundary forces odd multiplicity

Suppose a polynomial P defined G_3 inside either C_3 or H_3. Put

F(t)=P(phi(t)), L=t_1-t_2-t_3.

Consider the open boundary plane patch with t_2=b>0, t_3=c>0, t_1=b+c<1/2. There the other two triangle inequalities have positive margins 2b and 2c. In a small neighborhood, L<0 is feasible and L>0 is infeasible.

This neighborhood can be taken within the domain also for H_3. On the plane, the three determinant-polygon margins are

d_2+d_3-d_1=2bc,
d_1+d_3-d_2=2c(1-b-c),
d_1+d_2-d_3=2b(1-b-c),

all strictly positive. All determinant coordinates are strictly inside their cube intervals. Continuity supplies full neighborhoods contained in H_3.

Therefore F>=0 on the feasible side and F<0 on the infeasible side. Limits from each side give F=0 on the patch. F is not the zero polynomial: t=(5/16,1/8,1/8) violates the first triangle inequality, yet phi(t)=(55/256,28/256,28/256) is strictly inside H_3, its first determinant margin being 1/256 and the other two 55/256. At this point the proposed defining property forces F<0.

Apply the exact multiplicity lemma. Write F=L^m Q with Q not divisible by L. Choose a boundary-patch point with Q nonzero. The two signs forced by feasibility imply m odd. This selection is justified by a polynomial identity on an open plane patch, not by an assumption that every boundary point is generic.

## 6. The determinant involution forces the same exact multiplicity inside

The substitution t_1 -> 1-t_1 fixes t_1(1-t_1), hence the ring automorphism tau(t)=(1-t_1,t_2,t_3) fixes F. It sends L to -L', where

L'=t_1+t_2+t_3-1.

Applying tau to F=L^m Q gives

F=(-L')^m tau(Q).

The multiplicity of L' is exactly m. Indeed, if L' divided tau(Q), applying tau again and using tau(L')=-L would imply that L divided Q, a contradiction. This explicitly supplies exactness under the automorphism.

The plane L'=0 passes through (1/3,1/3,1/3). Its nearby plane patch lies inside D and inside all three strict triangle inequalities, since on that plane their margins are 1-2t_i>0. It also maps into the interior of H_3, because on sum t_i=1 its determinant-polygon margins are 2t_jt_k>0. A full small neighborhood therefore consists of feasible points in the relevant domain, and F is nonnegative throughout it.

The residual after division by (L')^m restricts nontrivially to L'=0 by exactness. Choose a point of the open interior plane patch where it is nonzero. The multiplicity lemma gives m even. This contradicts the odd multiplicity from the true boundary.

The reflection need not preserve D. Only its algebraic action on F and on plane factors is used. The argument does not pretend that the reflected image of the original boundary patch itself is the chosen interior patch.

Thus no polynomial defines G_3 by nonnegativity inside C_3 or H_3.

## 7. Exact zero-determinant faces give every n>=3

For a real matrix M, rank(MM^T)=rank(M). Consequently a nonzero real tensor with d_i=0 has mode-i flattening rank one, so it factors as S tensor u in that mode. Choose u to have norm one, absorbing the original norm into S. Then ||S||_F=||T||_F. For every remaining mode, each Gram entry is an inner product over the other factors, and the contraction over u contributes <u,u>=1. Thus every remaining mode Gram matrix is unchanged.

Iterating through modes 4,...,n proves

G_n intersect {d_4=...=d_n=0}=G_3 times {0}^{n-3}.

The zero tensor is immediate. Conversely, adjoining arbitrary real unit-vector factors to a three-mode tensor preserves its norm and the first three Gram matrices and makes all new determinants zero. This proves both inclusions. Iteration is valid because determinants of the factors not yet removed remain unchanged.

For B_n=C_n its intersection with this face is C_3 times zero. For B_n=H_n, the first three inequalities reduce exactly to H_3; each additional inequality is 0<=d_1+d_2+d_3. Hence the face is H_3 times zero.

If P_n defined G_n inside B_n, then P_3(d_1,d_2,d_3)=P_n(d_1,d_2,d_3,0,...,0) would define G_3 inside B_3. An identically zero restriction would include the infeasible point (55/256,28/256,28/256), so it cannot evade the contradiction. Section 6 rules out every other restriction. This proves the exact full quantified claim for all integers n>=3.

## 8. Boundary cases and limits of this result

For n=2, both determinants equal det(T)^2 and every value in [0,1/4] is attained by a norm-one diagonal matrix. The diagonal segment is defined inside C_2 by -(d_1-d_2)^2>=0. For n=1 the sole flattening has rank at most one, so d_1=0 and -d_1^2>=0 works. The threshold n>=3 is therefore essential.

The argument covers trace zero, determinant zeros, trace-discriminant endpoints, and eigenvalue ties. Local crossings occur with every t coordinate strictly between zero and one half and every determinant strictly between zero and one quarter. The higher-mode extension uses a closed zero-determinant face. It does not establish an obstruction for a differently posed punctured higher-mode domain, arbitrary fixed rank, unnormalized tensors, auxiliary quantified variables, or several inequalities.

Dropping determinant-only coordinates changes the problem: in nonnegative t coordinates the polynomial

-(t_1-t_2-t_3)(t_2-t_1-t_3)(t_3-t_1-t_2)

has nonnegative sign exactly on the triangle region. At most one triangle inequality can fail, giving this sign property. But this polynomial lacks the coordinate involution invariance necessary for any P(phi(t)), and cannot be used as the requested determinant polynomial. The negative checker explicitly detects this mutation.

## 9. Checkable supplementary artifacts

The standard-library-only checker retains exact rational polynomial arithmetic, exact coordinate substitutions and multiplicities, symbolic parity-weight and H-margin identities, a concrete rational tensor and rank-one embeddings, and rational local crossings. It tests twelve deliberately false variants. Every condition uses explicit exceptions, and the same checks pass with optimization enabled. These tests do not replace the exact multiplicity lemma, the polynomial identity arguments, or the all-n factorization proof.

No unsupported equivalent problem has been substituted for the central claim. The strongest verified result is the full determinant-only single-polynomial nonexistence theorem above. No mathematical gap remains within this claim and these domains.
