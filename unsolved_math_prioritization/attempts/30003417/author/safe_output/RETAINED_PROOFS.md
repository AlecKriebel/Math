# Retained mathematics, with explicit limits

These are supporting proofs, not a proof of either conjectured universal equality. The min–max results and their mechanisms are known: see Brendle, Brooke-Taylor, Friedman, and Montoya, *Cichoń's diagram for uncountable cardinals*, Proposition 30 and Corollary 31; and Brendle, *The higher Cichoń diagram in the degenerate case*, Theorem 1 and Corollaries 2–3. The exposition below is authored for this investigation. No priority or novelty is claimed.

## 1. Definitions and elementary bounds

Throughout let κ be a regular uncountable cardinal and assume 2^{<κ}=κ. Let X=2^κ, with basic neighborhoods [s]={x:s⊆x} for s∈2^{<κ}. A set is nowhere dense when each [s] contains a smaller basic neighborhood disjoint from it. Let M be the ideal of sets covered by at most κ nowhere dense sets. Replacing a nowhere dense set by its closure does not change this definition.

For a proper ideal I containing singletons, add(I) is the least size of a subfamily with union outside I; cov(I) is the least size of a subfamily covering its underlying space; non(I) is the least size of a set outside I; and cof(I) is the least size of an inclusion-cofinal subfamily of I. On κ^κ, f≤*g means {α:f(α)>g(α)} is bounded in κ. Define bκ and dκ as the least sizes of an unbounded and a dominating family, respectively.

**Lemma 1.1.** The union of fewer than κ nowhere dense sets is nowhere dense. The space X is not a union of κ nowhere dense sets. Consequently M is proper, is closed under unions of at most κ members, and κ^+≤add(M)≤cov(M).

**Proof.** Given δ<κ nowhere dense sets and a basic neighborhood, successively extend its stem to avoid their closures. At each limit stage below or equal to δ, the union of the earlier stems has length below κ by regularity. The resulting basic neighborhood misses every set. For a κ-long sequence of nowhere dense sets, perform the same recursion, also making the stem length at stage α at least α. Every intermediate stem has length below κ. The union at the end is a point of X missing all κ sets. Finally, a union of at most κ unions of at most κ nowhere dense sets is again such a union, since κ·κ=κ. ∎

**Lemma 1.2.** κ^+≤bκ≤dκ≤2^κ, and cof(M)≤2^κ.

**Proof.** If (f_i:i<κ) is a family of functions, define g(α)=sup{f_i(α)+1:i≤α}. The supremum is below κ by regularity, and g eventually strictly dominates every f_i. Thus no family of size at most κ is unbounded or dominating; for the latter, g itself defeats domination by the family. Every dominating family is unbounded: a bound h for such a family would contradict domination of h+1. All of κ^κ is dominating and |κ^κ|=2^κ.

There are κ basic neighborhoods. An open set is determined by the collection of basic neighborhoods it contains, so there are at most 2^κ closed sets. The unions of κ sequences of closed nowhere dense sets form a cofinal family in M of size at most (2^κ)^κ=2^κ. ∎

**Lemma 1.3.** For every proper ideal I containing singletons, non(I)≤cof(I).

**Proof.** Given an inclusion-cofinal family C⊆I, choose x_A outside A for each A∈C. The set Y={x_A:A∈C} cannot belong to I: otherwise Y⊆A₀ for some A₀∈C, contradicting x_{A₀}∉A₀. Thus non(I)≤|C|. ∎

The diagonal argument in Lemma 1.2 is also used below to bound any κ-sized family of functions. No inaccessible-cardinal hypothesis occurs in these lemmas.

## 2. Translation envelopes

Let Q⊆2^κ be the group of functions with bounded support, under coordinatewise addition modulo two, written ⊕. The assumption 2^{<κ}=κ gives |Q|=κ. Fix a bijection (q_β:β<κ) with Q. Every tail of this enumeration is dense: each basic neighborhood contains κ distinct members of Q and removing fewer than κ cannot empty it.

