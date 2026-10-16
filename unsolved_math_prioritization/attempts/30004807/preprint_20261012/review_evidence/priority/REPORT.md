# Independent priority audit: PR464 / problem 30004807

## Recommendation and exact limits

**Continue the narrowly stated counterexample, conditional on the separate mathematical audits, after adding the older metric-family attribution. No disqualifying earlier printed resolution of the exact report conjecture was established in this bounded audit.** Do not describe the spacetime, affine lapse family, or its stress tensor as new. Do not claim historical first priority, a currently open status certificate, or a resolution of the physical charged-particle program.

There is strong positive prior evidence: the candidate’s underlying affine-lapse metric formula and Einstein-tensor formulas already appear in Dadhich–Kar–Mukherjee–Visser (DKMV), arXiv:gr-qc/0109069 (2001), equations (8)–(15), published 7 February 2002 in Physical Review D 65, 064004, DOI 10.1103/PhysRevD.65.064004. The negative-mass specialization is algebraically immediate. The existing BKTZ boundary-flux calculation makes the numerical defect a short subsequent deduction once convergence and the test space are established. The defensible contribution is the application to the later universal regular-ZAS conjecture, together with the explicit convergent defect and its scope. That is a modest counterexample application, not a new class of exact Einstein solutions or a new general Stokes theorem.

An older construction plus an easy new application is not evidence that the application was historically identified earlier. Conversely, failing to locate an earlier application is not a proof of novelty. This review therefore supports proceeding with that precise, qualified contribution; it does **not** support changing `claimed_solved` to `already_solved` solely from the DKMV match or solely from absence of an exact printed hit. The root reviewer must reconcile the independent mathematical/source reviews before promotion. The independent recommendation was frozen in a report before any previous audit or peer/root verdict was received. A subsequent root message confirmed the old-family match and conveyed separate math-audit status; it did not generate this recommendation. No previous audit text has been reviewed and no status or remote changes have been made.

## Source parity and chronology

I independently retrieved and inspected the official OWR report, including rendered printed pp. 2232–2233 (PDF pages 76–77). Its conjecture quantifies over spacetimes with the geometric admissibility described immediately before it: regular negative-mass ZAS on spacelike slices. No independent energy condition or specified electromagnetic constitutive model is stated there. The static slices used in BKTZ Sections 1.3–1.4 are the relevant exhibited foliation; universal regularity of every conceivable tilted slice is a different condition not justified by these pages. This is an interpretation of the literal source and technical setting, not knowledge of the authors' unstated intent. [Official report](https://ems.press/content/serial-article-files/46918).

