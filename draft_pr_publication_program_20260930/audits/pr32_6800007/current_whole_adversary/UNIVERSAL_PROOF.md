# Independent whole-current reconstruction

This is a check of the precise current candidate, not a new proof-search response or publication draft. Fix a connected smooth second-countable boundaryless real three-manifold M, ordinary maps and homotopies through totally real immersions into the ordered integrable complex flag F=SL(3,C)/upper Borel. Compactness and orientability are unrestricted. All cohomology below is ordinary integral cohomology unless indicated. The literal second flag question supports this explicit convention; no claim about real-form uniformization, properness, embeddings, source diffeomorphisms or a permutation quotient follows.

## Geometric reduction and the simultaneous fiber

A real-linear map from a real three-space V to a complex three-space W is totally real and injective iff its complexification V tensor C→W is an isomorphism. For the forward implication, L(v)+iL(w)=0 gives an element in L(V) intersect iL(V), and hence v=w=0. Conversely an isomorphism forces both real injectivity and trivial intersection. Thus formal data are exactly a map f:M→F plus an isomorphism E=TM tensor C≅f*TF.

For any principal first-jet slice, fix the derivative on a real hyperplane. If the two fixed columns are complex dependent, its totally real part is empty. Otherwise its third-column possibilities are C³ minus their complex span. That is a connected real codimension-two complement. Given any point z, choose a vector w outside the span and a real N for which z±Nw both lie outside it; at most two values are forbidden. Their midpoint is z. Every nonempty component therefore has convex hull the full affine slice. This applies in every principal direction, after any real basis change. The relation is open and ample.

I freshly retrieved and directly read Forstnerič's general smooth-bundle theorem on printed p246 and its definitions; the scan's printed pp244–245 were also visually read. For the bundle M×F→M it gives weak homotopy equivalence from genuine C1 solution sections to formal sections for an open ample relation, without a compactness/orientability/open-source assumption. In particular it identifies their path components. Smooth approximation in an open relation, relative to smooth endpoints, gives ordinary smooth immersion homotopies; on noncompact M use positive local tolerances, not one bound at infinity. Theorem1.4 is expressly compact orientable and is not this universal input. No embedding theorem or properness is used.

Let T²⊂SU3 be the determinant-one diagonal torus. Over BT² the ordered lines L1,L2,L3 have specified product trivialization. The associated sum E0=L1+L2+L3 is an SU3 bundle; its classifying map b0 has homotopy fiber SU3/T²≅F. At the standard upper-Borel flag, sl3/b has the lower entries E21,E31,E32. Their actual adjoint characters are t2/t1,t3/t1,t3/t2, so the smooth complex tangent is associated to Eρ=L1*L2+L1*L3+L2*L3. This is not a holomorphic direct-sum splitting assertion.

A torus reduction of a trivial SU3 bundle gives the flag map; a path identifying Eρ with E gives its formal derivative. Classifying bundles with their isomorphisms and homotopies, or equivalently associative homotopy pullbacks, yields the formal space

    hofib_(*,τ)[Map(M,BT²)→Map(M,BSU3×BU3)],

where τ classifies the fixed generally nontrivial E. The two paths share the same torus datum. Polar decomposition permits unitary models. Replacing SU3 trivializations by free U3 trivializations introduces a false determinant degree; replacing E by a trivial bundle removes actual source sectors.

## Integral dimension bounds and existence

Smooth M admits a locally finite countable triangulation of dimension three. Complex numerable bundles are classified on this paracompact CW model by BU3. The low determinant fibration has fiber BSU3, whose π1,π2,π3 vanish, so rank-three bundles on M are classified by c1 and SU3 bundles are trivial.

Put A=H¹(M;Z), B=H²(M;Z), C=H³(M;Z). The ordered line data have (x1,x2,x3)=(x,y,−x−y). Summing the three roots gives c1(Eρ)=−4x−2y. The determinant of E is the complexification of the real orientation line. Lift its sign transition cocycle to integers; half its integral coboundary gives c1(E)=δ=βw1(TM). Thus precisely the pairs satisfying −4x−2y=δ admit both required bundle paths and formal data. Each is realized by the parametric h-principle.

