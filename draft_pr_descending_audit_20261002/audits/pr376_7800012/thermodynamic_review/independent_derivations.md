# Independent thermodynamic derivation (sealed before candidate read)

## Claim, model, normalization

The literal problem is a finite square torus with M sites, M divisible by 4, unit-modulus nearest-neighbor hopping A=A*, and objective S_n(A)=sum of its n=M/4 smallest eigenvalues. This is a one-spin sum. The two-spin convention has twice this energy when each of these orbitals is doubly occupied; multiplication by two changes no comparison. On an even-sided torus the bipartite unitary conjugates A to -A. The norm is at most 4 by maximum absolute row sum. A Laplacian convention subtracting 4I shifts both fixed-density energies by -4n, and cannot be silently mixed with the adjacency convention.

The finite question and a bulk question must be separated. A negative finite example disproves universal finite optimality for that size and holonomy comparison. It does not by itself establish a nonvanishing thermodynamic improvement. The bulk quarter-density question asks whether a competing sequence with n/M=1/4 has limsup energy/site strictly below the limiting uniform-pi/2 energy. A stronger all-sufficiently-large conclusion needs explicit boundary remainders and allowed sizes.

## Canonical sums and chemical potentials

For every Hermitian A and integer n, S_n(A)=min_{P=P*=P^2, rank P=n} Tr(PA). Equivalently,

S_n(A)=sup_mu {Tr(A-mu I)_- + mu n},

where Tr(B)_- sums negative eigenvalues of B. The maximizing interval is [lambda_n,lambda_{n+1}]. A noninteger density must be represented by fractional filling at the Fermi level, or a declared integer rounding. A grand-canonical energy comparison at one chemical potential is not a canonical comparison at density 1/4. A trial projector with exactly n particles gives a valid canonical upper bound even if it is not the ground-state projector.

For ||A||<=4, |S_n(A)-S_m(A)|<=4|n-m|. Thus integer-density repairs cost at most 4 per moved particle. A mismatch proportional to volume does not disappear in the limit.

## Bond, rank, and boundary estimates

Let A,B have the same diagonal. Delta=A-B is traceless. For every orthogonal projector P, |Tr(P Delta)|<=||Delta||_1/2, because the total positive and negative spectral traces of Delta are equal. Applying the variational formula in both directions gives

|S_n(A)-S_n(B)|<=||Delta||_1/2.

Changing one unoriented bond amplitude by z produces a rank-two Hermitian matrix with eigenvalues +/-|z|, hence trace norm 2|z|. Consequently deleting m unit bonds costs at most m in a canonical sum; changing phases on m bonds costs at most 2m. These constants apply at every n, including shell degeneracy, and require no Fermi gap. A coarser rank estimate is |S_n(A)-S_n(B)|<=rank(Delta)||Delta||/2; if both hopping operators have norm<=4 this is <=4 rank(Delta). Rank alone needs the norm bound.

Opening an Lx by Ly torus deletes Lx+Ly wrap bonds (for side lengths at least 3), so |S_n(open)-S_n(torus)|/M <=1/Lx+1/Ly. Two choices of winding phases are gauge-related away from seams; their per-site canonical energies differ by at most 2/Lx+2/Ly. Thus holonomy disappears only when both dimensions tend to infinity; a fixed-width cylinder is a different thermodynamic problem. Altering all magnetic phases in an extensive region has no boundary-only bound.

## Uniform pi/2 bulk normalization

Take vertical amplitudes exp(i*pi*x/2), horizontal amplitudes 1, and magnetic period q=4. Fourier transform gives a 4 by 4 fiber h(kx,ky), kx in a reduced interval of length 2pi/4 and ky in an interval of length 2pi. Its characteristic polynomial is

E^4-8E^2+4-2cos(4kx)-2cos(4ky).

Its lowest band is

b_-(kx,ky)=-sqrt(4+sqrt(12+2cos(4kx)+2cos(4ky))).

