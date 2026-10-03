# Independent universal verification of the literal claim

This is a verification after reading the candidate, recorded before historical review/checker semantics. It establishes the exact topological, per-element statement. It neither reconstructs the toroidal remark's intended geometry nor claims novelty.

## Countable common coordinate: complete domains and bounds

Let f_j, j>=1, be any countable family of homeomorphisms of R. Each is either strictly increasing or strictly decreasing: a continuous injection on an interval is strictly monotone. Denote its orientation by epsilon_j in {+1,-1}. A finite nonempty family can be repeated; for the empty family use h(x)=x.

Take r_0=0 and r_1=1. For n>=1 choose r_(n+1)>r_n+1, large enough that f_j([-r_n,r_n]) and f_j^(-1)([-r_n,r_n]) lie strictly inside (-r_(n+1),r_(n+1)) for every j<=n. There are finitely many compact images at each step, so each r_(n+1) exists. This is a countable recursion with no uniform growth or derivative assumption.

On each positive interval [r_n,r_(n+1)], define h by affine interpolation from n to n+1, and set h(-x)=-h(x). At0 the two definitions agree. Adjacent formulas agree at every endpoint, each slope is strictly positive, and r_n>=n tends to infinity. Therefore h is continuous and strictly increasing on the whole line, has limits +/-infinity at the two ends, is onto, and has a continuous inverse. Finite radii cannot cover infinity; the proof uses the entire infinite recursion.

Fix j. For n>=j+1 and r_n<=|x|<=r_(n+1), the forward condition at stage n+1 gives |f_j(x)|<r_(n+2). The inverse condition at stage n-1 gives |f_j(x)|>r_(n-1): otherwise f_j(x) belongs to the closed smaller interval, forcing x strictly inside (-r_n,r_n), contradiction. This also deals with equality endpoints x=+/-r_n. Hence n<=|h(x)|<=n+1 and n-1<|h(f_j(x))|<n+2.

The unique zero a_j=f_j^(-1)(0) satisfies |a_j|<r_(j+1), by stage j. Thus for |x|>=r_(j+1), monotonicity gives sign(f_j(x))=epsilon_j sign(x), including both orientations. Comparing the preceding magnitudes with these signs gives |h(f_j(x))-epsilon_j h(x)|<=2 on both tails. No orientation sign is assumed in the compact core.

If |x|<=r_(j+1), the forward condition at stage j+1 gives |h(f_j(x))|<j+2, while |h(x)|<=j+1. Their signed difference has magnitude <=2j+3. These two regions exhaust R. Setting u=h(x) gives a finite global B_j:=sup_u |h f_j h^(-1)(u)-epsilon_j u|<=2j+3.

For u,v in R set delta_j(u)=h f_j h^(-1)(u)-epsilon_j u. The reverse triangle inequality yields

    ||h f_j h^(-1)(u)-h f_j h^(-1)(v)|-|u-v||
        <= |delta_j(u)-delta_j(v)| <= 2B_j.

Therefore C_j=4j+7 is a positive valid constant. The same h works for every j; it is constructed once before fixing j. The identity causes no issue because constants may be positive upper bounds rather than minimal values.

In fact, for any monotone homeomorphism g of orientation epsilon, its two-point metric defect equals |delta(u)-delta(v)|, where delta(u)=g(u)-epsilon u. This follows by ordering u,v and using monotonicity of g. Thus the literal coarse1 condition is exactly finite oscillation of delta. Finite oscillation is equivalent to bounded signed displacement, since comparison with delta(0) gives a finite absolute bound. This independent characterization confirms that the constructed displacement conclusion is sufficient without changing the target's quantifiers.

There is also a group closure check: for oriented maps a,b within B_a,B_b of their signed identity maps, delta_(ab)(u)=delta_a(b(u))+epsilon_a delta_b(u), so B_(ab)<=B_a+B_b. Inversion preserves the supremum B_a, because delta_(a^-1)(u)=-epsilon_a delta_a(a^-1(u)). Thus a countable generating family suffices as well, and every finite word has a finite bound. No faithfulness or absence of fixed points is used.

## Finite-generator mechanism independently checked

For a finite symmetric set S of increasing homeomorphisms put F(x)=max(x+1,{s(x):s in S}). A maximum attained at x strictly increases at every y>x, so F is continuous and strictly increasing. All constituent functions tend to the appropriate infinite end, so F is onto; F(x)>=x+1 gives F^(-1)(x)<=x-1.

The orbit a_n=F^n(0), n in Z, satisfies a_n>=n for n>=0 and a_n<=n for n<=0. The closed intervals [a_n,a_(n+1)] cover R, with disjoint interiors. Choose any increasing homeomorphism h_0:[0,F(0)] to [0,1]. Define h(x)=n+h_0(F^(-n)(x)) on the n-th interval. Endpoint consistency, continuity, strict increase and unbounded integer endpoint values prove h is a homeomorphism onto R. The formula gives h F h^(-1)(u)=u+1 on all intervals, including endpoints.

