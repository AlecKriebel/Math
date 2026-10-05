# Independent analytic priority audit of the supplied 1966 sources

This audit's strongest conclusion is that neither supplied 1966 paper prints
the normalized pure-Blaschke Cayley answer as such, but their printed data
already yield it by a direct classical analytic adapter. Piranian prints a
completely fixed four-adic construction and the pointwise obstruction needed
for purity. Duren-Shapiro-Shields (DSS) explicitly prove the required Bloch
criterion. The missing application is a Cayley transform plus canonical
factorization and the positive converse of Fatou. That application is proved
below as this audit's deduction, not attributed as a literal 1966 result.

A separately requested check is stronger historical evidence. AAN (1999)
Theorem 2 and its printed quadratic-weight Cayley application give the exact
normalized target after a routine domain automorphism, with Bloch seminorm at
most 8. Hayman-Lingham (2019), Update 5.51, expressly calls AAN's inner-function
construction explicit. Thus the package may present an attributed effective
recursion, but it cannot use its modern finite-algebraic meaning of explicit
to dismiss the prior covering construction or imply the historical request
was still awaiting this contribution.

## Scope, pins, and independence

The target is an explicit pure Blaschke product on the disk, with B(0)=0 and
F=(1+B)/(1-B) in the Bloch space. Existence alone is not the requested novelty.
The exact immutable candidate is a hypothesis, not evidence of any theorem or
historical claim. The supplied context identifies PR65 as an open draft with
submitted/current literal status `claimed_solved`, head
`5cc1602c05d79502defb07cec7027963149494d2`, and original proof-turn count 2/5.
Those PR facts are intake context, not an independently refreshed remote view.

| Artifact | SHA-256 | Reading scope |
|---|---|---|
| Immutable CANDIDATE.md | `0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4` | Complete candidate |
| Current note.tex | `7b5b13db61725d8e27293d35402d8719f97ab2db2c5380f0c65cb14d37964b56` | Current exposition; treated as claims |
| duren1966.pdf | `03a0707ffce4f5e6ac6cb055e8ed2666804a7aa78d03385b3d56cd9a902443d2` | Complete body, all scans, printed pp.247-254 |
| piranian1966.pdf | `3e376dc57beee169e1b5165151b91d79bde1545df75b974bd1a19c9d06db61d1` | Complete body, all scans, printed pp.255-262 |
| carmona_donaire1999.pdf | `9a9e731d64add65796213d0096a659e998ac09d583ab93e489c78651ad524b74` | Ordinary/symmetric density definitions and positive Loomis theorem, pp.207-208, checked against scans |
| aan1999.pdf | `479babf99aeaf1f58e6ee44590d29046bd54b98cfa9603d496812985bae6c7be` | Text pp.318-320,326-329; decisive scans pp.320,326-329 |
| hayman2019.pdf | `1388a8c153a3eb16156d90542d1f00e4a6203b594566540c71c5f354238e14dc` | Problem and Update 5.51, printed pp.121-122 / PDF pp.127-128, checked against scans |

The complete 1966 readings and all sixteen page inspections preceded saving
FIRST_CONCLUSION.md. No ROOT, sibling, or earlier review opinion body was read.
Only after that checkpoint did ROOT request the AAN normalization check and
supply the HL2019 primary location. No new original proof-search turn was
undertaken. The deductions here test the source adapters and their hypotheses.

All full source bodies, extracted text, and rendered pages remain in a unique
external private cache. The public audit folder contains original analysis,
source pins, finite diagnostics, and genuine execution receipts. No external
individual was contacted. No shared Git/index, PR, editor, native-document,
Zenodo, or publication mutation occurred.

## What the 1966 papers actually print

