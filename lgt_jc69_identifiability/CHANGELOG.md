# Changelog

## Version 0.2 — prepared for author audit — August 2026

### Mathematical strengthening

1. **Principal theorem retained and generalized.** `main_manuscript.tex`, Theorem 1.1, states global injectivity and everywhere-full rank for every fixed known `mu > 0`, rather than only the normalization `mu=4/3`.
2. **Concrete omitted genealogy added.** Section 3 and Figure 1 give the two-transfer example at `0<u<v<t1`, separating cherry formation from a later noncoalescing lineage movement.
3. **Exhaustive occupancy-chain derivation expanded.** Sections 3–4 define “ancestrally unoccupied,” derive the three-state CTMC, prove normalization, and recover topology frequencies.
4. **Unknown-rate ambiguity proved.** Proposition 1.3 and Section 5 record the exact common time-rate scaling invariance.
5. **Joint topology theorem added.** Corollary 1.2 and Section 7 prove that the uniquely largest matching-pair aggregate identifies the rooted cherry before parameter inversion.
6. **Feasible-interval proof expanded.** Section 6 now gives the full `h(q)` crossing argument, including positivity, physical feasibility, upward crossings, and exclusion of re-entry.
7. **Likelihood statement justified.** Section 8 includes the exact population multinomial Hessian lemma and applies it only at positive regular exact fits.

### Precision and scope corrections

8. **Process theorem separated from the source formula conjecture.** The title, abstract, introduction, principal theorem, discussion, conclusion, summary, email, and handoff now use conditional model-specific wording.
9. **Auxiliary map renamed and defined.** The secondary map is consistently `F_table`, with its fourteen named classes, density convention, and absolute-time convention stated explicitly.
10. **Open-set multiplicity stated precisely.** Proposition 1.4 claims a nonempty open set of regular observed distributions with at least two preimages and makes no whole-image multiplicity claim.
11. **Model scope listed.** Theorem 1.1 and the introduction enumerate sampling, tree, transfer, substitution, rate-scale, ILS, and exact-population assumptions, followed by exclusions.
12. **Species-branch terminology corrected.** Section 2 defines an ancestrally unoccupied species branch as one carrying no currently traced sampled ancestry while retaining its population gene copy.
13. **Source notation translated.** Section 9 and `SOURCE_SNAPSHOT.md` map aggregate manuscript coordinates to `p_xxx`, `p_xxy`, `p_xyx`, `p_yxx`, and `p_xyz`, including multiplicities.
14. **Standalone prose audit completed.** Prompt-specific and workflow-specific language was removed from the mathematical body and confined to factual provenance metadata where appropriate.
15. **Terminology scan automated.** `tools/wording_audit.py` checks the requested obsolete phrases, species-branch shorthand, and email length.

### Source-audit reproducibility

16. **Exact arXiv version frozen.** `SOURCE_SNAPSHOT.md` identifies `2607.14653v1`, title, authors, submission time, retrieval date, PDF hash, and relevant PDF pages.
17. **Exact repository state frozen.** The same file records repository commit `1954b2…`, Git blob identifiers, local SHA-256 hashes, filenames, function names, cell headings, and line ranges.
18. **Unavailable source-archive hash handled explicitly.** The snapshot records the attempted arXiv TeX-source retrieval and the tool-level gzip limitation without inventing a checksum.
19. **Code-specific manuscript claims made immutable.** Section 9 and Appendix D cite the exact commit, `GetSitePatternProbs`, notebook history ranges, and `Pxxx` integration cell.

### Manuscript restructuring

20. **Theorem-first organization adopted.** The paper now runs from main results and model scope through the missing mechanism, exhaustive genealogy, compact map, global proof, topology, statistics, map comparison, and limitations.
21. **Secondary material moved.** The full interval box, detailed integrations, Jacobian algebra, source forensics, and reproducibility details are in appendices or verifier files.
22. **Abstract and title refocused.** The abstract leads with the missing movement, CTMC summation, global theorem, topology corollary, and concise three-map audit result.
23. **Version status unified.** Manuscript, technical summary, handoff, snapshot, provenance, and metadata use “Version 0.2 — prepared for author audit — August 2026.”
24. **Conventional context and bibliography added.** The introduction includes related context, and the paper ends with a standard bibliography.

### Verification changes

25. **Exact and numerical targets separated.** `make verify-exact` runs deterministic theorem-bearing checks and ends with `ALL EXACT CHECKS PASSED`; `make audit-simulation` is separate; `make verify` runs both.
26. **Acceptance checks broadened.** New exact scripts verify the exhaustive measure, topology formulas, cube inverse, scale invariance, matching-pair relation, diagnostic-point conversion, and likelihood-Hessian cancellation.
27. **Build quality gates added.** `make pdfs` uses `latexmk` and fails on overfull boxes, undefined references/citations, missing files, or fatal LaTeX diagnostics.
28. **Reproducibility files added.** Locked requirements, environment metadata, exact/simulation/clean-unpack transcripts, machine-readable certificate, file manifest, and archive checksums are included.

### Outreach materials

- `EMAIL_DRAFT.txt` is a 249-word plain-text email leading with the theorem, explaining the two-transfer mechanism, asking about intended interpretation, and inviting substantive joint follow-up work.
- `AUTHOR_HANDOFF.md` separates the technical theorem, CTMC correction, topology corollary, three maps, exact diagnostics, source snapshot, verifier command, and collaboration directions.
- `technical_summary.tex/.pdf` is a consistent two-page account of the revised paper.

### File/package changes

- The previous resolution package remains unchanged.
- The revised package adds `SOURCE_SNAPSHOT.md`, `PROVENANCE.md`, `CHANGELOG.md`, `ENVIRONMENT.md`, `requirements-lock.txt`, build/audit tools, and renamed verifier entry points.
- The earlier combined plain-text handoff was replaced by `EMAIL_DRAFT.txt` and `AUTHOR_HANDOFF.md`.
- New deliverables are archived as `LGT_JC69_author_ready_package.zip` and `LGT_JC69_author_ready_verifier.zip`, with hashes in `ARCHIVES.sha256`.
