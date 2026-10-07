# Independent priority and attribution audit

Checkpoint/search date: 2026-10-06 America/Los_Angeles (2026-10-07 UTC during the session). Mathematical resolution completion for this project is **not certified by this audit**; completion of this priority audit: 90%; publication package: 0%. Missing upstream validation overrides any optimism about the reductions.

## Bottom-line finding for the exact target

The algebraic reductions needed by the proposed project are already public. General explicit finite-field factoring reduces deterministically to prime-field root finding through Berlekamp's 1970 work. Prescribed-degree construction reduces to prime-field factoring through Shoup's 1988/1990 work. The especially simple `N=md` construction lift is written out as Algorithm 2 in Rai's 2024 primary paper.

A **valid new prime-field factoring theorem** would make unconditional arbitrary-base factoring and prescribed-degree construction immediately available through this established machinery. The source of that advance would be the new prime-field theorem and its analytic inputs. Our writeup could document an accurately attributed consequence and give a reproducibility/parameter audit, but could not present these reductions as independently invented or claim to have independently solved the base factoring problem.

This is not a finding that the unconditional core target was already proved before the upstream release. Primary comparator papers in 2024, 2025, and March 2026 explicitly still identify the relevant general deterministic problem as unresolved. It is a finding that the entire *extension proof mechanism* is inherited. No materially new in-scope mathematical extension was independently established by this audit. Search failures do not supply novelty evidence.

## Exact prior sources inspected

| Source/version | Public evidence | Exact relevant scope inspected | Relation to this effort |
|---|---|---|---|
| E. R. Berlekamp, *Factoring Polynomials Over Large Finite Fields*, Math. Comp. 24(111), 713–735 (1970), DOI `10.1090/S0025-5718-1970-0276200-X` | Original primary scan labels issue July 1970; received/revised dates in 1969 are not public-disclosure dates. Scan has a 1971 copyright notice; standard citation is 1970. | Introduction, pp.713–715; derivative/pth-root preprocessing p.716; §5 pp.727–729 equations (5.01)–(5.05) and separation proof; §6 pp.729–730; beginning of §7 p.730. | Already reduces general-field factorization to prime-field root finding. In §5, the functions `Tr(a^j x)` for a supplied power basis separate distinct roots by nondegeneracy, and gcds isolate their level sets. The small-prime version enumerates `F_p`; replacing this by a justified prime-root subroutine is the expected reduction. §6 gives a different route for large `p`. |
| V. Shoup, *New algorithms for finding irreducible polynomials over finite fields*, Math. Comp. 54(189), 435–447 (1990), DOI `10.1090/S0025-5718-1990-0993933-0`; author copy dated 1989-01-31 | Shoup's primary publications page identifies the FOCS1988 extended abstract, pp.283–290, and the 1990 journal article. No claim that the manuscript date is a first public disclosure. | Theorems 2.1, 3.1, 4.1 and full proofs in author copy §§2–4; Lemmas2.2–2.4, all prime-power branches and call counts. | Theorem3.1 supplies deterministic polynomial reduction in numeric degree and `log p`. Theorem4.1 already handles a supplied explicit extension base. Irreducible construction is an inherited consequence. |
| Shanthanu S. Rai, *Pseudo-Deterministic Construction of Irreducible Polynomials over Finite Fields*, arXiv:2410.04071v1 | arXiv original history: 2024-10-05 08:02:34 UTC. Only v1 listed when checked. | Representation §3.2.4; Algorithm2 and Theorem4.1 §4; Shoup reduction restated Theorem5.1; conclusion §6. | Algorithm2 constructs a prime-field irreducible of degree `dm`, factors it over degree-`m` base, and selects the first factor. Identical to our simplified lift. The overall paper is pseudo-deterministic because its factoring is randomized; it does not give the unconditional deterministic core theorem. |
| Daniel Altman, *Deterministic polynomial factorisation modulo many primes*, arXiv:2509.12705v1 | arXiv history: 2025-09-16 05:55:14 UTC. Only v1 listed when checked. | Introduction and exact Theorem1.1, plus comparison and limitations following it. | An amortized algorithm over many primes; dependence on splitting-field degree can be factorial in polynomial degree. It does not settle the worst-case single-input target. |
| S. Chatterjee, P. Harsha, M. Kumar, *Deterministic list decoding of Reed-Solomon codes*, arXiv:2511.05176v2 | arXiv v1:2025-11-07; v2:2026-03-24. | Exact Theorems1.1/1.2, introduction's factorization scope, correction on prior Sudan decoding at §1. | Handles structured bivariate factorization instances with evaluation information; it expressly does not solve general univariate factoring. This rules out claiming Reed–Solomon deterministic list decoding as a new generic corollary without accounting for this prior result. |

The Berlekamp scan was successfully fetched from the official AMS URL using an ordinary browser User-Agent after the web reader's direct open failed; its extracted text was then read locally. SHA-256: `0be0c0f245755b82f2daf30d7556c753496c8310be2a24e38d00d4af4cce56b0`. The Shoup author PDF SHA-256 is `00590fb8f0717338530b067626428781991edb840fb74c37cf846f07f50e0644`. These third-party PDFs are source evidence, not approved deposit attachments.

## Primary links and citation chain

