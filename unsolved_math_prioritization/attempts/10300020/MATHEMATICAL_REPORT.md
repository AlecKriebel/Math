# Exact norm spectra for normal lamination cycles

Problem 10300020 / AMR-102-0020, rank 1249, Calegari Question 7.5.

Status: partial, first proof-search attempt (1/5). The unrestricted question is not resolved. The results below isolate its exact numerical obstruction and close a chain-level equality gap in applying the known restricted straightening results. The known restricted cases are credited, not claimed as new.

## 1. Scope and conventions

Let M be a nonempty connected closed oriented 3-manifold. Every essential lamination considered here is required to be nonempty. Whenever discussing the original question for M, assume that M carries such a lamination; otherwise the original input hypothesis has no instances. Write C_*(M;R) for the ordinary singular chain complex: a basis element is a parameterized continuous map from the standard simplex, and a finite chain is written after combining identical maps. Its l1 norm is the sum of the absolute values of the resulting coefficients. In particular, opposite coefficients on the same singular map cancel; coefficients on distinct maps with overlapping images do not.

For an essential lamination L, call a singular 3-simplex L-normal in the topological normal-disk sense used in [K, printed p115]: inverse images of leaves consist of normal disks, characterized by their meeting each edge at most once. This is not a demand that the disks be geometrically affine. All allowed boundary/degeneracy conventions are held fixed throughout. A homeomorphism of the domain equal to the identity on its entire boundary preserves these conventions as well as normality. The proof below therefore does not need constant simplices to be normal, or an open ball disjoint from L.

The question asks whether every real fundamental cycle C admits a fundamental cycle C' and an essential lamination L', with ||C'||_1 = ||C||_1 and C' normal to L'. There is no requirement that L' be isotopic to the input lamination, or that C' be obtained by homotoping each simplex of C. Thus the input lamination supplies an existence hypothesis; the conclusion can use any essential lamination on M. No positivity constraint on the coefficients of C' is imposed.

These conventions agree with the finite real singular-chain convention explicitly stated in [C0, Definition 2.2.1] and the original question [C, Question 7.5]. We do not identify singular simplices under arbitrary reparameterization or homotopy. Passing to such a quotient would change the problem and invalidate the fresh-support argument below.

The main statements are proved for closed oriented M. The padding argument also works for finite relative fundamental cycles of a compact oriented manifold, after deleting basis simplices lying wholly in the boundary. This does not assert a result for arbitrary noncompact, locally finite or ideal-chain conventions, or for nonorientable manifolds without the appropriate local coefficients.

## 2. A normal boundary with fresh support

### Lemma 2.1 (normal reparameterization)

If sigma: Delta^3 -> M is L-normal and h: Delta^3 -> Delta^3 is a homeomorphism fixed pointwise on the boundary, then sigma composed with h is L-normal. It has precisely the same restrictions to every face as sigma.

Proof. For every leaf F, (sigma h)^(-1)(F) = h^(-1)(sigma^(-1)(F)). A homeomorphism carries each disk component to a disk component. Since h fixes every edge pointwise, the edge-intersection set of the new disk equals that of the original disk. In particular, its cardinality on each edge is unchanged. Faces and their allowed exceptional cases are fixed as well. The identity on the boundary also proves the face-restriction assertion. This uses the normal-disk definition, not a claim that an arbitrary homeomorphism preserves a literal affine equation. QED.

### Lemma 2.2 (infinitely many distinct maps)

If sigma: Delta^3 -> M is nonconstant, then the set of maps sigma h, as h ranges over boundary-fixed homeomorphisms, is infinite. Given any finite collection E of singular 3-simplices, two of these maps can be chosen distinct from one another and outside E.

Proof. The restriction of sigma to the interior is nonconstant: otherwise continuity and density of the interior would make sigma constant on the whole simplex. Fix an interior point x_0. The image of the interior under sigma is a connected set with at least two points in the Hausdorff manifold M, and therefore is infinite. More concretely, the image of a path between two points with different images is a nontrivial connected set and cannot be finite.

Homeomorphisms of a 3-ball fixed on its boundary act transitively on its interior. This follows, for example, by moving a point along an interior path with a finite composition of homeomorphisms supported in small interior balls. For each interior x choose h_x with h_x(x_0)=x. Then (sigma h_x)(x_0)=sigma(x). Choose two distinct values of sigma(x) outside the finite set {eta(x_0): eta in E}; the corresponding maps have the claimed properties. These homeomorphisms can be chosen isotopic to the identity, although this is not needed below. QED.

