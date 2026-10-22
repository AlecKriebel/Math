> **Root correction,17October2026:** This family inherited candidate-containing
> context and was not blinded. Freezing before a local file comparison does not
> establish prior ignorance. The historical account below is preserved; see
> INDEPENDENCE_CORRECTION.md / the archive chronology correction for the current
> interpretation. Its exact implementation and output remain checkable.

# Independent canonical-potential reconstruction for PR #1205

Review checkpoint: 2026-10-17, 09:29 America/Los_Angeles. Completion of this mathematical reconstruction/reproduction family: **100%**. This is not a priority audit or approval of the final publication package.

**Verdict:** the submitted canonical GHKK potential, its complete monomial support, coefficients, and exponent-bound failure reproduce exactly. No mathematical defect was found in this family. The separate full-solution/publication decision requires the other review families and priority audit.

## Independence and artifacts

I did not read submitted PROOF.md, AUDIT.md, or candidate code before constructing `reconstruct.py` and freezing `independent_output.json`. The frozen output has SHA256

```
fc5a5208035b011683168d1114af93c613de4f001e19ab49ce70a464e0b0d459
```

`INDEPENDENT_FREEZE.txt` recorded the hash before the first candidate read. `compare_after_freeze.py` is explicitly separate: it reads the submitted proof only after checking that hash. Its outputs are in `postfreeze_comparison.json`.

Run with Python 3 and SymPy 1.14.0:

```
python reconstruct.py
python compare_after_freeze.py
python source_controls.py
```

The independent script imports no submitted data/code, does not use submitted mutation routes, and uses exact symbolic rational arithmetic over the integers. The only input is the task's Dynkin diagram and reduced word. Computation takes about a second on the review host.

## Source conventions and falsifying controls

The sources inspected directly were [KS2022, published](https://link.springer.com/article/10.1007/s10801-022-01144-z), its [author preprint](https://arxiv.org/abs/2109.14439), [GKS, author preprint](https://arxiv.org/abs/1711.07176), and [OWR2021, printed pp.1123–1125](https://ems.press/content/serial-article-files/46898). Local copies have a source manifest and are review inputs, not proposed preprint-package files.

KS equation (3) uses the exchange pairing in order `(i,k)` for the X-coordinate indexed by i when mutating k. A frozen vertex is optimized when every adjacent mutable arrow points into it; its canonical summand is then the inverse frozen coordinate (Definition 7). Inclined reduced-word edges require adjacency in the Dynkin diagram, explicit in GKS Section 4.2.2. KS's displayed Definition 8 omits that adjacency qualifier.

There is a real source-version trap: GKS arXiv v1 equation (20) displays the transposed pairing order. The script follows the later KS equation and checks against GKS's explicit A2 Example 5.3: for word 121, the nontrivial summand is `X2^-1(1+X1^-1)`. Transposing the sign produces a different rational function and the control rejects it. A double X-mutation, with the mutated exchange matrix on the second step, returns every variable exactly. These controls would catch the most consequential orientation error.

An additional post-freeze control reproduces KS's corrected published D4 example with word `(2,1,3,4)^3` and its published ten-mutation route. The independently computed summand has 27 terms, precisely one coefficient 2, and the two support rows giving its displayed half-sum redundancy. This confirms the conventions in a source example with a nontrivial cancellation, independently of the submitted target. Results appear in `source_controls.json`.

## Mechanism and independent reconstruction

The script builds the simple-reflection matrices from the D4 Cartan matrix. All twelve successive root vectors are distinct and positive; the word product is `-I4`. It therefore certifies the proposed reduced word for the longest element.

It next constructs the reduced-word quiver from next-occurrence intervals, Dynkin adjacency, and last-occurrence frozen positions. The independently obtained frozen positions are 7,9,11,12 and its complete 16-arrow list agrees with the submitted list after comparison.

Optimized seeds are discovered by two breadth-first searches of the reduced-word braid graph with opposite neighbor order. A commuting move relabels its two position coordinates. A braid `aba -> bab` starting at position p mutates p and swaps p+1,p+2. **After every individual move**, the transported exchange matrix and frozen set are checked against a fresh construction directly from the new word. This detects a wrong braid position, wrong permutation, forgotten frozen relabelling, missing Dynkin adjacency, or quiver-mutation sign error.

The search stops at words ending in the desired simple root. The last position is frozen, and the final exchange row is explicitly checked to have no outgoing mutable arrow. Its inverse X-coordinate is pulled back by the exact rational maps. Thus the resulting polynomial is fixed by canonical optimized-seed normalization; it is not an arbitrarily chosen polynomial with the desired tropical properties.

Converting the discovered paths to the initial fixed vertex labels gives:

|Frozen position|Forward-search mutation route|Reverse-search mutation route|
|---|---|---|
|7|2,6,1,3,4,8,5,10|10,6,2,5,1,4,3,8|
|9|4,8,5,10|10,4,5,8|
|11|10|10|
|12|empty|empty|

Both routes give the same full rational functions for every summand. Canonicality does not depend on restricting to reduced-word seeds: the optimized-seed definition identifies the same global summands on the entire cluster variety. Reduced-word seeds here provide explicit certificates sufficient to calculate those summands.

## Exact result and post-freeze comparison

The independent result has **22 distinct terms**, all coefficient **1**. Summand sizes by simple-root labels 1,2,3,4 are **14,1,5,2**, or by frozen positions 7,9,11,12 are **14,5,2,1**. Every exponent is nonpositive. Exactly two exponent rows have an entry below -1:

```
( 0,-1,-1,-1,-1,-2,-1,-1,0,-1,0,0)
(-1,-1,-1,-1,-1,-2,-1,-1,0,-1,0,0)
```

Both lie in the frozen-position-7 summand. Thus X6 has exponent -2 twice. `independent_output.json` contains every term, coefficient, exchange-matrix entry, positive root, and word along each chosen route.

After freezing, I checked the submitted factored formula against this result: exact equality holds. The set of all 22 exponent rows in its certificate table equals the independently reconstructed support, after the declared `y=X^-1` sign change. All 484 separating scalar products were recomputed independently: every diagonal is -1 and every off-diagonal is nonnegative (minimum zero). This establishes essentiality for the actual canonical support, rather than for an unconnected proposed polynomial.

The chamber-ansatz matrix was also independently constructed from the stated Cartan/interval formula. Its determinant is 1, and all transformed exponent entries lie in {-1,0,1}. This confirms the paper's restriction to the original W-coordinate converse and its explicit nonclaim about the later pullback/string-coordinate converse.

## Status and exact remaining gap

Mechanism: independent reduced-word graph traversal, checked quiver transport, and exact canonical X-coordinate pullback. Evidence: complete executable reconstruction, two distinct routes for each nontrivial longer summand, source-orientation controls, frozen support, and exact comparison/certificate products. Status: **verified**.

There is no remaining computational or mathematical gap in this reconstruction family. This review does not establish novelty, that no later literature already records this distinction/counterexample, or the accuracy of a final PDF not yet prepared. Those are separate required audits. No outside individual was contacted.
