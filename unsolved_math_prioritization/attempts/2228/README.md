# EP-642: audited structural partial results

**UnsolvedMath 2228, catalog rank 900. Still unresolved: partial/stalled after 3/5 approaches.**

The target asks whether the maximum edge count of an n-vertex graph whose every simple cycle has strictly fewer chords than vertices is O(n). A chord is an existing graph edge between nonconsecutive cycle vertices. Equality of chord count and cycle length is forbidden.

## Accepted work

- Exact induced-edge and cycle-boundary identities
- Equivalence between a linear upper bound, an absolute minimum-degree threshold and bounded degeneracy
- Complete classification for graphs of maximum degree at most four
- An eleven-vertex four-regular, non-Hamiltonian admissible graph with 22 edges, 74 cycles, longest cycle six and maximum chord-minus-length margin -1; this rules out thresholds D<=4
- The admissible family K_{3,n-3}, giving the lower bound 3n-9 for n>=6

The missing global boundary inequality, or equivalently the absolute minimum-degree theorem, is not proved. No full solution, new asymptotic bound or novelty claim is accepted. The independent audit is AI-assisted mathematical review; it does not establish journal acceptance, external human peer review or formal proof-assistant verification.

## Evidence and exact correction

Read the [proof note](original_author/proof_note.md), [full audit](independent_audit/audit_report.md), [exact acceptance](independent_audit/acceptance_report.json), [actual correction patch](independent_audit/validation_hardening.patch), [corrected checker](independent_audit/corrected/validation.py), and [source verification](independent_audit/source_verification.json).

The original checker uses six assertions, which disappear under Python -O. Its optimized execution reproduces historical output but is **not active validation**: an invalid boundary mutation survives. The separately accepted derivative replaces those assertions with explicit ValueError checks. Mathematical formulas, finite domain and the 1,419-byte result file are unchanged. Original author and audit bytes, including historical pending/no-publication fields, are preserved exactly in the frozen archives and unpacked directories.

## Reproduce the checks

From this directory, run `python -B verify_publication.py .` for static, fail-closed archive, member, patch, acceptance, allowlist and manifest verification, including hostile mutations. It does not import or execute archive code. Repeat with `python -O -B verify_publication.py .`.

Run `python -B replay_checks.py` for the accepted finite checks, independent subset-DP oracle, original assertion-risk probe, ten semantic mutation controls and sixteen integrity controls. Repeat with `python -O -B replay_checks.py`. The oracle checks all 1,100 labelled graphs of orders zero through five, the obstruction and six bipartite-family members. Replays use relocated temporary directories and do not edit the frozen files. Finite checks do not prove the infinite target, and hashes establish identity rather than mathematical truth.

Optional complete-corpus/PDF identity checks take `--catalog`, `--problems`, `--reports`, plus `--dmms-pdf`, `--dg-pdf`, `--lms-pdf` and `--published-pdf`. These files are not distributed. Omitted optional checks report NOT_RUN; partial groups and wrong hashes fail. Publication-stage runs are in [EXECUTABLE_REPLAY_RESULTS.json](EXECUTABLE_REPLAY_RESULTS.json), [PUBLICATION_TEST_RESULTS.json](PUBLICATION_TEST_RESULTS.json) and [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json).

## Literature boundary

[Cycles with many chords](https://arxiv.org/abs/2306.09157) supplies O(n(log n)^8), the strongest upper bound verified in this bounded review. [Cycles with almost linearly many chords](https://arxiv.org/abs/2601.08769) keeps a polylogarithmic denominator and does not supply chord density one. [Nearly Hamilton cycles in sublinear expanders, and applications](https://arxiv.org/abs/2503.07147) gives the weaker sufficient exponent 130. The forum suggestion of exponent seven is not certified here, and no exhaustive best-known claim is made. Original 1997 wording and the complete 1996 historical paper were not inspected. Historical access failures and search results remain attributed to their original runs.

Only this target row's Status and Turns change in QUEUE.md, to partial and 3/5. Findings, all other rows, notes and existing chat links are preserved. Draft PR only; no merge, auto-merge, release, DOI or outreach. CI is reported separately for the exact final head, without treating no checks as a pass.
