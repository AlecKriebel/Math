# Independent universal derivations and exact controls

The mechanisms were fixed in the substantive early ledger before foreign primary bodies. This expanded reconstruction verifies the whole original theorem, while identifying the published separation result as an imported input. Finite controls supplement these deductions.

## D1. Regularity, ideal closure and effective data

For a nonempty two-sided sofic T, its language L includes epsilon, is factorial and prolongable, and is effectively regular. From a finite labelled presentation one can retain finite paths with infinite past and future using finite reachability to/from cycles, then determinize and complete an automaton for L.

For a local rule of length ell=a+b+1, a finite transducer keeps up to ell-1 input letters and the L-DFA state after emitted outputs. This recognizes B={w:F_*(w) notin L}; a word shorter than ell emits epsilon and is not bad. Memory/anticipation only locates the output's central coordinates and does not change consecutive-window output order.

For bad w, |w|>=ell. Every ell-window internal to w remains internal to uwv, so F_*(w) is a factor of F_*(uwv). Factoriality of L makes B a two-sided ideal. If w is allowed, choose its occurrence in x in T; its output is a factor of f(x) in T. Hence L and B are disjoint, without onto.

The transformation induced by a word on the disjoint union of complete L/B DFAs determines acceptance in both components. Enumerating the transition monoid therefore supplies a common recognizing morphism alpha:A*→M. It need not be syntactic or minimal. These are terminating finite constructions.

## D2. Normalization covers all radii, completions and alphabets

Suppose G:S→T extends the prescribed f and S is an SFT containing T. If its alphabet is larger than A, intersect with A^Z; forbidding the new symbols preserves finite type and containment. Let n be at least2 and at least the length of every word in a finite forbidden list for S. Those words are absent from T. If x in T[n] contained one, extend its occurrence inside x to an n-block: that allowed n-word would contain a word absent from T, a contradiction. Thus T[n] is included in S. An empty forbidden list is harmless; epsilon cannot be forbidden because S is nonempty.

Put the F and G rules on a common finite interval I. They agree on every I-word occurring in T because both restrict to f. Increasing n to at least |I| makes every I-window in T[n] a factor of an allowed n-word. Therefore F=G on T[n]. Consequently an extension exists iff the chosen F maps some T[n] into T. Conversely such an approximant and F provide an extension directly. This quantifies over all competing completions, radii and containing alphabets; it is not a bounded search for candidate rules.

## D3. Exact bad-word equivalence and onto

If w in Lang(T[n]) is bad, its forbidden output appears in F(x) for an occurrence in x in T[n], so F(x) is outside T. Conversely, if F(x) is outside T, it has a finite forbidden block z. The finite input interval producing z has length |z|+ell-1, occurs in x and is bad. Thus, for every n,

    F(T[n]) included in T iff Lang(T[n]) intersects B trivially.

No onto assumption is used here. For the specified onto f, T included in T[n] implies T=F(T) included in F(T[n]), so inclusion implies equality. This is the only use of surjectivity. The constant binary full-shift code extends from the full shift but has a singleton image; equality without onto would fail.

## D4. Exact approximation language and local testability

For n>=2, let H_n have vertices L_(n-1) and edges L_n, an edge joining its prefix to its suffix and labelled by its final letter. Given vertices u,v, irreducibility supplies an allowed u c v, whose successive n-blocks form a path from u to v. H_n is strongly connected; mixing and aperiodicity are unnecessary.

A word of length>=n with all n-factors allowed gives a finite path. Cycles and connectivity extend its ends bi-infinitely, so it occurs in T[n]. For a shorter word, occurrence in T[n] implies being a factor of an allowed n-word and hence membership in L. Conversely every short L-word occurs in T included in T[n]. Thus Lang(T[n]) tests allowed n-factors for long words and handles finitely many short words separately. It is LT: long-word tests are finite Boolean combinations of factor-presence predicates, as is length>=n; finite languages are LT. A successful normalized witness therefore gives the desired LT separator.

## D5. Exact published LT interface

In the actual final LMCS body, Place–van Rooijen–Zeitoun Theorem 4.2 states that regular languages recognized by a common finite monoid morphism are LT-separable iff they are LT[k]-separable for k=4(|M|+1). The additionally named common NFA exists here, for example the DFA disjoint union. Neither a syntactic monoid nor an onto morphism is required.

Its positions are 0<=i<|w|. Put l=floor(k/2), r=k-l. The position profile is

    (w[max(0,i-l):i], w[i:min(i+r,|w|)]).

LT[k] languages are unions of classes with equal profile SETS: the threshold is1, with no multiplicity constraint. These exact hypotheses, convention and constant were read independently after the early seal. The general algebraic separation proof is imported, not reproved or purportedly verified by finite examples.

## D6. Full saturation, including short words and overlap details

Let C in LT[k] contain L and avoid B, with n>=max(2,k). Suppose a bad w occurs in T[n]. Construct U in L containing every word of the finite nonempty L_n by repeatedly joining allowed words using irreducibility. Extend it until |U|>=n+k, possible by a bi-infinite occurrence.

