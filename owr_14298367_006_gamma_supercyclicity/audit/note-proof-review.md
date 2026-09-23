# Publication manuscript: independent adversarial proof review

Review date: 2026-09-23 UTC. Completion estimate for this bounded proof review: **100%**. Reviewer: an independent Codex subagent. Scope: the exact manuscript below, its compiled PDF text, and the source-theorem applications. This is an AI proof review, not external refereeing or proof-assistant certification.

Inspected manuscript: `manuscript/note.tex`, version 1.0.0, dated September 23, 2026.

SHA-256 of inspected TeX:

```text
eb97833f5641964f055ca8ea4b80e8378bd3d25aaf8d0a03c9b86ead554ef1b7
```

The extracted mathematical text of `output/pdf/note.pdf` agrees with the inspected TeX. This review concerns mathematical content; it does not certify the PDF's visual layout. Any subsequent manuscript change should be checked against this hash and reviewed to the extent it affects the argument.

Update during review: the manuscript was reread after a concurrent wording change to Proposition 3. Its equivalent restatement says that the two operators are supercyclic for exactly the same subsets. The verdict also applies to this subsequently inspected TeX hash:

```text
5042779310f724069530b088dc099845b542b302017fd0f0102c8b819882eea2
```

## Verdict

**PASS. No substantive mathematical gap or mandatory correction was found.** The manuscript proves the full stated equivalence for every subset of the complex numbers under the source setting's separability, finite-(p), dissipativity, boundedness in both composition directions, and bounded-distortion hypotheses. Its shorter proof is valid independently of the submitted candidate's longer construction. The prior-theorem derivation is valid and supports the note's restrained attribution.

The mathematical claim is an affirmative answer within the stated scope. The manuscript appropriately does not claim the scalar criterion or amplification mechanism as new, and it does not assert that an earlier publication explicitly stated the answer to the later Oberwolfach question.

## 1. Printed theorem hypotheses

The main theorem inherits all needed assumptions from the immediately preceding paragraphs: a complex separable (L^p(X,\mu)), (1\le p<\infty); a bijective bimeasurable (f); upper measure bounds for both (f) and (f^{-1}); a wandering generator (W) of positive finite measure; and uniform bounded distortion for every measurable subset of (W) and every integer iterate.

The two measure bounds imply (0<m_j<\infty) for all integers (j). Indeed, iterative upper bounds give finiteness, and applying an upper bound to the inverse transformation of a putative null image of (W) rules out zero mass. They also give (m_{j-1}/m_j\le A) and (m_{j+1}/m_j\le B), making the weighted shift and both scalar translations bounded. The allowed null remainder is harmless: the union of all integer iterates of (W) is invariant, and both directions preserve null sets.

The abstract section deliberately weakens bounded invertibility to bounded forward translation. This is valid: its proof uses right translations only on finitely supported sequences. No bounded global inverse is silently used there. The nonzero and separable hypotheses on (E) remain explicit.

## 2. The shortened necessary tail estimate

The large-time hitting claim is correct because a finite union of complex lines through (S^n x) is closed with empty interior in the infinite-dimensional scalar sequence space. A dense (\Gamma)-orbit therefore reaches every nonempty open set at times exceeding any prescribed integer. No hypothesis on the size or topology of (\Gamma) enters this argument.

The support of a scalar supercyclic vector must be unbounded above: support bounded by a common index would force all its forward translates and all their scalar multiples to vanish above that index. Such vectors cannot approximate a coordinate vector farther to the right.

For a fixed finite nonempty (F), the manuscript consequently may fix a single (k\ge\max F) with (x_k\ne0). Approximations to (v=\sum_{j\in F}e_j) at increasing times (n_r) give both displayed estimates. The first follows from coordinate errors tending to zero and from the moving finite block (F+n_r) escaping to infinity in a summable weighted sequence.

For the second estimate, (k-n_r\notin F) eventually, so the fixed coefficient (x_k) occurs at a coordinate where the target is zero. The key direction of the shift inequality is correct:

\[
S^d e_t=e_{t-d},\qquad c_{t-d}^{1/p}\le\|S\|^d c_t^{1/p}
\quad(d\in\mathbb Z_{\ge0}).
\]

Taking (t=k-n_r) and (d=k-j\ge0) gives the printed bound. The constant involving (k,F,\|S\|), and (|x_k|^{-1}) is fixed as (r\to\infty). Crucially, both tails use the same actual scalar (\lambda_r\in\Gamma\setminus\{0\}); no quotient or modification of an allowed scalar is required.

## 3. Baire sufficiency and amplification

Finitely supported sequences are dense in (Y_E) because (p<\infty). In the perturbation (z=a+\lambda^{-1}R_n b), the error at the starting vector is controlled by the (c_{j+n}) tail, whereas the error at the target is controlled by the (c_{j-n}) tail. The displayed order and scalar factors are correct. Choosing the tail tolerance below the two available open-ball radii divided by (H) proves density of each target preimage union.

The Baire argument is legitimate for arbitrary (\Gamma), including nonmeasurable and uncountable sets. An arbitrary union of open preimages is open. The countable intersection is over a countable base of the separable Banach target space, not over (\Gamma). A point in that intersection has a single dense (\Gamma)-orbit. This directly proves the needed universality property without assuming a general transitivity equivalence for arbitrary scalar sets.

