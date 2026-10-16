# PR209 /5100015: root mathematical audit, preliminary checkpoint

UTC 2026-10-16 04:43. Best estimate: 15% of the complete case. This is a proof audit and reproducibility checkpoint, not a priority finding, preprint clearance, or merge acceptance.

The authenticated head is `fd09a95b479f376234835a4494693bb1316c85ec`; original PROOF SHA256 is `4f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2`. All 23 native source files, all 16 entries of the author freeze, and all four inherited review-manifest entries match before and after isolated reproduction. The original source has not been edited.

## Claim and scope

For a fixed nondegenerate strictly nested confocal pair of ellipses, take a closed Euclidean billiard polygon. Intersect consecutive tangents to the outer ellipse to form its outer polygon. Project the common center O orthogonally onto those tangent lines to form the outer polygon's center pedal. Their ordered signed shoelace area product is constant over the fixed billiard family when its listed period is not divisible by four. Primitive star winding classes and repetitions require explicit treatment. Hyperbolic and degenerate caustics are outside the primary source's confocal-ellipse family; a circular extension must have a separate argument.

These are actual tangent-line intersections and feet. Feet on original billiard chords or sorted spatial vertices do not define this target. Finite constancy tests alone need not distinguish such constructions.

## Root reconstruction of the universal analytic chain

