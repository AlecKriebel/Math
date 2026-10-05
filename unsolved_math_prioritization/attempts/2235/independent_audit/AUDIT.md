# Independent audit: EP-655 / 2235, rank 765

Audited 2026-10-05 UTC. Verdict: **PASS, strictly scoped to known literal-counterexample verification and source correction.** This is neither a new solution nor an audit of a solution to the historically restricted question.

## Binding and publication disposition

The audited author archive is `ERDOS_2235_AUTHOR_SAFE_FREEZE.zip`, 15,683 bytes, SHA-256 `e5d6e7b26638daf7cedcc4e20456bb3bef3af3e5df3686ffa312164c3e072615`. Its ten files match the author directory byte for byte. The author manifest SHA-256 is `8c709f826b2646098379f87aa3b1a56a54f1486fb1839a6283f7159a12c07b56`. All nine manifested payloads match. The author freeze was not edited.

Recommended queue disposition: **unsolved, 1/5 substantive routes, zero original solution credit**, qualified by: **the displayed literal statement has an already-known regular-polygon counterexample; the intended historical target remains unresolved by this investigation.** “Unsolved” here applies to the ambiguous/historical queue target, not to the truth value of the explicitly defined literal statement.

The author's proposed `already_solved` designation is mathematically defensible only in a field that unambiguously identifies the displayed literal formulation. Do not apply it to a single undifferentiated “Erdős Problem 655 resolved” state. Publication that loses this distinction is **REVISE_REQUIRED** and is not covered by this PASS. No change to the elementary proof is required. This audit supplies an explicit conservative publication disposition; it does not silently rewrite the frozen author's separate recommendation.

## Mathematical review

Let A2 mean that every positive-radius circle centered at a selected point contains at most two selected points on its circumference. The center is selected; the circumcenter of the construction is not. “Circle” cannot be replaced by “disk.” Work with distinct points and positive distances, as the author does.

1. **Universal bound.** From any point, the other n−1 points split into distance fibers of size at most two. The count is at least ceil((n−1)/2) = floor(n/2), including odd n. Every pinned distance belongs to the global distance set. Therefore the global count D and maximum pinned count M are at least floor(n/2), and the sum S is at least n floor(n/2). These are minima over A2, not equalities for every admissible set.
2. **Construction.** For n ≥ 2, unit-circle points at angles 2πj/n are pairwise distinct. Squared chord length for index difference a is 2−2 cos(2πa/n). Folding a to k = min(a,n−a) gives positive length 2 sin(πk/n), 1 ≤ k ≤ floor(n/2). Sine is strictly increasing on this interval. Thus there are exactly floor(n/2) distinct lengths, not merely an upper bound.
3. **Multiplicity and parity.** From a vertex the only points at the kth length have offsets +k and −k. They are different except at k=n/2 for even n. Odd n has (n−1)/2 fibers of size two. Even n has n/2−1 fibers of size two and one antipode. Hence the polygon satisfies A2, and all three universal bounds are attained simultaneously. The singleton gives all counts zero; n=2 also works without treating two points as a nondegenerate polygon.
4. **Quantifiers.** Given any c>0 and any eventual threshold N, choose n≥max(2,N). The construction has D=floor(n/2)≤n/2<(1+c)n/2. Therefore it refutes the existence of a fixed positive c with the eventual universal property. It is not merely a finite small-n counterexample. The same construction refutes the corresponding A2-only maximum and sum improvements.
5. **Circumcenter.** All vertices have norm one, so the origin is absent. A circle centered there is irrelevant to A2. Adding the center makes the hypothesis fail for n≥3. The author's square-plus-center negative control correctly detects this.
6. **Convexity and cocircularity.** For n≥3, tangent support lines show all vertices are extreme, and no line meets the circumcircle in three distinct points. Adding convex position or no-three-collinear to A2 leaves the counterexample intact. For n≥4 the construction violates no-four-concyclic. No lower bound for arbitrary convex sets after deleting A2 follows from the fiber argument. Our exact convex quadrilateral negative control confirms that convexity alone need not imply A2.
7. **Zero-distance convention.** If self-distance is included, the polygon has floor(n/2)+1 values. Choosing n>2/c still contradicts the eventual linear improvement. The exact minima asserted in the packet deliberately concern positive distances.
8. **Distance graphs.** Each chord-length graph is a union of cycles, or an antipodal matching. They partition the complete graph while allowing crossings in their straight-line drawings. A degree bound of two does not itself give a planar-graph restriction on their union. The queue's proposed geometric-compatibility excess fails under its literal hypothesis.

All steps of the all-n argument pass. The claim min D=min M=floor(n/2), min S=n floor(n/2), under A2 is correct. No assertion of uniqueness of minimizers is warranted or made.

## Source fidelity and target identity

