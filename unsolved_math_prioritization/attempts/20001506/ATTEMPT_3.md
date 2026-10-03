# Turn 3: constructing the top attracting line without a relative-train-track shortcut

Date: 2026-10-03. This is a new direct proof construction for the credited depth-gap claim, not a claim that the depth gap itself is new. It repairs the explicit-representative gap isolated in SOURCE_GATE.md and then tests whether this suffices for the original QI target.

## A positive-substitution attraction criterion

Let theta be a positive automorphism of a finite-rank free group. Assume every generator image has length at least 2 and theta(x)=P x S, with P,S nonempty positive words. Place the distinguished x at coordinate zero and nest gamma_n=theta^n(x) through this occurrence. The resulting line is

    ell = ... theta^2(P) theta(P) P x S theta(S) theta^2(S) ... .

Suppose each of theta^n(P),theta^n(S) contains x for all sufficiently large n. Then every gamma_m, and hence every finite segment of ell, occurs in infinitely many left and right annuli. Thus ell is birecurrent.

Let C be a bounded-cancellation constant for theta on the unit-edge rose. Choose N large enough that both distances from the distinguished x to the ends of gamma_N exceed C, and |theta^N(P)|,|theta^N(S)|>C. These quantities go to infinity by positivity and the minimum expansion. If a reduced bi-infinite line contains gamma_N, applying theta and tightening removes at most C letters from either end of theta(gamma_N); the central copy of gamma_N survives. Thus the cylinder U of lines containing gamma_N satisfies theta(U) subset U.

Under repeated application, the surviving left and right radii around the distinguished copy of x grow at least by r↦2r-C. The added P,S only improve this estimate. Starting at r>C, both radii go to infinity, and all surviving central segments are segments of ell. Consequently for every finite segment beta of ell there is k with theta^k(U) contained in the cylinder of beta. The line ell itself belongs to every theta^k(U), since its unbased image is ell. The images are open because an automorphism acts by a homeomorphism on line space. They therefore form a neighborhood basis of ell.

This verifies the birecurrence and attracting-neighborhood definition of a generic line, as recalled in Appendix A of Dowdall et al., arXiv:2602.10433. No relative-train-track assertion about the original rose is needed. The bounded-cancellation theorem used here is standard; a quantitative bound BCC(f)≤Lip(f)vol(T) is recorded in Francaviglia–Martino–Syrigos, Lemma 2.34, https://aif.centre-mersenne.org/item/10.5802/aif.3747.pdf .

## Application to the exact upper map

Take theta=phi^3. Its positive images are

    a→ab, b→bc, c→cab, d→edeac, e→edeaedb.

Choose theta(e)=(ed) e (aedb), so P=ed and S=aedb. Both contain e, and theta preserves an e in every subsequent image. The criterion applies. Here Lip(theta)=7 and the rose volume is 5, so C=35 is a valid conservative bound. For gamma_3=theta^3(e), the distinguished e has 73 letters to its left and 88 to its right; the whole word has length 162. Also |theta^3(P)|=267 and |theta^3(S)|=288. Hence N=3 is already a fully explicit attracting-cylinder choice.

Let Lambda_top be the weak closure of this generic line. It is an attracting lamination for phi, since the generic-line definition permits a positive power.

## The lower lamination and proper containment

For the lower map, alpha^5(a)=c a b provides the same construction with x=a, P=c, S=b. Every image under phi^5 has length at least 3. Primitivity of the lower substitution makes both end annuli eventually contain every lower generator, hence makes the constructed lower line birecurrent. The same bounded-cancellation argument applies in the full five-generator rose, even to lines with upper letters outside the chosen lower core. Thus its closure Lambda_low is an attracting lamination for phi as well as the unique attracting lamination for alpha.

The upper line contains every theta^n(e). Since theta(e)=edeaedb contains a, theta^(n+1)(e) contains theta^n(a). The lower transition matrix is primitive, so every finite lower-lamination word occurs in some theta^n(a). Hence every finite segment of a lower generic line occurs in the upper generic line, which is precisely the weak-closure inclusion

    Lambda_low subset Lambda_top.

It is strict: the upper line contains d,e, whereas every lower-lamination segment uses only a,b,c and their inverses. The upper line is also nonperiodic: it has top letters and arbitrarily long lower-only subwords, impossible for a periodic line containing a top letter.

Therefore delta(alpha)=1 and delta(phi)≥2. The uniqueness/depth-one assertion for alpha is the credited fully irreducible example in Behrstock–Bestvina–Clay, Example 5.24. We do not claim delta(phi)=2 without an exhaustion argument for all attracting laminations.

## What this completes, and what it does not

Corollary 5.7 of Dowdall et al. now yields a properly supported noncommensurability consequence for this exact pair. This is a reconstruction of the supplied prior partial result. The 2026 theorem does not make lamination depth a quasi-isometry invariant. The extra implication needed to finish AIM Conjecture 3.4 remains open in the sources checked; this turn does not claim it.

## Verification

verify_t3() recomputes theta, the distinguished-center margins, the explicit cancellation bound, and finite lower-language containment controls. These finite tests support but do not replace the all-n attraction and recurrence proof above. No PDF or source transcription is included in the packet.