Put the caustic axes alpha>beta>0, modulus k=sqrt(alpha²-beta²)/alpha, k'=beta/alpha, K=K(k), K'=K(k'). For primitive period N and winding tau coprime to N, reverse orientation if necessary to put 0<tau<N/2 and v=2tau K/N in (0,K). Stachel's classical parametrization gives

    a=alpha dn(v)/cn(v), b=beta/cn(v),
    P(z)=(-a sn(z), b cn(z)), P_i=P(u+2iv).

The outer and caustic focal differences agree. Every required real cn(v), dn(v), and a²-(a²-b²)sn²(z) denominator is nonzero. Coverage of this parametrization is a classical input, not a new assertion proved by the finite checker.

Define f(t)=sn(t)cn(t)/dn(t) and T(u)=sum_i dn(u+2iv). Jacobi addition gives the endpoint determinant for H(z)=(A sn(z),B cn(z)), with the coordinate signs chosen consistently:

    det(P(z-t),P(z+t))=ab f(t)[dn(z-t)+dn(z+t)].

The signs are positive for the stated P. Summing gives area(P)=ab f(v)T(u). For the ordered edge-vector polygon D_i=P_(i+1)-P_i, determinant bilinearity gives

    area(D)=2area(P)-1/2 sum_i det(P_i,P_(i+2))
           =ab[2f(v)-f(2v)]T(u).

This calculation uses the indexed sum directly and does not assume that stepping by two gives one cycle. It remains valid for even periods and stars. Evaluating the caustic contact at the midpoint phase and applying ellipse polarity gives

    A'=(a²b²/(alpha beta))f(v)T(u+v).

The actual foot of O on the tangent at P(z) is

    Q(z)=(-ab²sn(z),a²bcn(z))/(a²-(a²-b²)sn²(z)).

With w=K-v, classical quarter-period identities give dn(w)=b/a and cn(w)=k' sn(v)/dn(v)>0. Adding P(z-w) and P(z+w), then using P(z-2K)=-P(z), gives the pointwise identity

    Q(z)=L[P(z+K-v)-P(z+K+v)],
    L=diag(b/a,1)/(2cn(w)), det L=b/(4a cn²(w)).

This is the negative of an ordered edge-vector polygon followed by one fixed linear map. The global minus has determinant +1 in the plane. Hence

    A'_O=b²[2f(v)-f(2v)]T(u+K-v)/(4cn²(w)),
    A'A'_O=C T(u+v)T(u+v+K),
    C=a²b⁴ f(v)[2f(v)-f(2v)]/(4alpha beta cn²(w)).

The phase alignment uses T(z+2v)=T(z). No division by an area is involved. C has length dimension four, as does the area product.

For q=N/gcd(N,2), r=N/q, primitive arithmetic reduces T=rU where

    U(z)=sum_(h in H) dn(z+h), H={2Kj/q:0<=j<q} mod 2K.

The relevant q is odd exactly when N is not divisible by four. On the compact torus with periods 2K and 4iK', U has at most simple poles, evenness, and imaginary anti-period 2iK'. At c=K+iK', evenness and anti-periodicity give dn(c+t)=-dn(c-t). Odd H contains no K modulo 2K, so every summand at c is finite and pairing h with -h proves U(c)=0. The self-paired h=0 is a zero, not a pole.

At every possible pole p of U, the partner U(p+K) is holomorphic and zero, by real subgroup translation and imaginary anti-periodicity. Conversely, at a pole of U(z+K), U(z) is holomorphic and zero. The two pole sets are disjoint because H has odd order. Thus U(z)U(z+K) has only removable singularities and is constant on the torus. The real value U(0)U(K)>0 fixes its nonzero value. This proves the required trace product, with the r² multiplicity retained.

Reversal changes both signed areas' signs. Repeating a primitive traversal multiplies both areas by the repetition count. An admissible listed period cannot have a primitive divisor divisible by four. N=2 would require a center-crossing caustic-tangent chord and is impossible for a strict inner ellipse. The k=0 circle is handled by rigid rotation, not by applying the nondegenerate complex-torus argument at a collapsed modulus.

Root has found no algebraic or meromorphic gap in this chain. Final mathematical acceptance is withheld until the three newly assigned family reports and their evidence are sealed, read in full, and reproduced.

## Actual reproduction and additional exact physical controls

`root_reproduction_01/REPRODUCTION.json` records genuine isolated runs of all three inspected scripts. Author verification reproduced every field and the exact saved output bytes: 5,660 exact assertions and 4,512 high-precision diagnostics. The inherited checker reproduced every field and exact stdout bytes: 6,195 exact assertions and 6,615 diagnostics. The exploratory probe also exited successfully. Scientific Python was used with -B; there were no installs, network calls, shared database writes, or original-file writes.

`root_exact_geometry.py` passes 340 exact assertions for six explicit closed polygons in x²/4+y²=1, checking every edge's common-caustic tangency, interior contact, every vertex's forward Euclidean reflection, actual tangent intersections, and actual perpendicular feet. Two separately constructed triangles share lambda=(8sqrt(13)-20)/9 and product (57+15sqrt(13))/2. Two excluded four-period orbits share lambda=4/5 but give products32 and50. Two author six-period witnesses (credited through the original submission to PR148) share lambda=4/9 and both give product40; here their physical closure/reflection/caustic hypotheses are checked in addition to their area values. Reversal and triple repetition are exact checks. These six finite polygons do not prove the universal result, and high precision is not interval certification.

## Independent approach families and remaining gaps

| Family | Mechanism | Current evidence | Status and exact remaining gap |
|---|---|---|---|
| Source/domain | Freeze exact primary statement and geometry before inherited proof | Independent source Table4 and Stachel checks; ellipse domain confirmed | Report and complete source/control evidence not yet finally accepted by root |
| Physical geometry | Cartesian reflection/caustic dynamics and direct tangent-line/foot construction | Independent freeze; direct algebraic pedal/edge transformation derived | Final programs, negative controls, failed probes, and universal-versus-finite limits still to read/reproduce |
| Meromorphic divisor | Independently derive direct-area elliptic functions and complementary pole divisors | Independent freeze; direct-area divisor and trace attacks report no defect | Final proof, all pole/phase cases, and complete evidence still to read/reproduce |
| Root | Reconstruct submitted identities and pole cancellation; replay frozen scripts; exact Cartesian polygons | Full proof algebra audit, exact original-output reproduction, 340 new physical assertions | No historical priority conclusion; all fresh family reports pending root acceptance |

The historical status/review/readiness files remain provenance evidence rather than current authority. One read command initially sought record_receipt.json at the attempt root; it actually resides at sources/record_receipt.json and was then read successfully. This path error did not execute submitted code or alter scientific evidence.

No priority audit, paper preparation, Zenodo action, spreadsheet action, native PR edit, or merge has occurred for PR209 at this checkpoint. Counts remain44 completed /21 preprints /21 merges /0 pending tracker; the overall goal remains active and incomplete.