| Source and location | Printed content | Exact gap to Holland's target |
|---|---|---|
| DSS p.247, canonical factorization and (1) | An exponential of minus a singular Herglotz integral is a conformal-map derivative and singular inner factor. | This exponential is zero-free, has a nonzero singular factor, and is not the requested Cayley transform. |
| DSS p.248, Theorem 1 | For a bounded-variation primitive, the exponential exp(-aF) is a suitable conformal-map derivative iff the periodic primitive is in the Zygmund class; rectifiability adds positivity and an integrability condition. | It concerns conformal domains and exponential derivatives, not a Cayley Blaschke product. |
| DSS pp.249-250, (7), (9)-(11) and proof | F'(z)=O((1-r)^(-1)) iff the periodic primitive is Zygmund. The same equivalence is restated on p.252. | This is exactly the Bloch input, but innerness and purity of the Cayley transform are not discussed. |
| DSS pp.251-254 | Further univalence, Fourier tests, sharpness examples, and references to Piranian. | No target B appears in the remaining body. |
| Piranian p.255, Theorem 1 and introduction | Explicit singular monotone Zygmund examples; one has derivative, where it exists, equal to zero or infinity. A degree-one periodic lift is described. | Its cubic route still contains sufficiently rapid choices; it is not a printed Cayley construction. |
| Piranian pp.256-260, Sections 2.1-2.5 | Piecewise-cubic building block, maximal admissible amplitudes, all-scale second-difference estimates, and no finite positive derivative. | This is a measure construction, with frequency choices stated qualitatively. |
| Piranian pp.260-261, Section 3 / Theorem 2 | Kahane's fixed integer-valued four-adic construction, absorption at zero, and minus-one in outer quarters / plus-one in middle quarters. Uniform convergence, no finite derivative other than zero, and Zygmund regularity are asserted/proved as described there. | All measure data are specified; the analytic adapter to a normalized pure Blaschke B is absent. The Zygmund proof for this rule is explicitly omitted as analogous to Section 2. |
| Piranian pp.261-262, Section 4 | Smooth variants with amplitudes tending slowly enough to zero and corner rounding. The paper explicitly says the prior exclusion of finite positive derivatives need not survive that modification. | These variants cannot be substituted into the purity argument merely because they are singular and smoother. |

In particular, the full 1966 record is not merely an existence statement or an
unspecified measure. Piranian p.260 prints all finite transitions of the fixed
rule. But neither paper writes B=(F-1)/(F+1), states B(0)=0, names the resulting
function a pure Blaschke product, or eliminates its singular factor. Their
printed endpoint is antecedent measure/Smirnov-domain/conformal-map theory.
The exact target is effectively recoverable from that theory, as follows.

## Checked direct adapter of the fixed 1966 construction

This section is a deduction of this audit. It is not a claim that the complete
following theorem was printed in 1966.

Start with w^(0)=(1), and replace each positive height a by
(a-1,a+1,a+1,a-1), and each zero by four zeros. This is Piranian p.260's
published Kahane rule. It differs from the submitted asymmetric tie rule;
the first old list is (0,2,2,0), whereas the submitted first list is (2,0,2,0).
We do not claim their particular resulting functions are identical.

For the four-adic cells I_(n,j)=[j4^(-n),(j+1)4^(-n)) on R/Z, put
mu(I_(n,j))=4^(-n)w_(n,j). Positive parent heights are integers; each child
sum equals four times its parent; 0<=w_(n,j)<=n+1 and total integer mass is
4^n. The consistent masses define a probability measure. Its possible atom
mass is at most two neighboring cell masses, hence at most
2(n+1)4^(-n), tending to zero. Endpoint conventions are therefore harmless.
The constant intervals on the full-measure open set in Piranian Theorem 2
have zero mu mass, proving singularity. Equivalently, the absorption walk
has symmetric +/-1 steps until zero and is absorbed almost surely under dx.

At every point, the specified nested-cell ratios are exactly w_n(x). They
are eventually zero, or change by one in absolute value at every generation.
They cannot converge to a finite positive number. Ordinary density L>0
would force that convergence. At a grid endpoint, ordinary density over
strictly containing intervals also forces one-sided density: append an
opposite interval of length h^2, and use positivity and its O(h^2) mass to
remove it. This also handles the circle seam. It is consistent with the
printed all-point finite-derivative exclusion on Piranian p.261.

