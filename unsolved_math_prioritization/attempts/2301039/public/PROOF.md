# Function Theory Problem 1.39: exact reductions and construction obstructions

**Problem:** 2301039 / AMR-022-1039, queue rank 564.  
**Disposition:** partial work only; neither sharp constant is determined.  
**Date:** 4 October 2026 UTC.  
**Credit:** The question is due to L. R. Sons. Historical bounds are due to D. F. Shea and L. R. Sons. The reductions and exclusions below carry no novelty or priority claim. This is AI-assisted, unrefereed work, not a formally verified proof.

## 1. Target and conventions

Write D={z:|z|<1}, L(r)=log(1/(1-r)), and

    alpha(f) = limsup_{r→1-} T(r,f)/L(r).

Here T=m+N is the usual Nevanlinna characteristic, counting poles with multiplicity; the contribution of a pole of order m at 0 to N is m log r. The target is restricted to finite alpha. Part (a) asks whether the bound 2 is sharp for holomorphic, zero-free f with f′(z)≠1 throughout D. Part (b) asks for the sharp bound for zero-free meromorphic f with the same derivative omission; its historical upper bound is 7. At a pole, f′ is infinite and hence is not 1. Nonzero constants cause no difficulty and have alpha=0.

The exact question and the reporting update were checked in Hayman–Lingham, arXiv:1809.07200v2, printed p.19. The two historical bounds are reported here as attribution, not re-proved or used as dependencies of our propositions. The original 1986 article could not be retrieved; see SOURCE_GATE.md.

Every theorem below concerns an explicitly stated reformulation or subclass. No theorem below asserts that all admissible functions have alpha=0, nor that either historical constant is sharp.

## 2. Reciprocal reduction, including every pole multiplicity

**Proposition 1.** There is a bijection between zero-free meromorphic functions f on D and non-identically-zero holomorphic functions u on D, given by u=1/f. Under this bijection, f′ omits 1 precisely when

    R = u′ + u²

is not identically zero and has zero divisor consisting of the zeros p of u, with multiplicity ord_p(u)-1. Zeros of u of order 1 therefore do not appear in this divisor. In particular, when f is holomorphic, both u and R must be zero-free. Moreover alpha(f)=alpha(u).

**Proof.** A pole of f becomes a removable singularity and then a zero of 1/f, while the zero-free assumption prevents any pole of u. The converse is immediate. Away from zeros of u,

    f′-1 = -(u′+u²)/u².

At a zero p of u of order m≥1, write u(z)=a(z-p)^m+O((z-p)^(m+1)), a≠0. Then u′+u²=m a(z-p)^(m-1)+O((z-p)^m). Thus the forced vanishing order is exactly m-1. Any other zero of R would give f′=1 at a nonpole, and conversely.

For the growth assertion, write u(z)=c z^k+O(z^(k+1)), c≠0, at the origin. Jensen's formula gives

    mean log|u(re^(iθ))| = log|c| + N(r,0,u).

Since log^+|u|-log^+|1/u|=log|u| and N(r,∞,f)=N(r,0,u),

    T(r,f)=m(r,u)-log|c|=T(r,u)-log|c|.

This identity extends through radii containing zeros by continuity of the circular means. Division by L(r) proves the claim. □

**Multiple-pole control.** For any integer m≥1, let f(z)=2/(m z^m). It is admissible in part (b): |f′(z)|=2/|z|^(m+1)>2 at every nonpole. Its reciprocal is u=(m/2)z^m, and

    u′+u²=(m²/4)z^(m-1)(2+z^(m+1)).

There are no extra zeros in D. For m>1 this R does vanish at the origin. Consequently, imposing R≠0 everywhere in the meromorphic case would discard valid functions and would change the problem. All these controls have alpha=0.

## 3. Two exact differential parametrizations

### 3.1 A zero-free function and its first two derivatives

**Proposition 2.** Every admissible f has a representation

    F(z)=exp(∫_0^z (1/f)(ζ) dζ),   f=F/F′,

where F is holomorphic and zero-free. The integral is single-valued because 1/f is holomorphic on the simply connected disk. F′ is not identically zero. All zeros of F″ are zeros of F′, and a zero of F′ of order m has order m-1 in F″.

Conversely, any zero-free holomorphic F with F′ not identically zero and F″ having no zeros outside the zeros of F′ produces an admissible meromorphic f=F/F′. Part (a) is exactly the subcase F, F′, F″ all zero-free. In either direction the characteristic to optimize is that of F′/F, not that of F.

