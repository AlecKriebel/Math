# Independent adversarial audit: Rubel L-atoms

Audit date: 4 October 2026 (UTC). Target: rank 576, problem 2305055,
Function Theory Problem 5.55. This is a fresh AI mathematical review, not
human peer review or a proof-assistant certificate.

## Verdict

**PASS: no mathematical correction is required for the stated claims.**

The frozen proof establishes both:

1. The literal disk theorem: a nonconstant holomorphic function on the unit
   disk is an L-atom exactly when it is injective.
2. The separately stated extension: the same equivalence holds on every
   nonempty connected open subset of the complex plane, using escape from
   every compact source subset and escape from compact subsets of each
   function's actual image.

The arbitrary-prescribed-perturbation surjectivization lemma is valid with
the quantifiers stated in the packet. The full-zero-order quotient is a
valid compact-tube-bounded fiber separator even on unbounded plane domains.
No claim about all open Riemann surfaces or several variables is certified.

The proposed `already_solved`, `1/5` disposition is mathematically supportable
as a reconstruction of the pre-existing public disk proof, subject to the
root's repository gate. It must retain attribution to DannyExperiments and
explicitly identify that source as an AI-assisted, unrefereed public
manuscript. Neither this audit nor the source's own audit counts establish
journal acceptance, specialist peer review, formal verification, or historical
priority. The all-plane-domain consequence must stay separately identified.

## Frozen target and audit independence

The following received hashes were independently checked:

- `public/SHA256SUMS`: `d0cda51cc3bae01a22703086f5e1166efc36071e7af471ac84f9d6a1acbdcfe0`
- `public/PROOF.md`: `70d0ec9b1ccae32fb0d68411e199aff5882f9cff8682ebb4a765ad2a0e484a94`

Every entry in the frozen checksum manifest passes. The source files were
left untouched; audit material is separate. No remote write was made, no
helper was used, and no external audit conclusion was adopted as evidence.

The primary 2018 PDF was read at printed page 106 and its rendered page was
inspected. The pinned external TeX was read directly and then retrieved
afresh through the GitHub connector. Fresh bytes match the private source
copy and its stated SHA-256. The external manuscript's mathematical mechanism
was assessed directly, not inferred from publication metadata.

## 1. Exact question and ordering direction

The primary source specifies the implication from the first member f to the
second member alpha. It asks whether every such f must be a holomorphic
function of alpha. The packet has this direction right throughout.

On the disk, compact-source escape is equivalent to |z_n| tending to 1:
each closed disk of radius less than 1 is compact, and every compact subset
of the open disk is contained in one such smaller disk. Thus the broader
definition specializes to the original question without losing or adding
disk sequences.

For a constant f, its actual image is a singleton compact set containing all
its image terms. It never has the L-property and it factors through every
nonconstant alpha as a constant function. Treating this case separately is
correct. The theorem's nonconstant-alpha hypothesis is essential and is
present in the definitions and every relevant claim.

The original page's adjacent update is indeed printed as Update 5.56.
The packet correctly reports that numbering mismatch rather than silently
changing the primary source.

## 2. Compact-image criterion

For nonconstant f and g, the criterion in PROOF section 1 is exact, with
relative compactness taken in G_f, not merely boundedness in the plane.

Sufficiency: if g-values meet some compact K infinitely often, the matching
f-values lie in the compact closure of f(g^{-1}(K)) inside G_f. Hence f does
not escape. This is precisely the contrapositive of the required implication.
There is no reversal of the ordered pair.

Necessity: failure of relative compactness means S=f(g^{-1}(K)) cannot be
contained in any compact subset of G_f. Since K is compact, g^{-1}(K) is
closed in U. Its intersection with a compact A_n is compact, and its f-image
B_n is compact in G_f. A point can therefore be chosen with its f-value
outside C_n union B_n. Such a point lies outside A_n. Cofinal increasing
exhaustions ensure both source escape and escape of the f-values, while
the g-values stay in the same K. All sequence quantifiers are satisfied.

This argument works for arbitrary plane domains, including unbounded ones
and domains with punctures. Compact tubes are not assumed compact,
connected, or bounded in the source.

## 3. Runge exhaustion and the adjoined-disk topology

### Holomorphic hull

The proof of a compact Runge exhaustion does not assume the exhaustion it
is trying to produce. For a nonempty compact C in Omega, the coordinate
function bounds its O(Omega)-hull. If Omega is proper, delta=dist(C,C\Omega)
is positive. Testing the hull against each reciprocal 1/(w-a), a outside
Omega, gives |w-a| at least min_{v in C}|v-a|, and hence at least delta.
Consequently the hull stays a uniform positive distance from the complement.
Relative closedness together with boundedness and this distance estimate
makes it compact in Omega. When Omega is the whole plane, boundedness and
closedness already give compactness.

