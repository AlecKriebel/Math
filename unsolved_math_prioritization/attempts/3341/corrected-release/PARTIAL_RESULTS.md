# Balanced-picture MSO alternation: five attempts and rigorous partial results

Problem 3341 / OPG-37448. Research date: 2026-10-04. **Status: unsolved, five substantive approaches used.** This is not a complete resolution and makes no novelty claim. In particular, the first-level separation below is a reconstruction of known mathematics, not a new answer to the hierarchy problem.

## 1. Exact target and conventions

A picture over a fixed finite alphabet A is a nonempty rectangular array p:[h]×[w]→A. Its **pixel structure** has one element per cell, horizontal and vertical directed immediate-successor relations H,V, and unary letter predicates. Boundary predicates Top, Bottom, Left, Right are first-order definable by absence of the appropriate predecessor/successor. There are no built-in row-equality, column-equality, arithmetic, order, or arbitrary binary relation variables. Using coordinate structures instead would change the logic.

Σ_k consists of sentences in monadic prenex form with at most k alternating blocks of set quantifiers, starting existentially, followed by an arbitrary first-order matrix. Π_k is its dual. Σ_0=Π_0=FO. The finite number of variables and the matrix may depend on the sentence, never on picture size. Classes are semantic relative to the stated domain of pictures. A separator at level k is one fixed Σ_{k+1} sentence with no equivalent Σ_k sentence on the entire domain.

Write Sq for square pictures. For fixed C≥1 and integer d≥1, write B(C,d) for pictures satisfying max(h,w)≤C min(h,w)^d. B(C,1) is linear balance; d>1 permits polynomial imbalance. The constants are fixed for the whole class/language. Allowing a different C for each individual picture makes the condition vacuous. In particular, the union of B(C,1) over all constants C is all finite rectangles, and is not the intended balanced problem. Requiring exactly w=P(h) is a different convention from a uniform polynomial upper bound. The original OPG question states linear/polynomial relatedness informally. Gardy’s slide 22 explicitly gives exact-format language conditions w=c h and w=P(h), with one fixed c or P for the language. Those are separate from the uniform upper-bound domains B(C,d) used here. Slide 23 states a folding/unfolding equivalence in the linear setting; this write-up does not invoke that claim as a proved transfer theorem. We preserve the square, fixed-linear-bound, and fixed-polynomial-bound questions; none is declared resolved.

**Target:** establish every level separation on balanced pictures, or establish an actual collapse/refutation, including the polynomial and linear regimes requested in the original question. Proving only Σ_1≠Π_1 does not do this.

### Domain-monotonicity lemma

If C⊆D are domains of structures of the same signature and a formula φ separates Σ_{k+1}(C) from Σ_k(C), that same formula separates on D. Otherwise a Σ_k equivalent on D restricts to a Σ_k equivalent on C. Consequently a separation on Sq implies that level separation on every B(C,d), since Sq⊆B(C,d). This is a claim about relative definability; it does not assume that the subdomain Sq has an FO definition.

## 2. Attempt 1: restrict the tower witnesses

**Mechanism:** retain an unrestricted rectangular-grid hierarchy witness after imposing balance.

### Proposition 1 (superpolynomial format witnesses become finite)

Suppose f:N_{>0}→N_{>0} is eventually at least h and f(h)/h^d→∞ for every fixed integer d. A language whose pictures all have formats h×f(h) has finite intersection with B(C,d), for every fixed C,d and fixed finite alphabet.

**Proof.** For sufficiently large h, f(h)>C h^d and f(h)≥h, so the balance inequality fails. There are only finitely many remaining heights, one finite width per height, and finitely many colorings at each such format. ∎

In particular this applies to every f eventually bounded below by 2^h. One elementary proof of 2^h/h^d→∞ is to retain the binomial coefficient binom(h,d+1) in 2^h: for h≥2(d+1), it is at least (h/2)^{d+1}/(d+1)!, and division by h^d gives a quantity tending to infinity.

Every finite language of finite relational structures is FO definable. For a finite structure of size n, existentially name n distinct elements, state that they exhaust the domain, and specify the complete atomic diagram, including negative relation instances. A finite disjunction defines any finite language up to isomorphism. Thus the above restricted witnesses are FO definable, regardless of their original alternation complexity.

