# Arithmetic triage (families 001–031)

Checkpoint: 2026-10-06 Pacific; triage completion estimate 85%. This is consequence screening, not verification of the new underlying proofs. Corpus-wide title/TeX searches were used to exclude announced corollaries. No external communication occurred.

## Recommended stream: deterministic finite-field construction and root extraction

**Exact initial deliverable:** remove Weak GRH from deterministic r-th nonresidue searches in prime fields, general fixed-r root extraction, and the standard irreducible-polynomial/finite-extension construction reductions. State the input model and dependence on r, extension degree n, and log p explicitly; do not claim polynomial in log r where algorithms require polynomial in r. Combine with the computation agent's finite-field factoring stream.

**Mechanism:** release 003 proves a common zero-free half-plane Re(s)>7/8 for every Dirichlet L-function. Functional equations give the matching left boundary. Thus the Weak GRH hypothesis of Bhargava–Ivanyos–Mittal–Saxena 2017 §6.2 holds, for example with epsilon=7/16 after slightly enlarging the strip. Their Theorem 6.7 yields a bound O(log(p)^32) for the least r-th nonresidue, not just quadratic nonresidues, and the paragraph following explicitly lists r-th root finding, constructing irreducible polynomials, and restricted factoring as applications. These are short deduction/algorithm-audit projects, not new analytic work.

**Evidence:** /Users/alec/Desktop/math/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/build/paper.tex:107 (main theorem); :325 (only quadratic/nonresidue and square-root corollary); /Users/alec/Desktop/math/lean/docs/003.md confirms the formalized half-plane and says later applications are outside Lean scope. Primary prior source: https://arxiv.org/html/1702.00558 (Theorem 6.7, §6.2 and immediately following discussion).

**Gap and risk:** audit each finite-field construction theorem's precise GRH use and extension representation; do not transplant a prime-field result to all extension fields without the known algebraic reduction. General root extraction in arbitrary extensions needs the field-model reduction. Prime-field square roots, Vinogradov's least quadratic nonresidue conjecture, and Miller primality derandomization are already explicitly in the release and are not new targets. The candidate is mathematically high-confidence as a consequence, with moderate incremental novelty. Likely hours to days for exact statements and a checked proof, more for executable artifacts.

## Certain but less novel: rational points remain undecidable for smooth projective varieties

**Exact claim:** there is no algorithm deciding whether an arbitrary smooth projective geometrically integral variety over Q has a Q-point. Dimension is unbounded and is part of the input. If desired, preserve Turing degree 0-prime under the existing reductions.

**Mechanism:** release 004's H10(Q) undecidability plus Poonen's 2009 JEMS Theorem 1.1(i), which reduces decision for arbitrary varieties to decision for smooth projective geometrically integral varieties over any fixed number field. Its contrapositive with k=Q settles the claim directly.

**Evidence:** /Users/alec/Desktop/math/preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/build/sections/01-introduction.tex; strongest source normal form /Users/alec/Desktop/math/preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/build/sections/07-consequences.tex. Primary reduction: https://math.mit.edu/~poonen/papers/chatelet.pdf ; journal https://ems.press/journals/jems/articles/1924 . No matching claimed consequence found in corpus searches.

**Gap and risk:** only composition of existing results; thus very high confidence but low independent novelty and likely already regarded by experts as part of H10. Do NOT claim undecidability for fixed dimension, curves, smooth hypersurfaces, or general number fields; these do not follow. H10 paper explicitly does NOT give many-one completeness or a diophantine definition of Z in Q. It already gives degree-at-most-four inputs, sum-of-squares-of-quadratics inputs and Turing degree 0-prime; those are excluded.

## Lower-priority equivalence: identify the canonical motivic Galois group with GRT

**Exact first target:** the canonical injective graded map from the unipotent mixed-Tate motivic Galois Lie algebra over Z to grt_1 is an isomorphism. Brown gives injection and the source is free on one generator per odd weight >=3; release 008 gives the same Hilbert function for the target, so finite weightwise dimension comparison gives surjectivity.

**Evidence:** /Users/alec/Desktop/math/preprints/The-Deligne-Drinfeld-conjecture-September-23-2026/build/sections/01-introduction.tex:84–110 explains both ingredients; /Users/alec/Desktop/math/lean/docs/008.md specifies the exact rational Lie algebra and completion covered. The paper explicitly already states H^0(GC_2) as a completed free Lie algebra, so graph-complex H0 is excluded.

**Gap and risk:** almost an equivalent reformulation of DD; little independent novelty. A larger project can derive a precise completeness statement for associator relations among **motivic** multiple zeta values, after checking the torsor identification and weight-two parameter. This does NOT prove period injectivity or numerical MZV algebraic independence. Do not rank ahead of more distinct new consequences.

## Important exclusions / routes that are not straightforward

- QRH alternate paper already states effective prime distribution in progressions, Miller primality derandomization, class-number lower bound h(D) >> sqrt(|D|)/loglog(|D|), and completeness of Euler's 65 idoneal numbers: /Users/alec/Desktop/math/preprints/The-Quasi-Riemann-Hypothesis-October-5-2026/build/paper2.tex:90–127.
- Full RH, optimal log-squared nonresidue bounds, and full Artin density do not follow from the fixed Dirichlet strip. Artin density needs Kummer-field analytic input absent here.
- Modularity of all elliptic curves over imaginary quadratic fields suggests modular-method Diophantine applications, but a blanket Fermat theorem is not immediate: residual modularity/level lowering, torsion Bianchi classes, fake elliptic curves, and local S-unit hypotheses remain. Primary comparator https://arxiv.org/abs/1908.11690 makes its Serre-modularity dependence explicit. No quick specific new field was certified in this scan.
- Density-one BSD for quadratic twists is explicitly already announced in 002+006. Finite Sha does give algorithmic consequences, but no sufficiently distinct new high-impact statement was checked here.
- Full higher Chowla, joint higher prime-factor statistics, Carmichael x^(1-o(1)), and all-number-field H10 cannot be inferred merely from the binary/one-field inputs; missing uniformity or extra variables preserve the central difficulty.
