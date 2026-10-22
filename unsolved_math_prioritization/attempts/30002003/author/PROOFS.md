# Five approaches to the spherical stringy Euler criterion

## 0. Scope, definitions, and external inputs

All varieties and groups in this note are over C. A spherical G-variety is a normal irreducible variety with an action of a connected reductive algebraic group G and a dense orbit of a Borel subgroup. Horospherical means that the stabilizer of the dense G-orbit contains a maximal unipotent subgroup. Toric varieties are a special case. These three classes are not interchangeable.

The correctly qualified mathematical target, checked against [BM, Conjecture 6.7], is:

> For every locally factorial spherical G/H-embedding X whose closed G-orbits are projective, e_st(X) >= e(X), and e_st(X)=e(X) if and only if X is smooth.

The exact current public dataset row, recovered after the five approach families had been developed, omits the projective-closed-orbit hypothesis and asks only for the equality criterion in the unrestricted locally factorial spherical class. Approach 4 completely disproves that literal formulation. It does not disprove the qualified statement above. See STATEMENT_AUDIT.md.

Here e is the compactly supported topological Euler characteristic, equivalently the Hodge–Deligne polynomial at (1,1). For complex algebraic varieties it agrees with the usual topological Euler characteristic. It is not the number of orbits and is not a normalized volume unless a separate theorem identifies them. It is additive under locally closed decompositions and multiplicative for products and locally trivial fibrations.

For a normal Q-Gorenstein log-terminal variety take a log resolution f:Y -> X with exceptional SNC divisors E_1,...,E_s and

    K_Y = f^* K_X + sum_i a_i E_i,    a_i > -1.

For J subset of {1,...,s}, let E_J^o be the locus lying in exactly the divisors indexed by J, including the complementary open stratum for J empty. Then

    e_st(X) = sum_J e(E_J^o) product_{j in J} 1/(a_j+1).

The empty product is 1. A resolution may be chosen to be an isomorphism over the smooth locus; further blowups of smooth centers give the same invariant and are allowed in the cone calculations below. One must take the limit at (u,v)=(1,1) of each rational stringy factor; substituting before cancellation would give 0/0. These are the ordinary/topological stringy invariants, not a substituted algebraic-cohomology invariant.

For locally factorial normal X the Weil divisor K_X is Cartier. A Q-Gorenstein spherical variety is log terminal; thus the target's invariant is defined. The latter implication, including its Q-Gorenstein qualification, is reviewed in [P, Section 5] and [BG, introduction]. Equivariant log resolutions with SNC exceptional locus are available [P, Remark 3.5]. With K_X Cartier, all a_i are integers, hence nonnegative by log terminality. Completeness or projectivity of X is not assumed in the target. Projectivity of its closed orbits is expressly retained.

The standard external foundations used below are the toric Cartier-divisor criterion, Euler-characteristic integration for algebraic morphisms, the torus fixed-point formula for Euler characteristic, Kodaira vanishing, Serre duality, the Hilbert polynomial, and Nagata's localization criterion for factoriality. Their uses and assumptions are explicit. No proposed new global theorem is imported as an axiom.

## Approach 1. Toric lattice regularity and the obstruction from colors

### Proposition 1.1
Every locally factorial toric variety is smooth, without a completeness assumption. Consequently its stringy and ordinary Euler characteristics are equal.

Proof. Work on a torus-invariant affine chart U_sigma for a strongly convex rational cone sigma in a lattice N. Let v_1,...,v_k be its primitive ray generators and M=Hom(N,Z). A torus-invariant Cartier divisor on U_sigma has a character as its Cartier datum. Local factoriality therefore says that for every i there is m_i in M such that

    <m_i,v_j> = delta_ij.

Indeed apply the toric Cartier criterion to the invariant prime divisor corresponding to v_i, with all other coefficients zero. These equations first imply that v_1,...,v_k are linearly independent. They also give a retraction N -> Z^k, n |-> (<m_1,n>,...,<m_k,n>), of the map Z^k -> N carrying the standard basis to the v_i. Thus the sublattice they generate is a direct summand and they extend to a Z-basis of N. In this basis the semigroup sigma^vee intersect M is N^k x Z^(rank N-k). Its algebra is a polynomial algebra in k variables with the other variables invertible. Hence U_sigma is A^k x (C*)^(rank N-k), which is smooth. These charts cover X. For smooth X use its identity as the resolution in the stringy formula; only the empty stratum occurs and e_st=e. QED.

