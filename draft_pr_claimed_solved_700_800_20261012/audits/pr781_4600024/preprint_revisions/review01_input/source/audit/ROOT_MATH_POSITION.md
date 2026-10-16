# Root mathematical position: prescribed block-code extension

Recorded 2026-10-16; problem4600024, PR781 immutable head4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f. This is verification of the frozen candidate, not an additional proof-search turn. Original budget remains3/5. Provisional completion35%; the independent families and full reproduction remain required.

## Exact claim and evidence boundary

The input is a finite labelled presentation of a nonempty two-sided irreducible sofic shift T over a finite alphabet, and a specified onto block map f:T→T with a given finite local rule. The source assumes mixing, which implies the irreducibility used here. The claim is a terminating criterion for whether this same map extends from an SFT containing T, with equality of shifts allowed. It does not quantify over all possible self-maps, supply a limit-set presentation for an arbitrary cellular automaton, or decide stability from a CA rule alone.

For any fixed completion F of the given local rule to the full shift, let L=L(T) including epsilon and B={w:F_*(w)∉L}, with empty output before a full input window is available. Given any common finite recognizing monoid M for L and B, put k=4(|M|+1) and N=max(2,ell,k). The proposed criterion is L(T[N])∩B=empty. On yes, T[N] and F are witnesses, with F(T[N])=T by the promised onto property. On no, every extension radius and every completion of the specified map is excluded.

The sole non-elementary imported theorem is the published Place–van Rooijen–Zeitoun LT-separation bound, not an empirical extrapolation. The candidate's new mathematical step is the reduction and saturation argument. Neither executable controls nor a hash inventory formally verify the infinite theorem or the imported theorem.

## Independent root derivation and failure tests

1. A finite presentation may be reducible even when its label shift is irreducible. Delete vertices without an infinite past or future. Every surviving finite path then extends on both sides, so using all retained vertices as initial and final recognizes precisely L. Determinization, including the empty subset, gives a complete DFA. Do not require the supplied graph to be strongly connected.

2. The output-buffer construction remembers at most ell−1 letters and a state of this language DFA. It emits one letter for each complete ell-window. All words shorter than ell have empty output and are excluded from B. Thus B is effectively regular. For any surrounding words u,v, F_*(w) occurs contiguously inside F_*(uwv); factoriality of L proves B is a two-sided ideal. This is a semantic argument, independent of how a nonminimal DFA happens to encode rejection.

3. Irreducibility connects any two length-(n−1) words inside T, so the canonical overlap graph is strongly connected for every n≥2. This, rather than a compactness stabilization assumption, makes every finite graph path extend to a bi-infinite point. Its appended-letter path labels recognize the whole finite language: missing initial context is supplied by an infinite backward extension. Short words occur exactly when they occur in T. Treating the empty collection of n-factors of a short word as automatic acceptance would be wrong; the proof explicitly avoids it.

4. If G:S→T extends f from an SFT, restrict S to the original alphabet if a larger one was used. A finite forbidden list for S and a common finite coordinate interval for F,G give one sufficiently large n with T[n]⊆S and F=G on T[n]. Agreement on T alone does not give agreement on the full shift; agreement on every common-window word of T[n] does. This proves the fixed-completion reduction, including arbitrary larger radii. Conversely any successful T[n] is an SFT witness.

5. F(X)⊆T iff L(X)∩B=empty for every shift X: a forbidden finite output block has a finite input window and conversely. This quantifies over all finite lengths. No bounded witness search is substituted.

6. A successful canonical witness gives an LT separator because its language is defined by finitely many forbidden n-factors with finitely many explicit short-word exceptions. This does not assert that arbitrary sofic languages or arbitrary graph languages are locally testable.

7. For the converse, suppose an LT[k] separator C exists and a bad word w occurs in T[n], n≥max(2,k). Irreducibility produces a long U in T containing every allowed n-word. Join U,w,U in T[n] to obtain W; the ideal property retains badness. Separately join U,U in T to obtain V. Both words have exactly L_n(T) as their n-factor sets and share long initial/final U. Every k-word of T extends to an n-word, so their k-factor sets coincide too. Their full k-profiles are length-k factors split after floor(k/2) symbols. Left/right truncated profiles depend on the same endpoint words. Both are long enough to prevent a profile truncated at both ends. Thus V and W have equal published profile sets, contradicting separation. The separator itself need not be factorial. Omitting padding, or comparing factors alone without endpoints, would invalidate this argument.

8. A single transformation monoid of disjoint complete DFAs, with identity and composition in reading order, supplies the common recognizing morphism required by PRZ. Minimality and surjectivity onto the ambient monoid are not required by the cited statement. The finite theorem supplies exactly this k, so saturation removes the unbounded positive semidecision. Taking N≥ell is harmless, though saturation itself does not need that extra inequality.

9. The final computation is finite reachability in a product graph, not a fixed cutoff on word lengths. Enumerating the generated transformations, all length-N words, overlap graph and product state space terminates even if impractically large. A bad product path is only a witness at N by itself; the previous equivalences, including PRZ, are essential for the all-radius negative conclusion. No efficient implementation is claimed by the finite-control scripts.

10. Onto is used only for equality of the final image with T; the inclusion criterion works for a specified non-surjective block self-map too. An automorphism on a non-SFT cannot satisfy it: extend its inverse locally and use the composition identity on a sufficiently fine successful neighborhood to force T=T[n]. The even-shift identity therefore supplies the claimed infinite negative family. A constant map to a fixed point is a positive inclusion control but fails the onto hypothesis. These are distinct cases.

## Actual primary-source inspection

The root freshly obtained the two PDF bodies in memory, checked their PDF headers and full SHA256/byte counts, extracted text, and rendered the actual cited pages. Boyle's printed17 confirms the prescribed-map question and adjacent, different16.1/16.2. PRZ printed4–6 supplies finite words/profiles/LT; printed8 contains Theorem4.2 with k=4(|M|+1), visually inspected, with its continuation on9. The theorem's full general proof is relied on as published, not independently reproved. Matching historical source hashes supports version identity, not current openness or novelty. Original source PDFs and copied extracts are not retained in the authored package.

## Pending falsifiable gates

Two fresh independent families must test the automata/LT and symbolic-dynamics arguments without reading peers before their initial positions. Root must finish the exact original-package replays and inspect their closed artifacts. If these pass, a separate in-depth priority audit follows. In particular, Ballier's steadiness literature and later extensions must be compared against the full specified-map criterion. No publication or merge is authorized by this provisional mathematical position alone; the user's complete review/publication process remains to be carried out.
