# Endpoint nonlinear Maurey extension: verification note

**Publication status: withheld. No Zenodo draft, record, DOI, or tracker row exists for this project.** The earlier September 2026 public announcement gives the substantive target through standard reductions. This packet verifies the theorem and attribution; it does not advertise a new solution.

## Contents and scope

`main.tex` is standalone, including its bibliography. `output/main.pdf` is a seven-page compiled note (page count is rechecked after revisions). It proves `N2(L1(mu;R)) <= 12 sqrt(21)` by adapting OpenAI family 332 and gives the full arbitrary-subset extension with `C=12 sqrt(21) kappa`, where kappa is an absolute constant in Mendel–Naor's Theorem 1.11. Measures are arbitrary countably additive positive measures; the source is any set-sized metric space with finite Markov type two. The Lp source bound is `4C sqrt(p-1)` for finite p>=2.

No arbitrary L1-subspace or noncommutative L1 target assertion is made. Complex targets use a separately stated sqrt(2) realification deduction. No formalization or conventional human peer review is claimed.

## Reproduce

Run `./build.sh` in this directory, with Tectonic available on PATH. It writes `output/main.pdf`. Any ordinary LaTeX installation supporting the standard packages can alternatively run pdflatex twice on `main.tex`; no bibliography program or external data is required. The native Codex editor compiler also successfully compiled this standalone source; its preview was not used as an export. The separately downloadable local PDF comes from Tectonic 0.16.9 (LaTeX2e 2021-11-15 patch 1, L3 layer 2022-02-24).

The verification archive contains only project-authored notes, the manuscript, source-custody receipts and the upstream manuscript-specific citation, plus the applicable license. Downloaded third-party papers, generated caches, tokens and secret state are excluded. The archive is an inspection/reproduction packet, not an uploaded deposit or an outer upload kit.

Mathematical dependency checks and priority evidence are documented in the project dependency ledger and agent reports. Later complete-package review reports are preserved under `../reviews/`; their hashes identify the exact reviewed inputs. PDF byte hashes can differ on rebuilding because creation timestamps and engine serialization are not fixed. Verify source hashes and successful clean compilation; no false byte-for-byte reproducibility claim is made.

## Publication condition

The original request allows publication only after substantive novelty and priority clearance. Naor, arXiv:2609.07564v2 (September 10), announces L1 metric Markov cotype two and the O(sqrt(p)) consequence from forthcoming Mendel–Naor work. We did not locate that full forthcoming proof; its absence in searches does not restore priority. The all-measure/all-Markov-source quantifiers follow from the announced result by complemented finite ell1, cut reconstruction, Mendel–Naor 2013 and classical L-embeddedness. No genuine new in-scope theorem was identified in independent audits. Publication is therefore withheld, and the tracker is left unchanged.

Author: Alec Kriebel, ORCID 0009-0001-9320-500X. AI tools were used extensively in research, drafting and verification. Automated audits are not human refereeing. See NOTICE for attribution and LICENSE for source terms.