For completeness the omitted circular all-scale Zygmund check does not
require a new existence theorem. Circular neighbors have height difference
at most two: within each parent this is immediate; between positive parents
their facing outer children both subtract one, preserving the old difference;
beside a zero parent the positive neighbor is at most two, so its facing
child is at most one. The first and last cells are zero from generation one
onward. Define H_n(x)=integral_0^x(w_n(t)-1)dt. Each increment has mean zero
on every old cell and absolute slope at most one. Thus H_n has a continuous
periodic limit H with ||H-H_n||_infinity <= (4/3)4^(-n), and dH=dmu-dx.
If ell=4^(-n)<=h<4ell, the interval [x-h,x+h] meets at most nine consecutive
cells. Their height range is at most sixteen, giving a deliberately loose
18h bound for H_n's second difference. The tail adds at most (16/3)ell.
Consequently the second difference of H is at most 24h, uniformly for every
small h and every x. For h>1/4, the bound ||H||<=4/3 gives the same estimate.
This is a global circle estimate, not a dyadic-only or sampled assertion.

Set

    F(z) = integral_(R/Z) (exp(2*pi*i*x)+z)/(exp(2*pi*i*x)-z) dmu(x),
    B(z) = (F(z)-1)/(F(z)+1).

Then F(0)=1, Re F>0 and, by DSS pp.249-250, F is Bloch. To match their
coordinates, take their cumulative primitive mu_DSS(t)=mu([0,t/(2*pi)]),
0<=t<=2*pi. Its total mass is one; their K in (4) is -1/(2*pi), so their
periodic primitive is H(t/(2*pi)). No missing factor 2*pi changes the
Herglotz mass or F(0).

The singularity of mu gives Re F->0 radially dx-almost everywhere. The
identity 1-|B|^2=4 Re F/|F+1|^2 and bounded analytic boundary limits show
that B is inner, and F(0)=1 gives B(0)=0. B is nonconstant: the normalized
constant F=1 has Lebesgue Herglotz measure, whereas mu is singular.

Purity requires a separate proof. If B had a nonzero singular inner factor
S_nu, with positive singular measure nu, then at nu-almost every point its
centered density is infinite. In any fixed Stolz cone, the Poisson kernel on
the centered arc of radius 1-|z| is bounded below by a positive constant
times (1-|z|)^(-1). Thus P[nu](z)->infinity nontangentially there;
|S_nu|=exp(-P[nu])->0 and the remaining bounded inner factors imply B->0.
Consequently F->1 and Re F->1 nontangentially.

The positive Loomis theorem, read in Carmona-Donaire pp.207-208, says that
a finite nontangential limit L of a positive Poisson integral implies
ordinary density L. Their separate radial result gives only symmetric
density and is insufficient here. Disk normalization can be checked
directly: rotate the point to 1, take z=(1+iw)/(1-iw), w=x+iy, and
zeta(t)=(1+it)/(1-it). For the real-coordinate pushforward sigma of mu,

    (1-|z|^2)/|zeta(t)-z|^2 = y(1+t^2)/((x-t)^2+y^2).

With d tau=pi(1+t^2)d sigma, this is the half-plane Poisson integral with
factor 1/pi. The required weighted integrability is
integral (1+t^2)^(-1)d tau=pi. There is no antipodal atom. Normalized angle
near zero is arctan(t)/pi, so ordinary tau density L becomes ordinary
normalized circle density L. L=1 therefore contradicts the all-point
exclusion proved above. The singular factor is zero: B is pure Blaschke.
A finite nonconstant Blaschke product has a nonzero angular derivative at
a boundary preimage of 1, creating a simple pole of F and violating its
Bloch bound. Therefore B is infinite.

