# A supercritical nonuniqueness example on a graph roughly isometric to the square lattice

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. Version 1.0.0,
22 October 2026. Five-page unrefereed preprint and exact supplementary checks.

The universal written proof is `main.tex` / `paper.pdf`. It constructs a fixed,
deterministic, connected simple graph of maximum degree four by keeping edges
inside two opposite square-lattice quadrants and replacing every other edge
by a private chain of length 100. The graph satisfies the original book's
multiplicative-plus-additive rough-isometry definition with constant 100.
All actual bonds have one common independent probability p. Independent coarse
probabilities p and p^100 arise by exact series reduction, with a bijection of
infinite components. At p=9/10 every root has positive survival probability;
at p=19/20 the probability of at least two infinite clusters is strictly greater
than 2200741829/6461571200>1/3. Thus p_c<=9/10<19/20.

## Exact scope

The original Problem 9.6 of Benjamini's 30 October 2013 manuscript asks for
uniqueness on bounded-degree graphs roughly isometric to Z^d, but omits the
p-quantifier. Its preceding chapter context discusses p>p_c. The note explicitly
declares and refutes the interpretation: every admissible G and each fixed
p_c(G)<p<=1 have almost-sure uniqueness. It does not claim that this was the
author's unique intended quantifier. A weaker near-one assertion, critical
nonuniqueness, almost-sure multiplicity, exact cluster count, or simultaneous
assertions over all p are not conclusions. Dimension two suffices to disprove
the declared universal statement; no dimension-one nonuniqueness is claimed.
No transitivity, quasi-transitivity, random environment, WSF analogy,
0/1/infinity law or uniqueness-monotonicity assumption enters the proof.

## Offline reproduction

Python 3.8 or later, standard library only; no installations or network:

```
python3 -B reproduce.py
python3 -B build_package.py --output ../rebuilt
```

The first command verifies every closed public member hash and rejects missing
or extra files, checks TeX/PDF provenance and metadata agreement, and runs
`verification/exact_checks.py` in normal, -O and -OO modes. Each output must equal
`verification/EXPECTED.json` byte for byte. The checker uses explicit failures,
not removable assertions. It does not import or execute original claimant or
prior-review mathematical code. It checks:

- all 2048 corner-containing subsets of a 3-by-4 quadrant patch, including holes,
  disconnected sets and degree-four dual vertices, with actual crossed-edge
  graphs and a found bottom-to-left simple path;
- all 64 bond configurations of a triangle replaced by disjoint chains of
  lengths 1,2,3:192 connectivity comparisons and the exact joint coarse law;
- a 4392-vertex actual subdivision patch, all edge-image bounds and 2116 metric
  sample pairs, including near-endpoint and midpoint positions;
- 200 explicit all-weak paths, including distant starts up to coordinate 100,
  with the exact n+3 distance and actual edge eligibility;
- every rational probability constant, strict power inequality and nonzero
  remainder of the all-length/all-start sums;
- nine false controls: wrong dual boundary, missing corner, series-OR,
  far-endpoint projection, degree-four and disconnected-set exclusions,
  an unsubdivided weak parameter, finite-start cutoff and shared-bond dependence.

Finite checks do not prove the infinite theorem. The written proof supplies
the parity lemma for every finite corner set, every possible long bridge,
uniform global metric bounds, the infinite-component bijection and independence
of the infinite-event sigma-fields. The checker supplements that argument.

The second command first verifies the package, then creates the scientific PDF,
deterministic source ZIP, matching metadata and deposit proposal, upload README,
and five-member upload kit. It reuses the exact frozen PDF, making archive builds
byte reproducible in the same Python/ZIP environment. Recompilation of TeX is
separate; byte-identical TeX recompilation is not claimed. Any ordinary LaTeX
engine with the standard packages in main.tex can produce another PDF.
The actual export used a hash-pinned official Tectonic 0.17.0 binary, only existing
cached resources, network denied and shared-cache writes denied. No new
dependencies were downloaded. The final source also compiled successfully in
the desktop LaTeX editor. All five PDF pages were rendered and visually read.
BUILD_RECEIPT.json and PDF_VISUAL_QA.json bind the source and frozen PDF.

## Credit and publication limits

Series reduction, Peierls counting, parity, bounded subdivision and product
independence are established methods. Benjamini–Schramm's hyperbolic-sector
example, high-density uniqueness theorems, Benjamini–Kozma's critical product
example and Hilário–Sá–Sanchis–Teixeira's annealed stretched-lattice law are
explicitly credited and distinguished. No older theorem is imported into the
self-contained counterexample. RELATION_TO_PRIOR_WORK.md and
SOURCE_PROVENANCE.json give the precise comparison, primary versions, hashes
and limits. The original question DOI is not a counterexample DOI.

The own-project PR1348, head 4222445c0fe52b32a6dbab7ee5ad791b5d044b08,
is an unpublished proof source. It is not represented as an earlier published
solution. Catalog 10000037/AMR-099-0037 is one result family. Bounded searches
authenticated no earlier publication of the exact result; they do not establish
exclusive firstness, exhaustive novelty or current openness. Two new independent
whole-package reviews and root adoption remain required. Publication readiness
is false. No upload, DOI reservation, release, merge, register write or
publication is performed by this package or its scripts.

No raw third-party bodies, private ledger captures, provider credentials,
operational drivers, old acceptance packets or unrelated private material are
included. Generic packaging code reuses Alec Kriebel's MIT helpers with provenance;
the mathematical checker is newly authored for this note.

## Authorship and licenses

AI tools were extensively used in all phases: planning, mathematical exploration,
proof development and reconstruction, computation, literature investigation,
writing, editing, and adversarial verification. Alec Kriebel is the named human
author. This is an unrefereed preprint, without conventional independent human
peer review, journal acceptance, or formal proof-assistant certification.
Internal AI audits do not provide those certifications. Authored prose is
CC BY 4.0 (LICENSE-PROSE-CC-BY-4.0.txt); authored code is MIT
(LICENSE-CODE-MIT.txt). Third-party works retain their own rights.
