# Independent audit of additive constancy for the original Borel QHI

## Decision and exact scope

Accept the corrected five-file derivative at the bounded scope stated below. The original proof's contraction mechanism is valid; its treatment of fractional-power phases was too compressed to distinguish the two different root issues. The supplied correction makes that step explicit, together with the shared-edge and charge conventions. The original author freeze is preserved unchanged. Acceptance is attached to the separately pinned corrected archive, not silently substituted for the original bytes.

For a fixed compact connected closed oriented 3-manifold W, nonempty link L, and odd N > 1, the original 2001 invariant satisfies

    K_N(W,L,rho_a) = K_N(W,L,1),  a in H^1(W;C),

where rho_a has unipotent holonomy U(a). This answers the real-additive Thurston-face subquestion affirmatively, with constancy on all real additive cohomology. The already-authored general B-bundle diagonal-reduction consequence and local holomorphic dependence on the multiplicative character also pass this audit. No broader multiplicative-fiber classification follows. Overall disposition remains PARTIAL.

This is an independent mathematical audit of an AI-assisted, unrefereed manuscript, not peer review, a novelty finding, or an independent reconstruction of every quantum identity underlying the cited invariant theorem. No publication was performed.

## Intake and source identity

The author archive and external manifest match their supplied SHA-256 pins. The archive contains exactly the five declared data files, without directory or executable entries, duplicate names, or unlisted members. Every member's byte count and SHA-256 match the external manifest and the working original. The audit re-read all five files.

The three complete corpus files were read and rehashed. They contain 15,458 catalog entries, 15,458 complete problem records, and 6,701 research reports. There is exactly one record for ID 10400135. The complete record and report yield pair hash 39a094222dec91e245c16ecef88cc0f374953d235b9bf8685c24e533182f9e84 using the stipulated default sorted JSON serialization. The report contains literature triage, not a prior substantive proof. Public hashes and match results are recorded separately; raw corpus contents are excluded.

The publisher's Ohtsuki source, Section 7.4, printed pages 485-486, was checked, including a fresh visual inspection of PDF page 114. Its bibliography identifies reference [43] as arXiv:math/0101234. The question therefore does point to the original Borel state sum, not a later cusped or reduced invariant. The surrounding paragraph distinguishes unipotent additive, exponentiated diagonal, and finite-coefficient diagonal bundles. Problem 7.19 asks more broadly about regularity and fibers. Problem 7.21 separately asks about the unpowered phase.

The local 2001 PDF was independently rehashed and inspected in Sections 2-4 and 8. PDF page 30, including both tensor formulas, was freshly rendered and visually inspected. The public arXiv listing confirms v2, 28 February 2001. An attempted version-specific PDF read returned a cache miss; the versionless public PDF read succeeded and identifies itself as the same v2. The audit did not infer fresh remote byte equality from a parsed web response. All eight author source-PDF byte pins match locally; this is not a claim that all eight papers' proofs were audited.

Public references:

- Ohtsuki, editor, Problems on invariants of knots and 3-manifolds: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- Baseilhac and Benedetti, Quantum Hyperbolic State Sum Invariants of 3-Manifolds, v2: https://arxiv.org/abs/math/0101234v2 and https://arxiv.org/pdf/math/0101234
- Baseilhac and Benedetti, Quantum Hyperbolic Invariants Of 3-Manifolds With PSL(2,C)-Characters: https://arxiv.org/abs/math/0306280

## Normalization and equivalence checks

Equation (2) of the 2001 paper is exactly the Nth power of the normalized finite state sum used by the author. The edge factor is x(e)^(-2m/N), with N = 2m+1, over edges outside H; the vertex factor is N^(-r_0). An edge-root determination expresses this factor as y(e)^(-2m). There is no omitted conjugate, absolute value, 2Nth power, or division by the global state sum.