The image of B²→B, (x,y)↦−4x−2y, is exactly 2B: if δ=2z, choose x=0,y=−z. Coefficient exactness says δ∈2B iff its mod-two reduction vanishes. The standard Bockstein identity ρ2βw1=Sq¹w1=w1² proves the stated existence criterion. Nothing divides torsion by two or presumes δ=0. In particular RP²×R and RP²×S1 have no admissible indices; a closed nonorientable source can have nonzero divisible δ, as the explicit Klein mapping torus shows.

The characteristic map

    φ=(c2,c1,c2): BSU3×BU3→K(Z,4)×K(Z,2)×K(Z,4)

is6-connected. Bott's freshly retrieved printed pp313–315 give the stable unitary period 0,Z. U(n)→U(n+1)→S^(2n+1) shows U3 is already stable through degree5. Hence BU3 has π2=π4=Z and π1,π3,π5=0; BSU3 retains π4=Z and vanishing groups below it and at5. Determinant detects π2. The complex rank-two quaternionic Hopf bundle over S4 has c2 of unit absolute value: its S3 sphere bundle has total space S7, and the integral Gysin sequence forces its Euler/top Chern class to be a generator. Stabilization preserves that generator. There is no factorial or hidden multiplier. φ is an isomorphism through π5 and surjects onto the zero targetπ6; its fiber is5-connected.

Needed domains M, M×I, M×S1 and M×S1×I have dimensions3,4,4,5. Replace φ by a fibration and solve relative lifts cell by cell. All obstructions vanish in those dimensions, and all comparisons lift as well. This works on an infinite CW pair directly: the finite dimension bound controls homotopy groups of the fiber, while the weak CW topology makes the cellwise maps continuous. No inverse limit, compact-exhaustion assumption, compact-support group or phantom-map claim is used. Thus φ preserves precisely the target mapping-space π0/π1 and the formal-fiber component orbit. It is not necessary to classify higher homotopy groups of the full mapping space.

## Complete prior theorem, with every hypothesis

The decisive available prior theorem is Taylor2012 Theorem1.2. I freshly retrieved the publisher PDF and read the entire paper, including all of its path-groupoid proof pp238–242. Its §2.1 works in a compactly generated convenient category with exponential law. Results2.3–2.8 identify lift sets and their free-loop groups; Lemma2.4 explicitly supplies the square/path criterion. Its full proof in§3 proves the isotropy image for arbitrary based spaces; the later CW/H-space restrictions occur only in§5.

After the characteristic replacement the target Y=Map(M,KZ4×KZ2×KZ4) can be modeled by a topological abelian group. Let X0=Map(M,BT²), and w:X0→Y be the representation characteristic map. Choose an admissible point a0 and a path from fixed b=φ(*,τ) to w(a0). Transport the fiber along that path; base X0 at a0 and Y at w(a0). Apply Taylor's theorem with OUTER source S⁰, one basepoint and one free point. Based S⁰-maps are arbitrary points in these entire unbased mapping spaces. The free-loop lift groups become π1(X0,a0) and π1(Y,w(a0)). The theorem's isotropy image is exactly the induced homomorphism between them. Its base point in the fiber is the chosen reference formal datum; changing it changes the origin, not the quotient.

No CW homotopy-type assertion about an infinite mapping space is required. Taylor Theorem5.2 is not applied there. No simple-connectivity premise on the homogeneous frame target is supplied or needed: that target has π1=Z/2, so a direct Koshkin Theorem3 transfer would fail. Nomura's product-rule statements3.7–3.9 are relevant prior context but omit some proofs. The following integral expansion itself verifies the needed substitution and does not depend on inaccessible Rutter/James–Thomas proofs. Consequently the chain does more than collect suggestive ingredients: an available published full component-isotropy theorem covers this exact formal object, all source quantifiers and the whole action.

## Coordinates, fixed E, and the full quotient

Source components are B² and source loops are A². The circle factor has finite free cellular chains, so relative integral cohomology on (M×S1,M×{*}) is H^(r−1)(M), even for infinite CW M. The map to absolute cohomology is injective because projection splits restriction. Target loop groups are therefore C⊕A⊕C, with raw coordinates (u,κ,v)=(-c2(V0)/S1,c1(Vρ)/S1,-c2(Vρ)/S1). These are actual additive π1 coordinates through the characteristic-space model; they are not a pointwise abelian gauge-group assertion.

