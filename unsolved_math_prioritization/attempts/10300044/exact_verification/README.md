# Verification and audit supplement

This accompanies Alec Kriebel, *Unbounded Godbillon--Vey numbers on a fixed hyperbolic manifold*, 13 October 2026. It documents a complete mathematical negative answer to the literal Question 10.6 of Calegari, arXiv:math/0209081v1 (2002), rather than a certified historically first solution. The theorem fixes one closed hyperbolic manifold, one a>0 and one all-leaf embedded positive transversal, and gives ordinary GV=Na for every finite positive integer N. Compact leaves are allowed; no minimal-foliation result is claimed.

## Reproduce the local controls

After extracting this ZIP, use Python 3.11 or later. From this directory run:

```
python3 controls/verify_forms.py
python3 -O controls/verify_forms.py
python3 controls/independent_integrable_controls.py
python3 -O controls/independent_integrable_controls.py
python3 controls/finite_sampling_counterexample.py
python3 -O controls/finite_sampling_counterexample.py
```

These six runs need only the standard library. The polynomial checker performs 2660 checks across 120 distinct pairs, 360 pair/compression cases and 50 potentials. The independently implemented rational Taylor-jet checker performs 58 checks on actual integrable local forms, including compression. The grid counterexample shows that 343 sampled positive denominators do not prove positivity between samples. It does not falsify the paper's theorem or its specific local diagnostic. Arbitrary input pairs in the polynomial checker need not define integrable forms.

The separate symbolic implementation requires SymPy 1.14.0 (requirements-symbolic.txt). In an environment with that package run:

```
python3 controls/independent_symbolic_checks.py
python3 -O controls/independent_symbolic_checks.py
```

It performs 1640 symbolic/local controls. All guards in these current scripts use explicit errors, so optimization does not remove them. Actual baseline and negative-control receipts are in audit_history/root_repaired* and the algebra family receipts. Deliberate false guards, wrong densities and missing compression Jacobians failed as recorded in both modes. The original authors' 2660 and 1641 checkers used assertions removed by optimization; their case families also repeated. Historical output proof digests were not proof authentication. The current scripts label that digest informational and do not read or certify the paper. Audit logs retain original failures as history, not current acceptance criteria.

## What establishes the theorem

The proof uses the classical nonzero compact-support suspension input with its actual GV compatibility, a relative smooth interval trivialization, a disk-fixed representative of a pseudo-Anosov mapping class, mapping-torus hyperbolization, product-collar gluing, all-leaf transversal verification and oriented integration. The finite controls cannot realize the required global holonomy representation, certify a hyperbolic metric, or replace the universal leaf or topological arguments. The paper and mathematical audit supply those arguments using the stated classical theorems. No claim of formal proof-assistant verification is made.

## Priority and source access

The nonzero block is credited to classical Mather--Thurston/Tsuboi theory, interval-bundle replacement to the classical operation documented by Gabai, and hyperbolization to Thurston. Three separately initialized priority families and root primary-body checks found no authenticated earlier explicit full consequence in the inspected corpus. This is a bounded search, not a firstness or guaranteed novelty certificate. Final 2003 target-chapter wording was not compared. Relevant Tsuboi 1984 and 1985, Mizutani--Morita--Tsuboi 1981 (Annals of Mathematics 113(3), 515--527; DOI 10.2307/2006995), Gabai 1999, and Walczak 2013 full bodies remain unread in the relevant checks. Detailed source versions, read depths, failed access routes, scope differences and family coverage percentages are retained in audit_history/priority_* and ROOT_PRIORITY_DISPOSITION_01.md. Public abstracts, keyword scans and metadata checks are not represented as full-body reads.

## Reading the archive

audit_history preserves dated scientific snapshots, including preliminary percentages, prepublication status language and corrected mode/timestamp diagnostics. Later final reports and additive corrections supersede intermediate findings; earlier files were not silently rewritten. The six scientific/priority families are separate from the subsequent whole-publication-package review sequence. Snapshot paths in receipts describe the original execution environment; runnable controls above are self-contained and require no such paths. Source URLs and bibliographic metadata are retained, but primary-source PDFs, copied source bodies, downloads, rendered source pages, private environments and mutation working copies are excluded. Only explicit authored-safe file lists were copied. In particular the target-history family's excluded custody controls are absent.

SHA256SUMS.json describes every supplemental payload file except itself. It is a corruption check relative to that supplied manifest, not an independent trust anchor or mathematical certificate. The outer reviewed packet manifest binds the exact PDF, source, ZIP and deposit specification outside the ZIP.

AI tools were used extensively in development, drafting, sourcing, reproduction and adversarial review. The preprint is unrefereed and has not undergone conventional human peer review. Own-authored material is distributed under CC BY 4.0; no third-party full text is redistributed.


## Version 2 bibliographic correction

The previous candidate expanded the initials MMT incorrectly in this README. The correct authors of the unread 1981 Annals paper are Tadayoshi Mizutani, Shigeyuki Morita and Takashi Tsuboi. See PRIORITY_CORRECTION.md for publisher metadata and the exact correction scope. The primary body remains unread; this metadata correction does not complete priority. The theorem, paper PDF/TeX, all executable controls and intended deposit metadata are unchanged. The first two whole-package reports and earlier candidate/native snapshots are preserved as dated custody history; their earlier PASS/pending statements do not override the required correction and subsequent fresh review. The corrected current package requires a new independent whole-package review before publication.