The report belongs to volume 18 (2021), with a September 2021 workshop. The official publisher lists **26 November 2022** as its publication date. A manuscript may refer to the “2021 report conjecture,” but should not conflate volume/workshop year with public publication date. BKTZ v3 was submitted 23 August 2021 and the journal article published the same date; DKMV predates both. [Publisher chronology](https://ems.press/journals/owr/articles/8415343), [BKTZ history](https://arxiv.org/abs/1901.00813).

I also independently inspected BKTZ v3's rendered p. 6 footnote permitting boundary support and p. 9 Definition 2.1/equation (2.5), and read the proof's boundary calculation on pp. 10–11. The published 31-page article has the same relevant convention (Theorem 1.1, footnote 5, Definition 2.1). For this comparison, boundary-reaching compact support is essential. Tests compactly supported only in the punctured open manifold have no such flux; tests required to be smooth after collapsing the boundary sphere need not contain the exhibited radial field. Neither alternative is silently interchangeable with the published manifold-with-boundary convention. [BKTZ v3](https://arxiv.org/pdf/1901.00813v3), [published article](https://doi.org/10.1088/1361-6382/ac1853).

## Exact older-metric comparison

The DKMV primary PDF's pp. 3–4 were rendered and visually inspected. In its notation the metric is
\[
 ds^2=-\bigl(\kappa+\lambda\sqrt{1-2m/r}\bigr)^2dt^2
       +(1-2m/r)^{-1}dr^2+r^2d\Omega^2,
\]
and its isotropic equation (15) is
\[
 ds^2=-\left(\kappa+\lambda\frac{1-m/(2\bar r)}{1+m/(2\bar r)}\right)^2dt^2
       +\left(1+\frac{m}{2\bar r}\right)^4
         (d\bar r^2+\bar r^2d\Omega^2).
\]
Use the dictionary
\[
 m=-2a,\qquad\bar r=\rho>a,\qquad\kappa=A,\qquad\lambda=B.
\]
It gives exactly \(\phi=1-a/\rho\) and \(N=A+B(\rho+a)/(\rho-a)\). Moreover
\[
 r=\rho\phi^2=\frac{(\rho-a)^2}{\rho}>0,\qquad
 \sqrt{1+4a/r}=\frac{\rho+a}{\rho-a},
\]
where positivity on the exterior fixes the square-root branch. Thus this is the same geometry on the same smooth interior, including the main \(A=B=1/2\) example. DKMV's subsequent wormhole classification takes \(m>0\) because otherwise the spatial metric has an unavoidable naked singularity; the equation match is the negative-mass specialization, not a claim that their positive-mass wormhole classification proves this ZAS statement. [DKMV original](https://arxiv.org/pdf/gr-qc/0109069).

Their \(\tau\) explicitly means radial pressure, with opposite convention to a radial tension. With \(G_{\rm Newton}=1\), equations (9)–(11) give
\[
 8\pi\rho_{\rm energy}=0,\quad
 8\pi\tau=-\frac{2m\kappa}{r^3N},\quad
 8\pi p=\frac{m\kappa}{r^3N}.
\]
Our substitution gives
\[
 G^t{}_t=0,\quad G^\rho{}_\rho=\frac{4aA}{\rho^3\phi^6N},\quad
 G^\theta{}_\theta=G^\varphi{}_\varphi
          =-\frac{2aA}{\rho^3\phi^6N},
\]
exactly the frozen candidate's tensor. Hence a paper claiming this family or tensor as a newly discovered solution would have a definite priority defect, even though the frozen proof currently avoids an explicit first-priority claim.

The spatial regular/harmonic ZAS example is independently old: Bray–Jauregui Definitions 6–7 give the flat resolution with \(\phi=1+m/(2\rho)\), explicitly identify negative-mass Schwarzschild as regular and harmonic, and Definition 10 supplies its mass. At \(m=-2a\) the resolution normal derivative is \(1/a\), so the standard mass formula gives \(-2a\). This spatial assertion does not constrain the spacetime lapse. [Bray–Jauregui](https://arxiv.org/pdf/0909.0522).

## What the defect deduction does and does not inherit

For the old metric, the weighted radial component is
\[
 N\phi^6G^\rho{}_\rho=4aA/\rho^3\longrightarrow4A/a^2.
\]
Inserting this in BKTZ's boundary-flux expression for a radial boundary trace of time integral 1 yields \(-4\pi a^2(4A/a^2)=-16\pi A\), hence \(-8\pi\) for \(A=1/2\). This is my equation comparison/deduction. **BKTZ Theorem 1.1 cannot be applied as a black box to that example**: when \(A>0\) and \(B>0\), the nonzero spatial Einstein components have the excluded borderline order \((\rho-a)^{-5}\), whereas that theorem assumes a strict positive power improvement. The boundary calculation is reusable only after convergence is verified separately.

That check is supplied by the candidate's full-density cancellation, rather than integrability of the individual connection summands. Independently, the old tensor gives the Euclidean weighted density
\[
 D^i{}_j=N\phi^6G^i{}_j
   =\frac{Aa}{\rho^3}(6n_i n_j-2\delta_{ij}),\quad n=x/\rho.
\]
It is smooth on the closure of the exterior, symmetric, and traceless. Contraction with the conformal spatial connection vanishes by these two algebraic properties; the time component is zero. The scalar density reduces to \(D^i{}_j\partial_i\psi^j\), integrable for every smooth compactly supported boundary-reaching test. Its Euclidean divergence is zero and its inward boundary flux is precisely the frozen defect. These are checkable algebraic steps; they establish the gap between a familiar tensor and a legitimately defined counterexample integral. No distributional product or regularization theorem is being imported.

Within this family the vacuum control \(A=0\) has zero Einstein tensor, while \(A>0\) has nonzero radial flux. The counterexample violates the angular null energy condition. Earlier Reissner–Weyl–Nordström failures do not resolve the same conjecture because their singularity is excluded from the regular-ZAS class. The 2019 BKTZ v1 used tests on the collapsed Cartesian puncture instead of the later blown-up boundary convention; it cannot supply this exact test-class claim by unproved equivalence. Specific electromagnetic models with a lapse relation such as \(g_{tt}g_{rr}=-1\), positive matter conditions, or different zero-bare-mass singularities are distinct targets.

## Bounded priority search and positive comparison evidence

The ledger records 40 queries across exact-title, exact-conjecture, author/correction, ZAS/weak-Bianchi, old-family, thesis, and primary-domain routes. Full primary BKTZ v1/v2/v3 and the published version were retrieved. Relevant weak-identity hypotheses, examples, and outlook were compared; no exact regular-ZAS finite nonzero defect example or later correction was located there. The latest arXiv metadata still lists v3. This is a version-specific finding, not a guarantee against unpublished amendments.

The INSPIRE API supplied eight citing records for record 1712022, seven distinct works after proceedings duplicates. Six distinct arXiv works and the separate MG16 chapter were obtained. Relevant passages and bibliographies were inspected; whole documents were searched for the operator/conjecture terminology. This was a relevance screen and paragraph comparison, not a complete adversarial audit of every theorem in those papers:

| Primary work | Inspected relevance to this question |
|---|---|
| arXiv:1906.00308, EIH legacy I | p. 12: restricted weak-Bianchi program and existing RWN/Hoffmann comparison; no regular-ZAS counterexample application found. |
| arXiv:1906.00479, EIH legacy II | pp. 2, 4: weak conservation as a working hypothesis and specific electromagnetic vacua; no present application found. |
| arXiv:1901.08346, initial data/matter models | Relevant citation/bibliography located; concerns different initial-data questions. |
| arXiv:1909.04483, null distance/convergence | Relevant bibliography citation located; no present counterexample found by terminology screen. |
| arXiv:2506.08799, radiation reaction | BKTZ bibliography citation; primarily electromagnetic motion with a different scope. |
| arXiv:2508.06270, finite self-energy charge | p. 2: its specific BLTP lapse/product falls outside a special sufficient result; it does not identify this zero-density anisotropic example. |
| MG16 chapter, DOI 10.1142/9789811269776_0046 | Printed pp. 619–626, Section 4.2 (p. 625): BLTP with zero bare mass and different lapse; a separate open application. |

The explicit source URLs are in BIBLIOGRAPHY.json. The later author-hosted July 2021 Burtscher handout, 2023 Kiessling slides (PDF pp. 58–60), January 2026 Kiessling slides (pp. 79–80), and October 2022 Fields Institute talk abstract were inspected for later announcements. They give a restricted program, not the present counterexample; they cannot certify continued openness. Author publication pages supplied additional bounded coverage.

Coverage gaps: web indexing is incomplete; INSPIRE is a specialist index and counts proceedings duplicates; no exhaustive MathSciNet/zbMATH review was performed; no private/unpublished correspondence, seminar discussion, or author-intent clarification is available. The located 2015 Rutgers mildly-singular-spacetime thesis was not full-text inspected. A direct local download of the APS published metric paper returned HTTP 401; its official bibliographic page was accessible, while the full mathematical equation comparison uses the independently retrieved 2001 arXiv original. No inference of absence is made from that gap. No external contact was attempted or drafted.

## Required publication changes and acceptance boundary

1. Add DKMV to the proof/paper bibliography and state before the construction that the metric and affine-lapse family are its known negative-mass specialization. Give the exact \((m,\bar r,\kappa,\lambda)=(-2a,\rho,A,B)\) dictionary and the equations above. Carry this attribution into the abstract/introduction whenever the geometry's novelty could otherwise be inferred.
2. State the contribution as an explicit counterexample to the literal report conjecture **under the BKTZ boundary-reaching convention**, with a convergent nonzero defect. Preserve the exclusions about energy conditions, specified matter models, arbitrary tilted slices, and collapsed test fields.
3. Credit the existing flux method and distinguish its theorem hypotheses from the separately proved cancellation. A concise research note is justified; inflated claims about a new spacetime family or the entire matter/evolution program are not.
4. Use only a bounded priority statement: no earlier application was found in the inspected routes. Historical first priority is unestablished.

Items 1–4 are concrete publication-attribution/scope requirements, not a mathematical counterexample against the frozen equations. Item 1 is the new repair identified by this audit; the frozen proof already contains most of Items 2–4. No paper has been reviewed or changed by this agent. The root must verify final global repairs and commission the requested fresh package reviews before publishing.

