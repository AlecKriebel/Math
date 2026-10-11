# Audit of Ferudun's Theorems D and F on Fuchs's reachable polygons

The existing proofs are attributed to Alper Ferudun's version 1.0 manuscript dated October 9, 2026, an unrefereed AI-assisted preprint. Acceptance here is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or a claim of new authorship, novelty or mathematical consensus.

The complete authored mathematical arguments, formulas and analytical constructions of both audits are retained. This is not a computational reproduction package: executable code, raw datasets or certificate tables, copied source PDFs/text/images, and private coordination material are not distributed. Historical finite checks are supplementary evidence; the all-n results rest on the written geometric arguments. Those historical computations cannot be reproduced from this edition alone.

Statements about source inspection and mathematical executions below describe the original audits, not new inspection or executions during preparation of this public review edition. The original audit documents remain unchanged. The first full audit is PROOF.md; the complete focused geometric acceptance is AUDIT.md.

## Decision and exact scope

**Mathematical audit: PASS for both target claims, with the source-reading conventions stated below.** The audited argument proves Fuchs Conjecture 2.3 for every integer n >= 5 and disproves both the existence and infinitude formulations of Conjecture 2.4 for every n >= 5. This is verification of Alper Ferudun's existing Theorems D and F, not a new solution or a novelty claim.

Ferudun's manuscript remains an **unrefereed, AI-assisted preprint**, version 1.0, dated October 9, 2026. This audit is a reasoned local acceptance of the specified arguments. It neither changes that publication status nor establishes acceptance by the mathematical literature. It does not audit the other five conjectures in the paper. Theorem E is read to resolve the n=6 conflict, but its complete all-n claim is not a target acceptance here.

The exact two conclusions accepted are:

1. If a linear orientation- and area-preserving map g sends the normalized regular n-gon P to a polygon whose nonzero vertices are reachable, the clockwise vertices from the distinguished origin have types A_0,A_1,...,A_(n-3),A_0. In fact, Ferudun proves the stronger four-vertex criterion: reachability of gX_1,gX_2,gX_(n-2),gX_(n-1) suffices.
2. Exactly the reachable points of type A_0 are vertices of infinitely many such polygons. Every other type occurs on at most one. The particular point

   w_n = 2 + 3 zeta + zeta^2,  zeta = exp(2 pi i/n),

   is reachable of type A_(n-3), but is a vertex of no reachable polygon.

The fixed origin and normalized sector are essential. No arbitrary translation of a polygon is allowed. Assertions about a wider class of translated polygons would be different problems.

## Sources and attribution

[F] Dmitry Fuchs, *Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra*, Arnold Mathematical Journal 7 (2021), 493-517, DOI 10.1007/s40598-020-00170-8. Public primary PDF: <https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf>.

[R] Alper Ferudun, *On Seven Conjectures of Fuchs on Billiard Trajectories in Regular Polygons and Geodesics on the Regular Dodecahedron*, version 1.0, October 9, 2026, DOI 10.5281/zenodo.23267641. Public record: <https://zenodo.org/records/23267641>. Audited PDF: <https://zenodo.org/api/records/23267641/files/AMR-049-paper.pdf/content>.

[F] has 25 PDF pages. [R] has 41. Page numbers below are PDF page numbers unless the journal page is given. The authenticated PDF identities are:

- [F]: 3,572,784 bytes; SHA-256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d
- [R]: 380,876 bytes; SHA-256 ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707

The original audit authenticated its source evidence. No author program, source archive, executable, Lean code, or author-generated certificate was retrieved or executed for that audit. Source copies and raw evidence are not distributed in this edition.

## 1. Exact reading of Fuchs's definitions

Put t=pi/n, omega=pi-2t, S=sin(2t), lambda=2cos(t), and lambda_k=sin((k+1)t)/sin(t). Number the initial vertices clockwise with X_0=0 and X_(n-1)=1. Then

- xi=X_(n-1)=1 and eta=X_1=exp(i omega)
- det(xi,eta)=S>0
- X_(k+1) has length lambda_k and argument (n-2-k)t
- X_2=xi+(lambda^2-1)eta
- X_(n-2)=eta+(lambda^2-1)xi

