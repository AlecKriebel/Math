# Independent review of 10400099: the logarithm of a finite-quandle coloring count

**Verdict: PASS — the exact conjecture is a consequence of an already-published theorem.** The justified source status is **already_solved**, with **zero new proof-search attempts**. No mandatory correction was identified. This is a source identification and complete verification of the stated deduction, not a new theorem or priority claim. The review is by a separate AI agent and is not human peer review.

The frozen artifact reviewed is `SOURCE_STATUS.md`, SHA-256 `d768efc46c7f312b4cba1a75a7b687682809bc17c020d839999c40dc84db2dfb`. Its byte-identical snapshot is included in `author_replay/`.

## Exact source and theorem coverage

[Ohtsuki's 2002 problem collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed p.459, Conjecture 5.3, concerns the total number of homomorphisms from the fundamental quandle of a classical knot in the three-sphere to a fixed connected finite quandle. It asks whether the logarithm can be a finite-type invariant without being constant. The subsequent quandle-cohomology material is outside this conjecture.

[Eisermann, *The number of knot group representations is not a Vassiliev invariant*](https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/twistseq.pdf), Proc. Amer. Math. Soc. 128 (2000), 1555–1561, DOI 10.1090/S0002-9939-99-05287-9, states Theorem 3 for **complex-valued knot invariants**, bounded in absolute value by an arbitrary integer-valued function of braid index. Such an invariant is constant or is not finite type. The theorem is explicitly more general than its paper's representation-count application. It does not require rational values, multiplicativity, a finite-group model, or a faithful quandle.

I checked the complete applicable argument in Section 1. A finite-type invariant restricts to a polynomial on each integer full-twist sequence (Lemma 4). Braid index stays bounded on each **vertical** twist sequence: a fixed number of strands represents every member as the closure of a fixed braid followed by an integer power of one full twist (Lemma 6). The same conclusion follows from the constant number of Seifert circles in these diagrams. A bounded complex polynomial on the integers is constant. Corollary 5 realizes an arbitrary crossing change by adjacent terms of a suitable such family, and crossing changes connect any knot to the unknot. The orientation carried by this argument is compatible with the oriented quandle convention. The horizontal twist-family braid-index bound is not being assumed.

The finite-difference polynomiality is additive: resolving one selected crossing in each of several full-twist blocks cancels the corresponding block in one resolution. An order exceeding the finite-type degree therefore gives zero alternating difference. Neither taking a logarithm of a finite-type invariant nor preserving finite type under exponentiation is asserted.

## Universal coloring estimate and logarithm

Let the nonempty finite quandle have cardinality q. Idempotence supplies q distinct constant colorings of every knot diagram. In a closed braid with b strands, its top colors have at most q^b choices. Each crossing determines subsequent colors uniquely. For negative crossings this uses the inverse of a right translation, which is a bijection by the quandle axiom; an involutory assumption is unnecessary. Closing the braid only imposes further constraints. Thus

\[
q\le h_X(K)\le q^{b(K)}.
\]

In particular the logarithm is everywhere defined. The singleton case gives the zero logarithm. In all cases the natural logarithm satisfies

\[
0\le \log h_X(K)\le b(K)\log q\le q\,b(K).
\]

Eisermann's theorem applies with the integer-valued function n ↦ qn. Real, potentially irrational logarithms are valid complex-valued invariants. A different fixed positive logarithm base other than one only rescales by a nonzero constant; the candidate's stated bases greater than one suffice. The conclusion covers all finite nonempty quandles and hence the connected quandles in the question. A constant invariant is finite type of order zero.

The literal count of the unknot is q. The preceding source remark on connected-sum multiplicativity must therefore not silently be imposed on the unnormalized count when q > 1. The artifact correctly avoids that issue. Replacing h_X by h_X/q subtracts the constant log q, so finite-type status and constancy give exactly the same answer. No multiplicativity or rationality hypothesis enters the deduction.

## Independent corroboration and attribution

[Cheng–Gao's published 2015 paper](https://msp.org/agt/2015/15-2/agt-v15-n2-p11-p.pdf), Algebraic & Geometric Topology 15, 933–963, Section 2, printed p.936, explicitly identifies quandle colorings with fundamental-quandle homomorphisms and gives the bounded vertical-twist argument for coloring counts, crediting Eisermann. One preceding bullet uses **bridge number**, whereas the concluding twist argument explicitly uses **braid index**; these are not being confused in the candidate or in this review.

That paper's discussion is corroboration. The decisive result is the unrestricted complex-valued boundedness theorem, which applies to the logarithm itself. A publication explicitly announcing the numbered Conjecture 5.3 as solved was not located in this audit. This bibliographic qualification does not weaken the complete deduction from a published theorem. There is no new discovery claim.

## Reproduction and independent controls

The submitted verifier was copied with its frozen artifact and receipt into `author_replay/`, run there, and its output receipt compared byte for byte with the submitted receipt: **687 exact assertions passed**.

A separate standard-library checker imports no submitted code. It verifies **5,769 exact assertions**, including seven Alexander-quandle models, three genuinely non-involutory models, positive/negative crossing inversion, the braid relation, mixed-sign closed-braid bounds, constant colorings, exact dihedral two-braid counts for positive and negative exponents, and additive finite differences. A finite periodic three-coloring example also supplies explicit nonconstant logarithm differences. No floating-point logarithms are used.

From this review directory, reproduce the independent receipt with:

```sh
python independent_checks.py > independent_results.replayed.json
cmp independent_results.replayed.json independent_results.json
```

For the submitted replay:

```sh
cd author_replay
python verify.py
```

The finite controls test the stated algebra and conventions; they do not replace the universal coloring argument or Eisermann's theorem. The primary-source hashes and inspected scope are recorded in `source_verification.json`. Source PDFs and rendered pages are not part of the publication bundle.

## Publication scope

Publish as a credited **already-solved source consequence**, with the fixed finite nonempty quandle, classical knot, and characteristic-zero numerical-invariant scope stated above. Do not advertise a new theorem, a finite-field-valued conclusion, or an unrelated quandle-cohomology solution. There are no remaining mathematical gaps in the exact conjecture's deduction.
