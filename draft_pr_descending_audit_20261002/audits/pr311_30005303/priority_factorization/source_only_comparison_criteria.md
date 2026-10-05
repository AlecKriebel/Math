# Source-only frozen comparison criteria: binary Markov/MTP2 clique factorization

This artifact was written before any candidate, inherited priority report, root file, sibling file, original priority gate, or candidate code/proof was read. Its mathematical comparisons use only the independently authenticated publisher source and deductions stated below. This is an independent audit of PR311/problem30005303; that label is task metadata, not evidence of a solution.

## Source authentication and reading

Primary source: Steffen Lauritzen, “Two open problems in graphical models of algebraic nature,” printed pp. 3125–3126 (references begin on p. 3127), in *Algebraic Structures in Statistical Methodology*, Oberwolfach Report 55/2022, DOI 10.4171/OWR/2022/55. Publisher URL: https://ems.press/content/serial-article-files/46992 . The workshop ran 4–10 December 2022; this is source metadata, not an independently established earliest publication date.

The downloaded publisher PDF has 600619 bytes and SHA-256 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65, matching the task's expected bytes and digest. PDF pages 5 and 6, bearing printed numbers 3125 and 3126, were rendered and visually inspected; layout text was independently extracted. The reference list on printed p. 3127 was read. Source binaries, extracted text and page renderings are private audit inputs excluded by this folder's .gitignore.

## Exact comparison target

Let V be any finite set; X={0,1}^V; G=(V,E) a finite simple undirected graph; and p:X→[0,∞) have sum 1. Zeros are permitted. Write x_A for coordinate restriction. The support S consists of states with p(x)>0.

The source's M(G) means **global** graph Markov: every separation of disjoint A and B by C in G implies X_A independent of X_B given X_C. Conditional independence at zero-mass conditioning values is vacuous. A check that only tests X_i independent of X_j given all remaining variables for nonedges is a pairwise Markov check and cannot be substituted without a proof under the exact hypotheses.

For finite probabilities, a fully checkable formulation for any A,B,C is that for each c the matrix [P(X_A=a,X_B=b,X_C=c)]_{a,b}, after marginalizing omitted coordinates, has rank at most one, equivalently all 2×2 minors vanish. This remains valid at zeros. The graph separation condition itself must also be verified.

The source's factorization is p(x)=∏_{A complete in G} ψ_A(x_A) for every state x, with ψ_A taking finite real values. The definition permits signed factors; it does not permit infinite factors or undefined zero-times-infinity expressions. Factors for all cliques, including singleton coordinates, may be used. Restriction to maximal cliques is equivalent: assign each smaller clique to one containing maximal clique and absorb its factor. For an isolated vertex its singleton is maximal. A constant empty-clique factor, if used, may be absorbed when V is nonempty; the empty-vertex case has its single probability equal to 1.

Signed factors do not enlarge this class for nonnegative p: if p=∏ψ_A, then ∏|ψ_A|=|∏ψ_A|=p. This elementary absolute-value argument is valid at every zero too. A counterexample to nonnegative finite factorization is therefore also a counterexample to the source's finite real factorization when the obstruction is proved for arbitrary finite factors or this equivalence is invoked.

The source's M_E(G) is the pointwise closure of the factorizing family (equivalently of the strictly positive Markov family). The source records M_+(G)⊆M_F(G)⊆M_E(G)⊆M(G). Membership of the closure is not exact finite factorization. Likewise, a proof of nonfactorization is distinct from a proof of nonmembership in the closure; either can refute an exact-factorization conclusion if the input hypotheses hold, but their strength and mechanisms must be stated correctly.

**Conjecture 2, exact target:** every binary p that is globally G-Markov and satisfies p(x∨y)p(x∧y)≥p(x)p(y) for every x,y∈X admits the above exact finite clique factorization. The inequality is MTP2 with coordinatewise max/min in the source's order 0<1.

**Conjecture 3, stronger exact target:** every binary globally G-Markov p whose support is closed under coordinatewise meet and join admits that factorization. Here “lattice” must mean the support is a sublattice of the Boolean cube, with its inherited coordinatewise operations, rather than an abstract lattice possessing unrelated meet/join. This follows from the source's strengthening immediately after the MTP2 inequality.

MTP2 implies this support closure: for x,y∈S the right-hand side is positive, hence both meet and join have positive mass. A support-lattice distribution need not be MTP2 because its positive weights can fail the multiplicative inequality. Consequently Conjecture 3 implies Conjecture 2, while a counterexample only to Conjecture 3 need not refute Conjecture 2.

Conjecture 1 (closedness of the pair/edge-factorizing MTP2 subclass) is a separate claim and is not the target of this audit. A counterexample to Conjecture 2 cannot automatically be called a counterexample to Conjecture 1: it needs the appropriate limiting sequence of MTP2 edge-factorizing distributions.

