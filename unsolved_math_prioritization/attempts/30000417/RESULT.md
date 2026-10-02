# Five-turn result: original path list-labeling conjecture unresolved

Problem 30000417 / OWR-1189-007. Recommended disposition after independent review: **unsolved, 5/5**.

## Source correction

The original OWR 7/2006, p. 416, Conjecture 2 uses

    floor(3d(1−1/n))+1, for paths on n>=3 vertices.

The imported catalog incorrectly uses ceiling. Lists are arbitrary finite sets of natural numbers; labels at path distance 1 or 2 must differ by at least d. The ceiling version already fails at d=1,n=4, but that is only a transcription error. It is not a solution of the original floor conjecture. [Official source](https://ems.press/content/serial-article-files/46037?nt=1).

## Proven scoped results

1. For fixed n,d,k, every list instance is feasibility-equivalent to one with labels at most 1+d(nk−1), by exact gap compression. Reachable-pair tables give exact finite obstruction certificates
2. A weighted path deficit lemma yields the conjectured upper bound when a global extremum is shared on one largest modulo-three class, and a more general criterion for nonextremal common labels
3. A complete computer-assisted closure proves that **for every path length**, six-element lists with **d=2 and union size at most nine** are labelable. There are 4,087,257 states and 343,329,588 input transitions; independent Python/C++ implementations agree on the full state-set digest. Together with the explicit five-list P6 obstruction, six is sharp in this restricted-union family for every n>=6
4. Variable anchor labels give an exact polynomially optimized sufficient criterion and an all-size local-minimum/local-maximum theorem with arbitrary palette size
5. An explicitly colorable 42-vertex instance has optimum anchor deficits 4 in every residue class, so that sufficient method cannot cover every instance. A feasible ten-label instance forbids any global reduction to nine labels that preserves six distinct options per list

The computational all-length theorem is distinct from a bounded-n scan. Its restriction is the total number of distinct labels. No argument reducing arbitrary list assignments to nine labels has been proved. The remaining gap is the original all-n, all-d upper bound for arbitrary palettes, or a counterexample at the conjectured cardinality.

## Credit and audit status

The d=1 and n=3 boundary cases, ordinary path-list machinery and common-extremum method have prior source credit. Kohl's dissertation also gives interval-list and other special cases. No novelty or priority claim is made for any scoped result. The original lower bound is stated in the primary report; explicit lower witnesses here are consistent with it and are not original-conjecture counterexamples.

All five author turns are frozen and author search has stopped. Independent final source/proof review is pending. Python replays require only its standard library; optional C++ cross-checks require a suitable C++17 compiler, and the packed turn-5 check additionally uses unsigned 128-bit integers. No raw source PDFs/imports are included.
