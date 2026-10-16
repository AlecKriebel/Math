# Acceptance: KP-1.30 Khovanov 2-torsion partial results

8 October 2026. Catalogue 2689, rank 1041. **Unsolved, 5/5.**
The complete author report and independent audit are accepted as rigorous
partial progress. No mathematical correction is required. No universal proof,
knot counterexample, or novelty claim is made.

## Mathematical scope

The target is ordinary even, unreduced integral Khovanov homology of nontrivial
classical knots. “2-torsion” means an element of order two, including one inside
a cyclic group of higher 2-power order. Five genuinely different approaches
were investigated; retrieval, computation and auditing add no solution turns.

The accepted deductions include:

- The exact torsion budget t(K) = 2a(K) + rank(delta_K), where t and a count
  unreduced and reduced 2-primary cyclic factors, and delta is the rational
  reduced/unreduced connecting map of degree (1,2). Its rank equals the number
  of length-one rational Bar–Natan torsion bars.
- For one proper rational tangle replacement from K to J,
  t(K) >= 2a(K) + max(0,(r(K)-r(J))/2). The written module lemma includes free
  summands and arbitrary fields; finite calculations do not replace its proof.
- Kh(K#J;Z) has 2-torsion if and only if at least one summand does. This follows
  from the signed tensor connecting map and the exact reduced torsion formula,
  and reduces the conjecture to prime knots.
- Explicit higher-page Turner cancellation models, first-Bockstein limitations,
  and a torsion-killing short exact sequence identify precise missing steps.
  The models are abstract complexes, without claimed realization by knots.

A hypothetical counterexample has reduced rational rank at least five, zero
reduced 2-primary torsion and zero rational connecting map, is a weak local
rank minimum under proper replacement, and has nonzero higher Turner
cancellation. Along a d-step proper replacement path to the unknot its rational
Bar–Natan torsion exponents lie in [2,d]. No contradiction among these necessary
conditions has been established. General rank descent, spectral collapse and
universal diagrammatic pattern existence remain unproved.

The [author report](author/REPORT.md) and [independent audit](audit/AUDIT.md)
contain the full arguments, exact hypotheses and public citations. In
particular, the stronger length-one-bar statement is a published question,
not an available theorem. All source and novelty boundaries are preserved.

## Immutable evidence

The six author files and ten independent-audit files are copied byte-for-byte.
The wrapper independently pins each one and both original manifests:

- Author manifest: 859d3ac083256be02e0c0f139b08c502304855d47831af75dd94119dd647d2cc.
- Audit manifest: 329e588edb809fe0bfb92bd6f0f08d95853dcddd0b63f9990ce9870506872e31.
- Historical author archive: 17653 bytes, SHA-256
  3feb6d48ac9e30cd1cf36a4a4e42430b9e8cb4f471a6439e1e393711975fe669.
- Historical audit archive: 24511 bytes, SHA-256
  92945ea4dad0d56830c05df5893bbb9818b2c842460ea18aa81727fecc3f86e9.

The original archives were checked against their file inventories during
packaging. They are not included in the publication packet. Frozen runtime
and source metadata remain historical records and are not relabeled as fresh.

## Reproducibility and boundaries

The fresh wrapper reproduces the complete author output, independent half-edge
cube output, and independent algebra output byte-for-byte; it also reproduces
all nine comparison records. The latter computations include six full
bigraded comparisons, three directly computed connecting ranks, 3126 valid
module-composition pairs, and two complete doubled Turner constructions.

Eight semantic mutations are required to fail by the exact mathematical
RuntimeError in each wrapper mode. Normal, -O and -OO replays together give
24 mathematical negative-control failures. Full stdout and stderr, with return
codes, are emitted for every arithmetic and semantic-control run. All replay
code runs as actual UID/EUID 1000 in temporary read-only inputs and working
directories, with failed write probes and pre/post byte checks. Publication
controls additionally exercise the trust boundary and hostile import paths.

SymPy 1.14.0 and mpmath 1.3.0 are required; this is not a standard-library-only
packet. The bootstrap and wrapper run with -I -S -B. Arithmetic subprocesses
also use -I -S -B and add only the interpreter's configured purelib directory,
without running .pth files or site startup. The installed interpreter and its
dependency code are trusted execution prerequisites, not authenticated by the
packet; version checks alone do not authenticate dependency contents.

Eight PDF hash/size/page matches belong to the historical independent audit.
Fresh source/PDF verification is **NOT_RUN** in this source-free replay.
Imported source theorems, knot realization, novelty and the universal conjecture
are not machine certified. No source documents, source extracts, dataset
contents, private sources, personal data or private coordination files are
included. Only authored mathematics, authored checking code, computed outputs,
and public verification metadata are published.
