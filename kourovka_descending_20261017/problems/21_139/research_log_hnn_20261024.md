# HNN finite-cover approach log, 2026-10-24

Scope: isolated mechanism study for Kourovka 21.139, particularly the all-virtual-H_2=0 free-by-cyclic remainder. No other approach files were read; only AGENTS.md and PROBLEM.md were read before independent work. Parent communications were used for cross-checks and explicit countercontrols. No Git, PR, queue, publication, or external communication was performed by this subagent.

## 2026-10-24T16:31:39Z — structural source checkpoint

Read the local policy/problem and checked primary arXiv:2510.10178v2, including its revision date, introduction, Theorem 4.1, and Corollary 1.5. The proposed both-associated-subgroups-free-factors structural input is real. No deduction that G is free or that it has finite-rank kernel is justified. Completion estimate toward the general HNN homology detection theorem: **5%**; this was a source/assumption audit.

## 2026-10-24T16:53:21.702982+00:00 — construction and validation checkpoint

Independently derived the finite-action telescoping construction for G_{p,k,epsilon}=<a,b,t | t^-1 a t=(ab^k)^p b^epsilon>, q=kp+epsilon. For q>=3, a local two-coordinate Fox kernel vector plus an unused sheet gives connected degree nq covers with b_2>=n. Found E=G_{2,2,+1}, for which every finite abelian cover has b_2=0, while explicit degree-5n covers have b_2=n. Proved the exact abelian-cover criterion gcd(q,k-1)=gcd(q,k+1)=1. Obtained a degree-five solvable monodromy certificate C5 semidirect C4, so nonsolvable monodromy is not necessary.

Generalized the unused-sheet construction to arbitrary edge rank as the sparse finite-action certificate lemma. This is conditional on a finite transitive base action killing both associated factors, a nonzero H_2 tuple, and a common zero in that tuple. It is not a proof that those certificates always exist. Parent's rank-two example A=<a,b>, B=<bc,ca> kills the whole base but has b_2=1 in its degree-two height cover, so killed-edge quotient triviality must not be treated as freeness.

Adversarial child independently verified signs, parity/boundaries, the telescoping formula, exact E kernel, gcd criterion, and sparse-certificate amplification. Parent identified a convention ambiguity between left Fox representation matrices and actual right covering permutations. Resolved it by using inverse right actions and adding direct relator-edge-walk equality checks, all passing. Parent's further finite p-group monodromy blindness argument for E was independently checked and included; it does not cover arbitrary prime-degree monodromy or all finite solvable covers.

Validation: exact rational chain ranks; d_1 d_2=0; direct cellular boundary equal to Fox-transpose boundary; exhaustive labeled transitive actions through degree four for G_{2,1,+1}; 24 generalized parameter/copy cases; exact E covers through degree 40; auxiliary all-120-stable-permutation enumeration at degree five; explicit rank-two degree-two certificate. Primary hyperbolicity gate checked against Kapovich arXiv:math/9704203 Proposition 4.11. Source files archived and hashed.

Strongest verified general result: sparse finite-action certificate implies unbounded virtual b_2, in arbitrary associated-subgroup rank. Strongest explicit diagnostic: E has zero H_2 in every finite abelian cover and every cover with finite p-group monodromy for any prime, yet connected degree-5n covers have b_2=n.

Exact remaining gap: no construction of such a finite certificate, or any positive finite-cover H_2 witness, for every nonfree hyperbolic free-factor HNN extension. A universal cyclic-sub-HNN reduction is blocked as an unsupported transfer of the central subgroup-existence difficulty. The known cyclic-edge subclass contains the explicit examples, so no new case of 21.139 or literature-wide novelty is claimed.

Completion estimate toward the general HNN detection theorem: **15%**. Construction/verification of the stated certificate mechanism and explicit family: **100%**. The general route remains incomplete, with the exact gap recorded rather than assumed.
