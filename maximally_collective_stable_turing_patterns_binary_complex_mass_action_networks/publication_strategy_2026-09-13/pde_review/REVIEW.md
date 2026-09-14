# Independent nonlinear/PDE publication review

Checkpoint: 2026-09-14 00:41 UTC (2026-09-13 local project date). Completion estimate: 100% of this bounded publication-readiness review; this is not a claim that the paper is formally verified or that all its open problems are solved.

## Verdict

I found no publication-blocking defect in the current nonlinear/PDE argument. The manuscript already supplies substantially more than an unstable linear example: an exact all-dimensional primary crossing, a negative cubic coefficient with the correct conservation gauge, and local exponential stability in a clearly specified phase space. The best next step is focused outside mathematical scrutiny of the present result, followed by journal submission; full Lean formalization and improved constants are not prerequisites.

This verdict comes from reading the current main manuscript sections 6–8 and Supplement S5–S10 before consulting any historical audit verdict. I also read the reaction construction, complete-realization statement, and limitations to check the PDE claims against their actual scope.

## Mechanism and checkable proof chain

1. The selected rational diffusion profile makes `(A-D)r=0` for the first Neumann cosine mode on `(0,pi)`. The homogeneous conservation zero is removed by fixing the spatial integral of `c^T x`. It is not permissible to delete the conservation direction pointwise; the manuscript instead applies it only to the zero Fourier mode, correctly.
2. Homogeneous spectral stability is proved by an all-dimensional modulus comparison; a separate spatial comparison excludes all other closed-right-half-plane roots for damping `t>=1`. Algebraic simplicity is explicitly established by differentiating the characteristic determinant, not inferred merely from isolation of zero. See main.tex lines 687–727 and Supplement S5.
3. The quadratic field and `cos^2=(1+cos(2 xi))/2` give the forcing `-B(r,r)/4` for both the zero and second harmonics. The zero-harmonic inverse is taken with `c^T w0=0`. The cubic projection `ell^T[B(r,w0)+B(r,w2)/2]/(ell^T r)` has the correct Fourier factors. Main.tex lines 739–753; Supplement S6.
4. Reflection about the interval midpoint makes the amplitude vector field odd and exchanges the two branches. The negative cubic and positive crossing coefficient produce the stable eigenvalue `-2 eta mu+O(mu^2)` on the branch. These are two reflected positive-concentration patterns, not positive and negative physical concentrations.
5. The main text explicitly proves the Fredholm range and high-mode inverse bound, establishes a complementary spectral gap, and supplies the semilinear setting needed to upgrade spectral stability to local exponential stability in H1. In one spatial dimension H1 controls the quadratic reaction term; the fixed-mass condition removes the homogeneous neutral direction and Neumann conditions remove continuous translation symmetry. Main.tex lines 755–830; Supplement S10.
6. Equilibrium scaling does not preserve dynamic eigenvalues by similarity to the unit design. The manuscript correctly derives the row-scaled normalized operator `H(A-t Delta)` and proves a new homogeneous modulus bound. It transforms the left critical vector and physical conservation gauge, and adjusts the zero-mode correction along the kernel. This is the key subtlety in the scaled-family theorem, and it is explicitly handled. Main.tex lines 912–1058; Supplement S7.
7. Robustness is a local, retuned codimension-one result at each fixed dimension. Flux/equilibrium perturbations remain on the realization manifold; a scalar diffusion multiplier is retuned by transversality. The paper does not claim every nearby parameter point is itself critical. Main.tex lines 1124–1145.

## Independent falsification checks

`independent_check.py` was created for this review and imports none of the existing project's verification code. It rebuilds the vector field directly from the listed reactions, differentiates it, and uses exact rational arithmetic to check:

- equilibrium, conservation, critical right and left eigenvectors;
- the mass-compatible zero-mode solve and second-harmonic solve;
- positive crossing coefficient and negative cubic coefficient for m=3,4,5,8,12 at the unit equilibrium and at rational scaled-family parameters L=4/5 and 9/10 (15 cases, all in the certified interval);
- supplementary numerical noncritical eigenvalue checks for k=0,1,2,3,10 (75 matrix blocks), after removing the single zero for k=0 and k=1.

All passed. Exact coefficient values and numerical spectral values are saved in `independent_check_results.json`. This finite-dimensional evidence is a falsification probe, not an all-dimensional proof and not a rigorous interval proof of the numerical eigenvalues.

I also replayed the repository's `independent_verifier/verify_symbolic_certificates.py`; it exited successfully with `ALL_SYMBOLIC_CERTIFICATES_PASS`. Its checks included mode isolation, harmonic corrections, cubic signs, the determinant identities, scaled-family certificate, cubic bound, and exposition identities. This replay has lower independence than the new reconstruction and is reported separately.

## Limits that matter for impact and presentation

- Stable patterns are local near onset, for each fixed dimension and fixed interval, within a fixed integrated-mass class. There is no global attracting-pattern theorem, arbitrary-data boundedness result, or dimension-uniform basin estimate. The semipositive invariant leaves X1 unbounded; the manuscript explicitly recognizes this, and it does not invalidate the local theorem.
- The family is a synthetic extremal mass-action construction. It demonstrates a structural limitation on reduction to small principal subsystems, not a demonstrated biological mechanism.
- The stationary diffusion threshold and exponent-optimality are topology-specific. They do not assert optimality over all binary-complex networks or classify arbitrary wave instabilities.
- The square-root result is exponent-optimal, not constant-optimal. Asymptotically at the certified endpoint, diffusion contrast is about `37.14 sqrt(m-2)` and equilibrium contrast about `0.8944 sqrt(m-2)`. The necessary minimax bound is about `2.828 sqrt(m-2)`. Thus the certified maximum is about 13.1 times the necessary lower bound. The endpoint is a boundary of the present sufficient certificate; it is not proved to be a dynamical boundary. These are worthwhile follow-up questions, not missing requirements for this paper's stated theorem.
- The product of the two contrasts is preserved along the scaled family. It reallocates heterogeneity; it does not eliminate the cost or attain a globally balanced optimum.

## Lean recommendation

Do not make full Lean formalization the next publication milestone. The main credibility-sensitive PDE steps are the translation from exact matrix algebra to center-manifold existence, parameter dependence, spectral perturbation, and nonlinear stability. Formalizing only rational signs would not formally establish those steps, while end-to-end formalization would be a separate substantial project. Conventional expert checking of this detailed proof and reproduction of the exact certificates are the more direct next investments.

A small optional formalization could add value as a reproducibility artifact: verify the general principal-minor expansion/diffusion-ray lemma and selected polynomial positivity certificates, with a precise statement of what remains assumed. It should not be presented as formal verification of the full stable-pattern theorem. The paper's research value must rest on its mathematical contribution, not the author's amateur/professional status or the presence of a proof assistant badge.

## Specific next outside scrutiny (research notes only)

The most useful independent reader would know both semilinear reaction–diffusion bifurcation and mass-action/CRNT structure. The concrete questions are whether the conservation-compatible reduction and scaled-family spectrum meet that reader's standards, whether the topology-wide quantifier is sufficiently distinguished from earlier subsystem-localization results, and whether the current theorem suite merits a dynamical-systems journal. No outreach was drafted or sent. The human user alone may initiate any external communication.

Public comments need not arrive before submission. Resolve any concrete objections that do arrive, reconcile all public release/version links with the intended submitted manuscript, and then submit the current result rather than waiting indefinitely for endorsements, public attention, complete formalization, or a sharp nonlinear constant.