For x∈X and f∈κ^κ define

U_α(x,f)=⋃_{β≥α}[(x⊕q_β)↾f(β)],

E(x,f)=⋃_{α<κ}(X\U_α(x,f)).

Each U_α is open dense. Indeed, given [s], choose β≥α for which x⊕q_β extends s. The two initial segments s and (x⊕q_β)↾f(β) are comparable, so their basic neighborhoods intersect. Hence E(x,f) is κ-meager.

If F is closed nowhere dense and x∉F⊕Q, then x⊕q_β∉F for each β. By closedness choose h_{x,F}(β)<κ such that [(x⊕q_β)↾h_{x,F}(β)]∩F=∅. If h_{x,F}≤*f, then

F⊆E(x,f).                                                   (2.1)

To see this, fix a threshold α after which f(β)≥h_{x,F}(β). The corresponding cylinders for all β≥α miss F, so F⊆X\U_α(x,f).

**Proposition 2.1.** add(M)≥min{bκ,cov(M)}.

**Proof.** Let (B_i:i<μ)⊆M, with μ<min{bκ,cov(M)}. Each B_i is contained in a union of κ closed nowhere dense sets F_{i,j}. The translates B_i⊕Q remain meager, because Q has size κ. Since μ<cov(M), choose x outside ⋃_{i<μ}(B_i⊕Q), enlarging B_i to ⋃_j F_{i,j} first. There are μ·κ<bκ functions h_{x,F_{i,j}}. Choose one eventual upper bound f for all of them. Equation (2.1) puts every F_{i,j}, and hence ⋃_i B_i, inside E(x,f). ∎

**Proposition 2.2.** cof(M)≤max{dκ,non(M)}.

**Proof.** Fix a dominating family D⊆κ^κ of size dκ and a nonmeager set Z⊆X of size non(M). We show {E(x,f):x∈Z,f∈D} is cofinal in M. Given B∈M, enlarge it to ⋃_{j<κ}F_j, with F_j closed nowhere dense. Because B⊕Q is meager, choose x∈Z\(B⊕Q). Bound the κ functions h_{x,F_j} by a function h using Lemma 1.2, and take f∈D with h≤*f. Equation (2.1) gives B⊆E(x,f). The family has the stated size. ∎

**Exact obstruction.** Proposition 2.1 needs a point outside a union of μ translates of meager sets. Eventual boundedness supplies f only after such x has been chosen. Replacing the hypothesis μ<cov(M) by μ<bκ assumes the missing covering inequality. Likewise Proposition 2.2 retains a nonmeager parameter set Z; shrinking it to size dκ would require precisely the missing uniformity bound. Neither parameter can simply be omitted.

## 3. A tree comparison in the reverse direction

We give the λ=κ specialization of the known tree mechanism. All concatenations and lengths here are ordinal, and all stems have length below κ.

Fix the prefix-free family

{1} ∪ {σ_γ:γ<κ}, where σ_γ=0⌢1^γ⌢0.

The first member is reserved as an omitted extension. For g∈κ^κ, recursively build antichains C^g_α⊆2^{<κ}:

- C^g_0={∅}.
- For s∈C^g_α and γ<κ, put into C^g_{α+1} all extensions t of s⌢σ_γ of length lh(s⌢σ_γ)+g(γ)+1.
- At a nonzero limit δ<κ, use all unions of coherent chains (s_α:α<δ) with s_α∈C^g_α and s_α⊊s_β for α<β.

Regularity ensures all lengths remain below κ. Induction shows that each C^g_α is an antichain, every node on a later front extends a unique node on every earlier front, and every node has descendants on every later front. Let T_g be the downward closure of their union, and put N_g=[T_g].

**Lemma 3.1.** N_g is closed nowhere dense.

