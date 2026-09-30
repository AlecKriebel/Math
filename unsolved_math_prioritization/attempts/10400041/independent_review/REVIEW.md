# Independent review of the self-delta partial results

**Verdict: PASS_SCOPED_SPLIT_BLOCK_CRITERION_AND_PAIRWISE_OBSTRUCTION.** The submitted arguments are correct within their stated scope. The general classification in Ohtsuki Problem 2.19 remains **unsolved, 2/5**. No mandatory correction is required. This is an independent adversarial AI review, not human peer review or a claim of priority.

The reviewed `PARTIAL_RESULT.md` has SHA-256 `63502b43d97fc80c4f5041e7ea75399434ef6ed496984b7382f33bafeb39e09b`. The submitted verifier and receipt are preserved in `author_replay/`. All 68,307 submitted assertions reproduce byte for byte. The separate `independent_checks.py` passes 48,042 exact assertions. Those finite controls support the algebra and bookkeeping; the geometric conclusions require the arguments and cited theorems below.

## 1. Original question and imported results

The rendered original page, Ohtsuki's collection, printed p.415, explicitly defines a self-delta move by requiring all three participating arcs to belong to the same component, then asks for necessary and sufficient conditions for equivalence of links with more than two components. The question concerns closed links. The submitted ordered, oriented convention agrees with the cited two-component theorem and recent pretzel paper. Neither string-link classification nor unrestricted delta equivalence can be substituted. [Original collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

For a link with m components, the normalization is

\[
\delta_1=a_{m-1}(L),\qquad
\delta_2=a_{m+1}(L)-a_{m-1}(L)\sum_i a_2(K_i).
\]

Nakanishi–Ohyama, Theorem 3, printed p.642, states completeness of this pair for **two** components. Its preceding definitions concern ordered, oriented links. The same page distinguishes the stronger question involving the invariants of **all** sublinks. I checked the rendered theorem page and surrounding definitions. The published two-component theorem is a credited input; this audit does not purport to reconstruct its entire clasper proof. [Published primary paper](https://www.jstage.jst.go.jp/article/jmath1948/55/3/55_3_641/_pdf).

Yasuhara's Theorem 1.3 assumes the vanishing of all Milnor invariants with length at most 2n−1 and maximum index repetition at most two. Under that assumption its remaining length-2n invariants classify self-delta equivalence. Corollary 1.5 recognizes the unlink by vanishing of all invariants with repetition at most two. Remark 1.6(2) explicitly prevents transferring that statement unchanged to string links; Remark 1.8 prevents treating the two-parallel link-homotopy test as a classification of arbitrary pairs. The candidate retains each restriction. [Primary preprint, version 3](https://arxiv.org/pdf/math/0610492v3).

The April 2026 pretzel preprint treats enhanced pretzel diagrams and states its higher-component criterion within that family. Its introduction also explicitly gives the ordered, oriented tame-link convention. Its classification is credited as a preprint claim; neither the candidate nor this review certifies every diagrammatic step of that paper. It supplies no general arbitrary-link classification. [Primary preprint](https://arxiv.org/pdf/2604.03698v1).

## 2. Restriction and the split-block criterion

Deleting components from a realizing sequence preserves every self-delta move on a retained component. A move on a deleted component disappears. A supporting ball meets only its specified local arcs, so deletion creates no new obstruction. Ambient isotopies restrict as well. Thus equivalence of corresponding sublinks is necessary.

For a fixed partition into one- and two-component blocks, assume both links are split along that partition. Necessity follows by restriction and the two-component theorem. For sufficiency, apply the two-component theorem in each two-label block. The unrestricted delta classification quoted in the primary papers makes every pair of knots equivalent; since all arcs of a knot belong to one component, this is precisely a self-delta sequence for a one-label block.

The support issue is legitimate. Each block has a finite realizing sequence, and its finite isotopy tracks and local move balls fit in a compact subset of three-space. A rescaling places that realization inside a designated ball. The starting and ending copies can be matched with the block embeddings by isotopies inside the ball. Choose disjoint balls for the different blocks and perform their sequences there. No move uses arcs from another block. This proves the stated restricted criterion; it makes no assertion that a general link admits such a split partition.

## 3. The Borromean diagnostic is geometric and correctly limited

Let L be the Borromean rings split from at least one additional unknot. The Conway polynomial of L is zero: apply the skein relation at a Reidemeister-I curl of the other summand. Both crossing choices represent the same link, while smoothing produces the split unknot, so multiplication of the split-link polynomial by z is zero. The integral polynomial ring has no z-torsion. The full unlink has the same zero polynomial. Consequently their full-link delta pairs vanish.

Every two-component sublink of the Borromean rings is an unlink. Extra components are split unknots. Thus all component knot types, pairwise linking numbers, and two-component delta pairs agree with those of the full unlink.

The retained Borromean three-component sublink has triple Milnor invariant of absolute value one, with zero indeterminacy because all pairwise linking numbers vanish. Cha–Powell's Lemma 2.1 proof explicitly identifies a Borromean component as a commutator of meridians of the other two. Passing to its preferred parallel longitude gives the degree-two Magnus coefficient of that commutator, namely the coefficients +1 and −1 of XY and YX. The sign depends on conventions and is immaterial. Yasuhara's introduction recalls preservation of nonrepeating Milnor invariants under link homotopy and that self-C2 equivalence implies self-C1 equivalence. Therefore the Borromean sublink cannot be self-delta equivalent to the three-component unlink. Restriction proves the asserted obstruction for the full links. [Cha–Powell primary paper, Lemma 2.1](https://msp.org/pjm/2014/272-1/pjm-v272-n1-p01-p.pdf).

This defeats **full-link Conway data together with all two-component data** for every component count at least four. It does not address completeness of the invariants of every sublink: the Borromean three-component sublink is information omitted from the defeated data set. It also is not a counterexample to the request for some unknown necessary-and-sufficient classification. Forgetting order or reversing orientations does not remove the nonzero-versus-zero triple obstruction.

## 4. Independent controls and their limits

The submitted program was run from `author_replay/`; its output receipt is byte-identical to the frozen receipt. The independent checker uses integer upper-unitriangular 3×3 matrices to calculate signed commutators, rather than the submitted truncated free-series engine. It also multiplies full formal polynomial coefficient arrays before extracting the delta expressions, enumerates one-/two-label partitions and verifies their telephone-number recurrence, and checks that two-label subsets omit the Borromean triple while the collection of all sublinks retains it.

Reproduction:

```
cd author_replay
python verify.py
cd ..
python independent_checks.py
```

The independent total is 48,042 exact assertions. Matrix commutators are an algebraic diagnostic, not a substitute for identifying an actual link longitude. Arbitrary formal Conway coefficients are not claimed to be realized by links. Neither checker proves a clasper theorem, enumerates all links, or establishes a general classification.

## 5. Publication scope

The original target remains unresolved. Publish this as a restricted consequence of existing classifications and a diagnostic against an insufficient invariant list. Retain the fixed split partition, the vanishing hypotheses of Yasuhara's result, the pretzel-family restriction, and the distinction between closed links and string links. No novelty claim or general completeness claim is justified by this package.
