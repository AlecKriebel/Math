# Root universal reconstruction: PR1142

Recorded 2026-10-17T23:16:59.784148+00:00

This record concerns the exact additive boundary Laplace–Beltrami question, not a Steklov/Dirichlet/Neumann problem. The actual PR claims a full negative result for every fixed m>=2, allowing disconnected boundary and requiring the domain itself connected. The conclusion is a hypothesis to be audited.

## Order and source scope

Root read the fresh actual body/STATUS and complete distributed PROOF plus source metadata, then independently reconstructed all steps and read fresh primary sources. No original AUDIT, acceptance report or new detailed family report has been opened at this checkpoint. Three concurrent family checkpoint messages arrived before this written record, confirming their independent arguments; their pass labels are not proof premises. Thus no complete information isolation is claimed for root. The families separately preserve earlier independent records.

Fresh primary files exactly match the historical source hashes: OWR33/2012 (1024557bytes), CDE0909.5346 single v1 (216749bytes), CEG1007.0826v2 (230881bytes), and De Lellis–Szekelyhidi precise Nash–Kuiper formulation (429804bytes). Root read the complete three-page Colbois talk, CDE standing convention/Thm1.4 and full Section5, CEG introduction/Thm1.1 and Examples3.1–3.2, and NK definition/Thm1.2/immediate context. Critical OWRp2036, CDEp6, CEGp14 and NKp4 were visually inspected. Underlying Colbois–Dodziuk/arithmetic-surface results and original Nash/Kuiper/Hirsch books are named established inputs, not independently reproved here. Fresh arXiv histories show CDEv1 September2009, CEGv2 October2011; CEG's internal May2022 compilation date is not a new version.

## Exact scope

The OWR question inherits Theorem3's all bounded smooth Euclidean domains and all numbered eigenvalues. No connected-boundary condition occurs in the full talk. This is reinforced positively by the cited CEG's Example3.1: its connected product domain has two boundary components and explicitly two zero modes. That example is in a different ambient space and does not itself prove the Euclidean negative answer. CDE uses zero index0 for its connected submanifolds, so its first positive eigenvalue becomes lambda2 in the present one-based convention. All zero modes and multiplicities must remain in the rank calculation.

## Metric/existence step

If c^-1g<=h<=cg, volume densities compare by c^±(m/2), inverse metric energies by c^±(1+m/2), and L2 norms by c^±(m/2). Thus Rayleigh quotients, and every numbered minmax eigenvalue on the common H1 space, compare by c^±(m+1). Uniformly convergent positive metrics on a fixed compact manifold have c->1, so volume and every fixed eigenvalue converge. No uniform-in-k spectral-continuity theorem is needed.

CDE supplies arbitrarily large normalized first positive eigenvalues on smooth closed connected hypersurface-embeddable manifolds: vary genus for m=2; use the sphere when m>=3. Choose one metric with normalized product>2LS^(2/m), then scale its volume to S, obtaining lambda2(g)>2L. A sufficiently small multiple of any smooth embedding is simultaneously strictly short relative to g and contained in B(r/8). The precise NK theorem supplies a C1 ISOMETRIC EMBEDDING, C0-close enough to remain in B(r/4), in codimension one. This is not an immersion being passed off as embedded.

C1 approximation by smooth maps gives embeddings for all sufficiently close approximations, since compact embeddings form a C1-open set. Their induced smooth metrics converge uniformly to g. If areas Sj->S, scale the image by aj=(S/Sj)^(1/m). The area is exactly S, eigenvalues multiply by aj^-2, and aj->1. The image remains in B(r) and lambda2>L for sufficiently close approximation. Equivalently normalized eigenvalues lose at most c^(m+2), so the initial strict factor2 leaves slack. Every final hypersurface is smooth. The required index/domain can be chosen separately at each q; no constructive finite mesh or uniform curvature bound is asserted.

## Topology

A compact connected smooth embedded hypersurface H in Euclidean space separates it into exactly two components, each having H as boundary; this is generalized Jordan–Brouwer, not a statement that either component must be a ball. It applies to varying genus or knotted embeddings. Smooth collars give a smooth bounded component U. Because H is contained in B(1/2), every point outside that ball can connect radially to infinity without meeting H, so U is contained in B(1/2).

For Omega=B1 minus closure(U), boundary is exactly the disjoint smooth pair S^m and H. Let E be the unbounded complementary component. It is open and connected, hence path connected; Omega=E intersect B1. Any point in this intersection with norm<3/4 can follow an E-path toward infinity until its first hit on the radius3/4 sphere. That initial path stays inside B1. All other points, and all endpoints, lie in the full connected annulus outside B(1/2). This proves connectedness without the invalid general claim that intersections of connected open sets are connected. Volume lies between v_m=omega_(m+1)(1-2^-(m+1))>0 and omega_(m+1), independently of q.

## Spectrum and divergence

Take Hq of areaq and first positive eigenvalue>Tq=q(q+m-1). Let rho_m=area(unit sphere); total boundary area Aq=q+rho_m. Harmonic polynomial decomposition gives sphere degreeell multiplicity C(ell+m,m)-C(ell+m-2,m). Summation telescopes: Nq=C(q+m-1,m)+C(q+m-2,m) counts exactly all sphere modes strictly below Tq. Hq contributes exactly one such mode, its zero. Therefore first Tq has rank kq=Nq+2, and lambda_kq(boundaryOmegaq)=Tq. At q=1 this says k1=3: both zeros precede the first positive spherical mode. Ties at Tq on the sphere cause no ambiguity. No uniform Weyl asymptotics over changing hypersurfaces are used.

For q>=m, kq<=2^(m+2)q^m, so kq^(2/m)<=Cm q², Cm=2^(2+4/m)<=16. Also I(Omegaq)^(1+2/m)<=K_m Aq^(1+2/m), K_m=v_m^(-(m+2)/(m+1)). Dividing the unweighted denominator by Tq Aq^(2/m) gives at most

    K_m (q+rho_m)/q² + Cm/(q+rho_m)^(2/m),

which tends to zero for each fixed m>=2. This directly proves the asserted unweighted quotient tends to infinity. For the subsequence q=t^m>=m the same expression is <=[K_m(1+rho_m)+16]/t², giving an explicit divergent lower bound for the quotient. Every finite pair of dimension-only constants is defeated; nonpositive constants are covered by domination by positive constants.

## Boundaries and strongest provisional finding

Domain connectedness, exactly two boundary components, smooth final induced metrics, all zero modes, fixed dimension and varying q are respected. No m=1, connected-boundary, fixed-topology surface or other spectral-operator result is inferred. The known multiplicative bound has the extra growth factor and is not contradicted; fixed-domain Weyl behavior is not contradicted. Root finds no universal mathematical gap to the exact stated class. Independent family review, complete reproduction, and subsequent priority audit remain required before promotion. This is not a novelty/priority or global openness certificate.
