# Independent adversarial review: Whitehead-double degree diagnostics

**Verdict: PASS_SCOPED_NORMALIZATION_AND_PARITY_OBSTRUCTION.** No mandatory correction is required. The original Kidwell–Stoimenow problem remains unresolved by this package, after two substantive approaches. This is an independent AI review, not human peer review.

Reviewed artifact: PARTIAL_RESULT.md, SHA256 **533481eb1b5a057d89eb4a441133b22e22fc0846e9ee760ed1b16930c7f06229**. The reviewed text was preserved in author_replay/ and not edited. The submitted 5,130 assertions reproduce byte-for-byte. A separately written checker passes **11,010 exact integer assertions**.

## 1. Exact question and source scope

Ohtsuki's full problem collection, printed pp.390–392, defines the unknot-normalized polynomials and asks for the maximum Alexander-variable degree relation for every nontrivial companion knot and its Whitehead doubles. The normalized target has an additive constant of two. Its adjacent alternating update is an upper bound, not a general equality. I checked the full PDF/text and visually inspected printed p.392.

The retrieved Gruber source is arXiv:math/0406106v4, 23 October2008, an eleven-page primary preprint. Sections1–3 and5, especially Remark1, Theorem3, Lemma7, Proposition9 and Theorems17–18, support the reported normalization, congruence, clasp reduction and credited alternating scope. The publisher record confirms the later paper and online date1July2009. The inspected preprint is not represented as a byte-identical copy of the final journal text. I checked the relevant printed pages visually as well as in extracted text.

Sources:
- [Ohtsuki collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)
- [Gruber primary preprint](https://arxiv.org/abs/math/0406106)
- [Gruber publisher record](https://doi.org/10.1017/S0305004109002370)

The source's diagrammatic theorems remain credited dependencies. This review audits their exact statements and the package's deductions; it does not claim a new reconstruction of all their geometric proofs or exhaustive proof of current open status.

## 2. Normalization and clasp tests

The two normalizing factors have maximum Alexander-variable degrees minus one and zero, respectively. The latter factor contains the constant term minus one, so treating its degree as minus one would be an error. Over an integral domain, leading coefficients multiply without cancellation. Thus the stated degree conversions are correct even when several framing-variable monomials share the leading Alexander degree. The empty diagram and unknot are explicitly distinguished.

For the displayed clasp, the skein expression has a first summand of degree minus one and a second summand of degree r+1 when the Rudolph degree r is positive. The top term cannot cancel. Converting the HOMFLYPT normalization adds one more, giving r+2. The positive-degree hypotheses are important and are retained in the artifact. My independent checker includes a formal r=0 case where the asserted extension would fail. No general positivity theorem for the Kauffman degree is assumed.

Mirroring inverts a framing variable and may change coefficient signs in the Alexander variable; it preserves the relevant maximum degree. The opposite-clasp reduction therefore does not smuggle in a chirality or framing assumption.

There is a harmless internal source inconsistency: Gruber's p.3 displays a positive framing exponent, while the proof of Proposition4 uses the opposite sign. The submitted text follows p.3. Both are framing-variable units, so all degree conclusions and the nonvanishing of top coefficient parity in this package are independent of that sign. No correction of the mathematical conclusions is needed.

## 3. Congruence and residual obstruction

For a knot, the total linking term in Gruber's Theorem3 vanishes. The map taking the framing exponent to minus twice that exponent is injective on Laurent monomials over the field with two elements. Substituting the square of the Alexander variable doubles the maximum degree. An odd coefficient in the top Kauffman coefficient polynomial therefore survives in the corresponding Rudolph coefficient and yields a lower bound.

The uniqueness of the integral residual Q in R=S+2Q follows coefficient by coefficient from the absence of2-torsion. Above degree2d, S has no terms, so the residual completely controls whether the proposed upper bound holds. At degree2d, an odd coefficient cannot be cancelled by twice an integer coefficient. An entirely even coefficient polynomial can be cancelled. These statements remain correct with negative Laurent exponents and nonconstant framing coefficients.

Both displayed formal examples correctly show logical insufficiency: parity alone permits higher even terms, and congruence plus an upper bound permits the loss of an even top term. Neither example is represented as a realizable knot invariant. This limitation is essential, and it is consistently preserved.

## 4. Credited geometric scope and exact gap

Gruber's Proposition9 supplies the upper bound for nontrivial prime alternating links, with framing invariance. Theorem17 imposes nonzero top coefficient modulo2; Theorem18 covers algebraic alternating links. The cited8_16 and8_17 examples fail this criterion without disproving the desired equality. Composition does not supply the missing prime cases. The submitted discussion matches these quantifiers.

The remaining unrestricted upper-degree estimate and integer noncancellation mechanism are genuinely absent from this attempt. The package must retain original status unsolved, two approaches, and no new knot counterexample or novelty claim.

## 5. Reproduction and publication files

The author replay uses only the standard library and writes its receipt; the generated JSON is byte-identical to the submitted file. The independent checker also uses only exact standard-library integer arithmetic. Its11,010 assertions test normalization, framing shifts, injective substitution, residual uniqueness, upper-bound equivalence, odd-top survival, positive-degree clasp separation, the degree-zero boundary, and both formal failure mechanisms. These are algebra controls rather than geometric certification.

Copy the seven files listed in review_summary.json unchanged. Run author_replay/verify.py from its own directory; run independent_checks.py from any directory. Third-party PDFs and rendered source images are not part of the publication package.
