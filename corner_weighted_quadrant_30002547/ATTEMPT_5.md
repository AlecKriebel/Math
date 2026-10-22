# Attempt 5: exact transition-point radius and critical value

## Result and scope

This attempt resolves the transition parameter a=−1/2, without coefficient positivity assumptions:

    rho_Q(−1/2) = 1/9,
    lim_{u ↑ 1/9} Q(−1/2,u) = 3/2,
    lim_{u ↑ 1/9} (d/du)Q(−1/2,u) = +infinity.

The value is a one-sided Abel limit. The proof below does not assert ordinary convergence of the signed series at its radius, nor any full coefficient asymptotic.

It also gives an exact Hilbert-space projection formula for the finite critical Abel value on the whole lower branch −1<=a<=−1/2. This does not yet establish the radius equality at the other negative parameters (except the previously known a=−1 endpoint).

## 1. Exact square factorization

Use the notation and independently proved operator identity from Attempt 2. On H=ell²(N_0²), U and V are the forward unilateral coordinate shifts, delta=e_(0,0),

    A=U+U*+V+V*,  B=U*V+UV*,  c=1−a,
    K(t)=I−tA+c t²B,
    q(t)=Q(a,t²)=<delta,K(t)^(-1)delta>.

Let C=U+V. Since U*U=V*V=I,

    C*C=2I+B.

For c>0 and t>0, exact expansion gives

    K(t)=c t²(C−alpha I)*(C−alpha I)+eta(t)I,
    alpha=1/(ct),  eta(t)=1−1/c−2ct².                 (1)

On the conjectured lower branch c∈[3/2,2], put

    t_*=sqrt((c−1)/(2c²)),
    alpha_*=1/(ct_*)=sqrt(2/(c−1)) ∈ [sqrt(2),2],
    d=ct_*².

Then eta(t_*)=0, and the critical operator is

    K_*=d T*T,  T=C−alpha_* I.                       (2)

The operator T is injective. For example, identify ell²(N_0²) with the bidisk Hardy space using e_(i,j)↔z^i w^j. T is multiplication by z+w−alpha_*, and multiplication by a nonzero polynomial is injective on analytic functions. One can also verify this directly from the coefficient recurrence and the least nonzero total degree.

## 2. The critical Abel limit as a projection norm

Attempt 2 proved that K(t)>0 for 0<t<t_*, that K_*>=0, and that

    q_* := lim_{t ↑ t_*}q(t)
         = lim_{epsilon ↓0}<delta,(K_*+epsilon I)^(-1)delta>

exists and is finite. The standard positive-operator variational formula gives

    q_* = sup_{f !=0} |<delta,f>|² / <f,K_* f>.

For completeness, the formula follows by applying Cauchy–Schwarz in the K_*+epsilon inner product, where the maximizing vector is its inverse applied to delta, then letting epsilon decrease to zero. The same supremum can be taken over finitely supported f because they are dense and T is bounded.

Let M=closure ran(T). For h=Tf, the constant coefficient is

    h_(0,0)=−alpha_* f_(0,0),

because C raises total degree. Inserting (2) into the variational formula and substituting h=Tf yields

    q_* = (1/(d alpha_*²))
          sup_{0 != h in ran(T)} |<delta,h>|² / ||h||²
         = c ||P_M delta||².                       (3)

Here P_M is orthogonal projection onto M; the last step uses d alpha_*²=1/c and continuity of the Rayleigh quotient under closure. Equivalently,

    q_* = c[1−||P_{ker(C*−alpha_* I)}delta||²].      (4)

This is an exact formula, not an inference from the full-plane symbol.

If alpha_*<2, set r=alpha_*/2∈(0,1). The nonzero square-summable vector g_(i,j)=r^(i+j) satisfies C*g=2rg=alpha_*g, and <delta,g>=1. Thus delta has a nonzero projection onto that kernel, and

    0<q_*<c  for 3/2<c<=2.                         (5)

At alpha_*=2 the kernel vanishes, as proved next. That endpoint has an explicit value.

## 3. No backward-shift eigenvector at eigenvalue 2

**Lemma.** ker(C*−2I)={0}.

Suppose C*f=2f. Since both U* and V* are contractions,

    2||f|| = ||U*f+V*f|| <= ||U*f||+||V*f|| <= 2||f||.

Every inequality is an equality. Equality in the Hilbert-space triangle inequality, together with the norm equalities and U*f+V*f=2f, forces U*f=V*f=f. But U*f=f implies f_(i+1,j)=f_(i,j) for every i,j. Square summability then forces every coefficient to vanish. This proves the lemma.

Consequently closure ran(C−2I)=H. Formula (3), at c=3/2 and t_*=1/3, therefore gives

    lim_{t ↑ 1/3}q(t)=3/2.                         (6)

