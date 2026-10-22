# Independent derivation and deliberate failure cases

This is a written mathematical check, not a computational proof of universal quantifiers. It was produced independently while reviewing the exact pinned PR1272 proof. The finite diagnostics supplement the deductions below.

## Exact claim

For a nonempty compact subset X of the complex plane, let R be the algebra of global rational functions with no pole on X. The same object can be described as the germs near X of those rational functions; it does not mean all independently specified holomorphic germs on components. Let positive weights satisfy M_0=1, M_(j+k) >= binomial(j+k,j) M_j M_k and sum(M_j/M_(j+1)) < infinity. Define ||r|| = sum_n ||r^(n)||_X/M_n. The claim is that this is a finite algebra norm and its abstract Banach completion A has character space X, including its topology. A is not asserted to embed injectively in C(X).

## Weight implication without regularity assumptions or Stirling

Put rho_j=M_j/M_(j+1). For any fixed N and n>N, let T_N=sum_(j>=N) rho_j. Positivity and tail summability give 0<T_N<infinity and T_N tends to zero. Telescoping and finite AM-GM give

    1/M_n <= (1/M_N) [T_N/(n-N)]^(n-N).

Since n! <= n^n,

    (n!/M_n)^(1/n)
      <= M_N^(-1/n) T_N^((n-N)/n) n/(n-N)^((n-N)/n).

For fixed N the last factor tends to 1: its logarithm is log(n/(n-N))+(N/n)log(n-N), which tends to zero. Thus limsup_n(n!/M_n)^(1/n) <= T_N. Let N tend to infinity. Nonnegativity proves that the limit is zero. The PR's sharper constant 1/e, obtained with Stirling, is also correct but unnecessary. There is no log-convexity, ratio monotonicity, or interchange of N and n hidden in this argument. The binomial condition is not used here.

## The actual algebra exists

For r in R choose a positive common radius delta whose closed discs about X stay away from all its poles, and bound r on their compact union by C. Cauchy's estimate gives ||r^(n)||_X <= C n! delta^(-n). The preceding root limit makes the sum finite, by the root test. Every rational inverse needed below is therefore genuinely in the normed algebra.

If ||r||=0, every derivative vanishes at any chosen x in X. Its Taylor series vanishes on a disc; the identity theorem for the rational function makes r identically zero. This works for singletons and finite sets because rational functions, rather than their value restrictions, are the starting algebra. Triangle inequality and homogeneity are termwise. Leibniz's rule and the binomial hypothesis imply

    ||(rs)^(n)||_X/M_n
      <= sum_(j=0)^n [||r^(j)||_X/M_j] [||s^(n-j)||_X/M_(n-j)].

Nonnegative-series summation proves submultiplicativity. Completion extends multiplication and the unit of norm1. The coordinate u belongs to R, since only its zeroth and first derivatives survive. No geometric regularity or differentiability-space completeness is assumed.

## General rational-generator lemma

Let any unital complex Banach algebra A have a dense rational algebra in one element u, with all rational inverses having poles outside a nonempty compact X present, and bounded evaluations at every point of X. Then every complex character is evaluation at a point of X.

Indeed a nonzero algebraic complex-linear multiplicative map chi has chi(1)=1. If |chi(a)|>||a||, the element a-chi(a)1 is Neumann-invertible, whereas applying chi to the inverse identity gives 0=1. Therefore |chi(a)|<=||a||, even before continuity was assumed. Put lambda=chi(u). If lambda is outside X, (u-lambda) has the inverse rational function 1/(z-lambda), again forcing 0=1. Thus lambda is in X. For every p/q with q zero-free on X, chi(p(u)/q(u))=p(lambda)/q(lambda). Boundedness and density identify chi with the extension of evaluation at lambda.

In the present weighted algebra evaluations are contractions because M_0=1. They extend multiplicatively by the continuous product, and are nonzero on1. Outside resolvents have the explicit norm bound

    ||1/(z-lambda)|| <= d^(-1) sum_n n!/(M_n d^n),
    d=distance(lambda,X)>0.

The series converges by the established root test. In fact sigma_A(u)=X: the inverse proves one inclusion, and evaluation at x prevents u-x from being invertible for the other. Neither semisimplicity nor polynomial density was used. The general lemma is an elementary Banach-algebra deduction; this review does not assert a first publication of its arbitrary-completion formulation.

## Topology, ideals and value realization

Restriction R -> C(X) has norm at most1, hence extends to a continuous algebra homomorphism J:A -> C(X). Each J(a) is a uniform limit of rational value functions and is continuous. Consequently x -> evaluation_x is weak-star continuous. It is injective because u separates points, surjective by the lemma, and therefore a homeomorphism (compact domain, Hausdorff codomain).

The standard Gelfand-Mazur identification of maximal ideals with complex characters in a commutative unital complex Banach algebra does not require a zero radical. Their intersection is the Jacobson radical, so rad(A)=ker(J). This is an exact equality, not a presumption that J is injective. The quotient A/rad(A) is a well-defined Banach algebra of value functions with its quotient norm; that quotient norm need not retain the originally displayed derivative norm on value restrictions.

For an already well-defined complete Banach function algebra with this rational norm and rational density, the same proof works directly. A perfect-set Dales-Davie space, when complete, supplies one such ambient algebra for its rational closure. No proof of rational density in the whole differentiable space is supplied or needed for the rational closure question. The printed source's claimed existence of a value-function algebra on arbitrary compact sets is ambiguous at isolated points; the explicit abstract-completion convention resolves that issue for the proved statement but must remain disclosed.

## Falsification controls

1. Singleton X={0}, M_n=(n!)^2. The weight inequalities hold; the ratio series is sum1/(n+1)^2. The element u has norm1 but zero values. For n>=0, ||u^n||=1/n!, since just the nth derivative survives at0. Thus u is nonzero quasinilpotent and lies in the radical, although the character space is just {0}. This refutes any universal injectivity/semisimplicity reading, not the proved character claim.
2. Finite or isolated-point sets cannot be handled by identifying two rational functions solely from equal values there while retaining the displayed derivative norm: u and0 already collide at the singleton. Rational functions/germs and their values must be distinguished.
3. Binomial weights alone are insufficient: for M_n=n!, the singleton norm of a polynomial is the coefficient l1 norm, the root ratio is1, and the resolvent with pole at1 has a divergent sum of derivative terms all equal to1. This violates the summable-ratio assumption and exposes the necessity of proving full-norm resolvent finiteness.
4. Polynomial density cannot replace rational density: the disc algebra viewed on the unit circle has characters at interior points as well. On the rational algebra, the inverse of u excludes the interior point0. There is no such inverse in the polynomial closure. This is an elementary mechanism check, not a counterexample under the hypotheses.
5. For X empty, the displayed formula is only a seminorm after choosing the supremum of a nonnegative empty family to be0. Its zero-seminorm quotient is the zero algebra, with no nonzero characters. The main unital nonempty theorem does not silently prove or assume this convention.

## Outcome

No substantive mathematical defect in the pinned PR theorem was found. Its category and empty-set qualifications are essential and accurate. The original literal rational-closure question is addressed in the explicit completion convention; replacing it by the unrestricted full Dales-Davie algebra would ask a stronger problem. Correctness of this elementary argument does not establish historical firstness or that a particular earlier DOI printed the all-compact abstract version.

The work and this review extensively use AI. They have no external human peer review or formal proof-assistant certification.
