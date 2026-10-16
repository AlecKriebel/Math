> INERT PROPOSED TEXT: not applied to the native attempt, repository, PR or external record. Root must authenticate the final package and finish whole-package review before use. Replace each UNRESOLVED field only after its fact is verified; retain later merge/current-main fields as unresolved until then. No publication or merge is asserted by this template.

# Five outgoing centers in a 16-realization cube move

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · Unrefereed research note

This is the proposed current proof entrypoint for problem 30004563. It follows the scientific content of frozen `publication_package_v2`, prepared 15 October 2026. The original `CANDIDATE.md`, original `certify_five_centers.py` and `turn2_exact_certificate.json`, and original `review/` remain historical prepublication evidence with their original 10^17 endpoint. This current presentation uses 10^16 and an analytic bound, as does the separately labeled publication verifier/certificate. The result concerns realizations permitting crossings.

## Theorem and precise scope

There exist six fixed distinct algebraic points A1,...,A6 in the plane such that both alternating triples are noncollinear, an incoming center Z makes A1A2A3Z, A3A4A5Z, A5A6A1Z into 16-quads, and at least five distinct outgoing centers X make A2A3A4X, A4A5A6X, A6A1A2X into 16-quads. Every selected center is distinct from every boundary point.

For an ordered quadrilateral PQRS, the 16-quad condition is

|P-Q|^16+|R-S|^16=|P-S|^16+|Q-R|^16.

The example contradicts the at-most-three expectation for construction curves sharing a focus in Melotti--Ramassamy--Thevenin, published Remark 4.8, p.811, and the maximal-three conjecture in the crossing-permitted OWR setting, p.1785. A strict crossing of the fixed boundary excludes proper embeddings. The exact total center count, universal maximum and alpha<1 are not determined.

## Rational data and scalar equivalence

Put A=(0,0), B=(b,0), C=(c,d), with

b=2073/10000, c=4719/10000, d=64/10000, lambda=27/1250, mu=1.

Seek common-focus solutions

|X-B|^16-|X-A|^16=lambda,
|X-C|^16-|X-A|^16=1.                                      (1)

For s>=0 take the nonnegative real eighth roots

u=s^(1/8), v=(s+lambda)^(1/8), w=(s+1)^(1/8),
x=(b^2+u-v)/(2b),
y=(c^2+d^2+u-w-2cx)/(2d),
G(s)=x^2+y^2-u.                                          (2)

These functions are continuous. The coordinate equations have determinant 4bd>0. If G(s)=0, they imply |X-A|^2=u, |X-B|^2=v, |X-C|^2=w, and eighth powers give (1). Conversely (1), with s=|X-A|^16, has exactly these nonnegative roots and these unique coordinates. Hence scalar zeros and geometric solutions correspond bijectively. Distinct s give distinct X; there is no extraneous branch or squaring solution.

Exact rational interval arithmetic establishes:

| s | strict interval containing G(s) |
|---|---|
| 9/10000 | (0.38,0.39) |
| 11/10000 | (-0.28,-0.27) |
| 13/10000 | (0.51,0.52) |
| 1/2 | (-0.91,-0.90) |
| 1 | (9,10) |
| 10^16 | (-4.766,-4.765) |

The intermediate value theorem supplies a zero in each of the five disjoint open intervals between successive cutpoints. Uniqueness within a bracket is not assumed.

At the final endpoint u=100 exactly. Concavity gives, for a>0,

0<(10^16+a)^(1/8)-100 <= a/(8*10^14).

Set x0=b/2=2073/20000 and y0=(c^2+d^2-bc)/(2d)=1249057/128000. Substitution into (2) gives

x0-lambda/(16b*10^14) <= x <= x0,
y0-1/(16d*10^14) <= y <= y0+(c/b)*lambda/(16d*10^14).

Both coordinate intervals are positive. Squaring their rational endpoints and subtracting 100 proves the final row. In particular x0^2+y0^2=39007985196121/409600000000<95.235, and the outward corrections are small enough for the displayed strict interval. This avoids subtracting nearly equal large radicals. As s tends to infinity, v-u and w-u tend to zero, coordinates tend to (x0,y0), and G tends to negative infinity; the fifth center is nevertheless at finite s.

## One fixed admissible boundary

Let J(qx,qy)=(-qy,qx). For q!=0 and the nonzero heights below, define T(q,h,l) as the unique real root t of

|q|^16*[((t-1)^2+h^2)^8-(t^2+h^2)^8]=l.                  (3)

For g(t)=(t^2+h^2)^8, g''(t)=16(t^2+h^2)^6(h^2+15t^2)>0. Thus g(t-1)-g(t) is strictly decreasing; its leading term is -16t^15 and its limits have opposite infinite signs. This proves existence and uniqueness of each boundary parameter, with rational polynomial coefficients.

Define

t1=T(C,10,1), t3=T(B,1,lambda), t5=T(C-B,-10,1-lambda),
A1=t1*C+10*J(C), A2=A, A3=t3*B+J(B),
A4=B, A5=B+t5*(C-B)-10*J(C-B), A6=C.                    (4)

Their exact defining identities are

|A1-C|^16-|A1-A|^16=1,
|A3-B|^16-|A3-A|^16=lambda,
|A5-C|^16-|A5-B|^16=1-lambda.                            (5)

Put a=|A1-A|^16, f=|A3-A|^16, g=|A5-B|^16. The six successive boundary-edge powers are

