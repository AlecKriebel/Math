# Independent review: mutation and unknotting number

**Verdict: PASS_SCOPED_PARTIALS_ORIGINAL_UNSOLVED_5_OF_5. No mandatory mathematical correction.**

This review binds to `FROZEN_MANIFEST_v2.json`, SHA-256 `cdaf035f9abf4bce476bc045b257af118adc8f7c0b0cee570505183bd488780c`, and the unchanged `RESULT.md`, SHA-256 `646dadaa9332a6449e6f930ad7f25bdfdce85b1db40c2784c084405ef4bcecf8`. The 46 bound artifacts include the original 42-entry freeze and the narrow deterministic-output correction. I did not contribute to the author routes or modify their proofs.

The approved claim is the collection of scoped results in all five turns. The original question about different ordinary unknotting numbers of Conway mutants remains unresolved in this packet. The exact alias is 2662(b); the connected-sum question 2662(a) is neither closed nor independently attempted here. No novelty assessment or new exact table value is certified.

## 1. Source and category

The original Ohtsuki page 538, Problem 12.15, was checked directly, including a rendered page. The 2026 Kirby list separates connected sum and mutation in Problem 1.3(a),(b). The category here is tame knots in the oriented three-sphere and ordinary single crossing changes. The topological cover arguments use the standard locally flat/smooth branched-cover and rational-tangle category. They do not apply to arbitrary wild actions, generalized untwisting or genus-two mutation.

Gordon–Luecke Theorem 7.1 was read with its full proof. Its exceptional EM-knot and EM-tangle arguments are essential; the author does not omit them or assume that every unknotting arc avoids the sphere. Theorem 8.2(2) and the supporting discussion supply the genuine failure of universal localization. Preservation of the unknot follows from the invariant double branched cover and the classical Smith theorem.

## 2. Marked distance and displayed diagrams

Turn 1's graph is a graph of marked pairs. Mutation transports each sphere-disjoint crossing ball, so it is an involutive graph automorphism. The target shell of number-one knots is invariant by the cited theorem. A marked tangle diagram admits finitely many descending crossing switches to the unknot; stopping before the first unknot proves finiteness of the distance to that shell. The inequality and defect subtraction then hold exactly as stated.

For the number-two subclass, transport gives an upper bound two, and reverse use of number-one invariance, together with unknot preservation, excludes zero and one. For larger numbers the same argument gives only an upper bound. The abstract graph in the packet correctly illustrates a logical possibility and is not presented as a realized knot graph.

Turn 4's full resolution cube is equivariant crossing by crossing, including half-turns that change the planar viewing convention. The zero and one Boolean predicates are preserved even when a resolved Conway sphere becomes inessential. Relabeling gives the cardinality and weighted-minimum consequences. Taking a minimum over all diagrams of the fixed marked pair is legitimate because mutation bijects that marked diagram class. Replacing it by all unmarked diagrams would be unjustified, and the packet does not do so. An EM example with no sphere-disjoint unknotting arc proves the stated strict gap `m(K,S)>u(K)`, while its mutant still has `u=1`.

## 3. Kim–Livingston family

The exact inverse/reverse conventions, Seifert matrix and threefold-cover character data agree with Sections 3–5 of the primary paper. The elementary polynomial is determined only up to a Laurent unit, including sign. The signature form has off-diagonal entry `3(1-cos(theta))-i sin(theta)`, so its two nonzero eigenvalues are opposite for every nontrivial unit-circle point. The two three-by-three presentation blocks each have determinantal divisors `(1,1,7)`, and the deck roots modulo seven are two and four.

The published choice of J depends on a fixed upper N and gives `g4(k L_J)=k` simultaneously for `k<=N`; the packet keeps that quantifier. To use only the given genus bound N against a smaller upper certificate would require at most N−1 crossing changes. The other knot has 2N nontrivial connected-sum factors, so such a certificate would contradict the separately stated summand lower-bound conjecture. This is a valid conditional implication, not an assumption that the conjecture holds. Componentwise sequences supply a common upper bound without proving additivity. Four-genus disparities alone do not settle ordinary unknotting numbers.