**Conclusion and exact gap.** The superpolynomial formats in the unrestricted-grid theorem cannot simply be intersected with the balanced domain to retain a separator. This proposition does not show that all balanced languages have low alternation, or that every possible adaptation of the original proof fails. A balanced infinite witness with a new lower-bound argument is still required.

## 3. Attempt 2: pad rectangles into squares

**Mechanism:** pad h×w, h≤w, to a w×w square using a fresh blank letter, keeping the original picture in the upper-left corner.

### Proposition 2 (the easy direction preserves monadic blocks)

On the promise of a correctly padded input, every Σ_k or Π_k formula on the original rectangle has an equivalent formula of the same monadic alternation level on the padded square.

**Proof.** Let Active(x) mean that x is not blank. Keep relation atoms and letter atoms, and relativize every first-order quantifier to Active: ∃x ψ becomes ∃x(Active(x)∧ψ), and ∀x ψ becomes ∀x(Active(x)→ψ). Leave set quantifiers unrestricted. By induction, a translated subformula depends on a quantified set only through its intersection with Active. The restriction map from all subsets of the square onto all subsets of the active rectangle is surjective. Therefore existential and universal set quantification have exactly their original semantics, without changing their order or polarity. The induced H,V structure on the active cells is precisely the original rectangle. ∎

This is only a **promise** statement. It does not assert that the entire language of valid padded encodings is FO definable, or that an arbitrary square formula ignores padding.

### Proposition 3 (why the needed converse is not automatic)

For unbounded w/h, this padding map cannot be a one-dimensional fixed-copy interpretation with at most c copies per original cell, for any fixed c.

**Proof.** The original universe has hw elements; such an interpretation has at most c hw elements, even if it subsequently takes a quotient. The padded square has w² elements, and w²/(hw)=w/h is unbounded. ∎

A d-dimensional tuple interpretation can create more elements, but replacing a unary predicate on output tuples gives a d-ary predicate on the original domain. It is not an automatic translation back into *monadic* second-order logic.

**Conclusion and exact gap.** Proposition 2 carries definability forward. Nondefinability would need an inverse translation for every allegedly simpler sentence on padded squares. That sentence may use arbitrarily many padding cells as computational storage. The cardinality argument rules out one standard inverse mechanism; it is not an impossibility theorem for every conceivable logic translation. A same-level inverse, or a padding-insensitive lower bound, remains unproved. For bounded aspect ratio the cardinality obstruction disappears, but disappearance of that obstruction is not itself a folding proof.

## 4. Attempt 3: a complete first-level separation directly on squares

**Mechanism:** an explicit existential mismatch certificate and an accepting-tiling splicing contradiction. This reconstructs the known non-complement-closure phenomenon mentioned in the source, using a square reflection language.

For binary n×n pictures let Mirror be horizontal reflection symmetry:

p(i,j)=p(i,n+1−j) for every i,j.

### 4.1 An explicit EMSO definition of the complement

All formulas below are macros for first-order formulas using H,V and unary sets.

Row(S) says (i) S has exactly one element on the left boundary, and (ii) for every H(u,v), S(u)↔S(v). Thus S is exactly one full row. Col(S) is the analogous condition with exactly one top-boundary element and invariance along V. Nonemptiness is part of each definition.

Define SE(x,y):=∃z(H(x,z)∧V(z,y)). Define SW by one horizontal step left and one vertical step down. Each is a fixed first-order relation.

Diag+(D) consists of these clauses:

1. On the top boundary D holds exactly at the top-left corner.
2. For each x∈D not on Bottom, there is y∈D with SE(x,y).
3. For each x∈D not on Top, there is y∈D with SE(y,x).
4. Every member of D on Bottom is on Right.

Diag−(E) has top-right in clause 1, SW instead of SE, and Left in clause 4. On an n×n square these clauses uniquely force D={(i,i)} and E={(i,n+1−i)}. Indeed repeated predecessors carry any marked cell to the unique marked top cell, and repeated successors force the entire corresponding diagonal. This also holds at n=1. On nonsquares the existence clauses need not be satisfiable; only the square semantics is used here.

