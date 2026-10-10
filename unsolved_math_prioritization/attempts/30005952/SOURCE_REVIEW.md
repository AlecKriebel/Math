# Sources, attribution, and acceptance boundaries

Problem 30005952 / OWR-14298580-008 concerns the strong geography restriction for the total, ungraded F₂[U]-module HF⁻ of a connected closed oriented smooth rational homology 3-sphere, summed over all Spinᶜ structures. If its U-torsion length is ℓ, the proposed restriction requires a direct summand containing one F₂[U]/(Uʲ) for each j=1,…,ℓ.

## Credited result and scholarly status

Alper Ferudun's *A Negative Answer to the Strong Geography Question of Alfieri and Binns*, dated September 30, 2026, Theorem 1.3, supplies Σ(30,47,83), its displayed decomposition, and the computer-assisted argument. Credit for the example and negative answer belongs to Ferudun. The note explicitly describes itself as an unrefereed, AI-assisted computer-assisted note; the public Zenodo record labels version 1.0 as a preprint. The independent audit preserves this status and makes no discovery, novelty, or priority claim.

- [Preprint landing page](https://eulersolve.org/papers/owr-14298580-008/)
- [Zenodo DOI and version record](https://doi.org/10.5281/zenodo.23063072)
- [Public source archive](https://zenodo.org/api/records/23063072/files/OWR-14298580-008-source.zip/content)

The audit accepts the precise counterexample over F₂ for both orientations. Its total minus module has U-torsion length 16 and zero length-15 cyclic direct summands. The example is an integral homology sphere and hence has one Spinᶜ structure. The acceptance does not extend to the note's exhaustive search, minimal-product assertions, further-example table, population counts, or priority survey.

## Original question and module scope

Antonio Alfieri's report, *Is the geography of Heegaard Floer homology restricted or is the L-space conjecture false?*, appears in Oberwolfach Reports 34/2024. Printed pages 1952–1953 state the definition and question. [Report DOI](https://doi.org/10.4171/OWR/2024/34).

Antonio Alfieri and Fraser Binns, *Is the geography of Heegaard Floer homology restricted or the L-space conjecture false?*, arXiv:2404.00490v1, March 30, 2024, Definition 1.6 and Question 1.10, give the same target. Section 2.1 and Remark 2.2 specify the total module and the plus/minus reduced-module identification. The October 10, 2026 source review found only v1 on the official record. Their knot- and large-link-surgery results are not a resolution for all rational homology spheres. [Versioned arXiv record](https://arxiv.org/abs/2404.00490v1).

## Published dependencies and exact conventions

1. Peter Ozsváth and Zoltán Szabó, *On the Floer homology of plumbed three-manifolds*, Geometry & Topology 7 (2003), 185–224: Definition 1.1 and Theorems 1.2 and 2.1. The negative definite plumbing has one bad vertex. The identified plus group is HF⁺(−Y(G)); the boundary-orientation sign is retained. Section 2 supplies the F₂ formulation. [Published PDF](https://msp.org/gt/2003/7-1/gt-v7-n1-p05-s.pdf).
2. András Némethi, *On the Ozsváth–Szabó invariant of negative definite plumbed 3-manifolds*, Geometry & Topology 9 (2005), 991–1042: Sections 2.2–2.4, Example 3.4(3), Proposition 3.5.2, Corollary 3.7, Proposition 4.7, Lemmas 7.6–7.7, Example 8.2(3), Theorems 8.3 and 9.3, and Sections 11.11–11.14. These supply the almost-rational graph/graded-root bridge, canonical Seifert sequence, finite module length convention, and grading normalization. Leaf-to-merger height differences give U-exponents without an off-by-one or factor-of-two change. Integral degreewise freeness permits passage to F₂ without additional coefficient torsion. [Published PDF](https://real.mtak.hu/141378/2/23424.pdf).
3. Mahir Bilen Can and Çağrı Karakurt, *Calculating Heegaard–Floer homology by counting lattice points in tetrahedra*, Acta Mathematica Hungarica 144 (2014), 43–75; arXiv:1211.4934v2: Sections 1–2, Theorems 1.3 and 2.3. These verify Seifert normalization, the homology-sphere criterion, finite cutoff and semigroup description. The exceptional triple (2,3,5) is irrelevant to this example. [Versioned primary PDF](https://arxiv.org/pdf/1211.4934v2).
4. Peter Ozsváth and Zoltán Szabó, *Holomorphic disks and three-manifold invariants: properties and applications*, Annals of Mathematics 159 (2004), 1159–1245: Section 2.1, Proposition 2.5 and Theorem 10.1. These supply the rational-homology-sphere HF-infinity structure and orientation duality. The plus/minus long exact sequence identifies the reduced plus module with minus torsion, and degreewise graded duality preserves each finite cyclic length under orientation reversal. No equality of absolute gradings is claimed. [Published PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v159-n3-p04.pdf).

The complete [mathematical audit](MATHEMATICAL_AUDIT.md) checks the actual 32-vertex plumbing, the finite tail, all theorem hypotheses, coefficient field, Spinᶜ scope, grading conventions, plus/minus transfer, both orientations, and the abstract direct-summand obstruction. These are imported published foundations; the audit does not reconstruct their analytic proofs.

## Computation and public certificate identity

This is an audit of a credited computational preprint. Its independent exact computations are substantive evidence, not merely illustrations. The publication edition does not claim to be a standalone code-free proof or a complete rerunnable computational package.

The public archive is 258522 bytes, SHA-256 36960972d2b2de7eedb9a3e8e794f4b292afeb0143566f5b6feed7ce93a80797. Within it, certificate_Sigma_30_47_83.txt is 21829 bytes, SHA-256 6d7130dbc0ecf948286ed5d2b7e51a2cdad322da0588a97f3c9ddf7a43f72943. Two certificate members had identical hashes. Every one of the 1707 index/value pairs matched the PDF and independent turning-point extraction. The archive and certificate are cited by public URL, name and identity; neither is copied into this edition.

The prior audit used newly authored Python standard-library code and exact integer, rational and F₂ arithmetic. No downloaded executable code was run. Three constructions matched all 109231 tau samples; four independent module routes matched the cyclic-length data, with 853 finite summands and reduced dimension 4864. Their normal, optimized and double-optimized runs agreed. The audit includes its mathematical decomposition and summarized verification findings. Programs, raw output files, full tau arrays, certificate contents and datasets are not distributed here.

## Retrieval history and bounded conclusions

The [source metadata](SOURCE_METADATA.json) preserves all seven source PDF hashes and byte counts, exact inspected locations, historical retrieval and visual-inspection accounts, archive/certificate identities and match results. The EulerSolve archive route returned HTTP 403; the audit used the deposited Zenodo copy. An incorrect initial MSP URL returned an unrelated paper, which was rejected by title/page-range checks and was not used; the correct Némethi paper was retrieved from the Academy repository. Some DOI or landing-page requests failed, while primary PDFs and the Zenodo record API were accessible.

These are historical October 10, 2026 audit findings. Edition preparation rechecked the sealed audit identities and editorial preservation; it did not fetch new scholarly sources, inspect source PDFs anew, repeat the mathematical computation, or conduct a new literature search. The review does not certify exhaustive literature status.

The source preprint and this AI-assisted audit are unrefereed. Internal mathematical acceptance is not external human peer review, journal acceptance, or formal proof-assistant verification. No substantive mathematical correction was required in the accepted scope; the rejected-source retrieval error was already disclosed and does not alter the argument.