**Proof.** Put u=1/f. Then F′=uF and F″=(u′+u²)F, so Proposition 1 gives the forward statement. Conversely, at a zero of F′ of order m, the nonzero numerator F gives a pole of f of order m. Elsewhere,

    f′ = 1 - F F″/(F′)².

The stated zero exclusion makes f′≠1. Differentiation gives the forced order m-1 of F″ at a zero of F′. The identity f=1/(F′/F) and Proposition 1 give the growth assertion. □

This transformation does not establish a growth bound: controlling the growth of F itself is a different assertion, and no universal estimate sufficient to optimize T(F′/F) is proved here.

### 3.2 A linear equation with an omitted primitive

**Proposition 3.** Let q be a zero-free meromorphic function on D whose poles are simple and whose residue at each pole p is -m_p, with m_p a positive integer. There is a zero-free meromorphic H with H′/H=q, having a pole of order m_p at p. Its reciprocal is holomorphic. Choose a primitive J of 1/H. For any constant C such that -C∉J(D),

    f=H(C+J)

is zero-free meromorphic, satisfies f′-qf=1, and has f′≠1. Every admissible f is obtained in this way. If q has no poles, the resulting f is holomorphic.

**Proof.** On the disk minus the poles, exponentiate a path integral of q. A closed path has integral 2πi times the sum of its winding numbers times the integer residues, by the residue theorem; only finitely many poles meet the compact region relevant to the path. Hence its exponential is single-valued. Near p the integral is -m_p log(z-p) plus a holomorphic function, so H has a pole of exactly that order. There are no zeros. The primitive J exists on D because 1/H is holomorphic.

Differentiating H(C+J) gives f′=qf+1. At an ordinary point, f is nonzero exactly when C+J is. At a pole p of H, J′ has a zero of order m_p. If C+J(p)=0, then C+J has a zero of order m_p+1, and f has a zero of order 1. If C+J(p)≠0, f has a pole of order m_p. Thus f is zero-free exactly when -C is omitted by J. In that case qf is zero-free meromorphic, so f′-1 never vanishes.

Conversely, given admissible f put q=(f′-1)/f. Away from poles of f it is holomorphic and zero-free. At a pole p of f of order m,

    q=f′/f-1/f=-m/(z-p)+holomorphic terms.

Thus q has exactly the required poles. Build H as above. The quotient f/H extends holomorphically and nonvanishingly through each pole, and its derivative is 1/H. Hence f/H=C+J, with the required omission. □

The unresolved construction step in this parametrization is to make a primitive J omit a value while the resulting H(C+J) has positive logarithmic characteristic of the required size. Prescribing a zero-free q alone does not verify that step.

## 4. Bounded-characteristic constructions cannot certify sharpness

**Proposition 4.** If f=g/h with bounded holomorphic g,h on D and h not identically zero, then T(r,f)=O(1) as r→1 and alpha(f)=0. In particular every rational function, including any with boundary poles, has alpha=0 on D.

**Proof.** Poles of f are a sub-divisor of zeros of h. Write h(z)=c z^k+O(z^(k+1)), c≠0. The elementary product bound for proximity functions and Jensen's formula give

    T(r,g/h) ≤ m(r,g)+m(r,1/h)+N(r,0,h)
             = m(r,g)+m(r,h)-log|c|.

Both means on the right are bounded. The possible pole contributions at the origin in the sub-divisor comparison need only an O(1) correction for r≥1/2 if cancellations occur there; this does not affect boundedness. For a rational function write it as a quotient of polynomials, which are bounded on D. □

Large pointwise boundary values do not contradict this conclusion. For example, for real a>0 and real b with (a/2)e^b>1,

    f(z)=exp(a(1+z)/(1-z)+b)

is zero-free and satisfies |f′|>1, yet alpha=0, as proved below. An arbitrarily severe exponential blow-up at one boundary point is therefore not a positive-alpha witness.

## 5. Complete exclusion of polynomial exponential Cayley models

Let W(z)=(1+z)/(1-z), a biholomorphism D→{Re w>0}.

**Theorem 5.** For f(z)=exp(P(W(z))), where P is a complex polynomial:

