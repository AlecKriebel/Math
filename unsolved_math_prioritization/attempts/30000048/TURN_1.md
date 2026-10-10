# Turn 1: the classification for all products of SU(2)

2026-10-01. First substantive author turn. This is a scoped extension of the credited rank-one mechanism; the original question for every simply connected compact Lie group remains unresolved. Independent review of this partial is pending.

## Theorem

Let G=SU(2)^r for any integer r>=0. If f is a virtual complex character of G, pointwise real nonnegative, and integral_G f=1 for normalized Haar measure, then

    f(g_1,...,g_r)=product_(j=1)^r chi_(d_j)(g_j)^2

for positive integers d_j, where chi_d is the character of the d-dimensional irreducible SU(2) representation. Thus f is the square modulus of one irreducible character of G. No assumption that f was an ordinary character is made.

The case r=1 is Serre's known theorem, proved in his final2025 paper, Proposition5.8. The proof below extends its extremal one-variable Laurent-coefficient argument through polynomial divisibility and integrality. It is not a proof for a simple group of rank two or higher, and no novelty claim is made.

## 1. Representation-ring and polynomial notation

On the standard torus of SU(2), write x=t+t^(-1), |t|=1, so -2<=x<=2. The irreducible characters are the monic integral polynomials P_d(x), d>=1, given by

    P_1=1, P_2=x, P_(d+1)=x P_d-P_(d-1).

They have degree d-1 and satisfy

    P_d(t+t^(-1))=(t^d-t^(-d))/(t-t^(-1)).                 (1.1)

For d>=2, their d-1 roots are exactly 2cos(j pi/d), 1<=j<d, all simple and in (-2,2). The identity follows from the recurrence, with the endpoint values supplied by continuity. Their orthogonality against Haar measure gives integral P_d=0 for d>1 and integral P_1=1.

Every virtual character of SU(2)^r is consequently an element of Z[x_1,...,x_r]. Conversely every such polynomial is a virtual character: the monic triangular family P_d is an integral basis in each variable, and irreducibles of a product are tensor products of the factor irreducibles. Pointwise positivity on G is exactly nonnegativity on [-2,2]^r.

For a polynomial f(x,y), with x the first trace variable and y the remaining r-1 variables, let h(y)=integral_SU(2) f(x,y) dx. Integrating its irreducible expansion in x selects the coefficient of P_1. Thus h is an integral polynomial and a virtual character of the remaining product. If f>=0 and integral_G f=1, then h>=0 and its own Haar mean is1.

## 2. An integral-polynomial domination lemma

Let

    H(y)=product_(j=1)^s P_(d_j)(y_j)^2.

If B is an integral polynomial in those variables and |B(y)|<=H(y) on [-2,2]^s, then B is one of -H,0,H.

**Proof of divisibility.** Fix a variable y_j and any simple interior root alpha of P_(d_j). For every fixed choice of the other variables in the open cube, the domination shows that B, as a polynomial in y_j, vanishes to order at least two at alpha. Indeed its value at alpha is zero; after division by y_j-alpha, a nonzero first derivative would violate the bound O((y_j-alpha)^2). Hence B and its y_j derivative vanish on the full open cube of the other variables at alpha, and are identically zero there as polynomial coefficients. So (y_j-alpha)^2 divides B in R[y]. Doing this for every distinct root and variable proves that H divides B over R[y]. Factors with d_j=1 equal1 and require no argument.

Because each P_d is monic in its own variable and has integer coefficients, sequential polynomial division by P_(d_j)^2 preserves integrality of the quotient and remainder. The real divisibility forces every remainder to vanish. Thus B=H Q for Q in Z[y]. On the dense subset where H is positive, |Q|<=1, and continuity extends this inequality to the closed cube.

**Proof of constancy.** Substitute y_j=t_j+t_j^(-1). The Laurent polynomial L(t)=Q(y) has integer coefficients, is real-valued on the unit torus, and has |L|<=1 there. Parseval gives

    sum_n |a_n|^2 = integral_(U(1)^s) |L|^2 <=1.