The adapter is effective under the candidate's chosen computational meaning
of explicit. Move each cell's mass to its midpoint, define p_(n,j)=w_(n,j)/4^n
and zeta_(n,j)=exp(2*pi*i*(j+1/2)/4^n), and let F_n be the finite Herglotz
sum with those weights. B_n=(F_n-1)/(F_n+1) is rational inner, hence finite
Blaschke, with algebraic coefficients and B_n(0)=0. The kernel x-derivative
is bounded by 4*pi*r/(1-r)^2 for |z|<=r. Each displacement is at most
4^(-n)/2, so

    sup |F-F_n| <= 2*pi*r/(1-r)^2 * 4^(-n),
    sup |B-B_n| <= 4*pi*r/(1-r)^2 * 4^(-n).

The latter uses B-B_n=2(F-F_n)/((F+1)(F_n+1)) and positive real parts.
No unspecified good shift, covering map, or measure choice is needed for
this old-rule adapter. The finite diagnostic checks levels 0-8 and the
quadratic-field identity for B_1=-z(z+1/sqrt(2))/(1+z/sqrt(2)). It is not
evidence for a universal boundary theorem; those claims have the proof above.

## Why an exponential or a generic Frostman shift is insufficient

For a positive singular measure, exp(-aF) is a zero-free singular inner
function with value exp(-a) at zero. Multiplication by z gives a zero at
zero while retaining the singular factor. Neither operation produces purity.
Bloch control of F is Bloch control of a logarithm of that exponential; it
does not turn the exponential into the requested Cayley function.

Singularity of a Herglotz measure establishes innerness of its Cayley
transform, not purity. Limits of finite Blaschke products can acquire
singular factors. For instance, z*((1-c/n-z)/(1-(1-c/n)z))^n converges on
compact disks to z*exp(-c(1+z)/(1-z)), for c>0 and n>c. The pointwise
positive-density exclusion is therefore an essential independent input.

Frostman's exceptional-parameter theorem would provide good shifts only
outside an exceptional set. It does not certify the uniquely normalized
shift at zero or provide an evaluated parameter. Even for a real shift
a, the Cayley transform is scaled by (1-a)/(1+a) while the value at zero
becomes -a. A chosen zero and domain automorphism can restore normalization,
but unspecified good parameters and zeros do not meet a fully specified
finite-formula recipe. The checked 1966 adapter avoids those choices.

## Independent AAN1999 quadratic-weight and purity check

AAN Theorem 2, printed p.320, supplies an interpolating Blaschke product
with (1-|z|^2)|B'(z)| <= phi(1-|B(z)|^2). In its proof on pp.326-327,
the function is a universal cover onto D\Lambda, where Lambda is a countable
discrete subset of D\{0} with cluster set contained in the boundary. The
proof first obtains innerness and then explicitly excludes a singular
factor by ruling out a radial limit zero. The exclusion uses 0 not being
a removed point; it is not an appeal to a generic Frostman shift. A radial
curve whose image tends to interior point zero eventually lies in one
evenly covered neighborhood and one inverse branch, and hence would tend
to an interior preimage, contradicting approach to the source boundary.

Take phi(t)=t^2. Zero belongs to the range, so choose p with B(p)=0 and
let psi(z)=(z+p)/(1+conj(p)z). For C=B composed with psi, C(0)=0 and the
exact identity

    (1-|z|^2)|psi'(z)| = 1-|psi(z)|^2

preserves the derivative inequality. Purity is preserved as well: for each
zero a, the modulus of its Blaschke factor composed with psi equals the
modulus of the factor for psi^(-1)(a). Automorphism distortion keeps
sum(1-|psi^(-1)(a)|) finite. The Green-potential sum for -log|B| therefore
transforms into precisely the sum for those zeros, with no singular
harmonic remainder. Equivalently C is still the same universal cover of
D\Lambda, and the above covering argument still excludes a singular factor.

Finally, G=(1+C)/(1-C) obeys

    (1-|z|^2)|G'(z)|
       <= 2*((1-|C|^2)/|1-C|)^2
       <= 2*(1+|C|)^2 <= 8.

Thus it gives exactly a normalized pure Blaschke product with Bloch Cayley
transform. This is a checked normalization deduction from the printed
construction. AAN already print the more general Cayley functions
F_alpha=(alpha+I)/(alpha-I), the quadratic derivative condition, and the
bound 8c on pp.328-329. These displayed statements are historical printed
evidence, rather than our new extrapolation.

