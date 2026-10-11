# Reduced complex bi-Lagrangian smoothness: full proof reconstruction

Date: 2026-10-11. Problem: 2100502 / AMR-020-0502.

This AI-assisted, unrefereed prose edition presents one internal AI mathematical reconstruction of a prior candidate. It is not human peer review or formal proof-assistant certification, and is not a computational reproduction package. AUDIT.md records editorial checks of that same reconstruction; it is not a second independent mathematical audit. The prior candidate receives explicit credit; no novelty or priority is claimed.

## Decision and exact scope

**ACCEPT, with an explicit baseline-source correction, the candidate's reduced complex smoothness theorem.** No defect requiring a change to its complex theorem or its proof was found. The reconstruction below supplies the algebraic details that matter for reduction and fixed loci. It is a mathematical audit, not external peer review, proof-assistant verification, a priority determination, or acceptance of every statement in its cited sources.

For alternating forms A,B on a finite-dimensional complex vector space V, put r = max rank(sA+tB), and give

    X = { L in Gr(dim(V)-r/2,V) : A|L = B|L = 0 }

the reduced closed-variety structure. Then X is smooth if and only if every Jordan **pencil** block in its Jordan-Kronecker decomposition has dimension 2. Odd-dimensional Kronecker blocks are unrestricted. Equivalently, after removal of the core, a regular recursion operator is semisimple. If m_lambda counts the dimension-2 pencil blocks at lambda, then

    X is isomorphic to the product over lambda of LG(m_lambda,2m_lambda),
    dim X = sum over lambda of m_lambda(m_lambda+1)/2.

A dimension-2n pencil block has two length-n operator chains. These two uses of “block size” must not be confused. The zero-dimensional regular part gives the empty product, a point, including the zero pencil.

This resolves the smoothness component of Bolsinov-Matveev-Miranda-Tabachnikov, arXiv:1804.03737v2, Problem 5.3 (PDF page 25). The general Aut(V,pencil)-orbit classification in the same problem is **not resolved**. Neither the original incidence scheme's reducedness, a full singular-locus classification, nor an ambient mixed-block normal form is established here. The real assertions are recorded separately in Section 9 and are not silently substituted for the primary complex theorem.

## 1. Sources, status, and inspection

The candidate is Anonymous, *A sharp smoothness criterion for bi-Lagrangian Grassmannians*, version 0.2.0-candidate, 12 September 2026, in repository ipitchford/sharp-bilagrangian-smoothness at commit 855d8cc512b7cd51af437b6e033ec0e0ae8b32ed. Its paper is explicitly unrefereed and AI-assisted. Its DOI and its producer-coordinated reviewer reports do not establish mathematical correctness. No candidate-author executable was run. The verifier in this audit was newly authored for this audit.

The candidate PDF's complete seven pages and its complete preceding proof note were read; all seven PDF pages were also rendered and visually inspected. The candidate PDF's three main proof stages are on pages 2-4. Its real claims are on page 5, limitations and disclosures on page 6, and references on pages 6-7. Exact PDF identity: 83,801 bytes; SHA-256 119336971c32c10d2fab4ab6d441ea1f59d276b2872b69f5c0a1d77199f12577. Fresh GitHub commit metadata independently supplies its Git blob identity; the locally recomputed blob identity matches, as do the proof note and README identities.

The originating problem was checked in arXiv:1804.03737v2, dated 14 January 2020: PDF pages 1 and 23-25. Its vector space is complex and its alternating pencils are general, including Kronecker blocks. Problem 5.2 on page 24 concerns a different orbit problem; the bi-Lagrangian smoothness/orbit bundle is Problem 5.3 on page 25. The authors are Bolsinov, Matveev, Miranda and Tabachnikov. PDF identity: 474,906 bytes; SHA-256 7d9f90ceafa500086ab069ae2a66618bc76afbf1b019203c31abf4242c8bbd5c.

Kozlov, *Geometry of bi-Lagrangian Grassmannian*, arXiv:2409.09855v1, 15 September 2024, was checked on PDF pages 1, 4-5, 14, 16-22, 94 and 96. The full 103-page paper was not audited. Theorem 3.1 and Corollary 3.2 concern core reduction; Theorem 3.2 concerns the eigenvalue product. Problem 14.8 and Remark 14.4 (page 96) pose the smoothness issue and propose the dimension-2-block criterion. Its abstract claims complete orbit descriptions in three cases: one block, equal blocks, and two distinct blocks. It does not claim general orbit classification. PDF identity: 1,602,442 bytes; SHA-256 e8e3f31849dfe32e9ee7f67e50f8e365ed6bd0956aca54bf0e6fd12d2842d837.

