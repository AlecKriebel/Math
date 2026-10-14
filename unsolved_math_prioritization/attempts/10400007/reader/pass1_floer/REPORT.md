# Quantum braid Floer specialization and the missing intrinsic bridge

## Result and scope

The Anghel–Juhász v4 construction supplies a precise starting point, but the available Jones specialization establishes a scalar identity. It does not supply a knot-invariant specialized chain object or the intrinsic three-dimensional local-system assignment in the adopted contract. Two bounded obstructions and one exact simplification are established below:

1. Nontrivial Jones monodromy cannot extend across a filled diagonal or auxiliary puncture divisor.
2. Equality of specialized Euler classes does not imply equivalence of specialized complexes; the published grading variables are not a coefficient action on quantum braid Floer homology.
3. Inverting both variables of the actual two-variable Floer deformation removes all its weights by a diagonal change of basis and returns ordinary knot Floer homology. The apparent Jones degree becomes the Alexander degree after this change.

These are obstructions to specified repairs, not an impossibility theorem for Roberts's question. Categorification, arbitrary-manifold extension, and all higher homotopy coherence are not required by the original question. A sufficiently natural homological pairing could solve it without a new Floer theory.

## 1. Source version and normalization

The authority here is Cristina Anghel and András Juhász, *Quantum braid Floer homology*, [arXiv:2601.08805v4](https://arxiv.org/pdf/2601.08805v4), 7 September 2026. Its theorem statements, definitions, continuation argument, Rees deformation, and examples were inspected. This is not a complete analytic audit of all compactness and transversality claims. The January version is not used as current theorem authority.

For a braid beta in B_(n+1) whose closure is a knot K, v4 defines a finite F2-chain complex C_beta^q with triple gradings (A,Q,M), where Q denotes the quantum Alexander grading. Its differential lowers M by one and preserves A and Q. The graded Euler polynomial is

    Omega_beta^q(x,d) = sum_(a,q,m) (-1)^m dim H_(a,q,m)(C_beta^q) x^a d^q.

Theorem 1.13 and Corollary 8.20 give

    Omega_beta^q(x,1) = Delta_K(x),
    Omega_beta^q(x,-x^(-1)) = V_mirror(K)(x).

The mirror overbar was visually checked in the retained PDF. Thus the source-normalized V_K(t) is obtained, for example, by Omega_beta^q(t^(-1),-t), using V_mirror(K)(t^(-1))=V_K(t). This normalization correction alone has no effect on the descent issues.

## 2. Exact local-system data in the disc model

To avoid a variable-sign ambiguity, write e for the second variable of the disc polynomial Omega'_beta and d for the second variable of the Floer Euler polynomial. The relation is

    Omega_beta^q(x,d) = Omega'_beta(x,-d).

The underlying disc model uses

    D_n^q = D^2 minus {z_0,...,z_n,w_0,...,w_n,q_0,...,q_n},
    X_n = UConf_n(D_n^q),
    R = Z[x^(+/-1),e^(+/-1)].

For n>=2, its rank-one local system is specified by the character rho:pi_1(X_n)->R^units with the following monodromies:

- One particle circling z_i anticlockwise: x
- One particle circling w_i anticlockwise: x^(-1)
- One particle circling q_i anticlockwise: -e
- A positive elementary exchange of two particles: e

For n=1 there is no exchange generator. This is Definition 2.1, not an inferred character. The two Lagrangian supports are a product of open arcs, acted on by beta, and a product of circles. Monodromy along each circle is xx^(-1)=1; this supplies the lift/trivialization needed in the intersection formula. The intersection exponents also use specified anchor paths, and the normalized polynomial includes writhe and strand-number corrections. These support conditions and choices cannot be erased by calling the generators Heegaard generators.

The Jones specialization is e=x^(-1), giving monodromies

    (z_i,w_i,q_i,exchange) = (x,x^(-1),-x^(-1),x^(-1)).

The Alexander specialization is e=-1, giving

    (z_i,w_i,q_i,exchange) = (x,x^(-1),1,-1).

The exchange sign in the latter is part of the signed intersection conventions. It should not be confused with a trivial ordinary local system extending across the diagonal.

## 3. Bounded extension obstruction

### Lemma 3.1: filling a nontrivial meridian

Let j:X\D -> X include the complement of a smooth codimension-two divisor near one of its points. If a rank-one local system L on X\D is the restriction of a local system on X, the monodromy of L around a small meridian of D is 1.

Proof. The meridian bounds the transverse disc in X. Its image in pi_1(X) is trivial. Any character of pi_1(X) therefore sends that meridian to 1. The conclusion also holds for a general local system with identity in place of scalar 1.

### Application to the attempted Heegaard extension

Near a simple collision in UConf_n of a surface, the elementary exchange is a meridian of the discriminant in Sym^n of the surface: a transverse coordinate is the square of the difference of the two colliding local coordinates. Its Jones monodromy is x^(-1), which is not 1 over Z[x^(+/-1)]. Likewise, filling the divisor where one particle meets q_i would kill a loop with monodromy -x^(-1), again not 1. For n>=2 the diagonal obstruction is already enough; for n=1 the auxiliary puncture obstruction remains.

Therefore the literal specialized disc rank-one system does not extend over those filled divisors. This rules out a specific shortcut: identify intersection generators after surface surgery, fill the divisors, and declare the original local system to be an ordinary coefficient system on the full symmetric product. Generator matching does not construct such an extension.

This lemma does not rule out working on divisor complements, keeping divisor intersection variables, using constructible/perverse rather than locally constant coefficients, changing the ambient space, or using a genuinely different local system. Nor does it assert that the authors attempted the invalid extension: their Heegaard quantum grading is defined through domains and additional data, rather than by that declaration.

## 4. What the Heegaard grading remembers

The quantum diagram has the data (Sigma,alpha,beta,w,z,q,h,x0). For a domain D from x to y with n_w(D)=0, v4 defines

    Q(x)-Q(y) = n_Delta(D)-2 n_h(D)+n_q(D)+W(x)-W(y),
    W(x) = sum_(i: x_i=x_i^0) (3(n-i)+1),
    Q(x0) = n+writhe(beta).

The correction W is a function of the distinguished generator and the ordered handle/curve labeling. It is not itself the holonomy of a loop. It records the effect of changing the anchor paths in the disc-to-surface comparison. The proof of Theorem 1.12 transports the grading through matched domains and surgery; it does not exhibit the marked q,h,x0 and their weights as data determined by the undecorated knot pair.

Set P=Q-W. The filtration used to define C_beta^q is (P,-W). Theorem 8.16 supplies filtered continuation equivalences for different representatives of the same braid action and permitted almost-complex structures. Its isotopies are supported away from the protected marked/canonical data. It does not assert filtered equivalences under arbitrary Heegaard moves or under changing the braid by conjugation or stabilization. Theorem 8.22 gives a spectral sequence from qHFB(beta) to the associated graded of ordinary hat knot Floer homology for G=Q-2W. This does not transport the Jones grading to the limit.

## 5. The scalar quotient: exactly what is invariant

Section 9.2 gives examples, expressed there in e:

    Omega'_(sigma1) = x e^2 + x e - e,
    Omega'_(sigma1 sigma2) = x^2 e^4 + x^2 e^3 - x e^3 + x e - e.

The stabilization difference is x e^2(e+1)(xe-1); a conjugation difference is e(x-1)(e+1)(xe-1). Thus the polynomial quotient in the disc variable is by (e+1)(xe-1). In the Floer variable the corresponding quotient is

    Z[x^(+/-1),d^(+/-1)] / ((d-1)(xd+1)).

Keeping the unconverted ideal while switching from Omega' to Omega^q is a sign error.

There is a useful elementary description of this latter scalar ring. Evaluation at d=1 and d=-x^(-1) embeds it into

    Z[x^(+/-1)] x Z[x^(+/-1)],

with image the pairs (a(x),j(x)) satisfying a(-1)=j(-1). It is a fiber product, not the unrestricted product of the Alexander and Jones branches. Indeed, the two principal ideals have intersection equal to their product and their sum is (d-1,x+1); the standard pullback exact sequence proves the claim. An explicit interpolation for such a pair follows because j-a is divisible by x+1. This description is entirely scalar and supplies no chain comparison maps.

Most importantly, x and d in the displayed Euler polynomial are formal grading variables. The paper's qHFB is an F2-vector space with three gradings, not a supplied Z[x^(+/-1),d^(+/-1)]-module on which the ideal can act. One may coarsen its gradings to

    J=A-Q,    p=M+Q mod 2.

The existing differential is odd for p and preserves J, and its super Euler polynomial is V_mirror(K). Coarsening keeps the underlying vector space and differential. It cannot be assumed to remove braid dependence. Section 9.2 alone proves failure of the original triple-graded invariant, not failure of every conceivable coarsening. No stronger noninvariance conclusion is inferred solely from its Euler examples here.

Even for an actual R-complex C, equality of Euler characteristics after R->R/I is insufficient to prove a quasi-isomorphism after derived base change. A two-term complex R->R with zero differential has Euler class zero but remains nonzero after tensoring with any nonzero R/I. A repair by Verdier localization must specify the morphisms/cones to be inverted/killed and prove their behavior; equality in K0 cannot substitute for that data.

## 6. Actual chain-level repair attempt: the Rees deformation

Definition 8.26 introduces a genuine polynomial coefficient ring k[U,V], k=F2, with a complex whose differential counts all ordinary knot Floer discs and records two nonnegative quantities. Let

    s(x)=|{i:x_i=x_i^0}|,
    R0(x)=(W(x)-s(x))/3,
    B(x)=P(x)+R0(x),
    C(x)=R0(x)-W(x).

The symbol R0 here is a function, distinct from any coefficient ring. For any disc contributing to the differential,

    b(u)=B(x)-B(y)=n_Delta(u)-2n_h(u),
    c(u)=C(x)-C(y)=W(y)-W(x)-n_q(u),
    differential(x)=sum_(y,u) count(u) U^b(u) V^c(u) y.

Both exponents are nonnegative for the permitted almost-complex structures. Setting U=V=0 gives C_beta^q; setting U=V=1 gives the ordinary hat knot Floer complex. With deg_J U=-1 and deg_J V=1, the differential is J-homogeneous. Proposition 8.28 proves braid-representative independence of this coefficient complex.

### Proposition 6.1: invertible-weight trivialization

Let S=k[U^(+/-1),V^(+/-1)]. There is an S-linear chain isomorphism

    qCFB_plus(beta) tensor_(k[U,V]) S
        ~= CFKhat(H_beta) tensor_k S.

Proof. In the localized complex take the basis

    e_x=U^(-B(x)) V^(-C(x)) x.

Then

    differential(e_x)
      =sum count(u) U^(-B(x)+B(x)-B(y))
                       V^(-C(x)+C(x)-C(y)) y
      =sum count(u) e_y.

This is exactly the ordinary knot Floer differential. All basis factors are units. Localization is flat, so the same conclusion holds for derived localization: there are no hidden Tor terms to preserve the discarded refinement. The same calculation applies after any coefficient homomorphism for which the images of U and V are units.

The grading effect is equally explicit. Since B-C=P+W=Q,

    deg_J(e_x)=J(x)+B(x)-C(x)=A(x).

If one also extends the Jones parity p=M+Q to this deformation by assigning odd parity to both U and V, then e_x has parity M+Q-B-C=M modulo 2, since B-C=Q. Thus both the transformed degree and transformed parity are the ordinary Alexander/Maslov ones.

Thus the localized complex can be transported using ordinary knot Floer theory, but the recovered generator grading is Alexander. This is not a reconstruction of Jones from ordinary HFK. Also, the finite-dimensional super Euler formula of Section 5 cannot simply be applied to the resulting infinite-dimensional Laurent-coefficient complex: a grading-changing unit identifies shifts and changes the decategorification problem.

### Two natural homogeneous specializations also collapse

The relation UV=1, or U=t^(-1), V=t over k[t^(+/-1)], is compatible with the displayed Jones degrees but makes both weights units. Proposition 6.1 applies again. By contrast, specializations retaining a nonunit U or V can retain extra information, but no Markov equivalences for those complexes have been supplied here. This proposition does not rule them out.

### Trefoil calculation: visible information loss

The completely worked v4 trefoil example has five quantum generators with (A,Q,M)

    (-1,3,-2), (0,3,-1), (1,3,0), (2,3,1), (2,4,0).

Its quantum differential vanishes. The full knot Floer differential has precisely the arrow from a=(2,3,1) to b=(2,4,0). Here W(a)=0, W(b)=1 and n=1 gives R0=0, so

    B(a)=B(b)=3, C(a)=0, C(b)=-1,
    differential_plus(a)=V b.

Consequently this summand contributes k[U,V]/(V) before localization and disappears when V is inverted. The other three free generators survive. At U=V=0 the summand instead gives two generators. This is an exact concrete explanation of how the proposed invertible-weight repair loses the extra data.

The five quantum generators have Jones super Euler polynomial

    -x^(-4)+x^(-3)+x^(-1),

the left-handed trefoil Jones polynomial. The ordinary three-generator Alexander Euler polynomial is x^(-1)-1+x. The two polynomials are not interchangeable; the precise chain computation exhibits the distinction.

## 7. What would complete a genuinely intrinsic attempt

A possible next construction would start with a geometric space X(K), a character/local system L(K), and classes or Floer objects assigned to the oriented knot pair, and then show that a quantum or symplectic diagram computes its extraction. If instead one starts with a diagram-indexed system, the missing work is explicit:

1. For every allowed move, give a geometric map/correspondence and an identification of pulled-back coefficient systems. If working across divisors, specify relative coefficients/weights and admissible discs rather than invoking a nonexistent extension.
2. Supply chain maps, pairing-compatible maps, or maps of the actual chosen homology theory. For a chain-level route, identify grading shifts and show cones of move maps become acyclic under the precise specialization/localization being claimed.
3. Check the relations between move sequences at the level needed for the claim. An intrinsic homology object with diffeomorphism transport needs maps independent of representing a fixed isotopy/diffeomorphism; arbitrary different knot self-diffeomorphisms may legitimately act nontrivially. Do not demand that every loop of presentation moves act as the identity regardless of the ambient mapping class represented.
4. For a homotopy-category-valued object, suitable composition and homotopy coherence is enough. Full infinity-functor coherence is an additional output, not a hidden condition of Roberts's question.
5. Show that the spaces and local systems really come from the three-dimensional knot pair, or identify the diagram system with such an object. Merely adjoining all presentation names and declaring scalar-equivalent presentations equal repeats the original scalar construction.
6. Establish finite support or a justified torsion/pairing operation and recover the complete normalized polynomial. Handle mirrors, writhe, reduced/unreduced conventions, and the unknot before claiming equality.

The current v4 maps solve only the same-braid representative portion of this program. The weighted deformation does not automatically supply the other maps.

## 8. Related symplectic constructions: useful but distinct

Manolescu's [*Nilpotent slices, Hilbert schemes, and the Jones polynomial*](https://web.stanford.edu/~cm5/hs.pdf) gives geometric descriptions and generator correspondences for Seidel–Smith theory. Generator bijections alone do not identify differentials, coefficient systems, or knot-pair transport. Its historical remarks about conjectural gradings must not be presented as a current status statement.

LePage–Shende's [*Aganagic's invariant is Khovanov homology*](https://arxiv.org/pdf/2505.00327v1), Theorem 1.1, identifies the Coulomb-branch Fukaya–Seidel Hom pairing with both-graded Khovanov homology over Z. Section 5.2 provides real cover-induced gradings and divisor-weight coefficients. This is a substantive symplectic construction, not merely a polynomial formula. Remark 9.2 establishes the stated comparison at homology and chain-homotopy levels, while leaving a stronger higher-coherence comparison unchecked. That latter limit is not itself an obstruction under Roberts's wording. The relevant missing step for the adopted contract is an identified intrinsic three-dimensional local-system realization. This audit has not supplied one, and does not claim that their theorem is false or that no such realization can be developed.

## 9. Disposition

The attempt produces a precise continuation problem and two proved bounded obstructions. The all-weights-invertible repair is fully computed and returns the Alexander-side Floer theory. The scalar quotient and Jones regrading do not provide the missing naturality maps. Other nonunit or divisor-relative repairs remain unproved rather than disproved. No solution, impossibility theorem, or present-day openness/novelty certificate for the broad problem is claimed.
