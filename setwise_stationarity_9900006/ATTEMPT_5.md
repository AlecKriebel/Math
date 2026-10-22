# Attempt 5: necessity and cost of the subsequence/randomization quantifiers

2026-10-20. This attempt seeks a simpler finite-time version of Attempt 3. It proves two obstructions, rather than assuming its universal subsequence quantifier or growing random-time supports can be dropped.

## 1. Random-time couplings along the original sequence alone do not characterize setwise convergence

Let S={0,1}^{N₀}. Let x⁰=(0,1,0,1,...) and x¹=(1,0,1,0,...), let μ=δ_{x⁰}, and let ν=(δ_{x⁰}+δ_{x¹})/2. The measure ν is stationary, and μ_n alternates between the two point masses. In particular μ_n({x:x₀=1}) alternates between zero and one and does not converge to ν's value 1/2.

Nevertheless, for each j choose T_j independently of X, equally likely to be 2j or 2j+1. Then θ^{T_j}X has law ν EXACTLY. Taking Y_j=θ^{T_j}X yields perfect full-path coupling, with no failure at any j, and preserves the full original X. Thus the existence of arbitrarily late independent random times and perfect comparison with ν-law variables, on its own, is strictly too weak. Requiring large uniform averaging windows also fails: choose any even window length, and its uniform mixture is exactly ν.

The universal subsequence requirement in Attempt 3 excludes this example: on the even subsequence, every mixture remains δ_{x⁰}. It is not cosmetic and cannot be replaced just by the single original time sequence.

## 2. No uniform finite bound on random-time support suffices

Return to the Bernoulli invertible-orbit example in Attempt 1. Its stationary reference ρ is fair product measure on {0,1}^Z; initial density is f(z)=2·1_{z₀=1}. On the initial-state space, the law at time n has density

    f_n=1+ε_{−n}, where ε_i=2·1_{z_i=1}−1.

Distinct ε_i are independent symmetric signs. The orbit embedding Φ preserves TV because its zeroth-coordinate projection is a measurable left inverse. Thus a finite mixture of m distinct shifted full-path laws with weights a_i≥0, Σa_i=1, has distance from ν exactly

    δ=(1/2) Eρ |Σ_{i=1}^m a_i ε_{−n_i}|.

Set W=Σa_i ε_{−n_i} and v=Σa_i². Independence gives E W²=v and

    E W⁴=Σa_i⁴+6Σ_{i<r}a_i²a_r²=3v²−2Σa_i⁴≤3v².

Hölder's inequality applied to |W|²=|W|^{2/3}|W|^{4/3} gives

    E W²≤(E|W|)^{2/3}(E|W|⁴)^{1/3}.

Rearranging yields E|W|≥v^{3/2}/(E W⁴)^{1/2}≥sqrt(v/3). Cauchy–Schwarz gives v≥1/m. Consequently

    δ≥1/(2 sqrt(3m)).

For equal weights the reverse bound E|W|≤sqrt(EW²)=1/sqrt(m) gives δ≤1/(2sqrt(m)). Thus the random-time support size required to bring the mixture within δ of ν grows at order δ^{-2}, up to constants.

For ANY coupling with a measurable success event on which the two full paths agree, its failure probability is at least δ: for every event A the difference of marginal probabilities is bounded by that failure probability, and taking the supremum gives TV. Therefore no coupling trick avoids this support-size lower bound. In particular, setwise convergence does not imply the random-time characterization with support sizes uniformly bounded in j. The finite support in Attempt 3 must be allowed to grow.

This result is exact for full paths, not just a bound for a finite coordinate projection. The computation uses the measurable inverse of the orbit embedding to identify the full-path TV distance with the state-space density calculation.

## 3. What this leaves

For this particular independent-random-time criterion, deleting its universal deterministic subsequence requirement or imposing a uniform bound on the sizes of its finitely supported sampling distributions is invalid. This is not a claim that every conceivable coupling characterization must have those features. The simpler alternatives fail in explicit standard Borel examples, so weakening to general measurable states cannot rescue them.

No single original-process/stationary-process orbit characterization has been proved. No literature-priority or resolution claim is made. The complete positive theorem obtained in these attempts is Attempt 3, whose varying stationary comparison copies and per-subsequence choice must always be disclosed.
