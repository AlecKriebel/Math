# Closed exotic four-manifolds and skein lasagna modules

## Result and exact question

This is an unresolved investigation of catalogue 2942 / KP-4.66, rank 694. Five distinct approaches were carried out. No closed exotic pair distinguished by a skein lasagna module is constructed, and no universal impossibility theorem is proved. The results below are scoped deductions, reductions, and algebraic countercontrols. They are not claimed to be new.

The controlling question is Problem 4.66 on pages 243–244 of the 436-page 2026 preliminary K3 problem book: “Can the skein lasagna module detect exotic smooth structures on closed 4-manifolds?” This numbering is not interchangeable with the 1997 Kirby list. The exact current dataset statement has SHA-256 338652cf78df7a4f0b2d8e1f02a9c04e0e6fcc16f35aae1cfd9fffd35ecc3d57 and agrees with the primary question.

We examine the ordinary Khovanov–Rozansky gl_2 skein lasagna module

    S(X) = S^2_0(X; empty link; Q).

Here X is smooth, compact, connected, and oriented, and is closed when it is a target for the question. The module carries homological and quantum gradings and a grading by H_2(X; Z). A diffeomorphism transports the latter grading by its induced homology map. An exotic oriented pair means orientation-preservingly homeomorphic but not orientation-preservingly diffeomorphic. A result for this rational gl_2 theory does not settle the question for all coefficients, all N, deformations, or other input theories. Neither simple connectivity nor any relative boundary marking is imposed by the literal question; those are additional hypotheses only where stated below.

Write CPbar^2 for the complex projective plane with its orientation reversed. CP^2 and CPbar^2 must never be conflated. The catalogue background loses an overbar; the visually checked K3 page does not. With these conventions S(CP^2)=0 and S(CPbar^2) is nonzero. The examples distinguished in Ren–Willis have nonempty boundary. Detecting an exotic surface in a fixed manifold is also a different problem from detecting the smooth structure of a closed ambient manifold.

## Imported results and proof boundaries

The following are credited inputs, not theorems established by the finite checker accompanying this report.

1. Manolescu–Neithalath, Proposition 2.1 and Proposition 1.6: adding a 3-handle gives a surjection on skein lasagna modules; adding a 4-handle gives an isomorphism. Thus removing a small open 4-ball preserves S. Their Theorem 1.4 and Corollary 7.3 give the tensor-product formula for connected sums over a field.
2. Ren–Willis, arXiv:2402.10452v3, Theorem 1.4: if an oriented X contains the knot trace X_n(K) with n >= -TB(-K), then the ordinary gl_2 module vanishes, for every permitted boundary link. Example 3.2 specializes this to a smoothly embedded sphere of positive square. This is Theorem 1.4 in v3, not the older numbering copied into the K3 remark.
3. Ren–Willis, Theorem 4.1: forgetting the integer quantum filtration, the rational Lee skein lasagna module has a basis x_(a,b) indexed by pairs a,b in H_2(X; Z) when the boundary link is empty. Its homological degree is -2a.b and its homology degree is a+b. The quantum mod-4 homogeneous symmetric/antisymmetric combinations have degrees determined by the intersection form. The integer filtration may take value minus infinity on nonzero vectors.
4. Ren–Willis, Theorem 1.11: for a 2-handlebody, the dimension of each associated-graded Lee piece bounds the corresponding rational Khovanov piece from below. The statement does not assert a spectral sequence of lasagna modules and is not an unrestricted closed-manifold comparison theorem.
5. Ren–Willis, Proposition 1.14 and its proof: S(CPbar^2) is nonzero; Section 6.12 explicitly describes the conditional positive-b_2^+ route developed below.
6. Ren–Sullivan–Wedrich–Willis–Zhang, arXiv:2510.05273v1, Theorem 7.1 and Corollary 7.2: a Gluck twist about an interior embedded sphere with trivial normal bundle induces a rational ordinary-module isomorphism. In a fixed homology class a the displayed bidegree shift is (minus/plus (a.[S])^2/2, plus/minus (a.[S])^2/2), in the source's conventions. In particular a null-homologous sphere gives an isomorphism preserving the gradings. The general case must not be advertised as an unchanged grading identification.
7. The standard classification of odd indefinite unimodular integral forms, and Freedman's classification of closed simply connected topological 4-manifolds by intersection form and Kirby–Siebenmann invariant. Smooth manifolds have zero Kirby–Siebenmann invariant. Freedman's original Theorem 1.5 was inspected in its smooth/almost-smooth applicable regime; its deep proof is not reproduced here.

