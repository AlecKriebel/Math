# Bounded starlike third coefficients: verified partial results

## Target and status

For M>1 let S*(M) consist of holomorphic, injective functions on the unit disk D, normalized by f(0)=0 and f'(0)=1, whose image is starlike about 0 and contained in {|w|≤M}. Write f(z)=z+a2 z²+a3 z³+… and B(M)=sup |a3| over this class. The target is the exact function B(M) throughout e<M<5 (Hayman–Lingham Problem 6.65; UnsolvedMath 2306065).

**This package does not solve that target.** Its main certified quantitative statement is

    1134162229/1250000000 ≤ B(3) < 957/1000.

The left endpoint is 0.9073297832. Neither endpoint is claimed sharp. The failure of the simpler proposed formula max(1−M⁻², 3−8/M+5/M²) was already found by Pearce; we do not claim a new disproof. No novelty is claimed for the bounds or mechanisms below.

## 1. Analytic coordinates and compactness

For f∈S*(M), the nonvanishing holomorphic function f(z)/z has a unique logarithm g with g(0)=0. Put

    g(z)=Σ(n≥1) c_n z^n,  p(z)=1+zg'(z).

The starlike criterion says Re p>0. Also |f(z)/z|≤M: apply Schwarz's lemma to f/M. Consequently Re g≤L=log M. Conversely, if holomorphic g(0)=0 satisfies Re(1+zg')>0 and Re g≤L, then f=z exp g is normalized and starlike univalent and |f(z)|≤M|z|<M. Thus these two real-part constraints are an exact characterization, not a relaxation. The coefficient identity is

    a2=c1,       a3=c2+c1²/2.                         (1)

By the Herglotz representation for p, |n c_n|≤2, hence |c_n|≤2/n. Explicitly, p(z)=∫(1+ζz)/(1−ζz) dμ(ζ), for a probability measure μ on the circle, and c_n=(2/n)∫ζ^n dμ. The extra boundedness condition is

    −2∫ log|1−ζz| dμ(ζ) ≤ log M   for every z∈D.    (2)

It cannot be discarded. Every finite atomic μ with positive mass at some ζ has a logarithmic blow-up as z approaches conjugate ζ, so no such μ gives a bounded f. Finite-atomic unrestricted Herglotz extremizers are therefore inadmissible for finite M.

The class S*(M) is compact for local uniform convergence. Montel gives subsequences; f'(0)=1 excludes a constant limit. Hurwitz preserves injectivity and the absence of nonzero zeros. The functions p converge locally, and the minimum principle upgrades Re p≥0 to Re p>0 because p(0)=1. The bound passes to the limit. Coefficient evaluation is continuous, so B(M) is attained.

Rotations f(z)↦e^(−iθ)f(e^(iθ)z) preserve the class and rotate a3 by e^(2iθ); hence B(M)=max Re a3. Moreover it suffices to use real c_n and c1≥0. After rotating a3 to be nonnegative real, replace g by

    g_R(z)=(g(z)+overline(g(overline z)))/2.

Both real-part constraints are preserved. If c1=x+iy, the new a3 is the old real a3 plus y²/2. Finally z↦−z changes the sign of c1 and preserves a3. This is the classical symmetrization used by Barnard (1975, Lemma 2); the displayed computation fixes its role in the certificates.

## 2. Explicit competitors, and why their envelope is insufficient

Let k(w)=w/(1−w)². The normalized Pick function F_M is specified by

    k(F_M(z)/M)=k(z)/M.

The branch at zero maps D to the radius-M disk with a radial slit on the negative real axis. This follows either from the usual Koebe slit-map construction or Barnard–Lewis (1975). Substitution of F_M=z+A2 z²+A3 z³+… gives

    A2=2(1−1/M),       A3=3−8/M+5/M².              (3)

The normalized analytic square root H_M(z)=sqrt(F_(M²)(z²)) is also bounded starlike: its logarithmic derivative is p_(M²)(z²), of positive real part; its modulus is at most M. Its third coefficient is 1−M⁻². Therefore

    B(M)≥max(1−M⁻²,3−8/M+5/M²).                    (4)

Their difference is 2(M−1)(M−3)/M², so the competitors tie at M=3 with value 8/9. Section 5 gives a strictly better admissible function at that same M. This refutes any proof that simply takes their envelope, but does not identify the true extremizer.

## 3. A strict, nonsharp upper bound throughout the target interval