### Lemma 2.3 (explicit null-homology)

Let h_1,h_2 be two boundary-fixed homeomorphisms of Delta^3. Then sigma h_1 - sigma h_2 is the boundary of a finite singular 4-chain in M.

Proof. Regard h_1,h_2 as singular 3-simplices of Delta^3. Their boundaries are identical term by term. Fix w in Delta^3. Cone a singular k-simplex f of Delta^3 to w by

K(f)(t_0,...,t_{k+1}) = t_0 w + (1-t_0) f(t_1/(1-t_0),...,t_{k+1}/(1-t_0)),

with value w when t_0=1. Convexity makes this well-defined and continuous. The usual face computation gives boundary K(f) = f - K(boundary f) in positive degree. Therefore

boundary(K(h_1)-K(h_2)) = h_1-h_2.

Push this equality forward by sigma. The resulting 4-chain has two terms. Its boundary is exactly sigma h_1 - sigma h_2 in the ordinary, unnormalized singular complex. No claim that stationary prism terms vanish is being used. QED.

### Lemma 2.4 (a fundamental cycle has a nonconstant term)

Every real fundamental cycle of a nonempty closed oriented 3-manifold contains a nonconstant simplex with nonzero coefficient.

Proof. If k_p^n is the constant n-simplex at p, then boundary k_p^4 = k_p^3 because the alternating sum of the five face signs is 1. Thus a chain supported entirely on constant 3-simplices is a boundary. It cannot represent the nonzero fundamental class. QED.

### Theorem 2.5 (exact padding)

Let z be an L-normal real fundamental cycle. For every real r >= ||z||_1, there is an L-normal fundamental cycle z_r satisfying ||z_r||_1 = r. The lamination L itself need not change.

Proof. If r=||z||_1 take z_r=z. Otherwise choose a nonconstant sigma in the support of z, using Lemma 2.4. Lemmas 2.1 and 2.2 give two L-normal simplices tau_1=sigma h_1 and tau_2=sigma h_2 which are distinct from each other and from every basis element in z. Lemma 2.3 gives a finite 4-chain B with boundary B=tau_1-tau_2. Set

t=(r-||z||_1)/2,     z_r=z+t(tau_1-tau_2).

Then z_r-z=t boundary B, so z_r is a fundamental cycle. Every term is L-normal. There is no cancellation between the old and new supports or between the two new simplices. Consequently ||z_r||_1=||z||_1+2t=r. QED.

Remarks. This construction may introduce a negative coefficient. It does not preserve an additional all-positive convention. It uses distinct parameterized maps, not the formally zero expression sigma-sigma. It does not depend on an open complementary region, normality of constant simplices, or the chain-map straightening being injective on basis elements.

## 3. Exact norm spectra, including the endpoint

Let

A(M) = {||z||_1 : z is a real fundamental cycle of M},

V(M) = inf A(M) = ||M||,

B_L(M) = {||z||_1 : z is an L-normal real fundamental cycle},

N_L(M) = inf B_L(M),

B(M) = union over all nonempty essential laminations L on M of B_L(M),

N(M) = inf B(M).

The infimum of the empty set is +infinity. Thus N(M) optimizes over BOTH the lamination and its normal cycle. It is not N_L for the supplied lamination. Whenever B(M) is nonempty, V(M) <= N(M) < infinity.

### Theorem 3.1 (upper-ray spectra)

Every nonempty B_L(M) is either (N_L(M),infinity) or [N_L(M),infinity), with the second case occurring exactly when its infimum is attained. Similarly every nonempty B(M) is either (N(M),infinity) or [N(M),infinity). The ordinary spectrum A(M) is either (V(M),infinity) or [V(M),infinity).

Proof. Theorem 2.5 says B_L is upward closed. Its union B is upward closed too: a particular witnessing lamination continues to witness every larger number. Any nonempty upward-closed subset of R with finite lower bound contains every number strictly above its infimum: for r>inf choose an element below r, and use upward closure. Only inclusion of the infimum remains undecided.

The proof of Theorem 2.5 with the normality requirement omitted applies to ordinary fundamental cycles, giving the statement for A. Fundamental cycles exist for closed oriented manifolds, and V is finite. QED.

### Theorem 3.2 (exact equivalence for Calegari's question)

For a closed oriented 3-manifold M carrying an essential lamination, the following are equivalent:

1. Every real fundamental cycle C has a same-norm fundamental cycle normal to some essential lamination, allowed to depend on C.
2. A(M)=B(M).
3. N(M)=V(M), and if V(M) is attained by an ordinary fundamental cycle, then N(M) is attained by a cycle normal to some essential lamination.

Proof. The first statement is exactly A subset B, and B subset A is automatic, giving equivalence with the second. Equality of sets gives equality of infima and the endpoint condition. Conversely suppose the third statement. If r is the norm of an ordinary fundamental cycle, then either r>V=N, in which case Theorem 3.1 puts r in B, or r=V=N, in which case the endpoint condition puts r in B. QED.

This is not a proof that equality of infima always holds. It identifies precisely the extra condition needed before using an infimum equality as a solution to the original exact-cycle question.

### Corollary 3.3 (nonattainment removes the endpoint issue)

If M carries a nonempty essential lamination and V(M) is not attained by any ordinary finite real fundamental cycle, the original exact-cycle question for M is equivalent to N(M)=V(M).

In particular, if N_L(M)=V(M) for one fixed essential lamination and V is not attained, every prescribed cycle norm can be realized using that same lamination. It is also sufficient that there be a sequence of pairs (L_j,z_j) with z_j L_j-normal and ||z_j||_1 tending to V; a single lamination realizing the infimum is not required.

### Corollary 3.4 (a counterexample needs a uniform gap in the nonattained case)

Assume M carries a nonempty essential lamination and V is not attained. Failure of the question is equivalent to N(M)>V(M), allowing N=+infinity. If N is finite this is a uniform positive lower gap across ALL essential laminations, not merely a gap for a selected lamination.

Proof. If N>V, the defining property of the infimum V gives an ordinary fundamental cycle C with ||C||_1<N, which cannot have a normal same-norm replacement for any essential lamination. Conversely, if a prescribed cycle of norm r cannot be replaced, Theorem 3.1 gives N>=r>V (or B empty). QED.

Consequently, a strict gap N_L>V for each individual L is not by itself a counterexample: these gaps could tend to zero as L varies. A finite menu of laminations each with a strict gap does have a positive minimum gap, and hence cannot handle all prescribed cycles.

## 4. Two classes with no ordinary minimizing cycle

### Proposition 4.1 (zero simplicial volume)

If V(M)=0, the ordinary infimum is not attained.

Proof. A finite singular chain has l1 norm zero exactly when it is the zero chain. The zero chain does not represent the nonzero fundamental class. QED.

Thus for such M, the remaining question is exactly whether normal essential-lamination cycles with norms arbitrarily close to zero exist. The padding theorem supplies exact equality with every positive input norm once that geometric fact is known.

### Proposition 4.2 (closed hyperbolic manifolds)

If M is a closed oriented hyperbolic 3-manifold, every finite real fundamental cycle C satisfies

||C||_1 > Vol(M)/v_3 = V(M),

where v_3 is the volume of the regular ideal tetrahedron.

Proof. Write C=sum a_i sigma_i with distinct supported maps and nonzero coefficients. Geodesic straightening is a chain map chain-homotopic to the identity. Its straight simplices lift to geodesic tetrahedra in H^3 with finite vertices. Signed volume evaluation therefore gives

Vol(M) = sum a_i Vol(str sigma_i).

Every finite-vertex tetrahedron has absolute volume strictly below v_3. For a nondegenerate tetrahedron, put an interior point at the center of the Klein ball and extend its four radial vertex rays to the sphere at infinity. The resulting ideal tetrahedron strictly contains the original tetrahedron, so has strictly larger volume, and ideal tetrahedra have volume at most v_3. Degenerate tetrahedra have volume zero. Because the supported family is finite, q=max_i |Vol(str sigma_i)| is strictly less than v_3. Consequently

Vol(M) <= q sum |a_i| < v_3 ||C||_1.

The equality V(M)=Vol(M)/v_3 is the Gromov-Thurston proportionality formula. The required straightening and volume facts are stated in [C0, section 2.4], [K, section 2C], and [T, section 6.1]. QED.

Here the word finite is important. No assertion about attainment by ideal, measure, completed l1, or locally finite chains is made. Nor is this proof silently extended to all JSJ-decomposed manifolds.

### Consequence 4.3

For closed oriented hyperbolic M carrying a nonempty essential lamination, the original question is exactly the equality

inf_{L essential} ||M||_L^normal = Vol(M)/v_3.

The inequality from left to right that would prove this is still missing in general. The exact norm requirement is fully restored by Theorem 2.5, rather than dropped from the target.

## 5. Known restricted results and what they really imply

