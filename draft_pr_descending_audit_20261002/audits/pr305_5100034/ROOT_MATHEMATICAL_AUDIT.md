# PR305: exact mathematical acceptance of the corrected focal-pedal assertion

Original submission: `cc083024dbd00de06ad444cd4070f51f60d209eb`, problem 5100034,
submitted `claimed_solved`, author turn `1/5`. This audit does not change that
historical turn count. Candidate proof SHA-256:
`1abb4eaea5ef795f056ea89636defc99eb48f526cd20012b70d663cbeb2c4a34`.

## Exact claim and falsifiable criteria

There are two distinct mathematical questions. The displayed equality E is
`A+/A- = B+/B-`, where A denotes the signed focal pedal area of the original
chord polygon and B denotes that of its outer tangent polygon. It is arXiv
2004.12497v11 Table 7 k606, printed p.9, and the 2021 journal Table 7 k607,
printed p.349. The proposed stronger assertion C says that the common focal
ratio is constant over the fixed billiard family. C is explicit in the imported
record and strongly encouraged by both primary articles' invariant terminology.

ROOT read both complete primary target editions and visually checked both table
pages. The imported record and its historical report were recovered read-only
from the versioned cache, match the submission's exact declared hashes, and
match the authenticated cached dataset revision. Neither the old open-status
mark nor that report is evidence of current historical priority.

Accepted domain: a noncircular outer ellipse, a strictly nested nondegenerate
confocal elliptical caustic, and a primitive closed billiard of least period
N>=3, with all coprime convex/star turning numbers. All areas use ordered signed
shoelace sums, and perpendicular feet lie on supporting lines. Reversal and
positive integral repetitions are derived extensions. Hyperbolic or collapsed
caustics, two-period diameters, unsigned lobe sums and segment-clamped projections
are excluded explicitly. The circle case is a separate elementary observation.

The acceptance test was a universal proof of E with every real denominator
justified, plus exact resolution of C, rather than finite numerical agreement.
Three independent families froze criteria and source-only routes before reading
the candidate: meromorphic analysis, direct reflection geometry, and source
fidelity. Their full reports were read by ROOT, their closed file sets and modes
were authenticated, and their scientific programs were replayed afresh.

## ROOT's local-to-global derivation

Scale the caustic major semiaxis to 1. Set k in (0,1), k'=sqrt(1-k^2),
v=2K*tau/N in (0,K), delta=2v, a=dn(v)/cn(v), b=k'/cn(v).
Stachel's published Theorem 4.3 and equation (4.9), printed p.1614, give
P(u)=(-a sn(u), b cn(u)) and the increment delta. ROOT independently read
the theorem, its proof and the preceding canonical-motion discussion, and
visually checked the theorem page. The currently fetched version-of-record
has different PDF bytes from the absent old Stachel copy; content verification
is recorded honestly rather than claiming byte identity. A nearby printed
dn real-period sign error is not used; dn(u+2K)=dn(u) is the correct identity.

