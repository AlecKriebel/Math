# Review summary of the complete Ford-circle proof audit

## Decision

Accept the existing proof of the exact Propp-Kenyon target in Alper Ferudun's version 1.1 preprint. No missing argument or theorem-changing patch was identified. PROOF.md reproduces the complete authored audit; the summary below locates its essential obligations without duplicating that full report.

This is an AI-assisted, unrefereed proof-audit edition. Acceptance records an independent internal AI audit of Alper Ferudun's existing version 1.1 proof; it is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical reconstruction, every written formula and example, and all acceptance qualifications are retained. Executable code, raw computational datasets, copied source PDFs or text, source renderings, raw search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution.

## Discharged obligations

- Geometry, Section 1: D(x,s) has radius s^2 and center (x,s^2). The necessary and sufficient nonoverlap condition is |x-y|>=2st. The boundary inequalities give s<=ab/(a+b), with a unique local greedy insertion. The connected-component argument identifies the algebraic gap with the original bounded geometric region. Rational interior points establish countability, and null disk boundaries identify area sum with union area.
- Complete greedy family, Section 2: determinant-one mediants give every positive primitive pair exactly once. The identity x_(v')-x_v=2 det(v,v') s_v s_(v') proves actual pairwise disjointness. Nonnegative primitive-pair decomposition gives sum w(s)=w(a)w(b). The convergence threshold p>2 and the totient divisor identity give G_p(1,1)=zeta(p-1)/zeta(p)-1.
- Universal analytic step, Section 3: the derivative expression has a positive prefactor times Omega. Its expansion by x-degree has omega_0=U_4, omega_1=U_2+U_3 and omega_n=nU_1+U_2 for n>=2. The explicit coefficient formulas prove nonnegativity in every degree, including all low-degree cancellations, and Omega(q,x)>=q^5/6>0 for positive variables. Entire exponential-polynomial expansions justify the conclusion at all scales. A finite coefficient grid is not used as its proof.
- Chain induction, Section 4: every degenerate split has two strictly smaller positive induction parameters. For a nondegenerate chain, the two-size deformation preserves L and has a nontrivial compact feasible component. Its endpoints cannot escape through zero sizes: the (0,2) and (1,3) constraints exclude the two parameter boundaries, including k=2. Additional contacts at the component endpoints allow induction. The exact two-factor objective and log-convexity imply the endpoint bound. Disconnected feasible sets and contacts with fixed endpoint disks are handled explicitly.
- Finite optimization, Section 5: a compact box with zero-size padding gives a maximizing packing for each finite cardinality. A shift-and-enlarge argument establishes contacts on both sides without assuming that tangent neighbors are immediately adjacent in base-point order. Extracted tangent chains and residual gaps invoke a separate cardinality induction, so there is no circular use of the chain theorem. Supremums of finite subsums yield the theorem for every countable packing.
- Powers and area, Section 6: scaled auxiliary inequalities integrate against t^(p-1)dt. All exchanges use nonnegative summands; Gamma(p)zeta(p) is positive and finite. Taking p=2alpha>2 proves radius-power maximality, and p=4 proves the exact attained area. Positive Borel scale superpositions use monotone convergence without an unstated sigma-finiteness requirement.
- Limitations, Sections 6-7: the four-disk authored example disproves an extension to every nondecreasing weight. Local strict log-convexity does not establish uniqueness of an arbitrary infinite maximizing packing. The alpha<=1 greedy sum diverges and is not a finite optimum claim.

## Source review and supporting checks

The original report's relevant page, PDF page 62 / printed page 722, was read and visually inspected; its other 69 pages were not audited. All twelve pages of Ferudun's version 1.1 were read and visually inspected. The mathematical proof in Sections 2-6 was reconstructed. The source author's code, numerical certificates, priority narrative and self-assessment were not proof premises.

The original audit independently recomputed the source hashes. A later attempt to reopen the Zenodo record, DOI and API failed; the successful same-day official retrieval remains the source of the pinned bytes. This edition preserves that distinction and makes no fresh source-retrieval claim.

The historical independent checker reported 242,391 successful checks: symbolic identities, a coefficient grid through degree 200 in each variable, and exact rational geometry in six boundary configurations through m+n<=24. The six configurations each contained 179 internal disks and 16,290 disk-pair comparisons. These are bounded diagnostics. They do not prove the all-degree inequality, deformation endpoints, countable reduction or final theorem. Source-author programs were not executed and random numerical optimization was not used.

The complete proof, rather than any numeric check count or integrity hash, is the basis of acceptance. No uniqueness, novelty, exhaustive priority, external human peer-review or formal-certification claim is made.
