# A counterexample to the obstruction-length comparison

## Scope and status

This is a complete candidate proof of a **negative answer to the second question** in UnsolvedMath 30000971 (OWR-1971-004). It does **not** disprove or prove the first question, the uniform bound reg(Z) <= n/c+1. The original two-part target therefore remains unresolved. Independent review is required before promotion.

All fields below are algebraically closed of characteristic zero. Regularity of a finite projective scheme means the regularity of its ideal sheaf, not of its structure sheaf. All fibers are scheme-theoretic. A general projection means one in a nonempty Zariski-open subset of the space of centers.

The source is Beheshti--Eisenbud, *Fibers of Generic Projections*, arXiv:0806.1928v3, Conjecture 1.4 and the definition of Q on page 2. The first, weaker question is their Conjecture 1.3. The OWR 26/2008 contribution on printed pages 1440--1442 contains both questions. No priority or first-discovery claim is made.

## Theorem

Set X=v_2(P^40) in P^860. For a general linear projection

    pi: X -> P^46,

there is a fiber Z supported at one point, with local algebra

    A = k[z_1,z_2,z_3,z_4]/(z_1,z_2,z_3,z_4)^2.

For that fiber,

    reg(Z)=2,    length Q(X,Lambda)=10,    c=6.

Consequently reg(Z)=2 > 10/6=q(X,Lambda). In particular the comparison in the second question is false even under its characteristic-zero and general-projection hypotheses. The numerical bound of the first question is 40/6+1=23/3, and this example satisfies it.

More generally the same construction works for every integer e>=4, with

    g=e(e+1)/2,    n=e*g,    c=g-e=e(e-1)/2,
    X=v_2(P^n),    pi:X -> P^(n+c),

and produces a single-point square-zero fiber of length e+1 with

    reg(Z)=2,    length(Q)=g,    q=g/c=(e+1)/(e-1)<2.

The proof below establishes this family; e=4 gives the stated example.

## 1. Parameter space and local incidence

Put m=n+c and H=H^0(P^n,O(2)). Let S=H^(m+1), the affine space of ordered tuples s=(s_0,...,s_m) of quadratic sections. Restricting eventually to the dense open where these sections are independent and basepoint-free gives morphisms f_s:P^n -> P^m, precisely the ordered-coordinate versions of linear projections of the fixed quadratic Veronese embedding.

The basepoint-free open is nonempty: for a fixed point p, simultaneous vanishing of all m+1 sections imposes m+1 independent linear conditions. Its incidence with p therefore has dimension dim(S)+n-(m+1)<dim(S); the image is closed because P^n is proper. Independence is likewise a nonempty open because m+1<=dim(H).

On a source and target chart where s_0(p) is nonzero, write f_s=(s_1/s_0,...,s_m/s_0). Consider

    D={(s,p): rank(d f_s at p)=n-e}.

This is a locally closed incidence; finitely many charts suffice. Quadratic sections prescribe an arbitrary first jet at a fixed point. Hence, as s varies, the m-by-n derivative matrix is unrestricted. The rank-exactly-(n-e) determinantal stratum is smooth of codimension

    (n-(n-e))*(m-(n-e)) = e(c+e)=e*g=n.

Thus D is smooth of dimension dim(S) on each such rank chart. At (s,p), its normal space in the derivative-matrix direction is Hom(K,C), where K=ker(df_s) has dimension e and C=coker(df_s) has dimension g.

To show that D -> S actually dominates, the equality of dimensions is insufficient. We next give a point where this projection is etale.

## 2. An explicit transverse quadratic jet

Index a basis of Sym^2(k^e)^* by pairs alpha=(i,j), 1<=i<=j<=e. There are g pairs. Let

    E = {(alpha,b): alpha=(i,j), 1<=b<=e}
        minus {((a,a),a): 1<=a<=e}.

Then |E|=eg-e=n-e. Use affine coordinates z_1,...,z_e and w_(alpha,b) for (alpha,b) in E on A^n near p_0=[1:0:...:0]. Define the following homogeneous quadratic sections:

    s_0=x_0^2;
    s_(alpha,b)=x_0*w_(alpha,b),      for (alpha,b) in E;
    s_alpha=z_i*z_j + sum_{b:(alpha,b) in E} w_(alpha,b)*z_b,
                                  for alpha=(i,j).

The tuple has 1+(n-e)+g=m+1 entries. On x_0=1 the corresponding local map is (w,q), with q_alpha the displayed last g polynomials. At the origin its derivative has rank n-e, K is the z-space, and C is the q-space.

