Scope: an authored mathematical partial result for the exact two-dimensional king-move Time-Bomb game. The unrestricted conjecture is not resolved. No novelty claim is made. Original contract SHA-256: 1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c.

## 1. A general hidden-block criterion

Choose strictly increasing integer times

1=S_1<S_2<S_3<...,

with S_j tending to infinity. Write L_j=S_(j+1)−S_j. The restricted Devil is required to satisfy:

If S_j≤n<S_(j+1), then every effective announcement (p_n,t_n) made in round n has t_n≥S_(j+2).

Past/current-time announcements are harmless and may also be permitted. Put

Q = sum_(j≥1) L_j / (2L_(j+1)+1)².

**Theorem 1.** If Q<1, the Angel has a deterministic infinite winning strategy against every adaptive Devil obeying this restriction.

### 1.1 Randomized legal motion

Set a_1=(0,0). For each block j, independently choose a random vector D_j uniformly from the integer square [−L_j,L_j]². Starting at time S_j, execute a fixed legal sequence of L_j king steps with total displacement D_j. For example, for each coordinate separately, move by its sign for the first |D_j^(coordinate)| steps, and then use zero increments for that coordinate. Combining the two coordinate increments gives legal king moves, including stays. Thus

a_(S_(j+1))=a_(S_j)+D_j.

The choices for future blocks are independent of all previously observed motion. They can be sampled when the block starts. The Devil sees every actual Angel move and can adapt every announcement to the entire observed history; it does not observe future random variables.

For probability bookkeeping, continue this hypothetical random path even after an eventual collision, and extend the Devil's rule after such a collision by any legal nonanticipating rule. Before the first collision this is precisely the legal play. This convention makes all future announced-pair hit events well-defined.

### 1.2 Conditional probability of one hit

Fix a round n with S_j≤n<S_(j+1), and define the effective hit event E_n={t_n>n and a_(t_n)=p_n}. Conditional on the entire observed history through the round-n Angel move and on the Devil's round-n choice, p_n and t_n are fixed. If t_n≤n, the conditional probability of E_n is zero; such an announcement cannot kill retroactively. In the rest of this paragraph assume t_n>n, so the lead restriction applies. The vector D_(j+1) is still independent and uniform: its block has not started at n. The lead restriction ensures that its whole block is completed by t_n.

Consequently the random location at the chosen detonation time has the form

a_(t_n)=D_(j+1)+Z,

where, conditional on that history and choice of t_n, Z is independent of D_(j+1). It contains any unrevealed part of the current block and all other complete or partial blocks contributing to a_(t_n). The Devil's later actions do not affect the hypothetical Angel path, which ignores announcements.

Convolution with a probability distribution cannot increase the largest point mass of a uniform distribution. Therefore

P[E_n | history and the round-n choice] ≤ 1/(2L_(j+1)+1)².

The same inequality holds unconditionally. It remains valid when the Devil chooses the position and time adaptively, since both are fixed by the conditioning. A randomized Devil can also be handled by conditioning on its independent random choices.

### 1.3 Positive survival probability and deterministic extraction

There are L_j announcement rounds n in the interval [S_j,S_(j+1)). The countable union bound gives

P[union_(n≥1) E_n] ≤ Q<1.

This union contains exactly the possible lethal collisions; ineffective current/past-time announcements are excluded.

Thus this randomized Angel survives forever with probability at least 1−Q, uniformly against every admissible adaptive Devil.

For completeness, this implies the asserted deterministic strategy without assuming that private randomness itself is the final strategy. If the initial state failed some finite-horizon winning predicate, finite perfect-information backward induction would give an admissible Devil strategy forcing loss by that horizon against every Angel move sequence, including every realization of the random path. That contradicts the strictly positive survival probability just proved. Hence every finite-horizon predicate holds. The compactness argument using nested nonempty subsets of the nine Angel moves now yields one deterministic infinite winning strategy. Absolute time is included in the state so that the announcement restriction is respected.

This reasoning does not commute an offline path-existence quantifier with an adaptive strategy quantifier. It directly bounds a randomized online policy against each adaptive Devil, then invokes exact game determinacy.