The normalization is fixed by [F, Sections 2.1-2.4, Figures 8-9]. The printed coordinate for eta in the unitary-pair paragraph has a sign inconsistent with both the normalized polygon and the explicitly printed n=6 basis. We use the actual side X_1, not that isolated inconsistent coordinate.

A reachable point is the endpoint of a developed trajectory from O which encounters no intervening vertex. Its direction lies in [0,omega]. A reachable polygon is gP with g in SL(2,R), acting linearly and therefore fixing O. The ordinary meaning of the area-preserving map here does not permit translations, scalings, reflection, or a freely chosen new origin.

### 1.1 Angles, parity, and the unsafe A_0 shortcut

Figure 8 defines alpha at the initial vertex and pi-beta at the terminal vertex, using the oriented boundary. The ranges are 0<=alpha<=omega and 2t<=beta<=pi. The sentence immediately preceding Definition 2.1 specifies the sign through N, the number of trajectory segments: use the sum for odd N and the difference for even N.

With that rule, the type residue k modulo n-2 is equivalently:

- odd N: alpha+beta=2jt, 1<=j<=n-1, k=n-1-j modulo n-2
- even N: beta-alpha=2jt, -(n-4)<=2j<=n, k=j-1 modulo n-2

This equivalence follows directly from the four branches of the printed definition. In the difference branches, the alpha cutoffs are the corresponding beta upper/lower bounds. In the sum branches they likewise become beta bounds. Representatives k=0 and k=n-2 both describe A_0 and must be allowed when checking the side endpoints.

**The parity rule cannot be discarded.** A one-segment diagonal OX_(k+1) has alpha=(n-2-k)t and beta=(n-k)t. Thus every diagonal satisfies beta-alpha=2t, while Figure 9 explicitly gives its type A_k. The sum rule returns that type correctly. Reading the bare A_0 shortcut literally without parity would contradict the source's own diagonal example. The conclusions in this audit concern the coherent reading of the source's parity rule, Figure 8, Definition 2.1 and Figure 9 together. They are not an endorsement of the inconsistent shortcut in isolation.

For a non-base direction only one of sum and difference can be a multiple of 2t. If both were, alpha would be a multiple of t. Such a ray from a polygon vertex first reaches another vertex of the initial polygon, so N=1; the diagonal convention resolves precisely these cases.

### 1.2 Odd-n first-case bound: no amendment is needed

For n=2m+1, the first printed branch permits k<=m+1. Ferudun calls this a typo for k<=m-1. The audit does not assume an authorized amendment. At either extra index k=m or k=m+1, that branch also requires

alpha <= (n-2(k+1))pi/n < 0.

Since alpha>=0, these extra cases are empty. The original printed branch and the shortened bound define the same admissible trajectories. This resolves the flagged difference without silently changing the target.

### 1.3 n=6 local convention check

In the basis (xi,eta), Fuchs's initial hexagon has vertices

(0,0), (0,1), (1,2), (2,2), (2,1), (1,0).

Its sector is exactly p,q>=0. The source's reachable-point criterion is: p+q is not 2 modulo 3, and either gcd(p,q)=1 or gcd(p,q)=2 with p+q=1 modulo 3. The four types are the explicit residue/parity types in [F, PDF 14, journal p.506]. These agree with the all-n angular conventions. The separate elementary proof of Conjecture 2.3 for n=6 in [F, PDF 16-17] is valid and is retained as prior work.

## 2. Dependency audit: unfolding, types, and cylinders

Theorem D depends on [R, Sections 2 and 4], and Theorem F additionally on Lemma 6.1. Theorems B, C, E, G and H are not needed to prove D or F. In particular, neither a computational classification nor any uninspected external theorem is being used to fill a gap in the relevant proof chain.

### 2.1 Double polygon and the angular invariant

Reflection of a regular polygon across an edge agrees as a polygonal set with point reflection through the edge midpoint: the difference is a symmetry of the regular polygon. Hence developed copies have the form c+epsilon P, epsilon=+1 or -1, and crossing the edge corresponding to [X_s,X_(s+1)] changes c by epsilon(X_s+X_(s+1)). This verifies [R, Lemma 2.1]. It does not assert that reflected vertex labels are unchanged; the later angle calculation accounts for orientation.

