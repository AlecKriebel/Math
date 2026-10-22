# What the controls establish, and what they do not

1. The complete target is unresolved. Every theorem in FULL_PROOF.md has a restricted hypothesis or is explicitly imported from prior work. None produces an orientable exotic pair.
2. verify.py performs deterministic exact-integer/rational checks of intersection-form identities, parity, small matrix ranks, and the formal exceptional-class algebra. It performs no numerical approximation and invokes no symbolic topology oracle.
3. Mayer–Vietoris rank checks only test the stated finite matrices after their topological interpretation has been proved in the text. They cannot prove that an arbitrary input diagram describes a manifold or that an embedding exists.
4. The lattice controls cannot certify homeomorphism or diffeomorphism. The rank-three stabilization matrix does not permit smooth cancellation. Rational signatures alone do not classify integral forms.
5. The controls do not compute Seiberg–Witten, Donaldson or Bauer–Furuta invariants. The gauge-invariant argument relies on a standard blowup formula and a sourced local Kirby-calculus identity. The author's cohomology calculation is restricted to closed simply connected manifolds with b₂⁺>1. No boundary or chamber-free b₂⁺=1 claim is intended.
6. Freedman's classification, Akbulut–Yasui's handle theorem, Gabai's light-bulb theorem and the stated KPR results are external mathematical inputs. Their hypotheses were checked; their complete foundational proofs were not reconstructed or formally verified.
7. AKMR is an author-hosted manuscript; the 2023 CV lists it as unpublished. A peer-reviewed publication of that text has not been verified. Its exact Lemma 2.3 proof and figure were inspected.
8. The direct catalogue is inaccessible (403). The exact target was recovered from the primary 2026 K3 source and pinned corpus. Bounded literature and duplicate searches do not establish the nonexistence of other results.
9. The source PDF/text/images are private research inputs and must not be published. The standalone verify.py controls do not need them or any network.
10. verify_manifest.py checks bytes, not correctness. Replaying the same control program is not an independent mathematical audit. That audit remains pending at author freeze.
11. The five-turn limit is exhausted. Review can verify or correct the fixed deductions; further unrecorded proof search is not authorized by this package.
