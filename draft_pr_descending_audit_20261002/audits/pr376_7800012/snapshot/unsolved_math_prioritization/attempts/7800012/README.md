# Problem 7800012: quarter-filled optimal-flux partials

**Reviewed disposition: unsolved, 5/5. Full independent scoped source/proof audit: PASS.**

Lieb's original question asks whether uniform pi/2 plaquette flux minimizes the lowest-quarter eigenvalue sum for arbitrary unit-modulus edge phases on a large periodic square lattice. This packet retains arbitrary nonuniform flux patterns and both torus loop holonomies. It does not prove that unrestricted global optimum.

- [Final result and exact limitations](RESULT.md)
- [Original-source normalization](SOURCE_NORMALIZATION.md)
- [Full independent review](final_review/REVIEW.md)
- [Original Lieb question](https://web.math.princeton.edu/~aizenman/OpenProblems_MathPhys/9802.OptFlux.html)

## Scoped results

1. [Turn1](TURN_1.md): full gauge coordinates, projection variational formula and the global4×4 optimum, including a zero-plaquette-flux tie with double antiperiodic holonomy.
2. [Turn2](TURN_2.md): all-even-L>=8 moment identities, a sharp polynomial-defect bound and a uniform improvement of a basic energy bound. The defect optimizer is not claimed to optimize energy.
3. [Turn3](TURN_3.md): exact uniform-pi/2 bands and complete loop-twist optimization for L divisible by4, plus the bulk integral and certified finite-size bounds. This optimization is within the uniform-flux class.
4. [Turn4](TURN_4.md): an exact8×8 strict local minimum modulo gauge against all128 phase directions. The certificate establishes63 gauge zeros and65 positive physical directions; it does not prove a global minimum or cover other sizes.
5. [Turn5](TURN_5.md): existence of the unrestricted canonical bulk optimum and all-rank convexified finite-box bounds. Unequal particle allocations and phase separation are retained, and the comparison with the uniform bulk benchmark remains open.

Classical gauge, variational, Harper, moment and perturbation ingredients are credited. No historical novelty claim is made. All41 frozen author files and the five manifest-bound review files remain byte-identical. Earlier pending-review wording is preserved as history; this wrapper records the completed scoped PASS.

## Reproduction

Author replay uses Python3.10+ standard library only:

    python REPLAY_ALL.py

It regenerates all102,005 assertions, the full exact Hessian/Fourier certificate and157 author manifest bindings. Source inputs are deliberately excluded. Optional `python REPLAY_ALL.py --sources PATH` verifies the original HTML and two primary PDFs when independently supplied; a source-free checkout must not report those three checks as having run.

Independent replay additionally requires **SymPy**:

    python verify_review.py

The additive portable wrapper verifies the frozen author/review hashes and reproduces984 independent controls. The audit includes the written proofs and the complete Hessian construction. It is AI-assisted, not external peer review. Finite tests alone do not establish the large-lattice or bulk optimum.
