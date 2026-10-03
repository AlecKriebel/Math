# Turn 2: unbounded low-minority-letter rigidity

2026-10-03 07:36 UTC. Substantive author turn 2/5. **NO FULL RESOLUTION.** Completion estimate: 6%, a planning estimate only.

## Proven proper-subfamily result

If the cyclically reduced representative of u contains at most four occurrences of b or b^-1 and those occurrences all have the same sign, every universally SL3-trace-equivalent v∈F2 is conjugate to u. The exponents of a may be arbitrary signed integers, so this result is not bounded by total word length. The same statement holds after exchanging generators or, more generally, simultaneously changing free basis by an automorphism.

Full derivation is in LOW_MINORITY_PROOF.md. Its first six sections prove the especially elementary ≤3 result; Section7 gives the four-occurrence extension. The extension is included in this turn's claimed partial result. No novelty claim is made.

## What makes the theorem apply to arbitrary companions

The argument does not assume that a potential companion has the same convenient format. It first recovers each unsigned cyclic letter count using a single fixed SL2 matrix C=[[2,1],[1,1]] and the Laurent degree in D(t)=diag(t,t^-1), embedded in SL3. In a maximal-block cyclic word the unique maximizing index choice has a product of nonzero C^p entries as coefficient. Signed exponent sums from Turn1 then recover the four positive/negative letter counts. Hence a companion really must have the same number and sign of b letters.

This recovers Horowitz's known letter-count restriction by a self-contained proof, with prior credit to Lawton–Louder–McReynolds §4.3 and the MEGL exponent investigations.

## Sparse substitutions and directed ordering

- Two occurrences: a determinant-corrected transposition matrix gives x^p y^q+x^q y^p+(xy)^(-p-q), determining the two gaps up to rotation.
- Three occurrences: a 3-cycle gives the cyclic orbit sum of the three gap exponents, modulo a common shift. The already-known exponent sum removes the common shift, including zero, repeated, and negative gaps.
- Four occurrences: extend to GL3, diagonalize A, and extract the coefficient of b11 b12 b23 b31 in the generic-B trace. It equals Σ_i x^(p_i+p_(i+1)) y^p_(i+2) z^p_(i+3). Given the total sum, this records the directed adjacent-pair multiset of the four gaps. The elementary equality-pattern case split proves that a cyclic sequence of length4 is determined by that multiset.

The logic is polynomial coefficient comparison on a dense open set, not an experiment with finitely many matrices. The finite checker is only a sanity check of this proof.

## Verification and exact remaining gap

check_turn_2.py uses standard-library exact Laurent arithmetic. It checks 6584 signed cyclic-word count cases (lengths1–7, both generator choices), 49 two-gap and343 three-gap formulas, all256 four-symbol length4 reconstruction patterns, and an explicit rational separated pair. See TURN_2_CHECK.json.

This excludes an infinite proper subfamily but leaves mixed-sign minority-generator words and general longer same-sign words. The automorphism extension does not establish that every word can be transformed into the covered family. Finite prior searches through length20 already appear in the literature; no search-bound improvement is claimed. Next turn: address mixed-sign two-occurrence words via adjugate coefficients, rather than merely expanding a brute-force search.
