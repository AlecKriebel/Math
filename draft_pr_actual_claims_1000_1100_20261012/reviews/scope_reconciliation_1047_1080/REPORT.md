# Independent scope reconciliation: PRs #1047 and #1080

Review completed 13 October 2026 UTC. Best estimate: **100% of this assigned scope review**; this does not estimate mathematical validation or the publication program. Both PRs contain complete asserted answers that should enter the full audit workflow. Neither mathematical truth nor novelty is accepted by this report.

The review read the pinned PR bodies, authored status and claim documents, and relevant source audit/report. It independently retrieved and visually inspected the exact original primary-source questions. No submitted program was executed; no PR, queue, publication or external service was changed. Input identities are in `INPUT_PINS.json`, source retrieval and inspection identities in `SOURCE_RETRIEVAL.json`, and decisions in `CLASSIFICATIONS.json`. Raw third-party material is locally excluded from Git.

## PR #1047: admit its complete negative uniform claim

Pinned head: `56b3a35182e5cb04b05e41f5017e47caf50582c1`. Problem `30004909` / `OWR-8415356-020`.

The complete Végh contribution in [Oberwolfach Report 53/2021](https://ems.press/content/serial-article-files/46931), printed p.2946 / PDF page54, asks about normalized nonnegative monotone submodular functions and approximation by one matroid rank on the same set. The displayed comparison is

\[
 r(S)/\alpha\le f(S)\le\alpha r(S),\qquad S\subseteq V.
\]

The primary page confirms the denominator omitted by the catalogue transcription. It contains no extra weights, scalar rescaling, sum of ranks, enlarged set or computational-oracle requirement. The next contribution starts on the same page, so no continuation was missed. The source calls for a “constant α > 0” without separately printing a quantifier over every finite ground set.

The PR explicitly asserts a complete negative answer to the dimension-independent interpretation and supplies two purported obstruction families plus square-root-family sharpness. Its status calls this a full negative result. This is more than partial progress and merits the full mathematical and priority audits.

The inferential boundary must remain visible: the displayed source does not say verbatim that α is independent of |V|. Reading “constant” uniformly is the nontrivial interpretation used by the PR. If V is fixed and α may depend on |V|, singleton normalization, monotonicity and submodularity place every nonempty value between 1 and |V|; the rank-one uniform matroid consequently gives a finite dimension-dependent factor. That elementary scope observation explains the uniform reading but is not author-intent evidence or acceptance of the PR's obstruction proof.

Recommended disposition: **workflow eligible**, for the precise ordinary-rank, same-ground-set, source-corrected uniform question. Do not advertise a theorem about weighted or scaled ranks, sums, larger ground sets, another intended output class, or the optimal exponent over all inputs. The PR's no-priority assertion does not substitute for the priority audit required by the user.

## PR #1080: admit the complete boundedness clause, retain the partial bundle

Pinned head: `64b252b199f2692eef2545656190c14bcaf63889`. Problem `11000150` / `AMR-109-0150`.

The [author-hosted source book](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf), Wajnryb chapter8, printed p.126 / PDF page133, states the restricted Smith question for a fixed genus-g one-boundary surface, one positive boundary twist and factor curves intersecting pairwise in zero or one point. It asks: “What is the maximal length n of such a product? Can it be arbitrarily long?” These are separately explicit questions. The source's genus-two discussion expressly allows repetitions.

The PR asserts bounded length for every fixed g≥1 and, more strongly, finitely many simultaneous-conjugacy classes of ordered factorizations. That assertion completely answers the second question negatively within the stated twist convention. It does not determine the numerical maximum for g≥3. Calling the whole bundle partial is correct; treating that label as a reason to ignore the complete binary clause would miss an asserted original-question resolution.

The inspected context distinguishes this restricted question from the unrestricted Smith question on printed p.125 and neighboring positive-Artin/Hurwitz classification questions. Chapter introduction p.122 explicitly uses orientation-preserving mapping classes fixing the boundary pointwise. Those conventions match the PR. Fixed genus is essential: allowing genus to vary changes the quantified target.

A source-language caution must be preserved. The question and chapter introduction do not expressly say that disk-bounding curves are excluded. The PR does exclude them. If identity twists about such curves count as factors, one can insert them repeatedly and get trivial arbitrary lengths. The p.124 discussion credits a no-positive-identity assertion and the surrounding discussion concerns geometric twists and vanishing cycles, supporting the usual nonidentity-twist reading. This is contextual interpretation, not an explicit missing word silently supplied to the source. Any paper must state the essential/nonidentity convention prominently. The source has no issue with the PR's broader permission for boundary-parallel factors; permitting them only strengthens its asserted boundedness statement.

Recommended disposition: **workflow eligible for the complete restricted boundedness clause**, with the overall maximum-length bundle still partially unresolved. Preserve the exact M(g) gap, absence of an explicit upper-bound formula or effective stopping rule, and absence of an extremizer/equivalence classification. Do not market this as a resolution of the unrestricted question or the whole question bundle.

## What this decision does and does not establish

Eligibility is claim-based, as requested. It does not validate the obstruction proofs, the Higman or topological arguments, source applicability of auxiliary results, any claimed stronger finiteness theorem, or mathematical novelty. Those belong to fresh adversarial math and priority audits. No conclusion is drawn from stale QUEUE status or from historical acceptance language. Both PRs currently withhold priority and human-peer-review certification; any eventual preprint must accurately retain those limits and the extensive AI disclosure.
