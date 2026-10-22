# Explicit low-weight classifications and controls

These are partial results for Problem 25 of the 2010 AIM Hilbert-schemes workshop. They do not settle the full question. The arguments are elementary; no novelty claim is made. All Grassmannians below use the quotient convention unless explicitly described as spaces of subspaces.

## Theorem 1. All positive weights up to two

Let k be any field, S=k[x_1,…,x_n] an A-graded polynomial ring, and λ:A→Z a homomorphism such that λ(deg x_i)>0 for every variable. Let h:A→N satisfy h(0)=1 and vanish in every other degree whose λ-weight is not one or two. In particular h vanishes in any degree not attained by a monomial.

For each A-degree a of weight one, let V_a be the span of the variables of degree a, m_a=dim V_a, and r_a=h(a). Form

B=∏_a Gr(r_a,V_a),

with universal quotient bundles Q_a, and put Q=⊕_a Q_a. Only the finite set of attained weight-one degrees is involved. Let V_b^(2) be the span of weight-two variables with A-degree b and put

E_b=(V_b^(2)⊗O_B) ⊕ (Sym² Q)_b.

The rank e_b of this vector bundle is

e_b=dim V_b^(2)+Σ_{a<c, a+c=b} r_a r_c+Σ_{2a=b} r_a(r_a+1)/2.

Here an arbitrary total order selects each unequal pair once. Degree equalities are equalities in A, including any torsion. Set q_b=h(b).

If every 0≤r_a≤m_a and 0≤q_b≤e_b, and h vanishes in unattained degrees, then

H_S^h ≅ ∏_B Gr_B(q_b,E_b).

Otherwise the scheme is empty. The product is over the finitely many attained weight-two degrees, allowing zero-dimensional bundles and rank-zero quotients. In the nonempty case this scheme is smooth and geometrically irreducible, of dimension

Σ_a r_a(m_a−r_a)+Σ_b q_b(e_b−q_b).

### Proof

Work over any k-algebra R; the proof is local on Spec R and glues. A family I with the specified h has I_0=0. In every degree of weight greater than two, and every other zero-rank degree, its ideal piece is the entire piece of S_R: a locally free quotient of rank zero is zero.

Weight one has no products of positive-weight variables. Consequently the remaining data there are the locally free quotients (V_a)_R→Q_a, represented by B. Write K=ker((⊕_a V_a)_R→Q).

The weight-two part of S_R is V^(2)_R⊕Sym²(V^(1)_R). The ideal condition on products involving K says exactly that I in weight two must contain the image V^(1)_R K in Sym²(V^(1)_R). The universal property of the symmetric algebra gives, degree by degree,

Sym²(V^(1)_R)/(V^(1)_R K) ≅ Sym² Q.

This is valid in every characteristic and over arbitrary R. One can also check it after locally splitting the locally free quotient V^(1)_R→Q. Hence choosing the remaining weight-two ideal pieces is precisely choosing locally free rank-q_b quotients of E_b.

There are no further multiplication constraints. Multiplication of a weight-two relation by any variable lands in weight at least three, already killed. Multiplication of a relation of greater weight also lands in a killed degree. Variables of weight greater than two are themselves killed. Thus the choices produce an ideal and the construction recovers every family I.

The constructions commute with arbitrary base change, because the quotients are locally free and symmetric powers of locally free quotients have the displayed universal description. This proves an isomorphism of functors, hence of representing schemes, rather than merely a bijection of field-valued points.

The inequalities are necessary and sufficient for the indicated Grassmannians to exist. The base is a product of Grassmannians, and each further factor is a relative Grassmannian of a vector bundle of fixed rank. They are smooth, projective and have geometrically irreducible fibers. Local trivializations over the geometrically irreducible base prove geometric irreducibility of their fiber product. The dimension formula is the sum of the base and fiber dimensions. □

### Consequences and a resonance example

For the standard grading, with V=k^n and h=(1,r,s), the scheme is Gr_B(s,Sym² Q) over B=Gr(r,V). This covers the entire suggested degree-0,1,2 layer of the imported attempt.

