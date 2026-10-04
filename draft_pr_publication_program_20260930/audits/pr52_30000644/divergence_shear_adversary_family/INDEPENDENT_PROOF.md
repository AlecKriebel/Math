# Independent divergence/shear reconstruction

Scope: PR 52, original head d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a,
problem 30000644 / OWR-1452-008. This reconstruction was formed after reading
the literal source record and original KNOWN_THEOREM.md, before consulting
historical reviewer prose, verdicts, results, or checker implementations.
It verifies the credited theorem, not a new discovery. No full JPAA article
proof has been obtained or represented as read.

## Exact claim and success criterion

For every commutative unital Q-algebra R and positive integers n,m, every
R[t]/(t^m)-algebra polynomial automorphism of n variables with Jacobian
determinant exactly 1 is the reduction of an R[t]-algebra polynomial
automorphism with determinant exactly 1. An automorphism, including its
polynomial inverse, is an input hypothesis. No inference from determinant
1 to invertibility is allowed. R need not be reduced, a domain, Noetherian,
or finitely generated. Determinant 1 means equality as a polynomial, not
only equality after evaluation at R-points.

## Explicit rational interpolation without division by ring coefficients

For d >= 0 and q in {0,...,d}, put

    L_q(Z) = product_{0 <= j <= d, j != q} (Z-j)/(q-j).

All denominators are nonzero integers and hence units in a Q-algebra.
For 0 <= k <= d, let w_(q,k) be the coefficient of Z^k in L_q(Z), divided
by binomial(d,k). Lagrange interpolation of Z^ell gives

    sum_q w_(q,k) q^ell = delta_(k,ell)/binomial(d,k),

for 0 <= ell <= d. Comparing coefficients proves the universal polynomial
identity

    X^(d-k) Z^k = sum_q w_(q,k) (X+qZ)^d.

This is an identity over Q, so it remains true after every base change to
R, even with nilpotent or zero-divisor coefficients. In particular, the
argument never divides by the coefficient of a polynomial monomial.

## Every divergence-free polynomial vector is a finite shear sum

Let F=(f_1,...,f_n) and sum_i partial_i(f_i)=0. For n=1, every positive
integer is invertible, so the equality partial_1(f_1)=0 implies that f_1
is constant in x_1. This uses coefficient equality in R[x_1], not a
cancellation or reducedness assumption.

For n>=2, choose H_i with partial_n(H_i)=f_i for each i<n, by termwise
integration in x_n with integration constant zero. Define

    D_i H_i = (partial_n H_i)e_i - (partial_i H_i)e_n,
    g = f_n + sum_(i<n) partial_i H_i.

Then F = sum_(i<n) D_i H_i + g e_n and partial_n g = 0. Hence g is
independent of x_n, and g e_n is a shear vector.

Write each H_i as a finite sum of monomials in x_i,x_n, with coefficients
in the polynomial ring in the other variables. Apply the preceding
rational identity separately to every homogeneous degree d. A summand

    H = a (x_i+q x_n)^d

contributes

    D_i H = a d (x_i+q x_n)^(d-1) (q e_i-e_n).

Here a depends only on the other variables. Setting h=a d (x_i+q x_n)^(d-1)
and v=q e_i-e_n gives h(X+s v)=h(X), as an exact identity in R[X,s]:
the linear form changes by s(q-q)=0 and the other variables do not change.
Degree-zero terms have zero Hamiltonian vector and are discarded. Every
sum is finite; no analytic or formal infinite series is introduced.

## Each shear is an actual special polynomial automorphism before reduction

For any a in R[t], define E(X)=X+a h(X)v. Exact translation invariance gives
h(E(X))=h(X). Thus X-a h(X)v is a two-sided polynomial inverse of E.

The Jacobian is I+a v(gradient h)^T. Over any commutative ring the
rank-one determinant identity follows by multilinearity of columns:
terms choosing two rank-one columns have repeated v columns and vanish;
the remaining terms give det(I+a v w^T)=1+a w^T v. Differentiating the
translation identity gives (gradient h)^T v=0. Therefore det J E=1
exactly over R[t], with no truncation and no Jacobian-conjecture step.

## Successive finite jet corrections

Let A=R[t]/(t^m). The monomials 1,t,...,t^(m-1) form a free R-module
basis; consequently coefficient extraction below is valid with arbitrary
zero divisors in R. If rho is an A-automorphism congruent to identity
modulo t^r, 1<=r<m, write rho(X)=X+t^r F(X) modulo t^(r+1).
The determinant expansion has only the trace term at this order because
2r>=r+1. From det J rho=1 follows div F=0 over R.

Decompose F into shear vectors h_s v_s and compose their actual lifts
X+t^r h_s(X)v_s in any fixed order. Their first coefficient is F:
substitution into h_s changes it only by an additional factor t^r, so
cross terms begin at t^(2r), which vanish modulo t^(r+1). Call this
composition Phi_r. Its reduction has the same t^r coefficient as rho,
and bar(Phi_r)^(-1) composed with rho is identity modulo t^(r+1).

For a given sigma in SAut_A, reduce sigma and its given polynomial
inverse modulo t. They give mutually inverse R-automorphisms sigma_0
and sigma_0^(-1), and reduction of the determinant gives det J sigma_0=1.
Extending both maps by fixing t gives an actual special R[t]-automorphism.
Replace sigma by sigma_0^(-1) composed with sigma, which is identity
modulo t. At stage r, maintain sigma=bar(A_r) composed with rho_r.
Replace A_r by A_r composed with Phi_r, and rho_r by
bar(Phi_r)^(-1) composed with rho_r. Associativity preserves the equality.
After r=1,...,m-1 the residual is identity in A. This finite product is
the desired lift. For m=1, extending sigma_0 already suffices.

## Boundaries and falsifiable checks

The constant automorphism sigma_0 can be wild; its existing inverse is
extended, not generated by the shear construction. No tameness conclusion
for all special R-automorphisms follows. No uniqueness, optimal degree,
uniform tame length, infinite formal lift, or characteristic-p analogue
is claimed. A zero Q-algebra, if permitted by the convention, makes the
assertion trivial and does not break the proof.

In characteristic p, x -> x+t x^p is a special automorphism modulo t^2
(inverse x -> x-t x^p at that truncation), but cannot lift as a special
automorphism over the domain k[t] in one variable: polynomial
automorphisms over a domain in one variable have degree one and determinant
1 forces the linear coefficient 1. This explains rather than removes the
Q-algebra hypothesis.

Independent finite checks will target rational interpolation, linear
kernel bases of the divergence map, shear inverses and determinants,
successive jet corrections and nonreduced Q[u]/(u^2) coefficients.
Finite computations supplement this universal proof and do not certify
the theorem for every R,n,m by enumeration.
