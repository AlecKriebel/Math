# Independent rate-domain addendum — Zenodo 21753997

**Disposition: demonstrated missing domain hypothesis in the literal statement of Theorem 3.1; defer this formulation for later correction.** The proposed counterexample is valid. This addendum qualifies the earlier adversarial review's acceptance of Theorem 3.1: that review treated rational input rates as the theorem's scope, but a reread does not find that input restriction explicitly stated. The frozen report, verdict, log and evidence files have not been modified.

This finding does **not** refute the clean or frozen integer constructions, their equilibrium conic, GCD computations, radical decompositions, fixed-support integral optimization, or frozen stability classification. It is a counterexample to the rational-parameter necessity in the unrestricted positive-rate reading of the published complete-family theorem. No source or proof repair was attempted.

## Exact published hypotheses

The current 14-page v2.0.0 PDF is SHA256 `fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b`; the source `releases/v2.0/source/MANUSCRIPT_V2.md` is SHA256 `e2ac3cf9556eb1bacf53a76dd09963a5a60ca2d47c7fe2c62a0bdfa164dd18db`.

- PDF page 2, Introduction, source lines 28–35: the mass-action model has “positive rates,” with real positive concentrations. No rationality condition is attached to the rates.
- PDF page 3, equation (6), source lines 138–142: the conic ideal is explicitly \(\mathfrak p=(L,Q)\subset\mathbb Q[x,y,z]\).
- PDF pages 4–5, Theorem 3.1, source lines 215–244: it starts with the mass-action field \(F(k)\) on the fixed support, and states that all three coordinates belong to \(\mathfrak p\) **if and only if** the rates have the displayed form for some \(a,b,c,d\in\mathbb Q\).
- Formula (10) explicitly sets \(k_{29}=a\), \(k_{43}=b\), \(k_{95}=c\), \(k_{98}=d\). These are uniquely forced free coordinates, not parameters that can be replaced by another tuple representing the same rates.

I reread the actual model and theorem, checked the PDF text, and searched all occurrences of rational/real/rate-domain language in the complete current manuscript. There is no explicit statement that all input rates are rational. A rational ideal, a rational matrix and exact rational computations describe coefficients and computational methods; they do not logically imply rational individual reaction rates. The counterexample below satisfies literal membership in the rational ideal, so the issue persists even if that membership is read strictly rather than as base extension to real coefficients.

## Exact counterexample

Start with the clean rate vector in the manuscript and let \(\eta=\sqrt2/10\). Change only

\[
k_{24}=1629+\eta,\qquad k_{27}=1-3\eta,\qquad k_{29}=653+\eta.
\]

All other seventeen rates remain the published positive integers. Since \(0<\eta<1/5\), the only decreased rate satisfies \(k_{27}>2/5>0\). The support remains exactly the same connected reversible graph, with the same stoichiometric rank and positive compatibility class.

All three changed reactions have source complex \(2=3Z\), hence source monomial \(z^3\). Their target-minus-source vectors are

\[
v_{24}=(0,3,-3),\quad v_{27}=(1,1,-2),\quad v_{29}=(3,0,-3).
\]

Therefore the change in the complete mass-action field is identically

\[
\Delta F=\eta z^3\bigl[v_{24}-3v_{27}+v_{29}\bigr]
=\eta z^3(0,0,0)=0.
\]

The new field is exactly the same rational polynomial triple as the clean field. Independent reconstruction of all twenty reaction terms and reduction over \(\mathbb Q\) modulo \((L,Q)\) yields the three zero normal forms. Thus the theorem's left-hand condition is satisfied literally in \(\mathbb Q[x,y,z]\).

However, its right-hand condition is impossible: formula (10) forces

\[
a=k_{29}=653+\sqrt2/10\notin\mathbb Q.
\]

No different rational tuple can reproduce the modified rate vector, because this rate is itself the parameter \(a\). Equality of the induced vector fields does not make different rate vectors the same object: the theorem expressly classifies the twenty directed rates.

`control.py` reconstructs the graph and both fields from the manuscript tables without importing the frozen review's helper or submitted verifier. It checks exact cancellation, rational coefficients of the resulting field, rational ideal membership, positivity of every rate, irrationality of the forced free coordinate and preservation of every frozen review file. Its output is `result.json`.

## Classification and exact scope

Under an **explicit rational-input restriction**, this example would be excluded. Such a restriction was the scope assumed in the earlier review, and the previously checked rational kernel classification remains supported. But it is not explicitly imposed on \(k\) in the published statement or global model. Reading the theorem as one about an implicitly chosen \(\mathbb Q\)-vector space of rates is a possible intended convention; it supplies the missing hypothesis rather than deriving it from the written antecedent.

This is more than the familiar observation that an irrational-rate field may not lie in a rational polynomial ring. Here the field does lie in that ring and in the stated ideal because the reaction-to-field map has a nontrivial kernel. Consequently, the rational-field condition cannot substitute for a rational-rate hypothesis. The exact positive counterexample establishes a literal failure of the claimed implication unless the domain is restricted by interpretation.

The underlying linear-family mechanism is not contradicted. The perturbation changes the value of the same free coordinate \(a\), and its cancellations are consistent with the existing displayed formulas when interpreted over an appropriate scalar field. That observation identifies the extent of the defect; this addendum does not provide or implement a revised theorem. Likewise, it does not extrapolate the domain issue into a failure of the separate integer examples.

**Strongest supported conclusion:** the earlier exact integer and rational-input results remain supported, while the published unrestricted positive-rate reading of Theorem 3.1 has the explicit counterexample above. The exact remaining issue is a missing stated input-domain hypothesis in that theorem. The original general PASS should not be used to certify this literal quantifier. Stop here under the defect-and-defer protocol; no repairs or further broad replays were undertaken.

This is an AI review addendum, not human peer review or a novelty certificate. It uses no sibling verdict as mathematical evidence; the proposed perturbation was supplied as a target and independently checked against the published definitions.