The mismatch sentence existentially quantifies six sets D,E,T,R,X,Y and uses the FO matrix asserting:

- Diag+(D), Diag−(E), Row(T), Row(R), Col(X), Col(Y);
- there exist a,b with T(a)∧D(a)∧X(a) and T(b)∧E(b)∧Y(b);
- there exist u,v with R(u)∧X(u), R(v)∧Y(v), and different input bits at u,v.

The row T chooses an index j: its intersections with D,E lie in columns j,n+1−j, so X,Y are exactly those columns. R then selects a row i in which they disagree. Conversely, any nonsymmetric picture supplies these six sets. Thus the sentence defines Sq\Mirror and belongs to Σ_1. In an odd square the central column pairs with itself and cannot give a spurious mismatch.

### 4.2 Mirror is not EMSO definable on Sq

We use one established theorem: on pixel pictures EMSO languages are exactly projections of finite local tiling languages (Giammarresi–Restivo–Seibert–Thomas; also Theorem 2.5/2.6 of Grandjean–Olive–Richard). The cited preprint uses cyclic successors with boundary predicates. For the direction used here, replace H(x,y) by succ_h(x)=y ∧ ¬Right(x), and similarly for V. This turns any EMSO sentence in our nonwrapping adjacency signature into an EMSO sentence in that source’s signature, with the same set prefix. Its recognizability theorem therefore supplies the needed tiling presentation; no converse FO definition of wraparound is required.

Fix a tiling presentation using a finite lift alphabet Γ, allowed 2×2 blocks on bordered pictures, and a letter projection. Domino presentations are a special case, or can be converted by finite blocking.

Suppose an EMSO sentence agreed with Mirror on every square. Its corresponding tiling system may do anything on nonsquares; this will not matter. Let g=|Γ|. For an even side n=2r and every binary n×r array A, the square P_A=[A | reverse_columns(A)] is symmetric. Choose one accepting lift Q_A over Γ.

Record, as the signature of Q_A, its two columns adjacent to the central cut (columns r and r+1). There are at most g^{2n}=g^{4r} such signatures, whereas there are 2^{nr}=2^{2r²} choices of A. Choose r>2 log_2 g, so the latter number is larger. Distinct A,B have identical signatures.

Form Q by the first r columns of Q_A followed by the last r columns of Q_B. Every 2×2 block not crossing the cut appears in one original accepting lift. Every block crossing the cut also appears there, because both boundary columns match the recorded signature. The same applies to blocks touching the top/bottom border; the exterior border symbol is fixed. Hence Q is accepted.

Its projection is [A | reverse_columns(B)], which is not symmetric because A≠B. It is still a square. This contradicts agreement with Mirror on Sq. ∎

### Corollary 4

On binary square pictures, Mirror∈Π_1\Σ_1 and Sq\Mirror∈Σ_1\Π_1. Since a dummy leading existential set quantifier places Π_1 in Σ_2, we have Σ_1(Sq)⊊Σ_2(Sq), and dually Π_1(Sq)⊊Π_2(Sq). Domain monotonicity gives the same strict adjacent-level separation on every B(C,d).

**Conclusion and exact gap.** This is a genuine complete proof of a known partial result, and the strongest unconditional separation established here. It supplies no Σ_3\Σ_2 witness. A lower-level accepting lift can be cut and pasted once; an alternating sequence of quantified sets requires preserving the responses to adversarial assignments, not merely one accepting lift. No such invariant was found.

## 5. Attempt 4: iterate Boolean combinations and projections

**Mechanism:** bootstrap the first-level mirror separation into arbitrarily many levels by iterating complement, conjunction, and disjunction, then adding color projection.

### Proposition 5 (Boolean closure cannot by itself climb arbitrarily high)

Every finite Boolean combination of EMSO sentences lies in Σ_2∩Π_2.