The converse, smooth toric implies locally factorial, is the general fact that regular local rings are factorial. The proposition therefore identifies the toric part of the target completely, but it has no singular locally factorial toric examples to control.

### What fails in passing to the colored fan
The same integral-basis condition is only part of spherical smoothness. Colors record additional geometry. The explicit four-dimensional factorial quadric cone in Approach 4 is singular and horospherical. Thus even inside the smaller horospherical class, a regular lattice cone is not sufficient to prove smoothness. Replacing a colored fan by its underlying uncolored fan discards precisely relevant information.

[BM, Theorem 5.3] proves the inequality and equality criterion for simple locally factorial horospherical embeddings with projective closed orbit. It is an established special-case theorem, not a solution of the arbitrary spherical target. No fresh proof of its root-system case analysis is claimed here.

**Exact obstruction:** the toric lattice argument detects only uncolored chart singularities. It supplies no bound on the stringy contribution of general spherical colors or spherical roots. The route stops at that missing representation-theoretic inequality.

## Approach 2. Cones, discrepancies, and a complete Fano-base criterion

This approach proves a genuine family theorem by computing a resolution, rather than inferring a universal result from examples. The cone calculation is known; compare [DD, Proposition 3.1] and [BM]. No novelty is claimed.

### Proposition 2.1: cone formula
Let V be a smooth connected projective variety of dimension d>=1, L a very ample line bundle, and assume the section ring R=sum_{m>=0} H^0(V,L^m) is generated in degree one. Assume the affine cone C=Spec R is normal and Q-Gorenstein. Suppose K_V=-rL for a positive integer r. Then C is log terminal and

    e(C)=1,    e_st(C)=e(V)/r.

Proof. The blowup of the vertex is the total space Y of L^(-1), with exceptional zero section D=V; this follows directly by taking the incidence variety of vectors in their projective lines in the degree-one embedding. Away from the vertex the cone is the punctured line bundle, and the incidence map is an isomorphism. Y and D are smooth, so this is a log resolution (it is allowed to blow up even when C itself is smooth).

Write K_Y=f^*K_C+aD, since D is the sole exceptional divisor. Restrict a Cartier multiple of this equality to D. The restriction of f^*K_C is Q-linearly trivial, since D maps to a point. Adjunction and the normal bundle give

    K_Y|_D = K_V - D|_D = -(r-1)L,
    D|_D = -L.

Since L has nonzero degree on a curve, a=r-1. In particular a>-1, and this log resolution verifies log terminality. The punctured cone has Euler characteristic e(V)e(C*)=0, since it is a locally trivial punctured line bundle. Adding its vertex gives e(C)=1. In the stringy formula the open part contributes 0 and D contributes e(V)/(a+1)=e(V)/r. QED.

The Q-Gorenstein condition in this proposition is a hypothesis, not an inference from normality. [DD] proves the stronger Gorenstein conclusion for the corresponding complete section ring under the subcanonical hypotheses. This note does not need that extra conclusion to deduce the formula.

### Proposition 2.2: equality forces a linear cone
Under Proposition 2.1, additionally assume H^odd(V,Q)=0. Then

    e_st(C)>=e(C)=1,

and equality holds exactly when (V,L)=(P^d,O(1)), in which case C=A^(d+1).

Proof. Let h=c_1(L). For each 0<=i<=d, h^i is nonzero in H^(2i)(V,Q): otherwise h^d=h^i h^(d-i) would be zero, contradicting the positive intersection number L^d. Thus every even Betti number b_(2i) is at least one. Since odd cohomology vanishes,

    e(V)=sum_{i=0}^d b_(2i)>=d+1.

