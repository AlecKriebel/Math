# Source gate for Kirby Problem 4.21 (ID 2897)

Checked 2026-10-03. This is a source-grounded partial investigation, not a claimed resolution.

## Exact problem and source correction

The catalogue URL is <https://www.unsolvedmath.com/problems/2897>. The direct retrieval returned HTTP 403. The mathematical question was independently verified in the full author-hosted *K3* book, Problem 4.21, printed pp. 206–207:

<https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf>

This is a 436-page author preliminary version, with April 2026 PDF metadata. It explicitly distinguishes closed manifolds from its compact-with-boundary counterexample. The earlier problem number, Kirby 1997 Problem 4.74, is identified there. The full 1997 scan could not be downloaded in this check; the numbering correspondence is attributed to the 2026 primary problem list, rather than claimed as a fresh reading of the 1997 page.

The catalogue-associated AIM link, <https://aimath.org/pastworkshops/kirbylistrep.pdf>, resolves through the web reader to a four-page workshop report. It is not the full *K3* problem list and was not used as the mathematical source.

The connected-manifold convention is made explicit. No orientability assumption has been added to the question. “Acyclic” means integral reduced homology zero, not rational acyclicity, and does not mean contractible. All proposed hypersurfaces are locally flat and collared on both sides.

## Primary theorem dependencies

1. **Freedman (1982), Theorems 1.4′ and 1.5.** The theorem statements and relevant construction/classification proof on printed pp. 367–371 were inspected. These give contractible topological fillings of integral homology spheres and the simply-connected form-plus-Kirby–Siebenmann classification. The construction of both odd-form types is essential; merely quoting classification without realizing the correct invariant would leave a gap. The deep disc-embedding and classification results are imported established theorems, not newly proved or formally verified here.
   - <https://doi.org/10.4310/jdg/1214437136>
   - <https://www.maths.gla.ac.uk/~mpowell/1982_The%20topology%20of%20four-dimensional%20manifolds.pdf>

2. **Quinn (1982), Corollary 2.2.3.** The corollary and the preceding handle-straightening argument on printed pp. 506–508 were inspected. The corollary is on printed p. 508 in the retrieved scan. It provides punctured smoothability. It is not a theorem that an arbitrary compact coordinate-ball complement is smoothable, or that a smooth exhaustion has a homology-sphere level.
   - <https://doi.org/10.4310/jdg/1214437139>
   - <https://www.maths.gla.ac.uk/~mpowell/1982_Ends%20of%20maps%20III.pdf>

3. **Friedl–Hambleton–Melvin–Teichner (2007 version).** Theorem 1.2, its complete lattice proof in §2, and Corollary 1.4 with its complete proof/construction in §4 were inspected. The latter gives a published supply of topologically slice knots that are not smoothly slice in any rational homology 4-ball. It supplies the knot input for the compact obstruction; the compact obstruction itself is developed in full in PROOF.md. The cyclic-cover nonsmoothability argument does not rule out topological acyclic caps.
   - <https://arxiv.org/abs/math/0611077v2>
   - <https://arxiv.org/pdf/math/0611077>

4. **Ruberman–Stern (1997).** The full four-page paper was read. Its displayed construction on p. 376 already decomposes the nonorientable star partner of RP4 as a smooth interval bundle with a contractible topological cap. Only this construction is needed here; no assertion that the general nonorientable problem is solved follows.
   - <https://doi.org/10.4310/MRL.1997.v4.n3.a6>
   - <https://bpb-us-e2.wpmucdn.com/faculty.sites.uci.edu/dist/3/246/files/2011/03/41_FakeCP2RP4_MRL.pdf>

5. **Standard background.** Integral Mayer–Vietoris, excision, Poincaré–Lefschetz duality, van Kampen, 3-dimensional smoothing/uniqueness, the topological 4-dimensional Poincaré theorem, and Rokhlin's theorem are used in their stated settings. The proof explicitly separates orientation-dependent assertions. Donaldson's diagonalization theorem is discussed only for closed smooth definite manifolds, never asserted for an arbitrary compact manifold with homology-sphere boundary.

## Bounded current-status check

Searches used the exact current and earlier problem numbers, “smoothable acyclic decomposition,” and “pseudo-handlebody,” together with the primary authors and titles. The inspected April 2026 *K3* version still poses the general question. No verified later theorem settling it was found. Search snippets, generated proof repositories, and catalogue status labels are not treated as proof. This is a bounded search finding; it is not a universal assertion about all published or unpublished work.

## Retrieved-source SHA-256 fingerprints

- K3 author preliminary PDF: `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`
- Freedman scan: `e1f8fa0954129889038b709a41e5583488e8527831351558af176b8326a713c7`
- Quinn scan: `53791846508aa8b81c218b314522c0209b482af3f62d46d54b6b7ed003d92b29`
- FHMT v2 PDF: `9f439ae9fd56bfd9d5b984a95c68901bf9bdd7ac3983b7859bdaaefc9c859334`
- Ruberman–Stern PDF: `5b3151e2cb37c21898e99c371a92f30bc0cf819c145b71c7ddee3538649e0018`

These fingerprints identify source editions. The source PDFs, extracted books, and screenshots are not redistributed in this artifact set.

## Gate result

**PASS for the limited, attributed partial-result scope. NOT SOLVED for the full problem.** The missing finite acyclic-end cross-section and the smooth-cap gap in the cyclic-cover argument are explicit. No claimed proof depends on an inaccessible source, an unverified generated assertion, or interpreting an unsuccessful search as a theorem.