Relevant theorem statements and selected proof passages were inspected. This does not amount to a complete audit of their upstream foundations. Ren–Willis is accepted/to appear in Annals of Mathematics, accepted June 24, 2026, according to the journal. The journal records a June 18, 2026 revision, whereas the inspected arXiv body is v3 of December 18, 2025. No byte equality or full-text comparison to the later accepted manuscript is claimed.

## Approach 1: closing the known boundary examples

### Proposition 1: puncturing is harmless, arbitrary caps are not

For a closed smooth oriented X and a small smoothly embedded ball B,

    S(X minus int(B)) is isomorphic to S(X).

Consequently a genuinely computed difference of modules of punctured closed manifolds gives the same difference after filling the spherical boundary. However, a difference for arbitrary compact manifolds with boundary does not by itself give a closed-manifold difference.

Proof. The first statement is imported result 1: filling that S^3 boundary is a 4-handle attachment. An arbitrary boundary is not asserted to be S^3. Attaching the additional handles needed for a general closure is a different operation; even the known 3-handle maps are only surjective. Distinct source vector spaces may have identical quotients: projection onto the first coordinate maps both Q^2 and Q^3 onto Q. Thus the information that the inputs differ and the maps are onto logically does not establish different outputs. This is an algebraic counterexample to an inference, not a pair of manifolds. QED.

For a more faithful model of general gluing, take A=Q e direct-sum Q f with orthogonal idempotents e,f and identity e+f. An A-module is a pair of vector spaces, one in each idempotent sector. If M=(Q,0), N=(Q,Q), and the cap module C=(Q,0), then M and N differ but

    M tensor_A C = Q = N tensor_A C.

Indeed all cross-sector tensors vanish because e f=0, leaving just the sectorwise tensor products. Therefore even an exact tensor/coend gluing formula is not automatically a faithful detector of module differences. Blackwell–Krushkal–Luo's cornered theory supplies gluing formulas, not the faithfulness needed to circumvent this issue.

### Proposition 2: a sufficient survival and comparison certificate

Let p_i: V_i -> W_i be the maps on modules from two specified capping constructions. Suppose the maps are surjective and preserve a chosen common grading (including any explicitly specified transport of homology). A linear functional lambda on a source graded component descends to the corresponding quotient if and only if it annihilates ker(p_i). If lambda(v) is nonzero, its descended functional proves p_i(v) is nonzero.

Proof. Necessity follows because lambda=bar(lambda) composed with p_i. Conversely define bar(lambda)(p_i(v))=lambda(v); annihilation of the kernel gives independence of the representative. The nonvanishing conclusion follows at once. QED.

This supplies a concrete capping goal: construct a nonzero functional compatible with all cap relations. It is not supplied merely by a nonzero boundary class. To prove an unmarked oriented exotic pair by graded dimensions, one must moreover exclude every possible intersection-form isometry induced by a candidate diffeomorphism, not only a chosen marking. In particular, if for every such isometry phi there is some (h,q,a) for which the two corresponding graded dimensions differ, an orientation-preserving diffeomorphism is impossible. This follows from functoriality. If H_2 changes under the cap, source homology degrees must first be grouped by their images; assuming automatically that the degree map is injective is invalid.

Outcome. The known trace examples cannot be promoted to closed examples by the 4-handle theorem alone. No surviving cap functional or complete cap calculation was constructed.

## Approach 2: nonvanishing and the positive-sphere obstruction

### Proposition 3: a smooth positive sphere forces vanishing