For weights deg x=deg y=1 and deg z=2, h=(1,r,s), the scheme is Gr_B(s,O⊕Sym² Q) over Gr(r,2). In particular r=s=1 gives a P¹-bundle over P¹. This permits a supported decomposable degree and a relation mixing z with quadratics; the earlier square-zero product formula does not describe it.

The theorem concerns weighted support, not merely a numerical Loewy length assertion under an unrelated grading.

## Theorem 2. A cubic top quotient of rank one

Let S=k[x_1,…,x_n] have its standard grading. Suppose

h=(1,r,s,1), with h(j)=0 for j≥4,

where 1≤r≤n and 1≤s≤N=r(r+1)/2. Then H_S^h is nonempty and geometrically connected over every field k.

No smoothness or irreducibility assertion is included. In particular r=3,s=2 is a known reducible standard-graded example in the characteristic range of Cartwright–Erman–Velasco–Viray.

### Proof for fixed degree-one quotient

First fix an r-dimensional vector space V as the quotient in degree one. Giving the top rank-one quotient of Sym³ V is equivalent to a line [F] in P((Sym³ V)^*), where this notation parametrizes lines in the displayed dual space. Define contraction by the multiplication pairing:

c_F:V→(Sym² V)^*,     c_F(v)(q)=F(vq).

This definition does not use ordinary differentiation or divide by factorials.

Let D_s be the determinantal closed locus where rank c_F≤s. If s≥r it is the entire projective space. If s<r, consider the incidence space parametrizing a subspace W⊂V of dimension r−s and a nonzero functional on Sym³(V/W), up to scalar. It is a projective bundle over Gr(r−s,V), hence irreducible. Its projective image is exactly the underlying space of D_s: rank c_F≤s means ker c_F contains such a W, and then F kills W·Sym² V and factors through Sym³(V/W). Conversely any functional from that quotient kills W·Sym² V. The same argument works after algebraic closure, so D_s is geometrically irreducible as a topological space. No claim about reducedness of its determinantal structure is needed.

The quadratic quotient of dimension s is dual to a subspace U⊂(Sym² V)^* of dimension s. The condition that its kernel I_2 generates relations killed by F is equivalent to im c_F⊂U. Thus the Hilbert scheme for the fixed V is the projective incidence scheme

X={(U,[F]): im c_F⊂U} ⊂ Gr_sub(s,(Sym² V)^*)×P((Sym³ V)^*).

For any geometric point [F] with contraction rank ℓ≤s, its fiber is Gr_sub(s−ℓ,N−ℓ), which is nonempty and connected. Every other relation lands in degrees ≥4 and is automatically killed. Consequently X→D_s is proper, surjective and has connected geometric fibers.

A proper surjection onto a connected scheme with connected geometric fibers has connected source: if the source were the disjoint union of two nonempty open-and-closed subsets, their proper images would be closed, cover the target and be disjoint because a fiber cannot meet both. This would disconnect the target. Applied after algebraic closure, this proves geometric connectedness of X.

### Varying the degree-one quotient

The degree-one quotient varies over B=Gr(r,k^n), with tautological quotient Q. The construction above is functorial in V and applies to Q on B. Alternatively, the total Hilbert scheme maps properly and surjectively to B with geometric fibers X as above. Since B is geometrically connected, the same proper-connected-fiber argument proves the claim. Nonemptiness follows by taking any nonzero rank-one contraction functional (evaluation at a nonzero linear quotient of V) and extending its image to an s-dimensional U. □

### Why the third layer is no longer a bundle