If a complementary component V had closure compactly contained in Omega,
its boundary would lie in the hull. For each holomorphic h on Omega,
continuity on that closure and the maximum principle bound |h| throughout
V by its maximum on the hull, which is at most max_C |h|. Every point of V
would therefore belong to the hull, a contradiction. This proves the needed
Runge property even for compacta with irregular boundaries.

Recursively taking a compact neighborhood of the preceding hull and the
next ordinary exhaustion member, then taking its hull, preserves the
neighborhood. It gives strict interior inclusion and cofinality. The empty
initial-exhaustion-member issue can be avoided by choosing a nonempty first
compact; there is no restriction on Omega.

### One isolated closed disk

Let V be the component containing the full closed disk of radius 2r. Its
complement after removal of the closed radius-r disk is path connected.
Points in the inner annulus connect radially to the radius-3r/2 circle;
points outside that circle follow a path in V toward the center only until
their first contact with the circle. The latter stopped path stays outside
the inner disk. Points already on the circle need no additional path.
The circle itself lies in V and connects all these paths.

The surviving component cannot become relatively compact: adding the
removed compact disk back would then place the closure of V in a compact
subset of Omega, contrary to the Runge property of K. Other components do
not change. Thus adjoining this disk is legitimate. This remains true when
V is unbounded or multiply connected, or K is disconnected. The double-radius
collar excludes the familiar failure caused by adding a barrier that closes
a hole.

The ordinary Runge approximation invoked has exactly the correct hypothesis:
a compact subset with no complementary component relatively compact in Omega,
and data holomorphic on a neighborhood of that compact set. There is no
unstated simply connectedness assumption or unjustified polynomial-only
approximation on a multiply connected target.

## 4. Surjectivization, infinite budget, and Rouché

### Continuing the construction

Omega=alpha(U) is a connected open plane domain, so it cannot equal a compact
K_{n-1}. The inverse image of its nonempty open complement is nonempty and
open in U. Since alpha is nonconstant on connected U, alpha' cannot vanish
on that entire open set. Thus a regular preimage x_n exists.

Only this chosen preimage must be regular. The value a_n need not have all
its preimages regular, so dense or complicated critical-value behavior is
not a hidden obstruction. The inverse function theorem supplies one local
branch; shrinking r_n places the closed doubled disk inside both its
neighborhood and the chosen complementary component.

Because the new disk and old compact are disjoint compact sets, their data
can be defined on disjoint neighborhoods. The prescribed data
q_n=P_n-b composed with s_n are holomorphic there for every fixed b in O(U).
No boundedness of b on U, on all tubes, or uniformly across the islands is
required. Ordinary Runge approximation yields both stage-n estimates.

Choosing K_n as a sufficiently late member of the fixed Runge exhaustion
protects the new disk, all earlier disks, and E_n. It is possible at every
finite stage and makes the K_n cofinal.

### Local uniform limit and all later errors

For each compact C in Omega, C lies in some K_N. Every subsequent correction
H_j-H_{j-1}, j>N, is uniformly bounded there by 4^{-j}. The sequence is
uniformly Cauchy on every compact, so its limit H is holomorphic on Omega.

For a fixed island n, its initial approximation error is less than 4^{-n}.
For every j>n that island is inside K_{j-1}, so its j-th correction is less
than 4^{-j}. The complete error is therefore at most

    sum_{j=n}^infinity 4^{-j} = 4^{1-n}/3 <= 1/3.

The index starts at n, not n+1, so the newly introduced approximation error
is not accidentally omitted. A weak inequality in the limiting estimate
causes no problem because the final comparison margin is strictly larger.

### Coverage of every target value

For |xi|<=n, the affine comparison P_n-xi has one zero strictly inside
Delta_n; its normalized distance from the center is at most n/(n+2)<1.
On the boundary its modulus is at least 2. The final error of
H+b composed with s_n relative to P_n is at most 1/3. Both functions are
holomorphic on a neighborhood of the closed disk, so Rouché applies and
gives a zero of H+b composed with s_n-xi inside it. Pullback by s_n gives
an actual point of U with F-value xi.

This proves coverage of the entire closed radius-n target disk, not merely
a dense or countable subset. Taking all positive integers proves F(U)=C.
No normal-family argument, numerical root search, or heuristic interpolation
replaces the infinite construction.

The quantifier is correctly 'for each analytic b, there exists H_b'. A
single H cannot work for every analytic perturbation, because a subsequently
chosen b=-H composed with alpha gives a constant sum. The packet explicitly
rules out that stronger statement. It also correctly gives H its domain
Omega; no extension of H beyond the actual image is assumed.

## 5. Disk theorem and actual-image requirement

