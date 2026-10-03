# Curve-cover / incidence-duality audit of frozen PR378

Frozen candidate head: **5da73632ab7a621de7b62edb5f70dfb8017e4a50**. Snapshot manifest SHA256: **cbc37df7cf062c444f42f5c81f600505dc7bcb1b662190a06a920196b4fa3c1f**.

## Result and disposition boundary

No mathematical defect was found in the cover/duality claims actually stated by the frozen five-turn packet. The unrestricted line-arrangement conjecture remains unresolved. This report supplies scoped mathematical evidence for the parent audit; it does not accept or merge the PR, certify novelty, or authorize publication of the post-exposure extension.

The strongest additional checked result concerns the final 9q-line residue subfamily. Its unrestricted fractional line-cover optimum is **11/3 at q=1 and 4q at every q>=2**. The frozen packet only claims component optimum 4q and explicitly declines unrestricted optimality, so this is a strengthening, not a mandatory correction. A fresh adversarial review of this extension was requested from the parent before promotion.

Every auxiliary line in that subfamily has at most q+1 singular points, with deleted Fermat lines attaining the bound. This also sharpens the packet's valid 4q auxiliary-line bound. For q=1 the repaired cover raises the all-nonlinear-curve lower bound to 3/11; the Seshadri value stays 1/5.

## Independence and source scope

