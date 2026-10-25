# Publication-scope review: positive tangent-bundle Seshadri constants

Checkpoint: 2026-10-24T23:51:21Z. Scope-review completion estimate: 100%. Overall catalogue work remains in progress.

## Verdict and independence

PASS for publication scope and faithful website wording, conditional on the root agent's separate mathematical review gate. I read the complete deposited five-page manuscript and its source independently before seeing any current analytic/adversarial review reports. I have not read those reports. No substantive scope mismatch requiring deferral was found. This verdict is not a substitute for independent proof checking and is not human peer review.

The website may describe the manuscript's theorem as establishing the statement of the Fulger–Murayama conjecture, but should not certify first historical priority or describe an AI-assisted audit as peer review.

## Bound source and date

- Zenodo record: https://zenodo.org/records/23331395
- Title: Positive tangent-bundle Seshadri constants characterize projective space.
- Author: Alec Kriebel; ORCID https://orcid.org/0009-0001-9320-500X.
- Declared publication date: 2026-10-12; version 1.0; DOI 10.5281/zenodo.23331395.
- Record creation timestamp is 2026-10-13T04:22:17Z, which is October 12 in Pacific time. Use the declared publication date in metadata; do not infer that the first public instant was October 12 UTC.
- PDF: paper.pdf, SHA-256 f3e5619c7e1560c45f7793b0f7e4dabfbbf66d08f568f3478b5bb8f35779ea17.
- Supplement: source-and-verification.zip, SHA-256 22bcb3d40fd734a6ee6e416319f329739395dcc66417da5f27e82d32a85694cf.
- content.json contains the complete deposited abstract, with notation normalized for readable text, and preserves the unrefereed status and extensive AI disclosure.

## Exact claim and scope boundary

Let X be a smooth integral projective variety of positive dimension over an algebraically closed field k. Positivity of the relative Fulger–Murayama Seshadri constant of T_X at ONE closed point x implies X is isomorphic over k to projective space. The manuscript works in arbitrary characteristic and retains the specified point; it does not assume X is already Fano, x is general, or T_X is globally nef.

The invariant uses the quotient convention P(E) = Proj(Sym E). Its curve ratio is the degree of the tautological class divided by the multiplicity at x of the pushed-forward curve; pushforward degrees include inseparability. It is not interchangeable with another vector-bundle positivity invariant. Although attached to a point, its definition tests entire curves, so popular copy should not suggest a purely infinitesimal local measurement.

Smoothness is essential for the advertised statement: Chang supplies a singular projective toric threefold with terminal singularities and positive tangent-sheaf Seshadri constant which is not projective space. The theorem does not classify singular varieties or varieties over nonalgebraically closed fields.

## Primary-source checks and credit

- Fulger–Murayama, Seshadri constants for vector bundles (2021), DOI https://doi.org/10.1016/j.jpaa.2020.106559. The final-numbering primary manuscript was read in memory from https://par.nsf.gov/servlets/purl/10198624. Its Theorem A gives the Fano, surface, and characteristic-zero general-point cases. Corollary 4.6 explicitly produces a rational curve through the SAME specified point. Proposition 4.8(1) is the arbitrary-characteristic Fano input. Conjecture 4.9 states the full one-point claim. These are proved inputs/target statement, respectively; the conjecture itself is not an input.
- The NSF PDF receipt is saved as fm-primary-receipt.json (528251 bytes; SHA-256 0c6930bb26fc8137ef3078659918e33aeae3cb320b54fd2ca0e8ff885de1dd2b). No third-party PDF was retained. The older arXiv v2 of 1903.00610 has different numbering and must not be used as a literal locator for final Conjecture 4.9.
- Fulger's 2019 Oberwolfach contribution, https://ems.press/content/serial-article-files/46833?nt=1, p. 3289, independently records the one-point question and established special cases.
- Chang, The Seshadri constants of tangent sheaves on toric varieties, https://arxiv.org/html/2211.17172v2 and https://doi.org/10.1016/j.jpaa.2025.108046. Theorem 0.2 handles smooth projective toric varieties in arbitrary characteristic. Example 0.4/2.4 supplies the singular counterexample. This was screened directly rather than inferred from a search summary.
- Abramovich–Oort, Stable maps and Hurwitz schemes in mixed characteristic, https://arxiv.org/abs/math/9808074, is the credited moduli framework. The Stacks Project trivial-inertia criterion, https://stacks.math.columbia.edu/tag/04SZ, is consistent with the manuscript's use. This scope review does not reprove every moduli theorem.
- Andreatta–Occhetta, Fano manifolds with long extremal rays, https://arxiv.org/abs/math/0504265 and https://doi.org/10.4310/AJM.2005.v9.n4.a5, provides context for the established numerical-generation method. The manuscript does not claim that mechanism as a new general method.

A bounded search did not identify a verified earlier resolution in the same full scope. This is not an exhaustive novelty or priority certificate. The final Fano identification relies on established theory; this review did not freshly reprove the entire Kollár monograph or every downstream reference.

## Argument and limitations to preserve

The proof first makes every rational-curve normalization through x very free. It minimizes degree absolutely over rational images through x, not just inside one chosen family. This eliminates broken maps and multiple covers in the degree-minimal pointed stable-map family; the manuscript also addresses contracted components and infinitesimal stabilizers.

Deformation theory gives surjective evaluation in arbitrary characteristic without appealing to characteristic-zero generic smoothness. The contracted marking section and line-bundle descent force numerical divisor classes to be proportional; the positive anticanonical class is ample. The proof then applies the already established Fano case. This dependence must remain visible.

Finite controls are not formal verification of stable-map geometry. The website should explain the mechanism briefly, not reproduce the verification log.

## Follow-up decision

follow_up is null. Dropping smoothness without a replacement is already false by Chang's example. Classifying possible positive constant values is an immediate reduction to projective space and its known values (2 on P^1 and 1 on P^n for n >= 2). Broader weaker-positivity or singular replacement questions were not precise and well-supported enough to advertise as new paper-worthy conjectures. Existing questions from Chang should not be recast as newly generated follow-ups.

content.json contains SEO title/description, faithful abstract, plain language, exact theorem, limitations, primary background, source files, and a professional invitation for substantive mathematical collaboration. No outreach was prepared or sent.
