# Independent audit of Hochman Pingree problem 1

## Verdict

Accept the negative answer for problem 4400001, AMR-043-0001, under the exact two-sided topological formulation in the frozen packet. Recommend `already_solved`, retaining the author's one research turn out of five. The result is a deduction from Ville Salo's published 2023 extension theorem, not a novel resolution or a new proof of that theorem. No substantive mathematical correction is required.

This audit binds to the 13,292-byte, nine-file author archive with SHA-256 `4b8fdb1f5a2115d73a5d7966671ee7488b1c2e03957261e1120a23ae0d9df724`. Every archive member matches the corresponding frozen file byte for byte. `BINDING.json` includes all nine file hashes, including the author's manifest. The author packet was read and executed without changing its bytes.

## Target and source match

The first problem attributed to Mike Hochman on page 1 of the 22 November 2010 Pingree list asks about the binary full shift and the proper three-coloring shift, indexed by the integers, after all periodic points are removed. The displayed question and its adjacent remarks were read from a newly downloaded primary PDF and visually checked. The remarks concerning Borel equivalence are separate from the question about topological conjugacy. A transposition in the final remark's notation does not redefine the deletion set.

The systems in the packet are exactly X = {0,1}^Z and Y = {y in {0,1,2}^Z: y_i differs from y_(i+1) for all integers i}. They use the usual product topology and its subspace topologies. The left shift is sigma(x)_i = x_(i+1). An aperiodic point means that sigma^n(x) differs from x for every positive integer n. The requested map is a homeomorphism commuting with sigma, including continuity of the inverse. A point with a periodic tail but no global period remains in the domain. These conventions agree with Salo's definitions on published pages 1683-1684.

Salo's Theorem 1 on published page 1683 applies to infinite transitive two-sided SFTs: conjugacies of their aperiodic parts extend uniquely to conjugacies of the full systems. The preceding page explicitly identifies the binary/proper-three-coloring pair and the 2010 Pingree question. The publication is Proceedings of the London Mathematical Society 127 (2023), 1681-1692, DOI 10.1112/plms.12567. The publisher records first publication on 25 October 2023. ArXiv records an initial submission on 20 April 2021 and version 3 on 22 September 2023. This is published prior work, regardless of a catalog's older open-status label.

The accessible search-index listing independently associates AMR-043-0001 with the same Hochman problem and formulas. The exact detail page remains inaccessible, so no claim is made about its current complete wording or AI notes. The internal numeric ID and selection rank are the supplied binding labels; the catalog bytes and remote blob match reported in the author metadata were not independently re-fetched in this audit. A catalog descriptor is not the raw problem record.

## Independent mathematical verification

### The full shifts satisfy the hypotheses

Both spaces are closed and invariant under the invertible two-sided shift. X has no forbidden words. Y has exactly the forbidden adjacent pairs 00, 11, and 22. Thus they are SFTs on finite alphabets.

For X, every binary word is legal and extends in either direction. For Y, a word of length n has three choices initially and two at each subsequent position. Every such word extends in both directions. Their language cardinalities are therefore 2^n and 3 times 2^(n-1). These unbounded cardinalities imply infinitude: in a finite shift-invariant set of k points, any length-n word can be shifted to position zero and hence there can be at most k such words. Both entropies equal log 2, but this equality is not used to force conjugacy.

The transition matrices are A = [[1,1],[1,1]] and B = [[0,1,1],[1,0,1],[1,1,0]]. A is positive. B squared has diagonal entries 2 and off-diagonal entries 1. If B^m is positive, then each entry of B^(m+1) sums two positive entries, so every B^m for m at least 2 is positive. A length-m transition path connects any two endpoint symbols for all sufficiently large m. Consequently any two legal cylinder words can be joined across every sufficiently long gap. This proves mixing of the full systems and therefore the transitivity actually required by Theorem 1. No claim about transitivity of the deleted subspaces is substituted for this hypothesis.

As a further check on the proof's stronger assumptions, every nonempty legal word in these one-step presentations is synchronizing: joining two configurations along that word preserves all adjacent transitions. Each one-sided cylinder in either direction has extensions with two choices at every new position. It therefore contains uncountably many tails, whereas periodic tails are countable. Aperiodic tails are dense. The same observations remain true after any positive power of the shift is represented by consecutive blocks. These facts directly establish the assumptions of the two-sided Theorem 3 used to prove Theorem 1 for this pair.

