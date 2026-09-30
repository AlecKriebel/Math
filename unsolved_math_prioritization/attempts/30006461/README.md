# Multiplication-table limit profile: unresolved Fourier obstruction

[OBSTRUCTION.md](OBSTRUCTION.md) records one unsuccessful Fourier-based approach to the exact arithmetic nonconstancy conjecture. The known kernel reduction is credited to Green–Sawhney. Explicit negative controls show why positive nonuniform factors and nonconstant finite approximants do not suffice. The common nonzero Fourier mode of the actual arithmetic measures remains unproved.

The full original contribution was recovered; [SOURCES.md](SOURCES.md) distinguishes its multiplication-table announcement from the full permutation-model manuscript and fixes the reflected-kernel and phase conventions. No full solution or novelty is claimed. The scoped claims passed [separate adversarial AI review](review/REVIEW.md). This does not resolve the original conjecture. Human peer review has not occurred.

Run `python3 verify.py` here. All 3,864 exact assertions pass, covering elementary rational Fourier and root-of-unity controls. The checker does not compute the arithmetic measures or decide the conjecture. One substantive attempt was used; work stopped at the precise unresolved measure identification and nonvanishing gap.

The copied independent checker passes 4,204 assertions. Run `python3 review/independent_checks.py`; its preserved adjacent `OBSTRUCTION.md` is a required frozen-hash dependency.
