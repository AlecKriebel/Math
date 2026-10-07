# An explicit complex polynomial retract in five variables

A consequence note by Alec Kriebel (ORCID https://orcid.org/0009-0001-9320-500X), dated October 6, 2026.

## Result and attribution
The package gives explicit split complex-algebra maps for the OpenAI family047 fourfold A=C[p,s,u,F,J]/(H), x=s²+u³+p²F, H=x²F−(1+2sx)J−p²J²−pu, into B=C[p,s,u,m,e]. Its image is a smooth integral, nonpolynomial algebra of transcendence degree four. This answers Costa's assertion negatively over C in ambient dimension five. It does not settle the ambient-four-variable question.

The cancellation example, its stabilization and nonpolynomiality belong to OpenAI. The cylinder-to-retract implication is classical (Nagamine Proposition1.4, arXiv1811.04153v2; earlier Epstein–Nguyen). This note adds an explicit five-component transport and checkable certificates; it is not an independent cancellation breakthrough or first-priority claim.

The nonpolynomiality input is explicitly cited, and its written proof was independently audited through all pivotal stages. Symbolic tests certify coordinate identities only. Actual upstream Lean sources were semantically inspected; a full kernel build, axiom report and comparator were not reproduced due disk constraints. No formal verification of this follow-on theorem is claimed.

AI tools were used extensively in research, drafting and verification. The preprint has not undergone conventional human peer review/refereeing. Automated adversarial audits are not human peer review. No external individuals were contacted.

## Files and clean reproduction
The standalone manuscript is main.tex; no external bibliography file is needed. Its source archive includes the exact scripts, requirements, source hashes, theorem/dependency ledgers, independent source audits and bounded priority audit. It excludes source reading PDFs, credentials, caches and machine-specific environments.

To reproduce the computational checks in a fresh directory, install Python and SymPy1.14.0 (requirements.txt). Run `python check_stabilization.py` and `python check_nonpolynomiality_certificates.py`. The first reports 32 exact symbolic identities and 7 exact rational regression points. The second checks the graded relation, determinant principalization and the sign-sensitive example LNDs. Neither tests nonpolynomiality as a black box; the proof remains in the cited theorem and written audit.

To build the paper use `tectonic main.tex` (tested Tectonic0.16.9) or a normal LaTeX installation supporting the standard packages listed in the source. The desktop built-in compiler also compiled this standalone source. The exported paper.pdf was produced by Tectonic and visually checked; a preview alone was not used as a deposit artifact.

The optional source-check argument `python check_stabilization.py --upstream-root /path/to/math` confirms the construction hash. Use the exact pinned OpenAI commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. The source/dependency manifests give every inspected manuscript and actual Lean closure hash. The archive also includes the unchanged Apache-licensed 55-module actual Lean source closure under lean/, with an adapted minimal build configuration. The formal-scope audit gives the minimal pinned Lean4.34.1 / mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 build route and precisely reports its unreproduced status.

## Licensing
This note and its original verification package are released under CC BY4.0, following the repository's established preprint deposit template. Attribution must preserve the upstream author's credit. The bundled lean/ directory is an explicit Apache2.0 exception: unchanged OpenAI proof sources and an adapted minimal build configuration/audit harness. Its license and an attribution notice accompany the package. Third-party primary-source PDFs are not redistributed in the deposit. See LICENSES.md and THIRD_PARTY_NOTICES.md.

## Archive navigation
- main.tex: standalone paper source; check_stabilization.py and check_nonpolynomiality_certificates.py: computational checks in the archive root.
- audits/: original independent audit snapshots; their working-tree paths describe audit custody, while the files here are the portable copies. formal_scope_logs/ under audits/ contains the retained failed-build logs.
- provenance/: exact manuscript, literature and actual Lean source hashes.
- lean/: unchanged 55-module proof closure, adapted lakefile.lean, lean-toolchain, PrintAxioms.lean and reproduction README. Run optional formal commands from this directory, rather than the original machine's verification/lean_copy path. They were not successfully completed in this audit.
- DEPENDENCY_LEDGER.md and THEOREM_LEDGER.md: mathematical claim/dependency snapshots. Review/publication receipts are maintained separately in the repository; they are outside the upload archive to avoid self-referential hashes.
