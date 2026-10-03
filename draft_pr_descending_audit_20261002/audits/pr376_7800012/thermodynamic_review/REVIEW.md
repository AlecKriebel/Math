# Independent thermodynamic audit of PR376 / problem 7800012

## Verdict

Scoped PASS. The frozen packet at head 9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1 supports the five stated partial results and the disposition **unsolved, five substantive turns**. In particular, Turn5's canonical bulk existence and two-sided convexified finite-box comparison are valid for the stated sequence of even square side lengths. No mandatory mathematical repair was found in this thermodynamic audit. This is an independently checked mathematical scope verdict, not external peer review or certification of historical novelty.

The original question remains unresolved: no proof establishes e_opt >= e_* for arbitrary spatial phases, and no admissible exactly quarter-filled competing construction has certified energy density below e_*. Uniform-field twist optimization, finite local Hessian positivity, and the moment-defect minimizer do not supply this missing implication.

## Independence and source boundary

Before reading any frozen candidate file or old/root/sibling proof or verdict, I fetched and read the literal Princeton statement and the specified Lieb1994 and LiebLoss1992 primary sources. I derived the finite/bulk normalization, the q=4 characteristic polynomial, canonical variational and chemical-potential identities, density corrections, bond/rank boundary estimates, holonomy qualification, phase-separation conditions and analytic falsifiers. independent_seal.md binds the source-first derivation and exact polynomial output.

The Princeton technical statement fixes the sum of M/4 lowest adjacency eigenvalues of a unit-hopping finite periodic square lattice. It allows arbitrary edge phases. Lieb1994's half-filled theorem cannot be substituted; LiebLoss1992's all-circuit gauge equivalence retains the two winding phases on a torus. The packet states its finite and thermodynamic domains separately and does not treat the source's imprecise word “large” as a quantified bulk theorem.

Raw retrieved sources and the private copied frozen packet are ignored. Their receipts are in sources_receipt.md. All candidate access and execution were read-only against the frozen input; execution used its private copy entirely within this folder. No candidate, Git, remote, release or outside-person communication was performed.

## Direct proof audit

1. **Fixed-rank perturbations.** The one-bond increment has eigenvalues +/-|c|. The variational identity gives |E_r(A)-E_r(B)| <= sum|c_e|. I derived the same bound independently via half the trace norm of a traceless difference. It applies at every rank, with no gap or nondegeneracy assumption. Removing 2L wrap edges therefore costs <=2L, and a phase-changing seam costs <=2 per changed bond.
2. **Exact-rank upper tiling.** For even L,l, R=L^2-floor(L/l)^2*l^2 is divisible by four. Every complete l-box carries rank l^2/4, and a diagonal leftover projector carries R/4. A block-diagonal projector has zero cross-block entries; all restored unit hopping bonds contribute zero to its trial trace. The absence of an upper boundary penalty is justified by the explicit projector, rather than an unsupported equality of coupled spectra. This also handles incomplete cores for every even L, not only a compatible subsequence.
3. **Limit existence.** For fixed l, the normalized bound tends to f_l. Thus limsup f_L <= inf_l f_l <= liminf f_L. Compactness makes finite phase minima well-defined, and the norm bound ensures a finite lower bound. The torus/open difference divided by L^2 tends to zero. The limit is over every even square side L tending to infinity. Rectangular or fixed-width limits are not asserted by this theorem.
4. **Canonical allocation and convexification.** The r lowest eigenvalues of a direct sum are obtained by minimizing over all integer block ranks summing to r. Equal local quarter filling cannot be inserted into a lower estimate. The finite convex envelope C_l allows every rank, its extremizer uses at most two integer ranks, and the weights at q_l are rational. A square array whose side is a weight-denominator multiple realizes the exact mixture counts. No common Fermi energy hypothesis is needed for a valid trial allocation.
5. **Lower cut and quantifiers.** Cutting an L=k*l torus into open l-boxes removes exactly 2L^2/l bonds, including wrapping seams for k=1. Substituting F_l(r) at each assigned integer rank and averaging via C_l proves E/L^2 >= C_l(q_l)/l^2-2/l. Applying the already established full limit along this subsequence yields the claimed lower bound. The same reasoning works for all-rank lower certificates or an affine supporting line. It does not use an unproved estimate for F_l at mismatched ranks.
6. **Uniform benchmark and shell boundary.** The independently checked polynomial E^4-8E^2+4-z-z^{-1}-y^4-y^{-4} yields one isolated outer negative band per four-site fiber. There are M/4 occupied fibers, explaining the factor 1/4 in the density integral. The uniform spectral gap excludes a Fermi-shell sorting ambiguity even when occupied states are degenerate. The turn-three finite formula, both twist endpoint optima, derivative-sign/divided-difference proof, and uniform K*pi/L remainder are consistent. Holonomy dependence survives in finite volume and disappears in the two-dimensional limit.
7. **Finite competitors.** A torus trial at side l gives an open-box trial upper bound E/l^2+2/l. Only a certified comparison of this quantity (or a convexified exactly counted mixture) with a rigorous lower bound for e_* would give a bulk disproof. The packet explicitly requires this margin and produces no competitor. It does not extrapolate a small finite deficit.
8. **Remaining partial results.** Turn1's bipartite Cauchy bound, exact 4x4 saturation and zero-flux/two-twist tie are algebraically valid. Turn2's moments, completed squares and singular-value defect-to-energy estimate have their stated L>=8 scope. Turn4's occupied cluster is isolated despite its internal multiplicity; the Hessian formula has the correct negative second-order denominators and its exact Fourier kernel/trace reduction certifies an 8x8 local minimum only. No one of these transfers its central difficulty to a claimed global optimizer.

