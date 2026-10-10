# Recursive determination of quantum knot invariants: scoped partial results

**Target:** 30000962 / OWR-1967-011, original report Conjecture 11, printed p.1223.

**Disposition:** The unrestricted complex-reductive target is not resolved here. Five mathematical approaches are recorded. There is a complete conditional theorem for a q-holonomic knot function, a resulting affirmative conclusion for the simple non-G2 types covered by the cited theorem, a direct all-simple-type unknot result, and explicit limitations of two proposed routes toward the remaining case. No novelty or priority claim is made. The mathematical literature inputs below are credited, not re-proved. This is an author packet awaiting independent review.

The question concerns formal q, and compares *all* functions with the prescribed sign-Weyl symmetry satisfying the invariant annihilator equations. It does not restrict competitors to knot invariants, to competitors having exactly the same annihilator, or to nonsingular weights. It asks for a finite set that may depend on the fixed Lie algebra and knot. It does not ask for a uniform bound over knots, an efficient algorithm, or a root-of-unity specialization. The adjacent strong-AJ/character-variety Conjecture 12 is a different problem.

## 1. Conventions and credited inputs

Let Lambda be a finite-rank lattice and W a finite faithful group of lattice automorphisms. Let B be a nondegenerate W-invariant rational symmetric bilinear form. Work first over F=C(t), where q is a positive integral power of the indeterminate t chosen so that every q^{B(alpha,beta)} belongs to F. The algebra A is generated over F by

- (E_alpha h)(lambda)=h(lambda+alpha),
- (Q_alpha h)(lambda)=q^{B(alpha,lambda)}h(lambda).

Both kinds of operators are invertible. W acts by conjugation: w(E_alpha)=E_{w alpha}, w(Q_alpha)=Q_{w alpha}. For a sign character chi:W -> {1,-1}, write S_chi for functions h with h(w lambda)=chi(w)h(lambda). For Weyl groups chi=det. Put I=Ann_A(f) for f in S_chi. Then I is W-stable: (wP)f=w(P(w^{-1}f))=chi(w)w(Pf)=0.

Let R_0 be the original Laurent-polynomial coefficient ring and K_0 its fraction field. When F=K_0, clearing scalar denominators shows Ann_A(f)=F Ann_{A_{R_0}}(f), and clears denominators in invariant annihilators as well. If F is a further finite parameter extension, denominator clearing alone is not the reason: write an operator in a K_0-basis of F. Since f has values in K_0 and the original operators preserve K_0-valued functions, each basis component of an annihilator also annihilates f. Since W fixes the scalar field, each component of an invariant operator is invariant. Clear denominators componentwise over R_0. Consequently every original-valued competitor satisfying the original invariant equations also satisfies all the F-coefficient invariant equations. Thus proving uniqueness over F implies the requested uniqueness among original Laurent-polynomial-valued functions. No value of q is specialized in a proof below.

The following results are used with their original scope.

1. **[Sikora08], Theorem 3 and Proposition 5:** for a simple complex Lie algebra other than G2, the rho-shifted quantum knot function on the entire weight lattice is q-holonomic and sign-Weyl-equivariant. Theorem 3 credits the argument of Garoufalidis-Lê. The G2 exclusion is retained. The inspected document is arXiv:0807.0943v2, not a verified journal-final version.
2. **[GL16], Proposition 4.1 and Theorem 7.4:** q-holonomic quantum-Weyl modules are closed under subquotients, and a q-holonomic function with values in an arbitrary vector space has a finite determining set among functions with the same annihilator. Theorem 7.4 is printed on p.523; Sections 2 and 3 make the arbitrary-value-vector-space convention explicit. Lemma 2 below handles the difference between equal-annihilator and annihilator-inclusion quantifiers.
3. **[Sikora08], Example 2:** the zero-framed unknot function is the Weyl alternant sum in Proposition 5 below. This is a prior formula.
4. **[KOY13], Section 5.4, Lemma 4:** explicit six-term left multiplication by the short-root generator in one G2 PBW basis. Section 6 uses only two of these terms to test a proposed simplification.

The survey's general introductory wording is not used to erase the G2 restriction in the detailed earlier theorem. Belletti's December 2025 preprint [Belletti25] concerns the elimination criterion and Kauffman-bracket/colored-Jones invariants of links in closed 3-manifolds. Its Section 3.2 does not supply a theorem for arbitrary G2 colors.

## 2. Approach 1: recover the full ideal from invariant equations

