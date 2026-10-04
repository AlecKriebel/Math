# Source and status gate — problem 30006308

Checked 2026-10-04 UTC. Rank 555, code OWR-14299288-014.

## Exact source target

The catalogue URL is https://www.unsolvedmath.com/problems/30006308 . A direct
request returned HTTP 403 (Vercel denial); web retrieval also failed. This is a
website-access failure, not mathematical evidence.

The matching catalogue record was recovered from the public Ulam AI
UnsolvedMath dataset, pinned at revision
`372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`:

https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json

The complete dataset file's SHA-256 is
`37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`.
Its local byte hash agrees with the LFS object hash returned by a fresh read of
Hugging Face's pinned tree endpoint. It contains 15,458 records; the matched
record has ID 30006308, the code above, and the requested title. The record
identifies *both* Questions 4 and 5 in the report. Its generated August 2026
literature assessment and “open” label were treated as search leads, not
mathematical authority.

The primary source is Sharon Robins's contribution, joint with Nathan Ilten,
“Locally trivial deformations of toric varieties,” in *Toric Geometry*,
Oberwolfach Report 19/2025, pp. 912–914, DOI
https://doi.org/10.4171/OWR/2025/19 . The question passage is on printed p. 914
(PDF page 32, zero-based index 31):

https://ems.press/content/serial-article-files/51856

PDF SHA-256:
`0511e00aa5e3c1b778f66f0e5b8fb00ab02b1103550bbd7941e2bd0c1bb62442`.
The local PDF was converted to text and the question page was also rendered and
visually inspected. The first displayed monomial there is `t3^2 t4`, not the
erroneous `t3^3 t4` produced in some search snippets.

Question 4 asks for tangent-cone determination; Question 5 asks for a relation
between the number of hull components and the number of first-order simplicial
complexes. The report does not specify a formula for Question 5, the equivalence
relation on “distinct” complexes, or that “any relation” means exact numerical
determination. Accordingly the proved count collision is explicitly narrower
than the catalogue's full two-question target.

## Updated primary mathematics and proof inspection

Nathan Ilten and Sharon Robins, *Locally Trivial Deformations of Toric Varieties*,
https://arxiv.org/abs/2409.02824v5 , revised 13 May 2026.

PDF: https://arxiv.org/pdf/2409.02824v5

PDF SHA-256:
`dd193430943321bff78810f8ea07ffee03cd47f0154167275f5de3225ab6002f`.

The current arXiv page identifies v5 as the latest version at this check and
states “To appear in J. Alg. Geom.” Ilten's
[publication list](https://www.sfu.ca/~nilten/pub.html) independently lists it as
forthcoming in that journal. This is not a claim that a final journal version
was inspected.

Relevant material read beyond the abstract:

- §§3.2–3.3 and Appendix B: the all-order hull construction, obstruction-space
  bound on equation generators, and the versality proof.
- §§4.3–4.4: the divisor complexes and generalized Euler-sequence comparison.
- Theorem 5.1.2 and complete proof: the graded Lie bracket.
- Theorem 5.1.4 and complete proof: equivalence with locally trivial deformations;
  smoothness makes these all deformations here.
- §5.2 and Proposition 5.2.1 with proof: the cochain lifting algorithm.
- The quadratic formula in Table 1, together with the defining bracket and BCH
  equation; only its second-order case is needed in the new verification code.
- Example 5.4.2, Theorem 5.4.4 with proof, and Lemma 6.4.1: the four-cone
  reduction used for the cycle calculation.
- Complete proofs of Lemmas 6.3.2–6.3.3, and the full relevant computations in
  Examples 6.4.2, 6.4.5, 6.4.6, including Tables 2–4 and Remark 6.4.7.

No assertion is made that every external foundational reference cited by those
proofs was independently re-proved or that the ancillary Macaulay2 code was run.
The public verification is a separate exact calculation of the finite degree,
quadratic cochain, and coordinate-change steps used here. In particular it does
not claim to reproduce an all-order hull computation for X(2,-4,4).

Version-sensitive correction: the rank-four quadric example is 6.4.5 in v5;
it was 6.4.4 in the 2025 report's numbering. On v5 p. 49, its final hull display
omits the free variable t7. The surrounding seven-variable equation and explicit
coordinate changes, its tangent dimension, the stated dimension-six conclusion,
and the OWR display confirm that t7 must remain. The page was rendered and
visually checked, and PROOF.md independently performs the seven-variable change.
No reliance is placed on the erroneous six-variable display.

## Prior-resolution check

Searches on 2026-10-04 included the exact title, the ID/code, “toric varieties
 tangent cone deformation,” “smooth complete toric 2026 deformation tangent,”
and combinations of Ilten, Robins, component counts, and deformation spaces.
The searches returned the 2025 report, the 2026 revision above, and adjacent
but different problems (affine toric singularities and moduli of maps).
The inspected current paper establishes explicit hulls and obstruction results,
not a general answer to either present question. In particular, its negative
answer to the older *quadrics-only* question is not a negative answer to
*tangent-cone determination*: homogeneous cubics also define cones.

No subsequent full resolution was found in these searches. This bounded search
result does not certify that no resolution exists anywhere, and is not a basis
for a novelty claim. The count-collision examples and their hulls belong to
Ilten–Robins; the package identifies a consequence of those examples.

## Actual repository-history check

Repository: https://github.com/AlecKriebel/Math . Read-only checks on
2026-10-04 found:

- `unsolved_math_prioritization/QUEUE.md` row 555 was `queued`, `0/5`, with empty
  Chat and Findings cells. Its fetched file blob was
  `c87c275c638939b8008fd58db80657491d14971e`.
- PR searches over all states for `30006308`, `OWR-14299288-014`, and the toric
  deformation title terms returned no matching prior PR.
- Branch and commit searches for `30006308` returned no matches.
- Repository code searches for `30006308` and `toric deformation` returned no
  matching attempt artifact. Code-search indexing is not exhaustive (it did not
  surface the known queue row), so the independent PR/branch/commit checks are
  recorded rather than inferring absence from the queue alone.

No prior attempt was located. There have been no remote writes for this packet
before independent review. The proposed final row status is `unsolved`, `5/5`,
with a finding that both broad questions remain unresolved and that only the
specified numerical determination versions of Question 5 are disproved.
Only this row's authorized cells should be changed during publication; no queue
script or unrelated row change is part of this packet.

## Public payload boundary

Publishable files contain original analysis, bibliographic pointers, and small
exact-check code/results only. No source PDFs, rendered source pages, extracted
source texts, catalogue record, full corpus, private context, or tool transcript
is included. Source material remains available at its cited original host.
The SHA-256 manifest binds the exact submitted public packet. It does not
constitute mathematical peer review or a proof of the unresolved assertions.