- Berlekamp official primary scan: <https://www.ams.org/journals/mcom/1970-24-111/S0025-5718-1970-0276200-X/S0025-5718-1970-0276200-X.pdf>.
- Shoup author paper: <https://www.shoup.net/papers/detirred.pdf>; author publication list: <https://www.shoup.net/papers/>. Shoup's §3 explicitly cites Berlekamp1970 for extension-to-prime factoring reduction.
- Rai exact v1: <https://arxiv.org/html/2410.04071v1>; dated abstract/history: <https://arxiv.org/abs/2410.04071>. Rai explicitly invokes Shoup and provides the degree-product lift with its proof.
- Altman exact v1: <https://arxiv.org/html/2509.12705v1>; history: <https://arxiv.org/abs/2509.12705>. Its comparison cites Berlekamp, Shoup, and later Frobenius-map improvements; the single-input distinction is explicit.
- Chatterjee–Harsha–Kumar exact v2: <https://arxiv.org/html/2511.05176v2>; history: <https://arxiv.org/abs/2511.05176>. Its correction illustrates why apparently new coding consequences must be checked against existing primary proofs.

No outreach was made, and no email addresses were used.

## Companion-corpus audit at the pinned version

Read-only upstream commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Local git author/committer timestamp: `2026-10-06T14:58:50-07:00`; local history contains one initial commit touching family142. The GitHub commit page was independently opened and confirms a public accessible initial-commit object. The primary manuscript README was also opened publicly. This verifies public accessibility as of this audit; it does not independently prove that an October4 manuscript label was its first public disclosure.

Primary commit: <https://github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a>. Family142 citation README: <https://github.com/openai/math/blob/main/preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/README.md>.

Family142's exact main theorem, introduction lines26ff, is restricted to dense nonzero polynomials over prime fields, with multiplicities, fixed exponent `10^12`, and no randomness/integer-factorization/primitive-root oracle/GRH. Its abstract/catalogue explicitly identifies dependence on the Hecke zero-free theorem from family029. Its internal arithmetic uses represented nonprime fields, but I found no standalone arbitrary-input-base construction/factorization theorem in the audited family142 source. This absence is an observation about these files, not a proof of independent novelty.

The corpus-wide text search for finite-field construction, arbitrary-base claims, and trace coordinates found relevant traces inside family142's cyclic-norm argument, plus BIMS citations in the quasi-Riemann papers. Family003's introduction already has an explicit quadratic-nonresidue/square-root corollary, and its October5 alternate paper lists this consequence too. Those consequences must not be relabeled as new. An appearance of BIMS in a bibliography alone is not an explicit general-`r` theorem; optional roots were not used to manufacture headline novelty.

The upstream repository README explicitly says that results have different stages of verification and that some unformalized results may contain issues. This statement agrees with the required independent validation protocol; it is not an endorsement of the prime-field theorem.

Source file SHA-256 entries read for this priority check:

| Pinned relative path | SHA-256 |
|---|---|
| `preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/build/sections/00-introduction.tex` | `a7048b62d7a31c5029827ad5db7e32187f5d29035138d6cc0677d48309a05af9` |
| corresponding family142 `README.md` | `925be7c0279cf5a4a67441c6e930b8c8a5d742c2042d335fd871799da16f73e3` |
| `preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/build/paper.tex` | `42a5ee0febca59fd1def55cfd6c6808c322ef4237d7726303ea52f711deac6a3` |
| `preprints/The-Quasi-Riemann-Hypothesis-October-5-2026/build/paper2.tex` | `d9a8f15aa770cf883d0eabd2b775fad694ce20b44cba7928f5c0c9a6d8750d4d` |

The manuscript-specific BibTeX gives the author as `OpenAI`, title `Deterministic Polynomial Factorization over Prime Fields`, year2026, and the manuscript-specific GitHub PDF link. Preserve this citation instead of attributing its theorem to Alec Kriebel.

## Claim classification and publication boundary

| Possible claim | Audit classification |
|---|---|
| Prime-field unconditional polynomial factoring | Upstream claimed breakthrough; validity is being independently audited elsewhere, not established by this priority check. |
| Arbitrary explicit finite-field factoring assuming prime root/factor oracle | Established Berlekamp reduction; exact traces are classical. |
| Prescribed-degree irreducible/extension construction assuming prime factoring | Established Shoup reduction; arbitrary-base scope already in Theorem4.1. |
| Degree-`md` then factor-and-select lift | Explicitly public in Rai2024 Algorithm2; not new. |
| Uniform bit-polynomial unconditional core target after a valid upstream theorem | Immediately newly available corollary, with the advance inherited from the base theorem; not an independently solved base problem. |
| Feasible exact implementation and parameter ledger | Useful verification artifacts; mathematical novelty not established by implementation alone. |
| Fixed-`r` roots by factoring `X^r-a` | Immediate classical consequence, poly(numeric `r`); no claim of poly(`log r`). |
| Least quadratic nonresidue / prime-field square roots | Already explicit in upstream quasi-Riemann papers; excluded as new results. |

If the upstream theorem fails validation, the strongest result from these notes is the old conditional reduction, supplemented by an audit and examples. Publishing that as a new unconditional solution would be false. If it passes, any concise note should title and abstract the result as a consequence of the upstream theorem and make the inherited reduction provenance unmistakable. I have not established a new mathematical theorem beyond the original sources; a stronger novelty claim requires additional work and positive evidence, not optimistic phrasing.

## Search record and limits

Searches included exact Shoup theorem/author-paper searches, Berlekamp1970 reduction/trace searches, current deterministic finite-field factorization and construction queries, exact release-title searches, and primary-source citation chains through Rai2024, Altman2025, and Chatterjee–Harsha–Kumar2026. Secondary search results were used only to locate original papers. No claim relies on a secondary abstract/summary. The final exact theorem statements and proof mechanisms described above were checked in primary full text or original scans.

This audit does not establish exhaustiveness or a first-priority claim, and it does not certify the family003/029 analytic proofs or family142 geometric algorithms. Those are separate dependency audits. The priority question should be revisited if a repaired, materially different core theorem is eventually established.
