# Independent adversarial review

Checkpoint: 2026-09-12 03:59 UTC (2026-09-11 local). This bounded adversarial review is 100% complete; that percentage concerns the review assignment, not completion of every manuscript formalization obligation. No production source was edited and no external individual was contacted.

## Verdict

I attempted to falsify the emerging distinction between an unconditional, correctly modeled main equality theorem and incomplete coverage of all mathematical assertions in the manuscript. The distinction survives this review. I found no additional fatal mathematical assumption or source-shadowing defect in the equality chain. The manuscript's unqualified scalar-positivity characterization of the strict residual domain is false, but the formal main proof does not use that characterization.

Compilation status of the new independent reproduction is left to its actual final receipts. I independently inspected source and compiler/dependency provenance; I did not perform a second simultaneous full build or treat historical receipts as a new build.

## Attempts to falsify the equality endpoint

`Bell/Quantum.lean:19–86` defines actual complex 2-by-2 local matrices, a positive semidefinite trace-one 4-by-4 bipartite density matrix, positive normalized POVMs, mutually orthogonal idempotent PVM effects, the tensor-product Born rule, and ordinary real convex hulls of complete strategy images. It does not define one hull in terms of the other. The architecture has independent input-dependent finite output counts. Taking the real part in `born` is consistent with the separately proved positivity and normalization contracts; it is not a scalar stand-in for a quantum model.

`Bell/Assembly.lean:76–96` proves the two-input equality and universal architecture formulation without a residual-reduction, stationarity, local-realizability, multiplier-sign, or equality premise. The argument selects an extreme maximizing behavior using `counterexample_has_extreme_maximum` (`QuantumCompactness.lean:215`), whose source derives the separation, compact maximizing face, extreme point, and actual raw strategy realization.

The apparently strong purification claim `full_pure_of_not_mem_convexPVM` (`SteeringRepresentation.lean:105`) does not assume extremality. I checked its mechanism because this looked like a possible hidden failure: the mixed state defines an assemblage on Alice's qubit, a singular reduced state is already in the PVM hull, and an invertible reduced state admits the explicit two-qubit purification with transformed Bob POVMs. Thus changing the shared state is essential and permitted; the theorem is not claiming that every mixed density matrix is pure or that simulation preserves a fixed state.

The residual endpoint `no_strict_residual_maximum` (`ResidualClosure.lean:54–105`) requires a concrete invertible frame `E`, `frameGram E = metric g.a g.b g.c g.d`, positive frames, and feasible incidence. It derives the local maximum, stationarity, and positive multipliers. The physical caller constructs those frame hypotheses from complex-qubit effects in `physicalResidualFrames` (`ResidualStrategy.lean:104`) and the declared `ResidualFrames` fields (`ResidualCoordinates.lean:65`). The formalization therefore retains the physical content that the paper's scalar equivalence accidentally loses.

## Independently confirmed manuscript counterexample

At `paper/main.tex:1036–1049`, the strict residual definition states that signature (1,3), normalization, and five distinct rays in a common future cone are equivalent to positivity of all distinct-ray products. Taken as an unqualified implication from the latter scalar conditions, this is false.

Set

\[
a=d=6/25,\qquad b=c=3/100,\qquad e=a+b+c+d-1/2=1/25.
\]

All four sums bounded by 1/2 are 27/100. The ten distinct-ray products are positive: the six products among the first four rays are 1/2, 6/25, 3/100, 3/100, 6/25, 1/25, and the four products involving the fifth ray are all 23/100. The five rays are null, and `uᵀgu=1`.

Nevertheless, the invariant subspaces `(x,x,y,y)` and `(x,-x,y,-y)` have matrix representations

\[
G_+=\begin{pmatrix}1/2&27/100\\27/100&1/25\end{pmatrix},\qquad
G_-=\begin{pmatrix}-1/2&21/100\\21/100&-1/25\end{pmatrix}.
\]

