# Independent geometric acceptance audit: Fuchs 2.3 and 2.4

The existing proofs are attributed to Alper Ferudun's version 1.0 manuscript dated October 9, 2026, an unrefereed AI-assisted preprint. Acceptance here is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or a claim of new authorship, novelty or mathematical consensus.

The complete authored mathematical arguments, formulas and analytical constructions of both audits are retained. This is not a computational reproduction package: executable code, raw datasets or certificate tables, copied source PDFs/text/images, and private coordination material are not distributed. Historical finite checks are supplementary evidence; the all-n results rest on the written geometric arguments. Those historical computations cannot be reproduced from this edition alone.

Statements about source inspection and mathematical executions below describe the original audits, not new inspection or executions during preparation of this public review edition. The original audit documents remain unchanged. The first full audit is PROOF.md; the complete focused geometric acceptance is AUDIT.md.

## Verdict

**ACCEPT Theorems D and F of the specified Ferudun manuscript, with the source convention stated below. No mathematical correction to those two proofs is required.** This independently confirms the preceding audit's acceptance, including the four-vertex strengthening in D and all three parts of F. Acceptance is a local mathematical audit judgment, not a formal proof certificate, a human referee report, a novelty finding, or a statement of scholarly consensus.

The accepted setting is the regular side-one polygon whose distinguished vertex is the fixed origin, with reachable points in its original angle sector, and **linear** maps in SL(2,R). The types use Fuchs's segment-parity rule and his explicit diagonal labels. This is the coherent reading of his definition and figures. The isolated printed assertion that A0 is always characterized by beta-alpha=2pi/n is false without a parity qualification; this audit does not accept that assertion literally. The inconsistency is confined to base-direction, one-segment trajectories and does not create an alternative coherent target compatible with the source's diagonal example.

Consequences accepted, and only these target consequences:

- Fuchs Conjecture 2.3 holds for every n>=5.
- Fuchs Conjecture 2.4 fails for every n>=5, both as bare existence and as infinitude.
- Every reachable A0 point belongs to infinitely many reachable polygons. Each other type belongs to at most one.
- The point w_n=2+3zeta+zeta^2, zeta=exp(2pi i/n), is reachable of type A_(n-3) and belongs to no reachable polygon.

The author is Alper Ferudun; the audited manuscript is version 1.0, dated October 9, 2026, and describes itself as unrefereed. Its disclosure of AI-assisted tools is retained in the provenance. No conclusion about all seven conjectures, later versions, peer review, or new authorship follows from this report.

## Sources, independence, and integrity

[F] Dmitry Fuchs, *Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra*, Arnold Mathematical Journal 7 (2021), 493-517, DOI 10.1007/s40598-020-00170-8. Primary PDF: https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf

[R] Alper Ferudun, *On Seven Conjectures of Fuchs on Billiard Trajectories in Regular Polygons and Geodesics on the Regular Dodecahedron*, version 1.0, October 9, 2026, DOI 10.5281/zenodo.23267641. Record: https://zenodo.org/records/23267641 ; PDF: https://zenodo.org/api/records/23267641/files/AMR-049-paper.pdf/content

The candidate audit manifest was independently rehashed to the supplied pin 320d127c0d6603bb5a022712ea2721d231b63090f770996c02154ccfb8b420d5. All 42 listed members match their byte counts and hashes; the listed set plus the manifest is exactly the file set. The mathematical source PDFs have hashes:

- Fuchs: 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d, 3,572,784 bytes.
- Ferudun: ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707, 380,876 bytes.

I read the controlling passages in the source texts and inspected the figures and displayed formulas in the PDF renderings, rather than relying only on the preceding audit's explanations. Fresh Poppler extractions from both authenticated PDFs match the candidate text files byte for byte. The earlier report was also read, but no candidate or author program was run or imported. The independent check program was written for this audit. Public browsing confirmed the Fuchs primary PDF; the Ferudun record could not be opened by the web tool, so no fresh metadata response is claimed. The authenticated PDF and saved record remain the version-specific evidence.

## 1. Original definitions and the precise convention issue