Glue P and -P along parallel corresponding edges by translation. The corner identifications are

(epsilon,s,omega)=(-epsilon,s+1,0).

There is one vertex for odd n and two for even n. Every short development from O is a saddle connection starting in the particular corner (+,0), and conversely. Keeping this corner is necessary: a holonomy vector alone need not identify the starting ray on the conical surface.

Define B(epsilon,s,phi)=s omega+phi modulo (n-2)pi. The corner identification makes B well-defined and continuous. Its direction agrees with B modulo pi. Therefore the difference of B at the terminal reversed ray and at the initial ray, divided by pi, gives an integer K modulo n-2. Direct substitution in the two possible orientations of the last polygon gives exactly the two parity formulas in Section 1.1. In particular K(OX_(k+1))=k. This checks [R, Lemmas 2.2-2.4], including the signs and the endpoint-ray orientation.

An orientation-preserving affine map whose lift of the direction action has the same B-offset at all vertices preserves K. The proof uses F(x+pi)=F(x)+pi and cancels the common offset. The explicitly described rotations and central symmetry have uniform offsets; the sector-bisector reflection negates K. The permutation and offset formulas in [R, Lemmas 2.5-2.6] respect the edge gluing for both parities of n. No unproved claim that *all* affine automorphisms preserve K is needed.

### 2.2 Cylinder geometry and the crossing bound

Parallel sides/diagonals subdivide P into quadrilateral or triangular strips. For the strip between X_aX_(a+j) and X_(a+1)X_(a+j-1), its copy in -P glues to it to form a cylinder. Its height and circumference are

h=sin((j-1)t),  ell=lambda lambda_(j-2).

Indeed, point-reflect the strip through the intervening edge midpoint. The two pieces form a parallelogram; the long-side length is the sum of the two chord lengths, and the height follows from the inscribed angle. Thus ell/h=2cot(t), including triangular strips, and the boundary vertex lifts are exactly the two endpoint families translated by integer multiples of ell. This checks the possible degeneracy j=2 and the case when one chord is a polygon side. Identified boundary saddle connections still have distinct boundary-side occurrences; the universal strip keeps those occurrences separate.

A geodesic entering a cylinder and ending at a vertex cannot stop before crossing its full height. There is no vertex in the open cylinder. If its transverse displacement equals the cylinder height, it ends on the opposite boundary at one of the listed vertex lifts. Conversely a straight segment between opposite-boundary vertex lifts has no internal vertex. This is [R, Lemma 2.9]. Its local half-plane statement is valid at each boundary occurrence of a conical vertex, not just at a smooth plane point.

Because all these cylinders have the same modulus, the shear with coefficient 2cot(t) makes a full twist in every cylinder and is identity along their boundaries. The pieces therefore glue to an affine automorphism tau_k with the claimed derivative in every base direction kt. It fixes the base-direction rays, so its B-offset is zero at every vertex and it preserves K. This validates [R, Lemma 2.10] without author code or an appeal to an uninspected Veech theorem.

### 2.3 Descent and orbit classification

A ray in any corner in a direction that is a multiple of t points at another polygon vertex, so the base-direction saddle connections are exactly polygon sides and diagonals. There are only finitely many saddle connections of bounded length: in the elementary proof in [R, Lemma 2.11], any three successive side crossings either include nonadjacent sides at a positive distance, or encounter two different ends of the shared side and again force a fixed positive displacement. Three edges around the same vertex would span an angle at least pi and cannot all be crossed by a line avoiding that vertex. Thus a length bound gives a bound on the number of crossed sides and hence finitely many polygon chains.

For a non-base direction, choose kt<theta<(k+1)t. In that orthonormal frame its vector has y>0 and x>y cot(t). An inverse twist replaces x by x-2y cot(t), strictly reducing squared length. Repetition must terminate by the just-proved finiteness. The terminal side/diagonal can be moved to the corner (+,0) by the explicit isometries. Finally the two sides at O are in the same orbit. K distinguishes the other diagonal representatives.

