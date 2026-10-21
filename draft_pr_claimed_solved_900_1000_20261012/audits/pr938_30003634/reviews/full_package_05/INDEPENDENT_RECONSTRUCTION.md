# Independent mathematical reconstruction, review05

This is verification of the candidate mechanism, adding zero substantive proof responses. The supplied conclusion was a hypothesis. I separately checked the original finite construction and the stronger finite-depth existential statement. The checked claim is: for every integer m>=3 and every finite integer k>=1, there is a pure braid in P_m^(k) whose standard oriented closure is not integrally smoothly1-solvable. Therefore for every m>=3,n>=1, P_m^(n+2) is not contained in F_n^m. The witness may depend on depth. No fixed element of the derived intersection or explicit word at every depth is supplied or needed. P1 is trivial and P2 is cyclic, so their positive derived subgroups are trivial.

## Universal topological obstruction

Use Otto Definition2.3 literally, rather than replacing the source filtration with a relative exterior cobordism, a knot-only definition or rational solvability. For an algebraically split m-component link L, zero surgery M_L has H1(M_L;Z)=Z^m on its meridians. A1-solution W has the inclusion-induced integral H1 isomorphism, and H2(W;Z) free on framed embedded surfaces L_i,D_i,1<=i<=r, disjoint except for one transverse positive dual intersection per pair. Both surface groups lie in pi1(W)'. Consequently the all-meridian sign character extends to W and is trivial on every basis surface.

Choose a finite cellular structure and lifts to the universal cover. The rank-one rational sign system evaluates group elements to +/-1. Its integer boundary matrices reduce mod2 to the ordinary boundary matrices, since both signs become1. Any nonzero minor modulo2 is odd and remains nonzero over Q. Thus each twisted differential rank is at least the ordinary F2 rank. The equal chain dimensions give

    b2(W;Q_alpha) <= b2(W;F2).

Integral UCT gives an exact sequence with H2(W;Z) tensor F2 and Tor(H1(W;Z),F2). The latter vanishes because H1 is free; the former has dimension2r by the integral surface basis. Hence twisted b2<=2r. An ordinary rational-b2 comparison without this UCT hypothesis would be unjustified; the candidate uses the correct mod2 comparison.

For each surface, a trivialization of its restricted local system supplies a local-coefficient fundamental cycle and an absolute twisted class. A framing supplies a disjoint push-off, so self-pairings vanish. Actual disjointness makes all off-pair pairings zero; the unique dual intersection contributes a unit +/-1. Rescaling one class per pair produces the matrix direct_sum([[0,1],[1,0]]). Its nonsingularity makes the2r classes independent even if an ambient radical was initially permitted. The rank bound makes them a complete basis. Therefore the entire twisted form and the ordinary hyperbolic form have signature0. Flat extension Q->R or C preserves this conclusion. For r=0 the upper bound gives zero twisted H2, so there is no exceptional empty-basis case.

Toffoli formula1.1 applies to the same extended unitary rank-one representation and gives rho=ordinary signature minus twisted signature=0. His one-colour Remark4.25/formula4.21 identifies rho with minus the pointwise Levine-Tristram signature plus framed-linking correction terms. For algebraically split zero surgery the entire framed matrix is zero, so all corrections vanish. The source domain is (S1 minus{1}), including -1 regardless of Alexander roots. No boundary acyclicity, averaged signature, extra nullity term or ordinary-signature homomorphism on string links is assumed. Thus sigma_L(-1)=0. This deduction, rather than finite signature examples, proves the universal obstruction.

## Nonhomomorphic homogeneous signature on the actual pure group

Gambaudo-Ghys TheoremA and Remark1 supply bounded defect for ordinary oriented link-closure signature s on B3; their p575 gives its homogenization q and |q-s|<=6. For x=sigma1,y=sigma2, define a=x^2,b=y^2,h=y*x^2*y^-1,z=(xy)^3. These are all pure. The Artin relation gives

    ahb=x^2*y*x^2*y=x*(xyx)*x*y=x*(yxy)*x*y=(xy)^3=z.

Two-strand positive powers have s(x^ell)=1-ell. Adding the split third strand changes no signature, and braid conjugation preserves oriented closure signature. Hence q(a)=q(b)=q(h)=-2. The n=3 full-twist identity s(alpha*Delta3^4)=s(alpha)-8 yields s(z^(2r))=-8r and q(z)=-4. A homomorphism on P3 would give -6 for ahb. Thus q|P3 is nonhomomorphic. Ambient nonhomomorphy alone would not imply this restriction statement; the explicit pure relation closes that possible gap.

## Persistence and the essential power step