**Proof.** Put a Boolean combination in disjunctive normal form. In any conjunction, each positive term is ∃U_i α_i and each negated term is ∀V_j β_j, with FO α_i,β_j and pairwise fresh bound variables. Pull the existential variables first and the universal variables second. The matrices do not contain other terms' bound variables, so this preserves the conjunction. This gives Σ_2. Finite unions of Σ_2 sentences are Σ_2: combine independent existential blocks and independent universal blocks; for a disjunction, universal counterexamples to both disjuncts exist exactly when each separately has a counterexample. Empty blocks are permitted by dummy quantifiers. Applying the same argument to the complement, itself a Boolean combination of EMSO sentences, gives Π_2 as well. ∎

Consequently arbitrary fixed Boolean nesting of the mismatch language, its complement, and other EMSO languages cannot witness a separation above this bound. First-level non-complement-closure alone is fully compatible with the possibility MSO=BΣ_1. The OPG discussion explicitly presents that possibility; it does not establish it.

A color projection is existential monadic quantification. If BΣ_1 were closed under all such projections, uniformly over finite alphabet expansions, it would be closed under complement, Boolean operations, and arbitrary monadic quantification. It would then contain every monadic-prenex sentence, and hence give MSO=BΣ_1. The induction starts from FO⊆EMSO and follows the monadic prefix from inside outward. Conversely, MSO=BΣ_1 would imply this closure.

**Conclusion and exact gap.** The bootstrapping proposal is blocked exactly at existential projection of a Boolean combination: neither its closure in BΣ_1 nor a counterexample escaping BΣ_1 was proved. For a full strict hierarchy one needs unbounded level lower bounds, not just failure of one closure property. Proposition 5 is a proven limitation of the Boolean-only route, not a collapse theorem for MSO.

## 6. Attempt 5: alternating-computation encodings

**Mechanism:** import alternation separation from computational complexity by encoding a deterministic verifier and alternating witness strings in square pictures. The following conditional connection explains both a valid route and its missing hypothesis. This connection is standard in spirit; no novelty is claimed.

For this section define Σ_k^P through k alternating polynomial-length bit-string blocks, beginning existentially, followed by a deterministic polynomial-time verifier. Complements define Π_k^P. Reductions are ordinary polynomial-time many-one reductions.

### Proposition 6 (data-complexity upper bound)

For a fixed Σ_k MSO sentence, its truth on explicitly encoded N-cell pictures belongs to Σ_k^P.

**Proof.** Guess/universally choose the characteristic vector of each quantified set, N bits per set, according to its block. There are a fixed number of sets. Evaluate the fixed FO matrix in polynomial time by brute force over its first-order variables. The exponent depends only on the fixed sentence. Reading the input, checking that its explicit format is square, or rejecting malformed encodings costs polynomial time and does not add a quantified block. ∎

### Proposition 7 (polynomial reductions into square Σ_k languages)

For each k≥1, every language in Σ_k^P polynomial-time reduces to the language of some fixed Σ_k MSO sentence on square pictures over a fixed finite alphabet. The alphabet and sentence can depend on the verifier and k, but not on its input. The alphabet can subsequently be reduced to binary by fixed-size block coding, as detailed below.

**Proof.** Let a verifier for L receive x and k witness strings of polynomially bounded, padded lengths. Replace it by a deterministic one-tape machine with a polynomial running bound, halting states made absorbing. Its bounded computation is a two-dimensional local tableau: rows are time, columns are tape cells. A finite cell-state alphabet records tape symbols and, in at most one cell, the head and machine state. A next-row state depends on three adjacent previous-row states, with separate finite boundary cases. Define a total local rule on invalid triples arbitrarily; starting from a legal initial row the simulation remains legal and deterministic.

Given x, choose a polynomially bounded square side t large enough for the initialized tape and at least one more than the running bound, plus any simulation overhead. Construct a t×t input picture: the top row contains x, delimiters, and k tagged regions of witness positions, followed by blanks; all other input cells are blank. This construction uses polynomially many cells and is computable in polynomial time. At the left boundary use a standard one-sided-tape simulation. The machine never reaches the right boundary for this choice of t.