The complete pinned dataset contains one exact target record with ID 2235 and code EP-655. Its statement hash is `371b53206be00b0d92af1e4a9f5a6148f46412ad2f2262db7f498f22ffdd35e1`. Its background already records Hunter's objection and uncertainty about an intended repair. Independent full-corpus SHA-256 checks match the public snapshot manifest; the full catalogue additionally matches its pinned live Git blob. The source record is not a newly discovered open theorem.

The inspected 1988 primary source, [Some old and new problems in combinatorial geometry](https://www.renyi.hu/~p_erdos/1988-32.pdf), printed p.35, explicitly includes both A2 and no-four-concyclicity. Equation (6) concerns the maximum pinned count, and the following discussion proposes a sum bound and already identifies the polygon obstruction when the cocircularity restriction is removed. The page image was visually checked. Its initial bound is (n−1)/2, not n/2 for odd n. Its display does not reproduce every eventual quantifier of the modern formulation. It supports the historical distinction, not an assertion that the 1997 text is identical.

The [journal's November 1997 contents](https://www.jams.jp/notice/mj/46-3.html) independently confirm Paul Erdős, *Some of my favourite unsolved problems*, Mathematica Japonica 46(3), 527–537. The precise passage behind Er97e remains **unretrieved and unverified**. No inferred repair is attributed to that unseen passage.

The [April 22, 2026 overview](https://www.ulam.ai/research/erdos655-overview.pdf), Theorem 3.1, already contains the exact A2 minima. It has no byline in the inspected first page and is a linked, unrefereed overview. Its mathematics was checked independently; it is not used to certify current resolution of repaired variants. The author's warning about its odd-n historical paraphrase is justified.

A fresh [FormalConjectures registry](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/655.lean) read returns Git blob `9720889b50b26dd2d73599cd0e94689465fbe38e`. The literal theorem is marked solved with negative answer; its A2-plus-general-position variant is marked open. Both local theorem bodies contain `sorry`. The linked external formalization was not built or certified. A registry label is not a replayed proof certificate.

Direct main-tracker and UnsolvedMath target-page requests returned 403. Search-served [tracker discussion](https://www.erdosproblems.com/forum/thread/655?order=newest) records OPEN, ambiguity, Hunter attribution and five comments through April 22, 2026, but is labeled months old. This independently corroborates the distinction while leaving live dynamic status uncertified. The audit does not substitute search freshness for a successful live check.

The two restrictions are logically different: A2 bounds points on circles whose centers belong to X, whereas no-four-concyclicity restricts all centers. Also M≤D: a lower bound for M would imply a global bound on the same class, but changing the class invalidates any claimed refutation. The 1988 pinned problem and the current general-position/global variant are not settled here.

## Exact controls and independence

The author's 711,511 controls replay identically in normal and optimized Python. Their sum and principal loop counts were recomputed. These checks are highly related regression cases, not 711,511 independent pieces of mathematical evidence. In particular, the author's ceiling/floor code simplifies to a tautological integer expression; the written proof establishes the claim, and our replacement control checks both defining inequalities for the least integer bound.

The separate `independent_verify.py` passes **711,870 controls**, including 690,880 exact chord comparisons for n=2,…,128. It uses a different arithmetic path: for an integer polynomial q and a primitive nth root ζ, sum |q(ζ^u)|² over gcd(u,n)=1. Expanding gives integer Ramanujan sums c_n(t)=sum_{d|gcd(n,t)} d μ(n/d). This identity follows by inserting the Möbius indicator for coprimality and summing geometric series. The nonnegative trace vanishes exactly when q(ζ)=0, because the primitive-root evaluations are conjugates. No floating tolerance or imported author arithmetic is used.

Additional independent controls cover positive chords, odd/even fibers, graph degrees and edge counts, exact rational c values, singleton and antipodal boundaries, a convex but inadmissible quadrilateral, an admissible nonminimal collinear set, and circumcenter insertion. Mutation tests reject changed payloads, missing files, extra files and symlinks. Normal and optimized independent outputs are byte-identical. These are finite regressions; the all-n conclusion rests on the reviewed proof.

## Repository and scope limits

At pinned main `6144d964777214c6963a915288c18fcf97b42026`, a fresh queue read shows rank 765, queued 0/5. Pinned source observations and matching Git object hashes show no ID-2235 state entry, no exact target in 48 history events or 23 assessment events, and no exact-ID related-group entry. The earlier bounded PR/branch/commit checks are consistent with no prior attempt, but were not independently repeated as an exhaustive repository search. No assertion about every historical branch is supported.

All review files contain authored reasoning, code, public source metadata and verification results only. No PDF, screenshot, source extract, raw dataset record or coordination file is included. There were no remote writes. AI-assisted independent review is not human peer review. The author packet remains immutable; this audit binds only the stated bytes and does not automatically cover later edits.
