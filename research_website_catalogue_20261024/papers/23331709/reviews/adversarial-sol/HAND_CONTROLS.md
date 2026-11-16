# Actual source-first derivations and adversarial controls

All calculations below were derived from the controlling manuscript and elementary linear algebra before opening supporting code, archived reviews/results or foreign primary bodies. Coefficients are rational, hence give valid characteristic-zero examples. These are checkable proofs/certificates; finite examples are not a substitute for the universal deductions.

## 1. A counterexample would have very little cycle budget

In an essential irreducible rank r factor, choose r independent normal forms as coordinates. Any degree1 logarithmic derivation has diagonal matrix diag(lambda_i). A further normal is an eigenvector; if two eigenvalues differ, all normals split by their coordinate eigenspaces and the represented matroid is a product. Thus irreducibility leaves only scalar Euler derivations. Essentiality excludes degree0 derivations. The exponent lists must therefore be (1,2^(r-1)) or (1,2^(r-2),3), not a silently assumed condition on the original possibly reducible arrangement.

For a rank2 flat containing m normals, use x,y,x+c_i y. A degree d_j logarithmic derivation has theta(x)=xP,theta(y)=yQ and each x+c_i y divides P-Q; degree(P-Q)<=d_j-1. If m>d_max+1, m-2>d_j-1, forcing P=Q for every basis derivation. All basis columns then have proportional first two rows over the fraction field, contradicting full rank. This also works over a characteristic-zero field with no chosen ordering or algebraic closure. The coefficients c_i are nonzero and distinct because hyperplanes are distinct; multiplicities cannot be imported into this argument.

Write u for triple-rich lines, v for quadruple-rich lines. Pair partition gives b2=binom(n,2)-u-3v, with no contribution from ordinary2-lines to the defect. From n=sum d and b2=((sum d)^2-sum d^2)/2:

- All2: n=2r-1, sum d^2=4r-3, b2=2(r-1)^2, u=r-1,v=0.
- One3: n=2r, sum d^2=4r+2, b2=2r^2-2r-1, u+3v=r+1.

Formality is essential for connectedness: local relation supports lie in incidence components, so any global relation splits as a sum of relations internal to components; equality between vectors in distinct component spans would then make each component contribution zero. Distinct components therefore give a direct-sum normal decomposition. Irreducibility forces connectedness, including absence of isolated normal vertices.

For a connected incidence graph, edges=3u+4v and vertices=n+u+v. Thus beta=2u+3v-n+1. This is0 in the all2 case and3-3v in the one3 case. In particular v>=2 is already impossible because a connected graph cannot have negative cycle rank. The dimension check dimR=r<=u+2v=r+1-v independently agrees. A hypothetical exotic counterexample cannot gain a second quadruple pencil without breaking connectedness/formality or the free factorization counts.

## 2. Obstruction certificate for every alternative minimal triple circuit

In the v=0 one3 case, there are r+1 triple-relation columns spanning dimR=r. Let T be any inclusion-minimal dependent column set, t=|T|, and s its normal-support size. Every column's three coordinates are nonzero because no two normals are proportional. Every dependence coefficient is nonzero by minimality. A normal used by just one column cannot cancel; hence its support degree is at least2 and 2s<=3t.

The incidence support is connected: otherwise restricting the zero vector to a component gives a smaller column dependence. Its cycle rank is2t-s+1 and cannot exceed the ambient value3. Hence 2t-2<=s<=3t/2, forcing t<=4. A fixed triple needs three other triples to cover its three elements because distinct rank2 flats share at most one normal, so t>=4. Thus t=4,s=6; every support degree equals2 and every pair of columns meets once, at six different normals. This rules out every t>=5 alternative by the explicit inequality beta>=ceil(t/2)+1>=4, rather than an enumeration cutoff. It also rules out a doubled intersection or a coefficient-supported singleton.

The four-column support already uses all3 cycles. Contract that connected support: any extra chord, outside path returning to a second core vertex, loop or multiple attachment raises the quotient's cycle rank above0. Therefore outside components attach at one core vertex only. Core triple vertices already have full degree3, so attachments can only be at core normal vertices. The global local-sum kernel has dimension1, so two independent relation-dependency cores would also contradict its dimension. These are separate necessary constraints on any candidate counterexample.

## 3. Full represented-core certificate, including ordinary flats

Use columns in Q^3, indexed by edges of an auxiliary K4:

    a=e12=(1,0,0), b=e13=(0,1,0), c=e14=(1,1,0),
    d=e23=(0,0,1), e=e24=(1,0,1), f=e34=(0,1,-1).

The four star triples are (a,b,c),(a,d,e),(b,d,f),(c,e,f). Their relation rows in order(a,b,c,d,e,f) are

    rho1=(-1,-1, 1, 0, 0, 0)
    rho2=(-1, 0, 0,-1, 1, 0)
    rho3=( 0,-1, 0, 1, 0, 1)
    rho4=( 0, 0, 1, 0,-1,-1).

rho1-rho2-rho3-rho4=0. The first three are independent using columns c,e,f, so row rank3. Normals a,b,d are independent, so normal rank3 and kernel dimension3; all relations are local. This directly verifies formality and the minimal four-triple dependency.

The four triples account for12 of15 pairs. The three remaining pair planes are span(a,f)={z=-y}, span(b,e)={x=z}, span(c,d)={x=y}. Substitution of the other four normals in each displayed equation shows none is contained, so these are exactly the ordinary pair flats; no unlisted triple is concealed. For L1=span(a,b,c)={z=0}, intersections with those three planes are Ka,Kb,Kc. Intersections with L2={y=0}, L3={x=0}, L4={x-y-z=0} are again Ka,Kb,Kc. Every rank2 flat has now been checked. Ranks0,1,3 are immediate, so L1 is modular and 0<Ka<L1<Q^3 is a complete modular flag. This includes the ordinary-flat case most likely to be missed by a triple-only check.

