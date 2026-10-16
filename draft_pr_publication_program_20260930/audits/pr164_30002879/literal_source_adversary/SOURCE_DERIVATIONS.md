# Independent source and coefficient-map derivations

This is the auditor's own derivation, with source locators only. Third-party PDFs, text extraction, headers, and rendered pages remain in `private/`. No original verification code, previous review, README, research log, or other audit-family verdict was read.

## 1. Exact target and module

The target is the upper triangular algebra with the lower-right idempotent specified in OWR 24/2015, Hermann Question 5, printed 1363 (PDF page 47). The scalar field is any field of characteristic two. The displayed group module requires an action, not just a two-dimensional vector space. Use the permutation action specified by the two arrows in Hermann v2 9.6 (PDF page 45), and independently in Xu v2 3.1 (PDF pages 15-16): g swaps alpha and beta, while h fixes both.

Set x=g+1 and y=h+1. On the two-dimensional module, x has square zero and rank one, and y acts as zero. The map A/(y) -> M taking 1 to alpha and x to alpha+beta is bijective and intertwines A-actions (after the opposite correction in Section 2). This proves M=A/(y), with its scalar right K-action. The two vectors alpha and alpha+beta are independent over every characteristic-two field. Any other nonzero homomorphism (Z/2)^2 -> Z/2 is obtained by changing the two group generators, so the quotient choice changes coordinates, not the isomorphism class of this one-point extension.

A two-dimensional trivial module is a different algebra. In that case every radical element of A annihilates M. The upper triangular center consists of (a,c) with augmentation(a)=c and has dimension four. For M=A/(y), the center condition is a mod y=c, with center dimension three. The negative control therefore detects the wrong module already in degree zero.

## 2. Exact orientation, rather than an unspecified convention

Hermann v2 9.6 explicitly fixes multiplication to be categorical composition f composed with g. Its arrows go from X to Y, its group acts at X, and Y has only its identity. Consequently, with idempotents ordered X,Y, the category algebra is

C = [[A,0],[N,K]],

where N is a right A-module. Taking the opposite yields

C^op = [[A^op,N],[0,K]] = [[A,M],[0,K]] = B,

since A is commutative and the right permutation action becomes the left action just proved. This is a required opposite, not merely a convention left unspecified in the source. Under the source's fixed multiplication, the literal same-orientation assertion in Lemma 9.7 cannot be true: the dimensions of the indecomposable right projectives of C are 4 and 3, whereas those of B are 6 and 1. Their multisets differ, so the algebras are not isomorphic.

An explicit basis map C^op -> B is

id_X -> f, g -> f+x, h -> f+y, gh -> f+x+y+xy,
id_Y -> e, alpha -> m_0, beta -> m_0+m_1,

where x m_0=m_1 and x m_1=y m_0=y m_1=0. The independent checker verifies all 49 products. It also verifies associativity of the three algebras involved, and the projective-dimension and wrong-module controls. Ordinary and optimized Python use explicit exceptions; optimization cannot remove checks.

Opposite-algebra cochain comparisons use reversal and integer sign factors. Every such sign is one in characteristic two. Hence opposite passage preserves the bracket after the characteristic-two specialization. The manuscript computes B directly, so no source-based opposite comparison is actually needed for its formula. The source's action supplies the intended module, not an uncorrected algebra isomorphism.

## 3. All hypotheses of the source machinery

For the manuscript's B, eBe=K, Be has underlying column (M,K), and eB is the one-dimensional row (0,K). Multiplication identifies Be tensor_K eB with

I=BeB=[[0,M],[0,K]].

This map is an isomorphism on the displayed three-dimensional vector spaces: m tensor 1 goes to m in the upper right, and c tensor 1 goes to c in the lower right. All higher Tor over the field K vanish. Thus e is stratifying. The quotient B/I is A, the quotient q is a K-linear surjection, and B and A are finite-dimensional K-vector spaces, hence K-projective. These establish every hypothesis used from OWR 3.2, Theorem 3, and Lemma 4 (printed 1362-1363).

For Happel's sequence, Hermann v2 Proposition 6.12 (PDF page 31) requires R and M to be K-projective; take R=A and M=A/(y). Both requirements hold over any field. M is not projective as an A-module, and no such stronger condition is used. For the characteristic-map identification, Hermann Lemma 6.9(3) (PDF page 29 and proof continuation through page 31) uses the right K-projectivity needed to tensor the A-bimodule resolution; this also holds. The K component in degree zero is signed negatively in general. In characteristic two subtraction equals addition; retaining the expression a mod y - c still fixes the conventional normalization.

Proposition 6.12 asserts strict Gerstenhaber compatibility of g, but only graded-algebra compatibility of the characteristic map h. The manuscript does not need h to preserve a Lie bracket and does not claim it does. The degree-zero K summand cannot be dropped from the start of Happel's sequence, although it disappears in positive degrees.

## 4. Independent all-degree normalization and image

