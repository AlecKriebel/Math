# Sealed independent baseline — global bounds family

Prepared 2026-10-03 05:42 UTC, before reading any candidate, prior audit, root or sibling verdict. Completion estimate: 20% of this audit; 0% claimed progress toward resolving the original optimal-flux problem.

## Sources read first

- Elliott H. Lieb, original 1998 problem: <https://web.math.princeton.edu/~aizenman/OpenProblems_MathPhys/9802.OptFlux.html>.
- E. H. Lieb, *The Flux Phase of the Half-Filled Band* (1994), especially definition, reflection positivity lemma/theorem and filling discussion: <https://arxiv.org/pdf/cond-mat/9410025>.
- E. H. Lieb and M. Loss, *Fluxes, Laplacians and Kasteleyn's Theorem* (1992 preprint), especially Sections I-II and Lemma 2.1: <https://arxiv.org/pdf/cond-mat/9209031>.

Paraphrases and deductions below are original; no primary-source text is copied into this artifact.

## Exact target and boundaries

Let T be the Hermitian unit-modulus nearest-neighbour hopping matrix on a large periodic square lattice with N sites, 4|N. The target is to minimize E_{N/4}(T), the sum of its N/4 lowest eigenvalues, over all edge phases. The proposed flux is pi/2 on each elementary square, with the complex-conjugate -pi/2 configuration having identical energy. This is a hypothesis; uniform-flux competition alone is weaker than optimization over arbitrary phase configurations.

A concrete finite torus C_Lx x C_Ly has four distinct neighbours only when both side lengths exceed 2. It is bipartite exactly when both side lengths are even. Divisibility 4|N does not imply bipartiteness: C_3 x C_4 is a boundary control. Finite-versus-thermodynamic targets must be kept distinct. Tiny dimensions create extra short wrapping paths. I will demand explicit size thresholds in moment identities.

Gauge equivalence on a graph requires agreement of fluxes around all cycles, not only faces. On a torus, elementary plaquettes satisfy product_p exp(i Phi_p)=1, and two additional independent cycle holonomies survive gauge transformations. In particular constant pi/2 faces require N divisible by 4. Different torus holonomies can have different finite spectra and finite energies even with identical face fluxes. The original problem's informal face-only spectral statement must be corrected on a finite torus rather than used as a lemma.

The 1994 reflection-positivity argument maximizes a grand-canonical partition function at the symmetry point and yields half filling; fixed quarter filling is not an automatic corollary. Particle-hole symmetry pairs one-particle eigenvalues on an even torus, but the quarter energy involves only the largest N/4 positive magnitudes, whereas the half energy involves all positive magnitudes. Determinant maximization, moment minimization, and quarter-energy minimization are separate objectives.

## Independent exact deductions

1. Degree four gives ||T|| <= 4 and tr(T^2)=4N, regardless of phases. This follows directly from the row sum bound and summing |T_xy|^2. Trace T=0.

2. On an even-by-even torus, let the positive magnitudes (including zeros) be s_1 >= ... >= s_{N/2} >= 0. Then sum s_j^2=2N. Cauchy-Schwarz gives E_{N/4}(T)=-sum_{j<=N/4}s_j >= -N/sqrt(2). Equality requires s_1=...=s_{N/4}=sqrt(8) and s_{N/4+1}=...=s_{N/2}=0. This is a global valid bound, but a proof of quarter-flux optimality requires a quarter-flux matrix to achieve it, or a stronger calibrated bound. Without bipartiteness, trace zero plus tr(T^2)=4N gives only E_{N/4} >= -(sqrt(3)/2)N by splitting the eigenvalue list into groups of sizes N/4 and 3N/4 and applying Cauchy-Schwarz to each.

3. For Lx,Ly >= 5, tr(T^4)=28N+8 sum_p cos(Phi_p). There are 28 phase-cancelling returning walks of length 4 per site, and each square contributes eight oriented/rooted walks. Zero flux has 36N, pi flux 20N, and uniform pi/2 flux 28N. If a dimension is 4, wrapping straight loops add 8 sum_rows cos(H_row) for that dimension. Thus a trace formula without size/holonomy qualifications can fail on a 4-by-4 torus.

4. Local fourth moment alone favors pi rather than pi/2; interpreting its minimizer as the quarter-energy minimizer is invalid. Nor do second and fourth moments determine quarter energy. As an abstract bipartite-spectrum control (not asserted to be lattice realizable), the two 8-point spectra with squared positive magnitudes A=(7,5,2+sqrt(3),2-sqrt(3)) and B=(8,4,2,2) have the same tr(T^2)=32 and tr(T^4)=176 but quarter energies -(sqrt(7)+sqrt(5)) and -(sqrt(8)+2), respectively, which differ. Exact inequality follows from (sqrt(7)+sqrt(5))^2=12+2sqrt(35)>12+8sqrt(2)=(sqrt(8)+2)^2 because 35>32.

5. For C_4 x C_4 with zero face flux, the untwisted spectrum is 4, 2 (four times), 0 (six times), -2 (four times), -4, giving quarter energy -10. With x-cycle holonomy pi and y holonomy zero, Fourier diagonalization gives quarter energy -4-4sqrt(2), which differs. This is an exact face-only-spectrum counterexample within a regular degree-four torus, though tiny and not a disproof of the large-lattice conjecture.

6. For a 4-by-4 pi/2 Landau-gauge torus with both magnetic cell holonomies zero, the characteristic relation is lambda^4-8lambda^2=0. Its spectrum consists of +sqrt(8) (four), -sqrt(8) (four), and 0 (eight). Hence E_4=-8sqrt(2) achieves the bound of item 2. This finite special case is unusually degenerate; it does not certify all larger tori. Its tr(T^4)=32N also displays precisely the wrapping correction missing from the local formula.

7. For arbitrary Hermitian T, fixed filling has the exact variational identity E_m(T)=max_mu [m mu - tr((mu I-T)_+)]. If a scalar polynomial P majorizes x -> (mu-x)_+ on [-4,4], then E_m(T) >= m mu - tr P(T). A valid polynomial surrogate is only a lower bound until equality or a sufficiently sharp comparison is proved. A polynomial calibrated at finitely many spectral values must still majorize on the full interval, and strict slack at the proposed optimizer prevents saturation. A Taylor expansion/local Hessian or sampled flux grid cannot substitute for the required universal majorization or global energy comparison.

## Adversarial checks fixed before exposure

- Replay exact moments at L=4,6,8 with phases in {1,i,-1,-i}; toggle holonomies without changing plaquette flux.
- Inspect every global inequality for the actual interval, filling, bipartite, finite-size, and equality conditions used.
- Test a proposed energy certificate against an exactly solvable 4-by-4 magnetic torus and against abstract moment-preserving spectral mutants, carefully distinguishing realizable and relaxed controls.
- Reproduce full executable output, preserving numerical discrepancies as discrepancies rather than repairing the candidate silently.
- Mark a route blocked when polynomial/moment optimization is transferred to an unsupported bridge to the original quarter-energy functional.

The independent baseline is to be hashed before candidate access. Any later findings and revisions will be separate files.