[K, Proposition 2.3 and Lemma 2.4] prove normal-norm equality for tight essential laminations and for the stated unbranched/one-sided-branching cases, with the boundary hypothesis where applicable. More strongly, the proof of Lemma 2.4 explicitly constructs a face-compatible homotopy of a given cycle, replacing each simplex by one normal simplex and preserving its coefficient.

Such a replacement directly gives a normal fundamental cycle z with ||z||_1 <= ||C||_1. Equality need not follow just from the unchanged displayed coefficient list, because different new maps could coincide and cancel after collection. Theorem 2.5 repairs exactly that issue: pad z to ||C||_1. Thus the published straightening argument, together with elementary padding, meets the exact-cycle formulation in these known cases, without any nonattainment hypothesis.

Agol's earlier [A, Lemma 5.1 and following remark] provides the surface case and the tight-lamination observation already cited by Calegari. These are prior results.

[K, Corollary 7.4] invokes Tao Li's 2006 preliminary manuscript: a closed orientable atoroidal manifold carrying a transversely orientable essential lamination carries a transversely orientable tight one. On that stated scope, changing L to the tight lamination and applying the preceding paragraph yields the exact prescribed norm. This is an application of the attributed tightening claim, not an independent proof audit of Li's manuscript. The legacy author PDF was not successfully retrieved in this attempt; its failed retrieval is recorded. The author's departmental page labels the work a preliminary draft, while the currently linked personal publication list omits it. Neither omission nor a failed fetch proves withdrawal or invalidity.

If M already contains a two-sided closed pi1-injective surface S of positive genus, that surface may be used instead of the supplied lamination, regardless of whether the supplied lamination is coorientable. Here the existing nonempty essential lamination gives the irreducibility/asphericity and universal-cover conclusions of Gabai-Oertel cited in [K, p116]; we are not asserting a surface route on arbitrary reducible manifolds. In this setting S is an essential surface: its leaves are pi1-injective, cutting an irreducible manifold along S leaves irreducible pieces with incompressible boundary, and closedness supplies the boundary-incompressibility condition. Its properly embedded lifts have a Hausdorff simplicial dual tree, so the surface is tight. One may replace S by a trivially laminated product neighborhood if adopting [K]'s convention excluding isolated leaves. Kuessner's general compact tight-lamination result then supplies the required normal cycle, and padding supplies exact equality. In particular, an incompressible torus is sufficient. No theorem that every essential lamination can be made coorientable, or can be tightened, is proved here.

## 6. Proof-search routes and exact obstructions

### 6.1 Keeping the lamination fixed can genuinely fail

For foliations, [K, printed p115] identifies normality with the transverse convention. [C0, Theorem 2.4.5] gives a strict foliated-norm gap for asymptotically separated foliations on hyperbolic manifolds. Hence for such a fixed essential foliation F, choose a fundamental cycle with norm between V and N_F: there is no F-normal fundamental cycle of the same norm. This is a rigorous conditional obstruction, based on the stated prior theorem, to a universal fixed-lamination straightening strategy.

It is not a counterexample to Question 7.5: a different essential lamination can have a smaller normal norm. The proof of Theorem 3.2 deliberately optimizes over all permissible replacements.

### 6.2 Normalizing a domain does not automatically descend a lamination

A cycle can be represented by maps of finitely many tetrahedra with face cancellations. Normalizing the pulled-back lamination separately on that domain does not supply a lamination of M unless the resulting plaques agree at all points identified by the map to M, including overlaps of simplex interiors. Boundary cancellation supplies no such interior compatibility.

An elementary local model shows the obstruction. Map two disjoint copies of a 3-ball homeomorphically onto the same ball U in R^3. Put the disk z=0 in the first copy and the disk z=x in the second. Each is an embedded smooth plaque in its own domain. The union of their images is not a lamination near the line x=z=0: two distinct local sheets cross there. Thus independently well-behaved domain plaques need not descend to a target lamination. This is only a local failure of that inference, not a global counterexample with essential laminations.

The same issue appears after passing to a finite cover. If a cover-normalization happens to produce the full preimage of a downstairs essential lamination, pushing its cycle down and dividing by the degree is legitimate and norm-nonincreasing, and padding then gives exact equality. Merely having some essential lamination upstairs is insufficient: its deck translates can intersect, and their union need not be a lamination.

### 6.3 An ambient coorientation cover is not automatic

