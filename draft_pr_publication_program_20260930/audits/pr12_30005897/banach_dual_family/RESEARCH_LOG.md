# PR12 Banach and duality audit log

Scope: independently audit the exact supplied candidate, chiefly Lemma 2.1,
the pointwise localization, and the converse for arbitrary real/complex Banach
spaces. This is a review of an existing result, not a new research program.
No external communication, git mutation, or canonical source edit is authorized
for this family. All audit deliverables stay in this folder. Any downloaded
source will stay under ignored `tmp/`.

## 2026-10-01 05:34:38 UTC — initiation; 0% audit completion

Read `source_snapshot/PROOF.md` and reconstructed the complete theorem before
opening any prior reviewer findings. The candidate asserts equivalence of
two-sided shadowing, generalized hyperbolicity, and a uniform pointwise density
drop on every orbit coordinate for dissipative invertible composition
operators on scalar L^p, 1 <= p < infinity. The candidate includes real and
complex spaces and makes no separability assumption.

## 2026-10-01 05:35:40 UTC — first reconstruction; 35% audit completion

Verified the dual telescoping endpoints independently: a finite adjoint orbit
segment gives exactly K(a_a + a_{b+1}), not K(a_{a-1} + a_b). The contradiction
argument using [-d,d-1] and the d-1 symmetric pairs is arithmetically consistent.
No norm attainment, reflexivity, or separability is used. The proof hash equals
the source manifest: `f38ae2dd97bb2aeb8f1e97da0f4133b84b6d43d803e2b38df2c91acc56817a8e`.

Assigned an independent subagent to challenge the noncommuting-projection
Green formula in Section 6. Pending work: make all forcing/shadowing constants
explicit, challenge endpoint L^1 dual localization and trivial bands, inspect
measure-theoretic assumptions, and build reproducible boundary probes.

## 2026-10-01 05:38:00 UTC — source/endpoint checkpoint; 65% audit completion

Independently inspected the primary OWR report and arXiv:2009.11526 through
the web reader. The source uses scalar L^p for 1 <= p < infinity, a finite
positive wandering set, invertibility with both nonsingularity bounds, and
two-sided pseudotrajectories without a boundedness restriction. Its 2024
generalized-hyperbolicity definition uses spectra inside the unit disk.
The candidate matches these assumptions and explicitly extends the separable
complex presentation to arbitrary real/complex scalar L^p spaces.

Rechecked localization at p=1: the full Banach dual is L^infinity because the
product measure is sigma-finite, and a positive-measure indicator has norm
one. Countable unions suffice for the common exceptional null set. No Bochner
duality or fiberwise choice of shadowing solutions is being used.

The independent Green-formula subagent reports PASS with an exact finite-tail
identity, an explicit noncommuting weighted-shift example, and an explicit
uniform forcing constant. The final report will independently check those
details and make scope/optional exposition recommendations. No mathematical
counterexample has emerged. Pending: exact-arithmetic adversarial probes and
the consolidated report/verdict.

## 2026-10-01 05:43:10 UTC — complete derivation draft; 90% audit completion

Wrote `REPORT.md` with full checkable forcing/shadowing equivalence, the exact
dual endpoint residuals, all quantitative estimates, the sigma-finite scalar
L^p duality and real/complex conventions, and the Green truncation identity.
Also reconstructed the measurable-band argument to test the full theorem's
dependency on the audited steps. No blocking mathematical defect was found.

The exact-rational program now passes 77 dual endpoint checks, 168 Green
truncation identities on a shift with noncommuting projections, 48 explicit
bad-fiber witnesses, and one L^infinity masking/localization example. A first
probe run failed due to stored zero coordinates comparing unequal to an empty
dictionary; removing zero entries in the probe's forcing representation fixed
that test-artifact error. The mathematical Green identity was unchanged.

Recorded analytic material-hypothesis counterexamples: individual strict
contraction fibers do not imply a uniform operator shadowing constant;
eta=1 and spectral radius <=1 permit unbounded accumulation of forcing.
Pending: adversarial review of the audit report itself and final artifacts.

## 2026-10-01 05:47:22 UTC — adversarial report review complete; 100% audit completion

The independent subagent expanded its adversarial check to the consolidated
report, reproduced every exact-rational probe, and independently rederived
the density bounds, uniform-fiber counterexample, equivalent real/complex
renorming, and support-band argument. Its verdict is PASS with no mathematical
gap found. It identified a factual provenance wording error: it read the whole
candidate before auditing Section 6, rather than reading only that section.
Corrected that sentence in the report; no mathematical source change was made.

Final artifacts: `REPORT.md`, `verdict.json`, `green_check.md`,
`adversarial_probes.py`, `probes_result.json`, and this log. All writes remained
inside this audit folder. Source proof hash remains unchanged. No git operation,
external communication, canonical edit, or new priority claim was performed.

Strongest verified result: the full Sections 1–6 theorem and pointwise criterion
are mathematically supported under the candidate's explicit scalar finite-p,
real/complex, sigma-finite dissipative assumptions; Lemma 2.1 and the Green
converse hold on arbitrary real/complex Banach spaces. No blocking repairs.
Optional exposition clarifications are recorded. Literature/priority and the
recent-paper assertions in Sections 7–8 remain outside this family's verdict.
