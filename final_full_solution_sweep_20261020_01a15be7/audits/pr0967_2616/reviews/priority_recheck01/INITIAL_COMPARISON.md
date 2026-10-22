# Independent initial theorem comparison

Recorded 2026-10-21, before reading historical audit reports. Original author/public/REPORT.md was read; prior audit folders were not read. The assigned closure allegation was treated as a hypothesis. This comparison uses the original theorem and a fresh web fetch of the current primary PDF, section 3.44, printed page 60 (zero-based PDF page 59).

## Exact claim

In ZFC there is a countably infinite Hausdorff nondiscrete topological Boolean group admitting a partition into countably infinitely many dense sets but no sequence of pairwise disjoint finite subsets that meets every nonempty open set eventually. The topology need not be first countable or metrizable. Resoluble/resolvable here is a topological density property.

## Independent comparison

Both sources choose a free ultrafilter U on N, the Boolean group of finite subsets under symmetric difference, and identity-neighborhood subgroups H_A consisting of the finite subsets of A, for A in U. Both partition by the 2-adic valuation of support size plus one, and extend any support by new coordinates of A to achieve each desired color. Both defeat arbitrary disjoint finite block families by mapping each nonempty support to its maximum, extracting infinitely many disjoint finite maximum sets, splitting these by parity, and using the ultrafilter to select an open subgroup avoiding infinitely many blocks.

The original proof explicitly chooses pairwise disjoint maximum sets by point-finiteness. The current PDF chooses the stronger separated-block subsequence (maximum of one below minimum of the next), which follows from the same finite-preimage property. This difference does not change the theorem or mechanism. Both handle empty blocks and the unique possible identity-containing block. Both require only an ordinary free ultrafilter, not a selective or rapid one.

## Checkable derivation and adversarial checks

For a fixed integer r there are finitely many nonempty finite supports with maximum at most r. Disjointness of the block families therefore implies only finitely many blocks have any such support. Each finite maximum set eventually lies above any fixed bound, so a separated subsequence exists. Its parity unions are disjoint; either the even union is ultrafilter-large and misses all odd maximum sets, or its complement is ultrafilter-large and misses all even maximum sets. If an element's maximum lies outside A, the element is not in H_A. Hence infinitely many blocks miss a nonempty open subgroup.

The density step uses an unbounded sequence of support sizes in each valuation class and the infinitude of A minus a finite support. It does not require the dense classes to be subgroups. Deleting one coordinate distinguishes two different group elements, proving Hausdorffness. Each H_A is infinite, proving nondiscreteness. All quantifiers match the original target, including eventuality separately for each open set.

A small PDF indexing typo appears in its count of supports with maximum at most r (the printed exponential is not the exact count for either standard indexing convention); only finiteness is used, so this is immaterial. The exact count under N={0,1,...} is 2^(r+1)-1. No correctness gap is detected in the full counterexample.

## Preliminary conclusion

The current source contains the full same result and same proof family. This establishes overlap, not chronological priority. An internal September date, an upload path, or a claimed archived timestamp alone does not establish public availability of this exact content before the PR. The archival bytes and receipts remain to be checked. The topology's known Mathias/free-Boolean lineage remains distinct from publication of this full dense-partition plus obstruction theorem.

Completion estimate for assigned priority/source audit: 25% (content equivalence established; chronology and older-source scope open).

## Visual correction at 2026-10-21T20:33:09.575135+00:00

The initial note about a PDF counting typo was an extraction-reading error. The rendered PDF says 2^r - 1 for supports indexed by {1,...,r}, which is correct. The web extraction had displaced the exponent and minus-one. The count is immaterial beyond finiteness, but the source itself has no identified typo here. This correction was made after direct visual inspection, before any sealing.
