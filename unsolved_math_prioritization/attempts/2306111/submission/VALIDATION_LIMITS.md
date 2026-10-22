# Validation limits and checks

The author has checked the mathematical derivations for branch choices, B=0 continuity, parameter boundaries, the distinction between univalence and starlikeness, and strictness for the closed coefficient ball. This is an author self-check, **not independent verification**.

The elementary control script tests finite identities and examples. It does not formalize the proofs. Its key negative control takes A=0,B=-1,eta=3/5>delta=1/2; the explicit perturbation loses local univalence at a certified rational bracket 4/5<r<9/10.

The main finite search has 15 fixed parameter pairs, three atoms, angles in [0.001,2pi-0.001], raw weights in [0,10] with third raw weight 1, 128-point Gauss–Legendre quadrature, and 256-point rechecks. Differential evolution uses population multiplier 10, maximum 160 iterations, tolerance 1e-9, polishing and one worker. All seeds, evaluation counts, optimizer statuses and library versions are preserved. No strict numerical ratio below 1-1e-7 was found. This is not a proof that a counterexample does not exist.

The preliminary search varies beta in [0.001,1.999] at B=-1, uses the same three-atom weight and angle parameterization, 128-point quadrature, four seeds (0–3), population multiplier 14, maximum 200 iterations, tolerance 1e-10 and polishing. Its output is preserved separately. It uses the direct eigenvalue formula and is more vulnerable to cancellation than the stabilized formula in the later main search. Neither method uses validated intervals.

Mathematical scope limits:

- Sharpness is proved, but the exact lower starlikeness inclusion remains unproved.
- The Herglotz representation is complete only at B=-1; its finite-atomic version is a certified subclass for B>-1, not an asserted representation theorem for the whole class.
- A boundary sample below one would require rigorously controlled evaluation and an interior continuation before being called a certified counterexample.
- No finite support-reduction theorem or global optimizer certificate has been proved.
- The smaller-disk deduction depends explicitly on the restricted-range theorem stated in the primary problem source.
- Fournier 2020's full text was not obtained. Current complete literature status and novelty are unverified.
- Hash checks certify bytes, not mathematics, authorship, originality, or publication readiness.

No source PDF, raw corpus, extracted source text or screenshot is part of the author publication set.