Since the a_n are integers, L is either zero or one monomial with coefficient +1 or -1. Reality implies a_n=a_(-n), so a nonzero exponent would require two nonzero coefficients. Hence L, and therefore Q, is the constant -1,0 or1. This proves the lemma. The substitution map is injective, for example by the distinct maximal Laurent exponent of a nonzero polynomial after a generic positive integer weighting. ∎

## 3. Induction and extremal Laurent coefficients

Proceed by induction on r. For r=0 the group is trivial and f=1. Suppose the assertion holds for r-1. In the notation of §1, the induction hypothesis gives

    h(y)=H(y)=product_(j=2)^r P_(d_j)(y_j)^2.              (3.1)

Introduce the rank-one Weyl density polynomial

    w(t)=2-t^2-t^(-2)=|t-t^(-1)|^2

and form

    F(t,y)=f(t+t^(-1),y) w(t)=sum_(j=-M)^M B_j(y)t^j,

where M is the largest positive exponent with a nonzero coefficient polynomial. Such M exists: f is not zero, w is not zero, and a nonzero constant Laurent polynomial could not vanish at t=1 as F does. The coefficients B_j are in Z[y], B_(-j)=B_j, and F is nonnegative on the product torus. The normalized rank-one Weyl integration formula is

    h(y)=B_0(y)/2,

so B_0=2H.

For each fixed y in the cube, Serre's elementary extremal coefficient inequality (Proposition5.2, or the following root-of-unity averaging argument) gives

    |B_M(y)| <= B_0(y)/2=H(y).                             (3.2)

Indeed summing F(t,y) over the M-th roots of1 and over the roots of t^M=-1 produces M(B_0+2B_M) and M(B_0-2B_M), both nonnegative. Terms with other exponents cancel because none beyond ±M is present. This remains true at y where the leading coefficient specializes to zero.

The domination lemma and B_M not identically zero imply B_M=epsilon H with one fixed epsilon in {+1,-1}. Fix y with H(y)>0. Equality holds in the root-of-unity averaging inequality. If epsilon=+1, all roots of t^M=-1 are zeros of the nonnegative trigonometric polynomial F(t,y); if epsilon=-1, all roots of t^M=1 are zeros. Every such zero has even multiplicity: a nonnegative real analytic function of the circle parameter cannot have an odd-order first nonzero Taylor term. The complex Laurent polynomial has the same zero multiplicity because t=e^(i theta) is a local analytic parameter.

The degree bound ±M now forces

    F(t,y)=H(y)[2+epsilon(t^M+t^(-M))].                   (3.3)

One may see this by multiplying by t^M: the 2M roots counted with multiplicity exhaust its degree, and the leading and constant Laurent coefficients determine the scalar. The identity for H(y)>0 extends to all y because that set is dense and both sides have polynomial coefficient functions.

But F(1,y)=F(-1,y)=0 identically. Taking y with H(y)>0, the first equality in (3.3) forces epsilon=-1 and the second forces M to be even. Write M=2d with d>=1. Division by w(t) gives

    f(t+t^(-1),y)=H(y)[(t^d-t^(-d))/(t-t^(-1))]^2
                  =H(y)P_d(t+t^(-1))^2.                  (3.4)

Both sides are polynomials, so the equality includes t=±1 and all trace variables. This completes the induction and proves the theorem.

## 4. Why this does not settle the original target

This proof uses two special features of type A1 factors: a single trace variable gives the whole integral representation ring, and the squared irreducible character has a monic polynomial factorization with all its zeros in the real trace interval. Those features make the domination lemma force divisibility by the entire Haar-marginal square. A general higher-rank simple group has a different real character image and a Weyl density with more than two extremal monomials; neither replacement is supplied here.

In particular, the theorem does not cover SU(3), Sp(2), G2 or the exceptional groups. Restricting an arbitrary f to a rank-one subgroup does not preserve the Haar mean-one assumption, so the established rank-one theorem cannot simply be applied to every root subgroup. Positivity on a grid is likewise insufficient.

The next author turn should attack a genuinely higher-rank simple group, with a globally certified candidate or a rigorous extension/obstruction. The original remains unresolved after1/5 substantive turns. The proof above is an unreviewed scoped partial until the final separate audit.