Next prove r<=d+1, including its equality case. For 1<=k<=r-1, the line bundle -kL equals K_V+(r-k)L. Kodaira vanishing gives H^i(V,-kL)=0 for i>0. There are no nonzero global sections of a negative ample line bundle: its effective divisor, if nonzero, would have negative intersection with L^(d-1); a nowhere-vanishing section would make it trivial, also impossible. Thus the degree-d Hilbert polynomial P(t)=chi(V,L^t) has distinct roots -1,...,-(r-1). Its leading coefficient is L^d/d!>0. Therefore r-1<=d.

If r=d+1, the d roots imply P(t)=c product_{j=1}^d(t+j). Kodaira applied to O_V=K_V+rL gives H^i(O_V)=0 for i>0, so P(0)=1 and c=1/d!. Applying Kodaira to L=K_V+(r+1)L gives h^0(L)=P(1)=d+1. The very ample complete linear system therefore embeds the d-dimensional irreducible V into P^d. A closed irreducible subvariety of the same dimension as P^d is all of P^d, and the pulled-back hyperplane bundle is L. Consequently (V,L)=(P^d,O(1)). Conversely that pair has r=d+1 and e(V)=d+1.

Now combine

    e_st(C)=e(V)/r >= (d+1)/r >= 1.

Equality throughout forces r=d+1, hence the stated pair. Its full section ring is a polynomial algebra and its cone is affine space. QED.

This covers, for example, cones over smooth projective homogeneous spaces with a very ample subcanonical polarization when the cone hypotheses hold, since their Schubert-cell decompositions give vanishing odd cohomology. To regard any such example as an instance of the original target, its local factoriality and spherical group action must also be checked. Proposition 2.2 alone does not assert those properties for every Fano base.

### Projective-cone corollary
For the projective cone Cbar over the same (V,L), assume normality and Q-Gorensteinness as before. The complement of its vertex is a line bundle over V, so e(Cbar)=e(V)+1. The vertex has the same local resolution and discrepancy as the affine cone. Hence

    e_st(Cbar)=e(V)+e(V)/r,
    e_st(Cbar)-e(Cbar)=e(V)/r-1.

The inequality and equality classification from Proposition 2.2 follow unchanged. This is not an assumption that every complete spherical variety is a cone.

**Exact obstruction:** a general spherical singularity need not have a resolution with a single smooth Fano exceptional divisor, and its global variety need not be either of these cones. In multiple-divisor resolutions, intersections and different discrepancies replace the single ratio e(V)/r. No reduction of all target singularities to this cone theorem was obtained.

## Approach 3. Local stringy weights and the direction of discrepancy bounds

### Proposition 3.1: exact orbitwise reduction
Let X be a Q-Gorenstein log-terminal spherical variety and choose an equivariant log resolution as in Section 0. For x in X define

    s_X(x)=sum_J e(E_J^o intersect f^(-1)(x)) product_{j in J}1/(a_j+1).

This is constant on each G-orbit O. Writing its value s_X(O), one has

    e_st(X)-e(X) = sum_{O in X/G} e(O)(s_X(O)-1).

Proof. The group G is connected, so it preserves each exceptional irreducible component and each stratum E_J^o. Equivariance identifies the relevant fibres over any two points in one orbit, giving constancy. Algebraic Euler-characteristic integration gives

    e(E_J^o)=sum_O e(O)e(E_J^o intersect f^(-1)(x_O)).

For completeness, this identity is the finite-stratification form of constructible pushforward: stratify the target into sets over which the Euler characteristic of the fibre is constant, then use additive Euler integration. Refining by the finitely many G-orbits does not change the identity. Substitute it into the finite stringy sum, interchange the two finite sums, and use e(X)=sum_O e(O). QED.

The local number is independent of the chosen equivariant log resolution: the same change-of-variables argument defining the stringy invariant works over a constructible subset, including the point x. Independence is not required for the displayed finite computation on a fixed resolution.

### Lemma 3.2: nonnegative orbit Euler numbers
Every homogeneous space G/H of a connected complex reductive G has nonnegative Euler characteristic. If it is projective, its Euler characteristic is positive.

Proof. Let T be a maximal torus of G. The torus fixed-point Euler formula gives e(G/H)=e((G/H)^T). A fixed coset gH means g^(-1)Tg is contained in H. If this never occurs the fixed-point set is empty and the Euler number is zero. Otherwise conjugate H so T is contained in H. Every maximal torus of H^0 is conjugate within H^0; thus every fixed coset has a representative in N_G(T), and

    (G/H)^T = N_G(T)/N_H(T).

