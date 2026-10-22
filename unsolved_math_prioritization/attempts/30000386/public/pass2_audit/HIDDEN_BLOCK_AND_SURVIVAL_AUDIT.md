# Independent audit: delayed announcements and scoped policy obstructions

Shared PASS2 mathematical audit. Exact accepted input versions are recorded in `HIDDEN_BLOCK_ACCEPTANCE_MANIFEST.json`. No unrestricted Time-Bomb solution is asserted.

## Decision and necessary event convention

The hidden-block criterion, its cubic and explicit logarithmic delay families, and the report's three additional scoped lemmas are valid with the following essential hit-event convention:

E_n = {t_n>n and a_(t_n)=p_n}.

Only an announcement made strictly before its detonation can cause a loss. Ineffective past/current-time announcements have event E_n empty. A statement bounding the probability that any announced pair is ever visited, without this restriction, would be false: Devil could announce (a_n,n) after observing the move. The accepted version must use the effective events above and extend hypothetical post-death Devil behavior legally and nonanticipatingly. This correction does not change the survival theorem or any numerical bound.

## 1. Legal randomized trajectory

Let 1=S_1<S_2<… tend to infinity and let L_j=S_(j+1)−S_j. The first move a_1=0 is legal and cannot hit a previous bomb. For each j, choose an independent uniform D_j in the integer square [−L_j,L_j]². In each coordinate, use its sign for |D_j| initial steps of the block and then zero. Combining the coordinates gives legal king moves and endpoint displacement exactly D_j after L_j moves.

The displacement may be sampled at block start. Its later partial revelation through the path is harmless: the probability argument always uses the next block, which has not begun. The randomized policy's hypothetical trajectory ignores bomb announcements. This is important for the conditional-independence proof and would need reconsideration if another response policy were mixed into the path.

For bookkeeping, continue this trajectory after a hypothetical first loss and extend Devil by an arbitrary legal nonanticipating rule. Every actual loss occurs along this same trajectory before any extension matters. All countably many effective hit events are then well-defined on one probability space.

## 2. Filtration and target-dependent times

Fix an announcement round n in block j. Condition on the complete observed history through the Angel move and the Devil's current choice (p_n,t_n). If the announcement is ineffective, its event has conditional probability zero. Otherwise its permitted lead satisfies t_n≥S_(j+2).

The future D_(j+1) is independent and uniform even after this conditioning. Neither the observed history nor the Devil's nonanticipating current choice depends on it. The block j+1 is completed by the now-fixed target time t_n. The endpoint therefore decomposes as

a_(t_n)=D_(j+1)+Z,

where Z is conditionally independent of D_(j+1). It includes the remaining part of the current block, the starting location, every other completed block, and any final partial block. Fixing the target time is essential: the block contributing to that final partial displacement is then fixed by the conditioning. Later Devil announcements do not affect the chosen hypothetical trajectory.

Thus the conditional and unconditional probabilities of E_n are at most 1/(2L_(j+1)+1)². Private random choices by Devil can be conditioned on as well, provided they are independent of unrevealed Angel randomness. No clairvoyant access to future private random variables is assumed.

## 3. Union bound and deterministic extraction

There are exactly L_j announcement rounds in [S_j,S_(j+1)). The countable union bound gives

P(union of all E_n) ≤ Q = sum_j L_j/(2L_(j+1)+1)².

If Q<1, the randomized online policy survives forever with probability at least 1−Q against every admissible adaptive Devil. Independence between different hit events is neither claimed nor required.

For deterministic extraction, include absolute time in the state, since the legal announcement domain depends on the round. Every fixed-horizon restricted game has the exact finite-cone reduction and backward-induction dichotomy. A losing horizon would give one admissible Devil strategy that defeats every sequence of legal Angel choices by that horizon. It would therefore defeat every realization of the randomized trajectory, contradicting its positive survival probability against that very strategy.

Every finite horizon is consequently winning. Nested nonempty subsets of the nine Angel moves then yield one deterministic infinite winning strategy by the accepted compactness proof. This does not select a path after seeing a completed schedule. The randomness is a proof device, and no algorithm for computing the extracted deterministic strategy is supplied.

## 4. Cubic blocks

For S_j=j³, L_j=3j²+3j+1 and L_(j+1)>L_j≥3j². Hence

L_j/(2L_(j+1)+1)² < 1/(4L_j) ≤ 1/(12j²).

Using the elementary bound sum_(j≥1)1/j²≤2 gives Q<1/6 and survival probability greater than 5/6 for the randomized proof device.