Set t=pi/n, omega=pi-2t, S=sin(2t), lambda=2cos(t), and lambda_k=sin((k+1)t)/sin(t). Fuchs fixes X0=0, X_(n-1)=1, and clockwise vertex order, with the polygon above the horizontal axis [F, sections 2.1-2.2, Figure 9; PDF pages 9-11]. Thus xi=1 and eta=X1=exp(i omega). Reachability refers to a short billiard trajectory starting at that same origin and having no intermediate vertex. Its development starts in the single angle [0,omega].

The reachable-polygon definition expressly uses an SL(2,R)-image of this initial polygon, and Conjecture 2.3 expressly sets v0=O [F, journal p.508; PDF p.16]. These are linear images, fixing O. There is no license to translate the polygon or to choose a fresh origin for each reachable endpoint. The printed coordinate -cos(omega) for eta in the later unitary-pair paragraph has the wrong horizontal sign. Figure 9, the fixed sector, and the n=6 basis (-1/2,sqrt(3)/2) independently identify the actual side; correcting that isolated coordinate does not change the polygon being considered.

Figure 8 and the preceding sentence of Definition 2.1 specify N as the number of segments and fix the sign by its parity. With the counterclockwise boundary orientation, alpha is measured at the initial vertex and pi-beta at the terminal vertex along the reversed terminal segment. Therefore 0<=alpha<=omega and 2t<=beta<=pi. The branches give:

- N odd: alpha+beta=2jt, with 1<=j<=n-1, and k=n-1-j modulo n-2.
- N even: beta-alpha=2jt, with -(n-4)<=2j<=n, and k=j-1 modulo n-2.

For example, the small-k difference cutoff is alpha<=pi-2(k+1)t, exactly beta<=pi; the large-k cutoff is alpha>=2(n-k-2)t, exactly beta>=2t. The analogous sum cutoffs are the same beta bounds. The two printed odd-n extra values allowed by k<=m+1 in its first branch give a negative upper bound on alpha and hence no trajectories. Replacing this with k<=m-1 changes no admissible case.

The source does contain a real textual inconsistency. For the one-segment diagonal OX_(k+1), alpha=(n-2-k)t and beta=(n-k)t, so beta-alpha=2t for every diagonal. Yet Fuchs explicitly labels it Ak, in both prose and Figure 9. These agree with the odd-N sum rule and disagree with applying the A0 shortcut unconditionally. The tables do not remove this overlap if read without the preceding parity rule.

The ambiguity is fully localized: if both alpha+beta and beta-alpha are multiples of 2t, then alpha is a multiple of t. A ray from O in such a direction encounters a vertex of the initial polygon immediately, so a short trajectory in it is precisely a side or diagonal and has N=1. Every other trajectory has only one applicable sign. Thus the parity sentence plus the explicit diagonal example uniquely specify the intended types for every trajectory; no new type assignment is invented. Nevertheless a statement about the unqualified shortcut alone would be a different, false statement. This limitation must remain visible in any acceptance summary.

## 2. Double-polygon gluing and the B invariant

A side reflection sends the regular polygon, as a set, to its point reflection in that side's midpoint. This uses the polygon's symmetry in the perpendicular bisector of the side; it does not preserve the original reflected labels. Therefore developed polygons have form c+epsilon P and crossing side s replaces c by c+epsilon(Xs+X_(s+1)).

On the double polygon, side es is glued to -es by w -> w-Xs-X_(s+1). Its endpoints identify Xs with -X_(s+1), giving the corner successor

(epsilon,s,omega)=(-epsilon,s+1,0).

Cycling this relation gives one cone vertex for odd n, of total angle 2(n-2)pi, or two for even n, each of angle (n-2)pi. The function B(epsilon,s,phi)=s omega+phi modulo (n-2)pi respects the successor relation and increases at unit speed around a vertex. For odd n it winds twice around its target circle; injectivity is neither true nor needed. The actual ray direction is B-s pi for a plus corner and B-(s-1)pi for a minus corner. Consequently it is B modulo pi.