On BT² the known associated-bundle formulas give

    Q0=−x²−xy−y²,
    P=−4x−2y,
    Qρ=5x²+5xy−y².

I read the freshly retrieved Borel–Hirzebruch Theorem10.3 and full proof p491, and Theorems10.7–10.8/full proofs pp494–495. Independently the three characters above and Whitney multiplication give these polynomials. A loop has x→x+pt, y→y+qt with t the parameter-circle class and t²=0. Ordinary coefficient extraction over integers gives

    a=(2x+y)p+(x+2y)q,
    k=−4p−2q,
    raw_v=−(10x+5y)p−(5x−2y)q.

Degree two commutes with degree one, so no concealed graded sign is used. To normalize at fixed nontrivial E, take ξ=Vρ−pr*E. The multiplicative Chern formula gives

    c2(ξ)=c2(Vρ)−c1(Vρ)δ+δ²−c2(E),
    ν=−c2(ξ)/S1=raw_v+δκ.

The base's degree-four terms vanish by dimension. This triangular shear is invertible over every abelian group and retains all torsion. For an admissible label δ=P, exact expansion gives ν=3a. The target-image subgroup is thus exactly {(a,k,3a):p,q∈A}. The fixed-E shear can be invisible ON THIS image because k is even and2δ=0; that does not excuse misidentifying generic target coordinates. On RP²×S1_x, E=L_b+1+1 and V=L_b+P_xt+1 over the parameter product have ordinary c2=bxt≠0 while c2(V−E)=0. This is a true target-loop countercontrol, not an admissible flag label.

Taylor's theorem now yields, over each admissible component, a torsor for (C⊕A⊕C)/im(a,k,3a). The integral automorphism

    (u,κ,ν)→(ν−3u,κ,u), inverse(s,κ,u)→(u,κ,s+3u),

has determinant−1 and maps the image to(0,k,a). Thus the torsor is exactly

    C⊕coker[(p,q)→(−4p−2q,(2x+y)cup p+(x+2y)cup q)].

No additional π2 term identifies components. This is the full quotient for moving base data, not just frames over one map. Realizations and the orbit criterion cover every actual immersion and every index. Disconnected sources give Cartesian products of these classifications over their open components, with an empty factor prohibiting a global immersion.

## Boundary falsifiers and what the computations mean

S3 yields a Z² torsor, with the extra sphere-frame integer already credited. S2×S1 gives the coupled finite Smith invariants rather than independent coordinate quotients. Klein×S1 retains an order-four extension; the orientation-reversing S2 mapping torus retains both top Z/2 coordinates; neither can be replaced by de Rham groups. The nonzero-divisible-determinant Klein mapping torus is a genuine closed smooth source, with affine h(X,Y)=(-X,Y−1/2) normalizing the Klein deck group. The time deck also shifts the third coordinate, so h²=b^−1 does NOT imply T²=b^−1. Its orientation character has no integral lift but does lift modulo4, giving δ=2 in H²=Z/4 and eight admissible labels. Reid's separate census example is supplementary source-supplied geometry; only its exact relator algebra is independently certified here.

A further infinite-source control is an open orientable handlebody formed by thickening a locally finite connected graph with one independent loop at each integer along a ray. Its interior is boundaryless smooth second-countable and retracts onto the graph. A=Hom(⊕countable Z,Z)=∏countable Z, and B=C=0. The formula becomes A/2A=∏countable Z/2. Independently the formal frame target has abelian π1=Z/2, so maps from that graph are exactly arbitrary assignments to its loops, with no conjugacy identifications. The all-ones assignment survives and has no finite support. This verifies why ordinary cohomology and direct bounded-cell arguments are necessary; a finite lattice or compact-support/direct-sum assumption would omit genuine classes. Finite-prefix controls merely illustrate this universal graph argument.

The actual original programs, full geometric controls, integral reproduction including expected failure, primary proof/arithmetic mutation runs, priority source controls and exact specialization algebra have all been executed unchanged in private copies. Newly designed finite integral lattice and T3 controls supplement the above universal deductions. Neither old PASS nor assertion counts prove these topological or primary-source assertions. No numerical result is represented as a formal proof or a novelty certificate.