If a homogeneous quasimorphism f vanishes on a normal N, then (gu)^r=g^r*u_r with u_r in N. Applying its defect inequality once gives |r*f(gu)-r*f(g)|<=D(f). Dividing by r proves exact constancy on cosets, so f descends as a homogeneous quasimorphism to G/N. For N=G^(k), finite k, that quotient is solvable and amenable. Calegari Proposition2.65 makes its homogeneous quasimorphisms homomorphisms; pulling back would contradict the established nonhomomorphy. Therefore q is nonzero on every finite positive P3 derived term. Kawasaki etal2025Lemma7.12 proves a stronger exact defect-restriction identity and receives explicit priority credit; this general group statement is not a new theorem here.

Choose v in P3^(k) with q(v)!=0. A positive power with r*|q(v)|>6 has |s(v^r)|>=r*|q(v)|-6>0. The same term contains v^r. The argument needs this power; nonzero q(v) alone does not force s(v)!=0. Linking numbers are homomorphisms on P3 and vanish on P3', so that closure is algebraically split. The universal obstruction excludes it from F1. Adding split vertical strands is a braid homomorphism and adds split unknots to the standard closure, preserving both derived membership and ordinary signature. Finally Otto's nested filtration gives Fn subset F1 for n>=1 and k=n+2 proves the advertised source conclusion.

## Explicit finite construction and exact checks

For c=[a,b],d=a^-1*c*a,e=b^-1*c*b,u=[c,d],v=[d,e], beta=[u,v], normality puts c,d,e in P3',u,v in P3'',beta in P3'''. Free cancellation yields104 letters. The exact strand tracing has identity permutation and all pairwise crossing sums0. Each pure component, after deleting the others, is the trivial1-braid and closes to an unknot. Those properties do not themselves establish its signature.

The authenticated cold release actually recomputed all original286 controls, the full independent planar face certificate and the full104-term Meyer data in four genuine processes. The planar construction has104vertices,208edges,106faces and49alpha regions. Deleting the outside region gives the48-dimensional matrix; actual crossing contributions are A_j on the appropriate anchor diagonal and -sgn(B_j)*(e_i-e_(i+1))*(transpose) for each sigma2 crossing. Only sigma1 crossings are exceptional, so correction=sum A_j=0. Exact congruences give inertia(23,25,0) and Bareiss determinant-7154819319988224. The ordinary signature is-2.

Erle's printed preceding-block off-diagonal index disagrees with his own block picture. The independent half-edge geometry gives the current-block sign. All-even B lengths make the incorrect witness matrix sign-congruent, so matching this witness's inertia alone would conceal the error. The retained mixed-parity control has geometric inertia(2,1,0) versus literal printed inertia(1,1,1); it falsifies that shortcut.

The independent Meyer implementation builds E=im(A^-1-I) intersect im(I-B) with lifts from ker[D1,-D2], checks the fiber radical, symmetry and both inertias, and never inverts a potentially singular D1/D2. The source form q(e)=Omega(v1+v2,e) is calibrated using two-strand signatures. All104terms match exactly:50positive,48negative,6zero; sum2 and signature-2. The final Burau determinant is1. Zero/empty forms, radicals, off-diagonal two-dimensional pivots, mirrors, relations and cocycles are included. These finite checks prove the explicit n=1 witness, not the universal topological/group lemmas or historical priority.

## Primary evidence and priority limits

Twelve actual primary PDFs were freshly fetched and hashed. Eleven unchanged prior copies were reused only after network-hash equality; the dynamic Erle wrapper has its own new pin. Fifteen relevant source pages were freshly rendered and inspected, alongside all four fresh current paper pages. Source dates and versions, formula locators and raw-file hashes are recorded separately. No extracted text or raster substitutes for byte authentication; no search snippet substitutes for theorems.

The exact question is Harvey's contribution, joint work with Park and Ray, Pure braids, Whitney towers, and0-solvability, Question3p3021, pp3020–3021, in Mini-Workshop: Interactions between Low-dimensional Topology and Complex Algebraic Geometry, DOI10.4171/OWR/2017/50. The report/workshop year2017 differs from publication2018. The corrected title is consistent across current TeX/PDF/generator/descriptor. The older exact-day EMS article versus issue/Crossref discrepancy is retained honestly.

I freshly read BK2015Proposition3.6, CHHarxivv3Example2.4/Proposition7.1 and surrounding braid discussion, Kuzbaryv2Theorem1.1 and the published DiPrisa-FrambaTheorem4.7/proof. BK establishes relevant ambient nonhomomorphy; its pure ambient-commutator example is not in P3' because linking is(-2,1,1). Otto's older second-derived construction does not establish third-derived membership. A quotient killing all pure braids kills every target derived braid and supplies no obstruction on those elements. CHH supplies related rho machinery without an inspected complete closure/F1/depth conclusion. Actual published CHH2012 bytes remain unauthenticated; the identified arxivv3 is checked. The author-hosted scl PDF is not asserted identical to2009 print. The prior two deep searches and fresh falsifier remain bounded historical evidence. My supplementary three-query search did not establish a complete predecessor. This establishes neither worldwide absence, firstness nor current openness.

No mathematical gap was found for the precisely stated theorem under its credited foundations. No new proof route or substantive proof-search response was added.
