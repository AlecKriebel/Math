Saved UTC: 2026-10-21T20:31:34.991511+00:00

# Initial independent mathematical analysis

Saved before reading original audit_1, audit_2, acceptance, or any historical closure/conclusion.

## Exact hypothesis and target

Directly inspected the downloaded official arXiv 1401.0300v48, PDF/printed p. 193 and predecessor p. 97, using full-page text extraction and rendered images. 21.107 asks whether a countable topological group partitionable into countably many dense subsets admits pairwise-disjoint finite blocks F_n eventually meeting each open set. The intended open sets must be nonempty; the literal empty open set makes the property impossible for every group. The candidate addresses the meaningful stronger interpretation. There is no first-countability, metrizability, connectedness, or subgroup-partition hypothesis on these pages.

The predecessor p. 97 has the same eventual-intersection definition without countability and records an uncountable box-product counterexample. It also mentions a simultaneous resolvability result for abelian groups with finitely many involutions, but that is not the present Boolean group and is not a proof dependency here. No claim of target novelty follows solely from the unannotated current problem.

Directly inspected 1612.04878v1 Section 8 p. 25. Its last paragraph identifies the Mathias topology with the free Boolean linear topology and gives the identity neighborhood base [empty,A], for A in the filter, equal to finite-subset subgroups. Thus the construction lineage is accurately identified, without requiring any selectivity hypothesis from adjacent results.

## Independent reconstruction

1. Let U be any nonprincipal ultrafilter extending the cofinite filter on N, whose existence follows from Zorn in ZFC. A chain union of proper extensions is proper. If a maximal filter does not contain C, then adjoining C would be improper, so some filter member is disjoint from C; upward closure gives N\C in U. No finite member is possible because its cofinite complement is already present. No special ultrafilter property is needed.

2. G consists of all finite subsets of N under symmetric difference. Encode a finite set s by sum_{k in s}2^k: this is a bijection G -> N, so G is countably infinite. H_A consists of finite subsets of A and is a subgroup. H_A cap H_B = H_{A cap B}; intersections of cosets, if nonempty at x, equal x+H_{A cap B}. Covers and finite intersection refinement prove the base axiom. For sums, (s+H_A)+(t+H_A)=(s+t)+H_A, proving joint continuity; inversion is identity. Excluding one differing coordinate by a cofinite A gives disjoint cosets of any two distinct elements, so Hausdorff. Each A is infinite and each H_A is infinite, so no isolated point exists. The clopen subgroup base also implies zero-dimensional regularity if a stronger separation convention is implicit.

3. Color s by nu_2(|s|+1). Each nonnegative integer has exactly one color and every j occurs. For a coset s+H_A and color j, choose q >= |s| from the unbounded progression q = 2^j(2r+1)-1. Add q-|s| fresh points of A\s. This produces a member of that coset of size q and color j. The fresh-coordinate choice is legitimate because A is infinite and s finite. This is an explicit partition into exactly countably infinitely many nonempty dense sets; the parts need not be subgroups.

4. For arbitrary pairwise-disjoint finite group blocks F_n, infinitely many empty blocks already violate the conclusion for G. Otherwise discard finitely many indices until all remaining blocks are nonempty and contain no identity; disjointness ensures the identity occurs at most once. Put M_n = {max(s): s in F_n}. Each M_n is finite nonempty. For a fixed k, there are exactly 2^k nonempty finite s with max(s)=k. Because no s is repeated across blocks, k occurs in at most 2^k of the M_n. This is point-finiteness, not uniform finiteness, and it is sufficient.

5. For any finite union B of already selected M_n, the indices meeting B form a finite union of finite sets. Beyond those indices and the last chosen index there remains an eligible index. This recursively selects infinitely many M_{n_i} with strictly increasing indices and pairwise-disjoint supports. The mechanism fails for a merely point-countable family and depends essentially on the finite-to-one maximum map.

6. Split that disjoint subsequence into even/odd unions C_0,C_1. A proper filter cannot contain both because their intersection is empty. Choose a side C_epsilon not in U; there can be TWO such sides, which causes no issue. Ultrafilter decisiveness, rather than freeness alone, gives A=N\C_epsilon in U. Every member s of each corresponding F_{n_i} has max(s) in C_epsilon, so s is not contained in A and F_{n_i} cap H_A is empty. Strictly increasing n_i of one parity are unbounded; hence the eventual meeting criterion fails. H_A contains the identity and is nonempty open.

## Deliberate attempted failure modes

- Empty blocks and the identity make max undefined but are explicitly removed using the exhaustive cases above.
- Maxima sets can overlap heavily and their sizes need not be bounded. Point-finiteness nevertheless gives the disjoint subsequence; no hidden bound is used.
- C_0 and C_1 need not partition N; only disjointness is needed. The complement is of a chosen nonmember C_epsilon, not necessarily of the union of both.
- A single missed block would not suffice. Infinitely many selected indices of the chosen parity are genuinely unbounded, so the proof establishes failure of the eventual quantifier.
- A free filter lacking ultrafilter decisiveness need not yield the complement step. The cofinite filter is a useful negative control: on this same countable group its topology is metrizable and one can build disjoint finite blocks hitting each of its countably many basic cosets eventually.
- A principal ultrafilter lacks the needed freeness. Its H_{singleton} base neighborhoods are finite, so it cannot support a countably infinite dense partition. Finite principal ultrafilters cannot certify this infinite proof.
- Dropping block disjointness destroys point-finiteness: repeated singleton group blocks can have constant maxima. The theorem under audit assumes disjointness exactly where needed.
- Dropping finite blocks makes M_n possibly infinite; the induction then has no finite exclusion guarantee.
- Replacing eventual meeting by infinitely-often meeting is a different condition and is not disproved merely by infinitely many misses.

## Initial verdict and precise remaining tasks

No mathematical gap found in the complete ZFC counterexample, conditional only on the standard nonempty-open reading of the primary statement. This is a validity judgment, not a priority/novelty judgment. The strongest verified result is the universal infinite proof reconstructed above; finite checks will only test its elementary identities and demonstrate that controls catch altered hypotheses. Remaining work: implement independent finite controls, inspect original scripts for writes before copying/rerunning any selected ones, compare original audit arguments after this file is saved, verify custody/hashes, and seal the independent record. Completion estimate: 45% of this audit task, not a probability of theorem truth.