HL2019, printed pp.121-122, repeats Holland's target and under Update 5.51
attributes the stronger inner-function result to AAN, expressly describing
I as constructed explicitly. That update's literal I need not itself be
the pure product of Theorem 2, and the update does not write the normalization
adapter above. It does establish that covering-style analytic construction
was treated as explicit in the historical problem's update. Restricting the
word to finite algebraic stages is an additional modern presentation choice.

## Required package corrections and remaining novelty scope

1. In note.tex lines 31-35 and 55-69, move the earliest now-read fixed-rule
   attribution to Kahane's construction as printed by Piranian (1966),
   pp.260-261. Kahane 1969 can remain as later elaboration/variant evidence.
   Do not imply the fixed absorption rule or no finite positive derivative
   was first supplied in the current package.
2. In the Herglotz-Zygmund section, credit DSS (1966), pp.249-250, for the
   explicit F' growth equivalence. AAN p.333 can remain a later reference;
   the new direct appendix is an exposition/check, not an uncredited new
   analytic mechanism.
3. Replace note.tex lines 95-103 and bibliography lines 580,585,589: the
   supplied DSS/Piranian full bodies and relevant HL2019 update are now read.
   Record exact page scope and retain any genuinely unread global literature
   gap. An earlier frozen artifact can retain its historical reading state,
   but the current package must distinguish that artifact from current evidence.
4. Strengthen note.tex lines 78-93 with the checked AAN normalization and
   purity-preservation deduction and the published 8c Cayley estimate.
   Explicitly cite HL2019 Update 5.51, pp.121-122, as historical attribution
   of an explicit construction. The package must not imply that a covering
   map automatically falls outside the historical request.
5. In the old-rule section, cite Piranian pp.260-261 for both the printed
   deterministic rule and all-point finite-derivative exclusion; DSS
   pp.249-250 for the Bloch step; and the checked positive converse-Fatou
   statement for purity. Label the assembled 1966-rule Holland adapter a
   present deduction. It is not a literal theorem found in either 1966 paper.
6. Preserve the immutable submitted CANDIDATE.md and original status history.
   Add the current evidence as an explicit correction/addendum and propagate
   its meaning to current priority notes, source matrices, README/abstract,
   review metadata and publication claims. Do not silently rewrite the
   frozen original or increment original proof-search accounting for this audit.
7. Separate mathematical validity from research novelty. The sources do not
   falsify the submitted target proof; they undermine any claim of a new
   construction mechanism or first explicit answer. This report is not a
   full correctness audit of all submitted inequalities or a publication approval.

No novel mathematical claim is verified here. A fully effective midpoint
presentation and compact error modulus are useful explicit exposition, but
the same formulas and estimates apply to the printed 1966 fixed rule.
Different asymmetric signs alone do not establish a research contribution.
A separately proved property unavailable from those antecedents, such as a
new sharp bound or new zero-distribution/evaluation theorem, would be a
different claim requiring its own proof and priority comparison. Historical
first articulation of the exact 1966-rule adapter is not established by this
bounded audit. The AAN printed application plus the 2019 update already
preclude treating absence of that precise adapter as evidence that the broad
explicit-construction request awaited PR65.

## Evidence and reproducibility limits

`source_pins.json`, `source_read_record.json`, `receipts/*.json`,
`finite_adapter_diagnostic.py`, and `MANIFEST.json` provide the pins,
reading coverage, exact command argv/cwd, actual subprocess PIDs, UTC times,
exit codes, runner/body hashes, and byte-stream hashes. Full primary-body
streams are referenced only by their private paths and hashes. `view_image`
is an API tool and has no invented subprocess PID. Its inspections are
listed as API observations, with recording time distinct from execution
timestamps. All diagnostic executions terminated successfully. The exact
primary 1943 Loomis body was not read; the theorem is used as printed in
the inspected 1999 primary article. No global earliest-date determination,
human peer review, formal proof verification, or publication clearance is
claimed.