## 4. Marked-cover surgery equivalence

Both directions of Turn 3 pass with the **full equivariant pair and quotient marking** retained. Disjoint crossing balls in one diagram lift to disjoint strongly inverted solid-torus neighborhoods in the standard unknot cover. The original and switched meridians have distance two. Conversely, the prescribed standard strong-inversion neighborhoods and equivariant fillings have rational two-string tangle quotients.

There is a useful direct check of the crucial slope assertion. Choose signs of primitive vectors a,b so `det(a,b)=2`. Their reductions modulo two agree and are nonzero. The integer matrix whose columns are `(a-b)/2` and `(a+b)/2` has determinant one. It sends `(1,1)` to a and `(-1,1)` to b. Hence an orientation-preserving pillowcase marking simultaneously carries the two standard opposite crossings to the specified slope pair. Pulling back the crossing disk gives an ordinary crossing change within that ball; no change to the exterior quotient is required. The common mod-two reduction preserves the endpoint pairing. These statements apply in all disjoint balls simultaneously.

The final equivariant identification identifies the branch knot, not merely its cover manifold. An unmarked homeomorphism of mutant covers therefore does not transfer a certificate. No effective minimization algorithm or new obstruction for that equivariant surgery problem is asserted.

## 5. Final certificate, data and finite-type scope

Each of the three initial sign changes and ten subsequent braid macro moves was checked independently. The Artin moves are literal neighboring-generator relations, including the mixed relation. At each end destabilization the extreme generator occurs exactly once. Cyclic conjugation moves it to the end; the cyclic reorder of the remaining word is itself conjugate to the displayed next word. Each state has a one-component closure, and the final one-strand empty braid is the unknot. Thus the upper bound is rigorous for the specified braid. Its name is attributed to the pinned database rather than independently recognized.

The 865-group, 1841-member read-only join reproduces the author's sole differing interval pair and finds no disjoint displayed intervals. The two reference cells are blank. Kanenobu–Matsumura Remark 3.1 explicitly includes 11n76 among unreferenced values above its elementary bounds. These facts establish a provenance gap, not an erroneous entry, a certified lower bound or a mutant counterexample. The 55 exhausted restricted search graphs remain only those move graphs. The four Bernhard–Jablan knots are correctly treated as crossing neighbors rather than a supplied mutant family.

Stoimenow's Theorem 1.2 and final proof were checked in full primary text and rendered pages. Starting with a number-one representative, the construction preserves the bounded finite-type data, changes unknotting number upwards by at most one per stage, and has unbounded signature lower bounds. It therefore attains every positive integer. The author's universal lower-/upper-bound corollary follows. It does not preserve a fixed mutant family or extra geometric data, and does not constrain arbitrary infinite collections or full polynomial invariants.

## 6. Verification and publication boundary

- Every one of the 46 frozen author entries and all five historical turn manifests matched their hashes; all pinned primary input hashes matched.
- All deterministic author receipts, both data screens and the restricted search receipt replayed byte-for-byte. The historical turn-1 receipt matched as parsed JSON; its v2 replacement replayed byte-for-byte, exactly as documented.
- A separately written checker passed **18,461 exact assertions**, using direct simultaneous slope matrices, determinantal divisors, literal braid rewrites, all-pairs graph distances, Boolean-cube controls and an independent pinned-data join. No author checker was imported.
- During reviewer-checker development, an Alexander normalization sign was corrected in the reviewer code; the author's stated up-to-unit polynomial and checker were already correct. The final reviewer receipt is deterministic.
- Historical completion estimates, where present, are subjective author notes rather than calibrated probabilities. They play no role in this verdict.

Recommended final queue disposition: **unsolved, 5/5**, with a link to the reviewed partial packet. No unrestricted equality theorem, distinct-u mutant pair, table-error allegation, new exact lower bound or historical novelty claim is approved. Parent publication authorization remains a separate gate.
