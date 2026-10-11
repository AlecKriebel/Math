# Source gate: 30004293 / OWR-17293-009

## Exact source and representation convention

Ben Green's complete contribution, *Propinquity of divisors* (joint work with Dimitris Koukoulopoulos and Kevin Ford), occupies printed pp3164–3167 of OWR50/2019. The model question is on p3165 / PDF25, visually verified. The report defines an infinite random set A of positive integers with independent inclusion probabilities 1/i. Its literal displayed question asks for max_x r_A(x), without an explicit D in that display. Immediately before it the discussion concerns subset sums of A in [1,D]; immediately afterwards it distinguishes the annular beta_k problem involving A intersect [D^c,D]. The full surrounding contribution was read, not just the imported sentence.

The detailed primary paper makes clear that representations are by distinct finite subsets, not ordered tuples or repeated use of an element. Write r_B(x)=#{C subset B: sum C=x} for a finite B. The empty subset has sum zero. The element 1 is selected surely. No arbitrary rescaling of the inclusion probability is part of this task.

Primary report: https://ems.press/journals/owr/articles/17293 and https://ems.press/content/serial-article-files/46829. The volume year is 2019; publication was 19 November 2020. The requested UnsolvedMath numeric URL failed direct retrieval; its pinned import was compared with the exact primary passage, which controls scope.

## Literal correction, separate from quantitative work

For each fixed x>=0, r_A(x) is finite, since only elements in [1,x] can occur. Published equal-sum lower bounds imply sup_x r_A(x)=infinity almost surely. Thus a finite attained unrestricted maximum is not the substantive quantitative question. LITERAL_COROLLARY.md gives the short credited deduction. This correction does not solve the intended growth problem.

## Explicit finite-prefix interpretation used for author work

Define

    M(D)=max over integer x of #{C subset A intersect [1,D]: sum C=x}.

The substantive interpretation is to determine its sharp growth as D tends to infinity. A precise leading-exponent question is whether

    log M(D) / log log D

converges in probability to a deterministic constant, and to identify that constant if it exists. This normalization is an explicitly stated quantitative interpretation; the OWR display does not itself specify it. A result for this leading exponent alone will not be advertised as resolving every finer version of the source's broader growth question.

The finite-prefix interpretation has direct support in Ford–Green–Koukoulopoulos, *Equal sums in random sets and the concentration of divisors*, Invent. Math.232 (2023),1027–1160, Lemma2.1 and its following remark (printed1035–1036; arXiv version p7). That remark specializes to [3,D] and explicitly describes a probably tight lower bound on growth of the representation function. Their theorem yields M(D)>=(log D)^(eta-epsilon) with probability tending to one for each epsilon>0, where eta≈0.3533227727. The numerical value is a published lower-bound constant, not an assumed exact prefix exponent.

The source annular threshold is

    beta_k=sup{c<1:P(m(A intersect [D^c,D])>=k)->1 as D->infinity},

where m(B)=max_x r_B(x). The detailed primary definition uses convergence in probability, in contrast to the short OWR phrase 'a.s. as D->infinity'. These modes are not silently identified. Exact beta_k values, their large-k entropy optimization, the prefix maximum and normal concentration of divisors are related but different questions.

## Current primary literature checked, 2026-10-02

1. Ford–Green–Koukoulopoulos, arXiv:1908.00378v3,12December2022,94pages, and the 2023 published134-page edition. The introduction, exact probabilistic definitions, Theorem2/Corollary1, Lemma2.1 with full proof and remark, and entropy-comparison scope were read. This gate does not claim a new independent reconstruction of the entire long entropy lower-bound proof. URL https://arxiv.org/pdf/1908.00378v3; published DOI https://doi.org/10.1007/s00222-022-01177-y.
2. Mao–Song, *Close Divisors of Typical Integers: The Ford–Green–Koukoulopoulos Conjecture*, arXiv:2609.22296v2,27September2026. The downloaded latest version has81pages; a web-cached unversioned PDF returned an older65-page version, so the local v2 is authoritative for this comparison. Its Theorems1.2 and1.5 claim alpha_k=beta_k/(1-beta_k) and equality of the strict/non-strict entropy thresholds with beta_k for each fixed k. It also records proposed local corrections to the FGK arguments. These are recent preprint claims, not independently fully audited here. They do not evaluate the large-k asymptotic beta_k or the sharp prefix exponent, and are not used as a premise that the prefix question is solved. URL https://arxiv.org/pdf/2609.22296v2.
3. De la Breteche–Tenenbaum, *On the concentration of divisors of powers*, current author PDF dated8September2026. Its introduction gives the original-divisor normal-order exponent gap approximately0.35332 to0.6102495 and treats powers/polynomial values. The raw downloaded date differs from a cached March2026 search snippet. This is not automatically an upper bound for the Bernoulli prefix model; no unproved transference is used. URL https://tenenb.perso.math.cnrs.fr/PPP/Delta%28n%5Er%29.pdf.

No primary source located in the bounded search determines the exact growth of M(D). This is a bounded literature observation, not a current-open or novelty certification. Recent results are separated from the mathematical inputs actually used.

## Prior-attempt gate

Exact ID/alias, 'logarithmic random', 'equal sums', and contribution-title checks covered GitHub issues/PRs, commit searches, target-path history and commit messages across475 locally mirrored refs, and413 live branch names. No matching prior proof attempt or invalidation was found. Two semantic commit matches concern a deterministic equal-row-sum/column-product matrix problem and are unrelated to random subset multiplicities. Current main rank401 is queued0/5. Related imported records were checked; no duplicate random-set target was found. This is not a claim of exhaustive full-text reading of all Git blobs.

Gate disposition: eligible for five genuine substantive turns on the explicitly labeled finite-prefix interpretation. The literal correction remains separate and credited. Retrieval, comparison and this gate count as zero author turns.