## 4. The origin is not in the range of the critical operator

At this transition,

    K_*=(1/6)(C−2I)*(C−2I).                        (7)

**Lemma.** There is no f∈H satisfying K_*f=delta.

Assume otherwise and put g=(C−2I)f. Equation (7) would imply

    (C*−2I)g=6delta.

Because (C*−2I)delta=−2delta, the vector −3delta is one solution of this last equation. The preceding lemma shows it is the unique solution. Hence

    (C−2I)f=−3delta.                               (8)

The coefficient recurrence in (8) has the unique formal solution

    f=(3/2) sum_{n>=0} (C/2)^n delta.               (9)

This statement is coefficientwise: C raises total degree, so each coefficient uses only one term, and the constant coefficient in (8) fixes f_(0,0)=3/2. No convergence of the operator series has been assumed.

The homogeneous vectors C^n delta have mutually disjoint total-degree supports, and

    ||C^n delta||² = sum_{j=0}^n binom(n,j)² = binom(2n,n).

Therefore the formal solution's squared norm is

    (9/4) sum_{n>=0} binom(2n,n)/4^n,

which diverges. For an elementary bound, the central binomial coefficient is the largest of the 2n+1 coefficients whose sum is 4^n, so binom(2n,n)/4^n >=1/(2n+1). Thus (9) is not in H, contradicting the assumed solution. ∎

In particular,

    ||K(t)^(-1)delta|| -> infinity as t ↑ 1/3.      (10)

Indeed, if a sequence of these vectors stayed bounded, weak compactness would give a weakly convergent subsequence f_j→f. Since K(t_j)→K_* in operator norm and K(t_j)f_j=delta, testing against arbitrary vectors would imply K_*f=delta, contrary to the lemma. This rules out every bounded subsequence, proving the full limit in (10).

## 5. Divergent derivative and radius equality

For real 0<t<1/3, put f_t=K(t)^(-1)delta. Differentiate the bounded inverse:

    q'(t)=<f_t,(A−2ctB)f_t>.

Since K(t)=I−tA+ct²B,

    A−2ctB = (I−ct²B−K(t))/t.

Consequently

    q'(t)=(1/t)<f_t,(I−ct²B)f_t>−q(t)/t
          >=[(1−2ct²)/t]||f_t||²−q(t)/t,           (11)

using ||B||<=2. At c=3/2 and t=1/3, the first scalar numerator tends to 2/3>0. Equation (6) bounds q(t), whereas (10) makes the squared norm diverge. Thus

    q'(t) -> +infinity as t ↑ 1/3.

Since q'(t)=2t (d/du)Q(−1/2,t²), the derivative in the half-length variable also diverges at u=1/9. The scalar function cannot be holomorphic through that point.

Attempt 2 already proved holomorphy for |u|<1/9. The lower and upper radius bounds therefore coincide:

    rho_Q(−1/2)=1/9.

This is genuine scalar threshold detection, unlike merely exhibiting a Weyl sequence for the full operator.

## 6. What remains, and why the proof does not extend automatically

For 3/2<c<=2, the critical kernel ker(C*−alpha_* I) is nontrivial. In the range argument above, solutions of T*g=delta are no longer unique. One cannot replace g by the particular constant vector and conclude that division by z+w−alpha_* fails in H. The orthogonal projection in (4) is exactly the missing correction. In fact the known a=−1 endpoint has a finite first derivative, so a proof claiming the same first-derivative divergence for the whole lower branch would be false.

For 1<c<3/2, corresponding to −1/2<a<0, the critical operator is not a pure square with zero scalar remainder. If alpha_*=1/(ct_*)>2 and d=ct_*², exact algebra instead gives

    K_* = d[(alpha_*−2)(4I−A)+(C−2I)*(C−2I)].      (12)

The contraction bound ||C/2||<=1 gives

    (C−2I)*(C−2I) <= 2(4I−A),

so

    d(alpha_*−2)(4I−A) <= K_* <= d alpha_*(4I−A).   (13)

This comparison shows a uniformly elliptic low-energy form in this open parameter range. It does not by itself identify the origin spectral density or justify comparison of higher inverse powers of noncommuting operators. Hence it does not establish scalar nonanalyticity.

The full all-parameter radius question remains unresolved by these arguments on the two open intervals (−1,−1/2) and (−1/2,0). The previously proved a=−1 case, the present transition-point proof, and Attempt 1's a>=0 theorem must not be substituted for the missing intervals.

## Public reference

Michael Albert and Mireille Bousquet-Mélou, *Permutations sortable by two stacks in parallel and quarter plane walks*, Conjecture 11, https://arxiv.org/abs/1312.4487. The operator contraction and real/complex disk bounds used here are fully proved in the accompanying authored Attempt 2. No priority claim is made about these partial results or the transition-point value.
