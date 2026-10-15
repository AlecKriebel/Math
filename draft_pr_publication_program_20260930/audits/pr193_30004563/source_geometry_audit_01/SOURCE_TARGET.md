# Primary-source target, fixed before candidate inspection

## Primary-source reading

Primary sources were fetched directly and complete relevant pages rendered and visually inspected. In arXiv v2, printed page = PDF page. In the final article, printed p.788 = PDF page 8 and p.811 = PDF page 31. In OWR, printed p.1785 = PDF page 27. Source copies and page PNGs remain private under private_sources/.

- OWR 35/2020 printed p.1785: alpha-quads use opposite-side power balance. The text introduces alpha-immersions as graph immersions into these quads, explicitly permits edge intersections, states Theorem 4 for alpha>1, then conjectures three as the largest possible number of central points. It does not specify a formal local-topology condition for immersion on that page. Its reference [4] is Melotti-Ramassamy-Thevenin, arXiv:2003.08941.
- arXiv:2003.08941v2 Def.2.1 p.7: ordered quad ABCD obeys AB^alpha+CD^alpha=AD^alpha+BC^alpha. Nonconvex and nonproper quads, with edges intersecting off endpoints, are explicitly allowed.
- Defs.2.2--2.4 p.8: proper polygon = distinct vertices and Jordan polygonal boundary. An embedding has proper noncollapsed faces, no nonendpoint edge intersections, disjoint face interiors. A realization is any map of the quad graph's vertices into the plane satisfying the face equations. It has no specified cyclic-angle preservation, orientation, local injectivity, or disjoint-face requirement.
- Def.2.5 p.9 and Fig.6 p.8: alpha is fixed. Boundary A1,...,A6 must be six distinct points and the triples (A1,A3,A5) and (A2,A4,A6) must each be noncollinear. Incoming faces are A1 A2 A3 A0, A3 A4 A5 A0, A5 A6 A1 A0. Outgoing faces are A2 A3 A4 A7, A4 A5 A6 A7, A6 A1 A2 A7. A realization flip requires existence on the two sides; the proper flip additionally requires embeddings and the face orientations of Fig.6. These are separate conditions.
- Def.2.7 p.10: with distinct foci A,B and distinct through-point C, the construction curve consists of M such that A C B M is an alpha-quad. Thus |M-A|^alpha-|M-B|^alpha=|C-A|^alpha-|C-B|^alpha. Curves C2,C4,C6 govern incoming A0; C1,C3,C5 outgoing A7 (p.11). Remark2.8 p.11 proves third outgoing equation follows from two plus incoming balance.
- Theorem4.7 p.27: every real alpha>1 has the realization flip property. It is an existence claim, not uniqueness or an embedding theorem.
- Remark4.8 p.27, retained in the published 2023 article printed p.811: simulation-based expectation of at most three intersections of two construction curves sharing one focus for alpha>1 (and at most two for alpha<1). The displayed wording does not attach properness, embedding, or orientation qualifications. Degenerate coincident-curve cases need separate exclusion for any globally quantified statement; a counterexample with three distinct noncollinear foci avoids that issue.

## Exact audit target

For fixed alpha>1, find a six-point boundary satisfying Def.2.5, an incoming A0 satisfying all three incoming equations, and at least four distinct outgoing A7 satisfying all three outgoing equations. This suffices to contradict the informal OWR maximum-three claim under its explicit crossing-permitted interpretation and, more precisely, the published Remark4.8 construction-curve expectation. The target does not require a proper incoming embedding unless a submitted claim explicitly adds it. If a submission claims an embedding, test it separately. Showing five centers establishes a lower bound five, not that five is the global maximum.

## Independent equations and falsifiable checks

Let d_ij=|Ai-Aj|^alpha and d_iX=|Ai-X|^alpha. Incoming balances, all with zero residual:

1. d12+d_30-d_10-d23=0.
2. d34+d_50-d_30-d45=0.
3. d56+d_10-d_50-d61=0.

Outgoing balances:

4. d23+d_47-d_27-d34=0.
5. d45+d_67-d_47-d56=0.
6. d61+d_27-d_67-d12=0.

Summing incoming yields d12+d34+d56=d23+d45+d61, and summing outgoing yields its negative, so any two outgoing equations imply the third. For an exact construction, all input-point distinctness, both nonzero triple determinants, center distinctness, absence of zero face edges or repeated face vertices, and the power equations must be proved. Properness can be disproved by one strict nonadjacent segment crossing; general self-crossing is permissible for realizations. Strict inequalities must be certified independently from any approximations. Limits in which centers collide, face vertices repeat, triples align, or a nonzero implicit derivative disappears must be recorded.
