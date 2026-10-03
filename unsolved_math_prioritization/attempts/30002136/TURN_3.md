# Turn 3: mixed-sign two-occurrence rigidity

2026-10-03 07:39 UTC. Substantive author turn 3/5. **NO FULL RESOLUTION.** Completion estimate: 8%, a planning estimate only. No novelty claim.

## Theorem

Every cyclically reduced word with at most two total occurrences of b±1 has no nonconjugate universal SL3-trace companion in F2. This strengthens Turn2 at count2 by permitting both signs; a-exponents remain arbitrary. The same holds after any simultaneous automorphism of F2.

Turn2 proves the zero-, one-, and same-sign cases. Its letter-count argument shows that a companion to a word with one b and one b^-1 must also have exactly one of each. After cyclic rotation, both words therefore have the form

u=a^p b a^q b^-1,    v=a^r b a^s b^-1,

with p,q,r,s nonzero integers: a zero gap would permit cyclic cancellation of b with b^-1. Their a-exponent sums agree: p+q=r+s. No hidden positivity restriction is used.

## Adjugate coefficient formula

Use the Turn1 extension to GL3 and put A=diag(x1,x2,x3), with independent invertible xi; let B=(b_ij) be generic. Set M_sigma=∏_i b_(i,sigma(i)). Expansion of the adjugate gives

det(B) tr(A^p B A^q B^-1)
 = Σ_(sigma∈S3) sign(sigma) M_sigma Σ_(i=1)^3 xi^p x_sigma(i)^q.

Indeed, the trace on the left is Σ_ij xi^p xj^q b_ij Cofactor_ij(B), and b_ij Cofactor_ij(B) is exactly the sum of signed determinant monomials M_sigma with sigma(i)=j. Distinct permutations give distinct monomials in the nine independent B entries. Thus universal equivalence implies equality of each displayed Laurent coefficient. This is a polynomial identity argument on a dense open set, not a numerical test.

## Reconstruct the two ordered gaps

For sigma=(12), remove its common sign. The coefficient is

x1^p x2^q+x2^p x1^q+x3^(p+q).

Since p+q=r+s, the last terms cancel. Linear independence of Laurent monomials implies {p,q}={r,s} with multiplicity. If (r,s)=(p,q), we are done. The only remaining case is (r,s)=(q,p).

For sigma=(123), the coefficient records the cyclic orbit of the integer triple (p,q,0):

x1^p x2^q+x2^p x3^q+x3^p x1^q.

The corresponding coefficient for (q,p) records the orbit of (q,p,0). Equality of the Laurent polynomials requires these two triples to be cyclic rotations. A zero exponent occurs in exactly the third coordinate because p,q are nonzero. Matching it forces the rotation to be trivial, hence p=q. In that case the two ordered pairs already coincide. Negative exponents and p+q=0 cause no difficulty; the three variables are independent, so there is no determinant-one relation among these Laurent monomials.

Thus the companion has the same ordered gaps and is conjugate to u. The automorphism extension follows by composing every representation with the inverse automorphism; conjugacy and universal trace equivalence are preserved.

## Checks and limitations

check_turn_3.py verifies the full adjugate identity symbolically with independent diagonal entries P_i,Q_i; checks all36 nonzero gap pairs in[-3,3]^2 for the two coefficient signatures and ordered reconstruction; and displays an exact rational separation between a b a^-1 b^-1 and a^-1 b a b^-1. Its assertions supplement the proof rather than replace it.

This theorem does not cover general words with three or more mixed-sign b occurrences. It also does not prove that every word is automorphic to a low-count word. The next route examines reconstruction from generic-matrix path coefficients beyond the four-gap boundary, where repeated-state sums become a real obstruction.