Theorem 4.2 and Proposition 4.3 supply invariance of this complex-valued K_N under the permitted decoration changes. The relevant cocycle equivalence is z'(uv) = lambda(u)^(-1) z(uv) lambda(v), with vertex values in B. Constant diagonal conjugation is included. Proposition 4.3(b) is read in its fixed-bundle context; it does not assert equality for arbitrary distinct bundle classes.

The unpowered H_N may have an Nth-root ambiguity. The object accepted here is K_N = H_N^N. Nothing in this audit chooses a canonical continuous global phase for H_N. Remark 4.31 of the 2003 paper explicitly distinguishes the Borel symmetrization from its general PSL construction. It is used only as a normalization warning, not as a replacement theorem.

## Triangulation, branching, and charges

A distinguished triangulation is required to carry L as a Hamiltonian subcomplex, not merely as an arbitrary union of edges. The source question explicitly allows such a triangulation with distinct endpoints on every edge. That endpoint condition is essential: a trivial-bundle additive coboundary would vanish on a loop edge. The argument selects a permitted triangulation once; it does not claim every singular triangulation has the endpoint property, and it does not confuse the paper's weaker term almost-regular with loop-free.

The branching and integral charge are fixed throughout the parameter family. Their conditions do not depend on its varying cocycle entries. The tensor charge is the integral charge divided by 2 modulo N, as in Definition 3.9 of the 2001 source. The correction states this convention expressly. No charge is varied to cancel a pole or a phase. No geometric positivity condition, hyperbolic shape with nonzero imaginary part, or generic real position is part of fullness here.

## Fullness, regular sequences, and local denominators

For an upper triangular edge value write z_ij = (t_ij,x_ij), meaning the matrix with diagonal t_ij,t_ij^(-1) and upper-right entry x_ij. The multiplication rule is

    (t,x)(u,y) = (tu, t y + x/u).

All t entries are nonzero automatically. Fullness requires every x entry to be nonzero. On a branched tetrahedron the cocycle rules give the three longer-edge entries, including

    x_02 x_13 = x_03 x_12 + x_01 x_23.

This identity was checked directly by substitution, including the diagonal factors. It is not limited to additive cocycles.

Take one local Nth-root choice y for each oriented edge and put A = y_03 y_12, B = y_01 y_23, C = y_02 y_13. All three are nonzero and C^N = A^N+B^N. A shared edge has a single root used in all incident tetrahedra. Choose root functions on disjoint discs around the finitely many distinct base values, including diagonal entries; this handles coincident values correctly. There is no need for a multiplicative branch of the Nth root. Only the Nth-power relations are used, as in the source's representation construction.

The consecutive representation sequence and its consecutive tensor products are regular because the six corresponding tetrahedral upper-right edge entries are nonzero. No additional regularity assumption is hidden in applying Proposition 8.3.

Every factor C-A zeta^j is nonzero: its vanishing would force B^N=0. The same argument handles the zeta shift in the inverse tensor. The cyclic numerators B are nonzero, so reciprocal cyclic products also have no poles. The quotient q=C/A is nonzero and q^N differs from 1. Thus the radicands in g(q), the factor h(q), and its inverse are regular in local determinations. The factor [q]=(1-q^N)/(N(1-q)) is a polynomial and has no problematic denominator; under fullness q also differs from 1. Charged monomials and edge normalization involve only nonzero roots.

These are formulas on an open neighborhood in ambient edge-coordinate space restricted to the cocycle equations. The argument does not require that the cocycle variety itself be smooth at a reducible point.

## Explicit phase cancellation and genuine complex continuity

Edge-root independence and the fractional-power branch inside g are logically distinct. Proposition 4.3(a) gives the former. The latter follows directly from the displayed formulas:

    h(q)^N = q^(-mN) product_{j=1}^{N-1}(1-q zeta^j)^j / g(1)^N.

This is single valued and nonzero in the full domain. Different local fractional-power determinations differ by an Nth root of unity. Crucially, h(q) in R and 1/h(q) in the inverse are scalar factors independent of all state indices. The charge shifts do not change that fact. Consequently

    H_N = (product_Delta h(q_Delta)^(epsilon_Delta)) S,