The source identities and inspection history below refer to the original reconstruction. This editorial edition performs no new source inspection and distributes no copied source documents, images, source-author executable code, raw computational outputs, dataset contents, or private coordination material. Public bibliographic and byte-identity metadata are recorded in SOURCES.json.

Public links:
- Candidate at inspected commit: https://github.com/ipitchford/sharp-bilagrangian-smoothness/tree/855d8cc512b7cd51af437b6e033ec0e0ae8b32ed
- Candidate PDF: https://raw.githubusercontent.com/ipitchford/sharp-bilagrangian-smoothness/855d8cc512b7cd51af437b6e033ec0e0ae8b32ed/paper.pdf
- Original source: https://arxiv.org/abs/1804.03737v2
- Kozlov baseline: https://arxiv.org/abs/2409.09855v1

## 2. Dependency ledger

The universal proof uses the following classical mathematical facts. It does not use a classification of automorphism orbits or of affine-Schubert singularities.

1. Jordan-Kronecker decomposition of a complex alternating pencil (the originating source, Theorem 5.1, pages 23-24). This supplies the canonical orthogonal blocks and is an explicit external linear-algebra dependency, not reproved here.
2. Smith normal form for full-rank submodules of C[t]^2, polynomial division by a monic linear polynomial, Cayley-Hamilton, and elementary symplectic dimension bounds.
3. Reduced affine complex varieties are determined by their closed-point vanishing ideals; a morphism into affine or Grassmannian charts whose equations vanish at all closed points factors through the reduced closed variety. This is the elementary reduced Nullstellensatz usage, never a license to identify unreduced schemes.
4. The tangent-space and local-dimension criteria for nonsingularity, and additivity of both dimensions for products at complex closed points.
5. A smooth variety's completed local ring at a complex point is a formal power-series ring; regularity can be checked after completion. Section 7 proves the involution fixed-locus statement from this fact rather than importing a fixed-locus theorem without its hypotheses.

Ordinary Lagrangian Grassmannians are smooth: after choosing complementary Lagrangians, a transverse Lagrangian is a graph of a symmetric linear map, giving an affine chart of dimension m(m+1)/2. Such charts exist at every point. The Kronecker and spectral reductions are credited to Kozlov but are reconstructed below, so the proof does not inherit the erroneous assertion identified in Section 3.

The candidate's historical comparisons to Malkin-Ostrik-Vybornov and Pappas-Zhou are not dependencies. Their papers were not audited in this pass; no priority conclusion or extension of their results is asserted.

## 3. Required correction to an overstrong statement in the baseline

Kozlov v1 Lemma 3.3(1), PDF page 21, asserts an equivalence between simultaneous isotropy of an arbitrary subspace U and B-isotropy plus P-invariance. That equivalence is false for general U; Section 3.1 (pages 16-17) uses ordinary simultaneous isotropy and does not impose admissibility as part of that definition. The correct identity is

    A|U = 0  if and only if  P(U) is contained in U-perp_B,

when A(u,v)=B(Pu,v). The replacement of U-perp_B by U requires U to be Lagrangian (or another appropriate maximality hypothesis).

An explicit counterexample uses one dimension-4 block. In W=(C[t]/t^2)e direct-sum (C[t]/t^2)f, set P=t and B((p,q),(p',q'))=[t](pq'-qp'). Let U=C e. Both alternating forms vanish on the line U, but Pe=te does not belong to U. This also pinpoints the quantifier error in the printed proof: isotropy tests u in U, whereas the displayed proof uses u in U-perp_B.

The Lagrangian version (Lemma 3.3(2)) is correct, independently of that flawed derivation: for L=L-perp_B, A|L=0 is equivalent to P(L) contained in L. The candidate applies precisely this valid version and directly states its argument. Therefore this baseline error does not invalidate the accepted theorem. It does prevent blanket acceptance of the source's stronger lemma.

## 4. Core and eigenvalue reductions as algebraic isomorphisms

