# Sources, overlap and priority limits

This is a credited alternative proof of the exact target, rather than a
claim that the problem remains open or that this is its first resolution.
The classical cone and cusp mechanisms and the contemporary labelled
solution below receive explicit credit in the manuscript and metadata.

## Exact problem

Dmitry Fuchs, *Billiard Trajectories in Regular Polygons and Geodesics on
Regular Polyhedra*, Arnold Math. J.7(2021)493-517,
DOI10.1007/s40598-020-00170-8.
[Full publisher source](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf),
SHA256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d.
Definition2.1 and its preceding parity convention: printedpp502-505;
parallelism: section1.1; labelled target Conjecture2.7: printedp512;
elementary lattice types: section2.3.
Short means first subsequent vertex; no numerical length cutoff.
Canonical representatives modulo n-2 and source dihedral parallelism
are essential. The source's unlabelled Proposition1.2 alone does not
identify the physical endpoint-angle labels.

## Exact contemporary coverage

Alper Ferudun, *On Seven Conjectures of Fuchs on Billiard Trajectories in
Regular Polygons and Geodesics on the Regular Dodecahedron*, version1.0,
9October2026, DOI10.5281/zenodo.23267641.
[Author release](https://eulersolve.org/papers/amr-049/).
TheoremC (printedp5, proofp17, supporting sections2-3 pp9-17) covers the
same canonical-labelled theorem for all n>=4; the n3 case is elementary.
Its reduced angular index is equivalent to this note's intrinsic K.
It supplies the type dictionary, uniform twists, finite shortening descent,
chord normalization and common-direction scaling. This note instead uses
hyperelliptic commutation for all affine maps and classical cusp reduction.

The actual target proof was inspected, rather than relying on the abstract.
No central target gap was found in that focused inspection; this is not
whole-package adversarial certification of its seven theorems.
The retrieved PDF SHA256 is
ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707.
The open submitted Zenodo API record, created2026-10-09T17:25:38.397439Z,
and its file sizes/MD5s match the live author PDF, ZIP and verification
report. The DOI registry independently records the October9 registration.
These establish present retrievability and strong dated release evidence,
not an exhaustive history of earlier drafts.

## Chronology of this candidate

[PR152](https://github.com/AlecKriebel/Math/pull/152) was created
2026-09-30T12:11:38Z. Original submitted head:
99ef28d28bf380658400886d1f8c2120a5096d97.
The original candidate SHA256 is
100454abdfcbeb6647e0e0596a86b86b3a39d330de2605fe485ae242d9e91c9a.
The content-bearing commit is7ef58eacc6c85150fcbbb37630c5c327d28850a1,
with author/committer date2026-09-30T11:51:54Z; an author-set commit date
is not a server-certified publication instant.
The public repository's unauthenticated original-head file now matches
the frozen candidate. Contemporaneous public/private visibility history
was not obtained.

That candidate stated the exact theorem, double-polygon cone construction,
hyperelliptic/cusp strategy, sign-invariance of sine weights and common
derivative cancellation. Its unconditional physical-label invariance and
reversal statement was false, and it lacked the Q-folding-chart
justification. The accepted repaired proof dated12October2026UTC proves
k=sigma K and k_reverse=(-1)^N k. The theorem and central weight strategy
survive, but a fully correct public proof is not certified as ofSeptember30.
The current proof is not backdated. The earlier recorded strategy and
different universal reduction routes support describing these as
contemporaneous separate developments. This describes the documented
proof routes and chronology, not a certified account of either author's
awareness. Neither shared mathematics nor the dates establish copying,
exclusive priority, or a literally simultaneous publication instant.
See PUBLICATION_CHRONOLOGY.md for the precise recorded events.

## Classical credit and inspected locators

- Veech1989, *Teichmuller curves in moduli space, Eisenstein series and an
  application to triangular billiards*, Invent. Math.97,553-583,
  DOI10.1007/BF01388890: Proposition2.10 p561 (saddle directions/parabolic);
  section4 pp564-565 (actual double polygon, cones/genus/hyperelliptic
  involution); section5 pp566-568 and Theorem5.8 with section7 pp572-573
  (group, cusp representatives and trigonometric boundary data).
- Veech1992, *The billiard in a regular polygon*, GAFA2,341-379,
  DOI10.1007/BF01896876: p343 closed-length spectrum; Lemma2.5 p347,
  pp348-350 saddle lifts/periodic reduction; pp351-355 relative-homology
  edge labels. These labels are not silently identified with Fuchs's k.
  Both full original papers were retrieved through public EuDML/GDZ and
  their relevant sections and model/theorem pages inspected in this audit.
  The original candidate's missing-fulltext qualification is historical.
- Finster2011, *A series of coverings of the regular n-gon*,
  [arXiv1005.4588v3](https://arxiv.org/abs/1005.4588): sections3.1-3.2,
  Remarks3.2/3.5 and p20 corroborate the actual even double group/cusps.
  Section3.2 describes the smaller opposite-side quotient. Immediately
  after Remark3.4 on printedp7, it invokes Hubert-Schmidt LemmaJ to
  identify its Veech group with that of the double. Remark3.5 on printedp8
  gives the group signature, rather than the cover-transfer argument.
- Tyszkowska2005, *On p-hyperelliptic involutions of Riemann surfaces*,
  Beitr. Algebra Geom.46,581-586: Theorem3.1 printedp583 gives uniqueness
  for genus g>4p+1; taking quotient genus p=0 yields g>=2. Its actual
  full text and proof were read at the [EMIS journal copy](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2tys.pdf).
  The theorem applies to holomorphic involutions. Our affine conjugate has
  derivative-I, extends holomorphically over zeros and has genus-zero quotient.
- Hubert-Schmidt2001, *Invariants of translation surfaces*,
  DOI10.5802/aif.1829: LemmaJ p473 identifies isomorphic Veech groups
  for the balanced two-polygon cover; section3 pp477-479 supplies saddle-vector
  equivariance and scaling vectors ordered by length.
- Eskin-Masur-Zorich2003, *Moduli spaces of abelian differentials:
  the principal boundary, counting problems, and the Siegel-Veech
  constants*, IHES97,61-179, DOI10.1007/s10240-003-0015-1:
  section3 preprintp11 and section11 record odd-pi cone return angles.
- Hubert-Lelievre, preprint2004/published2006, *Prime arithmetic
  Teichmuller discs in H(2)*, [arXivmath/0401056](https://arxiv.org/abs/math/0401056):
  preprint sections3.2/3.3.2 pp12-13 explicitly label return-angle rays.
- Boissy2015, *Labeled Rauzy classes and framed translation surfaces*,
  AIF65,905-932, DOI10.5802/aif.2947: sections3.1 pp914-915,
  Proposition4.1 p919 and section5 p925 supply cyclic separatrix labels
  and distinct-cone hyperelliptic transport. His odd-pi comparison
  differs by a pi shift from this note's backward-end convention.
  The underlying construction is classical.

No new Veech theorem, cone index, hyperelliptic transport or general affine
scaling mechanism is claimed. The note makes the physical chart/parity
dictionary explicit and presents a complete alternative deduction.

## Search limits

Three initially independent families inspected exact Fuchs history/citers,
classical labels and modern alternative mechanisms. They found no explicit
pre-September30 exact all-n physical-label theorem, a bounded negative
result rather than an absence certificate. Fuchs's formulation as a
conjecture establishes his stated prior-open problem, not exhaustive
historical novelty. Modern close sources include McMullen's 2025 online /
2026 volume paper DOI10.4171/LEM/1099: it has simultaneous affine scaling
and closed-geodesic results but not the inspected all-n A_k dictionary.
Pentagon-only results and unlabelled spectra are credited, not promoted
to all-n novelty.

Unresolved precise leads include Ward1998's full rational-triangle paper
and Veech1995's *Geometric realizations of hyperelliptic curves* chapter.
The search did not exhaust dissertations, languages, framed separatrix
literature, authenticated citation databases or unindexed manuscripts.
Citation indices omit the directly retrieved October2026 preprint and
therefore cannot certify absence. No person was contacted.
The archive contains only original notes/code/metadata, not external
copyrighted articles, scans, OCR, rendered source pages or downloaded ZIPs.

