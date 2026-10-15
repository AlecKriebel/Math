# Independent first assessment: singular braid family in PR177

Sealed independently on 2026-10-12 UTC, before any feedback to ROOT. Original
submission head supplied by ROOT: `cee82300baaa2e209aba8b62ae34673419237451`.
Problem: 10400049. This assessment is mathematical verification within the
explicit finite-order, characteristic-zero model, not a priority determination.
Family completion estimate at this checkpoint: 85%. Overall case estimate last
supplied by ROOT: 15%; science acceptance and priority are not started here.

## Provisional finding

I find no fatal topological or finite-order defect. The candidate's central
lemma, and hence its principal-ideal counterexample to the literal arbitrary-
ideal question, is valid in the stated uncompleted algebra of ordinary links.
The proof below was reconstructed through a local immersed-braid diagram and
resolution cube, without reading or running the submission's verification code,
author reviews, readiness statements, ROOT's analysis, or other audit families.

There are two presentational limits. Printed p.398 defines finite type for
oriented **knots**; the same local definition for disjoint unions of circles is
the link convention used here, rather than a separate explicit definition on
that printed page. The author archive displays a June 2001 posting label and
a July 2011 notebook/export date. These verify the formulation and are not a
new historical-priority finding. The linking-number-generator example remains
undecided by this argument.

## A geometric mechanism independent of Laurent-braid factorization

Work in a cylinder with height coordinate t, with both strands oriented toward
increasing height. A crossing unit consists, in a local chart, of arcs

    a_e(t)=(-1+2t, e*4t(1-t), t),
    b_e(t)=( 1-2t,-e*4t(1-t), t),   0 <= t <= 1.

Rounded corners concatenate these units without further intersections. At e=0
there is one double point at t=1/2 with independent tangent directions
(2,0,1) and (-2,0,1). At e=+1 and e=-1 the arcs are disjoint and have opposite
over/under crossings. Choose the chart's projection/sign convention so e=+1 is
the standard positive generator. Crucially, all three units exchange endpoints;
e=0 is an immersion with two specified arcs, not a four-valent graph surgery or
smoothing. This construction gives an actual singular braid with a domain of
two intervals and one double point per zero unit.

Concatenate 2n positive units, followed by r separated pairs consisting of one
positive unit and one zero unit. Each pair has identity endpoint permutation,
as does the prefix. Close each bottom position to its corresponding top
position along the standard exterior arcs. Tracking the two interval labels
shows the immersion's domain consists of two circles. Resolving a zero unit
does not change endpoint connections, so every one of the 2^r resolutions has
exactly two components. Additional split circles are untouched.

For any subset S of the r singular sites, resolve sites in S positively and
the others negatively. A positive resolution gives two positive crossing units.
A negative resolution gives a positive/negative pair that is removed by the
local Reidemeister-II isotopy relative to its endpoints. These are disjoint
local isotopies. After removing the negative pairs the diagram is the closure
of 2(n+|S|) positive crossing units, namely L_(n+|S|).

Using the local positive-minus-negative convention, the singular value is

    sum_{S subset {1,...,r}} (-1)^(r-|S|) v(L_(n+|S|))
      = sum_{j=0}^r (-1)^(r-j) C(r,j) v(L_(n+j)).

This is Delta^r(v(L_n)). This derivation uses the actual immersion, endpoint
tracking, and local isotopy certificates, not the formal factorization
`(sigma^2-1)^r = sigma^r(sigma-sigma^-1)^r`. If v has order at most d, the
constructed (d+1)-double-point immersion is within the defining vanishing
condition for every n>=0. Thus Delta^(d+1)(v(L_n))=0 for every n, regardless of
what v measures beyond linking number. This is the essential universal step.

## Orientation, labels, framing, and mixed crossing counts

Both resolved strands retain the orientation of their immersed interval. A
positive unit in the coherent closure has positive crossing sign; every crossing
is between the two different circle labels. The signed mixed-crossing sum for
L_n is 2n, so its linking number is n, not 2n. For n=0 the closure is the unlink.
Permuting component labels changes no sum of squared linking numbers. Reversing
component i multiplies each incident linking number by -1, so their squares are
unchanged. Choosing labels and orientations temporarily on an arbitrary
resolution cube is legitimate because crossing resolutions do not change the
circle domain or its labels.

The source's ordinary isotopy convention does not retain a framing. This proof
uses no Reidemeister-I move: the cancellation is a Reidemeister-II move between
distinct components, so it also introduces no blackboard self-writhe. No
framing correction or writhe normalization enters the stated unframed proof.
The diagram model independently checks no self crossings in these resolutions.
A result for a differently defined completed/framed algebra is outside the
candidate's claim and is not silently supplied by this audit.

## Finite type of g and the product-order rule

Fix an arbitrary link immersion with q double points and temporarily label and
orient its component circles. Let x_a=0 or 1 select the negative or positive
resolution at site a. Each pairwise linking number has the form

    ell_ij(x)=ell_ij(0)+sum_a epsilon_(ij,a) x_a,

where epsilon is +/-1 if site a is between those two circles and 0 otherwise.
This follows from the signed mixed-crossing formula; a self crossing has no
effect on a linking number. Hence g=sum ell_ij^2 has degree at most two on every
resolution cube, for every finite component count. Its third mixed difference
vanishes. The number of summands can increase with the component count while
the degree bound remains two. Thus g is globally finite type at most two.

