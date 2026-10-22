# Scope audit for second cohomology torsion of finite abelian quandles

13 October 2026. Target 30004307, source identifier OWR-17294-007.

## Disposition

**Defer on source scope.** The primary statement leaves the coefficient group unspecified and uses cohomological notation, while its principal cited results concern integral rack homology. The ambiguity affects the answer. The inspected sources do not explicitly correct the original statement or select a coefficient convention that reconciles all its surrounding assertions. This audit establishes a scope problem; it does not resolve the intended mathematical problem or certify its present-day openness.

## What the original source fixes

Victoria Lebed's contribution to Oberwolfach Report 51/2019 places Problem 1 on printed page 3220, PDF page 14. Its question concerns torsion in second cohomology for finite abelian quandles. The adjoining formulas genuinely have superscripts H² and T². The word and typography were checked against the PDF image, not inferred from text extraction. Printed page 3221 identifies the supporting references; its other problems and exact-sequence diagram are separate. [Original report, pp.3220-3221](https://ems.press/content/serial-article-files/46831?nt=1).

The input class is fixed by the displayed identity

(a ◁ b) ◁ c = (a ◁ c) ◁ b.

Thus the right translations commute. This must not be broadened to arbitrary medial quandles or narrowed to quandles whose structure group is abelian. No bound on size or orbit count, and no connectedness hypothesis, appears. The statement does not specify coefficients, distinguish rack from normalized quandle cohomology, or define a required form of computation. Its context expects examples with nonzero torsion and says a precise general description is missing. [Original report, p.3220](https://ems.press/content/serial-article-files/46831?nt=1).

For conventional discussion below, X is nonempty and coefficients have trivial action unless explicitly stated. Neither assumption supplies the missing intended coefficient group.

## What the cited results actually provide

Lebed and Mortier's arXiv v4 defines integral rack chains in equation (1.3), p.3. For r orbits, Theorem 7.1, p.14, states

H₂ᴿ(X; Z) ≅ Z^(r²) ⊕ T,  where T = ⊕ᵢ Tᵢ and Tᵢ = pₐ(G′), a ∈ Oᵢ.

The finite groups Tᵢ are quotients of the parameter/commutator group G′. Corollary 7.3 gives torsion-free H₂ for abelian structure group. Proposition 8.1, p.16, treats all two-orbit abelian quandles Uₘ,ₙ, with torsion (Z/gcd(m,n)Z)². Proposition 8.7, p.20, treats a particular cyclic-orbit family, including torsion-free cases with nontrivial G′. Question 1.2, p.3, asks about general parameter dependence. These are credited prior results, not a new solution or an independently audited proof. The quotient description alone does not evaluate every Tᵢ. [Lebed-Mortier v4](https://arxiv.org/pdf/1908.06745v4).

One sentence atop p.14 says “cohomology,” although the chain definition, proposition and theorem use homology. This is evidence of imprecise terminology in exposition, not an explicit amendment of the Oberwolfach problem. [Lebed-Mortier v4, p.14](https://arxiv.org/pdf/1908.06745v4).

García Iglesias and Vendramin use a left-quandle convention. Translating to a right operation requires transposing the arguments; one must not simply identify the displayed operation symbols. On p.6 they specify trivial coefficient action when none is named and state in Lemma 2.5

H²ᴿ(X; A) ≅ Hom(H₂ᴿ(X; Z), A).

They distinguish normalized quandle homology there. Their principal explicit cocycle formula in Theorem 1.1, p.3, assumes finite **indecomposable** X and a specified abelian coefficient group A with trivial action. It does not fix the omitted A in the all-finite Oberwolfach statement. [García Iglesias-Vendramin v3, pp.3,6](https://arxiv.org/pdf/1512.01262v3).

## Conventional readings have different outcomes

The following are standard coefficient consequences, recorded to expose the ambiguity. They are not new quandle-homology results or proposed solutions of the original question.

For ordinary rack cohomology with trivial coefficients, write T for the finite integral homology torsion above. Applying the cited Hom description gives

H²ᴿ(X; A) ≅ A^(r²) × Hom(T, A).

The displayed splitting is an abstract group description; no preferred splitting or evaluation of the unknown T is claimed.

- **A = Z.** Hom(T, Z) = 0, so H²ᴿ(X; Z) is free abelian and its torsion subgroup is zero. Equivalently, the degree-two universal coefficient theorem has no Ext contribution because H₁ᴿ(X; Z) is free on the orbits. This is a routine convention check, not an interpretation that reproduces the source's nonzero-torsion examples.
- **Ordinary normalized quandle cohomology with A = Z.** Its degree-one integral homology is likewise free on the orbits. The same universal-coefficient argument makes H²_Q(X; Z) torsion-free. Changing normalization alone does not repair the integer-coefficient reading. No normalized free-rank formula is needed for this conclusion.
- **Finite abelian A.** The displayed rack cohomology group is finite, so its whole group is torsion. Its size and structure depend on A as well as T; even the free homology summand contributes A^(r²). A coefficient-free answer is therefore impossible under this reading.
- **A = C× with trivial action, ordinary rack cohomology.** The finite dual Hom(T, C×) records homological torsion, but the full cohomology also contains (C×)^(r²). Its torsion subgroup contains (μ∞)^(r²), where μ∞ is the group of all complex roots of unity. In fact its torsion is abstractly (μ∞)^(r²) × Hom(T, C×). Thus the torsion of the entire cohomology group is not just the finite group T. Passing to a reduced group or taking only the finite character factor would require an additional convention.

The elementary one-element quandle already separates these choices: its ordinary rack H² with trivial coefficients is A. It has no torsion for A = Z, all of A for finite A, and all roots of unity as torsion for A = C×. This is a sanity check on coefficient dependence, not a counterexample to any precisely coefficient-specified conjecture.

Nontrivial coefficient actions and other cohomology theories are outside these conclusions. The source provides no basis for selecting them. None of the cases above determines every Tᵢ in the cited homological problem.

## Why an algorithm or a known quotient does not close this record

For a supplied finite operation table, the ordinary integral chain complex admits generic finite-matrix methods, including Smith normal form. Merely pointing to that procedure does not establish that the historical question intended algorithm existence, supply a new structural answer, or resolve the missing coefficients. No new algorithm was developed or tested here.

Similarly, the path-map image formula is already the content of the cited theorem. Rephrasing it as a complete computation would erase the unresolved evaluation step without evidence that this meets the question's intended success criterion. Restricted orbit counts, abelian structure groups, or the named cyclic-orbit families cannot be substituted for the full class.

The most plausible homological reading is to determine Tor H₂ᴿ(X; Z) throughout the finite commuting-translation class. That inference is strongly supported by the cited examples and formal definitions. It remains an inference: the report actually prints H², and no inspected correction authorizes replacing it silently.

## What would make the target ready

A ready contract must explicitly settle:

1. Homology H₂ or cohomology H².
2. Rack or normalized quandle theory, the coefficient group, and coefficient action.
3. Whether the target is the full torsion subgroup or a reduced/finite character component.
4. What output qualifies as computation beyond already available structural descriptions.

If the homological correction is explicitly adopted, an orbit-parameter formula or an effective evaluation of every orbitwise quotient could be assessed against the existing literature. This is a suggested clarified research direction, not a claim that the source demands a specific complexity bound or closed form. The prior quotient theorem and family computations must remain credited.

Until those choices are fixed, the honest classification is **source-scope deferred, mathematical target unresolved**. No new substantive proof search was undertaken. This audit does not change any queue record or claim a complete resolution.

## Evidence boundary

The three primary PDFs were locally rehashed and the relevant mathematical typography visually checked. Public source titles, URLs, PDF byte counts, hashes, and inspection locations are listed in `source_metadata.json`. The public packet contains this authored analysis and verification metadata only; it does not reproduce source PDFs, screenshots, extracted source text, or dataset contents.

The EMS landing page currently lists publication on 19 November 2020; the recovered Crossref record lists 18 November 2020. The report's volume year is 2019. That bibliographic discrepancy does not affect the mathematical adjudication. [EMS publisher record](https://ems.press/journals/owr/articles/17294).
