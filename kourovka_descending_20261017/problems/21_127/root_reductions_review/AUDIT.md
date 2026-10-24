# Fresh independent review of root reductions and the commutator test family

Completed 2026-10-24, 20:47 UTC. Assigned audit completion estimate:100%. Full problem21.127 remains unresolved.

**Verdict: PASS after one finite-graph scope clarification, now applied.** These are credited known-result deductions and exact controls, not a novel solution or a publication-ready resolution.

## Scope and primary sources inspected

Reviewed current `root_reductions/FINITE_SUPPORT_AND_JOINS.md`, `COMMUTATOR_TEST_FAMILY.md`, `graph_subclass.py`, and `graph_subclass.json`. Independently read the actual cached [Calegari, *Scl, sails and surgery*, arXiv0907.3541v3](https://arxiv.org/pdf/0907.3541v3), Rationality Theorem and Theorem3.14 (PDF p.12), and [Heuer, *Gaps in scl for Amalgamated Free Products and RAAGs*, arXiv1802.01107v3](https://arxiv.org/pdf/1802.01107v3), §7 and Theorem7.3 (PDF p.30). Source and reviewed input hashes are frozen in REVIEW_MANIFEST.json.

Calegari's actual theorem covers a **finite free product of finitely generated free abelian groups**, with rational piecewise linear scl on the homogeneous boundary-chain space. It therefore applies to every eligible individual element in the graph subclass described. No general free-product closure theorem for arbitrary PQL groups is asserted or used.

Heuer's actual §7 assumes a **finite simplicial graph**. Its Theorem7.3 applies to every **nonidentity element of the commutator subgroup**, with scl≥1/2. The support/retraction argument below correctly extends this application to the arbitrary defining-graph convention. No special-generator assumption is hidden in the gap theorem.

## 1. Finite supports and induced retracts

For a finite vertex set S, sending every generator outside S to1 respects every commuting relator. The induced-subgraph inclusion is split by this homomorphism, so it is injective. If g belongs to the ambient commutator subgroup and is represented using S, its retraction is the same element g and lies in the smaller commutator subgroup. Thus this reduction does not lose an ambient commutator expression merely because its individual factors used outside vertices.

Commutator length is nonincreasing under any homomorphism. Inclusion and retraction give the two opposite inequalities for every g^n, hence equality for every n and equality of scl. This works even when the ambient vertex set is infinite or uncountable: the individual word and any commutator expression are finite. The empty support and abelian cases contain only the identity in the derived subgroup and have scl0.

## 2. Direct products, joins, and the scope repair

For finitely many factors, projection gives cl((g_i))≥max_i cl(g_i). Conversely, pad optimal expressions by identity commutators and take componentwise handles. This gives equality, including the zero maximum case. Applying it to every power and taking a finite maximum of convergent sequences yields scl((g_i))=max_i scl(g_i).

After the finite-support reduction, Γ is finite. Complement components are joined to each other by every possible original edge, giving the claimed finite direct-product decomposition. If the maximum of finitely many scl values is irrational, one of the factors attains precisely that irrational maximum. Its induced subgroup is a retract, so it is a valid smaller ambient RAAG for the hypothetical counterexample. This proves the complement-connected reduction.

**Reported scope issue and accepted repair:** before repair the join paragraph did not explicitly restrict Γ to be finite. For a graph with infinitely many complement components the RAAG is the restricted direct product, not generally the unrestricted direct product. The author has now added “After the finite-support reduction, take Γ finite.” This is sufficient because every use in the proof is on the finite support. I inspected the repaired text; no infinite-product isomorphism is now required. Its current hash is in REVIEW_MANIFEST.json.

The rationality subclass follows by identifying a disjoint union of finite cliques with a finite free product of finite-rank free abelian groups, applying Calegari, and then taking finite direct products via the exact maximum formula. This does not silently upgrade to all cographs or arbitrary free products of already-PQL factors.

## 3. Independent graph census

The new standard-library `independent_census_and_covers.py` uses a different membership mechanism: it enumerates all set partitions as possible join factors, checks all cross edges, and checks that no factor has an induced three-vertex path. A graph is a cluster graph exactly when it has no such path, so this recognizes precisely the claimed subclass without computing complement components.

It independently computes isomorphism orbits by breadth-first application of adjacent label transpositions, rather than canonicalization over all permutations. All counts agree:

|Vertices|Labelled graphs|Labelled inside|Isomorphism classes|Classes inside|
|---:|---:|---:|---:|---:|
|1|1|1|1|1|
|2|2|2|2|2|
|3|8|8|4|4|
|4|64|40|11|9|
|5|1024|227|34|17|

The two excluded four-vertex classes have degree sequences (1,1,2,2) and (0,1,1,2), namely P4 and P3 plus an isolated vertex. Their exclusion is from this reduction only; it is not a claim that published rationality results exclude them. The n=0 trivial graph is not in the census, and is handled separately by scl0.

## 4. Odd surface covers and the universal upper bound

For every odd positive N, multiplication by2 is a permutation of Z/N. With σ(x)=x+1 and τ(x)=2x and the convention [σ,τ]=σ τ σ^(−1) τ^(−1), direct substitution gives [σ,τ](x)=x−1. It is one N-cycle. This includes N=1: all maps are the identity on one point, and that identity has one boundary cycle of length1.

Sending the first handle generators to σ and τ and the others to1 gives a transitive monodromy representation because σ alone acts transitively. The resulting connected degree-N cover of the once-punctured genus-k surface has a single boundary component of degreeN and Euler characteristic N(1−2k). Since a one-boundary orientable surface has χ=1−2h, its genus is h=(1+N(2k−1))/2, an integer for oddN. Its boundary maps to g^N up to conjugation and orientation, both harmless for commutator length. Thus cl(g^N)≤N(k−1/2)+1/2. Dividing along odd N and using the existing subadditive scl limit proves scl(g)≤k−1/2.

The independent program checks the exact permutations, single boundary cycle, and genus identities for all odd N≤255 and 1≤k≤8. The proof above, not this bounded computation, establishes all odd degrees. No claim is made that τ works for evenN; even powers are treated separately.

## 5. Consequences of the credited RAAG gap

For any nonidentity single commutator c=[u,v] in a RAAG, the universal upper bound is1/2 and Heuer's lower bound is1/2. Hence scl(c)=1/2 for arbitrary u,v. The identity has scl0 and is excluded from subsequent positive-length arguments.

If c=h^m with |m|>1, the torsion-free abelianization of a RAAG forces h into its commutator subgroup: m[h]=0 implies [h]=0. Since c≠1, h≠1. Homogeneity and the gap give 1/2=scl(c)=|m|scl(h)≥|m|/2, a contradiction. This argument is valid for infinite defining graphs as their abelianization is a free abelian direct sum and the gap passes through the finite-support reduction.

For N≥1 and k=cl(c^N), the element c^N is nonidentity (its scl isN/2), so k≥1 and the genus bound applies to an optimal expression. It yields N/2≤k−1/2 and therefore k≥floor(N/2)+1. The odd cover has exactly that genus when N is odd. When N is even, c^N=c^(N−1)c gives cl(c^N)≤cl(c^(N−1))+1=N/2+1, matching the lower bound. In particular N=1 gives1 and N=2 gives2. Conjugation and negative exponents preserve these length/norm statements with absolute exponents where appropriate.

The deductions do not give a half-integer scl spectrum for arbitrary RAAG words or a uniform bound on commutator length. An irrational candidate may lie outside conjugates of powers of a single commutator, but products of two or more commutators remain largely unrestricted by this test.

## Final assessment

No substantive objection remains after the explicit finite-graph clarification. The computations independently reproduce the exact finite claims. The established source theorems have the required hypotheses and are properly credited. These results supply useful reductions and controls, while the arbitrary-word rationality question remains fully open in the recorded research.