Taking the reversed terminal ray minus the initial ray defines K modulo n-2. Directly tracking orientation in the final developed polygon gives the parity formulas above: in a plus polygon the reversed terminal ray has corner parameter pi-beta; in a minus polygon it has parameter beta-2t. This proves K equals the source type. For a diagonal, its initial B is (n-2-k)t and its reversed terminal B is (k+1)omega+kt, whose difference is exactly k pi.

The common-offset requirement in [R, Lemma 2.5] matters when n is even and there are two vertices. An arbitrary affine map has not been assumed to preserve K. For the specified generators it is checked:

- Central symmetry sends (epsilon,s,phi) to (-epsilon,s,phi), with unchanged B.
- The even-n rotation sends s to s-1, shifting B by -omega; its direction lift differs by the same constant at each vertex.
- For n=2m+1 the pi/n rotation exchanges polygon copies and sends s to s+m, shifting B by m omega, with m omega-t=(m-1)pi.
- The bisector reflection sends B to omega-B and hence K to -K.

The side pairings respect these maps. Composition and inverse preserve uniformity. The ray-lift identity F(x+pi)=F(x)+pi then proves invariance of K for the orientation-preserving generators. Keeping actual corner rays throughout prevents an unjustified inference from equal holonomy directions to equal rays at a cone vertex.

## 3. Cylinder geometry, finite length sets, and descent

For a strip bounded by XaX_(a+j) and X_(a+1)X_(a+j-1), 2<=j<=n-1, attach its negative through side XaX_(a+1). Point reflection in that side's midpoint makes the two pieces a parallelogram. The other two side edges identify by translation along the chord direction. Therefore the quotient is a cylinder with

h=sin((j-1)t),
ell=lambda_(j-1)+lambda_(j-3)=lambda lambda_(j-2),
ell/h=2cot(t).

The two vertex lift families on each boundary are exactly the two original endpoints plus integer multiples of ell in the chord direction. For j=2 the inner chord collapses to a point and its two families coincide. For j=n-1 the outer chord is an original polygon side; its two occurrences on the quotient boundary are still separate occurrences for the strip chart. Neither degeneracy destroys the cylinder or its local half-disk.

This establishes the crossing argument geometrically. At a boundary occurrence of a vertex, the cylinder contributes a flat half-disk, of angle pi. Every ray obtained from the oriented boundary edge by a turn of strictly less than pi toward the cylinder enters that same half-disk. In the universal strip the transverse coordinate is affine along a straight geodesic. A segment that enters and eventually ends at a vertex must cross the entire height. If its total transverse displacement equals the height, it ends at an opposite-boundary vertex lift. Conversely, a segment between opposite-boundary lifts has interior in the open cylinder and is a saddle connection.

All base-direction cylinders have the common modulus 2cot(t). The shear of this coefficient makes an integral full twist in each; it is identity on each boundary and has the same derivative in every chart. The maps glue, including at conical vertices. It fixes every base-direction boundary ray, so its B-offset is zero at every vertex. Thus twists preserve K and actual base rays, not only their planar directions.

The finiteness argument in [R, Lemma 2.11] is valid; its short angular sentence can be made particularly concrete. Normalize the middle crossed side to [(0,0),(1,0)]. If both adjacent side pairs turn around the same endpoint, the first and third rays from that endpoint have directions -omega and +omega. Since omega>=pi/2, their points have nonpositive first coordinate. A chord between them cannot meet the positive interior of the middle side. If they turn around different endpoints, their side segments have forms a(cos omega,-sin omega) and (1,0)+b(-cos omega,sin omega), 0<=a,b<=1. The horizontal separation is at least 1. The remaining case involves nonadjacent sides in a compact convex regular polygon and has a positive minimum distance d0. Every two successive crossing intervals therefore contribute at least min(d0,1) length. A length bound bounds the number of crossed sides; finitely many chains and endpoint labels then give finitely many saddle connections. Boundary-running base trajectories are already finite sides or diagonals.

A non-base direction lies between kt and (k+1)t. In that frame its vector has y>0 and x>y cot(t). The inverse twist changes x to x-2y cot(t), reducing its absolute value and hence length strictly. Finiteness, rather than strict decrease alone, proves termination. A terminal base ray from a polygon vertex meets another vertex within that polygon; it is a side or diagonal. The explicit rotations and central symmetry move its actual initial corner to (+,0), and they identify the two side representatives. This establishes exactly the portion of Theorem A needed by D/F, without relying on the claimant's experiments or an uninspected external theorem.