### Lemma 1 (regular-orbit extraction, including singular target weights)

Under the conventions above, if h is in S_chi and P h=0 for every P in I^W, then P h=0 for every P in I. Consequently

Sol(I^W) intersect S_chi = Sol(I) intersect S_chi.

**Proof.** Choose beta in Lambda with trivial W-stabilizer. Such a point exists: for each nonidentity w, its fixed space is a proper rational linear subspace, and a lattice cannot lie in the union of finitely many such subspaces. Choose alpha in Lambda such that the numbers B(alpha,w beta), w in W, are pairwise distinct. Again the forbidden alpha lie in finitely many proper rational hyperplanes, because B is nondegenerate and the orbit points are distinct.

Write c_w=q^{B(alpha,w beta)}. Since q is an indeterminate, these are distinct nonzero elements of F. Define the multiplication operator

D = product over w != 1 of (Q_alpha-c_w).

It has value D(beta)=product_{w != 1}(c_1-c_w) != 0 and D(w beta)=0 for w != 1.

Fix any P in I and any target lambda in Lambda, including a weight fixed by reflections. Set gamma=lambda-beta. The left-ideal property puts T=D E_gamma P in I. Its unnormalized Reynolds sum R(T)=sum_{w in W} w(T) belongs to I^W. Compatibility of the operator and function actions gives

(w(T)h)(beta)=chi(w)(T h)(w^{-1}beta).

Every summand with w != 1 vanishes because of the D factor. Hence

0=(R(T)h)(beta)=D(beta)(P h)(beta+gamma)=D(beta)(P h)(lambda).

Since D(beta) is nonzero in the field F, (P h)(lambda)=0. Both P and lambda were arbitrary. The reverse inclusion is immediate. QED.

**Why simple averaging was insufficient.** An individual P may have zero Reynolds average, for example E_a-E_{-a} for the rank-one reflection. Multiplication by D before averaging retains a selected orbit value. Applying an additional shift E_gamma *before* extraction is essential: extraction only at regular weights without this shift would leave recursions evaluated on singular walls unproved. The statement does not assert I=A I^W as ideals; it asserts equality of the indicated solution spaces.

### Lemma 2 (uniform finite determination from the published vector-valued theorem)

Let W_r be the standard quantum Weyl algebra over R=k(z), z transcendental. Let I be a left ideal with W_r/I q-holonomic. There is a finite set S in Z^r such that every scalar-valued solution of I is determined by its values on S. In particular, competitors may have strictly larger annihilator ideals.

**Proof.** Let U={h:Z^r -> R : I h=0}, an R-vector space. Let V=R^U, the unrestricted vector space of families indexed by U. Define the universal sequence H(n)=(h(n))_{h in U}. Then I annihilates H and W_r H is a quotient of W_r/I, so it is q-holonomic. Apply [GL16, Theorem 7.4] to H with this value space V. It provides a finite S such that any V-valued G with Ann(G)=Ann(H) and G|S=H|S equals H.

Let V_0 be the span in V of {H(s):s in S}. Every R-linear automorphism T of V fixing V_0 pointwise satisfies Ann(T H)=Ann(H), because T is injective and commutes with all scalar-coefficient sequence operators. It also fixes H|S. Therefore T H=H.

The vectors fixed by every such automorphism are exactly V_0. To see the nontrivial inclusion, if v is outside V_0, extend a basis of V_0 by v and then to a basis of V. The automorphism that sends v to 2v and fixes the other basis vectors fixes V_0 but moves v. Characteristic zero ensures 2 != 1. Thus H(n) belongs to V_0 for every n. Write H(n)=sum_{s in S} a_{n,s}H(s). Coordinatewise, this says h(n)=sum_{s in S}a_{n,s}h(s) simultaneously for *all* h in U. Evaluation on S is therefore injective. QED.

This argument uses the algebraic vector space V; no topology, boundedness, continuity, finite-dimensionality of V, or interchange of infinite sums is assumed. The product R^U is a set. The only sums displayed in the reconstruction are finite. The set S is chosen once for I, not separately after selecting a competitor.

### Lattice and parameter bridge

