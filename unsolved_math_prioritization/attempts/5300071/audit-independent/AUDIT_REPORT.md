# Independent adversarial audit: 5300071 / AMR-052-0071

Audit date: 2026-10-04 UTC. Source rank: 650.

## Verdict and exact scope

**PASS AS AN UNSOLVED PARTIAL-RESULT PACKET.** No fatal error was found in the
common local disk, one-root case, equal-multiplicity two-root case, or stated
one-direction non-nesting example. The frozen packet does not solve the general
simultaneous common-arc problem and must not be classified as a complete candidate
or a verified prior resolution. Five author approach families are recorded; this
review audits those results and their boundaries, rather than adding a sixth
attempt to solve the general problem.

No mathematical correction is required to retain this scoped verdict. One minor
wording clarification for the conditional Blaschke discussion is recommended in
`CORRECTIONS.md`. It does not change a theorem or improve the completion status.

## 1. Input binding, established before mathematical review

The supplied archive is 18,826 bytes and has SHA-256
`291263a5a2454913eb161b8361acfdb56cf6840908eb0cdc995716061b122fb2`.
Its 13 regular-file members match the 13 files in the frozen submission exactly,
with no missing or extra members. The independently computed per-file manifest is
`ACTUAL_MANIFEST.json`. The author's `SHA256SUMS.json` itself has SHA-256
`5a30d804f6c0e6bf1e3c9f834aeb8eef7e21eda9434cd6ff0338073570a86978`.
Its verifier correctly checks the other 12 files; the archive and independent
manifest additionally bind the author's manifest. No author file was edited.

The author's verifier was read before execution. Its numerical/exact output
replayed identically to `CONTROL_RESULTS.json`; `REPLAY_AUTHOR.json` retains that
output. The author manifest verifier passed. Isolated temporary changes to a file, an
extra file, and an extra directory were each rejected by that verifier; the
originals remained unchanged. `audit_verify.py` supplies new,
standard-library-only exact controls and independently checks every author byte
against the frozen archive and the pre-review manifest.

## 2. Source identity and quantifiers

The original source was independently read in the exact cached IMS 92/7 PDF,
including printed pp.42-43. Printed p.43 was independently rendered and visually
inspected. Official web text was also opened. The selected item is Sutherland's
Conjecture 2, not the adjacent conjecture about families of bad polynomials.
The packet preserves the substantive quantifiers: a chosen root of multiplicity
m; the simultaneous intersection of its immediate basins for every real
0<h<=m; every radius R>=3; a lower bound 2*pi*R/(c*d) with an absolute constant.

The original circle-center omission is real. The packet explicitly chooses the
origin-centered interpretation consistent with the normalization and surrounding
circle estimates. Its off-center counterexample is valid, but is not a resolution
of that intended target. For f(z)=z^2-1/4, h=1, the basin of -1/2 is Re(z)<0;
a circle of radius 3 centered at 10 is disjoint from it. No claim of success may
be obtained by switching between these two readings.

The following distinctions were checked:

- d is the polynomial degree including root multiplicity. Reduced rational-map
  degree can be smaller: f=z^3(z-1/2) has d=4 while N_3 has degree 2.
- m is the multiplicity of the selected root, not the minimum multiplicity,
  number of critical points, number of accesses, or basin-map degree.
- h is fixed throughout each orbit. Uniform membership over h is not a claim
  about iterations with changing step sizes.
- The endpoint h=m is included; h=0 is excluded. The selected multiplier is
  1-h/m. Other roots need not attract on the entire selected interval.
- The roots lie in the normalized unit disk. Complex coefficients are arbitrary;
  there is no coefficient-height or separation lower bound in the target.
- Immediate-basin membership means membership in the connected basin component
  containing the root. Full-basin convergence alone is insufficient.
- The target is the intersection of the immediate basins, not the immediate
  component of that intersection. A common corridor would be a sufficient
  stronger mechanism, not a definition that can be silently imposed.
- The all-h intersection need not be open merely because each individual basin
  is open. Positive point counts or positive measure do not certify contained
  arcs. The packet correctly avoids those inferences.

## 3. Common local disk: general proof rechecked

Write f=(z-alpha)^m g and let delta be the nearest distinct-root distance. When
m<d, r=m*delta/(4d-3m) satisfies 0<r<delta. Factoring g into its zeros with
multiplicity gives, on the closed r-disk,

    |(z-alpha)g'/g| <= (d-m)r/(delta-r) = m/4.