## 4. Theorem D: four points, second cylinder, and the initial corner

Let u=g xi and v=g eta. Reachability and det(u,v)=S>0 place the two initial rays in the same original corner, with the ray of u clockwise from the ray of v by an angle less than pi. An orientation-preserving affine map takes this actual ray interval to another interval of angle less than pi; this is stronger than ordering directions modulo pi.

Choose a type-preserving affine map psi taking delta_k=OX_(k+1) to the connection of v. The pulled-back u connection enters the right cylinder of delta_k. Its transverse displacement is S/lambda_k; that cylinder has height sin((k+2)t). Therefore

sin(t)sin(2t)>=sin((k+1)t)sin((k+2)t).

For 0<=k<=n-3 this is cos((2k+3)t)>=cos(3t), leaving only k=0 or k=n-3, with equality. Equality also forces the pulled-back connection to join opposite-boundary vertex lifts.

The k=n-3 exclusion is genuinely geometric. Here the first strip is the triangle X_(n-2),xi,O; its opposite boundary consists of its collapsed vertex and the negative copy of the long diagonal. The extra reachable point gX_(n-2)=v+(lambda^2-1)u pulls back to a ray in the same clockwise interval. Its total transverse displacement is (lambda^2-1)sin(t), larger than the first height sin(t). It cannot leave at a vertex, which would be an illegal intermediate vertex of the supposed short connection. It therefore crosses the interior of the negative long diagonal into the cylinder built from the strip between OX_(n-2) and X1X_(n-3). That cylinder's height is sin(3t). The remaining transverse displacement is

(lambda^2-2)sin(t)=sin(3t)-sin(t),

strictly between zero and sin(3t) for every n>=5. It cannot reach a vertex in that cylinder. This is a contradiction, including n=5 where the adjacent strip ends at a side. No alternate vertex or boundary exit is omitted.

Thus v has type A0. Applying the sector-bisector reflection on both sides of g repeats the argument for u; the extra hypothesis then used is gX2. This accounts for exactly the four stated reachable vertices, without using all vertices prematurely.

For k=0 the right cylinder has height S and circumference lambda^2. The opposite-boundary lifts are xi+t' eta with t' in lambda^2 Z or lambda^2 Z-1. Full twists send the first family from the side xi and the second from delta_1; their types are 0 and 1 respectively. These are distinct modulo n-2. The pulled-back u, being A0, selects the first family. Composing psi with the appropriate integer twist gives an affine map Psi taking both side saddle connections to the specified connections of u and v. Its derivative equals g because it agrees on the basis xi,eta.

Finally the complete ray interval between the two initial sides maps into the interval between the two reachable rays inside (+,0). Every diagonal image therefore starts in the correct original corner. This proves actual reachability, not only existence of a saddle connection with the right vector somewhere on the double polygon. K then yields the vertex type order. The unitary-pair converse follows from this same exact-height and endpoint-family argument with both endpoints already A0.

## 5. Theorem F: common integer, boundaries, and obstruction

### Infinitude for A0

Choose an affine map taking the side eta to the connection of an A0 point w. Side-cylinder twists give A0 connections with vectors u_i=A xi+i lambda^2 w and determinant S against w. For w different from xi, arg(w)>0. Their actual initial rays approach w from the clockwise side within a fixed interval shorter than pi, so for sufficiently large positive i they lie in (+,0). The unitary-pair result gives reachable polygons. They are distinct because their side vertices at the fixed origin are distinct. The remaining boundary point xi follows by the sector reflection. No inference that every holonomy vector is automatically reachable is used.

### Common twist and uniqueness for other types

For 1<=k<=n-3, write X_(k+1)=a eta+b xi, where

a=lambda_k sin((k+2)t)/S,
b=lambda_k sin(kt)/S.

