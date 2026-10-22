# Approach log and stopping point

Date: 6 October 2026. Maximum authorized budget: five substantive approaches.

## Preflight: inherited record and prior work

- Read the entire matching problem record, including its background, from the complete problems dataset.
- Read the complete report entry: absent, so the stipulated default is the empty object.
- Verified the three supplied full-file SHA-256 hashes, the statement hash, and the default-json-serialization complete-pair hash.
- The inherited background is generic literature/status triage; it contains no mathematical proof to count as a prior substantive attempt.
- GitHub search in AlecKriebel/Math: issue/PR text queries for the exact title, GREEN-048, ham sandwich, Kupitz, the conjunction of 136 and balanced, and unbalanced; default-branch code queries for exact title and GREEN-048. No matches returned.
- Branch searches for ham, 136, and balanced were followed through terminal null cursors. Returned branches concerned other problem identifiers or topics. No matching prior attempt located. The search did not enumerate every historical commit, and no exhaustive absence claim is made.
- The requested unsolvedmath problem URL was attempted first but was unavailable through the web reader. The exact target was recovered from the hash-verified complete problem record and matched to Green's author-hosted Problem 75.

## Source recovery and literature checks

Inspected Green's statement and comments; Pinchasi's definitions, Theorem 1.2, its discrepancy consequence, and Conjecture 7.1; Conlon-Lim's introduction, Theorems 1.1-1.3, and the distinction between straight lines and generalized configurations; the introduction and results summary of the 2025 automated-symmetry paper; July and September 2026 material by Kalai.

A lower-bound inequality mismatch was detected and resolved conservatively: the primary evidence establishes examples with D=2, not D>=3. The survey's stronger phrase is not relied upon. The 21-point computational construction/minimality was recorded as a published report, not independently rerun.

Search terms included Kupitz-Perles conjecture, Pinchasi lines with many points on both sides, Conlon Lim everywhere unbalanced configurations, 2025/2026 qualifiers, and automated symmetric constructions in discrete geometry. No verified straight-line resolution was located. Sources and exact inspection scope are retained in SOURCES.md.

## Substantive approach 1: rotate from an exposed vertex with exact blocks

Rather than pretending simultaneous crossings are single events, order the rays from an exposed vertex and retain their complete collinear blocks. A median block yields the exact discrepancy formula |n-1-r-2s|. Parity gives the local bound m_p-2+(n mod 2). This is a complete proof for the stated bounded-collinearity subclass, but its bound grows with block size.

## Substantive approach 2: perturbation and limit audit

General-position halving lines can be passed to a fixed-pair subsequence. The remaining points collapsing onto the limiting line produce an unavoidable error term of at most k-2. This reproduces the global bound and identifies precisely why the naive limiting proof of a uniform constant fails. A family of chosen bisectors demonstrates arbitrarily large loss in a degenerate limit, without purporting to refute existence of a different good line.

## Substantive approach 3: exact structured classes and obstruction extraction

A centrally symmetric configuration admits a zero-discrepancy determined line. A line with at most 100 points off it directly solves that instance. The angular and rich-line inequalities give necessary structural conditions for any counterexample. Weighted multiplicities are shown to change the problem and are excluded from the target.

## Stopping point

Three substantive approaches used; no inherited substantive attempt. The remaining general case has unbounded collinear blocks without the proved symmetry/rich-line hypotheses. The known pseudoline obstruction means unrestricted allowable-sequence reasoning alone cannot close this gap. Stop with a bounded partial, exact source correction, and explicit unresolved target. No numerical experiment, claimed full resolution, or publication was performed.