This proves the form of Theorem A used below: every saddle connection of type A_k is the image of delta_k=OX_(k+1) under an element of the specified type-preserving affine group G_0. The finiteness step is essential; strict decrease alone would not prove termination. The manuscript supplies it.

## 3. Audit of Theorem D / Conjecture 2.3

Write u=g xi and v=g eta. The determinant is S, and reachability puts the two vectors in the normalized sector with arg(u)<arg(v). On the conical surface their initial rays are in the same corner and are separated by less than pi. An orientation-preserving affine map preserves that specific ordered ray interval, not merely the directions modulo pi. This is the ray fact in [R, Lemma 4.1].

Choose a type-preserving affine map sending delta_k to the saddle connection of v. Pull u back by it. The pulled-back ray is on the clockwise side of delta_k and enters its right-hand cylinder, whose height is sin((k+2)t). Its transverse displacement is S/lambda_k. The crossing bound gives

sin(t) sin(2t) >= sin((k+1)t) sin((k+2)t).

Equivalently, cos((2k+3)t)>=cos(3t). For 0<=k<=n-3, the argument ranges from 3t to 2pi-3t, so equality at the endpoints is the only possibility: k=0 or k=n-3.

The second possibility is excluded using the required point gX_(n-2)=v+(lambda^2-1)u. In this case the first cylinder is the triangle adjacent to delta_(n-3), with height sin(t). The pulled-back trajectory has total transverse displacement (lambda^2-1)sin(t). It crosses that first cylinder. Since an intermediate vertex is forbidden, it enters the next cylinder through a nonvertex. The next cylinder has height sin(3t), but only

(lambda^2-2)sin(t)=sin(3t)-sin(t)

of transverse displacement remains. This is positive and strictly less than sin(3t) for every n>=5. The crossing bound gives a contradiction. Thus v has type A_0. Conjugating by the sector-bisector reflection applies the same reasoning to u, using gX_2, so u also has type A_0. The four-point hypothesis is sufficient; no other vertex reachability was used in this reduction.

Now the relevant side cylinder has height S and circumference lambda^2. Its opposite-boundary vertex lifts are

xi+t eta, with t in lambda^2 Z or lambda^2 Z-1.

The two families have types A_0 and A_1 respectively, because full twists preserve K. Since the pulled-back u has type A_0, it belongs to the first family. Composing with the corresponding full twist gives an affine map with derivative exactly g and sending the two side saddle connections to those of u and v. Its ray interval from xi to eta goes into the original corner. Every diagonal from O therefore maps to the correct reachable point gX_j and preserves its type. This proves both the stronger criterion and the exact Conjecture 2.3 pattern.

The same construction, starting directly with an A_0 unitary pair of determinant S, establishes the equivalence between such a pair and the two vertices adjacent to O in a reachable polygon. The manuscript proves the equivalence; it does not rely on the incorrect theorem-number cross-reference in Fuchs's unitary-pair paragraph.

**No gap was found in this proof chain.** In particular, the determinant normalization, the side of the cylinder, the second-cylinder argument, all four required vertices, the distinction A_0 versus A_1, and the initial-corner restriction have been checked.

## 4. Audit of Theorem F / Conjecture 2.4

### 4.1 Infinitely many polygons through each A_0 point

For a reachable A_0 point w different from xi, choose an affine map carrying the side eta to w. The full side-cylinder twists give A_0 saddle connections with holonomies u_i=A xi+i lambda^2 w and determinant det(u_i,w)=S. As i tends to positive infinity, their initial rays approach that of w from the clockwise side within a ray interval shorter than pi. Since arg(w)>0, all sufficiently large i start in the distinguished corner. Thus they are genuinely reachable, not merely holonomy vectors somewhere on the surface. The unitary-pair equivalence gives infinitely many reachable polygons. Distinct u_i give distinct polygons because the ordered side vertices at the fixed origin identify the polygon. The boundary point xi is covered by the sector reflection. This verifies F(a).

### 4.2 At most one for the other types

Let 1<=k<=n-3. Write

X_(k+1)=a eta+b xi,

a=lambda_k sin((k+2)t)/S,  b=lambda_k sin(kt)/S.

