# Additive post-seal positive-characteristic boundary check

UTC: 2026-10-13T03:19:48.398338+00:00

This note is additive and was prompted by Root after the independently authored first assessment and source access/read coverage had been sealed. It does not revise either sealed file, and no positive-characteristic fact is needed for the PR177 characteristic-zero conclusion.

## Narrow result

The standard-form ordinary-polynomial intermediary in the proof of Proposition 4.3, journal p. 707 / PDF p. 27, is false as printed if interpreted as a polynomial over `F_p` in the local braiding arguments, reduced modulo `x_i^p-x_i`. The full printed page was read and visually checked after the first seal, so this is not an extraction ambiguity.

For a fixed two-component oriented link, set

`B_p(L) = binom(lk_12(L), p)`.

The binomial is integer valued for every integral linking number, including negative linking numbers using the usual polynomial binomial formula. As a rational polynomial of degree `p` in an order-one invariant, `B_p` is finite type of order at most `p` over `Q`. Its singular evaluations are integer sums of integer regular evaluations and vanish on `(p+1)`-singular links exactly. Therefore it is also a valid integer-valued finite type invariant of order at most `p`; reduction modulo `p` gives an `F_p`-valued finite type invariant with the same upper bound. This reasoning uses exact zero singular sums, not a reduction of coefficients having noninvertible denominators.

On the non-split positive Hopf-family links `L_n=closure(sigma^(2n))`, compare `n=1` and `n=p+1`. Both links are in the same fixed two-component class. The Hopf generating diagram has one fixed crossing and one odd local replacement parameter `x=2n-1`. Thus the two local parameters are `1` and `2p+1`, and are equal modulo `p`. But

`B_p(L_1)=binom(1,p)=0`,

`B_p(L_(p+1))=binom(p+1,p)=p+1 = 1 (mod p)`.

Every ordinary polynomial over `F_p` in `x` has equal values at these two equal residues. Hence no such polynomial can represent this finite type invariant on this braiding sequence. The claim that standard form modulo `x^p-x` suffices is contradicted for every prime. The odd-prime instances alone establish the boundary without needing to discuss the additional collapse of all odd local arguments modulo two.

The exact integer arithmetic for `p=2,3,5,7,11` is recorded in `MODULAR_BOUNDARY_CHECK.json`; the general identities above prove the assertion for all primes.

## Scope of the failure

This counterexample falsifies the ordinary-polynomial-in-`F_p` intermediary and a verbatim extension of characteristic-zero Theorem 2.1 with that meaning of “polynomial.” It does **not** on its own falsify the final determination statement of Proposition 4.3, its crossing bounds, or the later corollaries: the full braiding sequence of the two-crossing Hopf generator already detects `B_p`. Those statements might admit a proof with integer-valued/divided-power polynomial data or a different argument; no such repair has been proved here.

The characteristic-zero polynomiality used for PR177 remains valid. Over `C`, Newton-binomial denominators are invertible, a finite-order restriction is an ordinary polynomial, and equality at infinitely many integers is polynomial equality. The modular counterexample is therefore a source-boundary finding, not a counterexample to the target construction or a reason to recast this audit as a broad evaluation of the paper.
