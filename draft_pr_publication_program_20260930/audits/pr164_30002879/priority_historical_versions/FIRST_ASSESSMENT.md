# Independent first assessment: historical Xu/Hermann versions

Sealed UTC: 2026-10-12T09:49:17.798006+00:00

## Fixed target and audit boundary

The target is the full ordinary Gerstenhaber algebra of B=[[A,M],[0,K]], A=K[x,y]/(x^2,y^2), M=A/(y), over every characteristic-two field, including injectivity and image of the original coefficient map gamma. The proposed presentation is K+(y,u)R in R=K[x,y,u,v]/(x^2,y^2), with u=partial_x, v=partial_y and formal Poisson bracket. The priority cutoffs are the original public disclosure on 2026-09-30 and this audit on 2026-10-12. No global literature absence or independence is certified.

This assessment used the current proof/source record, original source manifest, directly fetched Xu arXiv v1/v2 (20 pages each), Hermann arXiv v1 (45 pages) and v2 (47 pages), and OWR Question 5 (printed 1363). No author independent_review, parent/sibling priority verdict, or prior priority review was read. Repository metadata was used only for version dating and publisher access attempts.

## Initial conclusion

I did not locate an explicit presentation of the target full Lie algebra in these four arXiv texts. Xu already calculates the exact example's cohomology ring/decomposition, with compatible corner restriction machinery in Section 2.4. Hermann already gives the ambient characteristic-two group-algebra Gerstenhaber structure and preservation of the corner/coefficient maps. More strongly, Corollary 6.17 (already v1, page 32; v2, page 33) has an exact special case equal to this algebra and explicitly yields injectivity of the positive-degree corner map and surjectivity of the characteristic map. This is closer than merely applying Proposition 6.12.

The special case is checkable: take D=K[t]/(t^2), U=D^ev=K[a,b]/(a^2,b^2), and M=D with both a,b acting by t. Put x=a and y=a+b. In characteristic two this invertible change gives U=K[x,y]/(x^2,y^2) and M=U/(y), so Hermann's U[D] is exactly the displayed upper triangular B. Thus a broad novelty claim for injectivity is contradicted by a disguised prior special case. Degree-zero injectivity onto K+yA follows immediately from the displayed center exact sequence and scalar action.

The explicit coordinate characteristic map chi(x)=x, chi(y)=0, chi(u)=0, chi(v)=eta and full restricted Poisson bracket are not printed as the answer for this example in the inspected sections. They are an unstated direct consequence of these old theorems plus a short coordinate calculation, rather than a new structural theorem. There remains a distinction between availability of a short deduction and an explicitly published solution to Hermann's particular question. I would not label the full Lie target already explicitly solved solely because the ingredients are present.

Xu v2 adds the ordinary ring's polynomial subring description to Section 3.1, while v1 supplies the same nilpotent-coefficient decomposition and refers to Xu's earlier ordinary-cohomology paper. Hermann v1/v2 keep Corollary 6.17. Section 9 is materially changed; v1's conclusions about nilpotent-generated Gerstenhaber ideals must not be imported into the target. V2 still ends by posing future-work questions about a Gerstenhaber quotient, not supplying the target full bracket.

## Material gap

Hermann's published range 687--759 is 73 inclusive journal pages, whereas arXiv v2 is 47 pages. The arXiv metadata labels it final/to appear, but that alone cannot prove exact equivalence with the version of record. Direct ScienceDirect article/PDF requests return 403; the publisher API default request gives bibliographic XML only; explicit FULL XML/plain/PDF requests return 401. Both Hermann and Xu VOR full texts remain unavailable in this initial assessment. Therefore the conclusion is limited to the named arXiv versions, and the possibility of additional VOR text is an exact unresolved gap. No outreach initiated or drafted.

Completion estimate for this historical family audit: 60%. The main mathematical comparison is established; visual page checks, version differences, exact-source records and the final audit remain.