If X contains a smoothly embedded oriented sphere of square n>0, then S(X)=0. Consequently S(X) nonzero forbids all such smooth spheres. Also

    S(X # CP^2)=0,
    S(X # (S^2 x S^2))=0.

Proof. A tubular neighborhood of the sphere is the disk bundle of Euler number n, equivalently the n-trace of the unknot. The unknot has TB=-1, so n>=1 is precisely within imported result 2. The line in CP^2 has square +1. The diagonal in S^2 x S^2 has square +2. Choose the connected-sum balls away from these spheres; they remain smoothly embedded in the sums. QED.

The condition is geometric and orientation-sensitive. A positive vector in the intersection lattice does not provide a smooth sphere. A topologically locally flat sphere is not enough for the imported smooth theorem. Reversing orientation changes the sign of the square. In particular the conclusion is not that every X with b_2^+(X)>0 has zero module.

### Proposition 4: a conditional route to closed detection

If a closed simply connected smooth oriented X satisfies b_2^+(X)=p>0 and S(X) is nonzero, then the oriented pair

    Y = X # CPbar^2,
    Z = (#^p CP^2) # (#^(b_2^-(X)+1) CPbar^2)

is homeomorphic and has different rational ordinary skein lasagna modules. This would answer the question affirmatively in the oriented category.

Proof. The intersection form of Y is Q_X direct-sum <-1>. It is unimodular, odd, and indefinite, with positive index p and negative index b_2^-(X)+1. The integral odd-indefinite classification identifies it with the diagonal form of Z. Both manifolds are smooth and simply connected, so their Kirby–Siebenmann invariants agree and vanish. Freedman's classification gives an orientation-preserving homeomorphism. The tensor formula gives

    S(Y) = S(X) tensor_Q S(CPbar^2),

which is nonzero: choose nonzero vectors in both factors and linear functionals taking them to 1; the product functional proves their tensor is nonzero. Meanwhile Z contains a +1 sphere from a positive projective-plane summand, so Proposition 3 gives S(Z)=0. Diffeomorphism invariance excludes an orientation-preserving diffeomorphism. QED.

This is a reconstruction of the route already stated in Ren–Willis Section 6.12, not a new theorem. Orientation-free non-diffeomorphism needs an additional check, which can be arranged conditionally here. Replace the single negative blowup by r negative blowups, where r=1 unless signature(X)=1, in which case take r=2. The same argument works because tensoring with r copies of the nonzero S(CPbar^2) remains nonzero; the forms remain odd and indefinite. Both resulting manifolds have the same nonzero signature signature(X)-r. An orientation-reversing diffeomorphism would negate that signature, an impossibility. Thus this slightly adjusted conditional construction would also produce an unoriented exotic pair. It still requires the missing nonvanishing X.

Outcome. No suitable X with p>0 and a rigorously nonzero module was found. Neither the existence of a positive lattice vector nor a nonzero module for a Stein subdomain fills this gap.

## Approach 3: the Lee deformation and filtration

### Proposition 5: the unfiltered Lee module cannot distinguish an oriented homeomorphic pair

Under the structure theorem in imported result 3, an orientation-preserving homeomorphism f:X->X' induces an isomorphism of the unfiltered Lee modules, preserving their homological, homology-class, and quantum mod-4 gradings. It need not preserve the integer quantum filtration.

Proof. On canonical basis vectors set x_(a,b) -> x_(f_*a,f_*b). This is a bijection of bases. The map f_* preserves intersection products and addition. Hence -2a.b and a+b are transported correctly. On an unordered pair {a,b}, the symmetric and antisymmetric combinations have quantum mod-4 degrees determined by -(a+b)^2 and the fixed empty-link correction; these degrees are preserved as well. When a=b the antisymmetric combination is zero and the surviving symmetric vector is handled by the same formula. This establishes all the stated unfiltered gradings. Nothing in the construction establishes equality of integer filtration values. QED.

The Lee vector space can be nonzero while every associated-graded piece is zero. As an algebraic example, set F_q V=V for every integer q on a nonzero vector space. Then every nonzero vector has filtration degree minus infinity and F_q V/F_(q-1)V=0. Thus the existence of canonical Lee generators alone does not prove nonvanishing of ordinary Khovanov lasagna modules.

### Proposition 6: a sufficient filtered two-handlebody test

Let W be a 2-handlebody with boundary S^3, and let X be obtained by adding a 4-handle. If a nonzero vector of the Lee module of W has finite integer filtration degree, then S(X) is nonzero.

Proof. A vector of degree q in the convention of the source lies in F_q but not F_(q-1), so its class in the associated graded is nonzero. Imported result 4 gives a nonzero ordinary rational Khovanov component for W. Imported result 1 transfers it to X. QED.

If W must first receive 3-handles, nonvanishing before those handles is insufficient without a survival argument. The comparison theorem's two-handlebody hypothesis is essential to this application. A bound in the form s(X;a)<=c is also insufficient: minus infinity satisfies it. A finite lower bound plus a finite representative bound would be sufficient.

Outcome. The easy unfiltered computation loses the desired information. No finite-filtration certificate for a closed positive-b_2^+ candidate, or for a suitable punctured candidate with only a 4-handle remaining, was established.

## Approach 4: cabled computations and directed limits

The 2-handlebody formula over Q uses cable homology, symmetry invariants/coinvariants, shifts, and dotted-annulus transition maps. Ren–Willis Proposition 2.10 and the proof of Theorem 1.11 express this as a filtered colimit; the diagonal indices (n,...,n) form a cofinal sequence. Thus the following elementary statements expose the certification issue independently of the knot calculations.

### Proposition 7: the exact survival criterion

For a sequence V_0 -> V_1 -> ... of vector spaces with transition composites f_(i,j), the image of v in V_i in the direct limit is zero if and only if f_(i,j)(v)=0 for some j>=i. For a fixed finite-dimensional V_i, the kernel K_i of its map to the direct limit equals the increasing union of ker(f_(i,j)); this union equals one finite-stage kernel, but there need not be an effective bound on the stage from a computed prefix alone.

Proof. In the standard construction of a directed limit, two representatives are equal exactly when they become equal at a common later index. Taking one representative to be zero proves the first assertion. The kernels increase because f_(i,k)=f_(j,k) f_(i,j). Their union is K_i. In a finite-dimensional vector space a strictly increasing chain can grow only finitely many times; alternatively choose a finite basis of the union and a common stage killing all its elements. A finite stage therefore realizes the union. This argument supplies no bound on when the last strict increase occurs. QED.

### Proposition 8: no finite prefix alone certifies the limit

For every integer N>=0, two sequences can agree through every vector space and transition map with indices at most N, have every stage one-dimensional, and nevertheless have respective direct limits Q and zero.

Proof. Take V_i=Q at all stages and all visible maps to be the identity. In the first extension use identity maps forever. In the second use the zero map V_N->V_(N+1) and zero maps thereafter. The first limit is Q; every representative in the second eventually maps to zero, so its limit is zero by Proposition 7. QED.

A genuine algebraic certificate is a compatible nonzero functional: if lambda_j f_(i,j)=lambda_i for all j>=i and lambda_i(v) is nonzero, then v survives. Otherwise a later zero image would contradict that equality. Constructing the compatible family requires control over the full tail, not a finite list of successful tests.

Outcome. Finite cabling computations may suggest a candidate, but were not promoted to an infinite-limit nonvanishing theorem. No cable complex for an uncomputed closed candidate was claimed to be computed by the checker.

## Approach 5: stabilization and Gluck-twist candidates

### Proposition 9: S^2 x S^2 stabilization erases this invariant

Every once-stabilized X#(S^2 x S^2) has zero ordinary rational module. Therefore equality of modules after this stabilization cannot justify cancellation of the stabilization factor or equality before it.

Proof. Proposition 3 already gives vanishing. Equivalently, the tensor formula tensors S(X) with zero. The algebraic operation V -> V tensor 0 is constant and cannot be cancelled: Q tensor 0 = Q^2 tensor 0. QED.

Even tensoring with a nonzero infinite-dimensional ungraded vector space does not always permit cancellation up to isomorphism. If W has basis indexed by nonnegative integers, then Q tensor W and Q^2 tensor W are isomorphic via (epsilon,n)->2n+epsilon. Grading bounds and finiteness must therefore be proved before using a Hilbert-series cancellation argument. Ren–Willis Proposition 6.17 makes its more specific CPbar-stable homotopy-sphere claim using Proposition 6.16's extra graded finiteness; we do not replace that hypothesis by bare nonvanishing.

### Proposition 10: the null-homologous Gluck route is blind over Q

Let S be an interior smoothly embedded sphere with trivial normal bundle and zero integral homology class in a compact oriented X. The ordinary rational skein lasagna modules of X and its Gluck twist are isomorphic as graded objects. In particular, a Gluck twist on a sphere in S^4 has the same ordinary rational module as S^4.

Proof. Imported result 6 supplies inverse isomorphisms. Since [S]=0, a.[S]=0 for every a, so the specified degree shifts vanish; use Corollary 7.2 for the homology-degree identification. For S^4 every sphere is null-homologous, and the 4-handle/ball calculation gives S(S^4)=Q. QED.

This is a credited exclusion of a proposed search route, not a proof that a Gluck twist yields an exotic sphere, nor an integral-coefficient or all-N obstruction. In the general non-null-homologous case the shifts must be retained. The one-dimensional-input variant introduced in the same paper is not silently identified with the ordinary module.

Outcome. Stabilization and the null-homologous Gluck class do not supply a closed detector. Their failure does not answer the existential question negatively.

## What remains

A positive answer still needs an actual closed homeomorphic pair and a complete smooth-invariant comparison, or a closed positive-b_2^+ nonvanishing example to feed Proposition 4. A negative answer requires a theorem covering every closed candidate in the intended coefficient/input theory; none is supplied. No cap kernel, infinite cable tail, or complete closed-manifold lasagna module was computed here. The finite exact controls check the elementary algebra and sign/degree safeguards only. The disposition is unsolved after five approaches, not solved in literature and not a new discovery.
