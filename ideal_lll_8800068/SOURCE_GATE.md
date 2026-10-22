# Source gate: worst cases for LLL on ideal lattices

Date: 2026-10-20 UTC. ID 8800068 / AMR-087-0068.
Scope: historical source-recovery snapshot preceding the proof attempts.

## Decision

**PARTIAL SOURCE RECOVERY / HOLD FOR PRECISE TARGET AND STATUS.** The historical question and its lattice model are recovered. The source does not fix the LLL parameters, exact sharpness criterion, or input-basis convention. No verified primary theorem resolving the requested ideal/cyclic lower-bound family was located. This is not a claim that the problem remains open in 2026. Do not inherit the catalog's “partially_solved” status as mathematical evidence.

## Historical source and model

Daniele Micciancio, *Ideal Lattices: cryptographic applications and open problems*, IPAM workshop, October 13, 2006, attachment 6240. The workshop schedule verifies speaker/date; its PDF title differs slightly from the schedule title.

- [Workshop schedule](https://docs.ipam.ucla.edu/today/helper_schedule.php?pc=SCWS1)
- [Primary slides](https://helper.ipam.ucla.edu/publications/SCWS1/SCWS1_6240.pdf), PDF page 37 (zero-based 36).

The relevant question is: “Find cyclic (or ideal) lattices where LLL achieves worst-case approximation factor”.

The definitions on PDF pp.8 and 23 use cyclic coordinate rotation and the coefficient map from Z[X]/q(X) to Z^n, with q monic of degree n. Ideals map to ideal lattices; q=X^n−1 gives cyclic lattices. Irreducibility is not imposed on this general definition. Subsequent cryptographic discussion specializes to irreducible polynomials, notably X^n+1 for power-of-two n (pp.24–26). Those specializations are not restated as restrictions on the question. The surrounding algorithmic target is approximate SVP/SIVP in Euclidean geometry, not runtime. The question itself does not distinguish these two targets or state an exact factor, δ, η, basis normalization, or asymptotic quantifier. It also does not require a principal ideal or a circulant input basis.

This recovery does **not** license replacing coefficient geometry with a freely chosen weighted canonical embedding. Such a replacement changes the problem. Full rank should be explicitly required for a proposed n-dimensional test family; a nonzero ideal in a reducible quotient need not have rank n.

## LLL conventions available from primary literature

[Nguyen–Stehlé, *LLL on the Average*, corrected ANTS VII 2006 paper](https://perso.ens-lyon.fr/damien.stehle/downloads/average-corrected.pdf), §2, PDF pp.3–4, gives the standard two-parameter convention:

- |μ_ij| ≤ η, with 1/4 < δ ≤ 1 and 1/2 ≤ η < sqrt(δ).
- δ ||b*_(i−1)||² ≤ ||b*_i||² + μ²_(i,i−1)||b*_(i−1)||².
- Set α=(δ−η²)^−1. Then ||b_1||/λ_1(L) ≤ α^((n−1)/2), while ||b_1||/det(L)^(1/n) ≤ α^((n−1)/4).
- Original parameters (3/4,1/2) give α=2. Parameters approaching (1,1/2) give α approaching 4/3.

These are different approximation measures. Calling a root-Hermite factor “the SVP approximation factor” is incorrect. The same paper studies experimental/heuristic average behavior, not a verified cyclic-ideal extremal construction. Its author page warns about a corrected constant; the corrected PDF above was used. See [author description and correction notice](https://perso.ens-lyon.fr/damien.stehle/practLLL.html).

The formulas above supply a possible convention, not missing text from the 2006 problem. A proof task must choose δ, η, and one target explicitly. For polynomial-time classical LLL discussion use a fixed δ<1; treating δ=1 as interchangeable requires a separate complexity justification.

## Quantifier and input safeguards (audit requirements, not claimed source statements)

A defensible lower-bound formulation must specify a growing-dimensional family of rings/ideals, their coefficient lattices L_n, and bases B_n. Then choose whether the goal is:

1. Existence of an LLL-reduced basis with a first-vector ratio close to the general guarantee.
2. A deterministic LLL execution from specified input bases producing such output.
3. The stronger requirement that a canonical representation such as HNF produces such output.

These are not interchangeable. A poor reduced basis can be a stationary input for an appropriately specified exact LLL routine, but that alone says nothing about HNF-start behavior, randomized restarts, or all bases of the same ideal. Likewise, a worst input basis is not an ideal intrinsically difficult for every algorithm or every basis representation.

For a proposed family, declare whether n ranges over all sufficiently large dimensions or an unbounded subsequence; whether q is X^n−1, X^n+1, or varies freely; whether ideals are principal; whether the output is b_1 or the shortest vector among all returned basis vectors; and whether “achieves” means equality, arbitrarily close for each n, a constant-factor lower bound, or matching exponential rate. These choices can materially change the task. None should be silently filled in as an authorial assertion.

A cyclic quotient group Z^n/L does not establish invariance under coordinate rotation. Neither do a knapsack-shaped basis nor an arbitrary isometry establish the required coefficient ideal structure. Any proposed transfer must explicitly verify multiplication by X preserves L in the declared quotient ring.

## Status audit and exclusions

The local source record contains a purported partial result attributed to “Nguyen–Stehlé (2000)” involving modular knapsack/cyclic structure, with no title, DOI, theorem, or explicit family. Searches did not verify it. The [author bibliography](https://perso.ens-lyon.fr/damien.stehle/index.html) identifies *Floating-point LLL Revisited* as 2005 and *LLL on the Average* as 2006. This does not prove that no other result exists, but the local attribution cannot support an acceptance decision.

A particularly relevant primary paper is [Plantard–Susilo–Zhang, *LLL for ideal lattices: re-evaluation of the security of Gentry–Halevi’s FHE scheme*](https://thomas-plantard.github.io/pdf/PlaSusZha14.pdf), DOI [10.1007/s10623-014-9957-1](https://doi.org/10.1007/s10623-014-9957-1), accepted March 4, 2014. Its §2.2 specifies (δ,η)-reduction; Theorem 2 concerns correctness of iLLL. Its contribution is reusing rotated vectors to improve running time while retaining LLL output quality. Its worst-case bit-complexity comparison, average-case analysis, and experiments do not construct ideals attaining the general worst-case approximation ratio. Do not mistake “same quality guarantee” for a matching lower bound. The paper uses specialized ideal/HNF forms; it is not a replacement definition for all ideals in the original source.

Also, [Peikert–Rosen, ECCC report 2006/147](https://eccc.weizmann.ac.il/report/2006/147/download), §1.4, discusses worst-case short-vector assumptions for number-field ideal lattices. This is a hardness-assumption context, not a proof of worst-case LLL output quality. Average-case cryptographic reductions and special ideal-SVP algorithms likewise do not settle the requested lower bound merely by existing.

Search coverage included exact-title/phrase searches and combinations of LLL, cyclic lattices, ideal lattices, worst case, reduced bases, and the catalog's author/year attribution. No current exhaustive bibliography or definitive later-status statement was recovered. A broad unsolved claim would therefore overstate this audit.

## Retrieval evidence and limitations

The exact historical PDF was downloaded successfully and text-extracted. The web PDF extractor corroborated the page-37 question and definitions. A web screenshot request for page 37 returned an internal error; this was not a source-access denial. The original Zhenfei Zhang iLLL URL was search-indexed but returned HTTP 404 on direct download; a working author-hosted copy on Thomas Plantard's site was found and downloaded instead.

Retrieved primary PDFs (hashes and sizes only; source documents are not redistributed):

- Micciancio: 824541 bytes; SHA-256 878de5ec70efe17303b591df6154c833d14c35bf096470df454fc6e22ac4d4c2.
- Plantard–Susilo–Zhang: 583160 bytes; SHA-256 6633f875d29c448de30b45955984c05d740fef4f13d88167bc6e5e4db29b14d4.

The catalog subject label “Graph Theory” and machine-produced status commentary are not primary mathematical evidence. No catalog records or dataset contents are included.

## Before a proof attempt

Choose and document one precise formalization above, then perform a targeted follow-up status search for that formulation. In particular, require an actual theorem and explicit ideal/cyclic membership argument before accepting the catalog's alleged partial progress. The present result is source recovery with unresolved convention/status gates, not a solved result or a failed proof turn.