This is a finite set, with positive integer cardinality |W_G|/|N_H(T)/T|. If G/H is projective, H is parabolic and contains a maximal torus, so this positive case applies. QED.

### Consequence and exact unproved local step
If one could establish s_X(O)>=1 for every orbit of every locally factorial X in the target, and s_X(O)>1 for every singular closed orbit, then Proposition 3.1 would prove the full conjecture. Indeed a nonempty singular locus is closed and G-stable. Among its finitely many orbits choose a minimal one in the closure order; it is closed in X. The assumed projectivity makes its Euler number positive, so that term is strictly positive while all others are nonnegative. Smooth X gives equality by the identity resolution.

This is a conditional reduction, not a proof of either local inequality. In particular, a singularity on an orbit of Euler number zero can be invisible to the global sum unless one controls a singular closed orbit. Approach 4 makes this issue concrete.

### Proposition 3.3: the elementary bound goes the other way
For a locally factorial spherical X and an equivariant log resolution Y as above,

    e_st(X)<=e(Y).

Proof. Since K_X is Cartier, all discrepancies are integers; since X is log terminal, a_i>=0. Every coefficient product 1/(a_j+1) is therefore in (0,1]. The spherical resolution Y has finitely many G-orbits, and each E_J^o is a union of such orbits. Lemma 3.2 implies e(E_J^o)>=0. Termwise comparison with coefficient 1 gives

    e_st(X)<=sum_J e(E_J^o)=e(Y).

QED. This only bounds the stringy number above by the Euler number of a resolution. It says nothing by itself about the required lower bound e(X). Even abstract nonnegative fibre Euler numbers and positive weights do not imply s_X(x)>=1: a single weight 1/2 times Euler number 1 is 1/2. This arithmetic example is a failure of an inference, not a claimed geometric counterexample.

The proven Mori-program monotonicity in [BG, Theorem 1.8] also compares stringy quantities on different birational models. It cannot be read as e_st(X)>=e(X). The latter substitution would discard the defining discrepancy weights and is not in that theorem.

**Exact obstruction:** prove the required lower and strict local bounds for the weighted Euler sum of a general locally factorial spherical slice. Positivity of orbit Euler numbers and of discrepancies alone is insufficient. The 2026 spherical-skeleton criterion [GHP, Theorem 1.5] recognizes smoothness through a different invariant; no comparison of that invariant with s_X was derived.

## Approach 4. Products, preservation results, and an exact hypothesis control

### Proposition 4.1: product formula
For a Q-Gorenstein log-terminal X and a smooth complex variety S,

    e_st(X x S)=e_st(X)e(S),
    e(X x S)=e(X)e(S).

Proof. The product of a log resolution of X with S is a log resolution of X x S. Its exceptional strata are E_J^o x S and have the same discrepancies, by the product formula for canonical divisors. Apply multiplicativity of Euler characteristic to each stratum. The ordinary formula is ordinary multiplicativity. QED.

More generally, multiplying two log resolutions proves e_st(X x Z)=e_st(X)e_st(Z) for two log-terminal Q-Gorenstein factors: the exceptional strata are the pairwise products, and the discrepancy weights factor. If e(X),e(Z)>0 and both deficits Delta=e_st-e are nonnegative, then

    Delta(X x Z)=Delta(X)e(Z)+Delta(Z)e(X)+Delta(X)Delta(Z).

All terms are nonnegative, and their sum vanishes precisely when both deficits vanish. This is a numerical preservation statement; geometric membership of a product in the target must be checked separately. In particular, multiplication by a smooth projective homogeneous space, of positive Euler number, preserves a strict or zero deficit.

### Explicit factorial horospherical cone
Set

    C = Spec C[x1,x2,x3,x4,x5]/(x1*x2+x3*x4+x5^2).

It has dimension four, is singular exactly at the origin, and is factorial. Here are checks of every assertion needed for the negative control.

