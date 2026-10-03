# Attempt 4 of 5: Arbitrarily many constraints with one shared power parameter

## Target and verdict

Attempt to remove the one-positive-atom limitation by allowing an arbitrary polynomial matrix controlled by one shared power U=p^s. This succeeds for that one-parameter class, including negative directed-relation constraints, but does not control independent power parameters.

We prove decidability of systems

    EXISTS s≥0, z∈Z^n:
       A(p^s)z=b(p^s),
       F_i(p^s,z) !=0,
       not R_p(L_j(p^s,z),M_j(p^s,z)),                 (1)

where all matrix entries and all coefficients of the affine forms in z are integral polynomials in T. There are finitely many constraints and no degree bound.

This is an existentially expressible class in the original structure: choose U by R_p(1,U), and use Attempt 3's positive-existential relation G_p(U,x,y) repeatedly to evaluate U^k times a variable or a constant. Intermediate evaluations are uniquely determined, so the negative R_p-literals retain their intended meaning. The theorem is not a claim that arbitrary independent atoms can be synchronized.

## 1. Generic ranks and exceptional parameters

Let A(T) have m rows and n columns and let B(T)=[A(T) | b(T)]. Compute ranks r_A,r_B over Q(T).

If r_B>r_A, a fixed nonzero r_B-minor of B must vanish whenever numerical ranks coincide. Its finitely many roots include every possible exceptional T. A Cauchy bound and direct checking of p-power values decide all candidates.

Suppose r_A=r_B=r. For r>0 choose a nonzero r-minor of A. Outside its finite zero set, both numerical ranks are r: all larger minors vanish identically. For r=0, A is identically zero; either b is also identically zero, or only finitely many common roots of the nonzero entries of b can work. In the identically zero case all z are available and the avoidance analysis below applies directly.

All exceptional nonnegative exponents are checked separately with ordinary integer linear algebra and Attempt 1.

## 2. Exact integral-solvability criterion

For a fixed generic T, let Δ_A(T) be the positive gcd of all r-by-r minors of A(T), and Δ_B(T) the corresponding gcd for B(T). Then

    A(T)z=b(T) has an integer solution iff Δ_A(T)=Δ_B(T). (2)

Here is a direct Smith-normal-form proof. Apply unimodular row and column operations to put A in diagonal form with positive d_1,...,d_r and zero remaining entries. The shared-rank hypothesis forces the transformed b to vanish below row r. The gcd of maximal minors of A is D=product_i d_i. The augmented matrix adds, up to sign, maximal minors (D/d_i)b_i. Its gcd equals D exactly when every d_i divides b_i, which is exactly integral solvability. Unimodular operations preserve determinantal gcds. This proves (2), including rectangular matrices.

## 3. Polynomial gcds reduce determinantal gcds to finite residue data

Given nonzero polynomial list f_1,...,f_k∈Z[T], let G be a primitive integral representative of its Q[T]-gcd. Gauss's lemma gives f_i=G g_i with g_i∈Z[T] and gcd_Q[T](g_i)=1. A polynomial Bezout identity, after clearing denominators, supplies a nonzero integer N with

    sum_i u_i(T) g_i(T)=N,  u_i∈Z[T].

For every integer T,

    gcd_i f_i(T)=|G(T)| gcd(N,g_1(T),...,g_k(T)).        (3)

The remaining gcd is positive and depends only on T modulo |N|. The formula handles G(T)=0, although generic ranks have already removed that case.

Apply (3) to the maximal-minor lists of A and B, yielding G,H and bounded positive functions d,e depending on a common modulus M. Thus (2) becomes

    |G(T)|d(T mod M)=|H(T)|e(T mod M).                 (4)

For each residue a, square (4) to obtain the polynomial equation

    d(a)^2 G(T)^2-e(a)^2 H(T)^2=0.                     (5)

Squaring introduces no false solutions since the two quantities in (4) are nonnegative. If (5) is a polynomial identity, all generic parameters of that residue are feasible. Otherwise only its finitely many roots can be feasible; use an effective root bound and direct checking.

The sequence p^s mod M is effectively eventually periodic, including when p divides M. Consequently the set of exponents giving a nonempty integer fiber is effectively eventually periodic, with a finite exceptional list. This is a complete decision procedure for the equality part of (1), rather than merely a rational-solvability test.

## 4. Negative literals on polynomial-matrix fibers

On any generic nonempty integer fiber, its affine Q-span is the rational solution space: integer homogeneous solutions span the rational kernel after clearing denominators. Gaussian elimination over Q(T) supplies a rational particular solution z_0(T) and rational kernel basis K(T). Exclude the finitely many zeros of its denominators/pivot minors. These can all be checked separately.

Substitute

    z=z_0(T)+K(T)w

into every F,L,M. The resulting affine forms in w have coefficients in Q(T). They describe identities on the fiber; w need not parametrize the integer points themselves, because an affine identity is unchanged by passing to the rational affine span.

A disequality fails identically iff every restricted coefficient is zero. Each coefficient is a rational function, so the identity condition is effectively eventually constant along p^s.

For a negative R_p-literal, let a(T),b(T) be the restricted coefficient vectors for M,L. The positive relation is identically true iff some p^t satisfies a(T)=p^t b(T). If b is generically zero, test whether a is zero. Otherwise choose one generically nonzero component b_k; away from its zero set the test is

    a_i b_k-a_k b_i=0 for every i,
    a_k/b_k∈p^N_0.

Clear denominators. Nonzero cross-product polynomials yield only finitely many exceptional parameters. If all vanish identically, Attempt 2's rational-function power lemma decides the remaining membership and shows it is effectively eventually constant.

Attempt 1 now says the entire list of negative requirements is jointly satisfiable on a nonempty integer fiber exactly when none forbids the whole fiber. Taking a common threshold for all these eventually constant tests reduces tail satisfiability to the already-decided eventually periodic equality condition. Finite exceptions are checked directly.

## 5. What this does and does not add

The class allows arbitrarily many independent integer unknowns, equations of unbounded degree in one power parameter, and arbitrarily many negative relation constraints. In particular it includes genuinely multi-equation systems, not just one affine row. Its decidability is proved through integral lattice indices, not numerical sampling or real solvability.

It does not decide the full AIM problem. General R_p-atoms supply separate exponents s_1,...,s_k. Their determinantal polynomial gcds live in Z[T_1,...,T_k]. The univariate Bezout-to-a-constant step can fail there even for polynomials with no common factor, and the rational-function tail argument no longer describes a one-dimensional sequence. Attempt 5 will examine this precise obstruction rather than assume it away.