The bilinear-form quantum torus in Section 1 need not have the standard coordinate commutation matrix. Choose a basis of Lambda and write B as a rational invertible matrix. Choose a positive integer c such that v_i=c B^{-1}e_i is integral for every coordinate vector e_i. Then the operators L_i=E_{e_i} and M_i=Q_{v_i} satisfy L_i M_j=q^{c delta_ij}M_j L_i. They generate a standard coordinate quantum torus with parameter z=q^c. Over C(z), F=C(t) is a finite extension. A word of length N in these coordinate operators has length O(N) in fixed original generators. Thus an O(N^r) growth bound over F for A f implies an O(N^r) growth bound over C(z) for the cyclic coordinate module; the constant increases by at most [F:C(z)]. This is enough to transfer the stated q-holonomicity to the coordinate convention of Lemma 2. More explicitly, let A_0 be this coordinate algebra over R=C(z), and let J=Ann_{A_0}(f). Every solution of the full original ideal satisfies J, and A_0/J is the cyclic coordinate module just bounded. To cover F-valued competitors, let U be all F-valued solutions of J and regard V=F^U as an R-vector space. The universal sequence H(n)=(h(n))_{h in U} is a quotient of A_0/J. The proof of Lemma 2 now applies verbatim using R-linear automorphisms of V. This invokes the published theorem over its stated rational-function field, without any additional coefficient-field version. No change of the lattice domain or enlargement of the multiplier algebra is required.

For the cited non-G2 application the growth premise can also be obtained directly in fundamental-weight coordinates. [GL05, Theorem 6] supplies the dominant-color function on N^r in standard coordinates. Extend it by zero to Z^r and shift by rho=(1,...,1); then sum its pullbacks by W with signs. There is exactly one nonzero summand at each regular weight and none on a chamber wall, so [Sikora08, Proposition 5] identifies the result with J_{g,K}. Zero extension, integral affine substitutions and finite sums preserve holonomicity by [GL16, Proposition 5.4 and Theorem 5.2]. After choosing one common integral-root parameter t, the original multipliers are integer monomials in the standard t-coordinate multipliers, so their word filtration is bounded by the standard one. Finite scalar-field extensions and restriction to C(z) change the dimension bounds only by fixed finite factors. If passing to t also adjoins standard coordinate multipliers, decompose their exponent vectors into the finitely many residue classes modulo the parameter power; each summand is a fixed multiplier applied to an old filtered piece, so the same O(N^r) bound remains valid. This supplies the required growth bound without assuming that a first-order ratio of an unrelated Gaussian belongs to A.

### Theorem 3 (conditional answer and credited non-G2 consequence)

If f is sign-Weyl-equivariant and q-holonomic on its lattice, then a finite set of values together with I^W determines f among all sign-Weyl-equivariant functions of the original value type. In particular this conclusion holds for J_{g,K} for every knot K and every simple complex g other than G2 covered by [Sikora08, Theorem 3].

**Proof.** A competitor satisfying invariant equations also satisfies every full-ideal equation by Lemma 1. Lemma 2, after the coordinate bridge, supplies a finite determining set for all such solutions. Agreement there forces equality. Scalar denominators can be cleared as explained in Section 1. QED.

This is a consequence of credited q-holonomicity and finite-determination inputs, with an explicit invariant-equation bridge. It is not a new proof of q-holonomicity or a certified first historical solution of these cases. The missing G2 premise is not established by Theorem 3.

## 3. Approach 2: direct nonsingular propagation and the singular-strip obstruction

An alternative way to bypass a general holonomicity theorem would be to construct a particularly well-behaved finite recursion system directly for the remaining knot functions.

### Proposition 4 (a sufficient global box certificate)

Suppose for each coordinate i there is a recursion

sum_{j=0}^{d_i} a_{i,j}(n)h(n+j e_i)=0, with d_i >= 1,

valid for every n in Z^r and with both endpoint coefficients a_{i,0}(n), a_{i,d_i}(n) nonzero for every n. Then every solution is determined by its values on the box product_i {0,...,d_i-1}. Its solution-space dimension is at most product_i d_i.

**Proof.** Fix every coordinate except the first within its box range. The first recursion propagates uniquely in both directions from d_1 consecutive values. This gives the first unrestricted coordinate and the remaining coordinates in their box ranges. Now fix the first coordinate arbitrarily and the third through last coordinates in their box ranges, and propagate the second coordinate in both directions. Continue until all coordinates are unrestricted. For uniqueness apply this procedure to a solution vanishing on the box. Consistency is irrelevant to uniqueness: a solution is already assumed to exist. QED.

