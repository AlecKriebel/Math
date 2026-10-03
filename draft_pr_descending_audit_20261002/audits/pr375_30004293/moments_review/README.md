# Independent moments and tails review of PR 375 / 30004293

**Scoped verdict: PASS; original quantitative goal remains unsolved.** No mandatory mathematical correction found in Turn 5's raw moments, rare polynomial tails, or logarithmic moments on the larger normalization. The first four turns' probability modes and restrictions are consistent with those results. This is a bounded independent audit, not a priority or novelty certification.

The independent source-first formulation was sealed before candidate text. The universal mathematical verdict was sealed before author checker and historical-review access. The original mathematical seal finalized at 2026-10-03 06:58:05 UTC; its opening metadata was subsequently corrected to that actual timestamp without changing the mathematical body. Original hash receipt and private original bytes retain the provenance.

`MATHEMATICAL_VERDICT.md` contains the universal proofs, exact gap, source scope, and counterexamples to invalid probability/moment implications. `independent_controls.py` and its full report/streams contain 55,580 exact assertions across 10,943 configurations through D=14. `replay_relevant_author.py` only corroborates the author's Turn 5 receipt after the independent verdict; it reproduces 16,818 assertions exactly. The initial wrapper's wrong expectation of 54 target files is preserved in full streams as an auditor setup failure. The correct freeze has 54 bindings: 53 target files plus sibling QUEUE.md. All sizes, SHA-256 and raw Git blob hashes were independently recomputed and agree.

The exact owned public allowlist in `MANIFEST.json` contains full independent/acquisition/replay/packaging code, logs, stdout, stderr, reports and source identity metadata. All third-party PDFs, extracts and page renders are private under ignored `tmp/`; none belongs to that allowlist. No candidate, Git/index, remote or service mutation, external communication, publication, release or DOI action was performed.

The key verified moment bound is

\[
 E[M(D)^q]\ge\frac{\prod_{i\le D}(1+(2^q-1)/i)}{(2^qD+1)^q},\quad q>0,
\]

including \(\liminf E[M(D)^2]/D\ge1/96\). Rare high-count configurations can dominate raw moments. The outstanding target is a matching typical bound and finite, identified in-probability limit for \(\log M(D)/\log\log D\), with any broader source growth claim treated separately. Counts do not prove that limit.

Original definitions and lower-bound scope were read in [Green's OWR contribution](https://ems.press/content/serial-article-files/46829), [FGK v3](https://arxiv.org/pdf/1908.00378v3), and the [published full Lemma 2.1 and remark](https://link.springer.com/content/pdf/10.1007/s00222-022-01177-y.pdf). The [recent Mao-Song v2](https://arxiv.org/pdf/2609.22296v2) and [Tenenbaum powers paper](https://tenenb.perso.math.cnrs.fr/PPP/Delta%28n%5Er%29.pdf) were checked for scope only; their full proofs are not independently verified here.
