# Independent recent/official priority audit: PR967 / 2616

Submitted target: immutable HEAD `b356dec5cb01e5f536b9cfeece56ad08844c03cb`. This is a priority-family report only. It is neither an entire-package review nor an acceptance decision.

**Adverse priority finding: an earlier-dated accessible preprint gives the complete exact result, with the same group, dense coloring, and obstruction. The submitted result must not be promoted as a new resolution on the evidence now available.**

The primary source is *Results on problems from the Kourovka Notebook*, credited on its title page to Codex gpt-6-astra, Michael Kinyon, and Josef Urban, mathematical edition Version 4, dated 19 September 2026. Section 3.44, printed/PDF page 60, gives a countably infinite Hausdorff Boolean topological group, a countable dense partition defined by `v2(|s|+1)`, and a proof that every disjoint finite-block sequence fails. It uses an ordinary free ultrafilter in ZFC. I read the complete target section, rendered and visually inspected the whole page, and independently reconstructed every step. No mathematical gap remains in this lead. The source is linked by the official repository under the generic label “Solutions of several problems”:

- [Official primary preprint](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf)
- [Official repository index](https://kourovkanotebookorg.wordpress.com/repository/)

The fetched preprint has 598,093 bytes, SHA-256 `eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7`. Complete mathematical adjudication is in `MATHEMATICAL_ADJUDICATION.md`; date evidence and its limitations are in `CHRONOLOGY.md`.

## What the official status does and does not establish

Fresh retrieval on 16 October 2026 confirms arXiv 1401.0300 latest v48, submitted 6 October 2026 07:25:00 UTC. Target 21.107 remains unannotated on printed/PDF page 193. The current direct official PDF has the same target wording. The repository index has no separate target-numbered entry. Those observations are accurate but insufficient: the generic attachment contains the complete exact answer. Thus the earlier absence of a target-specific index entry or annotation cannot support novelty.

The older 15.80 annotation on v48 page 97 records an uncountable box-product example and a dense-partition result. Its uncountable example fails the target's countability hypothesis; a partition theorem alone does not settle the finite-block conclusion. The decisive new finding in this audit is the complete countable proof in the generic recent preprint.

## Chronology assessment

The preprint's title-page date is 19 September 2026; its PDF CreationDate is 2026-09-19T12:47:43Z. The official server reports Last-Modified 24 September 2026 16:57:52 GMT. The immutable arXiv v47, submitted 30 September 2026, already cites this exact official attachment URL. These all precede the submitted candidate's October 2026 package.

This supports an earlier September preprint under ordinary bibliographic dating. I did **not** independently obtain a cryptographically fixed September copy of the whole preprint body. An archive-index attempt failed with HTTP 503. The v47 citation authenticates the URL's earlier circulation, not the precise bytes now served there. If a promotion standard demands immutable historical body authentication, that narrow chronology check remains open; it does not justify any novelty claim or promotion while this explicit earlier-dated complete proof exists. This audit assigns neither ultimate first discovery nor misconduct.

## Other serious recent leads

Aurichi–Maesano–Zdomskyy, [arXiv:2510.11033v2](https://arxiv.org/abs/2510.11033), first submitted 13 October 2025 and revised 6 July 2026, studies density selection properties. I inspected the relevant definitions, all introductory theorem statements, and Question 1.7. Its non-H-separability statements concern varying dense sequences. They do not by themselves rule out finite blocks from the constant underlying space, and its theorems cited here do not supply an exact countable group counterexample. No equivalence was silently assumed.

Dow–Pecoraro, [arXiv:2509.22590v2](https://arxiv.org/abs/2509.22590), first submitted 26 September 2025 and revised 21 October 2025, supplies non-H-separable spaces that are mH-separable. I inspected Theorems 1–3, Corollary 4, Definition 5, and the discussion of monotone selection. The elementary thinning lemma in `MATHEMATICAL_ADJUDICATION.md` shows that countable crowded T1 mH-separable spaces **have** expansive disjoint finite blocks. Hence these examples do not supply the target obstruction. Additional assumptions on some of those theorems were retained.

A GitHub metadata search found an exact-target repository created 6 September 2026. Target-only inspection of its current main contents, research tree, result tree, and README showed a scaffold with empty candidate-artifact and admitted-result records, not an inspected complete proof. Branches and PRs were not exhaustively investigated. No unrelated repository proof package was read.

## Scope, independence, and disposition

The complete query ledger records exact and variant identifiers, phrases about expansive sequences and finite blocks, and groupable-density/H/mH terminology. Search failures and access failures are recorded. Search absence is not a firstness certificate. This family did not read the independent classical family's findings. It did not contact anyone, prepare outreach, install software, mutate Git, publish, accept, or merge anything.

**Recommendation:** withhold novelty clearance and any promotion as a novel solution. Have the parent audit independently verify the earlier preprint's Section 3.44 and assess the historical-date qualification. The mathematical overlap is exact and checkable; ultimate firstness and complete literature coverage are not established. The current proof can remain a correct independent verification or rediscovery, with attribution and appropriately limited claims.
