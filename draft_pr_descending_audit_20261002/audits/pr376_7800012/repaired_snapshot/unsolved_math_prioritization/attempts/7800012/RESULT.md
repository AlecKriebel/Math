# Final result: quarter-filled optimal flux remains unresolved after five turns

**Proposed disposition: unsolved, 5/5 substantive turns, pending full independent review.** The packet gives several complete scoped results and exact certificates, but no global proof that uniform pi/2 flux minimizes the quarter-filled energy on arbitrary large square tori or in the thermodynamic limit.

## Exact source and normalization

The original1998 question by Elliott H. Lieb minimizes the sum of the lowest N/4 eigenvalues of the unit-modulus nearest-neighbor Hermitian hopping matrix on a periodic square lattice. It allows arbitrary edge phases and nonuniform plaquette fluxes. The quoted half-filled theorem is not a quarter-filled theorem. The full original HTML includes its technical TeX statement: https://web.math.princeton.edu/~aizenman/OpenProblems_MathPhys/9802.OptFlux.html

The source uses the word 'large' but specifies a finite objective rather than an explicit limiting assertion. This packet states finite and thermodynamic results separately. For finite square tori it uses even side L>=4, and retains both noncontractible loop holonomies in addition to compatible plaquette fluxes. Omitting the loop data is incorrect in finite volume, as the standard all-circuit gauge lemma of Lieb–Loss1992 makes clear.

## Proven scoped results

1. **TURN_1.md:** Complete torus gauge coordinates; exact projection variational formulation; universal energy lower bound; global4 by4 optimum−8sqrt2, attained by uniform pi/2 and also by a zero-plaquette-flux configuration with both loop phases−1. Saturation of that elementary bound is impossible for even L>=8.
2. **TURN_2.md:** Exact fourth/sixth closed-walk moment identities and a sum-of-squares proof that ||T³−8T||²_F>=44N/3 for L>=8. The defect constant is thermodynamically sharp. It yields a uniform positive improvement of the elementary quarter-filled energy bound. Optimizing this polynomial defect is explicitly not identified with optimizing the energy.
3. **TURN_3.md:** Full uniform-pi/2 band formula and complete optimization of both loop twists for every L=4n: periodic twists for odd n, antiperiodic twists for even n. The proof uses alternating derivative signs and a Chebyshev divided-difference argument. It includes an exact8 by8 uniform-class benchmark, the thermodynamic band integral, an analytic enclosure and a uniform finite-size error bound.
4. **TURN_4.md:** Exact computer-assisted proof that the holonomy-optimized uniform-pi/2 state on8 by8 is a strict local minimum modulo gauge against every phase perturbation. The128-dimensional Hessian has63 gauge zero directions and65 positive physical directions, certified by all64 Fourier blocks and integer-verified radical bounds. No global or other-size minimum follows.
5. **TURN_5.md:** Existence of the unrestricted canonical quarter-filled thermodynamic optimum, boundary perturbation bounds, and a two-sided finite-box comparison using the lower convex envelope over all particle counts. Phase separation and unequal block occupations are retained. This supplies a rigorous framework for future lower certificates or competitors, without producing the missing comparison.

The remaining target is a global comparison with arbitrary nonuniform fields. The exact uniform benchmark, finite global/local results and universal bounds do not close that gap. No source counterexample is claimed.

## Credit and verification boundary

Gauge equivalence by all circuit fluxes, the spectral variational principle, magnetic Harper fibers, closed-walk moments and spectral perturbation theory are standard ingredients. Lieb1994 proves the half-filled theorem; Lieb–Loss1992 supplies the general circuit-flux lemma and explains the uniform-field historical conjecture. This packet derives its stated formulas and supplies its finite certificates, without a historical novelty claim or recertification of every theorem in those papers.

All public checkers use Python3.10+ standard library only. Run `python REPLAY_ALL.py` from any directory. It reproduces every frozen checker output and verifies historical/final manifest bindings. Optional `--sources PATH` validates the complete original HTML and two primary PDFs, which are excluded from the public packet.

The author controls total102,005 assertions, including the complete exact8 by8 Hessian certificate. Finite checks do not establish a large-volume optimum; each all-size statement has a written proof. Every turn remains frozen, with the earlier state snapshots retained as history. Author search stops after turn5, pending independent review.
