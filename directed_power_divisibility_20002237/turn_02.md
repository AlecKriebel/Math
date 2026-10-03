# Attempt 2 of 5: One positive atom with unrestricted negative literals

## Target and verdict

Attempt a decision procedure beyond the prior positive-only theorem by combining exponential-fiber arithmetic with Attempt 1. We prove: for every fixed prime p, existential sentences whose DNF conjunctions contain at most one positive R_p-atom are decidable, allowing arbitrarily many negative R_p-atoms and additive disequalities. The full theory, with unboundedly many positive atoms, remains unresolved.

## 1. Exact fiber reduction

Solve all additive equalities first. If inconsistent, reject. Otherwise parametrize the integer solution set as x=x_0+Bz, z∈Z^r. Write the one positive atom as R_p(L_*,M_*). For T=p^s it becomes

    q(T)·z=h(T),
    q_i(T)=mu_i-T lambda_i,
    h(T)=T lambda_0-mu_0.

All q_i,h are integral affine polynomials. Let Λ_s be its integer solution lattice. Nonemptiness is exactly gcd_i(q_i(p^s)) | h(p^s), with the convention that a zero coefficient row is solvable exactly when h=0.

If every q_i is the zero polynomial, then h(p^s)=0 has either all exponents or at most one exponent. The fiber is the original Z^r whenever it exists; apply Attempt 1 directly. This covers r=0 as well.

Otherwise choose j with q_j not the zero polynomial. At its at most one numerical root, test the corresponding p-power exponent directly by integer linear algebra and Attempt 1. For all other exponents q_j(p^s)≠0. When Λ_s is nonempty, its affine Q-span is the rational hyperplane H_s:q(p^s)·z=h(p^s). Indeed its integer homogeneous kernel spans the rational kernel, by clearing denominators in a rational basis. Thus an affine identity on Λ_s is equivalent to the same identity on H_s.

## 2. Excluding identically false disequalities

For a required disequality F(z)=f_0+sum_i f_i z_i !=0, its forbidden identity on H_s is equivalent to the simultaneous equations

    f_i q_j(T)-f_j q_i(T)=0 for every i,
    f_0 q_j(T)+f_j h(T)=0.

These are polynomial equations in T. They either hold identically for generic T, or can hold only at the finitely many roots of a nonzero polynomial. Their truth along T=p^s is therefore effectively eventually constant. Exceptional exponents can be enumerated using a root bound and direct evaluation.

## 3. When a negated relation forbids the entire fiber

Let L=ell_0+sum ell_i z_i and M=m_0+sum m_i z_i occur in a negative literal. For indices i=1,...,r define

    A_i=m_i q_j-m_j q_i,    B_i=ell_i q_j-ell_j q_i,

and define the extra index 0 by

    A_0=m_0 q_j+m_j h,      B_0=ell_0 q_j+ell_j h.

Then R_p(L,M) is identically true on the fiber precisely when for some U=p^t, t≥0,

    A_i(T)=U B_i(T) for all i=0,...,r.                 (1)

This follows from Attempt 1 and the row-space identity test: M-U L is a scalar multiple of q·z-h exactly when these cross-products vanish. All A_i,B_i are affine polynomials.

If all B_i are zero polynomials, (1) says all A_i(T)=0. Its truth is effectively eventually constant. At numerical values where all B_i(T)=0, use the same test; these are finitely many unless all B_i are identically zero.

Otherwise choose k with B_k not identically zero. Outside its finite zero set, condition (1) is equivalent to

    A_i B_k-A_k B_i=0 for every i,
    A_k(T)/B_k(T) ∈ {p^t:t≥0}.                       (2)

If any cross-product polynomial is nonzero, only finitely many T can satisfy (2). If all are polynomial identities, only the rational-function power test remains.

## 4. Effective rational-function power lemma

Given a rational function f(T)∈Q(T), the set

    E_f={s≥0:f(p^s) is defined and belongs to p^N_0}

is effectively eventually constant. More precisely it is a finite set or a cofinite set, computable by a finite exceptional list and a tail truth value.

Proof. Zero f gives the empty set. Otherwise write f=G/H with nonzero G,H∈Z[T]. Remove their lowest powers of T:

    G=T^a g,  H=T^b h,  g(0)h(0)≠0.

Choose S greater than v_p(g(0)) and v_p(h(0)). For s≥S, every nonconstant monomial of g(p^s) has strictly larger p-adic valuation than g(0), so v_p(g(p^s))=v_p(g(0)); likewise for h. Put c=v_p(g(0))-v_p(h(0)). If f(p^s)=p^t, then necessarily

    t=(a-b)s+c.                                      (3)

Substituting (3) reduces the equality to

    g(p^s)=p^c h(p^s).                               (4)

Clear the constant denominator when c<0. If the resulting polynomial is nonzero, an effective Cauchy root bound gives a bound on all possible p^s and hence all exceptional s. If it is identically zero, f(T)=p^c T^(a-b), and membership is exactly (a-b)s+c≥0, apart from finitely many poles of the original representation. This inequality is eventually always true or eventually always false, with an explicit threshold. Directly inspect all smaller exponents. This also covers negative leading coefficients, constant functions, negative monomial degree, and zero/pole exceptions. QED.

No ineffective Diophantine approximation or unproved uniform bound is used.

## 5. Completing the decision procedure

For every negative literal and disequality the preceding analysis supplies an explicit threshold and its tail truth value for “forbids the whole fiber,” plus exact finite exceptions. Take a common threshold S.

- Test all s<S directly, using integer linear algebra and the lattice-avoidance theorem.
- If any forbidden identity holds for all s≥S, no tail fiber is admissible.
- Otherwise all tail fibers are admissible whenever nonempty, so decide whether gcd_i q_i(p^s) divides h(p^s) for some s≥S.

For completeness, this last positive-fiber test is elementary, and is the credited main result of the previous UnsolvedMath report:

(a) If gcd_Q[T](q_i)=1, a cleared Bezout identity produces N≠0 with sum U_i q_i=N. Hence the numerical gcd is gcd(N,q_1(T),...,q_r(T)). Solvability depends only on T mod |N|. Starting at p^S mod |N|, the residue orbit under multiplication by p is eventually periodic and finite, so it is decidable.

(b) Otherwise the common polynomial gcd is a primitive linear Q(T)=aT+b, a≠0, and q_i=c_i Q with c_i∈Z. With C=gcd_i|c_i|, nonzero fibers are solvable iff C|Q(T)| divides h(T). If h=kQ, the condition is C|k. If h=cT+d is not proportional to Q, then Q(T) divides the nonzero integer ad-bc, leaving only finitely many signed divisors and therefore finitely many T. The zero of Q is checked separately.

All tail restrictions s≥S can be imposed explicitly in these procedures. If a conjunction has no positive atom, use Attempt 1. Finite DNF completes the proof.

## Scope and remaining gap

This proves a strictly more expressive fragment than the prior positive-only one-atom result: arbitrary Boolean combinations are allowed so long as each DNF conjunction has at most one positive R_p occurrence. The proof does not allow two independently quantified positive exponents. Their polynomial minors and integral solvability conditions depend on several p-power parameters; the single-variable p-adic tail lemma does not make those multivariable conditions eventually constant. No answer to the full AIM problem is claimed.
