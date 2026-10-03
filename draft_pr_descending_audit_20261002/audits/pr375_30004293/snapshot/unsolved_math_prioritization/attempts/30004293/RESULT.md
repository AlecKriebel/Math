# Result: unresolved after five substantive turns

## Original source and the explicit quantitative interpretation

The OWR contribution concerns the infinite set A with independent P(i in A)=1/i and subset-sum representation multiplicities. Its unrestricted supremum is infinite almost surely by a short consequence of credited published lower bounds. That literal correction does not answer the source's intended growth question.

This packet studies the explicitly labeled finite-prefix interpretation

    M(D)=max_x #{C subset A intersect [1,D]: sum C=x}.

The leading question whether log M(D)/log log D converges in probability to a deterministic constant, and what that constant is, remains unresolved. The source does not itself prescribe that exact normalization; even solving it would not necessarily determine all finer growth features.

## Scoped results

- Almost surely, liminf log M(D)/log log D is at least zeta=sup_k log k/log(1/beta_k), with the equality of this supremum to the corresponding large-k limsup proved here. The credited FGK lower bound gives zeta>=eta≈0.3533227727.
- The almost-sure liminf and limsup on that scale are deterministic extended constants. They are not proved finite or equal. Element-cutoff and sum-cutoff versions have the same leading liminf/sup and any finite in-probability limit.
- Each fixed signed-relation length occurs only finitely often almost surely. Eventually every relation has support >c log of its largest entry whenever 0<c<1 and c log(2e/c)<1. Every fixed-cardinality representation maximum is therefore bounded and eventually stable almost surely.
- A self-contained diagonal-quotient flag argument proves M(D)=D^{o(1)} almost surely, then the stronger uniform result

      limsup log M(D) log log D/log D
           <=(log3−1)(log2)^2   almost surely.

  All fixed moments of this larger logarithmic normalization satisfy the same upper constant.
- Exact exponential tilting proves E[M(D)^q]>=c_q D^{2^q−1−q} for every q>1, including liminf E[M(D)^2]/D>=1/96. Polynomial lower tail bounds for rare polynomial-sized peaks explain why raw moments and typical behavior cannot be identified.

These bounds leave a wide gap between the polylogarithmic lower scale and the upper scale exp(O(log D/log log D)). No sharp prefix exponent, exact asymptotic constant, limiting law, original-question counterexample, or complete resolution is claimed.

## Credit and literature boundaries

The FGK annular thresholds, published lower constant, tensor mechanism, and flag framework are credited. The upper beta_2 value recovered in turn 4 is already discussed by FGK and is not presented as new. The 27 September 2026 Mao–Song v2 preprint claims threshold identifications and repairs in the more general entropy framework; its entire proof has not been independently audited here, and none of its claims is used to infer the prefix exponent. Bounds for ordinary divisors or divisor powers have not been transferred to the random-prefix model without proof.

The probability modes are stated theorem by theorem. Almost-sure assertions proved by independent annuli or summable dyadic estimates are distinguished from the primary fixed-threshold convergence-in-probability definition. Finite exact controls check algebra and combinatorics; they do not prove infinite probabilistic assertions.

Status: unsolved, 5/5 substantive author turns. No novelty certification.