### The obstruction applies after extension

Assume the requested conjugacy h exists. The verified hypotheses permit the published theorem to give a conjugacy H from X to Y extending h. If x is fixed by sigma, then sigma(H(x)) = H(sigma(x)) = H(x). The two constant binary sequences are fixed points of X. Every fixed point in a sequence space is constant, while every constant three-color sequence violates the adjacent-inequality condition. Thus Y has zero fixed points. Even the image of one binary fixed point gives a contradiction.

The author's full-system periodic counts are also correct. The number fixed by sigma^n is the number of cyclic legal n-words, equivalently the trace of the nth transition-matrix power: 2^n for X and 2^n + 2(-1)^n for Y. These count periods dividing n; they do not count only least period n. The formulas follow from the spectra {2,0} and {2,-1,-1}, or the matrix recurrences A^2 = 2A and B^2 = B + 2I. In the aperiodic parts, both corresponding counts are zero. Accordingly these counts alone do not refute h. The extension theorem is the indispensable imported step.

## Inspection of the applicable proof

The complete two-sided Section 3, published pages 1685-1687, was read in the publisher's full text, the fresh author PDF, and the retained published PDF. The published theorem page and all three proof pages were rendered and inspected. The proof is not being inferred from the abstract, nor from the separate one-sided result in Section 4.

The audit followed these dependencies and checked the points where an invalid compactness or continuity shortcut would matter:

1. Close the graph of h inside compact X times Y. Density of aperiodic points makes both projections of the resulting relation surjective. Continuity of h and h inverse gives singleton fibers at their existing aperiodic arguments. The graph's printed domain uses X where it must use X prime. This is a notation slip, already disclosed by the author packet; using the actual domain of h resolves it.
2. For a periodic argument, pass to a common power of the shift and a block presentation. The aperiodic set does not change, because periodicity under sigma and under any sigma^m are equivalent. The relation's fiber is a subshift. An infinite fiber would contain an aperiodic point, which would have both its legitimate aperiodic preimage and the periodic argument as preimages, contradicting the singleton inverse fiber.
3. Once that fiber is finite, a further common power fixes it pointwise. Compactness now forces long constant source blocks to have constant output interiors. Otherwise a sequence tending to the fixed source would have an output limit with unequal adjacent coordinates. Blocking only normalizes the relevant finite lengths; it does not assume a global finite-window rule for h on its noncompact domain.
4. The half-tail sets used next are genuinely compact subsets of the aperiodic domain. A point that is constant on one half-line and has a mismatch just across the boundary cannot be globally periodic. They are closed subsets of the compact full shift. Continuity is therefore uniform near each such compact set. This supplies boundary-dependent output symbols for long constant blocks. The uniform-near-a-compact-set assertion follows by a finite cylinder cover; it does not require uniform continuity on all aperiodic points.
5. Synchronization lets the two boundary choices be joined. If they give different output symbols, the joined point forces incompatible values. If the join happens to be periodic, inserting one repeated symbol yields an aperiodic join with the same conflict. The argument also rules out the case where each side has a single possible symbol but those two symbols differ. Hence all limiting periodic fibers are singletons.
6. The singleton relation is a bijective extension. Its graph is closed in compact X times Y. More explicitly, a sequence approaching any point, including a periodic one, has no image accumulation value other than the unique graph value; compactness supplies accumulation values. This proves continuity there. The inverse follows symmetrically. Shift equivariance follows from the shift-invariant graph, or from equality of continuous maps on the dense aperiodic set. Density also proves uniqueness.

Two elementary supporting facts were separately checked rather than numerically presumed. First, an infinite compact one-dimensional subshift contains an aperiodic point: if a nonisolated point is periodic, take distinct points agreeing with it on longer central blocks, shift a first departure to the origin, and take a subsequential limit with fixed periodic phase. The limit agrees with a periodic point on a half-line and differs at the boundary, so cannot itself be periodic. Either left or right departures provide the construction. Second, duplicating a symbol in a nonconstant bi-infinite periodic configuration destroys global periodicity. If the modified configuration were periodic, its unchanged half-line would force equality with the original everywhere. On the other half-line this would equate the original with its one-step translate and force it to be constant. The finite insertion controls supplement these arguments only.

