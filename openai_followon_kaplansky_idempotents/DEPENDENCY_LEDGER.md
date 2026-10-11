# Dependency ledger

| ID | Precise assertion | Assumptions / evidence | Status / exact gap |
|---|---|---|---|
| D1 | October 4 Theorem 1.1 constructs finite-presented torsion-free G with finite 2D K(G,1), a,b,c in F_2[G], ab=1, ac=0, c≠0 | Pinned OpenAI manuscript; no applicable Lean formalization identified | D2–D5 checked in separate detailed source audits; no substantive gap found. Existential rather than numerical |
| D2 | Parity criterion gives the three scalar identities | Finite loopless immersed graphs, stated intersection parities, protected B root | Complete independent algebra proof and source audit; root verified |
| D3 | Balanced types / conditioned matching model realizes prescribed labels | q=128; projective plane; Fano complements; m≡1 mod4 sufficiently large | source_combinatorics audit complete; exact supplemental computations reproduce incidence and contraction |
| D4 | Bounded pattern estimate plus planar extraction excludes every reduced spherical arrangement | Girth conditioning, bounded diameter, fixed small unpaired fraction | Complete source_combinatorics audit and root reconstruction; repeated-edge stage bounds and quantifier order checked |
| D5 | No reduced spherical arrangements implies asphericity and root protection | Finite labeled graphs, girth≥3 | Complete source_topology audit and root check; all four surgeries, endpoints, cone lifts, asphericity and torsion argument checked |
| D6 | e=1-ba nontrivial idempotent and module claims | Unital nonzero ring, ab=1, ac=0, c≠0 | Self-contained proof in main.tex and ALGEBRA_PROOF.md; maps are left multiplication on right modules |
| D7 | F_2[G]→K[G] injective | K field characteristic 2; group basis | Self-contained coefficient proof; every characteristic-two field, no change of characteristic |
| D8 | Exact positive-characteristic Kaplansky idempotent conjecture and classical reduction | Öinert Problem 1(c); Gardam pinned lecture proposition; Ara et al. report p9; Weibel K-book II.2 | Primary texts inspected independently; mechanism classical. Exact earliest-original attribution not claimed |
| D9 | Core consequence and proof outline already publicly disclosed | Public triage files at f27318d83bd7000ef817957a9a4b3087de28d198; decoded blobs and hashes in priority evidence | Affirmative duplication witness; user rule withholds new-discovery publication |

All upstream manuscript references resolve to sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026 at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. Source publication/citation alone does not certify a claim.

Scope: these are checkable mathematical proof audits, not human refereeing or a formalized full theorem. Fresh complete-package audits additionally test cross-file consistency, claims and reproducibility. No source or companion in a different characteristic, group with torsion or analytic algebra supplies a missing dependency.


## October 6 quantitative refinement

| ID | Precise assertion | Evidence | Status and limit |
|---|---|---|---|
| E1 | Exact 3-class quotient of squared turn matrix, any allowed inverse pairing | main.tex Eq(2), direct full matrix row audit | Verified; classes E,S,O count the excluded inverses |
| E2 | q=32 rho<1, word sum≤(5376/5)(987/1000)^(h−1) | exact ratios and positive vector;verify_parameter.py | Verified, no floating point dependence |
| E3 | q=4,8,16 rho>1 andword sum grows≥Cq(503/500)^(h−1) | common exact positive vector;full matrixindependent check | Verified; obstruction only unchanged decay criterion |
| E4 | q=32 full asymptotic construction valid | changed capacity, degree, switching, expansion, closure constants;parameter and independent falsification audits | Verified bysource proof adaptation, not numerical matching |
| E5 | finite PG(2,32) label certificate | GF32 irreducible polynomial, exhaustive field/incidence/Fano/inversechecks;data hash | Verified; no group witness certificate |
| E6 | classical 2-generator HNN host preserves finite 2D K, torsionfree, ringtriple | HNN 1949, Morozov–Schupp Obs.3.4, explicit free bases and tree-of-spaces proof | Verified standard machinery; no new embedding claim |
| E7 | refinement distinct from prior public core | exact pinned source/companions/triage inspected and current primary searches | Modest model calibration absent from checked texts; no first-priority claim |

D3's original q128 remains the historical source audit. E1–E4 explicitly adapt it; the source is not silently repinned. Original duplication D9 still applies to the core but does not disclose E1–E3. Complete package reviews of the prior core candidate do not certify this changed package.