We have s(x)<=F(x), and symmetry gives x=s^-1(s(x))<=F(s(x)), hence F^-1(x)<=s(x). Conjugation implies u-1<=h s h^-1(u)<=u+1. Displacements add under composition, giving B_g<=|g|_S and C(g)=2|g|_S+1. A nonsymmetric set would not justify the lower sandwich. Fixed points and the trivial group are harmless.

## Countability of the manifold application without an extra compactness premise

For a connected second-countable manifold choose a countable cover by simply connected coordinate balls U_i. Every overlap U_i intersect U_k has at most countably many path components: it is open and locally path connected, each component contains a basis element, and distinct components are disjoint. Fix one point per nonempty overlap component, and within each U_i fix paths from a chosen center to all such points. This creates a countable graph of centers and overlap connections, with paths mapped into the manifold.

Any loop has a finite subdivision whose subpaths lie in such U_i (compactness of its parameter interval). At each transition, replace the transition point by the chosen point of its overlap component using a path in that component. Simple connectivity of each U_i lets the resulting subpath be homotoped, relative endpoints, to the prescribed center paths. Thus finite loops in the countable graph surject onto pi_1(M). There are only countably many finite edge words, so pi_1(M), and its holonomy image, are countable. This avoids assuming the 2002 statement explicitly says closed or co-oriented, or importing triangulation machinery. For a disconnected manifold use the basepoint component.

Enumerate the holonomy image and apply the countable construction. Compose its h with any initial leaf-space homeomorphism L to R. Pull back C_j along the possibly nonfaithful representation. Atoroidality is not required for this literal topological conclusion. Standard manifolds are second countable; if one enlarged the category to non-second-countable manifolds, this application would need a separate countability hypothesis.

## Falsifying stronger interpretations and missing ingredients

Inverse control is essential: take r_0=0, r_n=2n-1 for n>=1 and f(x)=cuberoot(x). These radii retain r_1=1 and strict spacing r_(n+1)>r_n+1, and meet every forward inclusion. Their odd interpolation is h(x)=x for |x|<=1 and h(x)=sign(x)(|x|+1)/2 outside. At x=(2n-1)^3, |h(f(x))-h(x)|=((2n-1)^3+1)/2-n is unbounded. Thus removing only inverse control breaks the result. Finite-prefix interpolation likewise has linear tails; a dilation then has unbounded signed displacement beyond the last controlled radius. Such finite diagnostics cannot replace the infinite proof.

Orientation reversal must be measured against -u. Reflection has zero two-point defect and zero signed displacement from -u, but unbounded displacement from +u. A decreasing homeomorphism need not be an involution, and the proof does not assume it is.

A group-independent constant fails even after any topological conjugacy for the cyclic action x->2x. Its fixed point0 persists under conjugacy, while for x>0, h(2^n x) tends to the positive or negative infinite end as n grows. Its distance to h(0) diverges, so the additive defect at the fixed pair (h(x),h(0)) diverges across powers. This is a stronger negative control than exhibiting failure in one preferred logarithmic coordinate.

Countability cannot simply be dropped: for any proposed h, the full group Homeo(R) contains f=h^-1 composed with (u->2u) composed with h, whose conjugated two-point defect is unbounded. No common h works for that uncountable group. None of these controls falsifies the literal countable, per-element result.

Bounded displacement itself does not imply Lipschitz regularity. On [n,n+1], n>=1, interpolate through (n,n), (n+1/(n+1)^2,n+1/2), and (n+1,n+1), and set f(x)=x for x<=1. This is a whole-line increasing homeomorphism, with 0<=f(x)-x<=1/2, but its first slope in the n-th interval is (n+1)^2/2, unbounded. This control supports the separation of the countable proof from the stronger published Lipschitz theorem.

## Credited finite-case implication, not an earliest-priority claim

The published DKNP2013 Theorem8.5 supplies the stronger conclusion for finitely generated increasing irreducible actions. For any finitely generated increasing subgroup G, adjoin translations by1 and sqrt(2). The enlarged subgroup is still finitely generated, has no common fixed point, and is minimal because the additive translation subgroup Z+sqrt(2)Z is dense. Restrict its single conjugacy to G. Its per-element bounded displacement implies the required two-point bound by the same reverse triangle inequality. Thus neither a common fixed point nor lack of minimality obstructs the credited finite-case application. The fresh primary read verifies theorem applicability, not every stochastic dependency; the universal deterministic proof above does not depend on that chain. No claim is made that2013 was the earliest proof, or that this article explicitly answered Calegari's numbering. Literature priority of the countable extension is not asserted.