### 4.1 Dimension and kernels

For an alternating form C of rank 2q on a d-dimensional space, every isotropic subspace has dimension at most d-q. Indeed its image in V/ker(C), a symplectic 2q-space, has dimension at most q. Equality forces the subspace to contain ker(C), since dim ker(C)=d-2q. A simultaneous isotropic L of dimension d-r/2 therefore contains the kernel of every regular pencil member. Write K for their span.

For a canonical Kronecker block of dimension 2k+1, choose a k-dimensional half F and a (k+1)-dimensional half E, with the cross-pairing matrices of the two forms equal to [I_k 0] and [0 I_k]. Each nonzero pencil combination has cross-pairing rank k. Its kernel lies in E, and, for an affine pencil parameter lambda, has coordinates proportional to

    ((-lambda)^k, (-lambda)^(k-1), ..., -lambda, 1).

As lambda ranges over any cofinite subset of C these vectors span E, by the Vandermonde determinant. Restricting to parameters regular for the whole pencil removes only finitely many values. Because the kernel of a block diagonal form is the direct sum of its block kernels, no artificial correlation between different Kronecker blocks arises. Thus K is the direct sum of their E halves. This includes k=0.

For every regular pencil member E-perp equals E in each Kronecker block: E is isotropic, and the pairing of F with E has full rank k. The regular Jordan summands have zero kernels and are orthogonal to the Kronecker summands. Consequently the common orthogonal space of K is

    M = K direct-sum V_J.

Every L in X satisfies K contained in L contained in M. The restrictions of both forms to M kill K and descend to M/K, identified with V_J. The dimension identity is

    d-r/2 = dim K + (dim V_J)/2.

The usual Grassmannian isomorphism between the incidence locus K contained in L contained in M and Gr((dim V_J)/2,M/K) sends L to L/K; its inverse is the inverse image under M -> M/K. It is a genuine regular isomorphism and preserves the two isotropy conditions on closed points. Taking reduced closed subvarieties therefore gives X isomorphic to BLG(V_J). No claim about nilpotents in the initial incidence equations has entered.

### 4.2 Recursion and spectral decomposition

If V_J is zero, the result is already the point case. Otherwise choose tau such that omega=B+tau A is nondegenerate on V_J. Such tau exists because a regular determinant polynomial is not identically zero. Define P by A(u,v)=omega(Pu,v). Alternation implies omega(Pu,v)=omega(u,Pv), so P is omega-self-adjoint. Since B=omega-tau A, these two generators retain exactly the original isotropy conditions. For an omega-Lagrangian L,

    A|L=0 iff P(L) is contained in L-perp_omega=L.

Changing the two pencil generators amounts to a fractional-linear change of the eigenvalue parameter. On a Jordan primary summand an allowed fractional-linear function has nonzero derivative at its eigenvalue; if N is its nilpotent part, f(lambda+N)-f(lambda)=N times an invertible polynomial in N. Hence nilpotent chain lengths, including length one versus greater than one, are unchanged. Each original dimension-2n pencil block yields two length-n chains of P and a symplectic P-invariant summand.

For completeness, generalized eigenspaces V_lambda are mutually omega-orthogonal. If u is killed by (P-lambda)^a and v belongs to V_mu for mu different from lambda, the operator (P-lambda)^a is invertible on V_mu; write v=(P-lambda)^a w and move the polynomial across the pairing to obtain omega(u,v)=0. Each summand is symplectic by nondegeneracy of the total pairing. Chinese-remainder spectral projectors are polynomials in P, so a P-invariant L splits as the direct sum of its intersections L_lambda with V_lambda. Each intersection is isotropic, and its dimension is at most half the corresponding summand dimension. Equality of the total half-dimension forces equality separately.

Direct sum yields an algebraic map from the product of invariant-Lagrangian varieties in the primary summands. The inverse is given by the constant-rank images of the polynomial projectors on the universal subbundle; these define regular Grassmannian maps. They are inverse on reduced varieties. If all blocks have length one then P is scalar on each primary summand, so there is no further invariant-subspace condition. This proves the claimed product of ordinary Lagrangian Grassmannians and sufficiency.

## 5. A single block: the reduced quotient model

