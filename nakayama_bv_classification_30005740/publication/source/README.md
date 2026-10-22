# BV generators for polynomial Weyl subalgebras

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X
Preprint, version 1.0.0, 22 October 2026.

For every field k of characteristic zero and every nonzero polynomial h,
the ordinary canonical Hochschild Gerstenhaber algebra of
A_h = k<x,Y>/(Yx-xY-h) has a degree-minus-one BV generator if and only if h
is squarefree. A repeated irreducible factor forbids any bracket generator,
even without square-zero. The squarefree case has zero bracket and Delta=0.
The original embedded h=0 specialization is k[x] and is handled separately.

## Read and reproduce

Read main.tex or the separately supplied PDF. The universal proof uses the
precise published resolution and derivation spanning stated in Section 2.
DEPENDENCIES.md distinguishes those imports from our direct arguments.
PRIORITY.md identifies essential predecessors and the bounded search limits.

Run with Python 3.10 or later, using only its standard library:

    python3 -I -S -B exact_checks.py

Compare the JSON output byte for byte with CHECK_RESULTS.json. Optional -O or
-OO inserted before exact_checks.py gives identical output; guards do not rely
on assert statements. No package installation, network, claimant program, or
external data is used. These are finite exact diagnostics, not universal proof
checking or an independent computation of Hochschild cohomology.

To typeset, use a normal existing LaTeX installation supporting article,
fontenc, lmodern, amsmath, amssymb, amsthm, geometry, hyperref and microtype;
XeLaTeX twice or Tectonic main.tex is sufficient. The preparation used the
built-in LaTeX compiler and exported with a previously pinned Tectonic 0.17.0
in cache-only mode. Recompilation with other engines/versions can differ in
PDF bytes and layout. No compiler or third-party source body is distributed.

The source archive contains the exact manuscript, this documentation, exact
diagnostics/results, source/priority notes, licenses, scientific metadata,
build_release.py, and source-manifest.json. A frozen paper.pdf is included as
the input to an entirely offline byte-reproducible packaging build. It is the
same PDF as the separate deposit file. The builder does not compile TeX.

    python3 -I -S -B build_release.py --output /new/empty/output/directory

This recreates the six release files byte for byte, including the source ZIP
and the five-member upload kit. It does not contact a service, obtain credentials,
reserve a DOI, or publish. The deposit manifest lists only the separate PDF and
source ZIP. Archive member permissions and timestamps are fixed for packaging;
the source manifest hashes every other source member.

## Status, authorship, and rights

AI tools were extensively involved in mathematical exploration, proof
development and reconstruction, computational verification, source and
literature investigation, manuscript preparation, editing, and adversarial
auditing. This is an unrefereed preprint without formal independent human peer
review, journal acceptance, or formal proof-assistant certification. AI review
does not provide those certifications. Human author: Alec Kriebel.
Original prose: CC BY 4.0. Original code: MIT. Third-party publications are
referenced, not bundled. No firstness or exhaustive priority certificate is made.
