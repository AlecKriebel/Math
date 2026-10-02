# Source resolution: the unrestricted assertion is false

Problem30003538 / OWR-15577-010 is **already_solved, 0/5 proof-attempt turns**, subject to independent source review. This packet verifies an existing negative answer. It presents no new harmonic-analysis proof and makes no novelty claim.

## Exact original scope

The complete original contribution is Stefano Meda, *Some new results concerning Hardy spaces on the hyperbolic disc*, joint work with Alessio Martini, Maria Vallarino and Sara Volpi, OWR34/2017, printed pp2135–2137. The workshop occurred in2017; the report was published in2018. The imported record's expanded title is not the source of the mathematical hypotheses.

The question asks about every complete, connected, noncompact Riemannian manifold. With L the nonnegative Laplace–Beltrami operator, the operators are the unshifted geometric Riesz transform ∇L^(-1/2), the heat semigroup exp(−tL) and the Poisson semigroup exp(−t√L). The maximal operators use the supremum of the absolute value for all t>0. Both absolute-value signs, easily lost in text extraction, were visually checked on printed p2135. The defining functions belong to L1, with the Riesz magnitude or respective maximal function also in L1.

There is no global doubling hypothesis in this unrestricted question. The following paragraph discusses a *separate restricted setting*: doubling measure, positive injectivity radius and a Ricci lower bound. That paragraph is not a license to insert doubling into the earlier general question.

## The original source already states counterexamples

On printed p2136, Theorem1(a) states that the heat, Poisson and Riesz Hardy spaces are different on Riemannian symmetric spaces of noncompact type and real rank one. The paragraph immediately preceding it names the hyperbolic disc as the prototype. Thus the source already supplies admissible manifolds for which the proposed three-way equality fails.

This is enough to answer the universal equality question negatively. It does not classify every complete noncompact manifold, nor settle a different question restricted to doubling geometry. The subsequent theorem in the very same contribution must not be omitted when assessing whether the introductory question remains open.

Theorem1(b) there concerns the *modified* Riesz space, whose functions are also required to belong to the local Goldberg space h1. It proves non-density of its compactly supported functions. That statement alone must not be promoted to an assertion about the full Riesz Hardy space defined merely inside L1.

## Detailed later primary source and the full Riesz space

Martini–Meda–Vallarino–Veronelli, *Inclusions and noninclusions of Hardy type spaces on certain nondoubling manifolds*, arXiv:2207.02532v1, is the accessible detailed primary text. The published work appears in Journal of Functional Analysis286(3) (2024),110240, DOI10.1016/j.jfa.2023.110240. Publisher and institutional metadata corroborate its conclusions. The institutional version-of-record PDF returned HTTP403; theorem numbering here is explicitly that of the retrieved author preprint.

Its equations(1.1)–(1.3) use exactly the global operators above. Its class M requires completeness, connectedness, noncompactness, positive injectivity radius, a lower Ricci bound and a strictly positive spectral bottom. Rank-one noncompact symmetric spaces are among its examples, so these additional hypotheses narrow a legitimate counterexample class; they do not weaken the negative answer to the unrestricted assertion.

For that class, Theorem2.10 identifies the **full** Riesz Hardy space with X^(1/2), with equivalent norms. Corollary2.11 then gives the precise atomic obstruction on rank-one noncompact symmetric spaces: compactly supported members are not norm dense. Corollary3.4 gives a strict inclusion of the Riesz space in the Poisson space throughout class M. Corollary4.9 states, on Damek–Ricci spaces S,

- H_R^1(S) is properly contained in H_P^1(S)
- H_H^1(S) is properly contained in H_P^1(S)
- H_R^1(S) is not contained in H_H^1(S)

These three statements imply pairwise distinction. We do not reverse the last noninclusion or assert an unproved relation between H_H^1 and H_R^1.

The earlier Martini–Meda–Vallarino paper, arXiv:1908.10057v1, Theorem4.15, proves the compact-support obstruction for noninteger X^γ on rank-one symmetric spaces. Taking γ=1/2 is legitimate. Its introduction expressly stops short of identifying the full Riesz space, which is why the later Theorem2.10 and Corollary2.11 matter. The later corollary's short deduction and the cited earlier k=1 argument were read; this packet does not independently certify all analytic dependencies, kernel estimates or spectral calculus in either paper.

## Meaning and limits of the atomic conclusion

The verified obstruction rules out decompositions converging in the Hardy norm into compactly supported atoms belonging to that space: every finite partial sum would still be compactly supported, making the compactly supported members dense. Non-density prevents such a characterization.

It is not a claim that no possible abstract expansion, noncompact molecule system or frame can exist. It also does not assert that the heat or Poisson Hardy spaces never have atomic descriptions. The conjunction asked in the source already fails by the equality counterexample, and the full Riesz atomic obstruction provides the stronger, correctly scoped negative information available in later work.

Local maximal functions, restricted to0<t≤1, define different spaces; their later equivalences do not restore the global three-way equality. The Riesz operator here has no positive spectral shift. The standard Euclidean theorem remains consistent because Euclidean space has zero spectral bottom and is not in class M.

## Verification boundary

This is a source-resolution packet. The source statements, definitions, hypotheses, version identity and elementary implications are checked; the long published analytic proofs are cited, not newly proved or exhaustively re-audited. `verify_source_alignment.py` supplies small exact logical consistency checks of the reported inclusion directions and parameter matching. It is not a numerical or finite proof of a Hardy-space theorem.

The original OWR Theorem1(a) independently suffices for the negative equality answer; the later paper strengthens the full Riesz atomic conclusion. No substantive author proof-attempt turn was consumed. Further research under additional geometric assumptions would be a different task.

## Primary references

- Original report: https://ems.press/content/serial-article-files/46697 ; metadata https://ems.press/journals/owr/articles/15577
- Detailed later source: https://arxiv.org/abs/2207.02532v1 ; publication https://doi.org/10.1016/j.jfa.2023.110240
- Earlier fractional-space source: https://arxiv.org/abs/1908.10057v1 ; publication https://doi.org/10.1007/s10231-020-00956-9