No substantive proof defect affecting this application was found. For general subshifts beyond this target, the proof's synchronization and density hypotheses must still be checked; this audit does not extend the theorem's scope. The exact SFT pair also avoids any ambiguity about admissibility of the half-tail gluing steps, because matching boundary symbols suffices.

## Independent computations and adversarial controls

The author's verifier reproduces its stored checks byte for byte: 275 assertions and 90,618 candidate words, with its own manifest and mutation controls passing.

The separate `independent_checks.py` imports no author code. It enumerates 269,813 candidate words of lengths 1 through 11, counts legality directly from symbol inequalities, determines least periods by every cyclic rotation, and compares with independently implemented Mobius inversion. Walk dynamic programming checks the transition identities through 64 steps. Eight symbol relabelings preserve legality and least periods. Another 8,190 words check the finite proper-two-coloring control. There are 18,884 bounded period probes for the symbol-insertion step. The complete run contains 20,532 checked assertions.

Twelve deliberate false claims are rejected. They cover entropy versus periodic counts, a coloring fixed point, omission of wrap-around, period-dividing versus least period, deletion of fixed points only, confusion with proper two-coloring, adding a forbidden loop, finite-system and mixing hypotheses, direct application of periodic counts to free parts, the one-sided eventually-zero boundary, and a nonperiodic finite defect. These are computational category guards, not a model checker for topological conjugacy.

The packet verifier also rejects one-bit changes, truncation, and appended bytes against every recorded nonempty file. It checks the exact file set, independently generated results, and, when supplied, all original archive members and the author's replay. None of these finite checks purports to prove Salo's theorem.

## Provenance and limits

The original Pingree PDF and Salo author PDF were freshly downloaded, and their byte counts and hashes independently match the frozen source metadata. The published-PDF endpoint returned HTTP 403 on the new retrieval attempt, and the web PDF open failed. The available retained published PDF was independently hashed, extracted, and visually inspected; its provenance is accurately labeled as a retained copy, not a fresh successful download. A separate successful read of the publisher's full-text HTML independently confirms the publication, theorem, definitions, and full two-sided proof. No login, access restriction, or remote state was changed.

A bounded title-and-correction search and the author publications page did not reveal a correction affecting the theorem. This is not proof that no correction exists. The original theorem is imported as established mathematics; this is a source-and-application audit, not formal machine verification or an exhaustive re-audit of every cited paper. Later examples and unrelated open questions are not newly certified.

The exact current catalog detail page, its complete AI research notes, selected full AI corpora, and every historical repository branch were not inspected. The earlier bounded repository searches and catalog hash claims remain attributed author metadata, rather than new audit findings. These coverage limits do not alter the independently verified primary mathematical target or the published exact resolution. No novelty, first-discovery, global-openness, or exhaustive prior-attempt claim is made.

The public audit consists only of newly authored analysis, code, results, and verification metadata. It includes no source PDF, source extraction, screenshot, raw catalog or dataset record, private coordination file, or private personal data. No remote writes, queue edits, PR creation, merging, release, or outreach were performed by this audit.

## References

- Open Problems, 3rd Pingree Workshop on Dynamical Systems, 22 November 2010, Mike Hochman problem 1, page 1: https://math.huji.ac.il/~mhochman/open-problems/pingree-open-problems.pdf
- Ville Salo, Conjugacy of transitive SFTs minus periodic points, Proceedings of the London Mathematical Society 127 (2023), 1681-1692: https://doi.org/10.1112/plms.12567
- Publisher full text: https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/plms.12567
- Author PDF: https://villesalo.com/article/CoTSmPP.pdf
- Published-PDF repository URL: https://www.utupub.fi/server/api/core/bitstreams/1eee4e7b-a0a1-42a5-8d69-df25f496cdf6/content
- Version history: https://arxiv.org/abs/2104.09860
- Author publication list: https://villesalo.com/publications.html
