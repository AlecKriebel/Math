# Independent adversarial audit: virtual obstruction family

2026-10-24 21:58 UTC. Reviewer: the homology-obstruction agent, whose own main investigation was frozen before receiving the parent arguments. **PASS for the stated partial filters and exact method barriers.** No Hydra virtual-specialness answer, originality endorsement, or publication recommendation follows. Completion of this bounded review:100%; progress toward the original negative discovery remains4%.

## Frozen scope

The nine files in `../FROZEN_INPUTS.json` and the two files in `../FROZEN_METRIC_DELTA.json` were hash-checked against their frozen bytes. The centralizer-coset lemma, bounded index exclusions, uniform passing models, the failure of the powered Engel shortcut, and the separate metric necessary condition are mathematically consistent. The centralizer-coset route is genuinely insufficient uniformly in rank; the argument does not pretend otherwise.

## Algebraic falsification attempts

1. The commutator convention is \([x,y]=x^{-1}y^{-1}xy\). For \(x=a_2u\), \(u\in C(t)\), the calculation \([x,t^q]=u^{-1}a_1^qu\) is exact; it is nonidentity because the free-fiber generator \(a_1\) has infinite order. It commutes with \(t^q\). Both conjugated elements really lie in the hypothetical subgroup after taking a positive power of \(t\). A nonabelian free group cannot contain such a pair: its maximal cyclic subgroups are malnormal, so a nontrivial commutator cannot belong to the centralizer of its second argument. Baudisch therefore applies to the two-generator subgroup. The right-coset fixed-point condition has the correct conjugation direction.
2. Containment of \(a_2\) in every abelian-quotient kernel for \(m\ge3\), and in the kernel of every nilpotent quotient of class less than \(m-1\), follows from \(a_2=[a_m,{}_{m-2}t]\). These are necessary conditions on particular covers, not virtual nonembedding conclusions.
3. If a finite commutator trajectory first reaches identity at depth \(\ell\), a presentation of rank \(m\) can satisfy its terminal relation and keep \(a_2\ne1\) only for \(m=\ell\) or \(\ell+1\). Nonidentity periodic trajectories never terminate. This proves the census covers all ranks at each tested degree; no unbounded-rank assumption is hidden.
4. In each terminating case \(a_1\) commutes with \(T\), so its subgroup with \(T\) consists exactly of the products \(a_1^kT^r\). The orbit-avoidance criterion for the whole coset is correct. The independent program uses explicit breadth-first group orbits rather than the author's union/find test.
5. The wreath model has \(a_1=1\), \(a_2\) equal to a global layer flip, and satisfies every Hydra relation. Its transitivity follows by shifting a coordinate supporting the nonzero top vector. The **full** centralizer test is justified, not just sampled: a fixed free-fiber word has abelian exponent vector in \(\ker(\theta_{ab}-I)=\mathbb Z a_1\), and all lower-generator images commute with \(a_1\) trivial. Hence the image of every centralizing word is a power of \(T\). A global flip followed by a coordinate shift has no fixed point, including the boundary case \(m=2,N=1\).
6. For \(p\ge2,q>0\), the reduced word \([a_2^p,t^q]\) starts with \(a_2^{-1}\), and its \(\theta^q\)-image starts with \(a_1^{-1}\). The initial block cannot cancel. Thus the second Engel commutator is nonidentity for all such powers. The \(p=1\) exception is correctly retained. No assertion that all powered pairs are free is made.

## Exact independent reproduction

`independent_negative_checks.py` imports none of the author's modules. It enumerates every top permutation and one shift permutation per cycle partition through degree8; the representative order is reversed relative to the author's partition routine. Direct orbit breadth-first search gives exactly the same permitted ranks **and exact counts**, with887040representative pairs at degree8. The full tables, including counts, are in `independent_negative_results.json`.

The same program reconstructs the uniform examples using integers as bit-polynomials and verifies all defining permutation relations, transitivity, full centralizer-image coset derangements, and the shift-module dimension for ranks2through129. The program's nilpotency-class field records the independently checked symbolic argument below; it is not an exhaustive lower-central-series computation.

`independent_power_check.py` checks625pairs \(1\le p,q\le25\), including the initial-letter mechanism and the \(p=1\) exception, and saves exact lengths. The written unbounded proofs carry the universal conclusions; finite checks are controls only.

## Other negative routes and primary-source scope

The proper semisimple CAT(0) centralizer/minset argument really rules out an infinite-order element central in a subgroup and also a nonzero power in that subgroup's commutator group. The signed displacement along the canonical axis factor is a homomorphism; commutation excludes axis reversal. The existing proper cocompact Hydra action therefore prevents this obstruction. No claim that arbitrary CAT(0) subgroups are special is imported.

Carr's actual Theorems1.2/1.4 and Corollary1.5 were reread in the cached primary PDF text. They give the required algebraic and metric statements for two-generator RAAG subgroups. Finite support handles an infinite defining graph. Baumslag–Mikhailov's actual Theorem1 and §5.2 identify the exact iterated-commutator Hydra family as residually torsion-free nilpotent. Reversing its indices matches the parent presentation. The claimed exclusion of residual-finiteness, torsion-free-nilpotence and basic orderability counterarguments is supported. These source checks do not establish priority for the parent's partial observations.

## Metric delta

The proof in `TWO_GENERATOR_DISTORTION_ROUTE.md` has the right inequality directions. For \(L=\langle u,v\rangle\le K\) one has \(|w|_L\lesssim|\iota(w)|_A\lesssim|w|_K\lesssim|w|_G\). It uses only the upper Lipschitz bound for the embedding \(K\to A\), and never assumes that embedding undistorted. Taking the normal core and the exponent of its finite quotient gives one \(N\) valid for all pairs; the pair-dependent constants are explicitly permitted.

The exact missing negative criterion is therefore correctly stated: at one fixed Hydra rank, every possible \(N\) would have to admit a distorted nonabelian subgroup generated by two \(N\)-th powers. The known distorted two-generator subgroup of \(G_2\), where virtual specialness is already announced, falsifies shortcut arguments from one distorted subgroup. No persistence under powers is supplied. The current Andrew–Bering–Kapovich–Vidussi primary TheoremA, CorollaryB and CorollaryF were read: free rank-two subgroups need not be undistorted by that theorem, and the fully irreducible corollary cannot be used for the triangular Hydra automorphism preserving proper free factors.

## Separately frozen nilpotent-quotient delta

The separately frozen `NILPOTENT_QUOTIENT_DELTA.md` was read and its hash verified against `FROZEN_NILPOTENT_DELTA.json`. Its wreath-image refinement is correct. In \(\mathbb F_2[\Delta]/(\Delta^N)\), the top vector generates the ideal \(\Delta^{N-(m-1)}\), of dimension \(m-1\). The permutation image is the semidirect product of that additive ideal with \(C_N\), of order \(2^{m-1}N\). Its lower central series from the second term is obtained by successive multiplication by \(\Delta\); the last nonzero term is the global-flip line in degree \(m-1\). Hence its nilpotency class is exactly \(m-1\), including the abelian rank2case. The normal kernel also passes the full centralizer-coset condition. Thus the class lower bound is sharp **for this necessary test**, with no implication that the kernel embeds in a RAAG.

## Disposition

No substantive objection remains in the reviewed claims. The meaningful output is a necessary finite-index filter, exact small-index exclusions, and a rigorous uniform countermodel to that filter as a complete negative strategy. The original Hydra question remains open in this research family. The homology companion is being reviewed by a separate fresh agent and is not certified by this parent-file audit.
