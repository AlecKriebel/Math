# Spatial and informational finitary coding: scope correction and partial results

Problem 30005026 / OWR-9790359-007, rank 788. Checked 5 October 2026.

**Status:** the genuine finite-valued problem is unresolved by this work. The unrestricted-target wording in the catalog is false. The counterexample below concerns that wording defect only. These are AI-assisted, unrefereed notes, with no novelty claim and no independent audit yet.

## 1. Recovered target and quantifiers

For each integer d >= 1, let X be a stationary process on Z^d with a **finite** output alphabet. Suppose some IID source U admits a translation-equivariant finitary map to X whose radius R satisfies P(R > r) <= C exp(-c r), for some C,c > 0 and every integer r >= 0. The question asks whether, for **every epsilon > 0**, there is a **finite-alphabet IID** source Y and a finitary translation-equivariant map Y -> X such that

- h(X) <= H(Y_0) <= h(X) + epsilon;
- its radius R_epsilon has P(R_epsilon > r) <= C_epsilon exp(-c_epsilon r).

The source alphabet, its law, the map, and the positive constants may depend on epsilon. No common alphabet bound or uniform tail constants are requested. h(X) is entropy **per site**, not necessarily H(X_0). Use cubes B_r = [-r,r]^d; replacing this by another lattice norm does not change exponential-tail existence. The original source U need not be finite-valued. The lower entropy inequality is the usual entropy monotonicity under factors.

Sources: Spinka's contribution to Oberwolfach Report 8/2022, printed pp.447 and 449, and Meyerovitch--Spinka, arXiv:2201.06542v1, Question 8.3, printed p.35. The latter states the finite-output hypothesis explicitly. The workshop was held 13--19 February 2022; the report issue was published in 2023. A catalog citation calling the workshop itself a 2023 event conflates these dates. The short catalog statement omits the finite-output restriction and the Z^d setting. No alteration of the source dataset is made here.

## 2. Finite-source cardinality obstruction

### Proposition 1 (marginal support bound)

Let a process X be a finitary factor of any process Y taking values in a finite alphabet of size b. IID is not needed for this proposition. Let R be the minimal essential coding radius at zero. Write p for the law of X_0 and

T_p(M) = 1 - sup{p(S): S is a set of at most M output symbols}.

Then for every integer r >= 0,

P(R > r) >= T_p(b^((2r+1)^d)).

**Proof.** There are at most b^((2r+1)^d) source words in B_r. Each positive-probability word that determines X_0 can determine only one value. Let S_r be the collection of all values determined by such words. Outside a null set, {R <= r} implies X_0 belongs to S_r. Thus p(S_r) >= P(R <= r), and |S_r| has the displayed upper bound. Taking complements proves the result. This argument also applies when the map is defined on a shift-invariant full-measure domain. It does not assume that the event {R <= r} is independent of any source coordinate. QED.

### Proposition 2 (finite-entropy countable IID counterexample)

Use the countable alphabet A = {(k,j): k >= 1, 1 <= j <= 2^k}. Give each symbol the probability

p(k,j) = 4 / [k(k+1)(k+2) 2^k].

Let X be IID with this marginal on Z^d. Then H(X_0) <= 4 bits, X is a radius-zero factor of an IID process, and no finite-alphabet source can code X with exponentially decaying radius tails. More precisely, every finite-alphabet coding with source alphabet size b obeys

P(R > r) >= 1/[K_r(K_r+1)],
K_r = ceil((2r+1)^d log_2 b) + 1.

For b >= 2 this also implies E[R^(2d)] = infinity.

**Proof.** The total mass of group k is w_k = 4/[k(k+1)(k+2)]. The telescoping identity

w_k = 2/[k(k+1)] - 2/[(k+1)(k+2)]

shows that the weights sum to one and that sum_{k >= K} w_k = 2/[K(K+1)]. Furthermore,

sum_{k >= 1} k w_k = sum_{k >= 1} 4/[(k+1)(k+2)] = 2.

H(K) is finite, since its summand is O(log(k)/k^3). Comparing w_k to the geometric probabilities 2^(-k), the nonnegativity of relative entropy gives H(K) <= E[K] = 2. Conditional on group K=k, j is uniform on 2^k symbols. Hence H(X_0) = H(K) + E[K] <= 4.

Now let S contain at most M symbols and put K = ceil(log_2 M)+1. For every k >= K, the group has 2^k >= 2M symbols, at least half of which are outside S. Therefore