For completeness, an order-d invariant on any q-point cube has a unique
multilinear expansion sum_A c_A product_(a in A) x_a. Its coefficient c_A is the
mixed difference on the A-sites with the other sites fixed negatively. It is
zero for |A|>d: resolve the extra |A|-(d+1) sites first and use order-d
vanishing on each resulting (d+1)-singular link. Products of expansions of
degrees d and e have degree at most d+e after reducing x_a^2=x_a. This proves
the finite-type product rule without assuming it. In particular f=4g^2-g has
order at most four uniformly in component count.

## Newton interpolation on the entire algebra

For a sequence a_n with Delta^(d+1)a_n=0 for every n>=0, define

    Q(t)=sum_(r=0)^d C(t,r) Delta^r a_0.

Characteristic zero permits the denominators r!. The identity
Delta C(t,r)=C(t,r-1), or induction on n using the same (d+1)-st-order linear
recurrence and the first d+1 values, proves Q(n)=a_n for every n>=0. Uniqueness
holds because nonzero polynomials over a characteristic-zero field have only
finitely many roots. Thus each finite-order v determines a unique polynomial
P_v of degree at most its order.

This definition is intrinsic, so choosing a larger admissible order produces
the same polynomial. Given v,w with possibly different orders, their product
has finite order by the cube argument. P_(vw) and P_v P_w agree at every n>=0,
as do the polynomials needed for additivity and preservation of scalars. The
root argument proves exact equality. This constructs a unital algebra map on
the entire finite-order algebra, not just C[g] or a common-degree truncation.
For all finite-component links, use the two-component family to restrict the
global algebra; for fixed m>=2, add m-2 fixed split circles. Both constructions
preserve the requisite finite-order vanishing.

## Independent radical obstruction

On actual links g is a sum of integer squares and so is a nonnegative integer.
Consequently f=g(4g-1) vanishes exactly when g=0, equivalently all pairwise
linking numbers vanish. The unlink proves this zero set is nonempty. For the
principal ideal I=fV, the same set is its common actual-link zero set. Therefore
g is in its vanishing ideal J.

Evaluation of the polynomial map at t=1/2 gives a character chi of the full
algebra. The mixed-crossing computation gives P_g=t^2, so chi(g)=1/4 and
chi(f)=0. If g^N=fh for any N>=1 and h in V, applying this character gives
(1/4)^N=0, a contradiction. Hence g is outside radical(I). The obstruction
holds in characteristic zero even over an algebraically closed coefficient
field. It answers the arbitrary-ideal equality negatively under the stated
model. It does not identify J for the different ideal generated by linking
numbers and does not decide a repaired formulation.

## Exact controls and negative mutations

My independently written `independent_controls.py` imports no candidate code.
It tracks interval identities and closure gluing, computes mixed crossing sums,
records Reidemeister-II cancellation certificates, expands resolution cubes by
Mobius inversion, and computes Newton values with rational arithmetic.
Normal Python and Python -O both passed: 2,555 resolved diagrams, 10,220
closure/linking cases including 0/1/5/100 split additions, 225 grouped skein
coefficient cases, 3,645 cube-order cases, 384 orientation/label cases, and
additional exact polynomial and zero-locus controls. These are finite support
for the written all-invariant proof, not a substitute for it.

Eight deliberately false mutations were rejected in both modes: deleting the
ordinary companion crossing; substituting a smoothing; starting at odd braid
exponent; using positive-plus-positive extension; reusing one site for two
independent bits; identifying linking number with crossing count; assigning g
order at most one; and omitting the Newton factorial. Acceptance uses explicit
exceptions rather than removable `assert` statements.

## Source access and provenance limits

Only the supplied full CANDIDATE.md, source_record.json, and
source_manifest.json were read from the original submission. Their exact
paths, SHA256 hashes, and byte counts appear in INPUT_RECEIPT.json. No Git,
index, ref, checkout, tracker, author PR, publication, or original verifier was
modified or inspected. No people were contacted.

I downloaded two primary PDFs independently via their public HTTPS URLs and
recorded timestamps, status, resolved URL, content type, SHA256, and bytes in
private_sources/access_receipts.json. Hashes match the supplied manifest:

* Publisher PDF: 4,731,008 bytes; SHA256
  `33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd`.
* Author one-page PDF: 274,887 bytes; SHA256
  `59e99f21fb86be4b0cfca87717938cf7d27196ae66248c0e7bfee35fb0dd6e8c`.

The scientific reading was the complete rendered and extracted printed p.398
(PDF page 26), complete printed p.422 (PDF page 50), and complete one-page author
question. I inspected all three rendered page images, including the singular
resolution diagram on p.398. The source browser also returned incidental
neighboring text snippets from printed pp.396-399 and 421-424, plus table-of-
contents/preface material; these were not a complete reading of those sections.
I read the author June 2001 archive index as rendered web text, but did not
independently hash that HTML response and do not claim its full body was
downloaded. I did not read Appleboim, Ng, or Eisenbud bodies. Priority and current
literature status remain unestablished. Third-party source bodies, extracted
text, and rendered pages are private and excluded from the public allowlist.

Primary source locations: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
(printed pp.398,422), https://drorbn.net/AcademicPensieve/2001-06/ and the
linked one-page author PDF recorded in the access receipt. No verbatim source
passages are copied into this assessment.
