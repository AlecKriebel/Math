# Independent adversarial verdict: global bounds family

Sealed 2026-10-03 05:49:48 UTC. Audit completion estimate: 95%; original optimal-flux discovery remains unresolved. No prior review report, prior independent checker, root verdict or sibling verdict was consulted before this verdict. Candidate README's review-PASS label was incidentally visible after the independent baseline was sealed; it supplied no proof input.

**Scoped verdict: PASS. No mathematical defect found in the candidate's global finite-volume inequalities, their hypotheses, stated defect sharpness, or thermodynamic comparison theorem. The original quarter-filled optimal-flux claim remains unproved.** The missing comparison is acknowledged consistently in the five-turn result; it is not concealed by the defect optimizer or local certificate.

Candidate identity supplied by the audit coordinator: PR376, original packet at head `9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1`. This agent made no Git or remote mutations, no contact with external individuals, and no edits to candidate files. The audit is confined to its assigned directory.

## Source-normalized claim and evidence boundary

The [original Lieb problem](https://web.math.princeton.edu/~aizenman/OpenProblems_MathPhys/9802.OptFlux.html) asks whether uniform pi/2 flux minimizes the lowest-quarter spectral sum when all unit-modulus edge phases are admissible. This candidate provides scoped finite and bulk results, not the missing arbitrary-field comparison. The [1994 paper](https://arxiv.org/pdf/cond-mat/9410025) concerns half filling, and the [Lieb–Loss 1992 paper](https://arxiv.org/pdf/cond-mat/9209031) gives circuit-flux gauge equivalence. Neither is used to infer quarter optimality. The original problem's informal face-only spectral assertion requires the two torus loop holonomies in finite volume; the candidate supplies them.

The source-first independent baseline and exact controls were sealed in `receipts/baseline_seal.sha256`. Relevant candidate executables were read in full before execution: `gaussian_matrix.py`, `verify_turn1.py` through `verify_turn5.py`, `hessian_certificate.py`, and `REPLAY_ALL.py`. This verdict independently analyzes the global bounds and bulk comparison; full Hessian formula/code were read and replayed, but the separate local-Hessian audit family is responsible for its independent matrix reconstruction.

## Global proof ledger

| Claim | Independent check and mechanism | Status / exact scope |
|---|---|---|
| Complete face-plus-two-loop torus coordinates | Spanning-tree elimination; final closure is exactly the product-one face condition. Fourier twist control changes energy while faces stay fixed. | Verified on the stated finite square tori. |
| Projection reformulation of the phase optimum | Rank-q spectral variational principle followed by independently minimizing each edge's real contribution. Compactness permits joint minimization. | Verified; still an unsolved Grassmannian maximization. |
| E_q >= -N/sqrt(2) | Bipartite singular values, sum s_j^2=2N, q=N/4 and Cauchy-Schwarz. Equality requires the top q singular values sqrt(8) and the rest zero. | Verified for even side L>=4. |
| Exact L=4 global minimum and zero-face-flux tie | Polynomial spectrum T^3=8T and tr(T^2)=4N. Independent exact Gaussian trace control plus analytic Fourier spectrum. | Verified; -8sqrt(2), not a large-lattice theorem. |
| Non-saturation for even L>=8 | Unique length-three horizontal displacement of modulus one is incompatible with T^3=8T. | Verified; the L=6 exclusion is necessary for this argument. |
| Fourth and sixth moments | Independent stack reduction of all length-six direction words gives 232/144/24 returning classes. Independently multiplied sparse matrices with rational unit phases verify coefficients. | Verified for L>=8; no winding occurs at degree six. |
| D(T)=||T^3-8T||_F^2 >= 44N/3 | Exact moment substitution and sum of squares. Coefficients, normalization, adjacency count 2N and every square-completion term checked. | Verified for all phases/holonomies, even L>=8 (the moment identity itself does not need bipartite symmetry). |
| Thermodynamic sharpness of 44/3 | Quantize a constant face phase at the nearest 2pi m/N; product-one compatibility constructs the matrix. D/N=44/3+48(cos(phi)+1/6)^2. | Verified for the defect, not the energy. |
| Uniform positive energy improvement | Exact identity sum_top(s-r)^2+sum_bottom s^2=2r delta. Bounds |s(s^2-8)|<=M|s-r| and <=8s on [0,4], with r=sqrt(8), M=4(4+r). | Verified: E_q/N >= -1/sqrt(2)+11(3sqrt(2)-4)/1536. No sharp-energy claim. |
| Uniform-class band benchmark and twist error | Direct four-site characteristic polynomial; isolated outer band; derivative sign/divided-difference proof read; Lipschitz cell bound checked. | Verified within uniform pi/2 class, L divisible by four. |
| Edge perturbation bound at any fixed rank | Each edge difference has eigenvalues +/-|c|, hence every projection expectation has magnitude <=|c|. Sum and apply variational principle in both directions. | Verified, including ranks zero/full, with no gap assumption. |
| Optimized canonical thermodynamic limit | Open-box trial projections have zero cross-block trace. Exact rank budget includes leftover sites. Limsup <= each f_l and liminf >= inf f_l; torus/open difference <=2L. | Verified along even square side lengths; arbitrary phase patterns retained. |
| All-rank convex-envelope bracket | Decoupled eigenvalues permit arbitrary integer particle allocations. Two-support rank mixtures have rational weights. Cut exactly 2L^2/l edges; lower bound uses the convex envelope. | Verified: C_l(q_l)/l^2-2/l <= e_opt <= C_l(q_l)/l^2. |

## Detailed energy bridge and sharpness audit

Write D=2 sum_j [s_j(s_j^2-8)]^2, where the s_j are the N/2 singular values of the bipartite block. Degree four implies 0<=s_j<=4. For the upper q singular values,

`|s(s^2-8)| = s(s+sqrt(8))|s-sqrt(8)| <= 4(4+sqrt(8))|s-sqrt(8)|`.

For the others, `|s^2-8|<=8`, so their squared contributions are bounded by 64s^2, which is at most M^2s^2. Combining with the exact delta identity gives `D<=4sqrt(8) M^2 delta`. Thus the bound has the correct sign, factor of two, interval and filling dependence. Its algebraic simplification is correct. Nothing in this chain ranks energies by D; the candidate explicitly avoids that inference.

The defect sharpness construction is valid for arbitrary even L, because the necessary torus constraint is N phi=0 modulo 2pi, not L phi=0 in a particular Landau gauge. For nearest-integer quantization, |phi_L-phi_0|<=pi/N, and cosine is 1-Lipschitz, giving the independent rate

`0 <= D(T_L)/N-44/3 <= 48pi^2/N^2`.

As an additional audit deduction, equality cannot occur on any finite torus satisfying these hypotheses. The sum-of-squares zero conditions force sin(phi_p) constant and every adjacent cosine sum -1/3. Equal sine implies the two cosines in a pair are equal or opposite; opposite would sum to zero, so all cosines are -1/6 and all faces have the same phase. Compatibility would make that phase a root of unity, but its sum with its inverse is -1/3, which cannot be a rational algebraic integer. This supports the candidate's expressly thermodynamic sharpness wording.

The proven energy floor is approximately -0.70536912. The supplied uniform bulk enclosure lies strictly between approximately -0.68301270 and -0.68019413. These decimals are explanatory floating evaluations of exact displayed expressions; the report does not use them as certificates. Their separation makes the outstanding comparison visible.

## Adversarial controls and preserved failures

`receipts/independent_controls.json` contains three exact rational-phase matrix cases on L=8,8,10, independent of the candidate's Gaussian-integer multiplication. Exact controls use phases including (3+4i)/5 and its conjugate, not only quarter roots.

The following invalid generalizations are falsified, without mislabeling them as candidate errors:

- Dropping the size threshold gives tr(T^4)=640 rather than 576 for zero-flux L=4, and tr(T^6)=14544 rather than 14400 for zero-flux L=6. Both excesses are straight wrapping paths, 4N.
- Suppressing torus holonomies changes the same-face-flux L=4 quarter energy from -10 to -4-4sqrt(2); the double antiperiodic configuration reaches -8sqrt(2). Baseline L=8 exact tr(T^8) also changes by 256 under an x-cycle pi twist with unchanged faces.
- Second and fourth moments do not determine a quarter spectral sum. Exact abstract bipartite spectra with squared positive magnitudes (7,5,2+sqrt(3),2-sqrt(3)) and (8,4,2,2) have identical tr2=32 and tr4=176 but different quarter energies. These are relaxed spectral controls, not claimed lattice-realizable counterexamples.
- Equal particle allocation cannot be imposed in a lower-bound argument. An abstract trace-zero spectrum pair produces F-list quarter value -5 but convexified value -16/3 through ranks 1 and 4. This is an exact logical control for the allocation step, not a physical phase-separated competitor.

The first proposed allocation illustration gave equality, not a strict benefit. Its full receipt is preserved in `receipts/independent_controls_first_attempt.json`; the illustration was repaired before making the strict statement. No candidate failure or discrepancy was found or silently repaired.

## Full replay and remaining gap

`receipts/author_replay.json` records byte-for-byte agreement for all five frozen author check outputs, the full regenerated Hessian certificate, and the aggregate replay. It verifies 102,005 author assertions and 157 author manifest bindings. Private stdout/stderr contain the complete outputs, including the 17,042-byte Hessian JSON; their hashes and byte counts are public receipts. All 50 candidate files remain unchanged. Optional local primary-source hash checks were **not run**; the independent source-first online reading is a separate evidence channel.

The strongest verified global result here is the size-uniform energy floor combined with the exact unrestricted bulk-limit/convex-envelope framework. The exact unclosed gap is `e_opt >= e_*`, or its finite arbitrary-field analogue. The packet proves `e_opt<=e_*` by admissibility, not equality. Polynomial-defect optimization, the L=4 optimum, uniform-class loop optimization, and the L=8 local Hessian each retain their proper scope.

The defect-to-global-optimizer route is **blocked** without a new sharp inequality or independent energy comparison. Transferring the target to the defect optimizer would replace the central problem by an unsupported bridge. The current candidate does not make that transfer.

Required mathematical repairs for the reviewed global partials: none found. Severity if the packet were promoted to a solution of the original problem: critical, because the arbitrary nonuniform comparison is absent. Current proposed unsolved disposition is correct. No novelty certification or external peer review is asserted.