**Proof.** A tree body is closed, since a point outside it has a prefix outside the tree. Given any s∈T_g, choose t∈C^g_α extending s. The extension t⌢1 is incompatible with all descendants of t in C^g_{α+1}, which begin t⌢0. It is incompatible with all later nodes above t for the same reason; earlier compatible front nodes are prefixes of t. Therefore t⌢1 is outside T_g and its cylinder misses [T_g]. If s∉T_g, its cylinder already misses [T_g]. ∎

For each A∈M choose an increasing sequence (A_α:α<κ) of closed nowhere dense sets covering A. Such a sequence exists: take closures of unions of initial segments of a κ-sequence of nowhere dense sets and apply Lemma 1.1. Choose an extension h_A(t)⊇t with [h_A(t)]∩A_{lh(t)}=∅ for every t∈2^{<κ}. For each stem s define

f^A_s(γ)=lh(h_A(s⌢σ_γ)).

There are at most κ functions f^A_s, since |2^{<κ}|=κ.

**Lemma 3.2.** If g is not eventually bounded by any f^A_s, then N_g is not a subset of A.

**Proof.** Recursively choose t_α∈C^g_α, starting with the empty stem, so that [t_{α+1}] misses A_α. Given t_α, choose γ with g(γ)>f^A_{t_α}(γ). The child length prescribed in the construction exceeds lh(h_A(t_α⌢σ_γ)), so h_A(t_α⌢σ_γ) can be extended to a child t_{α+1} of that length. Because lh(t_α⌢σ_γ)≥α and A_ξ is increasing, this cylinder misses A_α. At a limit take the union of earlier stems. Lengths increase at every successor, hence x=⋃_{α<κ}t_α is a member of 2^κ, lies in [T_g], and misses every A_α. ∎

**Proposition 3.3.** add(M)≤bκ and dκ≤cof(M).

**Proof.** Let F⊆κ^κ be unbounded of size bκ. For any A∈M, the κ-sized family {f^A_s:s∈2^{<κ}} has an eventual bound h. Choose g∈F with g≰*h. Then g≰*f^A_s for every s, so N_g⊈A by Lemma 3.2. In particular ⋃_{g∈F}N_g cannot be meager, proving the additivity inequality.

For the cofinality inequality, suppose C⊆M has size μ<dκ. The union of all families {f^A_s:s∈2^{<κ}}, for A∈C, has cardinal at most μ·κ<dκ because dκ>κ. It is not dominating. Choose g not eventually bounded by any member of this union. Then N_g⊈A for each A∈C, so C was not cofinal. ∎

Combining Propositions 2.1–2.2 and 3.3 with add(M)≤cov(M) and Lemma 1.3 gives the known equalities

add(M)=min{bκ,cov(M)},     cof(M)=max{dκ,non(M)}.              (3.1)

These formulas do not assert add(M)=bκ or cof(M)=dκ.

## 4. Topology transfer and exact special cases

The use of literature written on κ^κ rather than 2^κ can be justified without assuming the entire two spaces are homeomorphic.

Let Y⊆2^κ consist of points whose coordinates equal to 1 form an unbounded subset of κ. Its complement is the union, over β<κ, of the closed nowhere dense sets of points identically zero on [β,κ). Thus Y is dense and X\Y is κ-meager. A homeomorphism from κ^κ onto Y is

f ↦ 0^{f(0)}⌢1⌢0^{f(1)}⌢1⌢···.

For each α<κ the concatenation of the first α blocks has length below κ by regularity; over κ blocks the length is κ. The inverse reads the ordinal lengths of the zero blocks between successive 1s. An unbounded subset of the regular cardinal κ has order type κ, so this inverse is defined on all of Y. Cylinders ending just after a block marker form a base in Y and are images of cylinders in κ^κ, proving continuity in both directions.

**Lemma 4.1.** If Y is dense in X and X\Y is κ-meager, the four κ-meager invariants agree for Y and X, provided these ideals are proper and contain singletons.