This band is separated from the next: b_- <=-sqrt(4+2sqrt(2)), whereas the next band is >=-sqrt(4-2sqrt(2)). Every fiber contributes four eigenvalues and the first band contains M/4 states. Therefore at exact quarter filling

e_pi/2=(1/4) average_{magnetic BZ} b_- = -(1/4) average_{u,v in [0,2pi]} sqrt(4+sqrt(12+2cos u+2cos v)).

The factor 1/4 cannot be omitted, and no particle-density optimization is needed for this fully occupied isolated band. The fiber polynomial above can be directly checked rather than assumed from historical Hofstadter plots. Finite holonomies shift grid points but not the bulk integral. q=4 Landau gauge is periodic when Lx is a multiple of 4; a general torus realization additionally obeys total plaquette flux=0 mod 2pi, so M must be divisible by 4.

## Density mixtures and phase separation

For two extensive regions of fractions a and 1-a and respective local densities rho1,rho2, quarter filling requires a*rho1+(1-a)*rho2=1/4. Decoupled canonical energy is obtained by minimizing over all allocations satisfying total n, not automatically by equal quarter filling in each region. An explicitly allocated trial state provides an upper bound a*e1(rho1)+(1-a)*e2(rho2). Joining regions along subextensive boundaries has o(M) cost, but all physical bonds must be restored with unit modulus. Merely deleting bonds in the final model is inadmissible. Equal chemical potentials characterize an optimum under free allocation but are not needed for a valid exactly counted trial allocation. A density-mixture calculation proves the arbitrary-flux conjecture false only if it respects total particle number; it addresses a stronger admissible class than uniform flux.

## Tiling and quantifiers

If a fixed L by L torus has a trial projector at rank L^2/4 with canonical energy E_cell, open it (cost at most 2L), tile copies, and restore seams (at most 2M/L bonds). The resulting large-torus trial bound per site is at most E_cell/L^2+4/L, up to leftover boundary and rounding terms for incompatible sizes. A finite-cell deficit delta survives this simple construction only if delta>4/L. A finite numerical strict deficit of any size does not automatically extend to bulk. Sharper constructions may avoid one or both opening/restoring costs, but require the corresponding explicit trial state or period-fiber proof.

For a sequence of expanding cells with deficit delta_L, proving liminf delta_L>0 suffices after O(1/L) boundary errors. If the deficit tends to zero or is less than unbounded numerical/error constants, no thermodynamic disproof follows. A proof stated only along L multiples of 4 establishes that subsequence; arbitrary large compatible rectangles need leftover estimates. For genuine bulk existence of a fixed periodic pattern, direct Riemann sums or boundary comparison give convergence for all sequences whose two side lengths tend to infinity.

## Analytic falsifiers and negative controls

1. M/4 eigenvalues must be counted exactly, including degenerate boundary shells; partial-shell sums require explicit integer rank or fractional occupations.
2. Compare candidate and uniform flux on the same lattice/volume and total density; if holonomies differ, bound their possible influence and state finite versus bulk scope.
3. Check the q=4 polynomial and first-band normalization against a direct real-space torus on small compatible sizes; q-fiber counts must total M.
4. Test a changed/deleted bond at empty/full filling and at a shell crossing. Full filling has S_M=Tr A=0, and empty filling S_0=0.
5. Test a fake competitor with a single seam perturbation: it can show a finite difference but has no bulk deficit, since the proven bound is O(1/min(Lx,Ly)).
6. A mixture with mismatched total density is rejected even if its energy is lower; integer correction is explicit.
7. Every purported fixed-cell tiling theorem must display an interface bond count and show its remainder is below the established deficit.
8. Half-filled reflection positivity or determinant maximality cannot be promoted to a quarter-filled spectral-sum theorem: their functionals and density hypotheses differ.

These are exact deductions from the stated unit-hopping finite model. The historical conjecture, any extrapolation from plots, and any numerical precision assertion remain hypotheses until a proof or certified computation establishes them.
