# Substantive turn 3: an exact bulk anti-concentration disintegration

## Route and outcome

The third route keeps the fixed-n uniform partition distribution exactly, and varies the numbers of1- and2-cycles within a mass-preserving fiber. It gives a precise finite Krawtchouk representation, integral representation-theoretic coefficients, growing fiber length on almost all columns, and a conditional route to zero density. The missing input is an anti-concentration estimate for these particular irreducible-character sequences. Neither genericity nor independence of conditioned cycle counts is asserted.

## 1. Exact measure on fibers

Fix a partition nu with every part at least3 and |nu|<=n. Put R=n-|nu| and s=floor(R/2). The partitions in its fiber are

mu_r = nu union (2^r,1^(R-2r)),  r=0,...,s.                (1)

Every partition of n occurs in exactly one such fiber. Conditional on nu, a uniform partition mu makes r **uniform** on the s+1 integers. The fiber itself has probability (s+1)/p(n), not equal weight among fibers and not a binomial weight. The independent row lambda remains uniform among the p(n) irreducible characters.

Most of these fibers are long. For an integer t<=n, deleting t unit parts gives

Pr(m_1(mu)>=t)=p(n-t)/p(n).                                 (2)

Since R>=m_1(mu), for any positive integer eta with2eta<=n,

Pr(s<eta)<=1-p(n-2eta)/p(n).                               (3)

Using the exact uniform ratio estimate in Peluse–Soundararajan2026 Proposition3, the right side is O(eta/sqrt(n)) whenever eta=o(sqrt(n)). In particular s tends to infinity in probability under the correct size-weighted fiber law. This is a genuine bulk source of randomness that survives conditioning total size; it does not give independent geometric counts.

## 2. Character restriction supplies the exact transform

Fix lambda,nu and realize a permutation sigma of cycle type nu on n-R letters. On the other R letters choose s disjoint transpositions t_1,...,t_s; the possible extra letter is fixed. Their elementary abelian group H has order2^s and commutes with sigma. Let V_lambda be the irreducible representation. Decompose its restriction to H into simultaneous eigenspaces V_T indexed by subsets T of {1,...,s}, with eigenvalue-1 at t_i precisely for i in T.

The permutation sigma preserves V_T. Set a_T=Tr(sigma|V_T). Permutations of the s disjoint pairs normalize H and commute with sigma; therefore a_T depends only on j=|T|. Denote this common value by a_j. It is an integer: the H-projector expression makes its trace a rational average of the integer character values of sigma h, while sigma has finite order on V_T, making the same trace an algebraic integer. A rational algebraic integer is integral. Positivity is not asserted unless sigma is the identity.

For tau_r=t_1...t_r, equation(1) is the cycle type of sigma tau_r. Summing the eigenspace traces gives

f_(lambda,nu)(r):=chi_lambda(mu_r)
 =sum_(j=0)^s a_j K_j(r;s),                                (4)

where

K_j(r;s)=sum_(l=0)^j (-1)^l binom(r,l) binom(s-r,j-l).      (5)

The H-character Fourier inversion gives the exact inverse

a_j=2^(-s) sum_(r=0)^s K_r(j;s) f_(lambda,nu)(r).           (6)

No probabilistic approximation is involved. Binomial coefficients in this transform arise from H, not from the uniform probability law in Section1.

For fixed j, K_j(r;s) extends to a polynomial in r of degree j with leading coefficient (-2)^j/j!. One way to check this is to use the generating function

sum_j K_j(r;s)t^j=(1+t)^(s-r)(1-t)^r
                =(1+t)^s exp(r log((1-t)/(1+t))).

The coefficient of t^j has leading r-power j with exactly that coefficient. Thus (4) is the unique polynomial of degree at most s interpolating the character values on the fiber. If it is not identically zero, its degree is exactly

d(lambda,nu)=max{j:a_j!=0}.                                (7)

## 3. What would prove vanishing probability tends to zero

A nonzero polynomial of degree d has at most d distinct zero nodes. Therefore the exact conditional bound is

Pr(chi_lambda(mu)=0 | lambda,nu)
 <= 1_(f identically zero) + [d/(s+1)]1_(f not zero).        (8)

Average with lambda uniform and the size-weighted fiber law in Section1. If one could prove both

Pr_(lambda,nu)(f identically zero)->0,
E_(lambda,nu)[d/(s+1); f not zero]->0,                      (9)

then the requested total zero probability would tend to zero. More refined root counts in (8), rather than degree alone, could replace the second condition. Growing s from (3) by itself is not enough: d can grow with s and may equal s.

There is a representation-theoretic interpretation of the top coefficient that makes the remaining issue concrete. Finite differences give

(-2)^s a_s = sum_(r=0)^s (-1)^(s-r) binom(s,r) f(r).        (10)

Equivalently, a_s is the trace of sigma on the simultaneous negative-eigenvalue space for all s chosen transpositions. In the classical Frobenius characteristic notation it is the coefficient pairing

<s_lambda, e_2^s p_1^(R-2s) p_nu>,                         (11)

because p_1²-p_2=2e_2 and (10) expands the s-fold difference. This can also be viewed as a signed residual-character sum after s vertical two-strip branching steps. Showing these traces vanish for all but small j, or instead controlling roots when the high-degree traces remain, is a real additional problem. It is not supplied by uniform random-partition shape convergence.

## 4. Adversarial countercontrols to tempting shortcuts

The sign irreducible character has f(r)=sgn(sigma)(-1)^r. Its interpolating polynomial has degree s, although none of the values is zero. Hence a full degree is not a zero-density prediction. These sign rows are thin, so this example by itself is not a statement about typical lambda.

Conversely, nonnegative integer coefficients a_j do not imply useful anti-concentration. Take nu empty, R=2s, and the regular representation of S_(2s), which is deliberately reducible. Its sequence is f(0)=(2s)! and f(r)=0 for r>0. Restriction to H has a_j=(2s)!/2^s for every j. The identity sum_j K_j(r;s)=2^s1_(r=0) verifies this directly. It has nonnegative integral weight-space dimensions and zero fraction s/(s+1), tending to1. Thus neither finite-group character integrality, positivity of identity traces nor the existence of a long fiber can replace the missing **irreducible bulk** information. This is a countercontrol to a proposed method, not a counterexample to the source question.

## 5. Finite exact checks and remaining gap

The checker reconstructs the transform and its integral coefficients directly from independently generated exact character values for every fiber through n=15. It verifies all fiber masses, the short-fiber bound, polynomial degrees by finite differences, root counts, identity-case nonnegativity, the sign-row control and the regular-character control. Small finite values of the resulting upper bound are recorded without asymptotic extrapolation.

This route has reached a valid distribution-preserving anti-concentration reduction, but it has not proved either condition in(9), nor an adequate alternative root bound. The next substantive route must test the actual residual traces or exploit additional structure of bulk irreducibles; assuming these coefficients are generic would simply restate the missing theorem.
