# Problem 2306044 / AMR-022-6044 / Function Theory 6.44

**Disposition: already_solved, negative answer.** Hayman–Lingham Update 6.44 credits Bshouty (1980). This packet supplies an independent reconstruction of a counterexample using a finite real Loewner flow and the classical Fekete–Szegő inequality. It claims no new resolution or historical priority.

The constructed function belongs to the normalized real-coefficient univalent class and has second and third coefficients `3/sqrt(e)` and `1+5/e`. Its weighted self-convolution violates a necessary coefficient inequality for univalent functions by an explicitly positive amount.

- [Complete argument](proof.md)
- [Sources and verification limits](sources.md)
- [Attempt log](approach_log.md)
- [Reproducible checks](controls/verify.py)
- [Machine-readable disposition](status.json)

Run `python3 controls/verify.py` from this directory. Python 3.10+ standard library suffices. Results are deterministic; the script checks exact finite algebra, rigorous rational bounds on the numerical margin, negative controls, and supplementary ODE approximations. It does not mechanically prove global univalence or the cited coefficient theorem.

One substantive reconstruction/verification turn was used. The argument is subject to independent audit; computational checks do not constitute peer review.