The quadratic form is nondegenerate and irreducible. The Jacobian equations force all five variables to vanish, so the origin is the sole singular point, and the tangent space there has dimension five rather than four. The hypersurface is Cohen–Macaulay and regular in codimension one, hence normal by Serre's criterion. Localizing at x1 eliminates x2 and yields the UFD C[x1,x1^(-1),x3,x4,x5]. The element x1 is prime: its quotient is C[x2,x3,x4,x5]/(x3*x4+x5^2), a domain because the rank-three quadratic is irreducible. Nagata's class-group localization sequence says Cl(C) is generated by prime divisors over x1; there is only the principal prime (x1). Thus Cl(C)=0 and its coordinate ring is a UFD, so all its local rings are factorial.

Under G=SO(5,C), the nonzero null vectors form a single orbit. A highest-weight null vector in the standard representation is fixed by a maximal unipotent subgroup; its stabilizer therefore contains that subgroup. Consequently the dense orbit is horospherical, hence spherical. The other orbit is the origin. Thus C is a simple, locally factorial horospherical embedding with a projective closed orbit (a point).

The blowup at the vertex has exceptional smooth projective quadric Q^3, and discrepancy a=2: the ambient blowup of A^5 has discrepancy 4, while the quadric has multiplicity 2, so adjunction subtracts 2. Thus C is Gorenstein log terminal. The odd-dimensional smooth quadric Q^3 has Euler number 4. One can compute this without a numerical guess: cutting by an isotropic-coordinate chart decomposes a smooth Q^m into A^m and a projective cone over Q^(m-2); hence e(Q^m)=2+e(Q^(m-2)), with e(Q^1)=2 and e(Q^0)=2. In particular e(Q^3)=4 and e(Q^4)=6. The cone formula gives

    e(C)=1,    e_st(C)=4/3,    Delta(C)=1/3.

### Counterexample only when the closed-orbit condition is dropped
Let Z=C x C*, with group SO(5,C) x C* acting on the respective factors. Its coordinate ring is a Laurent-polynomial extension of a UFD, hence is factorial. It is normal, Gorenstein, log terminal and spherical; a product of the dense Borel orbits is dense. Its singular locus is {0} x C*, so it is not smooth. But e(C*)=0, and Proposition 4.1 gives

    e_st(Z)=0=e(Z).

Its unique closed G-orbit is {0} x C*, which is not projective. Thus Z is explicitly OUTSIDE the full Batyrev–Moreau conjecture. It falsifies the unrestricted literal dataset statement recovered for ID 30002003, as well as an overbroad reading of the abbreviated OWR prose; it does not refute Conjecture 6.7. Neither C nor Z is assumed complete, and Z has not been silently substituted for a projective example.

**Exact obstruction:** products propagate an already known inequality or erase information when a factor has Euler number zero. They do not provide a reduction of general spherical varieties to known factors. The zero-Euler construction cannot survive the required projective closed-orbit hypothesis in this form.

## Approach 5. A proper spherical degeneration and failure of invariant transport

A possible strategy would be to degenerate a spherical variety to a horospherical one and transfer the known criterion. Flatness alone is insufficient, even in a small explicit projective family.

### Proposition 5.1
In P^5 x A^1, with homogeneous coordinates [x1:x2:x3:x4:x5:z] and parameter t, define

    X_t: x1*x2+x3*x4+x5^2 = t*z^2.

This is a proper flat family of four-dimensional projective varieties. For t nonzero, X_t is a smooth quadric with e_st(X_t)=e(X_t)=6. For t=0, X_0 is a locally factorial spherical projective cone, singular at its vertex, with

    e(X_0)=5,    e_st(X_0)=16/3,    Delta(X_0)=1/3.

Proof. The family is closed in P^5 x A^1, so its projection is proper. Its graded coordinate algebra over C[t] is free as a module over C[t,x1,x2,x3,x4,z], with basis 1,x5, because the equation is monic of degree two in x5. Hence it is flat over C[t]. The standard affine charts, obtained by homogeneous localization and taking degree zero, remain flat; these cover the projective family.

