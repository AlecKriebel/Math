# Construction research log — 21.136

## 2026-10-24 17:16 UTC — independent start (5%)

Read root AGENTS.md, exact original problem, source/priority audit and the complete cached published Wilson paper. The target is arbitrary profinite groups and the actual strict continuum cardinal bound. Begin with compact semidirect products, inverse-limit wreath systems, nonmetrizable coordinate fusion and torsion extensions. No reliance on QUEUE.md, PRs or external communication.

## 2026-10-24 17:19 UTC — normal abelian kernel obstruction (10%)

Derived independently: with A closed normal abelian and G/A torsion, any p-infinite x in A has continuum many unit powers modulo ambient fusion, because a conjugator's induced unit has finite order. Generalized to normal abstract locally nilpotent A using iterated commutators. Sent the restricted result to parent only after the independent derivation. Assigned a fresh internal adversarial reviewer. No complete-resolution claim.

## 2026-10-24 17:22 UTC — general procyclic strengthening and explicit candidate failures (12%)

Reviewer independently verified the p-infinite lemma and strengthened the abelian case to avoid the finite-prime reduction. For arbitrary infinite procyclic C, compact torsion normalizer images have bounded exponent, whereas Aut(C) has unbounded exponent. The locally nilpotent extension uses residue-unit images when infinitely many primes occur; the full image is not asserted torsion in that case. Recorded proofs and finite-series consequences in approach_constructions.md. Parent reports the abelian lemma was independently found by the parallel Lie route; mechanisms exchanged only after independent derivations.

Affine translation fusion gives countably many classes within the translation subgroup but continuum classes from its multiplier quotient. Continuous compact coordinate-permutation groups have finite coordinate orbits; block-order invariants exclude nontorsion finite-factor product bases. The standard full iterated C_p wreath limit has dense torsion, yet explicit antichain-supported odometers give continuum infinite-order classes detectable in finite-level cycle types. Exact finite verification prepared separately. The general inverse-limit conjugacy-tree realization remains unsupported, so no counterexample has been obtained.

## 2026-10-24 17:30 UTC — arbitrary ambient fusion defeated for unbounded abelian torsion (15%)

Derived the stronger power-coding lemma: any abelian torsion subgroup of unbounded exponent forces continuum ambient infinite-order classes, without normality or a preserved coordinate action. Recursively chosen powers E_i=lcm(i!,previous orders) and normal quotients encode a binary sequence; nested compact cosets supply points without assuming countable-base product convergence. Infinite supports force infinite order. Sent the exact proof to parent; the construction reviewer independently checked it line by line and found no gap. Parent assigned a second independent review. This is still a restricted structural obstruction, not a full resolution or a novelty claim.

The lemma excludes every profinite overgroup of a closed product of finite cyclic groups with unbounded orders, and also all profinite overgroups of the full rooted C_p wreath group or infinite unitriangular group, because these contain commuting finite-order elements of unbounded orders on disjoint blocks. The explicit unitriangular first-superdiagonal construction was also independently found by the parent. Corrected the coordinate-action discussion to discard trivial factors: their labels can have infinite permutation orbits while the induced base action remains trivial. This correction does not affect any nontrivial block-order conclusion.

Exact tree check completed: 170 finite permutations for p=2,3,5 and all binary supports up to the stated lengths; every cycle histogram agrees with the proof and distinct supports have distinct histograms. Independent reviewer is reproducing these computations with a separate implementation. Full problem remains unsolved; principal gap is a general pro-p/inverse-limit group without these commuting-torsion or finite-series mechanisms.

## 2026-10-24 17:32 UTC — independent construction audit complete (15%)

Both restricted theorem reviews pass. The supplemental independent tree implementation checked 1,396 support choices and 169,148 word images, including levels 0 and 1 and restriction compatibility. Its one minor objection, irrelevant trivial coordinate labels, was repaired explicitly. The finite-series consequence now explicitly requires all closed terms normal in the ambient group; finite-derived-length solvable groups provide such a series. Source provenance, authored proofs, exact code, independent reproductions and SHA-256 inventory are preserved. No counterexample, complete resolution, originality certification, publication recommendation or DOI. Parent is running a further independent check of the new power-coding lemma.
