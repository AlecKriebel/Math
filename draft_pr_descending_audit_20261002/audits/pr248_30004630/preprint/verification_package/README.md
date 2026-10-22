# Critical-wave quadratic-growth counterexample: verification package

Author: Alec Kriebel; ORCID 0009-0001-9320-500X. Version 1.0, 2026-10-14 UTC.

The separate six-page PDF proves the explicit negative answer to retaining the source ordinary-critical-cone strict-positivity implication to strong control-L2 quadratic growth after deleting beta2>0. Its cone is {0}; the strict condition is vacuous. A small positive constant cap gives a unique global optimizer. The actual nonlinear state is not confined to one eigenmode. Every fixed finite nonnegative terminal-velocity weight is allowed. The radial comparison neighborhood may depend on that weight; arbitrary-target upper estimates are uniform in the weight.

The paper also proves local L1 quadratic growth and fixed-basepoint optimizer estimates. It does not claim pairwise Lipschitz selection, perturbed uniqueness, L-infinity optimizer convergence, a sharp exponent, or a complete unregularized replacement theory. Classical concentration/noncoercivity, sparse threshold calculus and wave estimates are credited.

## Reproduction

Use Python 3.11 or later. The reference environment used Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0. Install the two pinned packages:

```text
python -m pip install -r requirements.txt
python verify_all.py
```

The runner first checks every packaged file against FILE_MANIFEST.json, then executes all seven checksets in separate temporary directories. It compares every field of each complete parsed receipt with its reference, excluding only the top-level informational `utc` and `python` fields. Dependency-version fields, all scientific values, category counts, assertions, diagnostic samples and stated limitations are compared. Runtime version is recorded in the resulting report; exclusion of Python text allows the explicitly supported Python versions. For scripts emitting a file, that complete receipt is read and compared; their temporary absolute output path is informational.

Total: 5,603 exact finite assertions plus five noncertified high-precision diagnostic assertions. These check eigenmode identities, pulse integrals, remainder orders, capped moment controls, weaker-norm algebra and threshold estimates. They do not solve a discretized nonlinear PDE, certify a numerical Strichartz constant, replace the analytic proofs, or certify priority. The universal inequalities and all optimizer quantifiers are proved analytically in the manuscript and derivations.

The standalone manuscript source can be compiled with an ordinary LaTeX toolchain. The delivered PDF was exported with Tectonic and all six pages were rendered with Poppler and visually inspected. The source also compiled successfully with the Codex desktop LaTeX compiler.

## Evidence and provenance

`original_submission/` preserves all 19 original files byte-for-byte at native PR head e9c5d10978764db2cf25fa7d49cf4bd14a82d604. Its early unreviewed headers and statuses are historical, not the current review outcome. `audits/` preserves the independently authored mathematical and bounded priority evidence used to develop this note. Source manifests intentionally bind excluded private reading copies; this portable archive does not redistribute whole external PDFs, extracted text, figures or provider responses. Those omitted files are not required to run the seven checksets. The relocated historical_snapshot_01 manifest shares four unchanged input/checker files with its parent audit-family directory; their exact preserved bytes remain in that parent directory. Some audit-only paths refer to the original workspace; the reproduction runner uses only paths inside this archive.

Priority findings are bounded. No earlier authenticated complete or automatically covering negative wave construction was located. Generic failure mechanisms were already known. In particular, applying an old conditional NDC theorem to the newly constructed data does not date the construction to that theorem. Inaccessible original/final publisher bodies and deposit/history searches are documented in the priority reports. No worldwide-firstness claim is made. Dunn's example was checked through the cited Casas-Tröltzsch reproduction, not through an obtained original chapter.

The paper uses a direct compatible-state contraction/local residual. It does not rely on the printed source proof's claimed surjectivity onto arbitrary continuous energy pairs. The direct pulse computation handles both source localizations; the older L2-neighborhood NDC theorem needs an explicit restricted-cap step to handle an L-infinity neighborhood, as the bridge audits explain.

AI tools were used extensively in solving, derivation, independent internal adversarial audits, exact computation, literature research and writing. This is an unrefereed research note without external human peer review or proof-assistant formalization. Later manuscript-review reports are separate repository evidence so that this reviewed scientific payload can remain immutable.

`FILE_MANIFEST.json` excludes itself to avoid recursive hashing. `verify_all.py` writes its final report outside the packaged file set, in the invocation directory. No network, repository mutation or outreach is needed for reproduction.
