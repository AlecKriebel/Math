# Erdős 949 / ID 2401: five-approach mathematical audit

Date: 2026-10-21 UTC. **Disposition: NOT SOLVED.**

This report addresses the unrestricted original real-set problem. It establishes several sufficient conditions and exact barriers, not a general answer. No priority claim is made for the auxiliary lemmas. In particular, the small-cardinality, Sidon and Baire-property cases are already recorded prior work, not discoveries of this investigation. The mathematical arguments below are authored derivations, not copied third-party proofs.

## 1. Target and source boundary

Write c=|R|. A set S is sum-free when (S+S)∩S=∅; repeated summands are allowed. The question asks whether every such S admits A with

|A|=c, A∩S=∅, and (A+A)∩S=∅.

It does **not** ask that A+A⊆A. It does not assume S is measurable, has the Baire property, or is Sidon. Both unary exclusion and diagonal exclusion 2a∉S are mandatory.

The primary original is Erdős, *Problems and results on combinatorial number theory III* (1977), printed p. 57, PDF page 15: https://www.renyi.hu/~p_erdos/1977-27.pdf . Its extracted text was reinspected. The source/status gate records the original formulation and bounded literature review. This investigation's direct refreshes of https://www.erdosproblems.com/949 and https://www.erdosproblems.com/forum/thread/949?order=oldest returned HTTP 403, so no fresh direct tracker-status certificate is asserted.

The primary formalization repository confirms a merged Sidon-variant proof, not a general proof: https://github.com/google-deepmind/formal-conjectures/pull/1509 . The page identifies the AlphaProof-derived contribution and merger on January 6, 2026. No local Lean build was performed. The general question remains unresolved by the sources and arguments inspected here; this is not a worldwide priority certificate.

## 2. Preliminary lemma: diagonal-safe points are plentiful

Let V={x∈R:x∉S and 2x∉S}. Then |V|=c for every sum-free S.

If |S|<c this is immediate, since R\V=S∪(S/2) has size <c. Suppose |S|=c. For every s∈S one of 2s,3s,5s lies in V:

* 2s∉S by sum-freeness. If 4s∉S, use 2s.
* Otherwise 4s∈S, hence 3s∉S since s+3s=4s. If 6s∉S, use 3s.
* Otherwise 6s∈S. Now 5s∉S since s+4s=5s, and 10s∉S since 4s+6s=10s. Use 5s.

Consequently S⊆(V/2)∪(V/3)∪(V/5), and finite-union cardinal arithmetic gives |V|=c. No regularity of the cardinal c is used.

This proves that unary and diagonal conditions alone do not exhaust the available continuum. It does not control sums of two different points.

## 3. Approach I: maximality and transfinite greedy extension

### Recovered known case

For |S|=κ<c, construct a sequence (a_α) indexed by α<c. At stage α avoid

S ∪ (S/2) ∪ {a_β:β<α} ∪ ⋃_{β<α}(S−a_β).

The forbidden set has size at most max(ℵ₀,κ,|α|)<c, so a new point exists. The resulting A has size c, lies outside S, and all its sums including doubles avoid S. Indeed this argument does not use sum-freeness. It remains valid if c is singular because the bound κ is uniform.

### Exact obstruction at continuum cardinality

On V from Section 2, join distinct x,y when x+y∈S. A solution is precisely an independent set of cardinality c. If I is a maximal independent set, then

V⊆I∪⋃_{i∈I}(S−i).

If |I|<c, this translates into the covering certificate

R=S∪(S/2)∪I∪⋃_{i∈I}(S−i).

Equality here means that the displayed union covers R; every constituent is already a subset of R. For |S|=c the cardinality estimate no longer rules out this cover. Sum-freeness gives S∩(S−s)=∅ for s∈S, whereas the maximal independent points i are outside S. Thus the familiar disjoint-translate identity cannot simply be applied to the relevant i.