p(A minus S) >= (1/2) sum_{k >= K} w_k = 1/[K(K+1)].

Apply Proposition 1 with M=b^((2r+1)^d). For b >= 2, K_r is bounded above by a constant times (r+1)^d, so the resulting polynomial lower bound is incompatible with any exponential upper bound. It also forces the 2d-th moment to diverge by the tail-sum formula. When b=1 the lower bound stays positive, excluding finitariness itself. Finally X is the identity factor of the countable-alphabet IID source X, with R=0. QED.

**Scope:** this disproves the unrestricted-target catalog wording even after adding finite entropy. It is not a counterexample to the finite-valued question in Section 1. It does not contradict qualitative entropy-efficient finitary coding: that theorem supplies no exponential-radius bound for countable targets.

## 3. Composition preserves exponential tails, but does not reduce entropy

### Proposition 3 (composition bound)

Suppose U -> Z -> X are stationary equivariant finitary maps. Let S_v be the radius for producing Z_v from U, and T_0 the radius for producing X_0 from Z. If

P(S_0 > r) <= C_1 exp(-c_1 r),
P(T_0 > r) <= C_2 exp(-c_2 r),

then the composite map has exponential tails. No independence between S and T is required.

**Proof.** An admissible radius of the composite is

R <= T_0 + max{S_v : v in B_{T_0}}.

If T_0 <= r and all S_v <= r for v in B_r, the U coordinates needed to determine every queried Z coordinate lie in B_{2r}. Thus the union bound and stationarity yield

P(R > 2r) <= C_2 exp(-c_2 r) + (2r+1)^d C_1 exp(-c_1 r).

A fixed polynomial times an exponential is bounded by a slower exponential. For odd radii use monotonicity and floor(n/2); finitely many small radii are absorbed into the constant. QED.

This closes the geometric step in a possible two-stage construction. It does not supply the missing near-entropy source. In particular, to simulate an existing finite IID source Z from another source U requires H(U_0) >= H(Z_0). If H(Z_0)-h(X) is positive, simulating Z cannot remove that entropy overhead. The qualitative Meyerovitch--Spinka theorem constructs a new coding of X; it does not assert the tail estimates needed to apply Proposition 3. If the existing source has infinite entropy, reproducing that source from a finite-valued IID source is impossible by entropy monotonicity.

## 4. Known positive subclass: finite-state mixing Markov chains

Harvey--Holroyd--Peres--Romik, *Universal finitary codes with exponential tails*, Theorem 2, proves that one finite-state irreducible aperiodic stationary Markov chain finitarily factors onto another with exponential tails whenever the source entropy rate is strictly larger. This is a literature theorem, not a new result of this investigation.

### Corollary 4

The question in Section 1 has an affirmative answer for finite-state irreducible aperiodic stationary Markov chains on Z. It also holds on Z^d for independent copies of such a chain on all lines parallel to the first coordinate axis.

**Proof.** Let h be the chain's entropy rate and epsilon>0. Choose a finite probability vector p of full support with h < H(p) < h+epsilon. Such a vector exists: choose m with log_2 m > h+epsilon, and continuously interpolate between a point mass and the uniform law on m symbols. At positive, nonterminal interpolation parameters the law has full support, and the intermediate value theorem gives an entropy in the desired interval. The IID process with marginal p is itself an irreducible aperiodic Markov chain. Apply the cited theorem.

For the Z^d statement, apply the same one-dimensional map independently on every first-coordinate line. Translating along a line commutes with the one-dimensional map, and translating transversely just permutes the lines. The map is therefore fully Z^d-equivariant. Its radius has the same law as in dimension one. Independence of source lines gives independent target lines. Entropy of a length-n block in the chain divided by n tends to h, so the entropy per site of their independent product field is also h. QED.

This does not cover an arbitrary finite-valued exponential-tail finitary factor, a general hidden Markov factor with entropy loss, or interacting multidimensional Markov random fields. Periodicity is excluded in the cited Markov theorem.

## 5. Why a random periodic block origin is unavailable

### Proposition 5 (no equivariant global grid phase)

For L>=2 there is no measurable factor of an IID Z^d process taking values in (Z/LZ)^d that transforms under each translation v by adding v modulo L.

**Proof.** Each event specifying a particular phase would be invariant under every shift in L Z^d. An IID field, grouped into the L^d cosets, is again a Bernoulli field under this sublattice action, which is ergodic. Consequently the phase must be constant almost surely. Equivariance under a unit-coordinate shift then requires a constant to equal itself plus that unit vector modulo L, which is impossible. QED.