When t is nonzero the six-variable quadratic form is nondegenerate, so X_t is smooth Q^4; the recurrence in Approach 4 gives e=6, and identity resolution gives e_st=6. The fibre at zero is the projective cone over Q^3. Away from its vertex it is a line bundle over Q^3, hence smooth and of Euler characteristic 4. The vertex chart z!=0 is exactly the affine factorial cone C from Approach 4. Thus X_0 is locally factorial and has e=4+1=5. Its resolution replaces the vertex by Q^3 with discrepancy 2, and its smooth complement contributes 4, so e_st=4+4/3=16/3.

For clarity these fibres are spherical under the same connected reductive group SO(5,C), acting on x1,...,x5 and fixing z. The special fibre has the dense nonzero-null-vector orbit on z!=0. For t!=0, that chart is the affine quadric q(x)=t, and a Borel has an open orbit. An explicit verification is available from a hyperbolic decomposition of the standard space: write q=2xy+q_W(w), dim W=3. The parabolic stabilizing the isotropic x-line has a unipotent subgroup acting, for v in W, by

    y -> y,
    w -> w+y*v,
    x -> x - B_W(w,v) - y*q_W(v)/2,

where q_W(w)=B_W(w,w). These transformations preserve q. They lie in the unipotent radical of that parabolic and hence in a Borel contained in the parabolic. On y!=0 choose v=-w/y to make w=0. A torus element scales y to 1, after which q=t uniquely determines x. Thus the Borel is transitive on the nonempty open chart y!=0 of q=t. The same calculation works on q=0, y!=0, proving its open orbit directly as well. Each projective fibre is therefore spherical. All its closed orbits are projective simply because the fibre is projective.

QED.

The three invariants e, e_st, and Delta all change in this family. In particular, neither flatness, properness, spherical symmetry, nor local factoriality of these fibres justifies replacing the stringy Euler number by that of the special fibre. This example is not a counterexample to the target: the singular special fibre has strictly positive deficit, exactly as the target predicts.

**Exact obstruction:** a degeneration proof needs a separate inequality or specialization theorem controlling the deficit, and needs strictness to reflect smoothness. None follows from flatness or the known horospherical theorem. The example disproves naive constancy, but not every possible one-sided specialization statement.

## Final mathematical status

The retained results prove the criterion in the toric subclass and in the explicitly hypothesized cone family, derive an exact orbitwise weighted-Euler reduction and a resolution upper bound, and exhibit rigorous controls for missing hypotheses and naive degeneration. The product control is a complete counterexample to the unrestricted literal dataset statement. None of these results proves the required general local inequality in the qualified spherical conjecture. The five approaches leave that conjecture unresolved. This is a source-statement correction and bounded investigation, not a solution paper for the qualified conjecture or a claim that the geometric observations are new.

## Public references

[OWR] Anne Moreau, joint with Victor Batyrev, “The arc space of horospherical varieties and motivic integration,” Oberwolfach Report 13/2012, pp. 766–767. https://ems.press/content/serial-article-files/46383 ; report DOI https://doi.org/10.4171/owr/2012/13

[BM] Victor Batyrev and Anne Moreau, “The arc space of horospherical varieties and motivic integration,” arXiv:1203.0671v2; Compositio Mathematica 149 (2013), 1327–1352. In particular Theorem 5.3 and Conjecture 6.7. https://arxiv.org/abs/1203.0671

[P] Boris Pasquier, “A survey on the singularities of spherical varieties,” arXiv:1510.03995v1. In particular Remark 3.5 and Section 5. https://arxiv.org/abs/1510.03995

[BG] Victor Batyrev and Giuliano Gagliardi, “On the algebraic stringy Euler number,” arXiv:1610.03842. In particular Theorem 1.8. https://arxiv.org/abs/1610.03842

[DD] Timothy De Deyn, “A note on affine cones over Grassmannians and their stringy E-functions,” arXiv:2203.06040v2; Proceedings of the American Mathematical Society 151 (2023), 2363–2373. In particular Proposition 3.1. https://arxiv.org/abs/2203.06040

[GHP] Giuliano Gagliardi, Johannes Hofscheier, Heath Pearson, “Toricness and smoothness criteria for spherical varieties,” arXiv:2601.06376v1, January 2026. Theorem 1.5 and the subsequent discussion distinguish the proved skeleton criterion from the conjectured stringy extension. https://arxiv.org/abs/2601.06376
