# Independent universal derivation for PR51

This is a verification of the submitted, credited proof. The exact hypothesis is a **positive integer** N and the exact target is nonnegativity of the coefficients of

    eta(N tau)^phi(N) / product_(d|N) eta(d tau)^mu(d).

Natural number zero is outside the domain: eta(0 tau) is undefined. No assertion concerns arbitrary eta products, regular systems of weights, strict coefficient positivity, or positivity at every cusp. The claim is the displayed Fourier expansion at infinity.

## Normalization and the algebraic setting

For q=exp(2 pi i tau), Im(tau)>0, write eta(d tau)=q^(d/24) E(q^d). Thus the leading shift is

    A_N = (N phi(N) - sum_(d|N) d mu(d))/24.

It can be fractional: A_1=0, A_2=1/8, A_3=1/3, A_4=3/8. The normalized product has integral powers, integral coefficients and constant term 1; the original coefficients are exactly these with their exponents shifted by A_N. The shift cannot change signs. Further, sum_(d|N) d mu(d)=product_(p|N)(1-p), which directly implies A_N>=0. For N=1 the eta factors cancel and the product is identically 1. For prime p the shift is (p^2-1)/24. The denominator 12 in the report's prime display is inconsistent with its own eta definition; it is not used by the candidate or this derivation.

All infinite Euler products below are legitimate formal power series: at any fixed degree, only finitely many positive factor degrees matter, and each factor has constant term 1 and hence an inverse. Rearrangement by exponents or by finitely many residue classes preserves this local finiteness. No modular weight, character, level, cusp holomorphy or Sturm bound is needed for this proof. In particular the finite coefficient calculations are not a modular-form certificate.

## Imported identities and absence of circularity

The two dependencies are identified openly rather than assumed to be new work:

1. E(q^t)^t/E(q) is the generating function for t-core partitions, for every positive integer t, including composite t and t=1. The familiar core/quotient partition bijection explains this identity: the ordinary partition series 1/E(q) equals the t-core series times t independent quotient partition series at base q^t. This bijection is a credited classical input. The independent hook computations check the convention in small degrees; they do not establish the bijection.
2. Berkovich–Garvan's theta identity (their Theorem 1.2) has integer a>=2, the zero-sum lattice Lambda_a, Q_a(n)=a sum n_i^2/2+sum i n_i, and monomials z^(a n_j+j). Its right side is E(q) E(q^a)^(a-2) [z^a;q^a]/[z;q]. This is exactly the dependency used in the local proof.

I checked the functional-equation argument independently. For fixed 0<|q|<1 the lattice side converges normally on compact subsets of C*. The quadratic term dominates all linear terms. The bracket quotient has only removable apparent poles: the denominator zeros z=q^k are simple and the numerator also has a simple zero at each such point.

Both sides F satisfy F(qz)=z^(-(a-1))F(z). The product side follows from [qz;q]=-z^(-1)[z;q]. The lattice side follows from the cyclic affine bijections derived below. At any nontrivial a-th root of unity z, every inner sum is sum_j z^j=0, and the product numerator vanishes. At z=1, the common limiting value is a E(q^a)^a/E(q), using the credited core theta identity; this is a separate classical identity, not the target composite eta-product theorem.

The standard uniqueness statement can be verified by the argument principle. A nonzero holomorphic H on C* with H(qz)=z^(-d)H(z) has d zeros in a zero-free-boundary fundamental annulus |q|R<|z|<R. Integrating q H'(qz)/H(qz)=H'(z)/H(z)-d/z around |z|=R gives the inner boundary count equal to the outer count minus d. Choose 1<R<|q|^(-1) avoiding zeros on both boundary circles. The difference of the two sides would have at least a distinct zeros at the a-th roots of unity, exceeding d=a-1. Hence it vanishes identically. This closes the analytic uniqueness step without assuming the target positivity theorem. The core partition and core theta identities remain credited inputs, not newly certified formal-library theorems.

## Formal positivity after specialization

On the zero-sum lattice,

    Q_a(n) = sum_i [a n_i(n_i-1)/2 + i n_i].

