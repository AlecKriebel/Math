# Recent and exact-model priority audit: PR 872

**Decision: PASS within the bounded search, subject to the credit and scope requirements below. No previous full theorem or verified implication covering the entire target was located. This is not a firstness certificate.** Mathematical acceptance remains the responsibility of the separate proof audits.

## Frozen target and independence

PR #872 concerns problem 30006628 / OWR-14299911-031, frozen head `e3d77731b45b5f463df46e769faa01d65fe193ec`. The candidate `PROOF.md` is 19,961 bytes, SHA256 `3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`. I saved `INITIAL_INDEPENDENT_MEMO.md` before reading any other priority lane. I never read the classical-priority lane. The completed source/model audit was read after that memo to check scope consistency.

The target fixes at least three arbitrary nontrivial finitely generated factors, their finite inverse-closed generating alphabets, and `1/3<d<1`. Relators are independent uniform draws with replacement from rooted cyclically syllable-reduced words of exact length. The limit runs through all integer lengths. This includes torsion and infinite or non-finitely-presented factors. Neither two factors, the endpoint `d=1/3`, nor parameter uniformity as alphabets vary is claimed.

## Mandatory antecedent credit

The [Montee–Steenbock project report in ESI Annual Report 2024](https://www.esi.ac.at/static/assets/extras/reports/ESI_Report_2024.43f879fc9471.pdf), printed pp. 77–79, is a particularly close antecedent. Its p. 78 already proposes cutting free-product relators into three syllable-respecting pieces and studying associated spectral graphs, following Ashcroft. It explicitly leaves both the needed gap and its implication for the quotient unfinished. This is a previously articulated research program, not a printed full solution. The report describes a 2024 project; the annual volume's preface is dated August 2025, so the project year should not be presented as a verified publication date.

The paper must cite this report directly and describe its contribution as completing the relevant model-specific steps of an existing spectral program. It must also give strong credit to Żuk/Kotowski–Kotowski, matrix concentration, and the earlier Markov/spectral methods. The general three-block strategy and spectral-transfer mechanism must not be described as newly invented here.

## Current exact-model source

The fresh [RQFP arXiv record](https://arxiv.org/abs/2502.08630) still lists v2, revised 28 September 2026. I read [v2](https://arxiv.org/pdf/2502.08630v2), pp. 1–5: Definition 1.1 matches the ball-alphabet law, and Question 1.9 remains printed. Its definition includes two factors; the all-length two-factor version fails because the odd-length cyclic universe is empty. The present claim must be called the at-least-three-factor case, or the OWR question, rather than a resolution of every literal parameter in Question 1.9. The already established collapse above `1/2` supplies a classical subrange, not the whole assertion.

Current metadata labels the manuscript to appear in Transactions AMS. Steenbock's page, updated 29 September 2026, labels it accepted. No distinct published final theorem body or journal DOI was located by the bounded publisher/title/metadata searches. Acceptance metadata is not evidence of a later solution.

## Oppenheim's September 2026 result

I read [Oppenheim v1](https://arxiv.org/pdf/2609.21255v1), Definition 1.1, Theorem 1.2, the full displayed criterion in Theorem 3.6, its proof conclusion and sufficient-condition setup, and §4's probability argument and final statements. This establishes a substantially better Gromov-model density bound, with lengths divisible by four. Its density definition selects uniformly among fixed-cardinality sets, not the target IID syllable draws. It must prevent any blanket assertion that the current Gromov upper bound is still one third.

There is also a concrete obstruction to using its criterion unchanged: it requires positive approximately uniform proportions across every pair of distinct first letters. Distinct syllables in the same factor have structural zero corners in the target. A new application would have to prove different hypotheses; citing the theorem does not discharge those model-specific estimates. I did not attempt such a new proof.

## Additional recent primary bodies

The current [Abbott–Berlyne–Mangioni–Ng–Rasmussen manuscript](https://arxiv.org/pdf/2507.16677v3), revised 26 January 2026, matters more than its older v2. I read pp. 1–3 and 54–56. Its Corollary F gives existence of a property-(T) quotient for each acylindrically hyperbolic relative HHG. Theorem E and §6 construct special common quotients using finitely many random-walk relations. This does not provide the target exponential family of uniformly sampled exact-length syllable relators, or its full arbitrary-factor quantifiers. The same body explicitly cites RQFP while distinguishing the random models.

[Barbieri–Jezernik v1](https://arxiv.org/pdf/2602.11905v1), pp. 1–4 and Theorem 1.1, studies random permutation representations of free products of finite groups. Its strong-convergence parameter is the permutation degree, not relator length; it does not assert the density-quotient conclusion.

[Orlef–Odrzygóźdź v1](https://arxiv.org/pdf/2609.24037v1), pp. 1–3 and Theorems 1.1–1.3, studies fixed length-four relators with the number of free generators tending to infinity, at a different bound. Its spectral construction is relevant background but supplies no target-law theorem.

[Ashcroft v2](https://arxiv.org/pdf/2202.12318v2), pp. 1–4, Theorems A–B and §1.1, supplies earlier hyperbolic-group, Markov and three-block methods. Its random elements lie in word-metric annuli, with different base-group hypotheses. Arbitrary finitely generated free factors need not produce a hyperbolic base group, and arbitrary bounded syllable alphabets are not those annuli. No unchanged general theorem was found to cover the present model.

These comparisons are theorem-scope readings, not independent certifications of every proof in the antecedent papers. `PRIMARY_READING_RECEIPTS.json` and `EXACT_COMPARISON_MATRIX.md` record the exact read scopes and gaps.

## Adversarial model checks

The following deductions are this audit's comparisons, not claims printed in those antecedents.

* Property (T) passing to quotients does not permit removal of sampled relations. Retaining only syllable-reduced relators from a Gromov sample produces a group mapping onto the full Gromov quotient, so the relevant implication points the wrong way.
* The laws can differ exponentially. For `n>=3` cyclic factors with alphabets containing a generator and its inverse, the syllable universe has exponential rate `2(n-1)` while the usual reduced-word universe has rate `2n-1`. Conditioning a whole presentation on the smaller universe is not automatically harmless.
* Lifting actual ball elements to free words changes multiplicities and word lengths. Permanence under quotients alone does not identify that lifted random law with a uniform free-group density model.
* Existence of one property-(T) quotient says nothing by itself about the probability that a specified density quotient has that property.
* Results on a subsequence of lengths do not prove the all-integer limit. The candidate's three residue calculations still need their separate proof audit.

Each route is blocked as a direct priority implication until its missing comparison is supplied. No unsupported equivalence has been promoted to evidence of a prior full solution, and no search for a new central proof was substituted for priority checking.

## Search coverage and exact limits

I made 40 recorded web queries, including current exact-title/model searches, author publication lists, official seminar/proceedings pages and nearby spectral work. Fresh primary retrievals, including successful and failed access attempts, have SHA256/byte receipts. Author pages for Steenbock, Krishna and Ng and Montee's April 2026 CV were checked. Einstein's two advertised hosts failed normal TLS access, and Montee's research page returned a browser fetch error; neither was bypassed or treated as read. The OSU seminar describes the distinct random-walk negative-curvature work. Search-index snippets were discovery leads, not theorem evidence.

OpenAlex's observed RQFP work entry and filtered citing-work query both return zero citations. This is demonstrably incomplete: the actual HHG v3 body cites RQFP. Consequently zero must never be reported as an exhaustive citation census. A five-result Crossref title query contained no exact title match. These bounded observations neither prove absence of a journal version nor absence of a later solution. Broad searches also returned irrelevant operator-algebra, group-action and nonmathematical items, which were excluded without deriving mathematical claims from them.

No full exact-model antecedent was located in the primary bodies actually read. The defensible publication statement is that the note proves the stated at-least-three-factor theorem using established methods and answers the printed OWR question, with substantial antecedent credit and a dated, bounded literature comparison. It must avoid a verified-firstness claim, an exhaustive contemporary openness claim, or novelty claims for standard methods. The work remains unrefereed, heavily AI-assisted, and neither formally verified nor externally human peer reviewed.

Only this lane's public allowlist is offered for publication. PDFs, extracted text, page images, full webpage/search dumps and raw bibliographic responses remain private and ignored. No people were contacted; no external messages, Git/queue/PR mutations, or writes outside this assigned lane were made.