Quantify sets X_1,...,X_k with the alternating prefix. Only membership at top-row positions tagged for the corresponding witness is read. Thus all bit strings of the prescribed lengths are quantified, and irrelevant membership elsewhere has no effect. The top-row cell-state symbols are a fixed local function of its input letter and the relevant X_i bit, with the initial head at the leftmost cell.

Use one extra set T_s for each member s of the finite cell-state alphabet. The FO formula Valid(T,X) asserts: exactly one T_s holds at each cell; the top row is the prescribed initialization; and every adjacent pair of time rows obeys the finite local transition table. A finite disjunction over allowed constant-size patterns expresses each transition. A triple of neighboring cells and the corresponding next-row cell can be named with H,V. Missing-neighbor boundary cases use Left/Right. By induction over time rows, for every assignment to the X_i there exists exactly one valid tuple of sets T. Let Accept(T) assert that an accepting machine state appears in the last row. Absorption ensures it represents the verifier's final answer.

If the last block is existential, put all T_s in that block and use Valid(T,X)∧Accept(T) as the FO matrix. If it is universal, put all T_s in that block and use Valid(T,X)→Accept(T). In the universal case, invalid tableaux satisfy the implication and the unique valid tableau enforces exactly the verifier's answer. Hence neither parity costs an extra block. The result is a Σ_k sentence accepting the constructed square exactly when x∈L. ∎

### Binary coding detail

For a finite input alphabet of size a choose ℓ=max(1,ceil(log_2 a)) and c=2ℓ+8. Replace each original cell by a c×c binary block. All pixels are 0 except a 3×3 ring

111 / 101 / 111

in rows and columns 1,2,3, and the ℓ code bits in row 6, columns 2,4,...,2ℓ. The ring's center is a unique FO-recognizable marker. Payload bits are isolated. The zero strips between neighboring blocks separate their nonzero regions, and no other 3×3 ring exists. The marker centers form a grid with each successor at distance c, which is FO definable by a fixed H- or V-path. Each original letter is read at fixed offsets from its marker. A c t×c t square remains square.

Relativizing first-order variables to markers and replacing original predicates by these fixed FO formulas translates each Σ_k sentence to Σ_k over binary pictures. As with Proposition 2, restriction of a monadic set to marker cells is surjective and preserves both quantifier polarities. The reduction only produces valid encodings, so no global recognition theorem for all valid code pictures is required. The translated sentence may accept arbitrary other binary pictures without affecting reduction correctness.

### Conditional consequence

If Σ_k(Sq)=Σ_{k+1}(Sq), then Σ_k^P=Σ_{k+1}^P: reduce any language in Σ_{k+1}^P to its square-picture sentence by Proposition 7, replace that sentence by a Σ_k equivalent, and apply Proposition 6. This argument works over binary pictures by the block coding. Therefore strictness of the polynomial hierarchy at every level would imply strictness of the square-picture hierarchy, and hence of every fixed balanced superdomain considered above.

**Conclusion and exact gap.** This is a conditional reduction, not an unconditional resolution. No polynomial-hierarchy separation was proved. Its converse is not asserted: logical expressiveness can distinguish languages of low data complexity, as the mirror example itself illustrates. Thus this route does not prove that the balanced-picture problem is equivalent to separating the polynomial hierarchy.

## 7. Finite computation cannot certify the missing hierarchy result

For any fixed size cutoff B there are finitely many binary pictures with at most B cells. Every subset of that finite universe is FO definable by the atomic-diagram construction in Section 2. Thus empirical equivalence or inequivalence on bounded pictures cannot establish unbounded MSO alternation separation. Controls in this package test the explicit diagonals, mismatch certificate, exact counting inequalities, quantifier-restriction semantics, Boolean certificate parity, and block-code interpretation. They are not proof certificates for the whole hierarchy and do not search all MSO formulas or all tiling systems.

## 8. What remains

The unresolved obligation is an unconditional separator at each arbitrary level on one fixed balanced domain, with quantified-set responses handled uniformly in unbounded picture size; alternatively a proof of collapse under the exact pixel vocabulary. Neither a Σ_3\Σ_2 square separator nor a square collapse is established here. The polynomial-balance variants are likewise unresolved. No conclusion about the absence of a later or unindexed solution follows from this bounded literature search.