Both are positive. Fix Psi(delta_k)=gamma_w, and set u=g xi, v=g eta for its derivative g. If a reachable g'P contains w, D fixes its index at k+1. Pulling back its left side vertex uses the left cylinder of delta_k, of height sin(kt) and circumference lambda lambda_(k-1). Exact height forces an opposite-boundary endpoint. The families based at X1 and Xk have types 0 and k-1. For k>=2 only the X1 family is A0; for k=1 the two geometric endpoint families coincide at X1. Thus v'=v+i c1 w for an integer i and c1=lambda lambda_(k-1)/lambda_k.

The right cylinder has height sin((k+2)t) and circumference lambda lambda_(k+1). Its endpoint families based at xi and X_(k+2) have types 0 and k+1. For k<=n-4 only the xi family is A0; for k=n-3 both are the same point xi. Thus u'=u-i' c2 w for an integer i' and c2=lambda lambda_(k+1)/lambda_k. The minus sign is a choice of integer indexing, consistent with opposite transverse sides.

The integers are not assumed equal by a vague global-twist assertion. The exact vertex equation a v'+b u'=w=a v+b u gives a i c1=b i' c2. Since

a c1=b c2=kappa=sin(kt)sin((k+2)t)/sin(t)^2>1,

it follows that i=i'. The bound is uniform: the sine product is minimized at k=1 or k=n-3 and kappa>=sin(3t)/sin(t)=lambda^2-1>1 for n>=5. This explicitly includes both endpoint values of k.

If the original polygon was reachable, u and v have nonnegative xi/eta coordinates. For i>=1 the xi coordinate of u' is

(1-i kappa) f_xi(u)-i c2 a f_xi(v).

Both coefficients are strictly negative, so nonnegativity forces both coordinate values zero, contradicting det(u,v)=S. For i<=-1 use the eta coordinate of v' in the same way. Thus i=0 and there is at most one polygon. In particular X2 lies only on the initial polygon.

### Explicit obstruction for every n

The source's ray tracking for w_n is sound. The diagonal D in the negative polygon from -X1 to -xi is the image of delta_(n-3) under central symmetry composed with a polygon rotation, so has K=n-3. Its initial ray lies in the immediately following corner (-,1), a counterclockwise angle omega from r0=(+,0,t). The twist in direction t fixes r0 and its next antipodal ray r_pi and preserves the ray interval between them. Its image has vector w_n and direction strictly between t and omega, hence lies in the correct original corner within that interval. This eliminates any cone-sheet ambiguity.

In xi/eta coordinates put L=lambda^2 and d=X_(n-2)=(L-1,1). The twist and preceding isometry have respective derivative matrices

T=((2-L,(L-1)^2),(-1,L)),
R=((0,-1),(1,2-L)).

They both have determinant 1. Direct multiplication yields T(eta-xi)=w=(L^2-L-1,L+1), and g0=TR sends d to w. For k=n-3 the common-integer lemma gives c1=L-1 and c2=1. A reachable polygon through w would have side vectors g0 xi-iw and g0 eta+i(L-1)w. Their eta coordinates are

L-i(L+1),
-(L^2-2L-1)+i(L^2-1).

Since L>=4cos^2(pi/5)=(3+sqrt(5))/2>5/2, the first nonnegativity condition forces i<=0 and the second i>=1. Contradiction. The subscript lambda_4 in the source is a diagonal length, with lambda_4=lambda^4-3lambda^2+1; it has not been confused with the fourth power in this calculation.

## 6. Independent three-segment development and n=6 obstruction

These checks independently verify the witness and conflict; they do not merely repeat the affine-orbit conclusion.

### Uniform development

Let A=X_(n-3)=((L-1)(L-2),L-1), d=(L-1,1), and w=(L^2-L-1,L+1). Consider the copies

P, A+d-P, A+d-xi+P.

The first side reflection is across [A,d], and the second across the copy [A+d-xi,A+d] of [xi,0]. With r1=(L-1)/(2L-1) and r2=L/(L+1), exact identities give

r1 w=A+r1(d-A),
r2 w=A+d-xi+r2 xi,
w=A+d-xi+d.