The original source [C, section 1.4, printed p2] explicitly distinguishes foliations from general laminations: laminations can have local obstructions to coorientability. Therefore the familiar orientation-double-cover shortcut for foliations is not a general proof that every essential lamination lifts to a coorientable one in an ambient finite cover. Even where a suitable cover exists, the descent compatibility in section 6.2 remains necessary.

### 6.4 Why the endpoint proviso is mathematically real

For clarity, equal infima can coexist with different endpoints even in an elementary normed chain complex. Take degree-3 basis e_0,e_1,e_2,... with l1 norm and zero outgoing differential. In degree 4 take b_n, n>=1, with boundary b_n=e_n-(n/(n+1))e_0. The class alpha=[e_0] has seminorm 1, attained at e_0. Indeed the cocycle phi(e_0)=1, phi(e_n)=n/(n+1) has norm 1 and evaluates to 1 on alpha.

Restrict admissible degree-3 chains to the span of e_n, n>=1. The representative ((n+1)/n)e_n has norm 1+1/n, so the admissible infimum is also 1. But every finite admissible representative c has

1=phi(c) <= sum |c_n| n/(n+1) < sum |c_n|=||c||_1,

so it never attains 1. This example is not asserted to be a manifold or lamination example. It verifies the logic behind retaining an endpoint condition when nonattainment has not been proved.

## 7. Remaining problem and next useful target

The proved partial result is an exact norm-spectrum theorem, including a source-correct padding construction and the complete endpoint criterion. For zero-volume and closed hyperbolic manifolds, nonattainment removes the endpoint issue altogether. The known tight and one-sided cases meet the requested exact norm after cancellation is handled.

The unresolved geometric task is to show N(M)=V(M), together with endpoint preservation whenever V(M) is attained, for every manifold carrying a nonempty essential lamination in the intended unrestricted class. A counterexample must establish a failure of that equality or of the required endpoint preservation; where ordinary nonattainment is known, it must establish a uniform gap across all essential laminations on a particular M. A gap for one chosen foliation, a finite-cover construction without descent, or an equality of infima without endpoint control in the general compact setting does not settle the question.

For the closed orientable setting, any remaining counterexample must evade the known incompressible-surface route and all applicable tight/unbranched/one-sided routes. Assuming the cited Li tightening claim, it must also evade the closed atoroidal transversely orientable route. This is a scope reduction, not a resolution of those broader existence/tightening questions.

No global proof, global counterexample, novelty claim, or current-openness certification is made.

## Review status

The [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the stated padding, upper-ray, infimum-plus-endpoint, and nonattainment results, together with the qualified applications of prior normalization theorems. This AI-assisted, unrefereed proof-and-audit edition is not external human peer review, journal acceptance or formal proof-assistant certification. The original general question remains unresolved. Li's unavailable preliminary tightening manuscript remains an attributed, unaudited premise for its expressly restricted application.

## References

[C] Danny Calegari, Problems in foliations and laminations of 3-manifolds, arXiv:math/0209081v1 (2002), Question 7.5, printed p14; coorientability warning, p2. https://arxiv.org/abs/math/0209081

[K] Thilo Kuessner, Generalizations of Agol's inequality and nonexistence of tight laminations, Pacific Journal of Mathematics 251 (2011), 109-172. Normality definition p115; Proposition 2.3, Lemma 2.4 and proof pp116-119; Corollary 7.4 p169. https://msp.org/pjm/2011/251-1/pjm-v251-n1-p.pdf

[A] Ian Agol, Lower bounds on volumes of hyperbolic Haken 3-manifolds, arXiv:math/9906182. Lemma 5.1 and its proof p6, following tight-lamination remark p7. https://arxiv.org/abs/math/9906182

[C0] Danny Calegari, The Gromov norm and foliations, Geometric and Functional Analysis 10 (2000), 1423-1447; arXiv:math/0007120v2 (2001), reflecting the published version. Definition 2.2.1 p5; section 2.4 pp9-12; Theorem 2.4.5 pp11-12. https://arxiv.org/abs/math/0007120

[T] William P. Thurston, The Geometry and Topology of Three-Manifolds, section 6.1, including the finite/ideal simplex volume bound and the Gromov norm formula. Public institutional copy: https://library.slmath.org/nonmsri/gt3m/PDF/Thurston-gt3m.pdf

[L-status] Tao Li, departmental publication list, listing Compression branched surfaces and tight essential laminations as a preliminary draft. This is status evidence, not a substitute for the original proof. https://www.bc.edu/bc-web/schools/morrissey/departments/math/people/faculty-directory/tao-li.html