Let n >= 2, R=C[t]/(t^n), W=Re direct-sum Rf, and N=multiplication by t. Define

    omega((p,q),(p',q')) = coefficient of t^(n-1) in pq'-qp'.

This is nondegenerate since t^i e pairs with t^(n-1-i)f, and N is self-adjoint. It is a canonical regular block. Subtracting a scalar eigenvalue does not change invariant subspaces, so this model suffices for a single block.

If L is an N-invariant n-dimensional subspace of W, its inverse image Lambda in C[t]^2 is a submodule containing t^n C[t]^2 and of colength n. Smith normal form gives elementary divisors t^a,t^b with a+b=n. The determinant ideal of Lambda is therefore generated by t^n up to a unit. Every determinant of two vectors in Lambda is divisible by t^n; equivalently pq'-qp'=0 in R for vectors in L. This proves isotropy and hence the Lagrangian property.

Conversely a colength-n submodule supported at t=0 has exponents a,b >= 0 with sum n, so a,b <= n and it contains t^n C[t]^2. This proves equality of the relevant closed-point sets. The algebraic chart constructed next supplies actual regular inverse maps on the reduced varieties; no smoothness conclusion is drawn solely from this set equality.

## 6. The single-block chart and its actual reduced structure

Take L0=tRe direct-sum t^(n-1)Rf, of dimension n. In the Grassmannian quotient chart where the images of

    e, f, tf, ..., t^(n-2)f

are a basis of Q=W/L, a stable L induces multiplication T. In this ordered basis its columns are specified by

    T e = a e + sum(i=0,...,n-2) b_i T^i f,
    T^(n-1) f = c e + sum(i=0,...,n-2) d_i T^i f,

with the other columns the specified shifts. These 2n scalar coefficients are regular functions on the stable-subspace locus within the quotient chart. Put b(t)=sum b_i t^i and d(t)=sum d_i t^i.

### 6.1 Determinant identity for every n

The characteristic polynomial is

    det(t I - T) = (t-a)(t^(n-1)-d(t)) - c b(t).             (6.1)

One direct derivation writes the lower-right (n-1)-square block as tI-C_d, the companion matrix block of t^(n-1)-d(t). Its determinant is t^(n-1)-d(t). The last row of its adjugate equals (1,t,...,t^(n-2)): multiplication of this row by tI-C_d gives (0,...,0,t^(n-1)-d(t)). The block determinant expansion therefore gives (6.1), including the minus sign of c b(t). This is an all-n identity, independent of any finite tests.

At a point of X_n, T^n=0 and hence its characteristic polynomial is t^n. Conversely (6.1)=t^n implies T^n=0 by Cayley-Hamilton. The map R^2 -> Q that sends t^i e to T^i e and t^i f to T^i f is well-defined; it is surjective because the displayed basis is included among its columns. The kernel has dimension n and is N-invariant, hence Lagrangian by Section 5.

### 6.2 Elimination and integrality

The characteristic-polynomial condition is

    (t-a)(t^(n-1)-d(t)) = t^n + c b(t).

Divide the right-hand side by t-a. Its remainder is a^n+c b(a), and its monic quotient has degree n-1, so it uniquely determines every d_i as a polynomial in a,c,b_0,...,b_(n-2). Thus the equation is equivalent to one remainder equation. The triangular polynomial coordinate change

    z=b(a),     b_0=z-sum(i=1,...,n-2) b_i a^i

turns that equation into a^n+c z=0. The parameter space is

    S_n = Spec C[a,c,z,b_1,...,b_(n-2)]/(a^n+c z).

As a polynomial in z over the UFD C[a,c,b_1,...,b_(n-2)], its coefficients c and a^n are relatively prime. It is primitive and is irreducible over the fraction field, where it has degree one. Gauss's lemma proves irreducibility in the polynomial ring. The quotient is therefore a domain: reducedness of S_n is proved, not assumed.

### 6.3 Regular inverse maps, not a pointwise shortcut

The preceding matrix construction defines a polynomial quotient matrix F from W to Q on S_n. The n columns corresponding to e,f,tf,...,t^(n-2)f form the identity matrix. Consequently the kernel is a regular Grassmannian-valued map, explicitly represented in this chart by an identity block and minus the other columns of F. Its closed points are N-invariant Lagrangians by Section 5. Because S_n is reduced, all equations for that reduced subvariety vanish identically, and the map factors through X_n.

