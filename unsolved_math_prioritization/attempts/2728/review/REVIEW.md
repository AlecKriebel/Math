# Independent review: KP 1.69 Bennequin-sharpness obstruction package

## Verdict

**PASS_SCOPED_ACCOUNTING_AND_GEOMETRIC_GAPS.** No mandatory correction is required. The original converse remains **unsolved, 2/5**. The submitted work correctly credits known reductions and identifies the missing transverse surface construction and canonical-genus hypothesis. It contains no general proof or counterexample.

The frozen `OBSTRUCTION.md` SHA-256 is

`b40a0e54e88291f7e9fbd07d0798f2eb6da3a6c927115afee8fe2ea5e5c0ef3c`.

This is an independent adversarial AI review, not human peer review or a novelty certification.

## 1. Exact source and a newer primary-source check

I read [K3 Problem 1.69 and all remarks](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp.65–66, and visually inspected p.65. Its hypothesis uses a Seifert surface in S3 and sharpness of the ordinary Bennequin inequality for a transverse link in the standard contact structure. It has no fibered, braid-index, FDTC, or canonical-surface restriction. The neighboring four-ball/quasipositivity question is different. The artifact preserves these distinctions.

The [Stoimenow paper published 1 April 2026](https://ems.press/journals/prims/articles/14299640) was checked at Conjecture 2.5, Corollary 4.31 and Appendix B; p.258 was visually inspected. It still states the general converse as a conjecture, while treating canonically minimal links and reporting the finite prime-knot census. The artifact does not represent the census as independently reproduced.

During this review I found an even newer author preprint, [*Grid diagrams, link indices, and quasipositivity*](https://stoimenov.net/stoimeno/homepage/papers/epart3.pdf). The author's index labels it 24 September, but the retrieved complete PDF is dated **29 September 2026**, as verified visually on its cover. Its SHA-256 is `7e836723ffa3313db11b866b19dcd0ca2ce44194e6208fc5be8772b99ad7b87e`. The relevant introduction, Problem 2.5, definitions, Remarks 5.11 and 5.14, the slice discussion in Section 5.2.1, and Section 5.2.5 were read.

That preprint still poses the general Bennequin-sharpness equivalence as Problem 2.5. Propositions 5.43–5.44 address specified Whitehead-double/reverse-parallel cases. The abstract's quasipositive but non-strongly-quasipositive examples do not supply counterexamples to the present problem: the untwisted positive Whitehead doubles in Remark 5.11 use the slice companions 9_46 and 10_140 and are themselves slice. The slice-Bennequin inequality bounds their transverse self-linking by -1, so they cannot be sharp for a genus-one Seifert surface. The detailed quasipositive braid calculations in that new paper were not independently re-proved here, nor are they required for this scope distinction. This newer check leaves the frozen artifact's unresolved status intact.

## 2. Band identity and the minimum over representatives

The embedded band-generator convention agrees exactly with [Ito–Kawamuro](https://arxiv.org/abs/1703.09322v4), p.1. A conjugate band has Artin exponent sum +1, and its inverse has exponent sum -1. For an n-disk, b-band surface, attaching each one-handle reduces Euler characteristic by one. Thus

`chi(F_w)=n-b_+-b_-`, while `sl(T)=b_+-b_--n`.

For a word representing the same transverse link as the sharp boundary, substitution of `sl(T)=-chi(Sigma)` gives exactly `chi(Sigma)-chi(F_w)=2b_-`. No minimality assumption on the displayed disk-and-band surface is used. Euler characteristic is counted directly, so the proof does not silently impose a knot-genus or fixed-component formula on links.

There is at least one transverse braid representative. Each integer negative-band count is nonnegative, so its set has an attained minimum. The equivalent set of surface Euler characteristics is nonempty and bounded above, hence has an attained maximum. Formula (4) follows. Naming this minimum supplies no argument that it vanishes. This is a correct restatement of the remaining construction and is credited to the zero-defect part of Ito–Kawamuro Observation 1.2.

Requiring the resulting strongly quasipositive braid to represent the **given transverse link** is stronger than merely obtaining strong quasipositivity of its underlying smooth link type. The artifact explicitly uses the stronger statement as a sufficient route, without claiming that the distinction has disappeared.

## 3. The topological-braiding shortcut fails at the right place

I checked Ito–Kawamuro Theorem 1.7 and its full proof on manuscript pp.17–18. The statement concerns a topological link type. The proof explicitly permits both signs of stabilization. Lemma 4.9 has the sign claimed in the artifact: a positive hyperbolic ab-tile is removed using negative stabilization, and conversely.

Positive stabilization changes `(n,e)` to `(n+1,e+1)` and preserves `e-n`. Negative stabilization changes it to `(n+1,e-1)` and lowers self-linking by two. Consequently it cannot preserve the original transverse isotopy class, although it preserves the smooth closure type. The missing transverse condition cannot be recovered merely by citing the topological surface theorem.

Both trefoil controls are correct. The negative stabilization has the same surface Euler characteristic and smooth knot type but lower self-linking. Inserting N adjacent cancelling positive/negative pairs gives precisely the same braid element, while the displayed surface gains N negative bands and loses 2N in Euler characteristic. Thus neither a single word with negative bands nor an arbitrary topological braid presentation is a counterexample.

## 4. Signed singularities and canonical surfaces

Ito–Kawamuro Lemma 3.1 gives the stated signed counts. Adding the two formulas yields

`chi(Sigma)+sl(T)=2(e_- - h_-)`.

Sharpness therefore forces equality of the two negative counts, not their vanishing. The numerical tuple in the artifact satisfies the identities, but its geometric realization and any cancellation moves are explicitly left unclaimed. Counts alone contain no information about the required separatrices or signs of available geometric moves.

For the knot-only route, the ordinary Bennequin inequality first forces the sharp Seifert surface to have minimal genus. The stated slice-torus inequalities then squeeze tau and the smooth slice genus to equal the Seifert genus. I read [Feller–Lewark–Lobb Theorem D, Corollary E and their proofs](https://arxiv.org/abs/1809.06692v3). Their criterion requires a canonical surface whose genus equals the slice-torus invariant. It therefore applies when canonical genus equals Seifert genus in the sharp case, exactly as used here.

This establishes a known positive case for the smooth knot type, not a general conversion of every fixed transverse representative to a positive-band word. It also does not prove that an arbitrary minimal-genus surface is canonical. The artifact does not assume either missing assertion. A counterexample to the original knot-type conclusion would necessarily lie outside the canonically minimal class; this is a restriction on a possible counterexample, not its construction.

## 5. Exact checks and their limits

All **324** submitted controls reproduce byte-identically from an isolated copy. The verifier SHA-256 is `d88a91d6dccd333d4114cd34d84b383385b5b5d4a6f6dd1e4c88759e85810e6c`; the receipt hash is `6d269ebc0277cc7e0aa26c13d3c131754021fb6e2bf39a923b1bf176f133249d`.

The separate standard-library checker passes **3,848** exact assertions. It verifies full free-group Artin substitutions and their inverses for 56 embedded bands, all short adjacent-band words through length four, both stabilization effects and component counts, all signed-singularity count tuples in a small box, exact cancelling-word reductions, and the scalar genus squeeze. It does not import the author's checker.

Run from the review directory:

```sh
python independent_checks.py
python author_replay/verify.py > author_replay/replayed.json
cmp author_replay/replayed.json author_replay/verification.json
```

These controls are algebra and accounting, not tests of arbitrary transverse isotopy, geometric realizability, or quasipositivity. The actual proof obligations were examined in the preceding sections.

## 6. Disposition

The source audit and scoped deductions pass unchanged. Preserve **unsolved, 2/5**, the distinction between the original link-type question and the stronger fixed-transverse construction, and both remaining geometric gaps. The newest primary source checked in this review does not remove those gaps. No proof, counterexample, or priority claim for the general problem is certified.