**Outcome:** known small-cardinality theorem recovered; no extension to arbitrary continuum S. The exact missing ingredient is a structural obstruction to the displayed small family of translates covering all eligible points.

## 4. Approach II: sparse difference fibers and a repaired translate

### Sufficient-condition theorem

Suppose |S|=c and some infinite cardinal κ<c satisfies

|S∩(S+d)|≤κ for every nonzero d∈R.

Then a continuum-sized A avoiding S in both degrees 1 and 2 exists. This theorem does not require sum-freeness.

**Proof.** For nonzero a∈S, define L_a={x∈S:2x−a∈S}. Choose distinct nonzero a,b∈S. The map x↦2x−a injects L_a∩L_b into S∩(S+(b−a)), so |L_a∩L_b|≤κ. If both S\L_a and S\L_b had size <c, their finite union would have size <c, and L_a∩L_b would have size c. Therefore at least one anchor a has |S\L_a|=c.

From S\L_a delete a and U_a={x∈S:x−a/2∈S}. Since a≠0, U_a=S∩(S+a/2) has size ≤κ. The remaining vertex set W has size c.

Join distinct x,y∈W when x+y−a∈S. For a fixed x∈W, neighbors belong to S∩(S+(a−x)). Since x≠a there are at most κ. A greedy recursion of length c constructs independent T⊂W of size c: before stage α<c, at most max(ℵ₀,κ,|α|)<c vertices have been selected or forbidden by their neighborhoods. Put A=T−a/2.

Unary exclusion follows from deleting U_a. Distinct sums avoid S by independence. Diagonal sums avoid S because T avoids L_a. Translation preserves cardinality. ∎

### Relation to existing work

A Sidon set has at most one representation of each nonzero difference, so the theorem includes the already proved Sidon case. This is a clean sufficient-condition generalization, not a claim of new literature priority and not removal of the essential additive-sparsity hypothesis.

### Singular-continuum caveat

If c is regular, the weaker assumption |S∩(S+d)|<c for each d≠0 also suffices, since fewer than c neighborhoods each of size <c have union of size <c. If c is singular, that inference is unjustified without a uniform bound. A graph consisting of cf(c) disjoint cliques with sizes cofinal in c has c vertices and every degree <c, but every independent set has size at most cf(c). This is a barrier to the generic graph argument, not an additive counterexample to the proposed weaker condition.

**Outcome:** conditional theorem with an independently checked proof; unresolved high-multiplicity regime remains.

## 5. Approach III: rich additive structure and reflection cores

Sum-freeness gives the useful exact identity S∩(S−S)=∅: if x−y=z with x,y,z∈S then y+z=x is forbidden.

### Reflection-core sufficient condition

Suppose a∈S and C=S∩(2a−S) has size c. Put A=C−a. Then A⊆S−S. For any x,y∈C,

(x−a)+(y−a)=x−(2a−y)∈S−S,

because 2a−y∈S. Thus A and A+A both avoid S, and |A|=c. The displayed identity includes x=y.

The location of the center matters. It is not enough merely to assert a large fiber S∩(t−S) for an arbitrary t and silently infer (S∩(t−S))−t/2⊆S−S. The argument above uses a∈S for unary exclusion.

### A rigorous obstruction to a sparse/rich dichotomy

Choose a Q-linearly independent B⊂(1/2,1) of cardinality c. Such B exists by transfinite recursion: the rational span of fewer than c previously chosen points has cardinality <c, while the interval has cardinality c. Put S=B+B. Then S⊂(1,2), hence S is sum-free.

For distinct b,b'∈B, let d=b−b'. For every t∈B, b+t∈S and b+t−d=b'+t∈S. Thus |S∩(S+d)|=c, contradicting the sparse hypothesis.

Nevertheless every reflection core centered at a∈S has at most three points. If a=b+b' with b≠b', the equation x+y=2b+2b', with x,y∈B+B, forces the coefficient multiset of x to be one of {b,b}, {b,b'}, {b',b'}, by rational independence. Hence x∈{2b,b+b',2b'}. If a=2b, the only possibility is x=2b. These are exactly the possible core points, so the bounds are attained in the distinct case.