We use one explicit literature dependency: Barnard–Lewis's subordination theorem states that log(f(z)/z) is subordinate to log(F_M(z)/z). Exponentiating, there is a holomorphic disk self-map ω with ω(0)=0 such that

    f(z)/z = F_M(ω(z))/ω(z).

Write ω(z)=u z+v z²+… . Schwarz–Pick applied to ω(z)/z gives |v|≤1−|u|². Comparing coefficients gives a2=A2 u and a3=A2 v+A3 u². For e<M<5, 0<A3<A2, since A2−A3=(M−1)(5−M)/M². Thus

    |a3|≤A2−(A2−A3)|u|²≤A2.                       (5)

Equality would force u=0 and |v|=1, hence ω(z)=ηz² with |η|=1 by the equality case of Schwarz's lemma. The resulting relaxed extremizer has logarithmic derivative

    zf'(z)/f(z)=2p_M(ηz²)−1.

Along ηz²=−r with r increasing to 1, p_M(−r) tends to 0. Indeed k'(−1)=0, while F_M(−1)/M lies strictly between −1 and 0 and k' there is nonzero; differentiate the defining equation for F_M. Consequently the displayed derivative has negative real part for r sufficiently close to 1. This relaxed extremizer is not starlike.

Compactness from Section 1 excludes equality at the actual maximum, proving

    B(M)<2(1−1/M),           e<M<5.                (6)

The argument also yields |a2|≤2(1−1/M), used below at M=3. It does not quantify the strict gap in (6).

## 4. Finite positivity gives rigorous outer certificates

For a real-coefficient admissible g and any positive integer N, Fejér averaging of the nonnegative harmonic functions Re p and L−Re g gives, for every real θ,

    1+Σ(n=1..N) w_n n c_n cos(nθ) ≥0,
    L−Σ(n=1..N) w_n c_n cos(nθ) ≥0,
    w_n=1−n/(N+1).                               (7)

For completeness, apply the nonnegative Fejér kernel to these harmonic functions on |z|=r, then let r tend to 1; the finite sums converge. No boundary continuity assumption on f is needed. Finitely many choices of θ produce necessary linear inequalities; they are not sufficient for admissibility.

We use N=40 and the 201 rational points x=j/100, −100≤j≤100. Let T_n be the Chebyshev polynomials, T_n(cos θ)=cos(nθ). At M=3, put U=1098613/1000000. Exact Taylor arithmetic proves exp U>3, hence L<U. Therefore every admissible real coefficient vector obeys

    −Σ w_n n c_n T_n(x) ≤1,
     Σ w_n c_n T_n(x) ≤U,       |c_n|≤2/n.         (8)

From Section 3, 0≤c1≤4/3. Partition this interval into K=64 slabs [l,h], where l=4k/(3K), h=4(k+1)/(3K). On each slab,

    c2+c1²/2 ≤ c2+(l+h)c1/2−lh/2.                (9)

This is just (c1−l)(c1−h)≤0. The right side is linear in the coefficient vector, apart from the fixed constant.

UPPER_CERTIFICATE.json records nonnegative rational multipliers for the inequalities (8) and for the coordinate bounds in each slab. Denote the weighted sum of left sides by d·c, its rational right side by R, and the linear objective vector in (9) by t=((l+h)/2,1,0,…,0). Then, without any requirement that a rounded dual be exactly feasible,

    t·c−lh/2 ≤ R+Σ(n=1..N) (2/n)|t_n−d_n|−lh/2. (10)

This follows directly from |c_n|≤2/n. The absolute residual term makes decimal rounding of the multipliers harmless. verify_upper.py builds every T_n and multiplier as a Python Fraction, checks multiplier nonnegativity and all 64 slabs, and verifies that every right side in (10) is strictly below 957/1000. The worst certified bound is approximately 0.956240484. Thus B(3)<0.957 follows for the entire analytic class, not just for polynomials or a sampled family of functions.

A floating-point optimizer was used only to discover suitable duals. It is not used by the certificate verifier. The exact verifier also proves U>log 3 using the positive Taylor sum of exp U through degree 30, which already exceeds 3.

## 5. An exact admissible witness exceeding the old envelope

WITNESS.json specifies 40 rational numbers c_n, all with denominator 10^9, and

    g(z)=Σ(n=1..40)c_n z^n,        f(z)=z exp g(z).

Let L0=549/500 and define real polynomials

    P(x)=1+Σ n c_n T_n(x),       Q(x)=L0−Σ c_n T_n(x).