The derivative, in a source direction v, of the normal derivative-matrix is

    B(v)_(alpha,b) = Hess(q_alpha)(v,partial/partial z_b).

For the e excluded coordinates ((a,a),a), this is 2*v_(z_a). For every other coordinate (alpha,b), it is v_(w_(alpha,b)) plus a linear expression in v_z. Order the excluded coordinates first, the z variables first, and the remaining coordinates and w variables in the same order. The matrix of B is

    [ 2 I_e     0       ]
    [   D     I_(n-e)   ].

Its determinant is 2^e. In characteristic zero B is an isomorphism from the n-dimensional source tangent space to Hom(K,C).

The equations cutting out D have independent parameter derivatives by first-jet surjectivity. Their source derivative at this point is B. Therefore the differential of D -> S is an isomorphism. Since both D and S are smooth and have the same dimension, the projection is etale at (s,p_0). This proves dominance with a concrete transversality witness, not merely a parameter count.

The intrinsic second derivative Sym^2(K) -> C is also an isomorphism there: after setting w=0, the q_alpha are the complete basis z_i*z_j. This is an open condition on D. Shrink to an etale neighborhood contained in this open condition. Its image in S is nonempty and open, since etale maps are open. Thus for every parameter in a nonempty open subset of S there is at least one corank-e point with this nondegenerate quadratic part.

The displayed witness tuple need not be globally basepoint-free; it is used only for the incidence differential. This is harmless: its open image intersects the dense basepoint-free and independent locus, producing the asserted property for general morphisms. We make no claim that this special tuple itself is the required general projection.

## 3. Exact local fiber algebra

At any corank-e point in the preceding open incidence, choose n-e target coordinate functions whose differentials are independent. The formal implicit function theorem makes these part of a regular system of source parameters. Quotienting the fiber equations by them leaves a complete regular local ring

    B=k[[z_1,...,z_e]]

and g residual equations with no constant or linear terms. Their quadratic initial forms form a basis of m_B^2/m_B^3. Let J be the ideal they generate. Then

    J subset m_B^2,    J+m_B^3=m_B^2.

Apply Nakayama's lemma to the finitely generated B-module m_B^2/J. Since this module equals m_B times itself, it is zero. Hence **J=m_B^2 exactly**, and not merely to second order. The completed local fiber algebra is B/m_B^2. Because it is Artinian, completion has changed nothing. This is the desired square-zero local component of length e+1.

Every globally basepoint-free tuple in our parameter space gives a finite morphism: f_s^*O(1)=O(2) is ample, whereas on a positive-dimensional projective fiber its restriction would be trivial. A positive-dimensional fiber would contain a curve and give an immediate degree contradiction. Thus all its fibers are finite.

## 4. Excluding every other point of the same fiber

A local bad component alone would not refute the comparison, because other components add to length(Q). We now rule them out for a general parameter.

For distinct p,q in P^n, the map

    H^0(O(2)) -> J^1_p(O(2)) direct-sum O(2)|_q

is surjective. Indeed first jets at p are already arbitrary; choose a linear form L vanishing at p but not at q. Then L^2 has zero first jet at p and nonzero value at q, so it adjusts the value at q independently. This uses only one first jet and one value. It does **not** assert that two full first jets of quadrics are independent.

Consider triples (s,p,q) with p!=q, with f_s defined at both points, with rank(df_s at p)=n-e, and with f_s(p)=f_s(q). On a common target chart, the preceding surjectivity lets the derivative at p and the two values vary independently. Thus for fixed (p,q), the rank condition has codimension n and equality of values has codimension m. The incidence of such triples has dimension

    dim(S)+2n-(n+m) = dim(S)-c.

This is strictly less than dim(S). Its image is constructible, and its closure is a proper closed subset of S. Remove this closure. For every remaining parameter, no corank-e point shares its image with a distinct point.

Intersect this dense open with the nonempty open constructed in Section 2 and with the basepoint-free independent locus. For every parameter in the intersection, at least one corank-e point has the square-zero local fiber of Section 3, and there is no other point in that fiber. Therefore the entire scheme-theoretic fiber has algebra A=k[z_1,...,z_e]/m^2.

## 5. Passage from tuples to general linear projections