There are no zeros of g there. After cancelling the removable root factor, the
denominator is m+(z-alpha)g'/g and has modulus at least 3m/4. Thus no hidden pole
is present, including at alpha or when h=m. With v=(z-alpha)g'/(mg) and t=h/m,

    N_h(z)-alpha = (z-alpha)(1+v-t)/(1+v).

For |v|<=1/4 and 0<t<=1,

    |1+v|^2-|1+v-t|^2 = 2t Re(1+v)-t^2
                               >= (3/2)t-t^2 >= t/2,
    |1+v|^2 <= 25/16.

Hence the squared radial contraction is at most 1-8t/25<1. This proves
convergence for every fixed positive h, on the same disk. Its connectedness and
containment of alpha establish the immediate component, rather than just the
full basin. In the one-root case cancellation gives the affine contraction
1-h/d directly, including the constant-map endpoint h=d.

This reasoning survives extremely small h and collapsing root separations.
It does not give a rate bounded away from 1 as h tends to zero. In the one-root
case, for any positive integer n one may choose h/m=1/(2n), and the n-step error
factor is at least 1/2. The shrinking radius under coalescence is genuine: at
fixed degree r is proportional to delta. Neither issue contradicts the lemma;
both prevent promoting it to the required exterior estimate.

## 4. Equal-multiplicity two-root family: full restricted target rechecked

For f=C(z-a)^k(z-b)^k, a!=b, d=2k and selected multiplicity m=k, the affine
coordinate u=(2z-a-b)/(a-b) gives

    F_t(u)=(1-t/2)u+t/(2u),  t=h/k in (0,1].

The Möbius coordinate w=(u-1)/(u+1) yields

    G_t(w)=w(w+q)/(1+q*w),  q=1-t in [0,1).

The exact difference (1-q^2)(1-|w|^2)>0 proves that the second factor has
modulus less than one in the unit disk. Its maximum on each closed subdisk is
strictly below one, proving convergence to zero for fixed t. Thus the right
u-half-plane converges to +1; odd symmetry proves the analogous statement for
the left half-plane. The imaginary axis, with poles and infinity interpreted on
the sphere, remains invariant and cannot converge to either real root. The two
open half-planes are consequently exactly the full basins and are connected
immediate basins. This verifies the stronger basin-identification statement,
not just an invariant subset.

Returning to z gives the Voronoi half-planes. Their common boundary passes
through (a+b)/2, whose modulus is at most one. Its distance from the origin is
therefore at most one. Each half-plane's intersection with C_R contains an open
arc of length at least 2R*arccos(1/R). For R>=3 this exceeds pi*R/2, since
1/3<cos(pi/4). For d>=2 that exceeds or equals 2*pi*R/(2d), so the claimed
absolute c=2 is valid on the entire restricted family. The half-planes themselves
are independent of h, which is exactly why taking the simultaneous intersection
is justified here. Rotated, translated, high-multiplicity and nearly coincident
root choices do not invalidate the argument.

There is no justified extension of this Voronoi proof to unequal multiplicities.
A new exact negative control uses f=z^3(z-1/2), h=3: the point 1/3 is in the
Voronoi half-plane of 1/2 but maps to -2/3 in the other half-plane. Also the
multiplier at 1/2 is -2. This directly checks the packet's warning about both
unequal multiplicities and hypotheses requiring every finite root to attract.

## 5. Nesting and fixed-parameter channel calculation

For f=z(z^2-1), N_1(1/2)=-1 exactly. At h=1/2 the factor multiplying x is
(5x^2-1)/(6x^2-2). On [-1/2,1/2], setting s=x^2 gives a positive denominator
magnitude 2-6s and |5s-1|<=1-3s. The two needed affine inequalities hold on
all of [0,1/4], so the contraction factor is at most 1/2. The entire interval
converges to zero and connects the point to the root inside the basin. Thus

    1/2 in U_(1/2)(0), but 1/2 not in U_1(0).

The asserted failure U_(1/2)(0) subset U_1(0) has the correct direction. The
opposite inclusion is not decided by this example. Scaling by 1/2 puts the roots
strictly inside the unit disk and preserves the conclusion.

