# Independent priority review: PR166 / problem30002720

Audit completed UTC: 2026-10-12T11:09:40.523575+00:00. Completion estimate: 100% of this assigned priority-family review, not 100% certainty of novelty. Head: efc3f35a72543ad9ae76fd31a860116f1ffd4a32. Original submission status supplied in the assignment: claimed_solved1/5.

The explicit square-position rank was not found in an earlier theorem or earlier application among the primary sources inspected. This does not establish novelty. The underlying discontinuity-crossing mechanism has substantial prior overlap, and a post-seal Baire argument now gives a supported existential theorem: a residual set of fixed nonboundary ranks has failure under every deterministic center. That deduction does not identify the candidate's specified rank.

## Exact claim and review standard

The candidate uses stationary independent binary Markov strings with persistence 3/4, singleton-stopped Radix Selection bucket operations, the fixed word whose ones occur at j² for j≥2, and t=F(v). It asserts that (Y_n(⌊nt⌋+1)−c_n)/√n is non-tight for every deterministic real sequence c_n. The rank is a continuity point outside the cylinder-endpoint set.

A priority falsifier must match source, cost, fixed rank, stopping convention and universal-center quantifier. Process non-tightness, a boundary rank, a moving rank, a uniformly random rank, or a data-dependent center does not match. A new missing lemma is recorded as a gap, not as theorem equivalence.

## What is already present

The nearest primary paper is [Leckey–Neininger–Sulzbach, Process convergence for the complexity of Radix Selection on Markov sources](https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf), published in Stochastic Processes and their Applications 129 (2019), 507–538, DOI [10.1016/j.spa.2018.03.009](https://doi.org/10.1016/j.spa.2018.03.009). Its model and cost match. Its full relevant arguments were read; the printed boundary and adjacent theorem pages were also visually inspected.

The paper already isolates sampling across dense profile jumps, and uniform string-indexed fluctuation control can replace the candidate's weaker elementary error estimate. The universal-center boundary conclusion follows by an elementary two-atom concentration argument even though the printed statement specifies centers. The constructive continuity-rank bridge is the square-word local geometry: approaching jump distances are much smaller than sampling widths, while jump heights are much larger. See COMPARISON.md for equations and the precise dictionary.

The [2014 primary preprint](https://www.math.uni-frankfurt.de/~neiningr/aofa14.pdf) and [Leckey's 2015 thesis](https://d-nb.info/107268702X/34) were also checked on their relevant theorem proofs. First-order nonboundary behavior, process obstruction, and the thesis's explicit marginal-limit questions delimit the historical scope; they do not establish the exact candidate conclusion.

## New deduction tested after sealing

The first independent assessment was sealed at 2026-10-12T10:49:08.317007+00:00, before any ROOT or sibling verdicts were read. Its SHA256 is 27c6c6f469c0dd823307ce76654e097475f58f5d3cfd5be3916f9d0d5cde48fc and its mode is 0444.

After that seal the parent asked a scientific falsification question about Baire category, without providing a verdict. The proposed route is valid after removing the full endpoint set as well as rational rank breakpoints. At each dense nonzero-jump boundary, first-order cost has a two-atom limit with masses 1/2. Consequently any root-n interval has asymptotic concentration at most 1/2, uniformly over its center.

For fixed n, rank distributions are locally constant away from k/n. On the Baire space X=(0,1) minus all endpoints and rational breakpoints, the sets on which concentration is at least 3/4 for every n≥N are closed. Each is nowhere dense because every interval contains a known bad boundary and a nearby open rank cell with the identical distribution. Their countable union is meagre. Outside it, every radius has arbitrarily large sample sizes with concentration below 3/4, which excludes every deterministic center.

This is a checkable deduction assembled in this audit from published boundary evidence and standard Baire machinery; the full proof and edge-case checks appear in COMPARISON.md. No explicit earlier radix Baire application was located. Ordinary linear uniform boundedness does not apply directly, and is unnecessary. The argument strengthens the coarse existential conclusion but does not certify the square-position rank. A new application of old tools alone is not evidence of historical preemption.

## Broader approaches and exact gaps

The reviewed general-source trie theorems include Markov and dynamical sources, but their global path-length, size, height or uniform-branch-depth statistics differ from the selected-path weighted bucket cost. The older bucket-selection theorem matches the cost under uniform digits and uniform random rank, not the present source and fixed rank. Density-model depth theorems additionally assume a Lebesgue density, whereas the Markov binary numeric law here is singular.

The nonregular L1/quantile route was checked against an actual theorem and its full proof. The relevant profile has signed jumps in every interval and is not locally an inverse CDF. An inverse-modulus theorem therefore needs a new valid dictionary and local signed-profile control. The comparison table records exact assumptions and failure points, not merely related titles.

No deterministic-centered, root-n convergence theorem for measure-theoretically typical fixed ranks of this nonmemoryless source was found in the inspected sources. The new residual-set conclusion is topological and makes no almost-everywhere claim. The first-order theorem covers continuity ranks and is compatible with the candidate's failure.

## Evidence limits, independence and disposition

Only the three permitted candidate/neutral submission bodies were read: COUNTEREXAMPLE.md, problem.json and source_manifest.json. Their exact identities, all independently retrieved primary source identities, actual read scopes, and web-only access limitations are in EXTERNAL_INPUTS.json. Searches were bounded; SEARCH_LEDGER.json records retained and unretained search batches. Source bodies, search outputs and rendered source pages remain private.

The submission's source audit, review, gate, status, verification and research notes were not read. No ROOT or sibling notes or verdicts were read. No other individual was contacted; internal coordination was only with the assigning parent. No Git, index, ref, branch, checkout, PR, remote, publication, tracker or release mutation was performed.

Disposition: priority not falsified for the exact constructive rank within this reviewed family; novelty remains unestablished. Published overlap must be disclosed. A broad claim that continuity-rank all-center failure requires the square construction is unsupported, because the Baire deduction proves existence without it. The precise remaining historical question is whether an earlier primary source already applied an equivalent argument, or independently treated this exact deterministic rank/profile geometry. No assertion of an exhaustive search is made.
