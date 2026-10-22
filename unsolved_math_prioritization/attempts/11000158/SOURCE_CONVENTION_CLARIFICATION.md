# Required clarification: homeomorphism equivalence versus ambient isotopy

Target: 11000158 / AMR-109-0158. Date: 2026-10-03.

## What the source actually says

Birman's printed p.142 / PDF p.149, in the paragraph preceding equation (2),
says that the splittings are equivalent when their splitting surfaces are
isotopic; the paragraph also requires a diffeomorphism B whose restrictions
preserve the two pieces. The source wording is visible in the
[original page](https://math.uchicago.edu/~farb/papers/mcgbook.pdf#page=149).
The original packet's statement that its conventions simply come from
the surrounding discussion was therefore too seamless. In particular,
`PROOF.md` section 1 and `SOURCE_GATE.md` must be read with this qualification.

Problem 2.1 itself, on printed p.149 / PDF p.156, asks how the handlebody
double coset is modified for compression bodies and for a knot space. It
does not separately formulate an ambient-isotopy classification. See the
[problem page](https://math.uchicago.edu/~farb/papers/mcgbook.pdf#page=156).
Scharlemann's printed/PDF p.2 distinguishes isotopic splittings from
homeomorphic splittings explicitly:
[Heegaard splittings of compact 3-manifolds](https://arxiv.org/pdf/math/0007144v1#page=2).

## Adopted interpretation and exact mathematical boundary

The packet's equation (3) uses orientation-reversing gluing maps between
fixed compression-body models, modulo the positive-boundary maps that
extend over each piece and preserve the chosen boundary data. Its equation
(4) is the same orbit set after fixing the orientation-reversing
identification j. These data classify orientation-preserving,
side-preserving **homeomorphism equivalence of the specified splittings**.
Both directions of that assertion are proved in `PROOF.md` section 3.
This is the equivalence encoded by the boundary compatibility equation
used in Birman's equation (2).

Those unmarked gluing data contain no identification of each glued manifold
with one preselected ambient M. They also impose no requirement that an
ambient equivalence be isotopic to the identity in that M. Consequently
the same double coset cannot, by itself, be promoted to a classification
of embedded splitting surfaces up to ambient isotopy in a preidentified
manifold. Such a formulation would require additional ambient marking
data and restrictions on the allowable equivalences. No construction or
classification for that stronger formulation is proved here.

The credited prior-resolution recommendation thus applies to Problem 2.1
in its stated **double-coset sense**, using the homeomorphism-equivalence
interpretation made explicit above. If a downstream reader instead treats
the p.142 isotopy sentence as an additional literal requirement of the
target, this packet is narrower than that requirement, and full resolution
under that reading is **not established**. The qualification is mandatory,
not a proposed theorem closing the stronger question.

## Other qualifications remain unchanged

- The full extendible image, the image fixing the negative boundary, and
  the subgroup preserving a specified peripheral slope are different groups.
- A torus-boundary gluing represents a knot exterior in S³ only with the
  required S³ filling; arbitrary exterior maps are not assumed to preserve
  a chosen filling meridian.
- The quotient retains the chosen splitting and side assignment. It is
  not a unique classification of underlying manifolds after forgetting
  their splittings. Stabilization is a separate relation.
- Sphere counts and labels remain extra punctured-model data. No marking
  kernel is claimed to recover them.
- Barbar's connected-boundary relative double quotient is corroborating
  prior use, not the proof of every boundary/marking case in this packet.

## Audit provenance

This note implements the source-convention correction required by the
independent review dated 2026-10-03, whose SHA256 is
`fa1c9d686d37ee72f3ead8941c001483fc2d6c8bf13a5bb957518194ce8db4de`.
That review's manifest SHA256 is
`049f344207c40bf091719b4c2c1629edab904188b10a83cfd78ee6999815a8be`.
The audit accepted the mathematical homeomorphism-equivalence model;
it did not grant full-scope acceptance under a stronger ambient-isotopy
interpretation. The present additive wording still requires narrow review
before publication. The historical ten-file packet is preserved verbatim.