Each coordinate summand is an integer and nonnegative. For n_i>=0 this is immediate. For n_i=-k<0 it is k[a(k+1)/2-i]>=k>0, since 0<=i<=a-1. Moreover each summand is at least a |n_i|(|n_i|-1)/2. The alternative half-square expression is integral because sum n_i^2 has even parity on the zero-sum lattice.

Let R rotate n one place to the left and write s=sum n_i. Directly,

    Q_a(R n)-Q_a(n)=a n_0-s.

For j>=1, add e_(j-1)-e_(a-1) to R n. The quadratic correction is a(n_j-n_0+1); the linear correction is j-a. Therefore

    Q_a(T_j n)-Q_a(n)=a n_j+j-s.

For j=0 take T_0=R, giving the same formula. On Lambda_a, s=0. Rotation followed by a fixed zero-sum integer translation is a bijection, with inverse R^(-1) after subtracting that translation. There is no missing index, sign or exceptional j=0 case.

For integers 0<r<M, specialize z=q^r and replace the theta identity's base by q^M. Every exponent becomes

    e(n,j)=M Q_a(n)+r(a n_j+j)
          =(M-r)Q_a(n)+r Q_a(T_j n)>=0.

The sublevel e<=H lies within Q<=H/(M-r). The coordinate lower bound above therefore forces a finite box, with all lattice points of any fixed degree included. This proves that the specialized series has nonnegative integral coefficients and finite coefficient multiplicities. It also justifies the substitution despite the unspecialized Laurent powers of z. This covers even M and r=M/2, where bracket progressions coincide and must be counted twice. Those cases are independently checked; the all-N factorization itself chooses odd M and distinct paired residues.

Multiplication by the positive core series at base q^M gives

    D_a(q^r;q^M)=E(q^(aM))^(2a-2) [q^(ar);q^(aM)]/[q^r;q^M]

with nonnegative coefficients. The cancellation of E(q^M) and the exponent 2a-2 are exact, including a=2.

## All integers, not a squarefree subcase

Mobius inversion assigns each factor 1-q^k in product_(d|M) E(q^d)^mu(d) exponent sum_(d|gcd(k,M)) mu(d), equal to 1 if gcd(k,M)=1 and to 0 otherwise. This works for every M, without squarefreeness. Consequently the denominator is the product over positive integers coprime to M.

For N=pM with p prime, p not dividing M, and M>1 odd, every reduced residue pairs distinctly with its complement. Representatives 1<=r< M/2, gcd(r,M)=1 number phi(M)/2. The associated brackets partition the coprime positive factor degrees exactly. Divisors of pM split into d and pd with mu(pd)=-mu(d), including zero Mobius terms. The product of D_p over these representatives therefore has numerator exponent

    (2p-2) phi(M)/2 = phi(pM),

and its bracket quotient is precisely the required Mobius numerator/denominator ratio. It equals the normalized target. Every factor is positive in the nonnegative-coefficient sense.

For N=p^alpha M with p not dividing M, let N'=pM and t=p^(alpha-1). The denominators for N and N' are identical because the nonzero Mobius terms depend only on the radical. Also phi(N)=t phi(N'). Therefore

    normalized S_N = normalized S_N' *
       [E(q^(N' t))^t/E(q^N')]^phi(N').

The extra factor is a nonnegative integral power of a t-core generating function. This includes alpha=1, for which t=1 and the factor is 1. When M=1, use normalized S_p=E(q^p)^p/E(q), then the same lift; do not apply residue pairing at M=1 or at M=2. For every even N>1 choose p=2 and remove its full power, leaving odd M. For every odd N>1 choose any prime divisor and remove its full power, again leaving odd M. This exhausts all positive integers, including arbitrary repeated factors in M and arbitrarily many distinct primes.

## Verdict of this mechanism

The universal derivation is valid subject to the explicitly credited classical identities, whose exact primary statements and proof mechanism were checked. There is no unsupported transfer to another open conjecture and no surviving case of the exact displayed target. Zeros are allowed; strict positivity is already false for the 2-core coefficient of degree 2. The strongest result is the known all-N theorem, not new research. The exact remaining limitation is ordinary imported classical mathematics plus lack of a formal proof assistant certificate or fresh line-by-line typeset journal comparison, neither of which the candidate claims.
