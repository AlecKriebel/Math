# H1: distinguish the finite-cutoff hybrid mean from the full Euler mean

The frozen §5 statement that the prime component has local mean (1) needs a qualifier. This is a publication wording correction; it changes neither (H) nor its constants. It does not supply a proof of joint growing-cutoff/time averaging.

## A concrete inequality

For the conductor-one character, weight one, and prime two, the sharp prime component at cutoff X=2 is exp(z). Its local mean on |z|=1/sqrt(2) is

    J_(2,2) = sum_{r>=0} (1/2)^r/(r!)^2.

Since 1/(r!)^2 <= 1/4 for every r>=2,

    J_(2,2) <= 1+1/2+(1/4) sum_{r>=2}(1/2)^r = 13/8 < 2 = J_2.

The definition also gives the identical prime-two factor at X=3. That example is inside the stated theorem's X>2 parameter range. The X=2 example is an elementary boundary definition, not an assertion that Sahay's theorem applies at its excluded endpoint. Both rule out literal exact equality at a finite cutoff. The own runtime checks use the in-range X=3 example.

## Exact primary definition and its correction

Sahay v3, printed pp.5–6, defines the prime factor by a sharp sum over n<=X, multiplied by the finite primitive Euler deletions. The support of u_X belongs to the zero kernel U; no v_X weight occurs in that displayed prime sum. The following argument uses this exact definition.

For each prime p<=X put K=floor(log X/log p). On |z|<1, define

    D_(p,X)(z) = product_i (1-psi_i(p)z)^(a_i 1_{p|q_i})
                  * exp(sum_i a_i sum_{j=1}^K psi_i(p)^j z^j/j),
    J_(p,X) = (1/(2pi)) integral_0^(2pi)
                  |D_(p,X)(exp(i theta)/sqrt(p))|^2 d theta.

The powers are the branches analytic at zero. This is the actual joint local phase mean of the sharp hybrid prime component, with the deletions retained. The full Euler local function B_p in (1) is its limit at a fixed p as X increases, rather than an exact finite-X identity.

## A rigorous Euler-phase limit, without a time/cutoff interchange

Put A=sum_i a_i. For the truncated exponential, coefficientwise absolute values are bounded by those of (1-z)^(-A): each truncated logarithmic coefficient is bounded by A/j, and exponential series multiplication preserves the positive majorant. For a deletion factor, the absolute coefficients of (1-u z)^a are bounded by those of (1-z)^(-a), because |(-a)_r| <= (a)_r for a>=0 and |u|<=1. Consequently D_(p,X) has the uniform coefficient majorant (2A)_r/r!, including exceptional primes. Away from those finitely many primes the sharper A-majorant suffices.

Since K>=1, the coefficient of z in D_(p,X) is exactly sum_i a_i chi_i(p), the same as that of B_p. Parseval and the polynomially bounded majorant imply, uniformly for p<=X,

    J_(p,X) = 1+|sum_i a_i chi_i(p)|^2/p + O_A(p^-2),
    J_p     = 1+|sum_i a_i chi_i(p)|^2/p + O_A(p^-2).

Both means are at least one. Thus their positive ratio is 1+O_A(p^-2). At a fixed prime, K tends to infinity; the logarithmic series converges uniformly on the circle of radius 1/sqrt(p), and the fixed deletion factors are continuous there. Hence J_(p,X)/J_p tends to one. The same majorant justifies this fixed-prime limit by dominated series convergence.

Extend the ratio to be one when p>X. For all sufficiently large p its logarithm is bounded by C_A/p^2, independently of X; the finitely many small-prime logarithms tend to zero. Dominated convergence over the countable primes therefore gives

    product_{p<=X} J_(p,X)/J_p -> 1.

For X beyond every prime dividing Q, this is also the complete ratio for the finite deletion factors. Mertens' theorem and the already defined prime-ordered arithmetic constant then give the Euler-phase-model asymptotic

    product_{p<=X} J_(p,X)
        ~ product_{p<=X} J_p
        ~ A_arithmetic * (exp(gamma) log X)^E.

This is a statement about local phase models as X increases. For each fixed finite cutoff, long-time phase equidistribution gives its exact finite-prime average. It does not authorize taking X=X(T) in that statement: a growing-cutoff critical-line mean still requires the declared hybrid model hypotheses.

## Exact proposed replacement for the start of §5

> For a fixed cutoff X, the sharp hybrid prime component has joint local phase mean J_(p,X), defined from its truncated exponential and the primitive Euler deletions. Formula (1) is the full Euler local mean J_p, and J_(p,X) tends to J_p at each fixed prime as X increases. Their first coefficients agree, and their remaining mean difference is uniformly O_a(p^-2); hence the product of local ratios tends to one. Fixed finite-prime phase equidistribution is exact. Replacing the long-time average by the resulting phase-model asymptotic while X grows with T remains a hybrid-model assumption.

Use (9) after that replacement. The diagonal exponent, arithmetic constant, Barnes-G constant, finite deletion correction, and all stated model limitations remain unchanged. The correction leaves no additional unsupported central application beyond the statistical hypotheses already explicitly stated in the frozen note.