The result rules out a specific shortcut: take entropy-efficient blocks on a fixed periodic tiling and obtain full translation-equivariance by choosing an IID-derived global phase. An externally supplied uniform phase changes the source to a non-IID source. Nonperiodic finitary marker partitions are not ruled out. To finish a block-compression approach one must preserve the exact joint target law, allocate random bits at entropy h(X)+epsilon per site, and control all marker, supply-deficit, and decoding radii exponentially. A block entropy estimate by itself provides none of these three conclusions.

## 6. Uniform tails at vanishing entropy gap are a stronger, generally false demand

### Proposition 6 (compactness with fixed alphabets and common tail constants)

Fix finite alphabets A and B. Let p_n be source laws on A, converging to p. Suppose equivariant finitary maps phi_n send p_n-IID fields to the **same** B-valued target law nu, and their essential coding radii satisfy

P_{p_n}(R_n > r) <= C exp(-c r)

with C,c>0 independent of n. Then p-IID admits an equivariant finitary factor to nu with the same bound. In particular, if H(p_n) -> h(nu), its limiting source has exactly that entropy.

**Proof.** For each r and each word w on B_r, record either the output symbol forced almost surely by that cylinder under phi_n, or a special symbol star if the cylinder has probability zero or does not force the output. There are only finitely many possibilities at each radius. A diagonal subsequence makes all these records eventually constant, simultaneously for every finite-radius word.

Restrict attention to words over the support A_+ of p. Each such cylinder has positive p probability and eventually positive p_n probability. A non-star limiting record is compatible with every larger-radius extension having a non-star record: the corresponding cylinder inclusions have positive measure for all sufficiently large n, where both records agree with phi_n. Indeed, if an inner cylinder has a non-star record, every positive-measure extension also has that record. These facts pass to the limit.

Define the limit output at zero from the first non-star record encountered, and use translated records at other sites. The probability, under p, that no record decides the origin by radius r is the limit of the analogous probabilities under p_n: it is a finite sum of cylinder probabilities, and the records have stabilized. Cylinders involving symbols outside A_+ have limiting probability zero. This undecided probability is at most C exp(-c r). Consequently all sites are decided on a translation-invariant full-measure domain. Compatibility makes this an equivariant finitary map with the claimed tail bound.

It remains to identify its law. Fix a finite set F of output sites and a radius r. Replace any undecided output at that radius by a fixed default symbol. The resulting vector is a function of finitely many input coordinates. Its law for p_n converges to its law for p, since the records stabilize and cylinder probabilities converge. Its difference from the true vector has probability at most |F| C exp(-c r) in both the n-th and limiting constructions. First let n tend to infinity, then let r tend to infinity. The limiting vector thus has law nu restricted to F. This holds for every finite F. Finally H is continuous on the finite-dimensional probability simplex, giving the entropy assertion. QED.

For a concrete boundary case, let the target be fair binary IID. Let p(t)=(t,(1-t)/2,(1-t)/2), and choose the unique t_* in (1/3,1) for which H(p(t_*))=1 bit. Entropy decreases strictly from log_2 3 to zero on this interval. Choose t_n approaching t_* from below, so H(p(t_n))>1 and decreases to 1. The Harvey--Holroyd--Peres--Romik theorem supplies exponential-tail codes from each of these three-symbol sources to fair binary IID. But their constants cannot have both a uniform upper bound on C_n and a positive uniform lower bound on c_n: Proposition 6 would produce an equal-entropy exponential code from p(t_*) to fair binary IID. Gabor's arXiv:2509.06018v1, Theorem 1.2, excludes that, since these positive marginal laws are not symbol permutations. This last exclusion is a cited 2025 preprint theorem, not independently reproved here.

This boundary case concerns a prescribed source family. It does not contradict the original existential problem: sources and tail constants there can vary without uniform restrictions, and the fair binary target itself is already an admissible source.

## 7. Exact remaining gap and stopping point

No argument here constructs the required near-entropy finite IID source with exponential tails for a general finite-valued exponential-tail IID factor. No counterexample in that genuine class is provided. Five approach families were explored and stopped at the gaps above; further independent checking may validate these partials but should not be counted as a sixth search attempt. The general target stays unresolved. The unrestricted catalog formulation should not be labeled a solution of the report's problem.

The exact finite calculations in verify.py check identities and examples used above. They are supplementary controls, not a proof of the infinite-process assertions. The written arguments and the explicitly identified literature theorems carry those assertions.