where epsilon_Delta is +1 or -1 and S is a finite locally holomorphic sum in the selected edge roots. On raising to N, the h factors become single valued and all their branch phases disappear. Proposition 4.3(a) identifies the resulting values for permitted edge-root determinations. This proves a genuine locally holomorphic complex-valued K_N, not merely a continuous phase class. A zero of S remains harmless; the argument never divides by S.

The correction adds this explicit calculation. It repairs a missing justification in the exposition, without changing the proposed theorem, invariant, or number of approaches.

## Gauge contraction and why the limit is covered

For any additive cocycle a, choose distinct complex labels u(v) on the finite vertex set and form b(uv)=u(v)-u(u). The endpoint condition makes b full. The family b+s a is additive and represents s a after the fixed unipotent vertex gauge. A single positive radius obtained from the minimum of |b(e)|/(2|a(e)|) over the nonzero a(e) makes the entire complex disc full. It includes s=0.

For every nonzero s, a diagonal matrix with entries r,r^(-1), r^2=s, conjugates U(a) to U(s a). A continuous square-root choice in s is not needed: the equality of invariant values is pointwise for nonzero s. The actual decorated state-sum family, b+s a, is holomorphic and converges to the full trivial representative b. No vanishing gauge matrix is ever substituted into the state sum.

The 2001 paper's cocycle-invariance argument applies to full representatives of the same bundle. It discusses generic full perturbations needed for intermediate moves and explicitly extends to the original full cocycles by continuity. The present path never leaves the full domain and does not require a simultaneous generic move sequence valid for every s. The paper's theorem identifies each point's scalar value, and the local formula proves its continuity at the full endpoint. Therefore the constant punctured-disc value equals the value at the endpoint. This is not an illicit continuity assertion at the zero edge cocycle.

Calling the orbit space a character variety is not used as a substitute for this proof. Indeed the orbit closures of unipotent representations motivate caution; the full-gauged path is exactly what makes the argument valid without assuming a Hausdorff orbit space or a GIT identification.

## Existing general diagonal reduction

For a general cocycle (t(e),x(e)), multiplication shows that (t(e),s x(e)) is still a cocycle. Choose vertex parameters avoiding the finitely many hyperplanes

    t(e)u(v)-u(u)/t(e) = 0.

Each is proper because the endpoints are distinct and t(e) is nonzero. The same fixed unipotent vertex gauge gives the full family with upper-right entries d(e)+s x(e). For nonzero s, constant diagonal conjugation identifies its class with the original bundle. At zero it represents the diagonal bundle. The same local-continuity argument proves precisely the already-claimed diagonal-reduction equality.

For the local holomorphic multiplicative dependence, choose a spanning tree and use the finitely many resulting based edge loops. Their character values are holomorphic monomials on each component of Hom(H_1(W;Z),C*); the torsion components are discrete. A fixed vertex gauge full at a selected character remains full nearby. This supplies the claimed local holomorphic scalar function. It does not identify its global fibers.

## What remains unresolved

The additive specialization is constant on all complex cohomology and hence on the entire real Thurston unit sphere, any faces and their boundaries. Degenerate seminorms, an empty unit sphere, and b_1=0 do not invalidate that statement.

The exponentiated specialization uses diagonal characters exp(a), not the unipotent representation U(a). Finite-coefficient inputs likewise give diagonal torsion characters. The accepted contraction preserves the diagonal character and therefore proves no equality between different diagonal characters. No full multiplicative or finite-specialization fiber description, fixed-N formula for every W and L, reduced invariant statement, boundary-weight statement, asymptotic theorem, or novelty result has been obtained.

Three approaches remain the authored count. This audit does not introduce a fourth research approach. The source-theorem reliance, normalization boundaries, publication restriction, and remaining multiplicative scope are all preserved.