verify_witness.py proves P(x)>0 and Q(x)>0 on the entire interval [−1,1], using exact rational Bernstein coefficients and dyadic subdivision. Here is the complete certification principle. Substitute x=2t−1 and express a degree-d polynomial as Σ b_k C(d,k)t^k(1−t)^(d−k). On [0,1] these basis polynomials are nonnegative and sum to 1, so the polynomial is at least min b_k. De Casteljau subdivision at t=1/2 gives exact Bernstein coefficients on the two half intervals. The verifier subdivides only where necessary, and accepts a cell only when every coefficient is strictly positive. Its terminal cells partition [0,1]. The actual certificates require 14 cells for P (maximum depth 8) and 7 for Q (maximum depth 4).

It follows that Re(1+zg')>0 and Re g<L0 on the unit circle. The harmonic minimum/maximum principles extend these inequalities to the closed disk. Thus the standard starlike criterion makes f normalized, injective, and starlike; also |f(z)|≤|z| exp L0<3. The last strict inequality is proved rationally by the Taylor series through degree 30, bounding the positive tail by

    (L0^31/31!)/(1−L0/32).

The ratio of each term after the first omitted term to its predecessor is at most L0/32, so this is a valid geometric tail bound. The verified upper estimate for exp L0 is below 3.

Finally, direct exact substitution into (1) gives

    a3=1134162229/1250000000 > 9/10 > 8/9.

This proves the stated lower bound and a checkable instance of the historical counterexample. There are no sampled-angle or floating-point assumptions in this proof.

## 6. The remaining sharp extremal problem

Barnard (1975, Theorem 1) reduces the sharp problem to normalized maps onto a disk with at most two equal-length, real-axis-symmetric radial slits. For prevertex parameters a≥b≥c in [−1,1], an interior double-slit candidate has

    p(z)=(1−2bz+z²)/sqrt((1−2az+z²)(1−2cz+z²)),

where the analytic square root equals 1 at zero. With S=a+c,

    q1=S−2b,
    q2=(3/2)S²−2bS−2ac,
    a3=(q1²+q2)/2.                              (11)

Matching the two circular boundary arcs to radius M requires

    ∫_0^1 (p(t)−1)/t dt = log M,
    ∫_0^1 (p(−t)−1)/t dt = log M.               (12)

The coefficients in (11) are verified algebraically in verify_algebra.py. The parametric description is a known reduction, not a solution. Our floating-point constrained search near M=3 gives approximately 0.91419512, consistent with Pearce's published numerical evidence. It is not an exact lower bound, upper bound, or uniqueness certificate. At larger M the artificial cutoff c≥−0.999999 yields values below even the known Pick competitor, exposing its failure as a global optimization procedure. SLIT_PROBE.json preserves that negative control rather than concealing it.

What remains is a sharp global optimization with all admissibility constraints and endpoint degeneracies proved, or a different analytic argument giving the exact B(M) for every e<M<5 and showing attainment. Finite necessary inequalities, a certified competitor, and an unvalidated local slit maximum do not supply that missing proof.

## References and dependency boundary

- W. K. Hayman and E. F. Lingham, Research Problems in Function Theory, arXiv:1809.07200v2, printed p.141, Problem/Update 6.65: https://arxiv.org/abs/1809.07200v2
- R. W. Barnard and J. L. Lewis, Coefficient bounds for some classes of starlike functions, Pacific J. Math. 56(2) (1975), 325–331, especially Theorem A and p.326: https://msp.org/pjm/1975/56-2/pjm-v56-n2-p04-p.pdf
- R. W. Barnard, A variational technique for bounded starlike functions, Canadian J. Math. 27(2) (1975), 337–347, equations (10)–(12), Lemma 2 and Theorem 1: https://doi.org/10.4153/CJM-1975-041-x
- K. Pearce, A constructive method for numerically computing conformal mappings for gearlike domains, SIAM J. Sci. Stat. Comput. 12(2) (1991), 231–246; author manuscript application section, pp.21–23: https://www.math.ttu.edu/~pearce/papers/gearlike.pdf and https://doi.org/10.1137/0912013

Standard analytic dependencies are Schwarz/Schwarz–Pick, Montel/Hurwitz, the harmonic maximum principle, the starlike logarithmic-derivative criterion, Herglotz representation, and Fejér-kernel positivity. The Barnard–Lewis subordination theorem is explicitly external. Exact scripts certify their encoded algebra and finite inequalities; they do not mechanically formalize these analytic theorems or establish novelty.