For a justified rational extension of the proposed Blaschke model, the two
attracting fixed points at zero and infinity have multiplier lambda=1-h/m.
With the remaining fixed points repelling on the unit circle, the index formula
is

    2/(1-lambda) - sum_j 1/(mu_j-1) = 1,

so the packet's sum 2m/h-1 is correct. The special model G_t independently
checks this: its boundary fixed point has multiplier 2/(2-t), giving the same
index. The modulus pi/log(mu_j) agrees with the inspected fixed-parameter
channel construction. These conditional calculations do not supply a global
model for every allowed h, and do not align the channels for different h.
The rotating-semicircle control correctly blocks the proposed inference from
individual positive arc lengths to a positive common arc length.

## 6. Flow and compactness limitations

The Newton-flow identity d f(z(t))/dt=-f(z(t)) is valid away from nonremovable
poles. The packet's finite-time Euler statement is conditional on a compact
pole-free trajectory neighborhood, uniform finite-time control, and a strict
entry margin into the trapping region. Under those assumptions the claimed
small-step conclusion is standard and consistent. It is not a degree-only
estimate, an infinite-time shadowing statement, or a route to arbitrary h.
The compactness observation correctly requires a common starting set first.

The new endpoint controls also distinguish excluded variants. At h=0 the
one-root map is the identity; at h=2m it can be a sign-flip two-cycle. Positive
varying step sizes need not converge either: for m=1 and h_n=2^(-n-2), the
infinite product of 1-h_n stays at least 1/2. None of these is a counterexample
to the actual fixed-h interval in the packet.

## 7. Reproducibility and source/literature scope

Author replay: 788 rational local cases, 245 exact conjugacy cases, 1,225 radius
identities, the interval control, and all finite surveys matched. The finite
survey still certifies only sampled full-basin labels for one polynomial, five
h values and three radii. It certifies neither immediate components, intervals
between sample points, nor the parameter continuum.

Independent controls: 450 exact polynomial local-contraction cases and 180 exact
affine/two-root conjugacy cases, with t as small as 10^-50, root separations as
small as 10^-20, mixed multiplicities, imaginary-axis invariance, fixed-point
indices, endpoint failures, nonuniform convergence time and the off-center
control. `INDEPENDENT_CONTROLS.json` gives the reproducible result. These finite
checks supplement the general arguments above; they are not their substitutes.

All five cached scholarly PDFs and both complete public corpus files were
independently hashed and byte-counted; all matched the author's metadata.
Fresh PDF-to-text extractions matched the previously stored extraction files.
Only verification metadata is retained in `SOURCE_CHECKS.json`, not source text,
source PDFs, or corpus contents.

The independently inspected source passages support the packet's cautious
literature summary. Sutherland's thesis and Hubbard--Schleicher--Sutherland
supply fixed-map geometric background; the latter's relaxed-map remark concerns
fixed h in (0,1). Pal's 2026 v1 preprint uses an all-roots-attract parameter
convention based on minimum multiplicity. Its qualitative statements do not
supply this common-arc theorem. The packet is also justified in not relying on
its global Koenigs-conjugacy step: differentiating a putative univalent conjugacy
at a critical point conflicts with a nonzero linear multiplier, while a zero
linear multiplier would force the map to be constant. This is a specific proof
objection, not a verdict on every theorem in that preprint.

The Benzinger and Kriete original full texts were not newly recovered. The
historical seminar collection remains a lead rather than a proof certificate.
The literature search is bounded. No assertion that the conjecture is globally
unresolved in all literature is certified by this audit.

## 8. Publication boundary and reproducible use

Permissible mathematical status: unsolved in this attempt, with the stated
verified partial results and explicit global gap. This audit does not authorize
or certify a merge, release, DOI, remote update, queue mutation, or external
communication. None was performed by the reviewer. No helpers or additional
reviewers were used. Original files, history and evidence remain intact.

From this audit directory, with the author files kept alongside it:

    python audit_verify.py ../submission ../rank650-5300071-author-freeze.zip
    python ../submission/verify.py > replay.json
    python -c "import json; assert json.load(open('replay.json')) == json.load(open('../submission/CONTROL_RESULTS.json'))"
    python ../submission/verify_manifest.py
    python integrity_negative_controls.py ../submission

The portable audit archive excludes scholarly PDFs, extracted source text,
datasets, private coordination records and source-page images.
