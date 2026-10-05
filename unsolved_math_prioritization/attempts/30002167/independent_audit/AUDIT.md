# Independent adversarial audit: problem 30002167

Audit date: 2026-10-05 UTC.

## Verdict and exact scope

**PASS: a valid partial counterexample to the radius-one planar disk Hamiltonian-cycle bound 8, as explicitly printed on page 2488 of Oberwolfach Report 40/2012.** No mathematical defect was found in the analytic six-point proof, its optional exact optimum, the three-point obstruction, or the necessary lower bound 9 on any universal replacement constant.

This is not a resolution of the separate perfect-matching bound 4 or the general other-convex-body question. It does not prove a universal upper bound 9. The audit does not establish novelty, priority, current global openness, or agreement with the inaccessible aggregator page or raw AI records. One substantive mathematical approach is recorded, not five. The frozen candidate's pending-audit fields remain unchanged; this separately bound audit supplies the independent result.

## Frozen input binding

The audit covers exactly the ten payload files listed in the candidate's 1,395-byte MANIFEST.json, with SHA-256:

e2645129ee536f33d58415f04b45323c816ffb3706ef02101e78de2172049180

All ten payload byte counts and hashes match. They total 23,472 bytes; including the manifest, the frozen packet totals 24,867 bytes. The input was checked before and after independent computation and was unchanged. INPUT_BINDING.json and EXACT_RESULTS.json retain the per-file binding. No candidate file was edited, no helper agent was used, and no remote write was made.

## Primary formulation and provenance

The supplied TIB PDF was hashed, freshly text-extracted, rendered, and visually inspected at PDF page 60 / printed page 2488. A fresh official EMS PDF was independently downloaded and inspected the same way. Both specify a planar disk of radius one, a Hamiltonian cycle whose squared edge lengths are summed, and threshold 8. Even cardinality qualifies the separate perfect-matching threshold 4. The preceding discussion returns from general dimension to planar squared costs. There is no stated restriction to boundary points or convex position.

The supplied TIB PDF is 2,390,786 bytes with SHA-256 100a7fbd6f82fdd9bdbbeedca1c8e3ce5e71b52ec2a5ed1d73f6ddd9c88cfb1a. The newly fetched EMS PDF is 2,426,569 bytes with SHA-256 9e3adbbc7530837df9e73a51f0792af7d657de87f18db360cf74e8f0de52a920. These are distinct PDF artifacts; their hashes must not be interchanged. Whitespace-normalized text of the complete Musin subsection is identical in the two extracts. No PDF, image, or extracted source text is included in this audit's safe packet.

The subsequent four-point remark does not explicitly say which subquestion it addresses. It does not override the explicit problem or add a hypothesis. This audit makes no claim about the author's unstated intention or whether the printed constant was a historical error.

The exact aggregator URL independently returned HTTP 403. Its page text remains uninspected. The raw AI corpora remain unavailable and uninspected. Accordingly, the rank, identifier, and record-to-primary mapping are supplied task metadata, not independently verified raw-record matches. Earlier repository/history search results in the candidate log were not independently repeated in this mathematical audit.

Sources:

- EMS publisher record: https://ems.press/journals/owr/articles/12012
- Report DOI: https://doi.org/10.4171/OWR/2012/40
- Fresh official PDF: https://ems.press/content/serial-article-files/46409?nt=1
- Candidate TIB PDF URL: https://oa.tib.eu/renate/server/api/core/bitstreams/045acad9-ea44-4831-af0c-05c431813bad/content
- Exact inaccessible aggregator: https://www.unsolvedmath.com/problems/30002167

## Model audit

Under the standard geometric meaning used here, the vertices are exactly the finite set P; edges join pairs of its points, every vertex has degree two, the graph is connected, and the closing edge is included. Thus a Hamiltonian cycle is not an open path or a disconnected cycle cover. All six-point tours are considered, including crossing tours. Proving a lower bound for this larger class also covers a noncrossing requirement. Added Steiner points, repeated visits, an average per edge, diameter-one normalization, or a square of total length would change the problem rather than repair the printed assertion.

The issue is substantive: an independent dynamic program finds an open-path optimum of 55473/10000, below 8. Scaling all coordinates by one half produces a radius-one-half instance with tour optimum 41839/20000, also below 8. Thus neither a missing closing edge nor a radius/diameter substitution can be silently accepted by the audit.

## Analytic proof audit

The six coordinate numerators are (95,0), (96,0), (-50,83), (-51,83), (-50,-83), (-51,-83), with denominator 100. They are distinct. Their squared norms have numerators 9025, 9216, 9389, 9490, 9389, 9490 over 10000, all strictly below 1.

