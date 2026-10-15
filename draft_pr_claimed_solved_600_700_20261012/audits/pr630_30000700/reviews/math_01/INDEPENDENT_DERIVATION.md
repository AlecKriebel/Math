# Independent mathematical derivation before consulting the old audit

Recorded 2026-10-15T03:45:38Z. This derivation uses the exact claim as stated in
the pinned `safe/PROOF.md`, but was completed before reading the old audit or
any of its verification code. It does not decide source interpretation or
priority. Completion estimate for this mathematical audit: 25%.

Let H1 mean `{f=a}={f'=a}` as sets in C. Let H2 mean
`{f'=b} subset {f^(k)=b}`, for integer k>=2 and b!=0. The claimed conclusion
at a=0 is `f=d exp(cz)`, with c,d nonzero and c^(k-1)=1.

## Direct obstruction

For any complex b!=0 and z0, take f=b(z-z0)^k/k!. Differentiation gives
f'=b(z-z0)^(k-1)/(k-1)! and f^(k)=b identically. Hence H1 holds for a=0,
with multiplicities k and k-1, while H2 holds everywhere. The preimage
`{f'=b}` is nonempty and consists of the k-1 distinct nonzero roots of
`(z-z0)^(k-1)=(k-1)!`. Since f(z0)=0, the conclusion is impossible for
every nonzero c,d. This does not use the restriction c^(k-1)=1.

## Polynomial necessity through divisibility (independent alternative)

For a nonconstant polynomial P of degree n, first handle the exceptional
case P'-a identically zero: then P' is the constant a!=0, so `{P'=a}=C`
whereas `{P=a}` has one point. If P'-a is nonzero and a!=0, every root of
P-a is simple, because P'=a there. There are n distinct roots of P-a, all
roots of P'-a, although the latter has degree <=n-1. Thus a!=0 is impossible.
For n=1 and a=0, P' is a nonzero constant: its zero set is empty whereas P
has one root. This also fails H1.

For a=0 and n>=2, factor P=A product (z-r_j)^m_j over its r distinct roots.
H1 implies m_j>=2, and implies that P' has no roots outside those r points.
Its total root multiplicity is therefore sum(m_j-1)=n-r. Since deg P'=n-1,
r=1 and P=A(z-z0)^n.

Write x=z-z0 and s=b/(An)!=0, where `(An)` denotes A*n. The polynomial
L=x^(n-1)-s is squarefree because its only possible common root with L'
would be x=0, and L(0)=-s!=0. H2 says that every root of L is a root of
R=P^(k)-b, so L divides R. If k>n, R=-b is a nonzero constant and this is
impossible. If 2<=k<=n then

    R=A*n!/(n-k)! * x^(n-k)-b,

whose degree is at most n-2 unless it is the zero polynomial. Since
deg L=n-1, divisibility forces R identically zero. Its leading nonconstant
term cannot vanish when n>k, so n=k, and then A*n!=b. This establishes the
full polynomial classification without a roots-of-unity argument.

## Transcendental family through the Euler operator

Put t=exp(lambda*z), lambda!=0. Differentiation on polynomials in t is the
operator lambda*t*d/dt. On t^j it acts diagonally with eigenvalue lambda*j.
Consequently, for f=(t-1)^2 and k>=1,

    f'=2*lambda*t*(t-1),
    f^(k)=lambda^k*(2^k*t^2-2*t).

Because t never vanishes, f and f' vanish precisely at t=1, with respective
orders 2 and 1 (t'=lambda at t=1). Choose b=-lambda/2. Then

    f'-b=2*lambda*(t-1/2)^2.

The exponential map with nonzero exponent is onto C\{0}, so these b-points
exist and there are infinitely many. At all of them,

    f^(k)-b=lambda*(lambda^(k-1)*(2^(k-2)-1)+1/2).

This vanishes precisely when
`lambda^(k-1)=-1/(2^(k-1)-2)`. For each integer k>=3 the right side is a
nonzero complex number, with k-1 nonzero complex roots. For k=2, the
displayed difference is lambda/2, so this construction does not work.
The zeros at lambda*z=2*pi*i*j, j in Z, are infinitely many and discrete,
and f is not identically zero. Thus f is transcendental entire and cannot
be a nonzero exponential. Its b-points have multiplicity two as roots of
f'-b. H2 is a value implication and does not constrain that multiplicity.

## Boundary attacks

* Constant f=K is excluded by the nonconstant hypothesis. If one allowed
  it, a=0 would satisfy H1 exactly when K=0; if a!=0, H1 would hold exactly
  when K!=a. H2 would be vacuous for every constant, since f'=0 and b!=0.
  In particular the zero function satisfies both hypotheses for all a,
  but is excluded by the nonconstant assumption.
* For nonconstant polynomials all values of f and every nonconstant f' are
  attained in C. In particular H2 is not vacuous in the classified family.
* For a=0, every proposed exponential conclusion is zero-free. This rules
  out the counterexamples regardless of any additive-constant typo or the
  discrete c constraint.
* The proof gives no result on the remaining nonzero-a transcendental
  question. It cannot infer historical intent or novelty.
