# Mathematical and source audit: AIM-LOGIC-0146

Problem 20002370, Zahidi's AIM Question 34. Audit date: 2026-10-03 UTC.

## Verdict

**The mathematical partial claims in the frozen packet are sound, conditional only on the explicitly cited standard theorem inputs. No mandatory mathematical correction was found. The original minimization problem is not resolved.**

The verified conclusions, in the pure ring language with no named generator, are:

- The minimum number of changes between adjacent blocks in a prenex quantifier prefix is exactly one.
- For a separator with prefix `forall x_1 ... forall x_n exists y_1 ... exists y_m`, where `m` is unrestricted, the minimum `n` is between two and three, inclusive. This audit does not choose between them.
- One distinct variable symbol cannot separate the fields. The minimum finite-variable width is at least two and is finite, but no exact value or explicit useful numerical upper bound is established.
- Sentences with at most two quantifier occurrences agree. This does **not** establish agreement for every formula using two reusable variable symbols.

These statements are consequences or reconstructions of prior results, together with elementary supporting arguments. This audit makes no novelty claim and does not certify that an exhaustive literature search has excluded every subsequent determination.

## Reviewed evidence and integrity

The original [AIM problem list, Question 34, p.7](https://aimath.org/WWN/hilberts10th/hilberts10th.pdf) was read before evaluating the packet. It concerns the real algebraic numbers and the reals, each with one indeterminate, and asks separately about quantifier complexity and variables. The PDF's extracted text loses the algebraic-closure bar. The pure-ring, unnamed-generator convention and the several syntactic metrics are explicit choices in the packet rather than extra wording quoted from that question.

The reviewed frozen manifest has SHA-256:

`99115a56632ebf35eef1e68258c45fedb8ff52c001d6b14b75aa4a39d3ea97d8`.

All six listed files were read. Every listed byte length and SHA-256 matches the actual file, and there are no extra files in the reviewed directory apart from the manifest. Running the supplied checker reproduced `exact_results.json` **byte for byte**, including its 3,364 assertions. The file-by-file digests are recorded in `independent_results.json`. This establishes the reviewed version's identity, not the validity of its mathematical proofs.

Sources checked:

1. [Anscombe–Fehm, author preprint v3](https://arxiv.org/html/2405.12771v3), especially Lemma 5.2, Remark 5.4, and the fragment definitions. The one-leading-universal transfer applies to the present pair. The unresolved two-leading-universal example in Remark 5.4 is instead the real field and a proper elementary extension. The packet keeps those pairs distinct. [Publisher metadata](https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/abs/universalexistential-theories-of-fields/2E8974B4ECE2B778B5BFB1A13FEAF2F7) confirms the stated dates, volume and pages.
2. [Vollprecht's dissertation](https://d-nb.info/1364825406/34), Definition 3.2.1, Lemma 6.1.1 and Section 6.3. The definition and cut-formula pages were also visually inspected. The superscript fragment permits branching; the subscript fragment bounds a prenex universal block. The named-generator integer definition is explicitly uniform over real closed constant fields.
3. [Denef's publisher record](https://www.ams.org/tran/1978-242-00/S0002-9947-1978-0491583-7/) confirms the bibliographic information. The precise definition input was checked through Vollprecht's Lemma 6.1.1, rather than by rereading Denef's entire original proof. The original publisher PDF was not obtained. The audit therefore does not upgrade the packet's disclosed source-access scope.

No source PDF, full source extract, or image of a source page accompanies this report.

## Mathematical review

### 1. Transfer and language

The coefficient-transfer proof correctly permits parameters in the smaller rational-function field. One fixes degrees only after choosing an actual witness; vanishing equations become coefficient equations, while each denominator and each required nonzero polynomial retains a specifically selected nonzero coefficient. The transferred system consequently still represents well-defined rational functions and preserves inequations. This proves existential closedness, not elementary equivalence of the rational-function fields.

The one-leading-universal argument is correct in both directions. Downward transfer follows by fixing the universal input in the smaller field and descending witnesses. For upward transfer, an element outside the real algebraic field is transcendental over it, so it can be the image of the unnamed generator under an embedding. The formula's lack of a named `t` is indispensable to this step. Negation gives the corresponding one-leading-existential obstruction.

The one-symbol induction is valid: quantification binds the only available symbol, making each such subformula closed. Agreement of simpler closed subformulas and existential/universal agreement finish the induction. It proves a width-one obstruction only.

### 2. The factorial-digit cut

With each factorial position counted once, the definitions of `A_n`, `B_n` and `s_n` are consistent. Infinite remaining nonzero digits make the tail positive, and infinitely many omitted positions make it strictly smaller than the full geometric tail. Thus the strict radius is correct even at the initial positions.

The Liouville argument is valid with unreduced denominator `2^(m!)`: a smaller reduced denominator only strengthens the lower bound needed in the contradiction. Infinitely accurate rational approximations establish transcendence without relying on any finite numerical computation.

The cut equivalence has the correct closed boundary: failure of `|A_n c-B_n| < 1` means `>= 1`, not `> 1`. The equation with the auxiliary square therefore correctly allows a zero witness on the boundary. The proof uses an Archimedean real subfield, as explicitly stated; it does not silently assert the same singleton characterization in a non-Archimedean field.

### 3. Constants and existential arithmetic

The curve `v^2 = 1+x^4` has a smooth projective model of genus one. Squarefreeness can be seen directly from `(1+x^4) - (x/4)(4x^3) = 1`; over an algebraic closure the double cover of the projective line has four simple branch points. A nonconstant rational solution would yield a separable nonconstant map from a genus-zero curve to this genus-one curve, contradicting Riemann–Hurwitz. Constants have square roots of `1+x^4` by real closedness. Thus the proposed one-existential-variable constant predicate is correct, and both coordinates of any solution are constants.

The arithmetic set of pairs `(2^n,B_n)` is computable. Using the stated integer-definition theorem, four squares, and DPRM gives a fixed finite existential formula with the generator as its only distinguished parameter. All integer and nonnegative-integer restrictions must be included on the coding variables; that is available within the quoted existential construction. The absence of explicit Denef/DPRM polynomials prevents a numerical count of auxiliary variables, but does not prevent the existence or prefix argument.

### 4. The separator and its attempted compression

For a constant different from the cut value, the witnesses at `t` transport under the isomorphism onto the subfield generated by any nonconstant `u`. The subsequent inclusion preserves existential truth. Surjectivity onto the whole ambient rational-function field is neither available nor needed, and the packet correctly avoids claiming it.

The three universally quantified variables have separate roles: testing a constant through its genus-one witness, and ranging over nonconstant candidate parameters. Pulling existential witnesses to the final block is valid after renaming; nonempty domains provide arbitrary witnesses for unused disjuncts. At the missing cut value over the reals and at `u=t`, every escape disjunct fails. Over the real algebraic numbers the cut value is absent, so the sentence holds.

The branched expression and the three-universal prenex expression are equivalent. This is not a two-universal prenex separator. Identifying the witness variable with the parameter variable forces a tautological disjunction because the genus-one witness is constant. The diagonal formula is therefore true over every real closed constant field, regardless of the arithmetic predicate. This rejects that particular construction only.

### 5. Existential guards

Every infinite field is existentially closed in its one-variable rational-function field by specialization away from finitely many zeros and poles. Consequently a nonempty existentially definable set over constant parameters must have a constant point. This proves the claimed unary nonconstant-guard obstruction. It says nothing prohibiting a suitable two-argument predicate whose second argument is an already nonconstant parameter. The packet states that boundary correctly.

### 6. Bounded semantics and unbounded witnesses

For a separately prescribed degree bound at each binding occurrence, rational functions admit coefficient-tuple representations with a nonzero denominator. Equality and inequality translate to finite coefficient conditions after cross multiplication. Universal quantification over all valid representations and existential quantification over some valid representation respect nonuniqueness. The resulting first-order sentence is over the real closed constant field, so it transfers. Degrees of intermediate terms are allowed to grow according to their syntax; truncating those terms would be a different, unjustified procedure.

This proof handles alternating quantifiers, but only the stated bounded semantics. It cannot interchange an infinite union of degree bounds with quantification. Likewise, the first cut violation for the rational partial sum at `m!` really occurs at `(m+1)!`. The growing witness index does not imply a growing number of variables in the single arithmetic formula.

## Normalization discrepancy

Let `lambda_p` denote the sum with each positive factorial position counted once. With ordinary `0!=1!=1`, the displayed definition in the dissertation is `ell_p = lambda_p + 1/p`. The printed alternative `1+lambda_p` exceeds this by `1-1/p`. The subsequent polynomial's limiting center is `2+lambda_p`, which exceeds the labeled `ell_p-1` by `3-1/p`; the latter offset is `5/2` when `p=2`.

Both are rational offsets. Translation by a rational number preserves whether an ordered field realizes the corresponding rational cut. Therefore these arithmetic discrepancies do not invalidate the stated existence result. The packet's independently normalized construction bypasses them. This conclusion concerns these displays and does not constitute an author-issued erratum or a general audit of the dissertation.

## Corrections and optional improvements

### Mandatory mathematical corrections

None found in the frozen mathematical claims. The partial disposition must be retained: the exact two-versus-three leading-universal minimum, exact total-variable minimum, and optimal quantifier rank are not established. No finite control should be presented as proving a function-field separation or equivalence.

### Optional precision improvements

1. In Lemma 2.2, replace “K is relatively algebraically closed over its real-closed subfield k” with “k is relatively algebraically closed in K.” The intended fact and its use are correct; the latter wording is standard and unambiguous.
2. In Proposition 6.2, replace the prose about being “strictly between or equal to” endpoints with `0 <= q_m-s_n < 2^(-n)` for `n <= m!`.
3. In Section 4.4, add the explicit second offset `3-1/p` if a reader should be able to compare the polynomial's center with the labeled cut immediately.
4. If a future revision supplies a numerical variable upper bound, it must expand and count all constant-predicate, integer-domain, four-square, and DPRM witnesses under a declared variable-reuse convention. Counting the three universal variables alone would be insufficient.

## Independent controls

Run `python audit/independent_controls.py` from the problem directory. Its recorded output is `audit/independent_results.json`.

The independent run passed 72,112 assertions, including:

- Frozen file inventory, sizes, hashes, and byte-exact replay of the original checker.
- All 65,536 two-element interpretations of an unrestricted binary guard, an existentially defined unary predicate, and an existentially defined binary predicate, checking branched-to-prenex conversion with the witnesses expanded.
- A diagonal counterexample satisfying both constant-coordinate implications.
- Direct factorial sums for `m=2,...,6`, with first violations at `6,24,120,720,5040` and exact boundary value one.
- Both normalization offsets in bases `2,3,5,7`.
- The quartic squarefreeness identity and 625 rational-polynomial cross-multiplication cases.

These are reproducible finite controls. Quantifier elimination, Denef's definition, DPRM, Liouville's theorem and Riemann–Hurwitz remain mathematical theorem inputs; this is an unrefereed audit, not a formal proof-assistant verification.
