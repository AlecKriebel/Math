# Independent source-scope review: PR948 / 30004549

Recorded 2026-10-16. Scope is the exact source category, both target clauses,
the credited generic theorem, and the withdrawn manuscript's evidentiary status.
This review does not certify the candidate mathematics, novelty, or present priority.

## Finding

The candidate addresses the source category of the integrability question. The
source imposes no fixed metric, fixed symplectic form, compatibility, taming, or
real-analytic requirement. Its smooth closed connected example, if valid, would
answer that question negatively. The generic clause has an independently
located prior theorem, and must receive prior credit rather than new-result credit.

## Primary statements and scope

The official [MFO report](https://publications.mfo.de/bitstream/handle/mfo/3805/OWR_2020_33.pdf?isAllowed=y&sequence=4)
and [EMS report](https://ems.press/content/serial-article-files/46869?nt=1),
printed p.1687 / PDF p.31, give Conjectures 2.4 and 2.5 respectively as generic
vanishing and the implication from h_J^- >= 3 to integrability on compact
four-manifolds. The preceding definitions use real closed anti-invariant
two-forms and identify their dimension with anti-invariant cohomology in this
dimension. Printed pp.1688-1689 distinguish noncompact and higher-dimensional
examples and a separate bound for symplectically tamed structures. Those examples
and bounds do not restrict the conjecture to those classes.

[Draghici-Li-Zhang, arXiv:1104.2511v1](https://arxiv.org/pdf/1104.2511),
printed/PDF p.5, is the primary origin of both numbered conjectures. Section 2,
pp.3-4, defines forms as C-infinity sections and anti-invariance by the -1
eigenspace of alpha(X,Y) -> alpha(JX,JY). Its real cohomology classes are those
with closed representatives of the appropriate sign. A J-compatible metric
makes a closed anti-invariant two-form self-dual and harmonic, so an exact one
vanishes; this explains the forms/classes identification. Neither conjecture
requires a symplectic form. The metric-related hypothesis belongs to their
separate Theorem 1.1 on p.2, not Conjecture 2.5.

[Tan-Wang-Zhang-Zhu, arXiv:1112.0768v3](https://arxiv.org/pdf/1112.0768v3),
printed/PDF p.2, Theorem 1.1, concerns every closed four-manifold admitting an
almost complex structure. It says the vanishing locus is open and dense in the
space of all smooth almost complex structures with the C-infinity topology.
Section 3, pp.6-12, defines that topology using every C-k seminorm. Its density
construction chooses a compatible metric at the starting structure; its openness
argument on p.9 permits arbitrary converging structures and constructs varying
compatible metrics. Thus the theorem is not confined to one fixed-metric family.
The [publisher record](https://link.springer.com/article/10.1007/s12220-014-9477-2)
confirms all four authors, J. Geom. Anal.25 (2015),1431-1443, DOI
10.1007/s12220-014-9477-2; online publication was 21 March 2014. Full theorem
inspection here used the author-hosted arXiv version, not a subscription PDF.

The current [Lejmi-Upmeier arXiv record](https://arxiv.org/abs/1507.00282)
identifies v2, 3 September 2015, as withdrawn. The stated cause is a crucial sign
error in the proof of Proposition14. The abstract describes an almost-Kahler
integrability claim, but the withdrawal prevents using it as an established
theorem or an obstruction to this candidate. This check neither proves nor
disproves any repaired version elsewhere; that belongs to later priority work.

## Category checks and deductions

| Issue | Audit conclusion |
| --- | --- |
| Regularity | Smooth category is supported by the explicit C-infinity definitions and cutoff deformation context. No analytic qualification occurs in the conjectures. |
| Real dimension | Four is real dimension: two-forms split into self-dual and anti-self-dual bundles, and the examples are complex surfaces. |
| Compact versus closed | The displayed conjectures say compact. Boundarylessness is the ordinary Hodge-theoretic setting used in their surrounding arguments; no boundary problem or boundary conditions are supplied. The candidate is closed, so it satisfies the stronger unambiguous case. |
| Connectedness | The displayed conjectures do not explicitly say connected. Connectedness is used elsewhere in the sources. No unsupported global convention is imposed here; the candidate is connected and therefore meets either intended reading. |
| Orientation | J supplies an orientation. No additional fixed orientation appears in the conjecture. The separate metric-related notion requires compatible orientation. The candidate uses its product complex orientation. |
| Forms versus classes | Independent de Rham classes imply independent closed forms. In the compact boundaryless four-dimensional setting the harmonic argument also gives the converse identification. |
| Exact h_J^- | The integrability implication is triggered by a lower bound of three; computing the exact dimension is unnecessary. |
| Generic theorem versus special example | An open dense vanishing locus allows exceptional structures. The two clauses are logically distinct. |

There is also a direct check against accidental application of the metric-related
theorem. On the candidate's cutoff-one region let k=1-epsilon*x. Its displayed
structure has J_epsilon(partial_u)=k^(-1/2)partial_v, whereas
J_0(partial_u)=partial_v. If a positive metric g made both structures orthogonal,
then g_uu=g_vv and g_uu=k^(-1)g_vv. Positivity forces k=1. For nonzero epsilon
there are nearby points with k != 1, so a common compatible metric is impossible.
This is a scope deduction from the frozen formulas, not a new repair or a
certificate of the rest of the construction.

## Evidence quality and qualifications

All24 original regular100644 files match the preserved record by SHA256, size,
Git blob encoding, and subsequent direct pinned git-show comparison. The original
head is be4313efafa1af5962394e07d8a4debff2e94d92. The selected statement's
SHA256 was independently reproduced. The raw SQLite review-hash match is read
from the root's preflight, not independently queried in this source family.
No earlier audit verdict was read before this interpretation or subsequently.

The actual intake sequence is recorded in AUTHENTICATION_END.json: gate and
snapshot metadata preceded source intake, but the selected raw record and first
web primary text preceded this reviewer's computed24-file authentication receipt.
The request required the complete authentication before any source reading;
this ordering deviation is explicitly disclosed. Downloads and all personal
rendered-page inspections followed the computed receipt. No timestamps are
backfilled and no stronger procedural certificate is asserted.

The two OWR downloads have different bytes, extracted texts, and rendered-page
hashes. Both decisive pages were personally rendered and read; their conjectural
content agrees. No byte-identity or full-text-equivalence certificate is claimed.
OWR p.1687 has a sign reversal in one prose description of the eigenbundles;
the displayed sign formula, real (2,0)+(0,2) identity, and primary DLZ definitions
resolve the intended anti-invariant convention.

The selected source's abbreviated Tan-Wang-Zhang citation omits Zhu. Its report
label contains 2021, whereas the MFO cover and official bibliographic record say
OWR17 (2020),1657-1691, and the meeting was 4-10 October2020. These bibliographic
details should be corrected in any final package. A DOI resolver failed through
the web tool, while the direct official PDF URLs worked. The Springer landing
page is subscription preview; no assertion of publisher/arXiv byte equivalence
is made. Small JPEG renders streamed through memory avoided intermittent ENOSPC;
the public evidence contains only hashes and inspection records.

The exact remaining gap is full mathematical adjudication by the independent
families, then fresh deep priority/current-status work and whole-package review.
The older source triage's partially-solved/open label was not accepted as evidence.
This family's source-scope work is complete (100%); the broader research goal
remains unadjudicated. New author proof responses:0; declared4/5 history is not
independently reconstructed here. No external individual was contacted and no
branch, index, HEAD, ref, original, status ledger, or remote service was changed.