In three variables, let K=span{x²,y²,z²} and K'=span{x²,xy,xz}. Both are three-dimensional subspaces of S_2. The distinct degree-three monomials in S_1K number nine; those in S_1K' are exactly x times the six degree-two monomials. Thus dim(S_3/S_1K)=1 while dim(S_3/S_1K')=4. This rank jump invalidates replacing a general next-stage parameter scheme by a fixed-rank relative Grassmannian. Theorem 2 handles a special next stage by a different projection.

## Control 3. A connected reducible finer-graded scheme

The following control is the family in Haiman–Sturmfels, Example 1.4. Assign deg x=(1,0), deg y=(1,1), deg z=(0,1). In P¹_a×P¹_b take a_1 b_1=0 and the homogeneous ideal generated by

x³, xy², x²y, y³, a_0x²z−a_1xy, b_0xyz−b_1y², y²z, z².

The required quotient Hilbert function is one in degrees (0,0),(1,0),(0,1),(2,0),(2,1),(1,2),(2,2), two in degree (1,1), and zero elsewhere. The total length is nine.

To reconstruct the scheme, all other degrees force the displayed monomial relations. The degree-(2,1) relation chooses a line in span{x²z,xy}, and the degree-(2,2) relation chooses a line in span{xyz,y²}. Multiplying the first relation by z requires a_1 xyz to vanish modulo the second. In the quotient line this is precisely a_1 b_1=0. All remaining multiplication conditions land in already killed pieces. This gives the indicated functorial incidence equation on the product of projective lines.

The equation is the union of {a_1=0}×P¹ and P¹×{b_1=0}, intersecting at ([1:0],[1:0]). Each is a projective line. This proves connectedness and reducibility. The three boundary monomial ideals and the two connecting curves form a path. The supplied computation checks the quotient Hilbert function over three finite fields; the geometric conclusion comes from the equation, not from point counts.

## Control 4. Why the five-variable example is not a three-variable one

For a≥2, in k[x_0,x_1,x_2,y_0,y_1] consider the monomial ideals

J_1=(x_0,x_1^a y_0^(2a)),
J_2=(x_0^(2a),x_0y_0,x_1^a y_0).

These are the two distinguished ideals in Cid-Ruiz's construction. Direct monomial intersection gives

J_2=(x_0,x_1^a)∩(x_0^(2a),y_0).

The verifier checks their bidegree counts against p_a for a=2,…,5 in a specified stable rectangle. Already at bidegree (1,0), the quotient dimensions are 2 and 3; equality of eventual polynomial is not equality of the whole function.

Dehomogenizing x_2=y_1=1 leaves ideals of the same written forms in k[x_0,x_1,y_0]. If the surviving monomials are assigned degrees (1,0),(1,0),(0,1), the quotient dimensions in degree (1,0) are now 1 and 2. Moreover, setting nonzero-degree variables to one is not a homomorphism preserving the original grading. This explains exactly why this simple proposed reduction does not produce the required pair. It says nothing about all other possible constructions.

## Control 5. Rank-one positive toric classification

Let L=Zℓ⊂Z^n with L∩N^n={0}, ℓ≠0, and write ℓ=u−v with disjoint nonnegative supports. Both u and v are nonzero. Use the quotient grading by Z^n/L and the toric Hilbert function, one on the monoid of attained degrees.

The common degree of x^u and x^v contains exactly those two monomials: an additional integer step along ℓ has a negative coordinate on one of the two supports. Any other degree fiber is a finite chain, and adjacent monomials have the form x^w x^u and x^w x^v. Finiteness follows from the presence of both signs in ℓ.

A line of relations [α:β] gives the ideal (αx^u−βx^v). On either standard projective chart one of α,β is invertible. Elimination along each chain identifies the quotient with a free rank-one module generated by the appropriate endpoint. Thus this family has the toric Hilbert function, including at α=0 or β=0.

Conversely an R-valued family in the toric Hilbert scheme determines a line subbundle of R² in the degree of x^u,x^v. Locally it has a generator αx^u−βx^v with one coefficient a unit. The principal ideal it generates is contained in I, and in every degree its rank-one locally free quotient surjects onto the rank-one locally free quotient by I. Such a surjection is an isomorphism. Hence the principal ideal equals I. The construction commutes with base change, proving H_L≅P¹.

The proof uses a generator of L itself, not a primitive generator of its saturation; torsion in Z^n/L causes no change. In three variables positivity excludes rank three because a full-rank sublattice contains a nonzero positive multiple of every coordinate vector. Together with the rank-zero point and the cited rank-two theorem, this proves precisely the positive toric classification, with no conclusion for arbitrary h. □