The corresponding rank-one statement needs only a finite exceptional interval. A nonzero Laurent polynomial a(q,q^n) is zero as an element of C(q) for only finitely many integers n. Indeed, after expanding a into finitely many monomials c_{u,v}q^{u+vn}, cancellation requires equality between two distinct affine exponents; outside finitely many collision values, the surviving monomials have distinct exponents. A recurrence with nonzero endpoint polynomials can therefore be propagated outside a finite interval containing all exceptional indices. A finite interval of seeds covers what remains. This reconstructs the familiar rank-one result without claiming a new theorem.

The same finite-exception argument fails in several dimensions. Consider r=2, M_1h(n,m)=q^n h(n,m), and

P_1=(M_1-1)(q M_1-1)(L_1-1),
P_2=(M_1-1)(L_2-1).

For every arbitrary sequence a:Z -> F, the function h_a(n,m)=delta_{n,0}a(m) satisfies both equations. The first difference is supported only at n=-1,0, where its coefficient vanishes; the second is supported at n=0. Given any finite set S in Z^2, choose m_0 not occurring as a second coordinate in S and put a=delta_{m,m_0}. This gives a nonzero common solution vanishing on S. Both equations have a shift and nonzero polynomial endpoint coefficients, but the coefficient-zero locus contains an entire integer line. Thus those properties alone do not give a finite determining set.

This is an obstruction to an *auxiliary inference*, not a counterexample involving any knot function, and not a counterexample to holonomic finite determination. No globally nonsingular box certificate for every G2 knot was found. Localizing coefficients away from their zeros cannot remove the missing values on singular strips in a uniqueness proof on the entire lattice.

## 4. Approach 3: solve the unknot by its finite spectral support

### Proposition 5 (the unknot needs one normalizing value)

For every simple root system, including G2, the zero-framed unknot function in [Sikora08, Example 2] is determined among sign-Weyl-equivariant functions by its invariant annihilator ideal and the single value J(ρ)=1.

**Proof.** Let eta_w=wρ. The points eta_w are distinct because ρ is strictly dominant. Define characters x_w(lambda)=q^{B(lambda,eta_w)} and

J(lambda)= [sum_w det(w)x_w(lambda)] / [sum_w det(w)x_w(ρ)].

The denominator is nonzero: B(ρ,ρ)>B(ρ,wρ) for w != 1, since the Weyl-invariant form is positive definite on the real root space, so the highest q-exponent occurs only once. Equivalently, use the usual Weyl denominator identity. Thus J(ρ)=1.

Let T=F[Lambda] be the commutative Laurent algebra of shifts. Each x_w is its joint eigenfunction with character E_alpha -> q^{B(alpha,eta_w)}. The eigencharacters are distinct. Let m_w be the corresponding maximal ideal and H=intersection_w m_w. Then H annihilates J, so H is contained in I. By the Chinese remainder theorem, T/H is the direct product of |W| copies of F, with mutually orthogonal idempotents e_w summing to 1.

If h is annihilated by H, the shift-module T h is a quotient of T/H. Consequently h=sum_w h_w, where h_w=e_w h satisfies E_alpha h_w=q^{B(alpha,eta_w)}h_w for every alpha. Taking lambda=0 in the shift equation gives h_w(lambda)=h_w(0)x_w(lambda). Hence h is a finite linear combination sum_w c_w x_w.

The characters x_w are linearly independent. For a direct proof choose a lattice vector alpha that separates eta_w, restrict to lambda=k alpha for k=0,...,|W|-1, and use the nonzero Vandermonde determinant on the distinct scalars q^{B(alpha,eta_w)}. The sign-Weyl condition therefore forces c_w=det(w)c_1. Thus h is a scalar multiple of J. The value at ρ fixes the scalar.

Finally a competitor satisfying I^W satisfies I by Lemma 1 and in particular H. The preceding argument applies. QED.

This directly includes the G2 unknot but says nothing about the colored function of an arbitrary nontrivial G2 knot: its spectral support need not be this finite Weyl orbit. The prior unknot formula is credited. No claim is made that one seed value suffices for an arbitrary knot.

## 5. Approach 4: tensor products, central Gaussian factors, and the limit of subgroup reduction

### Proposition 6 (product stability)

Let f:Z^r -> F and g:Z^s -> F each be finitely determined among solutions of their *full* annihilator ideals, with determining sets S and T. Then F_0(x,y)=f(x)g(y) is finitely determined among solutions of its full ideal by S x T.