In the opposite direction, the universal quotient over the reduced stable-subspace locus has the fixed displayed frame, and N descends to its regular operator T. Its coefficients define the regular map to S_n. The characteristic-polynomial relations and the two compositions hold on all complex closed points; because both domains are reduced, these equalities hold as morphisms. We therefore obtain an isomorphism of reduced affine varieties

    U = X_n intersect the displayed quotient chart
      isomorphic to A^(n-2) times {a^n+c z=0}.             (6.2)

At L0 all these coordinates vanish. The local ring there has dimension n: it is a nonzero principal hypersurface in n+1 variables. The equation lies in the square of the maximal ideal, so its cotangent space has dimension n+1. Thus L0 is singular for every n>=2. In contrast n=1 gives the smooth projective line LG(1,2).

This calculation does not establish that the unreduced incidence scheme itself equals S_n. Over a nonreduced coefficient ring the implication T^n=0 -> characteristic polynomial t^n is not generally valid. All uses of that implication above are on complex closed points followed by an explicitly justified passage to reduced varieties.

## 7. Why other blocks cannot repair the obstruction

After core reduction isolate a dimension-2n block W with n>=2 and let W' be its symplectic orthogonal P-invariant complement. Let s be +1 on W and -1 on W'. It is a symplectic involution, commutes with P, and acts algebraically on X(P).

