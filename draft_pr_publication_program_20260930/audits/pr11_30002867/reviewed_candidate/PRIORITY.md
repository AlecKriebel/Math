# Accepted-scope priority finding

**Current disposition:** already_solved by equivalent earlier methods, pending fresh acceptance review. No new paper or DOI.

The source asks whether a proper finite-positive-colength ideal in C[x_1,...,x_d] is generated globally by d polynomials, using its regular multiplication tuple. It does not require avoiding polynomial reconstruction or primary decomposition, or impose a degree-form/infinity condition. The convenient direct rank expression is not itself sufficient evidence of a new open-problem resolution.

Two independently developed checkable routes establish prior sufficiency:

1. Finite linear algebra recovers the faithful operator algebra B=C[M_i], isomorphic to R/I and of dimension N. Its coefficient kernel for the generators M_i−lambda_i gives a presentation of J_lambda=(M_i−lambda_i)B. Maximal determinant minors generate Fitt_0(J_lambda). On the selected local factor this is the zeroth Fitting ideal of its maximal ideal; on every other factor J_lambda is free rank one and that Fitting ideal is zero. Wiebe (1969), Satz 3, p.260, detects local CI by nonzero Fitt_0. Mohan Kumar (1978), Theorem 4, p.234, bounds the global generator count by d for locally CI ideals; finite colength gives the reverse height bound. This is a direct matrix-only criterion derived from old results.
2. The same faithful-algebra construction supplies matrix normal forms and unit coordinates to Abbott–Kreuzer–Robbiano (2005), Sections 2–3, which recover the defining ideal. Apply Kreuzer–Long–Robbiano's Algorithm 3.6 (2019 arXiv preprint, 2022 journal) and the same classical global bridge. This is a complete earlier-method answer to the literal target, including nonreduced and multi-support cases.

These are audit deductions, not claims that an earlier article explicitly named or advertised solving the 2015 question. No exact earlier D_2 formula was found; no first-priority claim follows. The candidate's stronger minimum-generator equation is itself a classical Koszul/Tor plus stable-generation corollary. No new efficiency, approximation stability or construction theorem is proved.

Detailed independent artifacts:

- [Equivalent-method proof, original source locations and eight exact consistency checks](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr11_30002867/priority/equivalent_methods/CHECKABLE_MAPPING.md)
- [Exact-question source/citation history and reconstruction adapter](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr11_30002867/priority/exact_question/REPORT.md)

Search coverage is bounded. The exact-question family inspected later Hermite, primary-decomposition, similarity and interpolation work. A 2026 ideal-complements chapter full text remained inaccessible. This gap limits any negative claim about explicit disclosures; it does not affect the positive sufficient-method certificate above. No external individual was contacted, and no external human peer review or formal proof verification is claimed.