The quotient map defined by a bounded complex-linear functional on (E) is onto, bounded, and intertwines the translations. Its image of a dense orbit is dense. The empty and zero-only scalar cases are explicitly handled and produce neither dense orbit on these nonzero sequence spaces. Thus the amplification proposition has no missing case.

## 4. Composition model

The transported set function (\nu_j(C)=\mu(f^jC)) is a measure on (W) because (f^j) is an injective bimeasurable map. Bounded distortion gives equivalence to (c_j\mu|_W) with a uniform constant. The integral identity and both sides of the norm comparison have the correct orientation.

These same bounds justify use of equivalence classes under (J). The inverse construction glues countably many measurable representatives over the wandering partition, and the norm inequality proves (p)-integrability. It therefore establishes onto-ness rather than only a bounded embedding. The identity (JT_f=S_EJ) has the correct iterate direction.

The scalar diagonal isometry (D) uses (c_j^{-1/p}), and the convention ((B_wa)_j=w_{j+1}a_{j+1}) matches the computation (DB_w=SD). Both conjugacies are complex-linear, so they preserve the same prescribed scalar set exactly. Extension by zero makes (L^p(W)) a nonzero separable closed subspace of (L^p(X)), validating the application of amplification.

## 5. Separability caveat

The caveat is mathematically correct when the Bernoulli factors are the usual nondegenerate equal-probability factors. Distinct coordinate functions on the uncountable product are uniformly separated in (L^p), and so give nonseparability. For (c_j=2^{-|j|}), both finite-block tails tend to zero with (\lambda=1), whereas no operator on a nonseparable Banach space can have a dense projective orbit: such an orbit lies in the separable closed span of its countable ordinary orbit.

**Optional precision edit, not a proof repair:** replace the phrase about an uncountable Bernoulli product by the fully specified choice (\Omega=\{0,1\}^I), (I) uncountable, with product measure having each coordinate probability (1/2). This avoids any possibility of reading “Bernoulli” as allowing degenerate factors. The example's role and the theorem do not otherwise change.

## 6. Applications of previous theorems

Theorem B and Definition 4.1 of Abbar–Kuznetsova were rechecked in the preserved primary-source text. The two discrete groups used are second-countable, locally compact, noncompact, and abelian. Their weights are positive and locally (p)-integrable, since compact sets are finite. The permitted translations are bounded powers of the scalar translation; on the product group they have the same norm. No additional condition requiring the generated subgroup to be dense in the full group is imposed by Theorem B.

With counting measure, an exceptional set of measure less than one is empty. The scalar specialization therefore gives the simultaneous finite-set maximum estimates with the original allowed scalars. Projection onto the first coordinate proves the product-group criterion and yields amplification by (\ell^p(\mathbb Z)). The series defining (R\) converges absolutely, and its range contains every (e_k) via the input (2^k\delta_k). Its coordinatewise extension consequently has dense range, is bounded, and commutes with translation. A continuous dense-range intertwiner transfers dense orbits without requiring surjectivity. This establishes the printed derivation for general nonzero separable (E).

**Optional explanatory sentence:** the maximum form also permits (n>L), as asserted by reference to the full tail condition. For a fixed nonempty finite set, the product of the two positive maxima has a positive minimum over finitely many (n\le L). Taking both tolerances sufficiently small excludes all those times. This is immediate but not spelled out in Section 4.

Abbar's Theorem A and Theorem 2 were also checked using the primary publisher's indexed PDF text: [2019 paper, printed pp. 74–75](https://bulmathmc.enu.kz/index.php/main/article/download/55/93/364). The source gives a scalar tail characterization and a sufficient criterion involving a single sequence of permitted nonzero scalars. To apply it here, one diagonalizes finite blocks and uses the right translations on finite-support vectors. The manuscript's attribution is correct; its self-contained proof avoids dependence on any abbreviated source proof. Finite maxima, finite sums, and the source's one-coordinate formulation are equivalent here using the bounded forward-shift ratios.

## Disposition

No blocking mathematical change is required. The two optional clarifications above improve explicitness without altering the established theorem. The publication claim should remain the attributed explicit application stated in the abstract and introduction; this review supplies no new priority claim.

## Final release-hash approval

At 2026-09-23 13:57:54 UTC, I independently checked the two clarifying additions and confirmed the manuscript SHA-256:

```text
5950e74b23cb2be12626cb0c8d266cf3e3d6040c0dcfe8908a1fb49741796c94
```

The nonseparability example now explicitly uses $\{0,1\}^I$ with an uncountable index set and fair Bernoulli factors. This makes the coordinate functions uniformly separated: distinct coordinates differ on a set of measure $1/2$, so their $L^p$ distance is $2^{-1/p}$. The example and its contrast with the hypercyclic scalar shift are correct.

The added large-time explanation in Section 4 is correct. For fixed nonempty finite $F$, the product of the two quantities in the maximum criterion is

\[
\left(\max_{j\in F}c_{j-n}^{1/p}\right)
\left(\max_{j\in F}c_{j+n}^{1/p}\right)>0,
\]

independently of the nonzero scalar. Its minimum over the finitely many integers $0\le n\le L$ is positive. Choosing the tolerance smaller than the square root of that minimum forces $n>L$. An empty finite set requires no estimate.

**Final verdict for the hash above: PASS, with no remaining mathematical corrections requested.** The prior optional precision comments have been addressed. This approval is for the attributed explanatory note and does not introduce an originality claim.