The caustic chord through P(u-v),P(u+v) has equation
(-sn(u),cn(u)/k') dot X = 1; this follows directly from Jacobi addition.
The outer tangent at P(u) has normal (-sn(u)/a,cn(u)/b). Projecting F+=(k,0)
onto these actual lines gives

    q(u) = ((k-sn(u))/(1-k sn(u)), k' cn(u)/(1-k sn(u))),
    Q(u) = (a(k-a sn(u))/(a-k sn(u)), ab cn(u)/(a-k sn(u))).

The chord area A(w) uses q(w+v+i delta); B(w) uses Q(w+i delta).
The different phases are essential. The real denominators are bounded below
by 1-k and a-k, respectively. Central inversion gives A-(w)=A(w+2K)
and B-(w)=B(w+2K), with no area sign change.

Both cyclic traces have periods 4K and delta, so Bezout gives their common
real period L=4K/N for every primitive period. A shift by 2iK' fixes sn,
negates cn, and reflects each foot polygon in the x-axis; therefore both
traces negate. Their common compact torus has periods L and 4iK'.

Common Jacobi poles are removable in both maps. Put r=K+iK'. The remaining
q denominator has its unique double root at r on the sn torus. The quarter
shifts make q(r+z) even and give leading vector (2/k)(1,i)/z^2. Its regular
neighbors combine as q(r+z+delta)-q(r+z-delta), an odd holomorphic vector.
Thus the two incident determinants have at most a simple pole. Primitivity
gives only one singular original-foot vertex at a phase. Neighbor expressions
at common Jacobi poles, including delta=K, are removable.

The Q denominator has exactly the two simple roots r-v,r+v, since sn has
degree two. At both, its numerator is (-ab^2/k)(1,i), while the denominator
derivatives are opposite nonzero values +/-b^2 sn(v). The residues are
opposite and collinear. There are exactly two adjacent singular outer-foot
vertices. Their common edge's quadratic principal part is det(R,-R)=0;
every other incident edge has at most one singular endpoint. This includes
N=3 and the cyclic closing edge, and does not assume separated poles.

Consequently both area traces have only the two possible simple poles
K-v+iK' and K-v+3iK' modulo the common lattice. No higher principal part
or further denominator root remains.

For either ellipse, a focus lies strictly inside it. Its foot vector relative
to the focus is a positive multiple of the outward normal. For the normal
n(u)=(-sn(u)/R,cn(u)/S), det(n,n')=dn(u)/(RS)>0. The lifted normal angle
advances exactly pi in a length 2K, so every consecutive increment delta
lies strictly between zero and pi. Each consecutive focus-relative determinant
is positive, including the lifted closing edge of a star. Translation leaves
shoelace area unchanged. Thus all four real areas are strictly positive,
and the two meromorphic traces are nonzero.

If one possible pole of a trace were absent, its imaginary anti-period would
remove the other. Compactness would make it constant and the anti-period
would force zero, contradicting positivity. Both first residues are therefore
nonzero. Choose C0=res(B)/res(A) at the first pole. Then B-C0 A has no pole
at either listed point, is constant by compactness, and is zero by the
anti-period. Real positivity makes C0 a positive real number. Focus exchange
supplies the identical C0 at the other focus, proving E with no real zero
denominator. For even primitive periods, focus exchange is a real period
and the focal ratio is 1; this does not make repeated odd orbits symmetric.

These deductions reproduce the needed credited PR210 outer-pole and PR261
original-pole/positivity mechanisms locally. Their earlier PASS verdicts or
parity-restricted final conclusions are not premises of this theorem.

## Exact negative resolution of C

The candidate's triangle lies on x^2/21+y^2/16=1, has vertices
(sqrt(21),0),(-3sqrt(21)/5,+/-16/5), and caustic squared semiaxes
189/25,64/25. Exact ellipse incidence, reflection, segment contact,
tangent intersections and perpendicular-foot areas were independently checked.

    A+/- = 84(7sqrt(21)+/-sqrt(5))/625,
    B+/- = 7(7sqrt(21)+/-sqrt(5))/10,
    B+/- / A+/- = 125/24.

All four areas are positive. Central inversion preserves traversal orientation
and the family, but exchanges foci. Its focal ratios are R and 1/R with R>1.
Hence C is false inside the original domain. Independent families also derived
different exact triangles: squared axes (8,5) with multiplier 27/4; squared
axes (8,3) with multiplier 125/8; and two phases of the (2,1) ellipse with
focal ratios 3.5884019759... and 1. These are supplementary independent
falsifications, not numerical substitutes for the exact counterexample.

## Reproduction and precise disposition

ROOT ran all 13 scientific checker programs: the two author programs, two
inherited-review programs, four new meromorphic/source controls, and five new
geometric controls. All native exit codes were zero and stderr streams empty.
Exact author/inherited receipts match their original bytes; all new scientific
outputs match their sealed counterparts (only a wall-clock UTC field differs
in one output). The direct-reflection data contain 117 configurations across
39 primitive families; the complex diagnostics contain 34 cases. Exact and
high-precision evidence, runtime identities and complete streams remain bound
by the root receipts. Numerical calculations are finite NONINTERVAL diagnostics
and do not certify universal bounds or the theorem by sampling.

**Mathematical verdict: E proved, C disproved; no remaining mathematical gap
identified within this explicit scope.** The original problem is resolved only
with this positive/negative split. Do not describe the uncorrected constancy
assertion as affirmatively solved or blame its wording solely on the dataset.
The strongest result is the phase-independent outer/original multiplier at
both foci, together with an exact counterexample to constant focal ratios.

This is an AI-assisted, unrefereed mathematical audit, not human peer review,
a priority certificate, or permission inferred from mathematics to merge or
publish. Historical priority must now be investigated before paper preparation.
Completion estimates: mathematical audit 100%; bounded priority audit 0%;
overall PR workflow 30%. The persistent descending goal remains active.
