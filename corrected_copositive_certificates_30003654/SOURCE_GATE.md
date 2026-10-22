# Source gate: row 1847 / ID 30003654 / OWR-15957-007

Inspected 2026-10-21 UTC. No prior recovery directory existed. No queue or GitHub changes made.

## Disposition

**Exploratory/underspecified question, with substantial relevant later results; not a well-posed theorem to mark solved.** The primary report asks what further roles a certificate might play in extending copositive reformulations. It does not designate a unique conjecture, target class of extensions, complexity bound, or success criterion. Do not replace this with a generic Positivstellensatz question, or count an already published conditional certificate as a new solution.

The normalized dataset statement asks for hypotheses for certificates on S intersect h^{-1}(0), expressed through nonnegative polynomials on S and the ideal (h), to extend copositive formulations and optimization methods. This is broader than a definite proposition. Dataset status is open, but that label is curation, not primary evidence of a mathematically specified unresolved assertion.

## Provenance

The exact ID 30003654 occurs once in problems.json with problem_number OWR-15957-007. The exact key OWR-15957-007 is ABSENT from research_results.json (6,701 keys); no differently keyed entry was substituted. Full files were freshly hashed, rather than trusting a prior manifest. The package disposition is UNSOLVED, 5/5 approaches; no queue mutation is performed by this package.

Primary report: Juan C. Vera, “Positive polynomials on unbounded domains,” joint work with Luis F. Zuluaga, in Copositivity and Complete Positivity, OWR 2017/52, report PDF pages 38–39.
- https://publications.mfo.de/handle/mfo/3616
- https://doi.org/10.4171/OWR/2017/52
- https://publications.mfo.de/bitstream/handle/mfo/3616/OWR_2017_52.pdf?isAllowed=y&sequence=1

The MFO record dates the workshop 29 October–4 November 2017 and cites Oberwolfach Reports 14 (2017), 3071–3120. The dataset's parenthetical 2018 is not the workshop year.

The report's central object is a closure certificate based on nonnegative polynomials plus h times an arbitrary polynomial. It discusses copositive rather than exclusively SOS certificates, and potential LP hierarchies using Pólya. It gives no formal open conjecture or computational complexity claim.

## Contemporaneous precise formulation and caution

Primary companion: Peña, Vera, Zuluaga, Positive polynomials on unbounded domains, arXiv:1709.03435v1, 11 September 2017, pages 4–6.
https://arxiv.org/abs/1709.03435
https://arxiv.org/pdf/1709.03435

Write P_d(S)={p in R[x]: deg p≤d, p≥0 on S}. The ambient topology is the finite-dimensional coefficient topology on R_d[x]. For closed S contained in a closed pointed convex cone K, and h in P_d(S), the certificate cone is

C_d(S,h) = closure(P_d(S) + h R_{d-deg h}[x]).

For d≥2, the paper's Theorem 2 asserts C_d(S,h)=P_d(S intersect h^{-1}(0)) iff
(S intersect h^{-1}(0))^infinity = S^infinity intersect tilde(h)^{-1}(0).
The horizon cone consists of limits lambda_k x_k, with x_k in S and lambda_k decreasing to zero. This is a fixed-degree closure result, not finite exact decomposability for every weakly nonnegative p, and not finite convergence or polynomial-time optimization.

**Source-level defect requiring caution:** Theorem 1 uses tilde(p) defined as the highest *actual-degree* homogeneous part of p in a formula for C_d, although d is only an upper bound on degree. The PDF page 5 was rendered and visually checked: this is not an extraction artifact. The preprint also visibly contains an unfinished proof marker in Example 1. Do not cite the displayed Theorem 1 as literally correct without a degree convention repair and proof audit.

### Authored check of the degree defect

Take S=K=R_+², d=4, h(x,y)=(xy+1)(x-y)², and p(x,y)=1+x-y.
All printed assumptions of Theorem 1 hold. Put t=y-x. Then

p+h = 1-t+(xy+1)t² ≥ 1-t+t² = (t-1/2)²+3/4 on S.

Therefore p=(p+h)-h lies in P_4(S)+h R_0, even before closure. But the actual-degree leading form of p is x-y, which is negative at (0,1). That point belongs to S^infinity intersect tilde(h)^{-1}(0), because tilde(h)=xy(x-y)². Thus the displayed right-hand condition in Theorem 1 fails for a member of the displayed left-hand cone.

This check refutes the literal notation of Theorem 1. Using the degree-d homogeneous component of p (zero when deg p<d) avoids this particular counterexample. This report does not assert that this change alone proves every statement of that preprint, nor that the discrepancy settles the OWR research program.

## Later primary development

Kuryatnikova, Vera, Zuluaga, arXiv:1909.06689:
- v1 (14 September 2019), Copositive certificates of non-negativity for polynomials on semialgebraic sets.
- v5 (22 March 2024 submission; PDF internally dated March 25), Reducing nonnegativity over general semialgebraic sets to nonnegativity over simple sets.
https://arxiv.org/abs/1909.06689
https://arxiv.org/pdf/1909.06689v1
https://arxiv.org/pdf/1909.06689v5

The versions have different formulas: do not silently cite v1's unscaled lifting as the current v5 theorem.

In v5 Definition 2 and Theorem 2 (pp.22–23), S={x:g_i(x)≥0} must be nonempty. Strong positivity means p>0 on S and its leading form is >0 on every nonzero point of the set defined by the leading forms of the displayed constraints. This condition depends on that description of S, and is stronger than p≥0 or merely p>0 on S.

Set D=max_i(deg g_i, ceil(deg p/2)) and L=1+sum y_i+sum z_i. Theorem 2 gives a strictly positive orthant polynomial F of degree at most 2D satisfying

L^(2D-deg p) p(y-z)
 = F(y,z,L^(D-deg g_1)g_1(y-z),...,L^(D-deg g_m)g_m(y-z)).

It additionally imposes weighted leading-form positivity on F. Thus this is a concrete conditional fixed-degree lifting to a simpler cone, not unrestricted weak-nonnegativity completeness. Proposition 9 subsequently supplies a Pólya-type non-SOS certificate with an existential extra exponent r. The displayed degree 2D is not a universal bound on all later hierarchy levels or a polynomial-time complexity guarantee. These are genuine developments of the report's theme, not a uniquely identifiable resolution of its entire open-ended question.

## Acceptance boundaries

- Preserve weak versus strict/strong positivity and actual degree versus ambient degree.
- Preserve closure versus a single finite decomposition.
- Preserve h nonnegative on S, pointed-cone containment, and horizon compatibility when discussing the 2017 formulation.
- Do not assume S is semialgebraic in the 2017 closed-set formulation; the later lifting theorem does assume a basic semialgebraic description.
- No source text, PDFs, or dataset contents belong in a public patch. No source copies are included.
- A defensible queue finding is “source gate: exploratory generalization question; conditional horizon/strong-positivity results recovered; no precise novel theorem selected.” A solved claim is not justified.
