# Independent audit: pressing-balance mixture obstructions and endpoint exchanges

Date: 2026-10-12 UTC. Problem row: 1747.

## Verdict and accepted scope

**ACCEPTED as a separate mathematical supplement.** The two abstract countermodels, the indexed determinant identity, the endpoint-swap criterion, and the eleven-position forbidden pattern are accepted in the intended complete-singleton-addition-path scope. This public edition applies a meaningful scope-precision correction: the path-language result does not assert that arbitrary maximal chains of the inclusion poset are rank-complete, and every feasible set lying on a full path does not justify that broader assertion. The arguments for the intended path language and the other accepted results are unchanged. The packet does not resolve the pressing 1/3–2/3 conjecture and does not exhibit a pressing counterexample.

The accepted source is the original authored proof (identified by the original-proof record in ORIGINAL_INPUT_PINS.json), SHA-256 `28a14a8616b238cd70dad154584b7ae9a9274eaa0f6a5cdaaab4a407afe17937`, 12,650 bytes, together with the eight-file manifest and its pinned supporting files. The manifest itself and all eight entries are independently pinned in the original audit input pinset (identified in ORIGINAL_INPUT_PINS.json); every supplied byte count and SHA-256 matches. Originals were only read. Author computations were replayed from separate copies. No repository, queue, publication, or original audit was changed.

Accepted claims are about full-length successful permutations of nonsingular symmetric matrices over F2, conditional on existence of such a permutation. An abstract family is not promoted to a matrix language. Neither computational samples nor the finite automaton are promoted to a proof of general balance. The nonrealizability result concerns the exact seven-word language; it does not identify the displayed prefix sets with all nonsingular principal subsets.

## 1. Source attribution and the V-poset mixture