An s-fixed subspace splits under the projectors (1+s)/2 and (1-s)/2. Its two intersections are isotropic, and their dimensions are bounded above by half the dimensions of W and W'. Since the total dimension is the sum of these upper bounds, both bounds must be attained. The P-invariance condition then holds separately in the two factors. As in Section 4, direct sums and constant-rank projector images are inverse regular maps. Thus

    (fixed subscheme X(P)^s)_red
      isomorphic to X(P|W) times X(P|W').                 (7.1)

Products of reduced varieties over C are reduced, so there is no unacknowledged product reduction here. The second factor is nonempty: in each remaining canonical block choose one full chain half. The same convention makes a zero-dimensional complement a point.

At (L0,L') the first factor has tangent dimension n+1 and local dimension n. For the second, tangent dimension is at least local dimension. Both dimensions add for the product, giving strictly larger tangent dimension than local dimension at this pair. Hence (7.1) is singular.

Here is a scheme-level proof of the requisite fixed-locus fact. Suppose X were smooth at a fixed complex point x. The action of s on m_x/m_x^2 is diagonalizable with eigenvalues +/-1. Choose a basis, lift it to m_x, and average each lift with its image under s, using the matching sign. This gives an eigenvector regular system of parameters. The completed local ring is C[[u_1,...,u_p,v_1,...,v_q]], with s(u_i)=u_i and s(v_j)=-v_j. The completed fixed ideal generated by h-s(h) is precisely (v_1,...,v_q): every difference belongs to that ideal, and 2v_j is such a difference. Its quotient is C[[u_1,...,u_p]], regular and reduced. Therefore the fixed subscheme is smooth at x. Completion faithfully detects this property for these Noetherian local rings.

If X(P) were smooth, its fixed subscheme and reduction would therefore be smooth at every fixed point, contradicting (7.1). This proves necessity for arbitrary block mixtures, including multiple blocks with the same eigenvalue. It even shows that the ambient X(P) is singular at the displayed direct-sum points. It does not identify the ambient local singularity with (6.2).

## 8. Audit attacks and outcomes

- **Kronecker omission:** ruled out by the exact core reduction, including zero blocks and cofinite parameter sets.
- **Discarding a pencil generator:** ruled out by omega=B+tau A and B=omega-tau A.
- **Block versus chain confusion:** dimension 2n means two chains of length n; semisimplicity means n=1.
- **Set bijection mistaken for an isomorphism:** ruled out by ambient quotient Grassmannians, constant-rank projector maps, and the identity-minor kernel construction.
- **Unreduced nilpotence equations mistaken for a reduced chart:** ruled out by irreducibility of a^n+c z and reduced closed-point factorization, with no scheme claim.
- **Single-block singularity embedded in a smooth ambient variety:** an arbitrary singular subvariety would not suffice; the proof uses the entire reduced fixed locus of a finite-order action and proves its smoothness consequence.
- **Complement assumed smooth or eigenvalues assumed distinct:** neither is needed. Nonemptiness suffices; tangent excess survives any reduced complementary factor.
- **Baseline Lemma 3.3(1) imported uncritically:** rejected by the explicit line counterexample; only its correct Lagrangian specialization is used.
- **Finite symbolic checks substituted for a universal proof:** rejected. Sections 4-7 are the universal argument. The exact computations are supplementary regression checks.
- **Original bundle marked solved:** rejected. Only the smoothness component is accepted; the arbitrary-pencil orbit partition remains outside this packet.

## 9. Real claims: separate scope and hypotheses

The candidate's real discussion was read, and its mechanisms are consistent with the complex proof, but the primary acceptance and computational packet here concern the reduced complex theorem. In particular an algebraic variety smooth over R, its real-point set as an embedded C-infinity manifold, and an abstract topological smoothing are different assertions.

For the algebraic statement, if “the reduced real variety” means the reduction of the real incidence scheme, then base change to C is reduced because R is perfect; the reduction becomes precisely the complex variety. Smoothness ascends and descends along C/R. Thus the complex theorem gives the real algebraic criterion in terms of complexified chain lengths. This does not demand that nonreal-conjugate real blocks themselves have real dimension 2.

For the embedded-manifold argument, on a real primary component with eigenvalues alpha+/-i beta, the semisimple part S is a real polynomial in P. The operator J=(S-alpha I)/beta is self-adjoint, has J^2=-I, and makes Omega(u,v)=omega(u,v)-i omega(Ju,v) complex bilinear and nondegenerate. Invariant L are J-stable, and their real isotropy is equivalent to Omega-isotropy. This explains why the conjugate-pair component is the underlying real space of a complex invariant-Lagrangian variety. A separate full real-form canonical-decomposition audit was not undertaken here.

The candidate's geometric-cone calculation has the required distinction from the Zariski tangent space. For n=2 the secant cone of a^2+c z=0 at zero is that nonlinear quadratic cone. For n>2, rescaling the equation shows that every tangent direction satisfies c z=0. Directions with c nonzero are attained using a=epsilon A, c=epsilon C and z=-(epsilon A)^n/(epsilon C); the reversed choice handles z nonzero, and closure handles the intersection. Thus the cone is the union of two planes. The argument works for real coefficients and for complex coefficients viewed as a real space. A product with any nonempty remaining real factor has a tangent cone whose projection is exactly this nonlinear cone, by keeping the other coordinate fixed. Since a linear space has a linear projection, that product cannot be an embedded smooth manifold at the chosen point. The fixed-set theorem for a smooth real involution then gives the same type of contradiction, under the real decomposition just described.

These observations support the stated real mechanisms, but they are deliberately not a claim that this audit has reproduced every real normal-form or real-algebraic convention in the baseline. No inference of embedded real smoothness is made merely from a complex Zariski tangent-space excess.

## 10. Verification and publication boundaries

The original reconstruction used a newly authored exact verifier for n=2,...,9, with five quotient-kernel reconstructions at each n (40 total), seven Kronecker sizes k=0,...,6, singular-point fingerprints, and the arbitrary-isotropy counterexample. Its normal, -O and -OO runs passed; the original control suite executed 11 integrity mutations and eight semantic mutations in each mode. Semantic controls reached the mathematical checker directly. These finite computations are supplementary regression evidence. The universal proof is Sections 4-7, not an extrapolation from those computations.

The original audit inventory and its separately pinned external seal authenticate the retained evidence. The present edition retains the entire mathematical argument and separately binds the eight distributed files by sizes and SHA-256 values. Those identity checks protect recorded bytes and do not prove the theorem. The private preparation checks the exact editorial transformations, strict additions-only patch, native Git identities, and unchanged repository siblings and queue. No executable code or raw outputs are distributed in this prose edition.

This edition is AI-assisted and unrefereed. It records one internal AI mathematical reconstruction, not human peer review or formal proof-assistant certification. The accompanying editorial AUDIT.md does not constitute a second independent mathematical audit. This is not a computational reproduction package. No novelty, priority, general orbit classification, full singular-locus classification, mixed-block ambient normal form, or reducedness of the original incidence scheme is claimed. Section 9 remains a separately bounded discussion of real mechanisms, not the primary full acceptance. No remote mutation was performed during preparation.