(a, f, f+lambda, g, g+1-lambda, a+1).                    (6)

Their alternating sums agree exactly.

Exact polynomial bisection gives these coarse rational coordinate enclosures:

| point | x | y |
|---|---|---|
| A1 | (0.17194,0.17196) | (4.72219,4.72221) |
| A3 | (-0.55229,-0.55227) | 2073/10000 |
| A5 | (0.40359,0.40361) | (-2.64281,-2.64279) |

Together with A,B,C these certify six distinct vertices. The even determinant is 0.00132672>0 and the odd determinant det(A3-A1,A5-A1) lies in (6.37,6.39). In fact all twenty boundary triples are noncollinear.

No solution of (1) is a boundary point. Positivity of lambda gives |X-B|>|X-A|, hence x<b/2, excluding A1,A5. The point A fails since b^16!=lambda; B and C fail the first and second equations respectively by positivity. Exact intervals give |A3-C|^16-|A3-A|^16-1 in (0.98,0.99), excluding A3.

## A directly certified incoming center

Define the fixed positive algebraic constants

L=|B-A5|^16-|B-A3|^16=g-f-lambda,
M=|A-A1|^16-|A-A3|^16=a-f.

Set b'=A5-A3, c'=A1-A3, D'=det(b',c')>0. For s in [1/100,11/1000] put

u'=s^(1/8), v'=(s+L)^(1/8), w'=(s+M)^(1/8),
R1=|b'|^2+u'-v', R2=|c'|^2+u'-w',
Yx=(R1*c'y-R2*b'y)/(2D'),
Yy=(b'x*R2-c'x*R1)/(2D'), H(s)=Yx^2+Yy^2-u'.

All boundary roots and L,M are fixed; interval boxes enclose them and do not choose them anew. Positive radicands and D'!=0 give continuity. Exact rational intervals prove

H(1/100) in (0.00037,0.00038),
H(11/1000) in (-0.00081,-0.00080).

At an intermediate zero, the same squared-distance equivalence gives Z=A3+Y with

|Z-A5|^16-|Z-A3|^16=L,
|Z-A1|^16-|Z-A3|^16=M.                                  (7)

The whole retained incoming box lies in (0.1677,0.1717) x (-0.0036,-0.0026), disjoint from all boundary points. Incoming existence is certified directly and does not assume a flip-existence theorem.

## All six exact face identities

Let ri=|Z-Ai|^16 and qP=|X-P|^16 for any selected outgoing X. Equations (1),(6),(7) imply:

| incoming face | exact opposite-side identity |
|---|---|
| A1A2A3Z | a+r3=r1+f |
| A3A4A5Z | (f+lambda)+r5=r3+g |
| A5A6A1Z | (g+1-lambda)+r1=r5+(a+1) |

| outgoing face | exact opposite-side identity |
|---|---|
| A2A3A4X | f+qB=qA+(f+lambda) |
| A4A5A6X | g+qC=qB+(g+1-lambda) |
| A6A1A2X | (a+1)+qA=qC+a |

The third incoming identity uses M-L=a-g+lambda. These are symbolic equalities, not deductions from intervals merely containing zero. This proves the theorem.

## Verification, geometry and attribution

The proposed publication files `publication/verify_five_centers.py` and `publication/exact_certificate.json` must be populated from Root's final authenticated package. Their current frozen-v2 versions use only Python's standard library, integer/Fraction sign decisions, checked eighth-root bounds on the 10^-36 grid, 128 exact boundary bisections and 100 sign-preserving bisections of each outgoing bracket. Default verification recomputes and compares its certificate without writing. Internal check counts are bookkeeping, not independent propositions. The publication verifier derives from the algebra/analysis audit implementation; it is not represented as a newly independent implementation. Earlier independent audits are separately identified historical evidence.

The verified boxes exclude every boundary-pair line for each selected outgoing center and for the incoming center. No repeated face vertex, collapsed edge or collinear face triple explains the result. Nevertheless the orientation signs for (A1,A2,A3), (A1,A2,A4), (A3,A4,A1), (A3,A4,A2) are respectively -,+,+,-. Hence the fixed boundary segments A1A2 and A3A4 strictly cross; proper embeddings are not covered.

The curve family is older: Ash--Bolker (1986) studied weighted costs phi(|x-P|)+w(P), including phi(t)=t^4; Bourne--Peletier--Roper (2014), Definition 4.12 in the author manuscript, explicitly defined |x-xi|^p-wi cells; Bourne--Roper (2015), Section 5, p.2568, repeated this p-power family. With p=16 and weights 0,lambda,1 the equality of those three costs is exactly (1). No new curve family is claimed. Ash--Bolker's separate oscillatory non-power example does not itself settle this pure-power intersection count.

A bounded search completed 15 October 2026 located no earlier at-least-four pure-power shared-focus witness in the checked corpus. Historical priority, firstness and independent awareness remain unestablished. See `SOURCE_AUDIT.md` for references and limits. AI systems were used extensively in exploration, drafting, code generation and adversarial checks. This work is unrefereed and has not received conventional human peer review.

Final accepted package: UNRESOLVED_FINAL_ROOT_ACCEPTED_PACKAGE_AND_HASHES.
Verified DOI and landing page: UNRESOLVED_VERIFIED_DOI / UNRESOLVED_VERIFIED_DOI_URL.
Whole-package final review: UNRESOLVED_ROOT_FINAL_WHOLE_PACKAGE_REVIEW_RECEIPT.
