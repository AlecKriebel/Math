# Public sources and dependency verification

Verification date: 20 October 2026. Public URLs and bibliographic information below identify inspected sources or explicitly marked leads. Source PDFs, extracted text, page images, and catalog contents are not part of this package.

## 1. Original line-union problem

Stefan Steinerberger, "Three problems for discrepancy and QMC," pp. 2890–2892, in *Uniform Distribution Theory and Applications*, Oberwolfach Reports 10 (2013), no. 4, pp. 2837–2917. The line question is on printed p. 2891.

- [Official bibliographic page](https://ems.press/journals/owr/articles/12723)
- [Official report PDF, relevant page](https://ems.press/content/serial-article-files/46480?nt=1#page=55)
- [DOI: 10.4171/OWR/2013/49](https://doi.org/10.4171/OWR/2013/49)

The meeting ran 29 September–5 October 2013. EMS gives publication on 3 September 2014; these are distinct dates, not evidence of a 2014 workshop.

The official PDF was retrieved and text-extracted; printed p. 2891 was rendered and visually inspected. The contribution's opening and closing text was also checked. Cubes contained in the unit cube, positive normalized arclength, and full line intersections were verified. Orientation and boundary conventions are not explicitly specified. The label OWR-12723-007 is a catalog identifier, not a printed problem number.

Retrieved PDF: 709,488 bytes; SHA-256 63628ee4c7120db2d13407a1fbae48a024a2f3ec0ac168a6be9a41cc9e0e984c.

## 2. Imported bounded-error flow theorems

Bence Borda, *Bounded error uniformity of the linear flow on the torus*, Monatsh. Math. 189 (2019), 221–237; inspected author preprint arXiv:1803.06968v1, submitted 19 March 2018.

- [arXiv record](https://arxiv.org/abs/1803.06968)
- [HTML full text](https://arxiv.org/html/1803.06968)
- [Institutional author PDF](https://real.mtak.hu/98617/2/180306968v1.pdf)
- [Journal DOI](https://doi.org/10.1007/s00605-018-1211-x)

The arXiv record supplies the journal reference. The author PDF was retrieved and text-extracted; printed p. 4 was rendered and visually inspected, and the statements were checked against HTML. The journal DOI page was unavailable to the retrieval tool; the typeset journal version was not independently inspected.

Corollary 2 supplies the following dependency: for a fixed direction alpha whose coordinates are real algebraic and Q-linearly independent, one finite K_alpha bounds

    |integral_0^T 1_R({s+t alpha}) dt - T volume(R)|

for every T>0, every starting point s, and every axis-parallel box R in the unit cube. The bound is unnormalized time discrepancy, and is uniform over boxes, not merely finite separately for each box. Independence of the coordinates together with an extra 1 is not required for this continuous-flow result. In particular alpha=(sqrt(2),sqrt(3),1) is admissible.

Theorem 1 supplies the fixed-orientation dependency in Attempt 5: algebraic facet normals, each transverse to the fixed direction, yield a bound uniform over positions and sizes for the prescribed finite set of normals. Its constant is allowed to depend on those normals. It is not uniform over all rotations, and excludes faces parallel to the direction.

Borda explicitly discusses a disproof of Drmota's continuous-curve conjecture. No occurrence of Steinerberger or an express resolution of this line question was found in the inspected preprint. The present package gives a reduction; it does not attribute that reduction or intended orientation to Borda.

Retrieved author PDF: 222,149 bytes; SHA-256 fddef4d3a9f17befc11ab06e9d65c86e7db1bd18a7ba8893ed5da400065ad1b9.

## 3. Imported ordinary planar square discrepancy

Jiří Matoušek, *Geometric Discrepancy: An Illustrated Guide*, §6.3, Theorem 6.3, printed pp. 180–182.

- [Inspected book PDF](https://people.fjfi.cvut.cz/vybirja2/TUM-IBC/Matousek_Geometric_Discrepancy.pdf)

This inspected presentation gives an unnormalized Omega(log N) discrepancy lower bound for axis-parallel squares contained in the unit square, via a constant-factor comparison with rectangle discrepancy. It attributes the earlier square bound to Halász and an elementary rectangle-to-square reduction to Ruzsa, *The discrepancy of rectangles and squares*, Graz proceedings (1993), pp. 135–140. The Ruzsa proceedings paper is bibliographic attribution from the inspected book, not a separately inspected source.

The package imports that ordinary square theorem. WEIGHTED_SQUARE_ROUTE.md separately supplies the side-length-weight transfer required for lifting points to three-dimensional cubes and handles closed-boundary mass. No higher-dimensional cube-versus-box theorem is inferred from the planar theorem. No historical novelty is asserted for the transfer.

## 4. Neighboring continuous-curve result, not a solution

Michael Drmota, *Irregularities of continuous distributions*, Annales de l'Institut Fourier 39 (1989), 501–527.

- [Official journal PDF](https://aif.centre-mersenne.org/article/AIF_1989__39_3_501_0.pdf)
- [DOI: 10.5802/aif.1175](https://doi.org/10.5802/aif.1175)

Theorem 2 and Remark 3 on printed p. 504 were text-checked and inspected in a rendered page image. The bounds concern continuous curves with time-occupation measures and distinguish torus-wrapping from contained cubes. They do not identify normalized arclength on disconnected full-chord unions. The upper construction permits variable-speed travel and dwelling. Joining arbitrary chords can add length not controlled by their original total. No full-chord logarithmic theorem or counterexample is imported from this source.

Retrieved PDF: 1,478,751 bytes; SHA-256 411f9ae194eeaad20cd3e45200cfb107836bfb7d16676122abae33430b8b9dbc. A web screenshot request returned a cache miss; local rendering succeeded. A separate Borda workshop-slide URL returned 404 and was not treated as inspected evidence.

## 5. Status search and nonmatches

A bounded search using the original title, subheading, author, and line/cube/continuous-discrepancy terminology did not locate an inspected resolution with matching object, measure, geometry, normalization, norm, and quantifiers. That negative search does not prove current openness.

- Stefan Steinerberger, [*Buffon Discrepancy and the Steinhaus Longimeter*, arXiv:2603.27807](https://arxiv.org/abs/2603.27807), [inspected HTML](https://arxiv.org/html/2603.27807v1), concerns planar intersection counts and an essential supremum over lines, not this three-dimensional arclength-in-cubes question. The [author's publication page](https://faculty.washington.edu/steinerb/) stated acceptance by Mathematika when checked. That is the stated status of a different paper.
- Florian Pausinger, [*On the expected L2-discrepancy of stratified samples from parallel lines*](https://pcwww.liv.ac.uk/~karpenk/JournalUDT/vol18/no2/03_2478-udt-2023-0012_pdf.pdf), Uniform Distribution Theory 18 (2023), no. 2, pp. 31–56, concerns random planar point samples, not the requested full-chord supremum.
- An author open-problem PDF appeared in search results, but extraction failed and an ordinary retrieval timed out. Its full contents were not inspected, and snippets were not used to infer either resolution or continued openness.

All retrieval limitations above are recorded as limitations, not mathematical evidence. Public hashes identify the retrieved source bytes; they do not certify the correctness of theorems or this package's arguments.