Let h=dim(H)=binomial(n+2,2). Independent tuples are frames of (m+1)-dimensional subspaces of H. They form a principal GL_(m+1)-bundle over the Grassmannian of those subspaces. Changing the frame postcomposes f_s by a projective automorphism, so the fiber property just proved is invariant under this action.

Take the union of all GL_(m+1)-translates of the nonempty open of good tuples. It is an invariant nonempty open, still consisting of good tuples. Its image in the Grassmannian is open (the frame-bundle projection is open). Duality identifies these subspaces with linear projection centers for v_2(P^n). The basepoint-free condition means that the center misses X. We have consequently proved the assertion for a genuinely general linear projection of the fixed smooth projective variety X.

## 6. Obstruction length, directly from the defining module

Write the entire fiber as Z=X intersect Lambda. Since Lambda has codimension m=n+c in the Veronese ambient projective space, its conormal restricted to Z is free of rank m. The source X is smooth of dimension n. In completed local source coordinates the fiber ideal is

    I=(w_1,...,w_(n-e))+(z_1,...,z_e)^2
       in R=k[[w_1,...,w_(n-e),z_1,...,z_e]].

The restriction map from the conormal of Lambda onto I/I^2 is surjective. Dualizing over A gives the injective left map in the defining exact sequence

    0 -> Hom_R(I/I^2,A) -> A^m -> Q(X,Lambda) -> 0.

Eliminating the regular w variables splits the conormal and gives

    dim Hom_R(I/I^2,A)
      = (n-e)(e+1) + dim Hom_(k[[z]])(m_z^2,A).

We calculate the last dimension without invoking a Hilbert-scheme smoothness assertion. There are g quadratic monomial generators z_i*z_j. An A-valued homomorphism assigns each such generator an element of A. For i!=j the relation

    z_i*(z_j^2) - z_j*(z_i*z_j)=0

forces the constant terms of both assigned images to vanish, since z_i and z_j are independent in m_A. These relations eliminate the constant term of every generator. Conversely, every relation among the minimal quadratic generators has all its coefficients in (z_1,...,z_e); hence any assignment of generator images to m_A satisfies all relations, because m_A^2=0. The image of each of the g generators can therefore be any of e independent linear elements. Thus

    dim Hom_(k[[z]])(m_z^2,A)=g*e.

It follows that

    length Q = m(e+1) - ((n-e)(e+1)+g*e)
             = (c+e)(e+1)-g*e
             = g.

Dividing by c=g-e yields q=(e+1)/(e-1). No free summand or contribution from a second support point is omitted.

## 7. Projective regularity

The fiber algebra has dimension e+1 and square-zero maximal ideal. Choose a projective affine chart containing its unique support point. The restrictions of ambient affine linear coordinates generate A, and consequently their centered versions span m_A/m_A^2=m_A. Together with the constant section, degree-one ambient sections therefore span all of A. For the Veronese embedding, choose original affine source coordinates t_i centered at the point; the ambient sections x_0^2 and x_0*t_i supply the constant and the classes spanning m_A. This does not require the formal coordinates from Section 3 to be ambient linear coordinates.

Thus the restriction map H^0(O_P^r(1)) -> H^0(O_Z(1)) is surjective; the degree-zero restriction has rank one and is not surjective because e+1>1. The usual ideal-sheaf sequence for a finite scheme then gives reg(Z)=2. Higher cohomology conditions are the elementary vanishing for O_P^r(t), and the only nontrivial regularity test is this interpolation degree. In particular this is the ideal-sheaf convention required in the conjecture.

For e>=4, (e+1)/(e-1)<2. This completes the candidate proof of the stronger comparison's failure. It supplies no counterexample to reg(Z)<=n/c+1.

## Verification boundary

As an independent consistency check, the square-zero algebra has derivation space of dimension e^2: every generator can map arbitrarily into its e-dimensional maximal ideal, and characteristic zero forces its constant term to vanish. The fixed-scheme bound of Beheshti--Eisenbud, arXiv:0911.3924v1, Theorem 1.1, therefore reads (e+1)+e^2/c<=n/c+1. Our parameters satisfy equality. The construction is thus at, rather than below, the dimensional threshold imposed by that later theorem.

The argument is a finite algebraic proof. The accompanying standard-library script checks the exact normal matrix, its failed nontransverse control, monomial-syzygy ranks, numerical Q formula, and regularity Hilbert values for e=2,...,6. These bounded computations are reproducible controls; they do not replace the algebraic openness, incidence dimension, Nakayama, or projective regularity arguments, and do not resolve the still-open first question.