Before reading any candidate, prior audit, root output, or sibling output, literally first opened [the EMS primary PDF](https://ems.press/content/serial-article-files/46833), read printed 3295-3297, and locally rendered/viewed all three pages. Also read the definition at printed 3272. The primary target is epsilon(P2,O(1);Z)=1/K, with Z the full nonempty singular set of a reduced arrangement of distinct complex lines and K the maximal collinearity over **all projective lines**. Irreducible reduced test curves must meet Z. Empty singular sets are excluded; concurrent arrangements and reducible effective witness polynomials are treated explicitly.

The assignment exposed the mechanism label curve-cover/duality and the suggestion to devise a 9q-line family. I first derived a different family, full Fermat n=3q, with K=3q+1 and exact component/all-line cover optimum 3q. A self-contained exact cyclotomic checker verified all pair-line columns for n=1,2,3,6,9. n=2 independently supplied a strict LP-domain distinction: component optimum 3, unrestricted optimum 5/2. The independent proof, checker, full stdout, source PDF and renderings were sealed at **2026-10-03T04:31:03.826290Z** in independence_seal.json. Every sealed hash still verifies. Only afterward did a file inventory expose sibling filenames; no sibling file content was used.

After exposure, read [Pokora v3](https://arxiv.org/pdf/1711.09364v3), rendered/viewed printed 6-7, and checked Question 3.1, Proposition 3.3, Example 3.4. These support the existing Fermat credit and show why its component-line question should not replace the OWR all-line target. This is a bounded primary-family check, not a claim that the literature contains no matching theorem. Historical novelty is unverified.

## Independent mechanism and exact gap

For nonnegative line weights covering each p in Z with total T, weighted Bezout gives sum mult_p C<=T deg C for every integral curve outside the positive line support. A support line has ratio at least 1/K by its point count. Therefore epsilon>=min(1/T,1/K); if T<=K, a K-point line gives equality. The supported-line exception must be explicit. A matching feasible point-weight dual proves exact LP optimality by finite weak duality.

Component and arbitrary-line LP domains are different. For |Z|>=2 the unrestricted domain can be reduced to the finite set of distinct point-pair lines: singleton columns are dominated by pair-line columns and empty columns are useless. A component dual requires extra checks before it is globally feasible. A cover cost exceeding K is a blocked certificate route, not a counterexample to the conjecture.

In the full Fermat family, all auxiliary lines have at most two singular points. For the key three-nonzero-coefficient case, exact roots-of-unity conjugation gives a nonzero quadratic in one coordinate, so at most two grid points occur. This algebraic classification, rather than floating point or extrapolation from a scan, proves the all-n dual feasibility. The generic-arrangement gap remains finding a cover of cost at most actual K or a separate all-curve multiplicity argument. Neither the independent reference family nor the candidate resolves that gap.

## Integration check of all five proofs

All five full TURN files and all five checkers were read, along with final scope, author/turn manifests, old review prose/code, and historical binding records.

* Turn 1: The genus inequality on the integral strict transform, Cauchy-Schwarz step, monotonicity threshold and exact integer-root cutoff are consistent. The effective-coordinate restriction and strict r<k^2 range remain explicit. Reducible/nonreduced kernel polynomials still upper-bound epsilon through a component ratio; thus no irreducibility oracle is hidden in the finite algorithm. The general range and r=k^2 boundary remain outside the result.
* Turn 2: The support-line exception and tau<=k0 certificate establish all-line maximality before the global dual is invoked. Hesse component optimum 6 and all-line optimum 9/2 are correctly distinguished. The final dual uses the independently obtained primal cardinality bound, with no circular optimality assumption.
* Turn 3: Absorbing lines through the modular point preserves coverage. The at-most-two outside points argument handles every stated branch and degeneracy. Adding zero-weight component lines to the finite exception list is legitimate; positive support and cover cost are unchanged. The high-multiplicity dichotomy is valid.
* Turn 4: n>=3 prevents the invalid n=1,2 full-family extension. Exact losses require both other lines deleted; the retained-center requirement is explicit. The sumset condition, strict budget inequality and pair/triple correction in total losses are consistent. Sufficient deletion criteria are not promoted to necessary criteria.
* Turn 5: Distinct roots, pair-intersection exhaustion, 7q^2 triple grid points, 6q^2 double grid points, and three centers hold for every positive q. q=1 centers remain singular and do not collide with grid points. Component counts 3q+1 and 4q+1, primal cost 4q, all-degree Bezout bound, all-line K=4q+1 and exactly 6q computing components are valid. The dual proves only component optimality as written.

At q=1, the Turn 5 dual has load 3/2 on each of the six lines joining the unique 000 point to a double point. Extending that dual unchanged to the unrestricted LP would be false. The candidate never makes that extension, so there is no corresponding defect to correct.

## Stronger checked replacement for the unclaimed unrestricted optimum

The analytic all-q proof is in stronger_all_line_optimum.md. For q>=2, the candidate dual is globally feasible: retained lines have load 1, deleted Fermat lines load 1/2, axes/non-root-ratio lines load zero, and any remaining line has at most two grid points and load at most 2/q<=1.

For q=1, the unrestricted primal uses residue-0 component weights 1/9, residue-2/3 component weights 4/9, and weight 1/9 on each of the six 000-to-double joining lines. Every point receives coverage exactly 1, total 11/3. A global dual assigns 2/3 to 000, 1/3 to doubles, 1/6 to 023 triples, and zero to vertices. All support loads are at most 1 and its total is 11/3. The full classification handles every other line, including singleton columns. This proves equality without a numerical solver.

The post-exposure exact checker uses the previously sealed field implementation, reconstructs actual projective equations, exhausts every arrangement intersection, and checks every distinct point-pair line for q=1,2,3. Its full outputs report respectively 51, 921 and 5268 pair-lines and global optima 11/3, 8 and 12. The all-q conclusion rests on the analytic proof, not these samples.

## Reproduction and hash boundaries

Fresh private author replay: **214070 assertions**, **62 manifest entries**, all turn receipts byte-exact, empty stderr. Fresh replay of the old independent checker: **93918 assertions**, full stdout byte-exact against INDEPENDENT_CHECKS.json, empty stderr. Full stdout is preserved, not excerpts. All 47 frozen snapshot files, eight pre-exposure seal files, 36 historical local Git-blob bindings and seven old-review manifest entries verify.

Portable replay reports **source_files_checked=0**. Separately downloaded EMS and Pokora PDFs match their two original source bindings. The four other historical source artifacts, including the old exact screenshot, were not reproduced in this family audit. Locally rendered/viewed screenshots establish direct reading but are not substituted for the old screenshot hash. No fresh remote-Git binding or external service audit was performed by this agent.

All writes stayed within cover_duality_review, including private replay copies and a local SymPy dependency used only for the old/author replay. The independent exact code itself has no external package dependency. No candidate byte, branch, index, service, Git history or remote was changed; no external individual was contacted. Raw downloaded sources and runtime_deps are local verification inputs, not deliverables for public redistribution.

Local family-audit completion best guess: **100%** for the assigned source/cover/duality and frozen integration checks. Post-exposure strengthening: analytic and exact-computational checks complete; adversarial promotion gate remains with the parent. Original conjecture status: **unresolved**. No completion percentage is being substituted for a proof of the global target.
