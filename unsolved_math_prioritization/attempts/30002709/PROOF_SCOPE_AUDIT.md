# Proof and hypothesis correspondence

This is a reading audit of the published proof and elementary notation matching, not an independent new proof of Knaf's conjecture.

## Dependency map checked in Datta

Theorem1.2's equivalences use Knaf's necessary condition and the classical unique-extension integral-closure criterion for the henselian step. The difficult direction is descent from W^h finite over V^h. The complete Section3 proof, the valuation descent lemma, and the final argument were read.

The proof uses the integral closure A of V in F. Its henselian base change splits into the henselizations of the local rings at A's finitely many maximal ideals (Proposition3.6). Finite V-subalgebras B with fraction field F and separating those maximal ideals form a filtered approximation (Corollary3.7). The relevant localized base changes inject into the selected local factor. Finitely many module generators of W^h lie in one such stage. Faithful-flat descent then makes B_(B∩m_W) a valuation ring of F. Domination by W forces equality. The finite algebra B is torsion-free, hence flat over V; the cited finite-presentation result completes the stronger assertion.

This checks the actual missing sufficiency mechanism. It does not confuse an arbitrary noninjective tensor product with a filtered union of subrings; Corollary3.7 establishes precisely the needed injections. It also does not assume the integral closure A is already finite.

## Critical boundaries

1. A local extension of valuation rings is automatic from restricting the given valuation, and the fraction-field extension is finite. These are exactly the theorem's hypotheses.
2. No assumption that V is Noetherian or that F/L is separable is used. The henselization argument retains arbitrary finite extensions.
3. For multiple valuations, compatible henselizations isolate one field factor; [F:L] does not replace its degree. Datta Definition4.8 and the corrected original conventions use this distinction.
4. A localization of a finite V-algebra can fail to be a finite V-module. The theorem's finite B must not be identified with W itself.
5. Torsion-free modules over valuation rings are flat; an arbitrary such module need not be free. The general “free” wording in the preprint's introductory convention paragraph is not used. The proof correctly uses flatness; its finite torsion-free algebra B is indeed finite free. No stronger freeness assertion is carried into this packet.
6. The initial-segment quantifier is universal over all positive base values. For a dense rank-one base group it can contain only0, even when e>1. Finite rational samples are diagnostics, not proofs of an infinite ordered-group classification.

The tests in verify.py check these convention distinctions in elementary finite models and the split-prime polynomial. They are not a computational proof of Datta's theorem. The classification is a credited published input whose proof and full scope have been inspected.