For the displayed three pairs A, B, C, the least squared intercluster distances are 27914/10000 for A-B and A-C, and 27556/10000 for B-C. In any Hamiltonian cycle and each proper nonempty cluster S,

2|S| = 2e(S) + |delta(S)|.

The cut is positive by connectedness and even by this equation, so it has at least two edges. Summing over the three clusters counts each intercluster edge twice. There are therefore at least three such edges. The total squared cost is at least 3 times 27556/10000, namely 20667/2500. Its excess over 8 is 667/2500. This argument needs no optimization program or floating-point tolerance.

The triangle argument is valid: three equilateral unit directions give three squared edges of length 3, hence cost 9. A common radius r strictly between sqrt(8/9) and 1 puts the triangle in the open disk while retaining cost above 8. The six-point instance independently handles even cardinality, distinctness, strict interior containment, and any objection to three-vertex conventions.

The fixed-cardinality limiting argument is also sound. For each n at least 3 and epsilon in (0,1), allocate n distinct points among three nonempty radial clusters with radii in (1-epsilon,1). Between distinct equilateral directions, squared distance is r^2+s^2+rs, strictly exceeding 3(1-epsilon)^2. The cut argument gives tour cost greater than 9(1-epsilon)^2. For every K below 9 one can choose epsilon sufficiently small to exceed K. This proves a necessary bound K at least 9 for each fixed n at least 3, including every even n at least 4. It neither attains 9 in the open-disk limit nor proves 9 sufficient.

## Independent finite controls

The audit program imports no candidate code. It constructs all 15 edges of K6 and inspects all 5,005 six-edge subsets. Exactly 70 have degree two at every vertex. Ten are disconnected pairs of triangles and are rejected. The other 60 are all undirected Hamiltonian cycles. This is an independent enumeration route from the candidate's fixed-first-vertex permutation/reversal method.

The exact minimum is 83678/10000 = 41839/5000. Exactly two undirected edge sets attain it. The supplied witness (0,1,2,3,5,4,0) has edge numerators 1, 28205, 1, 27556, 1, 27914. A separate Held-Karp subset dynamic program, run with each of the six starting vertices, independently returns numerator 83678 every time. EXACT_RESULTS.json records every pair distance, cost histogram, optimal edge sets, and crossing-count histogram.

The audit also inspects all 455 three-edge subsets. Exactly 15 are perfect matchings. Their minimum numerator is 3, achieved by the three short cluster edges. Every edge has numerator at least 1, so this matching optimum has an independent analytic proof. A bad or expensive tour does not imply an expensive optimal matching; alternating an even tour supplies only the implication from a tour upper bound K to a matching upper bound K/2.

## Adversarial rejection tests and replay

Fifteen independent negative controls reject: false tour minimum, false analytic bound, false cycle count, false matching minimum, wrong coordinate denominator, a repeated-vertex witness, a disconnected 2-factor, a path missing its closing edge, a payload-byte mutation, an extra file, a missing file, a payload symlink, a manifest symlink, a nested directory, and a reauthored manifest whose new hashes agree with a changed payload but whose manifest anchor differs. All mutations occur only in disposable copies.

Normal Python and optimized Python produce byte-identical independent results. The candidate manifest, exact checker in both modes, and original eight negative controls in both modes also pass from an unrelated working directory. REPLAY_RESULTS.json retains those results. The candidate manifest checker is an integrity check relative to a manifest, not an external authenticity guarantee; the independent script adds the supplied manifest SHA-256 anchor explicitly.

## Literature and remaining limits

The supplied Bern-Eppstein PDF hash and size match the candidate metadata. Its first two pages were independently extracted and checked, and the author-hosted public PDF was opened. Its setup optimizes ordinary edge length before evaluating powers, so its logarithmic lower bound is not an unboundedness result for tours selected to minimize squared cost. The inspected author-hosted version has nine pages and is dated November 10, 1992; the candidate's 1993 proceedings entry is bibliographic metadata and should not be mistaken for the exact edition inspected. No full proof audit or fresh exhaustive literature search was performed.

Author-hosted paper: https://ics.uci.edu/~eppstein/pubs/BerEpp-SCG-93.pdf

The matching question, other convex figures, exact best universal constant, global historical status, and inaccessible-record correspondence all remain outside this PASS. No publication-ready novelty claim follows from independent arithmetic and proof checking.

## Reproduction

Run python3 -B audit_exact.py with the frozen candidate directory as its optional argument. Run again with -O. Compare JSON output with EXACT_RESULTS.json. The default path expects the original sibling layout; an explicit input path supports relocation. The script uses only Python's standard library and makes no network calls. The audit's own MANIFEST.json binds its payloads; its hash must be supplied separately when this packet is transferred.