## Independent adversarial evidence

checks/thermodynamic_checks.py imports no candidate module. Its 17,809 exact controls verify geometrical cut counts, exact leftover particle budgets, a nontrivial block projector with unit joining bonds and zero joining trace, and a rigorous uniform bulk enclosure. The enclosure uses rational Machin pi bounds, a cosine Taylor remainder, directed integer square-root bounds, and an analytic periodic-cell Lipschitz error. It is not an empirical finite-lattice extrapolation:

    -0.682758268908 <= e_* <= -0.681881708457.

A generic traceless-Hermitian negative control has total rank two direct-sum energy -7, while forced equal local rank gives -6. This demonstrates the invalid allocation mechanism and is explicitly not represented as a lattice competitor. A wrong-rank four-cycle energy comparison is rejected by exact particle count. A seam-only comparison is bounded by 4/L per site, so a finite twist effect cannot be promoted to an extensive deficit. Source-first checks independently confirm the q=4 polynomial and the 4x4 normalization.

## Reproduction and exact remaining gap

The full author replay, all five individual stdout/stderr streams, and the entire regenerated Hessian Fourier certificate are preserved under checks/author_streams. REPLAY_ALL.py reproduced 102,005 assertions and 157 manifest bindings. The source-free run honestly reports zero source checks. A separate source-supplied replay verifies all three independently fetched source bytes. No stream has an error or nonzero exit.

The successful numerical/algebraic controls substantiate their declared finite assertions. The thermodynamic conclusions rely on the written variational and boundary arguments, not on a count of assertions. No cross-review agreement was used to reach this verdict.

The best verified unrestricted result is

    -1/sqrt(2)+11(3sqrt(2)-4)/1536 <= e_opt <= e_*.

The exact gap is the unsupported reverse bound e_opt >= e_* (or a strictly better admissible trial configuration). The convexified finite-box principle retains the central difficulty in the unknown all-rank phase minima F_l(r), rather than pretending those quantities have been solved. That route is a valid framework; any attempted conclusion from unsupported matching F_l bounds is blocked until new evidence supplies them.

## Minor expository observations

No mandatory repair. The independent pre-candidate note used a deliberately coarse opening-plus-restoring upper tiling error 4/l; the candidate's explicit block-projector construction proves the sharper zero joining cost and is correct. In the independent canonical chemical-potential formula, use lambda_0=-infinity and lambda_{M+1}=+infinity to include empty/full rank endpoints. These are qualifications to this review's independent preliminary derivation, not candidate defects.
