# Independent graph and boundary analysis

Checkpoint: 2026-10-03 19:50:22 UTC. Best guess completion of this audit: 20%; completion of the original universal symmetry discovery: unknown. This is a pre-candidate source/mechanism seal. Only the routing SOURCE_MANIFEST.json, fresh primary source PDFs/text and rendered source pages were exposed. Routing descriptions themselves exposed claimed source scopes and an assertion of no later solution; neither was treated as verified. No candidate proof, code, history, current claim, queue, PR body, root review or sibling review has been read.

## Exact hypothesis and success criteria

For finite simple tripartite graphs with nonempty independent parts A,B,C, no A-C edges, and all four conditions

- d_B(a) >= x|B| for every a in A;
- d_A(b) >= x|A| for every b in B;
- d_C(b) >= y|C| for every b in B;
- d_B(c) >= y|B| for every c in C,

let m_C(G)=max_c |N_A^2(c)|/|A|. The universal guarantee psi(x,y) is inf_G m_C(G). The target hypothesis is psi(x,y)=psi(y,x) for all real x,y in (0,1]. A proof must cover all finite supports, every real parameter and all endpoints; a counterexample must prove a strict difference of universal values. One individual graph with different directional maxima does neither.

For each graph m_C is at least its infimum, so the greatest universally valid guarantee exists even when no graph attains that infimum. Exact extremizer existence is a separate claim. For every z>psi(x,y), a finite graph with m_C<z exists by the definition of infimum. This strict-witness formulation avoids requiring extremizer attainment.

## Source deductions and independent mechanisms

OWR 2019 Report1, Seymour contribution printed46-47 (physical PDF42-43), adds the B-to-A and C-to-B conditions and explicitly poses universal psi symmetry. The complete contribution was read and both pages rendered/viewed.

The arXiv v3 and EJC29(2)(2022)P2.47 editions have five authors, including Patrick Hompe. Their Theorem2.3 proves phi symmetry. Full2.1-2.3 proofs were read in both; published pages8-10 and v3 physical7-8 were rendered/viewed. Published OCR ! means >= and quotation-like glyph means <= in these inequalities; the visible page10 formula is phi(y,x)<=z, whereas v3 has the typo phi(y,z)<=z. The next paragraph says no analogous proof or counterexample was known there for psi or xi. This is a historical statement about those sources, not a certificate about later literature.

The phi proof eliminates supports and chooses separate replacement measures on A,B,C. Its missing-reachability complement H allows reweighting C so that reversed output maxima stay bounded. In psi, reweighting B must preserve BOTH A-to-B>=x and C-to-B>=y; replacing A and C must also preserve B-to-A>=x and B-to-C>=y. The phi lemma certifies only the designated directed constraints. Any extension must prove the other constraints explicitly; citing2.3 alone transfers the central difficulty.

The source2.3 opening chooses an exact extremizer at z=phi(x,y) without a separate general attainment argument in the displayed proof. The argument can instead be organized with a strict witness at z>phi(x,y), minimal finite support, and an infimum limit. This observation does not invalidate the established phi theorem. It is an audit requirement for new claims that invoke exact extremizers. Source12.1 uses exact equality witnesses and12.2 omits its proof; they should not be used as substitutes for a new proof of full psi symmetry.

Sections4 and12 were read in both editions, including all displayed proofs in those sections. The source's diagonal result psi(t,t)=1/floor(1/t) for t>0 follows from the constructive upper bound and4.2; its displayed inclusion of t=0 has no finite largest integer and is outside the defined domain. The source4.2 hypotheses x+ky>1 and kx+y>=1 distinguish strict and weak boundaries.

## Finite graph checks derived before any candidate exposure

1. Reversing the same graph to (C,B,A) preserves every four degree condition, with parameters (y,x). Its output is m_A(G)=max_a |N_C^2(a)|/|C|, which need not equal m_C(G). Explicit example: |A|=|B|=|C|=4; B-C is the matching b_i-c_i; A-B neighborhoods are {b1,b2,b3}, {b1}, {b2}, {b4}. All four minima are at least1/4, yet m_C=2/4 and m_A=3/4. Both extremal universal values at (1/4,1/4) are1/4 by four disjoint paths. Thus naive graph reversal is blocked as a proof of equality of maxima, and the asymmetric graph is not a counterexample to the original hypothesis.

2. Write P for A-B support and Q for B-C support. Two-step support R has R_ac=1 iff some b satisfies P_ab=Q_bc=1. Missing supports H_ac=1-R_ac have NO such intermediate b. All degree and support identities must be computed on actual Boolean support, not an ordinary matrix product mistaken for a Boolean relation. A repeated intermediate path does not multiply the number of distinct reached endpoints.

3. If x+y>1, N_B(a) and N_B(c) overlap for every pair a,c, so every c reaches all A and psi=1. At x+y=1, nonoverlap is possible only when both neighborhoods have exactly x|B| and y|B| elements and are complements. For irrational x, ceil(x|B|)+ceil((1-x)|B|)=|B|+1 for every finite |B|, so again every pair overlaps and psi(x,1-x)=1. This uses exact finite rounding; no numerical tolerance is permitted. For rational x=1/2, y=1/2, two disjoint three-vertex paths give psi=1/2. At x=1/3,y=2/3, a three-part cyclic example gives psi=2/3 by the elementary lower bound. These show why continuity, floating-point boundary tests and replacing >= by > would be unsafe.

4. For any k>=1, k disjoint three-vertex paths give an (x,y)-biconstrained graph whenever x,y<=1/k; m_C=m_A=1/k. If max(x,y)=1/k, the elementary lower bound max(x,y) makes this exact. A uniform complete blowup preserves normalized degrees and both reachability fractions. Unequal class sizes must be checked separately in all four directions; zero-size classes disappear, and support reachability can shrink after deletion.

5. Rational weights admit an explicit finite unweighted graph by integer class multiplicities after common-denominator clearing. A claimed finite witness requires actual nonnegative integer class sizes, all four integer degree bounds (with ceilings), correct absence of A-C edges, and distinct-endpoint reach counts. Irrational weighted witnesses or rational approximations at active equalities require justification; ordinary density of rationals does not automatically preserve several non-strict inequalities at irrational boundary parameters.

## Planned independent controls and exact remaining gap

Controls will materialize finite graphs for the directional-max example, disjoint paths, rational x+y=1, complete regimes, nonuniform blowups and a deleted zero class; compare explicit two-step endpoint sets with Boolean support multiplication; test integer ceilings and strictness without floating arithmetic. The primary published figure's matrix will be independently transcribed/tested only after this derivation is sealed. Candidate finite checks will be treated as supplementary evidence.

Strongest verified claim so far: correct source identification and definitions; direct finite graph reversal preserves feasibility but not individual maxima; exact universal values in the elementary regimes above. Exact remaining gap: no mechanism here proves universal psi symmetry away from these regimes, and no strict universal-value asymmetry has been proved. The simultaneous replacement-weight/support conditions remain central, not solved by phi2.3.

Private raw PDFs, extracted full text, renders, and lossless command streams are retained under graph_boundary_review/private. They are not for publication. Public receipts may identify hashes, source URLs, read scopes and exact regeneration recipes without redistributing primary text. Initial bootstrap commands before the logger are explicitly recorded as a capture exception; no blanket perfect contemporaneous-capture claim is made.