**Proof.** Ann(f), acting in the first variables, and Ann(g), acting in the second variables, are contained in Ann(F_0). If a solution h of Ann(F_0) vanishes on S x T, then for every y in T the first-variable slice is annihilated by Ann(f) and vanishes on S, so it is zero for all x. For every x, the second-variable slice is annihilated by Ann(g) and now vanishes on T, hence it is zero for all y. Apply this to the difference of two solutions. QED.

For semisimple direct sums, the standard quantum-group tensor construction gives the requisite product identity: an irreducible representation is an exterior tensor product, the two factors of the universal R-matrix act on their own tensor factors, evaluations and coevaluations tensor, and the final quantum traces multiply. Thus the result extends the simple non-G2 cases to semisimple direct sums having no G2 factor. Applying Lemma 1 for the product Weyl group gives the invariant-ideal version.

A formal central factor f_z(n)=q^{Q(n)}, for a fixed rational quadratic polynomial Q with exponent denominators cleared, has a one-value certificate **provided each first-order shift ratio is a multiplier in the actual operator algebra A**. Explicitly, require for each i that Q(n+e_i)-Q(n)=c_i+B(v_i,n) with v_i in Lambda and q^{c_i} in F. Then E_{e_i}-q^{c_i}Q_{v_i} annihilates f_z, and its nonvanishing two-ended first-order recursion determines the function from n=0. Clearing scalar exponent denominators does not by itself imply this multiplier-lattice condition.

For an exact warning, take Lambda=Z, F=C(t), q=t^2, B(a,n)=2an, and f_z(n)=q^{n^2/2}=t^{n^2}. The available basic multiplier is Q_1 h(n)=t^{4n}h(n), whereas the one-step ratio is t^{2n+1}. Every full-annihilator solution space contains h(n)=c_{n mod 2}t^{n^2} with independently chosen c_0,c_1 in F. Indeed, write any annihilator in normal order P=sum_{a,b} p_{a,b}(t)Q_1^a E_1^b. Dividing P f_z by t^{n^2} gives sum_{a,b}p_{a,b}(t)t^{b^2}(t^{4a+2b})^n. Distinct exponential characters are linearly independent by a finite Vandermonde argument, so cancellation occurs separately within equal-slope groups. Equal slopes force b to have the same parity, and replacing f_z by h multiplies each such zero group by the single scalar c_{(n+b) mod 2}. Thus P h=0 for every P in Ann(f_z). One seed cannot distinguish these solutions. The nonsingular relation E_1^2-t^4Q_1 determines them from two consecutive values. This counterexample concerns only the unrestricted one-value aside; it does not contradict finite determination or the coordinate bridge in Section 2.

The one-value certificate therefore covers only central factors whose chosen reductive invariant convention verifies the displayed multiplier-lattice condition. It does not settle all normalization and bilinear-form choices for an unrestricted reductive center: the original use of a Cartan determinant/Killing-form normalization is stated for semisimple data in the accompanying formulas.

Replacing a direct product by a Lie subalgebra inclusion is not the same argument. Restricting a representation to rank-one subalgebras does not factor the braiding into independent tensor factors; the root operators need not commute and the coproduct/R-matrix data are not specified by a mere list of restricted dimensions. Proposition 6 therefore cannot remove the simple G2 case. No all-G2 reduction to rank-one knot functions is proved.

## 6. Approach 5: G2 PBW multiplication and failure of a naive q-multinomial shortcut

The remaining simple type has six positive roots. [KOY13, Section 5.4] gives explicit finite-shift formulas for multiplication by its two Chevalley generators. A possible route is to expand arbitrary powers of such multiplication operators by a fixed-dimensional q-multinomial sum, then insert those coefficients into the fixed-knot R-matrix state sum. This would require a justified uniform summation formula; knowing only a one-step matrix does not supply it.

Here is an explicit obstruction to the simplest proposed expansion. Use the PBW exponent order (a,b,c,d,e,f) in [KOY13, Lemma 4], whose root degrees are

(0,1), (1,1), (3,2), (2,1), (3,1), (1,0).

Two terms of left multiplication by e_1 are the weighted shifts A and B:

A v_n = -(q-q^{-1}) [c]_{q^3} q^{3a+b-3c+2} v_{n+(0,0,-1,2,0,0)},

B v_n = [3]_q [b-1]_q [b]_q q^{3a-b+2} v_{n+(0,-2,1,0,0,0)},

where [m]_u=(u^m-u^{-m})/(u-u^{-1}). Both shifts increase the root weight by the short simple root (1,0), as required. For b>=2 and c>=1, both compositions are nonzero and lead to the same exponent vector. Their coefficient ratio is