The primary PDF, [Cooper–Gartland–Whitlatch, A New Characterization of V-Posets](https://people.math.sc.edu/cooper/VPosets.pdf), and the [official arXiv entry](https://arxiv.org/abs/1810.07276) were independently opened during this audit. PDF Lemmas 3–4 support the leading-minor criterion and instructional-poset decomposition. Section 5 explicitly describes disjoint extension classes. Definition 10 and Theorem 3 concern V-posets and autonomy. They do not classify every instructional poset in a graph with several classes as a V-poset. The packet attributes these facts correctly.

For the authored sixteen-label construction, each poset has precisely one incomparable pair; all other comparisons are fixed by the stated ordered blocks. Starting with two isolated elements and appending single greatest/least elements constructs it as a V-poset. Each therefore has exactly two extensions. Class i reverses its distinguished a_i,b_i pair in both extensions, and its c_i,d_i pair in exactly one. Every other class preserves those pairs. Consequently the union consists of eight distinct words, with minority counts:

- 112 unordered pairs have count 0;
- 4 unordered pairs have count 1;
- 4 unordered pairs have count 2.

Dividing by eight gives 0, 1/8, and 1/4. None lies in the closed interval [1/3,2/3]. The internally balanced pair depends on the class, so balance of every class and equality of class sizes do not imply balance of their mixture.

Each class is a single adjacent-swap edge. Across classes, at least the two distinct a,b blocks are reversed. A one-letter relocation changes only the moved letter's relative order with other letters; it cannot reverse two pairs on disjoint supports. Thus no cross-class adjacent swap or one-letter relocation occurs. The four connected components are exactly the four extension classes.

The independent verifier generates each complete linear-extension set from predecessor relations, rather than merely trusting the proposed two words. It separately checks disjointness, marginals, and one-letter-relocation separation. The source correctly declines to assert that this eight-word union is a full maximal-chain language or a pressing language. The accepted conclusion is failure of the listed abstract sufficient conditions only.

## 2. Generic prefix-set countermodel

Let B_t=[t], and let branch i have active level sets C_i(t)=(B_t\{i})∪{i+k} for i≤t<i+k. These differ from B_t and from each other at the same level. All other prefixes of that branch coincide with the baseline.

Every singleton-addition edge between consecutive levels can be classified directly:

1. B_t to B_(t+1) is a baseline edge.
2. B_t to an active C_j(t+1) is possible only at its starting level t+1=j, since otherwise j is already in B_t but missing from the target.
3. Active C_i(t) to B_(t+1) is possible only at its ending level t+1=i+k, because its extra element i+k must have entered the baseline.
4. An active branch cannot change to a different active branch. If j≤t, the first set contains j while the second omits it. If j=t+1, then i+k>k≥t+1 and the first set's extra element is absent from the second, since i≠j.

A path that enters branch i must remain on it until its endpoint. All starts occur by level k and all ends after k, so it cannot subsequently enter another branch. Therefore the complete empty-to-full singleton-addition path language is exactly {e,s_1,...,s_k}. In this family every set lies on a full path. The asserted language is the exact family of complete singleton-addition chains from empty to full; no assertion is made that every maximal chain of the inclusion poset is rank-complete.

There are (2k+1)+k²=(k+1)² distinct feasible sets: baseline levels plus k active sets on each of k distinct branches. The packet's k=6 count of 49 is correct.

The pair-reversal classification is correct. Among same-half pairs, a_i,a_j reverses only in s_i for i<j, while b_i,b_j reverses only in s_j. Pair a_i,b_i reverses only in s_i. For mixed pairs a_i,b_j, there are no reversals if i<j, and two reversals, in s_i and s_j, if i>j. At k=6 the 66 pair minorities are 0 for 15 pairs, 1/7 for 36 pairs, and 2/7 for 15 pairs. Hence this uniform full-path language has no balanced pair.

For k≥2, e and s_i differ by a nonadjacent transposition, which reverses the two endpoints and each endpoint's order with intervening letters. No single moved letter can cause all those reversals. Distinct s_i and s_j differ by two disjoint transpositions, also impossible by moving one letter. Therefore the nonempty fixed-deletion insertion fibers are singletons and all adjacent-swap components are singleton extension classes.

The independent computation reconstructs every maximal path from the feasible-set inclusion graph for each k=2,...,12, verifies all pair formulas, and checks every nontrivial one-letter-relocation possibility. This is finite corroboration; the argument above proves the arbitrary-k claim.

## 3. Fully indexed Cauchy–Binet identity

Fix one-based i≤k<j and C=([k]\{i})∪{j}. With A=UᵀU and R=U[[k],[k]], Cauchy–Binet yields

    det A[C,C] = Σ_(S⊂[n], |S|=k) det U[S,C]².

The non-j columns in C vanish in every row greater than k. A minor with two such rows therefore has two rows supported only in the j column and has determinant zero. Every remaining row set is either [k] or ([k]\{r})∪{s}, where 1≤r≤k<s≤n.

The first minor is a column replacement of R. Moving column j to its displayed sorted position produces only a sign, which is immaterial over F2. Cramer's rule and det R=1 give contribution (R⁻¹c)_i, where c=U[[k],{j}].

For the second form, expansion along the unique row beyond k leaves U_sj times det R with row r and column i removed. The cofactor-to-inverse indexing is precisely

    cofactor_(r,i)(R) = (R⁻¹)_(i,r),

again because det R=1 and all signs vanish. This confirms the potentially delicate index reversal: the fixed inverse index is the deleted column i, not the deleted row r. Every scalar square equals itself over F2. Summing these minors over r and s gives

    [Σ_(r=1)^k (R⁻¹)_(i,r)] [Σ_(s=k+1)^n U_sj].

Upper triangularity truncates the second sum at j. The first is (R⁻¹1)_i. Thus the displayed identity (1) is correct with exactly the stated index ranges, including k=i and k=j−1.

Exchanging positions i,j changes precisely the intermediate prefixes with i≤k<j, so all their determinants being 1 is necessary and sufficient for the exchanged order. No suffix condition has been omitted. Invertibility of R is automatic because it is unit upper triangular.

Fixing earlier columns fixes R, R⁻¹, and the row-sum coefficient. The right side is linear in the entries of column j before fixing its diagonal; after U_jj=1 is imposed, the constraints are affine in its strictly upper entries. There are no omitted terms involving later columns.

For j=i+1, the determinant is 1+U_i,j, so success is equivalent to U_i,j=0. For j=i+2, writing a=U_i,i+1, b=U_i,i+2, c=U_i+1,i+2 gives b=c and b+ac+a=0. If a=1, substitution b=c makes the second condition 1=0; hence a=0 and then b=c=0. Conversely all three zero entries suffice. Earlier and later vertices do not affect these conditions.

Independent arithmetic checked every unit upper root through order five, including the order-one boundary: 1,099 roots, 21,154 replacement determinants, and 10,650 endpoint orders. It additionally checked 34,560 identities in 120 deterministically sampled ambient roots of orders 8, 11, and 15. The independent implementation imports no authored modules and uses a separate row-basis determinant algorithm and forward-substitution inverse-row computation.

## 4. Human proof of the three-exchange obstruction

### Window localization

Partition the root at the positions before a window:

    U = [P Q; 0 T].

Then UᵀU has blocks PᵀP, PᵀQ, QᵀP, QᵀQ+TᵀT. Eliminating the earlier successful prefix gives Schur complement

    QᵀQ+TᵀT − QᵀP(PᵀP)⁻¹PᵀQ = TᵀT.

This remains true in characteristic two, where subtraction equals addition. Its leading seven-position principal block is the Gram matrix of the corresponding seven-by-seven principal block of U: rows later than that block vanish on its columns. Hence the local calculation legitimately applies inside an arbitrary ambient root. Conditions imposed only on the eleven-position interval suffice.

### Necessary equations from one successful six-step exchange

Use local positions 0,...,6, put x_r=U_r,6 for 0≤r≤4, and assume consecutive entries are 1. Then U_5,6=U_6,6=1. Let v be row 0 of the inverse of the leading six-by-six block. Upper triangular inversion makes its initial segments the inverse rows for smaller leading blocks. In particular v_0=v_1=1.

At prefix sizes 1 and 2, the indexed identity yields

    D_1=x_0+x_1+x_2+x_3+x_4,
    D_2=x_0+x_1.

Success forces D_1=D_2=1, and therefore x_2+x_3+x_4=0. At sizes 5 and 6, writing V=Σ_(r=0)^4 v_r x_r and H=Σ_(r=0)^4 v_r gives D_5=V and D_6=V+H. Their common value 1 forces H=0.

The inverse recurrence gives v_2=1+U_0,2 and

    v_4=U_0,4+U_1,4+v_2 U_2,4+v_3.

Thus v_0+v_1=0 and cancellation of v_3 yield

    H=1+U_0,2+U_0,4+U_1,4+U_2,4+U_0,2 U_2,4=0.

Both packet equations (2) and (3) follow exactly.

### Two windows force an entry in two incompatible ways

If exchanges start at i and i+2, the first window's zero-sum relation says

    U_i+2,i+6+U_i+3,i+6+U_i+4,i+6=0.

In the second window's H equation, set f=U_i+2,i+4 and x=U_i+4,i+6. The three displayed terms cancel, leaving 1+f+fx=0, or f(1+x)=1. Since the field is F2, the only solution is f=1,x=0.

The first two exchanges therefore force U_i+4,i+6=0. Applying the same implication to exchanges starting at i+2 and i+4 forces that same entry to equal 1. This contradiction proves the stated proposition. It does not depend on a finite enumeration or a solver certificate.

### Exact seven-word nonrealizability

If the seven-word family were exactly a matrix's full success set, identity would succeed. Every consecutive root entry would have to be 1, because a zero would admit the corresponding adjacent swap, absent from the family. The family also includes the exchanges (1,7), (3,9), (5,11). These violate the proved proposition. Thus it cannot be the exact success language of any such matrix. This reasoning makes no assumption about additional nonsingular principal subsets that do not occur on a successful full path.

## 5. Complete automaton and execution corroboration

A six-position chain root has 15 strictly upper entries, five fixed consecutive entries, and therefore ten free bits. For each of all 1,024 states the audit tries all 32 choices for the next column's five free bits. This enumerates all 32,768 seven-position chain roots. A direct rank-one pressing test of the order (6,1,2,3,4,5,0), without using identity (1), determines each allowed edge. Exactly 2,560 local swaps succeed. On every one, the audit also verifies equations (2), H=0, and the expanded polynomial (3).

The independently built graph has the exact same serialized edge SHA-256 as the authored affine graph:

    50e1b3bfc758c00a20f5550b20f3f25138211d2d7bfa26be0354214772c7dc30

This checks the full labeled graph, not merely counts. Independent terminal-layer elimination recovers every stored state rank, with histogram 512,256,128,64,64 at ranks 0,...,4. Every edge strictly decreases rank. Dynamic programming gives weighted path totals 1024,2560,6400,11520,23040,0,0 at lengths 0,...,6. Empty length-five path set is consistent with the human obstruction on starts 1,3,5; the automaton additionally requires the intervening starts.

The original Python checks and affine certificate checker were replayed from copied files in normal, -O, and -OO modes. Their JSON results agree exactly with the supplied result files. The independent checker was likewise run in all three modes with byte-identical output. None of its checks relies on Python assert statements.

The authored C++ checker was compiled with C++17, -O2, -Wall, -Wextra, and -pedantic. Its replay exactly reproduces all stage counts. The attempted counts sum to 1,425,408. Its recursion checks all band entries relevant to consecutive seven-position windows; remote upper entries are correctly irrelevant after the localization argument. It is corroboration of this forbidden-pattern constraint, not exhaustive enumeration of arbitrary twelve-position pressing families.

## 6. Nonblocking wording clarifications

The arguments for the intended complete-singleton-addition-path claims are unchanged. The maximal-chain wording requires a meaningful scope-precision correction to avoid asserting that arbitrary inclusion-poset maximal chains are rank-complete. The insertion-fiber clarification is nonblocking. The two explicit interpretations used in this edition are:

1. Replace “every fixed-order one-letter insertion fiber is a singleton” with “every nonempty fixed-order one-letter insertion fiber is a singleton; all other fibers are empty.” Fibers indexed over every possible deleted-label order need not be nonempty.
2. Replace “all maximal-chain/prefix-splicing closure conditions” with “the exact family of complete singleton-addition chains from empty to full, and hence closure under every splice at a common prefix set.” This avoids an undefined universal quantifier over possible additional closure axioms.

Acceptance uses those explicit interpretations, without silently asserting any further closure property or realizability. Original source files have not been edited.

## 7. Integrity and completion limits

The audit has a separately hashed input pinset, explicit optimization-safe validation, mutation/missing-file/self-consistent-manifest controls, an internal complete file freeze, and an external seal. The original packet's eight manifest entries and manifest bytes are rechecked at completion. Exploration scripts and preexisting cache files are not mathematical evidence and are excluded from the accepted input set.

The general balance conjecture remains unresolved. No full-language matrix counterexample, inequality comparing instructional-class weights, or general global-balance theorem is established here. No assertion of novelty has been audited or added. No third-party source text or original source PDF is included in the deliverable.