## Source-only deductions that can support comparisons

1. For any finite clique factorization, support equals the intersection of the cylinders where each factor is nonzero. In particular, S must equal its clique-projection join J_G(S)={x: x_A∈π_A(S) for every maximal clique A}. Proof: S⊆J_G(S) trivially. If x∈J_G(S), for every clique A choose s∈S with s_A=x_A; since p(s)>0 all its factors are nonzero, in particular ψ_A(x_A)≠0. All factors at x are then nonzero so p(x)>0. Conversely this condition alone gives a factorization of a **uniform** mass on S: use support indicators of the maximal-clique projections, with normalization absorbed into any factor. For general weights, this support condition is necessary but need not settle the numerical factorization.

2. A uniform distribution on any nonempty Boolean sublattice S is MTP2. If either x or y is off-support, its right side is zero. If both lie in S, meet/join also lie in S and both sides equal |S|^{-2}. Thus a globally Markov sublattice support with J_G(S)≠S would refute both conjectures. This deduction does not assert such a support exists.

3. Let two finite lists of cube states have equal multiplicities of every configuration on every clique. Any exact finite factorization forces equality of the corresponding products of probability masses, by substitution and reordering finite products. This works for signed and zero factors. Such a clique-balanced binomial/invariant can obstruct factorization and also every pointwise limit of factorizing distributions. A previously known invariant alone is not a previously known input distribution satisfying MTP2/global Markov.

4. On the four-cycle G with edges 12,23,34,41, all nontrivial separations are 1 separated from 3 by {2,4}, and 2 separated from 4 by {1,3}. Indeed removing zero or one vertex leaves a connected graph; removing two leaves only singletons to separate. Thus both corresponding conditional-independence statements are an exact global-Markov certificate on C4, not merely a pairwise surrogate. The graph's maximal cliques are its four edges. For larger graphs, neither the C4 reduction nor pairwise/global equivalence may be transferred without proof.

## Criteria for target success and historical equivalence

A positive resolution needs a proof for every finite G and every binary p under the exact relevant hypotheses, including zeros, with finite real clique factors. Positive-only Hammersley–Clifford results leave the central zero boundary unresolved. Results assuming decomposable/chordal G, a specific support condition not automatic here, stronger positivity/connectivity, or higher/lower-order interactions must not be described as solving the general source claim without an explicit specialization showing every added hypothesis holds.

A negative resolution of Conjecture 2 needs a graph, explicit nonnegative normalized masses, a global-Markov proof, a full MTP2 proof, and a checkable exact-finite-factorization obstruction. The same witness refutes Conjecture 3 through the MTP2→sublattice deduction. A negative resolution only of Conjecture 3 needs the same checks with support closure replacing MTP2, and must retain that limited scope.

For **already solved**, a prior primary statement/proof must have the same quantified claim or a genuinely equivalent stronger result that specializes with all hypotheses checked; alternatively a prior explicitly checkable witness must meet all target hypotheses and the nonfactorization criterion. Cite exact theorem/example locations and derive the specialization. Metadata, titles, abstracts, citation counts, bare assertions, and a failure to locate results are insufficient.

For an existing graphical-model counterexample, establish its support and masses, prove global Markov under the source definition, verify Boolean lattice/MTP2 in the source coordinate order, and establish finite signed-factor nonfactorization. A relabeling/bit reversal is permissible only with the transformation and transformed inequalities checked; coordinate reversal can change MTP2. A known C4 toric invariant and a newly selected MTP2 witness using it represent different priority claims. A known support pattern whose **uniform** law already qualifies is enough for prior disproof if the exact primary pattern and independent specialization are supplied, even if the old text did not use MTP2 terminology. A support pattern existing only as an arbitrary pairwise-Markov example is insufficient unless C4/global or other global Markov is established.

Separate priority of (i) graph/invariant/toric characterization, (ii) support or probability table, (iii) MTP2/global-Markov specialization, and (iv) general solution or refutation. Describe new specialization of old tools accurately without claiming the tool is new.

## First independent conclusion and remaining gap

The authenticated source poses a genuinely zero-inclusive, global-Markov, exact finite-factorization question. Conjecture 3 is stronger than Conjecture 2; a single globally Markov uniform nonfactorizing Boolean sublattice would disprove both. Finite signed factors are equivalent to nonnegative factors here. These are source-and-deduction conclusions only; **no candidate or prior solution has been examined and no claim of novelty or historical priority has been established**. The exact remaining gap is to inspect primary prior results and any released candidate against these criteria. Completion estimate for the assigned priority audit at this checkpoint: 15% (criteria authenticated; historical comparison pending).
