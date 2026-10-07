# Regular-pentagon polyhedra: bounded investigation

## Outcome

5500072 / AMR-054-0072, queue rank 929: **stalled partial**, 3/5 substantive approaches used. No full proof, counterexample, or prior literature resolution was established. The authored mathematical result is the local four-valent obstruction in `proof_note.md`; it is not asserted to be new.

## Identity and prior-work gate

The current default-branch queue identifies rank 929 with this exact ID and title, at queued 0/5. Its observed Git blob SHA was 03f0ef6adc2b8d550f8b2b370f63689d72757553. All three complete corpora matched their supplied byte counts and SHA-256 values. The exact inherited research report contains literature/status triage only, with no substantive proof attempt. It therefore passes the no-repeat gate. The absence of exact-ID GitHub search results is supplementary, bounded evidence, not proof of no prior work.

The input diagnostic uses the whole problem record and `reports.get(problem_number,{})`, serializes the two-element list with Python `json.dumps(...,sort_keys=True)` and default remaining options, and compares its SHA-256 to the catalog's review hash. It does not project fields. The expected pair hash is 8b339393cebf5ccaee4df9fcd5290875ff54c34aa811cee58f9041e9d54df4c5; the serialized pair is 3,943 UTF-8 bytes.

The requested [UnsolvedMath page](https://www.unsolvedmath.com/problems/5500072) returned HTTP 403 to direct retrieval and could not be opened with web retrieval. Its live contents were not inspected. Identity and archived statement checks use the hash-pinned complete corpus, corroborated by the actual public source below. This access limitation is not hidden.

## Source reconciliation

1. [TOPP Problem 72](https://topp.openproblem.net/p72), consulted 2026-10-06, currently labels the problem Open and separately says the embedded version is open. It attributes the question to Richard Kenyon in 2006 and records a January 2009 restatement. This is maintained-source status evidence, not an exhaustive literature theorem.

2. The actual earlier source is **Discrete Differential Geometry**, Oberwolfach Report No. 12/2006, workshop March 5-11, 2006, Problem 4 on printed p.693 (PDF p.41). [Public report PDF](https://oa.tib.eu/renate/bitstreams/5e8dec33-aefd-438d-8e6d-7517a9a00a61/download). The requested objects have an abstract spherical topology, congruent flat regular pentagonal faces, and an immersion in three-space. Intersections of different sheets are permitted; coincident distinct faces are excluded. The source expressly leaves the appropriate meaning of a union of facet-glued dodecahedra to be formulated. Treating this as an ordinary embedded set boundary would silently narrow or change the immersed question.

3. **Open Problems in Discrete Differential Geometry**, collected by Günter Rote for the 2009 workshop, Problem 2 and Ulrich Brehm's note, p.1. [Author-hosted PDF](https://page.mi.fu-berlin.de/rote/Kram/OWR-DDG09-problems.pdf). This source identifies a material error in the current TOPP ancillary description: the great dodecahedron's pentagram vertex links prevent local embedding at a vertex, so it is not an immersion under the standard local definition. Its genus is four as well. It is not a counterexample to the spherical immersion question. The source also distinguishes a weaker variant allowing crossings at vertices.

4. Elena Arseneva, Stefan Langerman, Boris Zolotov, **A Complete List of All Convex Polyhedra Made by Gluing Regular Pentagons**, Journal of Information Processing 28 (2020), 791-799, DOI [10.2197/ipsjjip.28.791](https://doi.org/10.2197/ipsjjip.28.791), [arXiv:2007.01753](https://arxiv.org/abs/2007.01753). The downloaded arXiv v1, p.1, explicitly allows folding inside the original polygonal pieces. This convex Alexandrov-gluing classification does not classify immersed flat-pentagon-faced surfaces. Replacing the present question with that solved problem would be invalid.

The three decisive PDF pages were textually and visually inspected. No source PDF, extracted source text, corpus record, or inherited report is included in this public-safe packet.

## Literature search scope

Searches covered the exact problem title, Richard Kenyon with pentagons/dodecahedra/immersed surfaces, and regular pentagonal polyhedral surfaces with convex and nonconvex qualifiers. Exact-ID repository code, issue/PR, and commit queries were also checked through the GitHub connector. These searches found the maintained open entry and the related convex classification above, but no full resolution. This is a bounded search result; it is not a claim that no relevant paper exists.

## Accepted partial and remaining gap

Under explicitly stated standard edge-to-edge hypotheses, Euler incidence forces at least twenty trivalent vertices. Trivalent geometry fixes the absolute cosine between neighboring face normals to 1/sqrt(5). An exact Gram determinant then prohibits two adjacent edges from a four-valent vertex ending at trivalent vertices. For the valence-{3,4} subclass, the four-valent vertices must form an induced graph of minimum degree at least two whenever they occur.

These facts do not produce a removable cap, control higher valences, or prove a global union-of-dodecahedra description. The explicit continuously varying four-valent star is only a local realization, not a counterexample or closed-surface construction. A proof must still close the global face constraints and supply a precise, valid dodecahedral decomposition or a rigorously certified counterexample.

## Verification meaning

`diagnostics.py` uses only the Python standard library, with exact rational arithmetic in Q(sqrt(5)) for its decisive identities and determinant tests. Its output is reproducible under normal and optimized Python. It verifies algebra, corpus identity when all input paths are supplied, and consistency of the frozen status. It is not an automated proof verifier for every geometric argument, an exhaustive surface search, or an independent audit. Independent mathematical review remains required before publication.