For D=K[t]/(t^2), the bimodule differential is multiplication by t_L+t_R. In D^e this operator has image and kernel both spanned by t_L+t_R and t_L t_R; its square is zero. Tensoring the x and y complexes gives P_n with one free A^e generator e_{i,j} for each i+j=n. Characteristic two removes every tensor sign. Applying Hom_{A^e}(-,A) gives zero differential. The shuffle comparison sends e_{i,j} to all normalized bar words with i x's and j y's. Internal unlike products cancel in paired words; equal adjacent products vanish. The outer terms are exactly the stated differential.

Derivations partial_x and partial_y are well-defined because differentiation kills the relations x^2,y^2 in characteristic two. Their ordered cup powers evaluate on the shuffle to one exactly on e_{i,j}, so their classes u,v give the stated coordinates without an unspecified polynomial isomorphism. The commutator/evaluation formulas determine [u,x]=[x,u]=1 and [v,y]=[y,v]=1, with all other generator brackets zero. The Gerstenhaber biderivation identity then yields

[F,G]=F_x G_u+F_u G_x+F_y G_v+F_v G_y.

This is compatible with the generator formulas in Hermann 9.4, but the derivation here does not rely on the source's extra squaring statement.

The A-resolution Q_n=A with differential y is exact because ker(y)=yA. Applying Hom_A(-,M) gives zero differential, and identity shifts show Ext_A^*(M,M)=M[eta]. The chain map Q -> P tensor_A M is defined by 1 -> e_{0,n} tensor 1. Its differential is y_L, since y_R annihilates M, so it lifts the identity on M. Evaluating an A-bimodule cochain on this map proves, in every degree,

chi(x)=x, chi(y)=0, chi(u)=0, chi(v)=eta.

Thus chi is onto, and its kernel is (y,u)R. This is an all-degree statement over arbitrary characteristic-two fields, with no finite-field assumption.

Happel's sequence now gives injectivity of HH^n(B) -> HH^n(A) for n>=1, with image ker(chi)_n. In degree zero, a central matrix must be diagonal and satisfy a mod y=c. Projection to A is injective with image K+yA. Therefore the whole image is L=K+(y,u)R.

## 5. Identification of the original gamma, not a replacement sequence

Let f=1-e and E=Kf direct-sum Ke. E is separable over K. In the normalized E-relative bar complex, B/E has an A/K summand from f to f and an M summand from f to e. A composable tensor chain therefore consists either of all A/K factors, or of A/K factors followed by one M. There are no remaining nonidentity e-to-e factors. E-bimodule cochains with coefficients in A=B/I must vanish on the latter mixed chains: their output would have to be in fAe=0. They have no eAe output either. The all-A chain component is exactly the normalized Hochschild cochain complex of A.

The coefficient map B -> A restricts a B-valued relative cochain to that all-A/output-A component. This is the same component as the corner restriction g from Happel's sequence. Since E is separable, the relative bar resolution computes ordinary Hochschild cohomology. This identifies gamma from the original coefficient sequence with g in all degrees.

For cup products, insertions, and braces evaluated on all-A inputs, every intermediate output is in fBf=A. There is no possible mixed or e-corner intermediate output. Thus projection commutes with every insertion, including degree-zero insertions, and hence with the bracket. This gives a direct compatibility argument matching OWR Lemma 4 and Theorem 3. In particular gamma is injective and transports the ambient bracket to L.

The original coefficient Ext groups then follow from exactness:

Ext^0_{B^e}(B,I)=0,
Ext^1_{B^e}(B,I)=A/(K+yA)=M/K,
Ext^{n+1}_{B^e}(B,I)=HH^n(A)/L_n=M eta^n for n>=1.

The maps from these coefficient Ext groups into HH^*(B) vanish. These assertions describe vector spaces and their coefficient-sequence maps, not an additional Lie structure on the coefficient Ext groups.

## 6. Boundary cases and exact requested structure

The dimension of L_0 is three. For n>=1, the terms with at least one u contribute 4n basis monomials, and the terms with no u but one y contribute two more. Thus the positive-degree dimension is 4n+2. Formal differentiation and the biderivation expansion give manuscript equation (4), including its integer coefficients reduced mod two. Terms with negative powers have zero prefactors; terms divisible by x^2 or y^2 are zero. Brackets with scalars vanish. Degree-zero brackets with positive-degree classes are included. L is closed because its ideal generators y and u bracket to zero, and every biderivation expansion of brackets of ideal multiples retains at least one such factor.

Every construction above is field-linear with coefficients zero or one. No algebraic closure, finiteness, perfection, or prime-field restriction occurs. Extension of scalars to any field of characteristic two preserves the resolutions and comparisons. This meets the unrestricted field quantifier.

The OWR question is about the Gerstenhaber Lie bracket and whether its displayed coefficient sequence can be used. Its context does not ask for restricted powers, divided squaring, or all higher brace operations. The manuscript explicitly leaves those additional structures outside its claim. This is consistent with the literal target.

Hermann Definition 3.4 and 3.8 (PDF pages 10-11) locate the separate squaring operation on even HH degrees, with target degree 2|alpha|-1. The printed formula in 9.4 giving sq(alpha)=alpha^2 has ordinary cup-square degree 2|alpha|. For example alpha=u^2 would produce a nonzero degree-four cup square, whereas the squaring target is degree three. This is a literal source-text inconsistency and must not be used as a verified squaring formula. It is not used in manuscript equations (1)-(10).