It is also a free (1,2,3) example. Put Q=xyz(x+y)(x+z)(y-z). The derivations

    E=(x,y,z), D2=(x^2,-y^2,-z^2), D3=(x^3,y^3,z^3)

are logarithmic: in coordinates (x,-y,-z), differences of kth powers are divisible by the corresponding difference, with one coordinate fixed at0. Their coefficient determinant is Q. To see directly why a determinant certificate proves a free basis, solve for any logarithmic theta by Cramer's rule. For each defining linear h, all four derivations are tangent modulo h; each replacement determinant is divisible by h. Distinct factors are coprime, so Q divides every numerator and all coefficients are polynomial. No finite computation or unproved freeness inference is needed for this example.

## 4. Pencil extensions and an actual failure without formality

Coordinate extension control: take a represented configuration spanning W, a nonzero a in it, and a new independent z. Append distinct p_i=z+c_i a. For any flat generated by inside normals T and k outside normals: k=0 gives span(T); k=1 has intersection with W exactly span(T); k>=2 spans z and a, giving intersection span(T,a). All intersections are represented. Thus W is a modular coatom and every modular flag in W lifts. Each extension adds one rank and m-1 normals, hence m-2 relations. This explains both the coatom and chain-extension claims, not only a relation-count identity.

Formality cannot be silently dropped from the manuscript's pruning lemma. Take

    a=(1,0,0), p=(0,1,0), q=(1,1,0), b=(0,0,1), c=(1,2,1).

The only rich line is {a,p,q}: a pair from it plus b or c is independent, while det(a,b,c)=-2, det(p,b,c)=1 and det(q,b,c)=-1. Thus p,q occur in no other rich line, but deleting them leaves {a,b,c} of rank3, not rank2. The whole relation space has dimension2 and its only local subspace has dimension1, so the missing hypothesis is precisely formality. Its n=5,b2=9 characteristic polynomial is(t-1)(t^2-4t+5), incompatible with integral free exponents. This is an actual out-of-hypothesis counterartifact, not a defect of the stated theorem.

Two in-hypothesis terminal controls have explicit freeness certificates:

- All2 tree Q=xyz(x+y)(x+z): E, (0,y(x+y),0), (0,0,z(x+z)) have determinant Q, giving exponents(1,2,2).
- One3 tree Q=xyz(x+y)(x+2y)(x+z): E, (0,0,z(x+z)), (0,y(x+y)(x+2y),0) have determinant -Q, giving exponents(1,2,3).

The Cramer argument above proves both certificates. The pencil structure and modular flag follow from the coordinate-intersection calculation. These test both permitted tree regimes independently of a free-deletion theorem; no arbitrary deletion is asserted to remain free.

## 5. Exact two-cubic boundary, with freeness and nonsupersolvability proved

Consider the seven normals x,y,z,x+y,x+z,y+z,x+y+z and let Q be their product. Define

    A=x(x+y)(x+z), B=y(x+y)(y+z), C=z(x+z)(y+z),
    E=(x,y,z), D1=(A,-B,0), D2=(A,0,-C).

All coordinate/pair-sum tangencies are immediate from the factors. For S=x+y+z, D1(S)=(x+y)(x-y)S and D2(S)=(x+z)(x-z)S. The coefficient determinant is xBC+yAC+zAB=2Q. The same Cramer divisibility argument proves this arrangement is free with exponents(1,3,3) in characteristic zero.

Its six triple lines are {x,y,x+y},{x,z,x+z},{y,z,y+z},{x,y+z,S},{y,x+z,S},{z,x+y,S}. They account for18 of21 pairs; the ordinary pair planes are the three pairs among d=x+y,e=x+z,f=y+z. Their equations are x=y+z, y=x+z, z=x+y respectively. No additional rich line occurs, by substitution. None of the nine rank2 flats is modular:

- For the first three coordinate-plane triple flats, intersect the opposite ordinary pair plane to get respectively (1,-1,0),(1,0,-1),(0,1,-1), none a represented normal.
- For the latter three triple flats y=z,x=z,x=y, intersect respectively span(d,e), span(d,f), span(e,f), obtaining (2,1,1),(1,2,1),(1,1,2), none represented.
- Each ordinary plane fails against respectively the coordinate plane x=0,y=0,z=0, with an unrepresented difference direction as above.

A rank3 supersolvable lattice requires a modular rank2 element. None exists, so this is a free nonsupersolvable arrangement. Its counts n=7,u=6,b2=15 agree with(t-1)(t-3)^2 and incidence beta=6. This demonstrates the single-cubic restriction does real work; it is not a counterexample to the original at-most-one3 claim.

## 6. Low rank, products, quantifiers and exact remaining interface

Rank0 has one lattice element; rank1 a two-element chain; in rank2 all atoms are modular and any atom gives a maximal flag. Appending a rank1 coordinate factor to the six-normal core creates a disconnected incidence graph and an additional exponent1, but a product modular chain still exists. Adding unused ambient coordinates creates zero exponents without changing the intersection lattice. Thus connectedness and exactly-one1 must only be applied after essential irreducible reduction, as the manuscript does.

The universal core obstruction and pencil proof do not enumerate ranks or rely on numerical tolerances. The outstanding external interfaces are the exact characteristic-zero factorization/formality statements, original conjecture scope and bounded credit/withdrawal context. Native code may corroborate examples but cannot settle those interfaces or first-priority claims. No current peer/root conclusion has been read and no source program has run.
