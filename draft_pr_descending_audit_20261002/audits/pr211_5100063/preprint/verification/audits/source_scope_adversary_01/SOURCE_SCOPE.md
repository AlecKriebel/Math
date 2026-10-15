# Source scope frozen before candidate reading

Frozen: 2026-10-15 10:19:45 UTC. Candidate proof, inherited reviews, and candidate checker results have not yet been read.

## Primary pins and reading

Read arXiv:2004.12497v11 (29 October 2020), title *Eighty New Invariants in the Elliptic Billiard*, introduction, Section 2, Section 3 table convention, Section 3.9 in full, Table 10 (printed p.12), its surrounding notes, and Appendix A notation. Visually inspected printed pp.3, 9–12. PDF SHA256: `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da`.

Read the actual journal companion *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Math. J. 7 (2021), 341–355, introduction, preliminary definitions, numbering table, Section 3.9 and Table 9; visually inspected printed p.350. PDF SHA256: `c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42`. Its Table 9 contains only inverse-distance sums, inverse-distance-product sums, inversive perimeter and angle sum. It does **not** contain k904,a, or a paired inversive area product. This is a coverage fact, not evidence for or against a later proof.

Read Stachel, *On the motion of billiards in ellipses*, European J. Math. 8 (2022), 1602–1622, introduction and Theorem 4.3 with its preceding parametrization. PDF SHA256: `9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8`. This is a potential canonical-coordinate input, not a proof of k904,a.

## Exact claim and definitions

The source domain is a real billiard ellipse E with semiaxes a>b>0, together with an inner, nondegenerate, confocal **ellipse** C. Write c=sqrt(a²−b²) and f±=(±c,0). Equivalently C has squared semiaxes a²−λ,b²−λ with 0<λ<b². This excludes a circle, hyperbolic caustics, the degenerate focal segment, and the boundary caustic. The source introduction explicitly defines the EB as a confocal ellipse pair.

For an ordered N-periodic billiard P=(P_i), let Q_i be the intersection of the tangent lines to E at consecutive P_i,P_(i+1), indices modulo N. The source denotes these Q_i by P'_i. They are not caustic contact points and not original orbit vertices.

For each original billiard focus f±, set W_(±,i)=f±+(Q_i−f±)/|Q_i−f±|², the unit-radius Euclidean circle inversion of Q_i. Define S±=(1/2) sum_i det(W_(±,i),W_(±,i+1)). The target k904,a is that S+ S− is constant as phase varies in each fixed Poncelet family for odd N. The straight polygonal edges join the inverted vertices; these are not inversions of the original edges as circular arcs. The product is not a product of unsigned region-union areas.

Do not replace Q by P (k903,a). Do not move the inversion centers to the foci of the outer vertex locus (the separate double-dagger notation used near k906). Do not infer this product from an individual-area invariance assertion.

## Domain and boundary obligations

The table labels simply 'odd', with no stated convexity or turning-number restriction. A robust general-N proof should therefore handle every regular odd least period and all admissible winding numbers, including self-intersecting star trajectories; evidence restricted to winding one must be labeled narrower. The source does not explicitly define N as least period. For an odd repeated N-cycle with odd least period n and repeat factor r=N/n, the signed-area sums multiply by r, hence the target product by r²; proving primitive odd cycles would cover that interpretation by this explicit argument.

Reversing traversal reverses both signed areas and preserves their product. Cyclic reindexing has no effect. Real outer intersections are finite: parallel tangents at distinct points of a central ellipse imply antipodal points, whose chord crosses the interior elliptical caustic and cannot be a tangent side. Outer intersections lie outside E, while f± lie strictly inside E, so real inversion centers are never hit. Complex poles may still be proof-critical and cannot be dismissed by this real-domain observation.

For the circle a=b, the original source assumption fails; any claimed circle result is a separate extension or limit. Hyperbolic and degenerate caustics likewise require separate argument if claimed. A proof confined to the stated ellipse-pair domain has not narrowed the source for that reason.

## Falsifiable success criteria before reading candidate

1. Every area in the proof/checker corresponds to the ordered straight-edge W above, with fixed original centers and unit radius.
2. Canonical parametrization is justified for the fixed elliptical caustic and all relevant odd primitive turning numbers; repetitions/orientation are either included directly or reduced explicitly.
3. All identities used on real families are valid throughout that regular family. Any meromorphic continuation has a specified period lattice, denominators, and complete pole argument; real boundedness alone does not prove absence of complex poles.
4. Tests sample multiple phases, semiaxis/caustic shapes, odd sizes and winding numbers, and check original billiard geometry; finite tests remain evidence rather than proof.
5. A source-accurate theorem may assert the source-domain product only. Open/priority/literature metadata must distinguish the actual arXiv row from the journal companion's smaller table.
6. The strongest claim and remaining gaps are reported without treating an inherited PASS, earlier PR, or queue status as a premise.

Source checkpoint: source scope identification 100%; this assigned audit overall approximately 30% complete; mathematical validity and status wording are unassessed at this checkpoint.
