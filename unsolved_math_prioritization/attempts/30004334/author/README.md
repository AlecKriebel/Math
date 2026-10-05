# Root-of-unity blowups: scoped partial results

Problem 30004334 / OWR-17296-019. Assessment dated 2026-10-05.

**Outcome: unresolved over the complex numbers, five substantive approaches completed.** No general bound for fixed order m >= 4, and no complex counterexample, is claimed. The packet contains independent derivations of partial results and reproducible arithmetic certificates; it claims no novelty, priority, or peer review.

## Exact target

Fix a positive integer m and a primitive m-th root of unity epsilon in C. Set

Z_m = { [1:epsilon^a:epsilon^b] : 0 <= a,b < m },

and let X_m be the smooth surface obtained by blowing up P^2_C once at these m^2 distinct points. The problem asks whether the self-intersections of **reduced irreducible** curves on this fixed X_m have a lower bound, and, if so, for their optimal lower bound b(X_m). We use the source's signed convention b(X_m) = inf C^2, rather than the positive magnitude used in some later papers.

The target is the final problem on printed p. 3310 of the 2019 Oberwolfach report, and Problem 3.12 in the revised Dumnicki et al. manuscript. The problem paragraph does not restate the field; its intended characteristic-zero/complex context is supplied by the surrounding discussion and the original authors' arXiv abstract. We explicitly work over C. An arbitrary-characteristic interpretation is false for m > 3 prime to the characteristic, by later work of Cheng and van Dobben de Bruyn.

These are m^2 torus points. The three coordinate vertices, which are additional singularities of a full Fermat line arrangement, are **not** blown up. A lower bound uniform in m is **not** asked for and is false: the arrangement lines have strict-transform square 1-m. Boundedness for integral curves is equivalent to boundedness for all reduced curves by the standard Zariski-decomposition argument, but their optimal constants need not agree. For example, on X_3 two arrangement lines from different families have disjoint strict transforms; their reduced union has square -4 although b(X_3)=-2. Allowing nonreduced divisors makes any bound false, because (rE)^2 = -r^2 for an exceptional curve E.

## Retained results

1. b(X_1) = b(X_2) = -1 and b(X_3) = -2, with short proofs independent of negative-curve classification.
2. The Fermat pencil is a morphism X_m -> P^1. For m >= 2 its only singular fibers are three unions of m lines. Every irreducible vertical curve is a smooth whole fiber of square 0 or one of these lines of square 1-m. Exceptional curves are sections.
3. Every nonexceptional curve with equal multiplicities at all m^2 centers has nonnegative square. For m > 3 no positive multiple of -K_X is effective.
4. On X_4 an explicit infinite sequence of numerical classes passes every line-Bezout inequality, nef-fiber testing, and the arithmetic-genus inequality, while its square tends to minus infinity. None is represented by an integral curve: the first two are excluded by certified full-rank interpolation matrices, and the remainder by the known weak bounded negativity theorem. This is a negative control against mistaking numerical feasibility for a counterexample.
5. The characteristic-p power-image construction has a completely different explicit self-intersection formula over C, growing like d^2. Its only negative instance over C is a line case. Divisibility and finite-cover implications are established, but give no missing upward boundedness theorem.

PROOFS.md contains the arguments. APPROACHES.md records the five routes and the exact remaining gap. LITERATURE.md distinguishes later primary results and source versions. SOURCES.json contains only public source metadata and retrieval/inspection facts. CERTIFICATES.json contains authored finite certificates, not external dataset contents.

## Reproduction

Run `python3 verify.py --self-test` in this directory. For a pinned replay, also pass `--expected-manifest SHA256_OF_AUTHOR_MANIFEST_JSON`. The verifier uses Python's standard library, verifies the packet inventory and hashes, recomputes exact Gaussian-rational line incidences and modular interpolation determinants, and rejects deliberate mathematical-certificate mutations. CHECK_RESULTS.json records the expected deterministic mathematical output.

Computations certify finite arithmetic and the stated interpolation nonexistence claims. They do not certify every geometric argument, establish the general conjecture, or turn literature search into proof of global openness. A fresh uninvolved audit is required before publication. No remote write was made while preparing this author packet.
