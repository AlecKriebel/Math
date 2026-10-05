# Three-period focal equality and multiplier: an explicit old-results implication

This deduction is independent of the accepted all-period focal-pole proof. It
closes the restricted N=3 implication gap in both historical reviews. Its inputs
are pre-2026 published geometric results, not a located older explicit statement
of the target focal theorem. It removes any separate triangular novelty claim.
Independent adversarial verification closed on 2026-10-05. ROOT authenticated all 60 sealed payloads and 21 external input bindings and freshly replayed the independent exact, phase, and primary scalar-power checks. Zero mandatory findings remain for this restricted conditional deduction; it removes a triangular novelty claim and grants no all-period priority or publication clearance.

Let the boundary axes be a>b>0, X=a², Y=b², c²=X−Y, and
D=√(X²−XY+Y²). Set n=X−D>0, m=D−Y>0 and
ρ=r/R=2mn/(X−Y)². A triangular billiard has incenter I, circumcenter O,
circumradius R, inradius r. Its outer tangent triangle is its excentral triangle:
reflection makes the boundary tangents external angle bisectors. Its circumcenter
is the Bevan point H=2O−I, its radius is 2R, and its area is 2/ρ times the
original area. The direction H=2O−I is essential; reflecting O in I would be wrong.

The inspected 2021 IMPA book, Theorem2.1 printed13–15, gives the incenter
locus axes m/a,n/b with its supplied parametrization/CAS proof. The inspected
Helman–Laurain–Garcia–Reznik arXiv:2102.09438v4, section3.4 PDF6–7, gives
circumcenter locus axes n/(2a),m/(2b); its section3.5 Proposition5 PDF7–8
gives the Bevan-circle center power. The preceding original circumcircle power
and ρ are also proved in Garcia–Reznik–Koiller arXiv:2001.08054v3, Theorems1
and3 and the IMPA book Theorem2.3. Specifically,

    R²−|O|²=D,       4R²−|H|²=X+Y+2D.

These supplied old statements and their relevant proofs were directly read.
The source's CAS summaries are not advertised as a separately reproduced
full general vertex CAS certificate here; the priority deduction is conditional
on these published geometric theorems, whose hypotheses match real noncircular
elliptic triangular billiards. The familiar Euler relation gives
|O−I|²=R²−2Rr. Combining it with H=2O−I and the two powers yields

    |I|²+4ρ|O|²=X+Y−4ρD,
    4O·I−|I|²=X+Y−2D.

Write u=O_x², v=I_x². The two locus equations give

    |I|²=n²/Y + v(1−X n²/(Y m²)),
    |O|²=m²/(4Y) + u(1−X m²/(Y n²)).

Substitution in the first displayed relation, reducing D²=X²−XY+Y²,
gives α(v−4m²u/n²)=0, where α=1−X n²/(Y m²)>0. Indeed its numerator is

    Y m²−X n²=2(X−Y)[D(X+Y)−X²−Y²]>0;

the last sign follows from
D²(X+Y)²−(X²+Y²)²=XY(X−Y)²>0, with both compared quantities positive.
Consequently I_x²=4m²O_x²/n².

The coordinates are real analytic on the connected real phase circle: the
triangle stays nondegenerate and its side lengths are positive. Since
(I_x−2mO_x/n)(I_x+2mO_x/n)=0 identically, analytic continuation fixes one
sign globally; O_x is not identically zero. At the major-axis-vertex symmetric
phase, O_y=I_y=0 and O_x=n/(2a)>0. The latter follows directly from
R²=(a−O_x)² and R²−O_x²=D. The incenter locus gives |I_x|=m/a. The second
power relation forces O_x I_x=−nm/(2X), because
X+Y−2D+m²/X=−2nm/X. Hence the global sign is negative:

    I_x=−2m O_x/n,       H_x=(2+2m/n)O_x.

Let U=D−c²>0 and V=X+Y+2D−c²=2(Y+D)>0. The same algebra gives

    2+2m/n=V/U.

U>0 since D²−(X−Y)²=XY>0. By Querret/Sturm's signed triangle formula,
the focal pedal areas of the original and excentral triangles are, respectively,

    A±=[T](U±2cO_x)/(4R²),
    B±=[T](V±2cH_x)/(8ρR²).

Both foci lie strictly inside both triangles, so all factors are positive for
positive orientation. Substituting H_x=(V/U)O_x proves

    B±=V/(2ρU) A±.

The multiplier is positive and independent of phase. Thus both E and M on
the entire primitive N=3 subdomain are explicit short consequences of old
results, even though a prior explicit focal statement was not located. Reversal
and repetition follow by signed scaling. This deduction says nothing about
odd primitive N≥5 or an all-period M theorem.

The exact rational coefficient identities were freshly checked by
root_triangle_priority_bridge_v02.py, native run root_triangle_priority_algebra_actual002.
At squared axes21,16 it gives exactly125/24. The first run is retained with
exit1: four central identities passed, then an incorrectly transcribed ancillary
factorization failed. Version02 corrects that factorization and adds its exact
strict-sign squared comparison; all six algebraic residuals are zero. Neither
run is represented as a prior author's computation or as a proof by sampling.

Exact primary files and native acquisition/extraction custody are in the closed
focal route's SOURCE_CUSTODY.json and FINAL_SEAL.json. Unavailable journal finals
remain coverage limits, but cannot support a separate N=3 novelty claim after
this old-results implication. ROOT must still adjudicate full-domain priority.

## Closed adversarial review and primary-source qualification

The new adversary froze criteria before candidate access. Its rational parameter t=m/n>1 independently gives X/Y=t(t+2)/(2t+1), rho=2t/(t+1)^2, and M=(t+1)^3/(2t). It proves strict focal positivity through U^2-c^2 n^2/X=Y^2(2t+1)/(t(t+2))>0. A general signed triangle identity and the actual squared-axes(21,16) billiard were checked exactly. Fifty-four actual caustic-tangent billiards at 90 digits, including t=1.00000001 and t=10000, reproduce all center/locus/reflection/multiplier predicates; these are finite noninterval diagnostics. ROOT independently reproduced the full native outputs byte for byte at 2026-10-05T00:38Z.

The inspected arXiv:2001.08054v3 p9 has a faulty printed isosceles example and ancillary reciprocal-Cayley/area-ratio prose. ROOT inspected its facsimile and reproduced its nonzero caustic/circumcircle residuals with an explicitly expected exit1; the unchanged error evidence is retained. That example is not used as a proof certificate. The scalar power algebra in arXiv:2102.09438v4 pp7-8 was independently reproduced exactly, while generic old vertex-CAS proofs of all locus/ratio inputs were not fully replayed. Accordingly this remains a deduction conditional on the stated older geometric theorems, and no claim that every printed old proof line is correct is made. The inspected triangular v3 header is dated12 December2021; its internal July2020 title date is not used to backdate the v3 wording. All decisive input statements are pre2026.

The closing seal descriptor is self-generated before its final manifest, not a native process-completion receipt. ROOT instead verified the actual final bytes and read-only modes. An initial ROOT custody parser assumed that descriptor had an ordinary run schema and failed; its new version handles the declared distinction and passes. Both attempts remain retained.
