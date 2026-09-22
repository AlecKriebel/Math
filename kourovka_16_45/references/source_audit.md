# Source and convention audit

Checked during the 19 September 2026 research session.

## Primary sources

1. Official Kourovka Notebook site:
   https://kourovkanotebookorg.wordpress.com/
   The displayed most recent update is 1 September 2026.

2. September 2026 full 21st edition, 307 PDF pages:
   https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21tkt.pdf
   Problem 16.45 is on printed page 100, PDF page 100 (zero-based page 99).
   The relevant page was read as parsed text and inspected as a PDF screenshot.
   The statement attributes the question to P. J. Cameron. It defines maximal
   minimal-base size over all representations and maximal independent-set
   size, states the known inequality, and asks whether maximal Boolean
   meet-semilattice rank can always be realized with normal bottom.
   There is no attached solution comment at 16.45 in this version.

3. September 2026 separate update, 10 PDF pages:
   https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf
   No occurrence of 16.45 was found in its parsed text.

4. Peter J. Cameron, "The symmetric group, 7", 22 July 2010:
   https://cameroncounts.wordpress.com/2010/07/22/the-symmetric-group-7/
   Explicitly permits representations that are not faithful or transitive.
   His b_2 is the user's b, and his mu* is the user's mu'. His mu concerns
   independent generating sets for the whole group and is not mu'. His b_1
   concerns greedy/ordered irredundant bases; his b_3 concerns minimum base
   size. Neither is the invariant at issue here.

5. Peter J. Cameron, "Some measures of finite groups related to permutation
   bases", arXiv:1408.0968, posted 2014:
   https://arxiv.org/abs/1408.0968
   https://arxiv.org/pdf/1408.0968
   Uses b_2 and mu' for the invariants studied here. Propositions 3.1--3.2
   and Corollary 3.3 supply the underlying Boolean-lattice formulations and
   inequality. The paper asks the equality question rather than resolving it.
   These foundational results are attributed to Cameron, not claimed new.

6. Peter J. Cameron, "Groups, lattices and bases", 6 August 2014:
   https://cameroncounts.wordpress.com/2014/08/06/groups-lattices-and-bases/
   Restates the question and suggests systematic computational investigation.

## Convention decisions

A base for rho(G) has stabilizer ker(rho) when pulled back to G. Requiring
stabilizer 1 inside G for a nonfaithful action would change the problem and
would contradict the all-representations lattice formulation. Minimal means
inclusion-minimal, not smallest cardinality. Repeated points cannot appear in
a minimal base, so the sources' sequence language and the user's subset
language have the same maximal size.

The empty intersection is the entire ambient group. The empty base is a base
for the trivial permutation image. Empty independent sets are permitted, and
the trivial group has all the relevant invariants equal to zero.

The auxiliary b_f used in the proof means faithful-only maximal minimal-base
size. It is not silently substituted for Cameron's b_2. A more recent article
on regularity/base-related invariants surfaced in search with a faithful-only
convention; its terminology was not imported into this argument.

The Boolean construction preserves meets and the top element. No general
join-preservation or full Boolean sublattice is claimed. No quotient by a
nonnormal subgroup is taken. Cores are used only to compute a coset-action
kernel or to demonstrate explicitly why the coring shortcut fails.

## Literature search scope and limits

Focused searches included the problem number with Kourovka/Cameron, maximal
minimal permutation bases, normal-bottom Boolean meet embeddings, and later
base-related papers. A final check also searched the explicit complement and
the order 100920. These searches did not locate an earlier resolution.
Some very specific searches returned irrelevant results; those were not used
as mathematical evidence. The official notebook and primary Cameron sources,
not absence of search hits, establish the reported source status.

This is not an exhaustive bibliographic audit and does not certify priority.
No external mathematician was contacted and no publication was made. The
counterexample and its proof are the outcome of the work in this bundle,
not an existing result attributed to a retrieved source.