1. If deg P≥2, alpha(f)=+∞.
2. If P(w)=aw+b, then

       T(r,f) = |Im a|/π · log((1+r)/(1-r)) + O(1),
       alpha(f)=|Im a|/π.

3. If Im a≠0, f′ assumes 1 infinitely often in D.

Consequently every member of this polynomial-exponential family satisfying the hypotheses of either part of Problem 1.39 has alpha=0.

**Proof of (1).** Set t=1-r and θ=ty, with y in a fixed bounded real interval. Uniformly on that interval,

    t W(r exp(ity)) → 2/(1-iy).

If P has degree d≥2 and leading coefficient c≠0, then

    t^d Re P(W(r exp(ity))) → Re[c(2/(1-iy))^d].

As y runs through R, the argument of (1-iy)^(-1) runs through (-π/2,π/2). For d≥2, the real part on the right is strictly positive somewhere. Indeed, an interval of arguments of length at least 2π cannot have its cosine everywhere nonpositive. There is therefore a finite closed y-interval I and κ>0 on which it is at least 2κ. Uniform convergence gives Re P(W)≥κt^(-d) on the corresponding θ-arc for all sufficiently small t. The arc has length t|I|, so T(r,f)≥κ|I|t^(1-d)/(2π). Its ratio to L(r) tends to infinity.

**Proof of (2).** Write W=P_r+iQ_r, where

    P_r(θ)=(1-r²)/(1-2r cos θ+r²),
    Q_r(θ)=2r sin θ/(1-2r cos θ+r²).

The circular mean of P_r is 1, and Q_r is odd. Direct integration gives

    (1/(2π))∫_0^(2π)|Q_r(θ)| dθ
        = (2/π)log((1+r)/(1-r)).

Because |x^+-y^+|≤|x-y|,

    |mean (Re[aW+b])^+ - mean (-Im(a) Q_r)^+|
        ≤ |Re a|+|Re b|.

Oddness divides the absolute-value mean by 2 and proves the formula. Constant P is included by a=0.

**Proof of (3).** Since W′=(W+1)²/2, the equation f′=1 is

    (a/2)(w+1)² exp(aw+b)=1,    Re w>0.

Fix any logarithm ell_a of a/2. Let integers n tend to infinity with the sign of Im a, and put w_n^0=2πin/a. Then Re w_n^0=c|n| for c=2π|Im a|/|a|²>0. On the closed disk |w-w_n^0|≤K log|n|, where K>2/|a| is fixed, use the analytic branch Log(w+1) with imaginary part in (-π/2,π/2). The disk lies in Re w>0 for sufficiently large |n|. Define

    Phi_n(w)=w_n^0-(b+ell_a+2 Log(w+1))/a.

On that disk |w+1| is bounded above by a constant times |n| and bounded below by a positive constant times |n|. Therefore

    |Phi_n(w)-w_n^0| ≤ (2/|a|)log|n|+O(1)
                      ≤ K log|n|,
    sup |Phi_n′(w)| = O(1/|n|) < 1/2.

The mean-value integral along a line segment gives the contraction estimate, since the disk is convex. The contraction mapping theorem yields a fixed point w_n in the disk. Exponentiating its defining identity proves f′((w_n-1)/(w_n+1))=1. Different n give different fixed points because the same chosen logarithm would otherwise make 2πin equal for two distinct integers. This proves infinitely many derivative 1-points in D. □

For the example at the end of Section 4, a>0 and

    |f′|=(a/2)|w+1|² exp(a Re w+b)>(a/2)e^b>1.

Part (2) gives alpha=0. This also checks that the exclusion theorem does not mistakenly rule out every nonconstant admissible function.

## 6. What remains

The exact unrestricted quantities are

    A = sup{alpha(f): f holomorphic, zero-free, f′≠1, alpha(f)<∞},
    B = sup{alpha(f): f meromorphic, zero-free, f′≠1, alpha(f)<∞}.

The historical context places A≤2 and B≤7, and A≤B follows by inclusion. This investigation determines neither supremum. It does not construct a positive-alpha admissible function or prove that none exists. No deduction of A or B follows from the reciprocal/differential parametrizations without a new growth or construction argument.

The separate MODULAR_OBSTRUCTION.md eliminates another substantial family, using a cusp expansion and an exact symmetry. Together these are scoped exclusions, not a full counterexample or a full solution. The companion verifiers check finite exact algebra; infinite analytic assertions are established by the proofs, not by sampling.