U is a path label in H_n: precede an actual occurrence by its(n-1)-block. The word w is also a path label, even if shorter than n. Connect U's ending vertex to a chosen starting vertex for w by a path labelled c; after w, connect to a starting vertex from which U can be read by a path labelled d. Concatenating path labels gives the literal word W=U c w d U in Lang(T[n]), with no silent overlap convention. The ideal property makes W bad. Separately choose e by irreducibility so V=U e U is in L.

Both words contain every L_n word because U does, and no extra n-factor: V is allowed and W is in Lang(T[n]). Their k-factor sets both equal L_k. There are no extra k-factors since k<=n; every allowed k-word prolongs to an allowed n-word already present in U. Both words start/end with U, hence have identical(k-1)-prefixes and suffixes.

Full profiles correspond to k-factors split after l letters. Any profile truncated on the left is determined by a prefix of length at most k-1, and one truncated on the right by such a suffix. Both word lengths exceed2k, excluding double truncation. Thus their entire profile sets agree. Since V is in L included in C and C is a union of profile classes, W is in C, contradicting W in B.

Therefore Lang(T[n]) avoids B for every n>=max(2,k). This proof handles every bad-word length, arbitrary period and every local-rule window; it does not sample a finite language cutoff.

## D7. Complete equivalence and finite reachability

An extension implies a normalized successful T[n] by D2, and hence an LT separator by D3/D4. D5 yields an LT[k] separator; D6 gives avoidance at N=max(2,ell,k). D3 and onto give F(T[N])=T, whose restriction provides the required extension. This closes all four implications.

Enumerate H_N and mark every vertex initial and final. Every finite path extends bi-infinitely, so its label belongs to Lang(T[N]). Conversely, an occurrence of any finite word in T[N] can be read after its preceding(N-1)-block. Thus this finite automaton recognizes the exact language, including short words and epsilon. Its product with a complete B-DFA accepts precisely the intersection. Initialize every overlap vertex paired with the B-DFA start state. Finite reachability of a B-accepting pair decides emptiness and terminates without a guessed word-length bound.

This is a terminating arbitrary-input specification, not an implementation or a useful complexity estimate. M, N and H_N can be enormous. Failure rules out every alternative extension by D2 and the established equivalence, not by finitely testing alternative rules.

## D8. Universal edge and negative controls

If T is SFT, S=T is permitted and works for any onto self-code. If an automorphism f is steady, let g be its block inverse, with an arbitrary rule completion. The composite identity gF=id on T holds on every sufficiently large T[n], because it is a finite-window identity. D2 also gives image inclusion for every sufficiently large approximant. Choose n satisfying both. Every x in T[n] then equals g(F(x)) in T, so T=T[n] is SFT.

For the even shift use E--0→E, E--1→O, O--1→E. The graph is strongly connected and has a loop, hence the shift is mixing. Odd-gap words0 1^m 0 are minimally forbidden with unbounded lengths, so it is not SFT. For every n choose odd m=2n+1. The point(0 1^m)^infinity is outside T, but each n-block has at most one zero and is allowed. Thus it belongs to T[n]. This proves the identity obstruction for every n; selected computed periods are only diagnostics.

Finite irreducible periodic orbits are SFT and do not challenge the irreducible/nonmixing scope. Nonemptiness ensures L_n and H_n are nonempty; unused alphabet symbols are handled by completion and the canonical languages. For the reducible shift consisting of0^infinity and1^infinity, L=0* union1*: no allowed word contains both00 and11. This diagnoses the failure of a global U across components, without claiming a counterexample to a reducible generalization.

## D9. Reproducible finite evidence and its scope

The inspected own controls.py performed36 checks. For(n,k)=(2,2),(3,2),(3,3),(4,3),(4,4), finite graph/subset-state breadth-first searches construct actual U,c,d,e,V,W, retained in CONTROL_RESULTS.json. Searches explore finite reachable states rather than a guessed connector-length cutoff. Each V is allowed, W is bad but locally allowed, and profile sets agree while multiplicities differ. The latter would catch an illicit counting-based LTT substitution. The pair010/101 illustrates why equal factors alone do not ensure equal profiles without endpoints.

An actual-bound positive case uses T={0^Z} in alphabet{0,1} and identity completion. The common recognizing monoid consists of identity and constant-dead transformations, so k=N=12. Its actual canonical overlap graph has a single0-edge; the B-DFA product has no accepting reachable state. Five finite odd-gap periods illustrate D8. None of these finite computations proves the universal PRZ bound or all shifts/radii.

## D10. Strongest surviving result and limits

The complete original Theorem 1, saturation lemma and stated controls survive. The exact imported result is verified at its primary interface and credited. The paper does not claim new general separation machinery, historical firstness, existence-over-all-maps, arbitrary reducible steadiness or cellular-automaton stability. Exact priority remains unknown, particularly with the unacquired Barth–Dykstra and final Ballier journal bodies. No substantive mathematical defect or indispensable gap was identified.