Both a and b are strictly positive. Fix a type-preserving affine map carrying delta_k to the connection of a reachable point w, and put u=g xi, v=g eta. If another reachable polygon g'P contains w, Theorem D fixes its vertex index at k+1. Apply the exact-height cylinder argument on both sides of delta_k. The A_0 condition on the two side vertices selects one endpoint family on each cylinder. It follows that, for an integer i,

g' eta=v+i c_1 w,  g' xi=u-i c_2 w,

where c_1=lambda lambda_(k-1)/lambda_k and c_2=lambda lambda_(k+1)/lambda_k. The same integer occurs on both sides because

a c_1=b c_2=kappa=sin(kt)sin((k+2)t)/sin(t)^2.

The endpoint cases k=1 and k=n-3 cause the two lifts in one boundary family to coincide; they do not create an extra family. This is explicitly handled in Lemma 6.1.

For the given range of k, kappa>=sin(3t)/sin(t)=lambda^2-1>1. If the first polygon is itself reachable, u and v have nonnegative xi/eta coordinates. For i>=1, the xi coordinate of g'xi is

(1-i kappa) f_xi(u)-i c_2 a f_xi(v).

It cannot be nonnegative unless both f_xi(u) and f_xi(v) vanish, contradicting their nonzero determinant. For i<=-1 the eta coordinate of g'eta gives the same contradiction. Consequently i=0 and g'=g. This verifies F(b). In particular the initial diagonal endpoint X_2 occurs only on P.

### 4.3 The explicit point lies on no reachable polygon

Let L=lambda^2 and d=X_(n-2)=(L-1)xi+eta. The affine twist in direction pi/n, in the xi/eta basis, has matrix

T = ((2-L, (L-1)^2), (-1,L)).

The orientation-preserving isometry used in [R, F(c)] has derivative

R = ((0,-1), (1,2-L)).

Both determinants are 1. Direct multiplication gives

T(eta-xi)=w_n=(L^2-L-1)xi+(L+1)eta,

and g_0=TR carries d to w_n. This agrees exactly with 2+3zeta+zeta^2. The ray argument in [R] tracks the twisted diagonal from the adjacent corner back into (+,0); it proves reachability and type A_(n-3), rather than only computing a holonomy vector. An independent three-polygon verification is given in Section 5 below.

For this k=n-3, Lemma 6.1 has c_1=L-1 and c_2=1. If a reachable polygon containing w_n existed, for some integer i its adjacent vertices would satisfy

g'xi=g_0xi-i w_n,  g'eta=g_0eta+i(L-1)w_n.

Their eta coordinates are respectively

L-i(L+1),

-(L^2-2L-1)+i(L^2-1).

For n>=5, L>5/2 and L^2-2L-1>0. The first nonnegative-coordinate requirement forces i<=0; the second forces i>=1. This contradiction verifies F(c) for every n>=5.

The distinction between lambda_4 and lambda^4 in the source PDF was visually checked. The formula used there is lambda_4=lambda^4-3lambda^2+1. Treating the subscript as an exponent would corrupt this calculation; the independently expanded matrices above avoid that transcription hazard.

## 5. Independent exact checks of the stated witnesses

These checks audit existing claims. They are not a new search for a conjecture solution and do not establish novelty.

### 5.1 Exact three-segment development of w_n

In xi/eta coordinates, let

A=X_(n-3)=((L-1)(L-2),L-1),

d=X_(n-2)=(L-1,1),

w=(L^2-L-1,L+1).

Use the three polygonal copies

P,  A+d-P,  A+d-xi+P.

The first reflection is across [A,d]; the second is across the corresponding copy of [xi,0]. The line r w has its two side intersections at

r_1=(L-1)/(2L-1),  r_2=L/(L+1).

Exactly,

r_1 w=A+r_1(d-A),

r_2 w=A+d-xi+r_2 xi,

w=A+d-xi+d.

For L>5/2, 0<r_1<r_2<1, since

r_2-r_1=(L^2-L+1)/((L+1)(2L-1))>0.

Each side parameter is strictly between 0 and 1. Convexity makes each intervening segment lie inside its corresponding polygon, with no intermediate vertex. The last endpoint is its X_(n-2) vertex. Therefore there are exactly three trajectory segments and the odd-N type formula gives k=n-3. This validates the claimed reachable point uniformly in n, independently of the author's computation and independently of the orbit-descent implementation.

