# Attempt 5: full polynomial-bit extremality theorem, with audit boundaries

Date: 20 October 2026. Proposed resolution for the exact rational sparse-list problem. This manuscript is an authored derivation, not a claim that a new efficient orbit-counting algorithm was invented. It imports Agol–Hass–Thurston's algorithm through the reduction below. Novelty relative to all literature is not independently established.

## Theorem

For a rational f and a rational, periodic, piecewise-linear minimal valid function for the one-row Gomory–Johnson infinite group problem, supplied by a sparse sorted breakpoint list and rational point values and one-sided limits, extremality can be decided in time polynomial in the total binary input length.

The input may be discontinuous from both sides at zero. The competitors in the definition of extremality are unrestricted valid functions, not functions restricted to the input grid or any prescribed regularity class.

## Proof assembled from the preceding attempts

1. Add f to the breakpoint list if necessary, and let q be the least common multiple of the breakpoint and f denominators. Then log q=O(L), where L is total input bit length. Set N=4q, but do not enumerate its grid.

2. By Basu–Hildebrand–Köppe Part I Theorem 4.11, unrestricted extremality is equivalent to uniqueness of the complete normalized N-grid point/affine tight system (10). Subtract the given function to obtain a homogeneous system for h. This imported theorem is what justifies reducing arbitrary competitors to a finite PL system. No separate continuity assumption is inserted.

3. Build the sparse arrangement of x=b, y=b, x+y=b, including relevant periodic translates in [0,1]^2. Use genuine relative strata: a closed triple intersection with no simultaneous relative-interior realization is not a face with the claimed trace data. Each input slack is nonnegative affine on its face, so its zero set is empty, one vertex, one edge, or the whole face. Polynomial-time rational geometry suffices; even enumerating all triples of sparse cells takes only polynomial time.

4. By the local equivalence in Attempt 3, rewrite the homogeneous N-grid system as three independent families of signed interval-pairing/zero-range relations for slopes, jumps, and spikes, plus polynomially many residual endpoint-sector equations, periodic compatibility, and h(f)=0. The normalization h(0)=0 is built into the trace reconstruction. Every zero limiting-face incidence is retained. Six open local sectors, six rays, and the origin suffice for endpoint equations; feasible directions are determined by exact rational comparisons.

5. Let K be the number of residual equations and D the total dimension of the three local signed systems. By Attempt 4, AHT computes D in polynomial bit time. If D>K, the residual system has a nonzero kernel. Because the slope/jump/spike representation is injective after normalization and periodic compatibility, this yields a nonzero N-grid h satisfying the complete tight system, so the input is not extreme.

6. If D≤K, extract all free signed-orbit representatives by prefix-flip binary searches, using at most O(K log N) AHT calls. Weighted AHT reconstructs their signed prefix sums and singleton values at every required projected sparse vertex and at f. Retain original forced-zero relations, but remove the temporary SEARCH flips before reconstruction. This produces a K-by-D rational matrix for the residual equations.

7. Compute its exact rational rank. Its kernel is zero exactly when the complete N-grid system has zero kernel, hence exactly when the input is extreme by Step 2. This is a decision algorithm; an exponentially long explicit perturbation need not be output.

8. The number of pairing descriptions, zero ranges, marker coordinates, prefix boundaries, and residual equations is polynomial in L. All pairing endpoints have O(log N)=O(L) bits. Counts and signed sums have magnitude at most N. Reconstructed trace coefficients have denominators dividing 2N and numerators of O(log N) bits. AHT's weighted runtime is polynomial in these encoded parameters. Exact rank of the polynomial-size rational matrix is also polynomial bit time. Therefore the total runtime is polynomial in L.

This proves the stated theorem, conditional only on the cited established BHK and AHT theorems and the fully stated local/orbit lemmas proved in Attempts 3–4.

## What the theorem does not say

- It does not establish strong polynomiality: gcd/lcm arithmetic, prefix searches, and orbit algorithms depend on binary lengths.
- It does not cover arbitrary irrational input encodings or higher-dimensional group relaxations.
- It does not replace unrestricted competitors by original-grid competitors.
- It does not claim that the existing practical grid-free code already has this complexity.
- It does not require accepting the earlier weak NP-hardness conjecture as a theorem. The reduction would rule out such hardness for this exact promised language unless P=NP, but that is a consequence, not an ingredient.
- It does not claim an implemented compressed AHT-based extremality solver. The attached scripts implement dense exact validators for the new reduction, not its asymptotically fast implementation.

## Primary sources

Basu, Hildebrand, Köppe, *Equivariant Perturbation in Gomory and Johnson's Infinite Group Problem. I. The One-Dimensional Case*, https://arxiv.org/html/1206.2079v2, especially Theorem 3.2 and Theorem 4.11.

Agol, Hass, Thurston, *The Computational Complexity of Knot Genus and Spanning Area*, https://arxiv.org/html/math/0205057v2, especially Theorems 12 and 16.

Original complexity question: Köppe's contribution in *Combinatorial Optimization*, Oberwolfach Reports 2014/51, printed p. 2899, https://ems.press/content/serial-article-files/46541.

## Validation status

The exact sparse-face reduction was checked against the complete dense q-grid tight system on 35 rational minimal inputs, including five two-sided-discontinuous inputs. All full, structured, and joint matrix ranks agree. Five genuine 4q refinements also passed exact full/structured/joint row-space comparison, including two-sided-discontinuous inputs with both zero and nonzero kernel. The end-to-end dense signed-orbit pipeline independently reproduced the full 4q nullity on four cases (nullities 0, 32, 0, and 2). These are recorded in `checks/fourfold_refinement_results.json` and `checks/orbit_pipeline_results.json`. Independent signed-orbit and trace checks are recorded in Attempt 4. The continuous special case has an additional independent proof and tests under `structural/`.

The original source gate alone was not a resolution. The accompanying acceptance report records the review status of this proposed full theorem.