This example lies in neither sufficient-condition class. It is emphatically not a counterexample to Erdős 949: every negative half-line is an immediate witness, because S is positive.

### Other false shortcuts

* A=2S can fail: S={1,4} is sum-free, but 2+2=4∈S.
* A=S−S can fail: S={1,5,8} is sum-free and 4∈S−S, but 4+4=8∈S.
* A=(S\{a})−a/2 can fail without the diagonal repair: S={1,3,5}, a=1 gives 5/2∈A and 5∈A+A∩S.

**Outcome:** a second verified sufficient condition; an explicit continuum example proves that combining it with the sparse condition does not settle the problem.

## 6. Approach IV: Ramsey theory on the sum graph

A tempting strategy is to apply a general large-independent-set theorem to the graph on V. The next realization lemma shows why a restriction to an arbitrary large candidate set loses almost all useful structure.

Let P⊂(1,11/10) be Q-linearly independent with |P|=c. For any simple graph G on P define

S_G={p+q:{p,q} is an edge of G}.

Then S_G⊂(2,11/5), so S_G is sum-free. Every p∈P lies outside S_G by magnitude. Also 2p∉S_G: the relation 2p=q+r for distinct q,r∈P would violate rational independence. Finally p+q∈S_G for p≠q exactly when {p,q} is an edge, because distinct unordered pairs have distinct sums. Thus P⊂V and its induced sum graph is exactly G.

Taking G complete gives a clique of size c inside V. In particular, the full graph need not have finite or countable chromatic number; and no theorem asserting an independent c-set in every arbitrary continuum subset of V can hold. Even the exact induced graph on a selected continuum Q-independent transversal can be entirely hostile.

This does not realize an arbitrary graph on all of R, and does not disprove existence of an independent c-set elsewhere. In this bounded example a negative ray supplies one. Finite simulations likewise cannot distinguish the hard global case from such trivial examples.

**Outcome:** a precise obstruction to naive Ramsey or countable-coloring reductions, not a negative solution.

## 7. Approach V: algebraic subspaces, quotients and nonregular examples

A sufficient algebraic certificate is a Q-vector subspace H⊂R with |H|=c and H∩S=∅. Since H+H=H, it is a valid witness. Similarly, a homomorphism φ with a continuum kernel and 0∉φ(S) gives H=ker φ.

This is useful for genuinely nonregular S. Choose a surjective Q-linear map φ:R→Q with a nontrivial continuum-dimensional kernel H, and set S=φ⁻¹({1}). Then S+S⊆φ⁻¹({2}), so S is sum-free, and H is a continuum witness. H is dense, since it contains a nonzero rational line. Its countably many cosets cover R. If H were measurable, measure zero would contradict that cover; positive measure would force H to contain a neighborhood of 0 by the difference-set theorem, making the subgroup all of R. Both are impossible. The Baire-property argument is parallel: meagerness contradicts the countable cover, and nonmeagerness plus the Baire property forces H−H=H to contain a neighborhood. Thus H and its translate S have neither regularity property. Absence of measurability or the Baire property alone is nowhere near a counterexample.

However, the subspace certificate is not universal. For S=(1,2), every nonzero Q-vector subspace meets S, since Qx is dense for every x≠0. Yet a negative half-line solves the original problem. Hence even solvable sum-free sets need not admit any nonzero subspace witness. An attempt to force an additive subgroup changes the mathematical target and can fail needlessly.

**Outcome:** explicit large pathological families are solved, but algebraic closure is too strong a universal witness requirement.

## 8. Known regularity cases and the diagonal audit

These cases are included to delimit scope, not counted as novel general progress.