### 5.2 Complete n=6 finite obstruction check

For n=6, L=3, so w_6=(5,4). It is reachable because gcd(5,4)=1 and 5+4=0 modulo 3, and its type is A_3. The three-segment development uses side indices 3 and 5, collision parameters 2/5 and 3/4, and endpoint X_4 in the third polygon.

A reachable hexagon has adjacent vertices v_1=v=(p,q), v_5=u=(p',q') in the nonnegative integer quadrant, det(u,v)=1, and interior vertices 2v+u,2v+2u,v+2u. Fuchs's independently checked n=6 type theorem excludes w_6 from v_1,v_5 and places its only possible position at v_4=v+2u. Write u=(a,b). Then

0<=a<=2, 0<=b<=2,  4a-5b=1.

The integer solutions are (a,b)=(4,3)+j(5,4), none in that box. This proves nonexistence directly from Fuchs's own lattice formulas, without the all-n Theorem D or Lemma 6.1.

The independent program also examines all three interior positions, not just the type-selected one. Its only determinant-one candidate at a wrong interior position for (5,4) has v_1=(1,1), v_5=(3,2); these are not reachable tile vertices. It verifies that (4,5) likewise occurs on no reachable hexagon and that X_2=(1,2) occurs exactly on the initial hexagon. The bounds in this finite check follow from nonnegative coordinates and the displayed positive linear combinations; they are exhaustive bounds, not an empirical radius cutoff. Edge positions are explicitly excluded by the source's n=6 theorem, not by the finite box.

### 5.3 Check limits

The independent program uses exact rational/integer arithmetic and symbolic polynomial identities. It checks the printed angle cases on every interval cell cut by their rational bounds for n=5 through n=64, including both parities, boundary angles and diagonal endpoints. It separately compares the printed odd-n first-case bound with the proposed shorter bound. The all-n equivalence is supplied by Section 1, not inferred from those finite tests.

Normal, -O and -OO executions are retained. Deliberately false witness-type, determinant-sign, existence, and A_0-shortcut checks must fail. The program does not formally certify the geometric prose; that is the role of the dependency-by-dependency mathematical audit above.

## 6. Resolution of the apparently conflicting n=6 proof in Fuchs

The paragraph at [F, PDF 17, journal p.509] is headed as proofs of Conjectures 2.4 and 2.5 for n=6, but its actual argument fixes an A_0 unitary pair and classifies integer points on u+tv. It does not begin with an arbitrary reachable point of another type and does not produce a polygon through such a point. That missing implication cannot be recovered from its conclusion: the explicit reachable point (5,4), using the same source's formulas, has no polygon.

There is also a constants mismatch. The n=6 argument obtains step 3 and offset 2. Since lambda=sqrt(3), these are lambda^2 and lambda^2-1, not the printed lambda+1 and lambda. Thus the paragraph supports a line-classification statement with different constants. Neither its heading nor the word “proves” cures the mismatch or establishes Conjecture 2.4.

Accordingly:

- Fuchs's n=6 proof of Conjecture 2.3 remains valid.
- The n=6 heading asserting a proof of Conjecture 2.4 overstates what the following argument does, and the universal statement is false under the fixed-origin definition.
- Ferudun's attributed counterexample and classification resolve this conflict without changing the distinguished origin or permitting translated polygons.
- The n=6 example alone refutes the catalogue's universal claim; the checked all-n argument gives the stronger failure for every n>=5.

## 7. Acceptance boundaries

There is no identified correction gap in Theorems D or F under the explicitly stated source conventions. The source typography and parity ambiguity have been addressed rather than ignored. This audit does not claim the formulas printed without their parity context form an unambiguous classification, does not elevate the manuscript to peer-reviewed status, and does not infer current mathematical consensus from repository metadata.

No claim is made here about Conjecture 2.4 for n=3 or n=4, about other definitions allowing translations, or about the other five target conjectures in [R]. This public review edition includes only authored audit material and public verification metadata, with full attribution. Copied sources, raw evidence and private coordination material are excluded.
