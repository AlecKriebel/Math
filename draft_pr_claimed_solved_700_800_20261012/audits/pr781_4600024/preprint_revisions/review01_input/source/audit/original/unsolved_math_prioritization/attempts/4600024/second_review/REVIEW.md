# Second adversarial review of the prescribed block code extension criterion

## Disposition

PASS. The claimed equivalence and computable bound are valid for a nonempty two-sided irreducible sofic shift T and a specified surjective block map f:T→T, assuming the explicitly credited published separation theorem. No mathematical correction to the frozen proof is required. In particular, the saturation step compares the exact finite-word profiles, including boundary profiles, and the negative outcome rules out extensions of every radius.

This is an independent AI mathematical review, not formal verification or human peer review. It establishes no novelty, priority, or current community consensus about the historical problem. The published separation theorem is used as an external theorem, not independently reproved.

The reviewed author archive has SHA-256 5775d3247c3a368945025a74975e6498c26ae0755e1138ccc33ff639c47257ef (15,624 bytes). The prior independent audit archive has SHA-256 35396a4ad2a774484bd35f92a782bb2a27ff6af0f670e388bb6ff8ab43331be9 (32,106 bytes). Both remain unchanged.

## Exact target and source check

Boyle's Problem 16.3 fixes a surjective self-code of a mixing sofic shift and asks for an SFT containing that shift from which the code maps into the original shift. The same page separately poses the existential-over-code question with an additional receptive fixed point assumption in Problem 16.2. These targets must not be merged. The wording in 16.3 permits equality of the containing SFT and T. The source page was freshly rendered and visually checked during this review. [Boyle, Open Problems in Symbolic Dynamics, printed page 17](https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf).

The supplied full catalog and both full corpora independently match their published byte counts and hashes. Reselecting ID 4600024 gives rank 820 and AMR-045-0024; re-encoding its complete problem record together with the associated report reproduces the 3,101-byte review hash. This validates identity, not any claim that the historical open-status label remains current.

## Independent reconstruction of the proof

### 1 The problem is a language sandwich problem for a fixed completion

Let A be the alphabet of T. Fix a full-shift completion F of the prescribed local rule, with input window length ell. For a finite word w, apply the rule to each complete ell-window to obtain F_*(w), taking the empty word when |w|<ell. Let L=L(T), including the empty word, and let B consist of w for which F_*(w) is outside L.

A finite automaton recognizes L: trim the labelled presentation to its bi-infinite part, use all remaining vertices as both starting and accepting states, and determinize. Every finite path in this trimmed graph extends left and right. The graph itself need not be strongly connected even when its presented shift is irreducible; the argument does not make that assumption.

A finite buffer of at most ell−1 letters, together with the state of the automaton for L, recognizes B. No output is produced before a full window has arrived. Thus the empty word and every input word shorter than ell are correctly excluded from B. Since L is closed under taking factors, forbidden output words remain forbidden after surrounding input is added. Consequently B is a two-sided ideal and L∩B is empty.

For any shift X over A, F(X)⊆T is equivalent to L(X)∩B being empty. A forbidden output block has a finite input preimage window, and every bad word occurring in X produces a forbidden output block in the corresponding point. This statement has no finite witness-length cutoff.

Suppose a possibly different block map G:S→T extends f, where S is an SFT containing T. Intersect S with A^Z if necessary. Choose n large enough to dominate a finite forbidden list for S and a common contiguous coordinate window for F and G. All words in that common window which occur in T[n] then occur in T. Hence T[n]⊆S and F=G on T[n]. This yields F(T[n])⊆T. The converse follows by taking S=T[n]. Thus choosing the fixed completion loses no possible larger-radius extension.

### 2 Canonical approximation languages really are locally testable

For n≥2, use vertices L_(n−1)(T), edges L_n(T), and the usual overlap incidence. Irreducibility of T joins any two vertex words inside L and therefore makes this overlap graph strongly connected. Finite paths extend to bi-infinite paths. In particular:

- L_n(T[n])=L_n(T).
- A word w with |w|≥n occurs in T[n] exactly when every n-factor of w lies in L_n(T).
- A word w with |w|<n occurs in T[n] exactly when w∈L(T).

The last clause is essential: short words are not admitted by a vacuous universal condition. Their occurrence in an n-block proves the necessity; occurrence in T proves sufficiency.

The language described by these clauses is locally testable. It is obtained by forbidding finitely many factors, together with finitely many short-word corrections. Hence any successful canonical approximation provides an LT separator of L and B.

### 3 Exact saturation lemma with no factoriality assumption on the separator

Let C be an LT[k] separator of L and B under the published profile definition. Choose n≥max(2,k). Suppose w∈B∩L(T[n]).

First choose U∈L of length at least n+k containing every n-word of T. Irreducibility lets us concatenate a finite enumeration of those words, then extend if needed. Every n-word has an occurrence in U, regardless of connecting words.

Using irreducibility of T[n], join U to w and then the entire joined word to a second U. This produces W=UcwdU∈L(T[n]). Since B is a two-sided ideal, W∈B. Separately join U to itself in T to obtain V=UeU∈L.

Both words have exactly L_n(T) as their n-factor set: all factors are allowed, and U supplies all of them. Since every k-word of T extends to an n-word, both have exactly L_k(T) as their k-factor set. Both also have the same first and last k−1 letters, supplied by U.

Here is an explicit check of the boundary issue. Put l=floor(k/2) and r=k−l. At a position i of a word z of length at least 2k, its profile consists of the preceding min(l,i) letters and the next min(r,|z|−i) letters including position i. Its profile set decomposes into:

1. Full profiles: each k-factor v contributes (v[0:l],v[l:k]).
2. Left-truncated profiles: positions i=0,...,l−1, completely determined by the first k−1 letters.
3. Right-truncated profiles: positions |z|−t for t=1,...,r−1, completely determined by the last k−1 letters.

There is no position truncated on both sides at these lengths. These statements also cover k=1, when the two truncated lists are empty. Thus V and W have exactly the same published profile set. Their lengths can differ, and profile multiplicities need not match; neither matters for LT[k].

Because V∈L⊆C and C is a union of profile-equivalence classes, W∈C. This contradicts W∈B. Therefore an LT[k] separator implies B∩L(T[n]) is empty for every n≥max(2,k).

This reasoning never requires C to be closed under factors or concatenation. Padding is performed in the shift languages, and the ideal property is used only for B. Equal factor sets without boundary information would not suffice: 0010 and 1001 have identical two-factor sets but different 2-profile sets.

### 4 The published bound applies to the proposed common monoid

Take complete DFAs for L and B on disjoint state sets. Letter transitions preserve each component. Generate their finite transformation monoid, including the identity, and let alpha map each word to its state transformation. With multiplication taken in reading order, alpha is a monoid morphism. Evaluating at each component's start state shows that this same morphism recognizes both languages. Minimality is unnecessary.

The required external implication is precisely that LT separability of languages recognized by a common finite monoid M yields an LT[k] separator with k=4(|M|+1). The definitions include words in A*, the empty word, and profiles at letter positions. The published theorem and its surrounding definitions were inspected; printed page 8 was freshly rendered. [Place, van Rooijen and Zeitoun, Theorem 4.2](https://lmcs.episciences.org/1163/pdf), [published identity](https://doi.org/10.2168/LMCS-10(3:24)2014).

Set N=max(2,ell,4(|M|+1)). Sections 1–3 now prove that an arbitrary extension exists if and only if B∩L(T[N]) is empty. Surjectivity of the prescribed f gives T=f(T)⊆F(T[N]), so the successful inclusion is equality. Surjectivity is not needed for the underlying inclusion/existence test; it is needed for the equality assertion.

### 5 Decidability and the negative certificate

The complete finite automata, generated monoid, integer N, and overlap graph can all be constructed by terminating finite procedures. Enumerating the transformation monoid is finite even when prohibitively expensive.

Label each overlap edge by its appended symbol and use all graph vertices as starts and ends. This graph recognizes L(T[N]), including its short words: every labelled path extends backward to provide the omitted initial context, and any finite point block has such a path. A product with the bad-word DFA decides emptiness by graph reachability.

An accepting product path gives a finite word in B∩L(T[N]); the strong connectivity supplies a bi-infinite input extension. This alone would ordinarily only disprove the chosen radius. The all-radius conclusion additionally uses the proved implication: any successful radius, completion, or extension would give an LT separator, and the imported bound plus saturation would force success at N. Therefore a failure at N excludes every such extension. No stabilization of the descending approximation sequence is assumed.

## Challenges that did not reveal a gap

The proof correctly handles a larger ambient alphabet, empty and short words, periods greater than one, unused alphabet letters, redundant reducible presentations of irreducible shifts, arbitrary local window offsets, and possible differences between two completions away from T. Mixing is stronger than needed; the concatenation arguments use irreducibility only. No assertion for arbitrary reducible shifts is accepted by this review.

For automorphisms, locally extend the inverse composition identity to a sufficiently fine canonical neighborhood. If the completed map sends that neighborhood into T, applying the inverse shows the neighborhood is contained in T, so T is SFT. Conversely equality is an allowed witness when T is SFT. This is consistent with the infinite family of identity obstructions on non-SFT modular shifts.

## Undecidability does not conflict with this input model

Di Lena and Margara state undecidability of stability for a given cellular automaton, and of several properties of its dynamics on its limit set. Their input is the CA rule; no finite presentation of the limit set is supplied. [Undecidable Properties of Limit Set Dynamics of Cellular Automata, Proposition 2.6 and Corollary 3.7](https://arxiv.org/pdf/0902.1441).

The reviewed procedure needs an explicit finite presentation of T. Applying it to a CA limit set requires obtaining that presentation and establishing that it is the limit set, steps the criterion does not provide. Nor does deciding the extension question for one supplied f decide whether any self-code exists: its bound depends on the supplied code, with no bound over all codes proved here. These distinctions remove the apparent contradiction. This is a scope comparison, not an exhaustive survey of undecidability results.

## Reproducible finite controls and integrity

Both original frozen verifier suites replayed successfully. They report 3,456 author mathematical checks, 221,468 first-auditor checks, and 32 first-auditor integrity controls. Their scopes remain finite.

The fresh checks in this packet are separately authored and report 22,859 checks. They include 19,116 exhaustive binary-word checks of the profile decomposition, 24 saturation cases for modular shifts of moduli 2–5 and approximation orders 2–7, short-word controls, an explicit factor-only countercontrol, a reducible presentation of an irreducible shift, and direct generation of a common monoid for even-shift identity. That monoid has seven elements, giving the published bound 32; a length-35 forbidden word has every length-32 factor allowed. These controls exercise the formulas and examples, not the universal separation theorem or a production implementation of the general decision procedure.

The release verifier rejects unlisted files, directories, symlinks, special files, hash mismatches, and malformed inventories before executing the checked source using isolated, bytecode-disabled Python. Ordinary and optimized execution must reproduce the stored results. An external archive hash remains the trust anchor; an unkeyed manifest does not defend against coordinated rewriting of the entire packet.

The deliverable contains only authored review, code, results, and public verification metadata. It excludes source PDFs, extracts, rendered source pages, corpus contents, and private coordination. No remote mutation, publication, or outreach was performed.