Their determinants are respectively `-529/10000` and `-241/10000`. Each symmetric block has one positive and one negative eigenvalue, so the full metric has signature **(2,2)** and determinant `127489/100000000 > 0`. This is an exact rational argument, independent of numerical eigenvalue calculations. The separate referee computation/Lean counterexample preserves further checkable evidence.

This falsifies the paper's scalar characterization, not the main equality. In particular, `Bell/Lorentz.lean:17` explicitly warns that `StrictParameters` does not imply Lorentz signature, and the physical closure proof supplies a real Lorentz Gram representation separately. A repair to the manuscript is to retain signature (1,3) as a standing premise when describing the equivalence with common future orientation.

## Coverage distinction survives adversarial checking

The paper asserts a smooth 14-dimensional incidence manifold (`main.tex:1205–1225`), finite POVM duality (`1260`), and the complete weighted Hessian/inertia formula (`1466–1495`). The production proof can certify the equality without certifying those precise assertions: `ImplicitCurve.lean:19–42` constructs a once-differentiable feasible curve from a surjective strict derivative, and `:52–100` uses an exact quadratic gap and first derivative. `DeterministicGap.lean:92–107` forces positive multipliers directly from deterministic replacement gaps, with no semidefinite duality premise. These are valid alternative mechanisms; their success is not evidence that the omitted smooth-manifold, full inertia, and general duality statements have been formalized.

Likewise, the paper uses Hilbert spaces of dimension at most two and includes stochastic output postprocessing (`main.tex:252–280`); the formal core uses a fixed two-dimensional carrier. The existing `CERTIFICATION.md` and `docs/CERTIFIED_COVERAGE.md:27` already acknowledge that generic smaller-dimension embedding and stochastic-channel closure are not named formal endpoints. The standard mathematical bridges are sound: embed the state in the qubit subspace and complete each measurement on the unused orthogonal complement; expand each finite stochastic channel into deterministic maps and combine all choices into the complete-strategy random index. This preserves the hull meaning, but the distinction between an informal bridge and a kernel-checked generic bridge must remain explicit.

## Independent provenance and trust check

Machine-readable evidence is in `../evidence/adversarial_provenance.json`.

- Resolved executable: `/Users/alec/.elan/toolchains/leanprover--lean4---v4.19.0/bin/lean`.
- Executable SHA-256: `5c1fe58db7d10b1cd0ddff1a1cbc49db2396fff9c6c983cc3b49f1c5c1ae241b` (49,968 bytes).
- Reported compiler: Lean 4.19.0, arm64 release, full commit `6caaee842e9495688c1567e78c0e68dbb96942aa`, agreeing with the pin.
- Inherited `LEAN_PATH`, `LEAN_SRC_PATH`, `LEAN_SYSROOT`, and `ELAN_TOOLCHAIN` were all unset. `lake env` generated only the expected dependency source/build paths, project build path, and pinned toolchain paths.
- All nine dependencies matched their manifest revisions and had clean tracked diffs, including Mathlib at `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
- Searching all untracked `.lean` files, including ignored files, found none outside the dependency `.lake` directories. Searching dependency Lean build roots for `Bell*` namespace entries found none. Thus I found no source or namespace-shadowing escape in the active dependencies.

The runner checks pinned identities, positive/negative compiler controls, a fresh local project build, statement contracts, public transitive axiom reports, and unchanged protected source. Its lexical scan excludes admitted proofs and source-level kernel bypasses. I found no extra loophole in the examined current inputs. The executable fingerprint is identification evidence, not independent proof that the binary or its linked runtime is correct. Cached dependency `.olean` files are not all rebuilt or hashed here; their producer and the compiler/runtime remain the expressly documented ordinary trust boundary. The receipt field `all_imported_source_kernel_checked` should be read in the documented project-source scope, not as a claim of rebuilding every transitive Mathlib source from scratch.

Strongest conclusion: subject to the fresh build's successful final receipt, the formal equality endpoint is correctly modeled and unconditional under Lean's standard logical axioms and documented implementation trust. The stronger claim that the development proves all mathematical assertions in the primary paper is not supported, and the counterexample makes that distinction substantive.