For L>5/2, 0<r1<r2<1; the difference is (L^2-L+1)/((L+1)(2L-1)). Both collisions are strictly internal to sides. In the first and third polygon a segment runs between a vertex and the interior of a nonincident side; in the middle it joins interiors of two distinct sides. Strict convexity puts their open parts inside their respective polygons. There is no intervening vertex, so the billiard has exactly three segments. The last plus-polygon vertex index is n-2, giving odd-N type k=n-3. Independently, using eta=-zeta^(-1) and L=2+zeta+zeta^(-1) gives w=2+3zeta+zeta^2.

The check program verifies these identities exactly as rational functions/polynomials. A separate numerical reconstruction from regular-polygon edge vectors checks the geometry for n=5 through 40 and n=64,100,257,1000; these are finite diagnostics only. The uniform proof is the identities plus convexity, not extrapolation from the tested values.

### n=6 without the all-n argument, and even without type ambiguity

Fuchs's lattice basis is xi=(1,0), eta=(-1/2,sqrt(3)/2), and the initial hexagon's coordinates are (0,0),(0,1),(1,2),(2,2),(2,1),(1,0). Tile vertices satisfy p,q>=0 and p+q not equal to 2 modulo 3. The reachable-point criterion is gcd(p,q)=1, or gcd=2 and p+q=1 modulo 3, with the tile-vertex restriction retained [F, journal p.506]. Thus w6=(5,4) is reachable. Its source type is A3, but the obstruction can be proved independently of the angular interpretation.

Any reachable hexagon has side vectors v=v1 and u=v5 with det(u,v)=1 and interior vertices 2v+u, 2v+2u, v+2u. Reachability of the even middle vertex forces sum(u)+sum(v)=2 modulo 3. Neither side endpoint has coordinate sum 2 modulo 3; hence both have sum 1 modulo 3. Since w6 has sum 0 modulo 3, it cannot be either side endpoint. Its odd first coordinate excludes the middle vertex.

At position v4=v+2u, write u=(a,b). Nonnegativity gives 0<=a,b<=2, while det(u,w6)=4a-5b=1. The integer solutions are (4,3)+j(5,4), and none lies in that box. At position v2=2v+u the only determinant-one nonnegative candidate is v=(1,1),u=(3,2), neither a tile vertex because its coordinate sum is 2 modulo 3. Therefore there is no reachable hexagon through (5,4), without using D, F, the double polygon, or a resolution of the source's A0 shortcut. The exact finite enumeration checks every nonnegative possibility, with bounds justified by the positive vertex coefficients. It also checks the mirrored point (4,5) and uniqueness for (1,2).

The paragraph on [F, journal p.509] headed as proofs of 2.4 and 2.5 starts with an A0 unitary pair and only classifies points on u+tv. It contains no argument producing a polygon through every other reachable point. Its conclusion cannot imply the missing statement, as the same source's lattice formulas give the obstruction above. Its arithmetic step and offset are 3 and 2, respectively; these equal lambda^2 and lambda^2-1 for n=6, not the printed lambda+1 and lambda. This audit does not accept the full Theorem E, but this local mismatch is sufficient to explain why the heading is not competing evidence against F.

## 7. Check coverage, limitations, and disposition

The independent checks cover exact witness identities and obstruction matrices, complete bounded n=6 enumeration, exact rational corner cycles and diagonal parity for n=5 through 80, and explicitly finite geometric/coefficient diagnostics. Normal, -O, and -OO runs all pass. No Python assertion is used, so optimization does not strip tests. Negative controls detect the wrong witness endpoint, wrong twist sign, wrong type, reversed determinant sign, and unconditional A0 shortcut. These checks support, but do not formally certify, the preceding geometric argument.

No hidden unresolved source convention changes the fixed-origin problem. The only necessary qualification is that the source's mutually inconsistent shortcut cannot be true simultaneously with its parity rule and diagonal labels. The latter specify a unique coherent classification, used consistently in D/F and in this acceptance. The bare existence refutation already follows from the original n=6 lattice geometry independently of that qualification.

No author-code execution was performed in either original audit. This edition contains the complete focused acceptance of existing attributed arguments and public verification metadata. Third-party renderings and raw evidence are excluded. Its exact eight-file inventory is recorded in MANIFEST.json.