If S has the Baire property and is nonmeager, it is comeager in some nonempty open interval after shrinking a Baire open representative. For sufficiently small t, that interval and its translate overlap, and the corresponding comeager copies of S meet. Therefore S−S contains an interval about 0. Since S avoids S−S, a sufficiently small interval A about 0 has A∪(A+A) disjoint from S and has cardinality c.

If S is meager, put U=S∪(S/2). Write U inside a countable union of closed nowhere-dense sets. The relation R={(x,y):x+y∈S} is meager in R²: addition is a continuous open map, so the inverse image of a closed nowhere-dense set is closed nowhere dense. A Cantor fusion construction gives a perfect set P avoiding U, with all distinct-point pairs outside R. Explicitly, start inside a bounded interval. At stage n choose two child intervals inside each prior interval; choose their finitely many centers in the dense open set of tuples avoiding coordinate-equality diagonals, the first n unary nowhere-dense sets, and the first n sum-preimages for every pair of distinct coordinates. Coordinate-equality diagonals are closed nowhere dense; coordinate projections and coordinate-sum maps are open, so each other forbidden tuple set is also nowhere dense. Choose small disjoint closed child intervals retaining all these finite avoidances and diameters tending to zero. The limiting Cantor set avoids every unary bad set; any two distinct branches eventually occupy distinct intervals, so their sum avoids every binary bad set. Because P avoids S/2, diagonal sums avoid S as well. Thus P is the required continuum witness.

The positive-measure measurable case follows in the same way from the difference-set neighborhood theorem. The null measurable case is reported in existing working literature via a null-set perfect-set theorem, but no new proof of that specialized theorem is supplied here and it is not an acceptance dependency. In particular, a category theorem must not be substituted without justification for a null-set theorem: null sets need not be meager. The full measurable-case literature assertion is treated as a duplicate-warning lead rather than as something independently certified by this report.

## 9. Reproducible exact checks and review

Run `python erdos_continuum_complement_2401/exact_checks.py` from the workspace root. It uses only Python's standard library and exact integer/rational arithmetic. The saved output is `exact_checks_result.json`.

Checks completed:

* all 356 sum-free subsets of the integers from −6 through 6;
* 1,186 instances each of the diagonal-dilate lemma and reflection-core construction;
* all 1,024 simple graphs on five designated vertices, realized exactly by sum-free sets;
* three explicit counterexamples to naive witness formulas;
* an eight-generator base-5 coefficient model, with 36 pair sums, maximum centered reflection fiber 3, and a selected difference fiber of size 8.

All final checks passed. An initial test overclaimed the entire intersection (S−S+S−S)∩S for S={1,5,8}; exact evaluation found {1,8}, not {1,5,8}. The test was corrected to the only needed assertion, 8∈(S−S+S−S)∩S. The mathematical counterexample never depended on the incorrect enumeration.

These finite checks do not prove continuum statements, verify novelty, or certify an exhaustive search over real sets. Proofs of the continuum lemmas are above. Independent adversarial review of the thin-fiber theorem, singular-cardinal caveat, reflection-core theorem, diagonal-safe lemma, and nonexhaustive B+B example is recorded separately in `INDEPENDENT_AUDIT.md`. No formal proof assistant verification is claimed.

## 10. Acceptance decision

**Reject any claim that the general problem has been solved or refuted by this work.**

The five substantive routes yield: (I) an exact cardinality/cover obstruction; (II) a thin-difference sufficient-condition theorem; (III) a rich-reflection theorem and proof that the sparse/rich split is not exhaustive; (IV) arbitrary induced-graph realizations ruling out naive Ramsey simplifications; and (V) algebraic certificates with both successful pathological examples and a rigorous limitation.

The known small-cardinality, Sidon and Baire cases remain known cases. No assumption of continuum regularity, CH, measurability, perfect-set containment, additive closure of A, or finite-to-infinite transfer has been used to pretend to resolve the unrestricted question. A full solution still needs a genuinely global argument for arbitrary continuum-sized sum-free S, or an actual sum-free S for which every continuum subset of its complement has a pairwise sum in S. No such object or proof is established here.