For j³≤n<(j+1)³,

(j+2)³−n ≤ 6j²+12j+8 ≤ 26j² ≤ 26n^(2/3).

The middle inequality is equivalent to 4(5j+2)(j−1)≥0. Thus the stated integer lead ceil(26n^(2/3)) implies the exact hidden-block rule, including j=1.

## 5. Explicit logarithmic lead

Let b(j)=1+floor(log₂j), L_j=j b(j)², S_1=1 and S_(j+1)=S_j+L_j. The lengths are positive and nondecreasing. The dyadic group 2^k≤j<2^(k+1) contributes at most 1/(k+1)² to sum 1/L_j. Therefore Q<(1/4)sum 1/L_j≤1/2.

The exact sufficient lead is g(n)=S_(j+2)−n in block j. The all-n upper bound

g(n)≤21√n(1+log₂n)

is correct. For j≥2, the floor(j/2) terms ceil(j/2)≤i<j satisfy i≥ceil(j/2) and b(i)≥b(j)−1≥b(j)/2. Since floor(j/2)ceil(j/2)≥j²/5,

n≥S_j≥j²b(j)²/20.

Also j+1≤3j/2 and b(j+1)≤3b(j)/2, so L_(j+1)≤27L_j/8. Thus

g(n)≤35L_j/8≤(9/2)j b(j)²

≤(9/2)√(20n)b(j)<21√n(1+log₂n),

using S_j≥j. Block j=1 consists only of n=1; its exact g(1)=9 is below 21. This establishes the ceiling version as a simple explicit sufficient lead for every positive integer round. It is a genuine restriction on the original Devil, not coverage of arbitrary short-lead bombs.

## 6. Fixed-size earliest raw-deadline memory

The report's deterministic-policy obstruction is accepted under its explicit history-equivalence definition, which forbids retaining hidden summaries of discarded deadline data.

For k retained deadlines, set M=(2k+1)² and T=2k+M+1. The k decoys at T−k,…,T−1 are installed in rounds 1,…,k. They remain all pending through the Angel move at T−k under the stated t≥n convention. Hence time-T targets remain excluded from every retained-history projection through that move.

The policy's position a_* there is therefore predictable independently of those target positions, unless a decoy has already killed it. Announcing every time-T target in a_*+[−k,k]² during rounds k+1,…,k+M is legal and finishes at T−k−1, before the position used for the trap. The apparent prediction is not circular because all these targets are hidden by the specified policy restriction. When they become visible, only k moves remain; every possible endpoint is already bombed.

This defeats that deterministic raw-deadline sensitivity class. It does not cover a policy that filters spatially irrelevant targets first, retains additional summaries, or uses unrestricted randomized information.

## 7. Exact nonlinear two-move predecessor

For terminal bomb set B and two moves remaining, after a first move to q Devil can fill all nine terminal neighbors with one announcement exactly when at least eight are already in B. Thus the exact losing set is

L_2(B)=E(A_8(B)),

with A_8(B)={q:|N(q)∩B|≥8} and E(C)={a:N(a)⊆C}. Both the observed first move and the adaptive response are represented.

For the report's periodic truncation B_m, the count is exactly 8m². Every full interior 3-by-3 neighborhood has exactly one omitted residue-(0,0) cell and eight bombs, yielding the stated lower bound |L_2(B_m)|≥(3m−4)². Its ratio to 8m² tends to 9/8 and exceeds one for sufficiently large m.

In fact boundary or exterior centers see at most six supported cells, so A_8 and L_2 equal the respective interior squares; this stronger observation is unnecessary for the reported lower-bound obstruction. No claim that such a preloaded state is forceable from the original empty board is made.

## 8. Moving-room transport primitive

For a 2-by-2 room translated by one cardinal unit, every point in the old room can reach at least two points in the new room in one king move. If unchanged, all four are reachable. With at most one already announced bomb at the arrival time inside the new room, at least one reachable point is safe. The update after that move cannot retroactively kill it.

The stated cardinal-motion and Manhattan-time limitations are necessary to this proof: a diagonal room translation can leave a corner only one reachable destination. The lemma supplies no terminal hazard guarantee against a stockpile targeting every point of a small final room. Its reported scope is correct.

## Remaining gap

The delayed-announcement theorem handles arbitrarily many mixed adaptive timestamps only under the specified minimum lead. The proof does not combine unrestricted short-lead responses with the hidden-block independence. The policy obstructions and nonlinear density example likewise do not supply a full-game Devil win. All conclusions remain partial.