For the disk, b(z)=z is bounded. On alpha^{-1}(K), F is bounded by max_K|H|+1.
Because surjectivization has already established G_F=C, that bound places
all such values in a compact subset of the actual image. The compact-image
criterion consequently gives exactly (F,alpha) ordered.

Distinct p and q in one alpha-fiber satisfy F(p)-F(q)=p-q, which is nonzero.
This prevents even a set-theoretic single-valued factorization through alpha,
and thus certainly a holomorphic factorization. Conversely, an injective
holomorphic map of a plane domain has nonzero derivative and a holomorphic
inverse on its image; f composed with that inverse supplies the desired
factor for every holomorphic f. There is no properness or boundary-extension
assumption.

Surjectivity is not dispensable in this proof. A bounded subset of a proper
range can accumulate at an omitted boundary point, as the identity on the
disk shows. The packet uses boundedness as relative compactness only after
proving that the relevant image is all of C.

## 6. All-plane-domain separator

Take distinct p,q with alpha(p)=alpha(q)=c. Nonconstancy and isolated zeros
give a finite exact order m>=1 at p. Factoring locally as
alpha(z)-c=(z-p)^m u(z), u(p) nonzero, proves the quotient extends holomorphically
at p. Away from p its denominator has no zero. Thus b lies in O(U), with
b(p)=u(p) nonzero and b(q)=0.

Choose a closed source disk about p contained in U. Its b-maximum B is
finite by continuity. Outside that disk, |z-p|>=delta, so on alpha^{-1}(K)
the quotient is bounded by max_{w in K}|w-c|/delta^m. Combining the two
regions gives a bound for the entire tube. This estimate explicitly covers:

- points approaching any finite boundary component;
- points escaping to infinity in an unbounded domain;
- infinitely many components or sheets of the same tube;
- critical fibers, including when both p and q are critical points.

There is no assumption that the tube is compact or that alpha is proper.
It is unnecessary for b to be globally bounded. The full multiplicity is
essential: for alpha(z)=z^2(z-1)^2, p=0, q=1, dividing only once leaves value
zero at both points, while dividing by z^2 gives b(z)=(z-1)^2 and separates
them. Dividing beyond the exact multiplicity would instead create a pole.

Applying the already proved prescribed-b lemma to this b yields an onto F.
Both summands are bounded on every compact alpha-tube, so (F,alpha) is
ordered. Their H terms cancel on the chosen fiber, leaving the nonzero
b-value difference. The contradiction to atomicity is complete.

The global plane coordinate z-p is being used, so the argument legitimately
covers every plane domain and is not automatically an argument on arbitrary
nonplanar Riemann surfaces. The packet's stated scope is exact. Compact escape
is an explicit interpretation of the open-ended general-domain question,
not a claim that every possible interpretation has been classified.

## 7. Source status, finite controls, and disposition limits

Fresh GitHub reads confirm the pinned manuscript blob and bytes, and current
release metadata records publication on 5 August 2026. The source's separate
AI disclosure says no human specialist peer review or full proof-assistant
verification is claimed. This supports retaining the packet's explicit
AI-assisted, unrefereed-source qualification.

The frozen verifier was rerun after inspection. All 28,840 assertions pass,
and stdout is byte-for-byte identical to the frozen verification.json. These
are supplementary algebra/transcription/diagnostic controls only. They cannot
certify Runge approximation, holomorphic convergence, Rouché, historical
priority, or the unrestricted theorem. The analytic arguments above are the
basis for this verdict.

One provenance nuance merits preservation in subsequent writing: the GitHub
release API reports `immutable: false`. The manuscript is nevertheless
content-addressed by the pinned commit and blob, and the release's TeX
asset digest equals the inspected SHA-256. Say 'commit-pinned manuscript'
rather than claiming the GitHub release itself has enforced immutability.
No frozen mathematical claim depends on that platform flag, and the packet's
immutable-manuscript link is a commit-pinned link.

The current audit does not certify an exhaustive literature search, the
Zenodo deposit, or the absence of every possible repository duplicate. The
root must apply its own live repository gate before publication. No related
Problem 2.56 disposition or theorem is included in this verdict.

## Required repairs and final gate

- Mathematical repairs: none.
- Frozen file edits: none performed or requested.
- Scope restrictions to retain: nonconstant alpha; plane domains; explicit
  compact-source escape; actual target images; H dependent on prescribed b.
- Attribution to retain: the disk mechanism and theorem predate this packet
  in the pinned DannyExperiments public manuscript; all-plane-domain quotient
  consequence is separately labeled, with no originality claim.
- Review qualification to retain: independent AI mathematical audit passed;
  human specialist review and full formalization are not established.

Subject to those disclosures and the root's repository gate, the audited
proof is ready to support the proposed `already_solved`, `1/5` record.
