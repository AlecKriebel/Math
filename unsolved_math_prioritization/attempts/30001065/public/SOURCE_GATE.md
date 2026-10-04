# Source and scope gate

Checked 2026-10-04 UTC. **Primary mathematical target recovered; full original
target unresolved.** The catalogue endpoint itself was not retrieved.

## Identity and exact question

The repository queue names rank 552 as 30001065 / OWR-2090-018,
“Universal Optimality of Exceptional Spherical Codes.” The primary source is
Achill Schürmann's contribution “Universally optimal and balanced spherical
codes” in *Discrete Geometry*, Oberwolfach Report 44/2008, printed
pp.2538–2541; the question is on p.2539.

* [Publisher report page](https://ems.press/journals/owr/articles/2090)
* [Complete original report PDF](https://ems.press/content/serial-article-files/46191?nt=1)
* [Report DOI](https://doi.org/10.4171/OWR/2008/44)
* [Catalogue endpoint, inaccessible in this pass](https://www.unsolvedmath.com/problems/30001065)

The question asks for universal optimality of two specific codes: 40 points
in R^10 and 64 points in R^14. The report defines unordered-pair energy
using squared Euclidean distance on the unit sphere and completely monotonic
potentials on (0,4]. The comparison class is every code of the same size in
the same dimension. No fixed distance distribution, symmetry, integrality,
association-scheme, or coordinate-cube restriction is imposed.

The adjacent question about balanced versus group-balanced configurations is
a different target. So are lattice energy minimization and E8/Leech optimality.

The catalogue fetch returned HTTP 403 with a Vercel denial, and web retrieval
also failed. The title-to-primary-source identification is based on the queue
entry and the matching original report passage, not on a recovered catalogue
transcription. The original mathematical statement itself was read in full.

## Construction and proof sources actually inspected

1. **BBCGKS**, *Experimental study of energy-minimizing point configurations
   on spheres*, Experimental Mathematics 18 (2009), 257–283,
   [arXiv:math/0611451v3](https://arxiv.org/abs/math/0611451v3),
   [journal DOI](https://doi.org/10.1080/10586458.2009.10129052).
   Read §1.2 and all of §4.1–§4.2, including the parity construction for
   C40, the full one-parameter rival, and Table 12's F8 Gram construction for
   C64 (preprint printed pp.30–33). The rival comparison is explicitly left
   unproved in §4.1. This packet uses and credits those constructions. The
   locally inspected document is the arXiv preprint, not an asserted reading
   of the journal-layout version. Both Gram constructions are independently
   reconstructed and verified exactly in the checker.

2. **Cohn–Kumar**, *Universally optimal distribution of points on spheres*,
   JAMS 20 (2007), 99–148,
   [arXiv:math/0607446](https://arxiv.org/abs/math/0607446),
   [DOI](https://doi.org/10.1090/S0894-0347-06-00546-7).
   Read the exact sharp-design theorem, the potential-class reduction on
   p.106, Hermite interpolation discussion, and Proposition 4.1 with its
   complete proof and equality conditions on pp.119–121. The design
   hypotheses do not hold for either target. Our low-degree proof is given
   directly via tensors, and the all-degree LP obstruction has its own
   analytic tail argument.

3. **Cohn–Woo**, *Three-point bounds for energy minimization*, JAMS 25
   (2012), 929–958,
   [arXiv:1103.0485](https://arxiv.org/abs/1103.0485),
   [DOI](https://doi.org/10.1090/S0894-0347-2012-00737-1).
   Read Lemmas 9–10 and Corollary 11 with their proofs, pp.944–946.
   They justify the Hermite/Newton reduction; their warning that this
   sufficient strengthening need not follow from universal optimality is
   retained. No projective-space theorem is misapplied as a spherical-code
   resolution.

4. **Boyvalenkov–Dragnev–Hardin–Saff–Stoyanova**, *Universal lower bounds
   for potential energy of spherical codes*,
   [arXiv:1503.07228v1](https://arxiv.org/abs/1503.07228v1),
   Constructive Approximation 44 (2016), 385–415,
   [DOI](https://doi.org/10.1007/s00365-016-9327-5).
   Read the normalized recurrence, LP-universality definition, and §4.3–4.4,
   including Theorems 4.10–4.11 and their proofs in the inspected arXiv PDF.
   The journal's related result is numbered 4.12. This prior work already
   establishes non-LP-universality of (10,40) and (14,64). Its numerical
   table is not treated as an exact certificate in this packet. Our narrower
   quartic-attainment obstruction is proved directly. Non-LP-universality
   is not non-universality.

5. **NIST DLMF 18.10.4**, the normalized ultraspherical Laplace integral,
   [exact formula](https://dlmf.nist.gov/18.10.E4).
   Read the formula and parameter restrictions. With DLMF alpha=(n-3)/2,
   its integral is expectation over one coordinate of S^(n-2). This is the
   source of the all-degree tail bound; the moment normalization and the
   two rational tail constants are checked separately.

## Recent results checked and why they do not settle the target

* **Cohn–de Laat–Leijenhorst (2024)**,
  [Optimality of spherical codes via exact semidefinite programming bounds](https://arxiv.org/abs/2403.16874).
  Read Theorem 1.1 and the complete §4 proof of Theorem 4.1. Its universal
  theorem concerns 288 points on S^15, not 64 points on S^13. The names
  “Nordstrom–Robinson” and “Kerdock” occur in several different constructions;
  they do not license transfer after shortening or deleting points. The
  theorem's finite SDP certificates were not replayed, because no result
  depending on their validity is asserted here; its exact stated scope
  already excludes this target.
* **Boyvalenkov–Cherkashin–Dragnev**, revised 17 May 2026,
  [Universal optimality of T-avoiding spherical codes and designs](https://arxiv.org/abs/2501.13906v2).
  Inspected its model definitions and named code families. The comparison
  class excludes specified inner-product intervals. No unrestricted theorem
  for the two present codes was found. This is not used as a proof input.
* [Cohn's harmonic-optima page](https://cohn.mit.edu/harmonic-optima/)
  still lists these two configurations as conjectural. The same page has a
  dated general “no other known” sentence superseded by the 2024 288-point
  theorem. Therefore it is used for identification and distribution data,
  not as an exhaustive up-to-date literature certificate.

The literature search did not find a full resolution. Absence from the
searched sources is not a proof that no resolution exists anywhere. No
priority or first-resolution claim is made for the restricted results either.

## Prior repository work check

The actual `AlecKriebel/Math` default/main queue was read through the GitHub
connector. Its target row was `queued`, `0/5`; its title and ID agree with
the assignment. Exact-ID PR search and branch search returned no matches.
Searches for the exact title and “universal optimality” also returned no PR
matches. A conventional attempt README at
`unsolved_math_prioritization/attempts/30001065/README.md` was absent (404).
These checks found no prior target attempt; they do not claim to exhaust
every possible historical file name. A read of the large catalogue JSON
returned metadata but no content, and a blob read failed with transport
closure; neither was counted as an inspected target record.

No remote changes were made during this author pass. The intended queue
edit, after an independent gate passes, is only this row's Status to
`unsolved` and Turns to `5/5`; all other cells and rows are to be preserved.

## Reproducibility and distribution boundary

SOURCE_HASHES.json records source URLs, sizes and SHA-256 hashes of local
PDFs. Those PDFs and their full text extractions are not part of the public
packet. The public checker needs no source files, network, corpus, or private
conversation material. Its finite certificates support only the scoped
theorems explained in PROOF.md. The original global question is still open
in this work.