coefficient(AB v_n) / coefficient(BA v_n)
 = q^{-5} [c+1]_{q^3}/[c]_{q^3}.

Indeed B decreases b by two and increases c by one, which multiplies the A coefficient by q^{-5}[c+1]_{q^3}/[c]_{q^3}; A does not alter a or b and therefore leaves the B coefficient unchanged. The ratio depends on c. For instance at q=2 it is 65/256 for c=1, and 4161/16640 for c=2. Consequently no scalar κ in C(q), independent of PBW coordinates, satisfies AB=κ BA. The pairwise q-commuting hypothesis needed for the elementary q-multinomial theorem fails for this decomposition.

This does not prove non-holonomicity, invalidate the published formulas, exclude a different decomposition, or refute Conjecture 11. It identifies the exact failed step in this attempted summation route. [GL05] specifically needs uniform q-holonomic data with arbitrary power and PBW indices; its Appendix A, Remark A.3 records the G2 structure-constant issue. This packet supplies neither those uniform data nor a substitute finite-determination theorem for every G2 knot.

## 7. Result and remaining tasks

The following statements are established at the stated scope:

- Invariant equations and full equations have the same sign-equivariant solution space, by a direct algebraic proof that includes singular target weights.
- A fixed q-holonomic ideal has one finite determining set for all its scalar solutions, using the published arbitrary-vector-space finite-determination theorem and the universal-family argument.
- The original uniqueness conclusion follows for every simple non-G2 type covered by the cited knot-holonomicity result, and by products for semisimple sums of those types.
- The zero-framed unknot has a direct one-value uniqueness proof for every simple type, including G2.
- Global nonsingular rectangular propagation is sufficient. Merely having coordinate recursions with nonzero polynomial endpoints is insufficient, as the singular-strip model proves.
- Two terms in the natural G2 one-step PBW expansion fail the scalar q-commutation test, so the naive q-multinomial shortcut does not finish the missing case.

The general G2-knot case and the full unrestricted reductive statement remain unproved in this investigation. No counterexample is given. Search nonfindings do not certify the current literature-wide status. These five approaches exhaust the assigned author budget; source checking, finite diagnostics, packaging, and future audits are not additional attempts.

## References

[OWR08] A. S. Sikora, contribution “Quantizations of Character Varieties and Quantum Knot Invariants,” in *Invariants in Low-Dimensional Topology*, Oberwolfach Reports 5 (2008), report 22, pp.1221–1224. Conjecture 11 on p.1223. Report published 31 March 2009. https://ems.press/journals/owr/articles/1967 ; https://ems.press/content/serial-article-files/46168 ; https://doi.org/10.4171/OWR/2008/22 .

[Sikora08] A. S. Sikora, *Quantizations of Character Varieties and Quantum Knot Invariants*, arXiv:0807.0943v2 (18 July 2008). Theorem 3, Example 2, Proposition 5, Conjecture 7. https://arxiv.org/abs/0807.0943v2 ; https://arxiv.org/pdf/0807.0943 .

[GL05] S. Garoufalidis and T. T. Q. Lê, *The colored Jones function is q-holonomic*, Geometry & Topology 9 (2005), 1253–1293. Inspected author PDF dated 20 July 2005, Theorems 1, 2, 6; Section 7 and Appendix A. https://people.mpim-bonn.mpg.de/stavros/publications/holonomic.pdf ; https://arxiv.org/abs/math/0309214 .

[GL16] S. Garoufalidis and T. T. Q. Lê, *A survey of q-holonomic functions*, L'Enseignement Mathématique 62 (2016), 501–525. https://doi.org/10.4171/LEM/62-3/4-7 ; https://ems.press/content/serial-article-files/44334 .

[KOY13] A. Kuniba, M. Okado and Y. Yamada, *A Common Structure in PBW Bases of the Nilpotent Subalgebra of U_q(g) and Quantized Algebra of Functions*, SIGMA 9 (2013), 049, 23 pp. Section 5.4 and Lemma 4, printed p.19. https://doi.org/10.3842/SIGMA.2013.049 ; https://arxiv.org/abs/1302.6298 ; https://emis.de/ft/13018 .

[Belletti25] G. Belletti, *An equivalent condition for q-holonomicity*, arXiv:2512.10837v1 (11 December 2025), preprint. Theorem 2.7 and Section 3.2. https://arxiv.org/abs/2512.10837v1 ; https://arxiv.org/html/2512.10837v1 .