**Proof.** A nowhere dense subset of X has nowhere dense trace on Y. Conversely, if A⊆Y is nowhere dense in Y, its closure in X is nowhere dense in X: a nonempty open subset of that closure would, by density, give a nonempty relatively open subset of the closure of A in Y. Thus, for A⊆Y, meagerness in Y is equivalent to meagerness in X. Every B∈M_X is contained in (B∩Y)∪(X\Y), and the latter set belongs to M_X whenever B∩Y belongs to M_Y.

Trace and adjoining X\Y therefore transfer cofinal families in both directions. They transfer witnesses for nonadditive unions in both directions, since adding or removing a fixed meager set cannot change meagerness. Covers transfer by adjoining X\Y to one member; cardinalities are infinite. A nonmeager subset of Y is nonmeager in X, while for a nonmeager B⊆X the trace B∩Y is nonmeager and no larger. These observations give, respectively, equality of cof, add, cov, and non. ∎

On κ^κ, for g∈κ^κ the set B_g={f:f≤*g} is meager: write it as the union over α<κ of the closed sets satisfying f(β)≤g(β) for every β≥α. Each such closed set is nowhere dense by extending a stem at one fresh β with value g(β)+1. Hence a family of size below bκ is meager, and a dominating family yields a meager cover. Transfer by Lemma 4.1 gives

bκ≤non(M),     cov(M)≤dκ.                                  (4.1)

**Corollary 4.2.** In the target regime:

1. add(M)=bκ if and only if bκ≤cov(M).
2. cof(M)=dκ if and only if non(M)≤dκ.
3. If bκ=κ^+, the first equality holds.
4. If dκ=2^κ, the second equality holds.
5. If 2^κ=κ^+, both hold, and all six invariants in (3.1) and (4.1) equal κ^+.

**Proof.** The first two assertions are immediate from (3.1). The last three follow from Lemmas 1.1–1.2, Proposition 3.3, and the bound cof(M)≤2^κ. ∎

For comparison with sources that assume κ^{<κ}=κ, this is equivalent here to 2^{<κ}=κ. The nontrivial direction follows because every function μ→κ for μ<κ has bounded range; for each λ<κ choose ν<κ with λ≤2^ν and bound λ^μ by 2^{ν·μ}≤κ. Taking the union over λ<κ proves κ^μ≤κ.

**Limits.** These proofs do not identify topologically meager sets with every combinatorial notion called meager. In particular, a chopped-function or eventual-difference characterization from the inaccessible case must not be inserted at a successor cardinal without proof. The topology transfer above concerns the topological ideals only.

## 5. A precise failure of an automatic limit argument

One tempting forcing approach assumes that an increasing union of <κ-complete filters is still <κ-complete. That implication is false, even for uniform filters extending the co-small filter.

**Proposition 5.1.** For any regular uncountable κ, there is an increasing sequence (F_n:n<ω) of proper uniform <κ-complete filters on κ whose union is not countably complete.

**Proof.** Partition κ into disjoint sets (P_n:n<ω), each of size κ. Let A_n=⋃_{m≥n}P_m, and set

F_n={B⊆κ: |A_n\B|<κ}.

Each F_n is proper, upward closed, and closed under intersections of fewer than κ members: the complement inside A_n of such an intersection is a union of fewer than κ sets of size below κ, which still has size below κ by regularity. Every member has size κ, and every set with complement of size below κ lies in F_n. Because A_{n+1}⊆A_n, F_n⊆F_{n+1}. Thus F=⋃_n F_n is a proper filter. It contains every A_n, but ⋂_n A_n=∅, so it is not countably complete. ∎

This does not refute a carefully designed forcing preservation theorem or the target conjecture. It pinpoints why completeness at all earlier stages, by itself, does not discharge a limit-stage obligation. No iteration separating cov(M) from bκ, or non(M) from dκ, has been constructed in this investigation.

## Final boundary

The retained proofs give known machinery and special cases, plus elementary warnings about invalid transfers. The exact unresolved inequalities are bκ≤cov(Mκ) and non(Mκ)≤dκ under regular uncountable κ and 2^{<κ}=κ. No universal proof and no countermodel for either has been obtained here.
