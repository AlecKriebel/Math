# PR #1031 independent adversarial geometry review

**Reviewed head:** `f6570e093267a7f910faf9cdd60dfbc1c12f5681`.

**Verdict:** the geometric bridge is proved under the submitted definitions.
No geometric defect or counterexample was found. This verdict does not by
itself accept the full negative existential theorem, the external Fawzi
obstruction, the moment/SOS consequence, or any priority claim.

The strongest independently verified result is

    C(4,12) intersect {Phi=1, Q=0} = A(K_0)
                                      isomorphic over R to complex Sep(3,3).

Here A is an explicitly defined rational real-linear injection from the
225-dimensional Hermitian space of exterior^2_C C^6 into the 495-dimensional
real exterior space. K_0 is the positive convex hull of the projectors of unit
simple mixed bivectors. The section and inverse are affine/real-linear, so a
finite semidefinite lift of C(4,12) would give one of complex Sep(3,3).

## Independence and scope

The submitted proof was read as a hypothesis. Before independently deriving
the bridge or constructing the checker, no acceptance file, historical audit,
priority report, submitted checker/certificate, or other family's conclusion
was read. The all-file integrity check hashes bytes without interpreting
their contents. All 29 submitted input pins match. After the reconstruction
and initial exact run succeeded, the submitted checker was reviewed and
executed in its ordinary read-only mode, and the two coordinate certificates
were compared. No proposed source edit, git/index operation, publication,
communication with an individual, or outreach was performed.

The argument here needs only elementary skew-adjoint operator theory,
orthogonal decomposition, exterior algebra, positive convex combinations,
and basis extension. The named Wirtinger result is proved directly rather
than accepted from an external citation. No third-party source body was
fetched. The separable-state obstruction is a separate external obligation.

## Findings by attack family

| Attack | Independent finding | Checkable evidence |
|---|---|---|
| Wrong Kähler maximum or equality orientation | The compression of J has two skew singular values at most 1. Product +1 forces both equal 1, so the plane is J-invariant; exactly the complex orientation gives +1. | Universal operator argument in `INDEPENDENT_DERIVATION.md`; positive, reversed, partially complex, totally real, and near-face exact controls. |
| Nonmaximal generators hidden inside a convex face | Every finite positive combination attaining the maximum has only maximal positive-weight summands. The generator set and its hull are compact. | Convexity proof; no numerical inference. |
| Complexification sign or omitted normalization | uj=(ej-i fj)/sqrt(2) has eigenvalue +i. The map has factor 1/4 in the unnormalized w basis. The two exterior signs cancel. | All coefficients of the quartic identity in 24 real indeterminates agree; sign, scaling, and conjugated-coordinate controls reject the incorrect alternatives. |
| Reality, linearity, injectivity, or dimension error | Hermitian conjugation and even-degree factor interchange give reality; distinct (2,2) basis elements give injection. The source space has real dimension 225. | Rational coordinate matrix rank 225, all 225 real columns, exact Gram matrix, and rational denominators 1 or 2. |
| Nonorthogonal, zero, dependent, or phase boundary | The projector identity holds for all a,b without orthogonality. Unit simple bivectors can be orthonormally refactored; phase leaves the projector unchanged. | Universal polynomial identity includes all such boundaries; direct zero/dependent and nonorthogonal controls. |
| Wrong face functionals | Phi(A(H))=trace H, Q(A(H))=trace(P_D H) on all Hermitian H. | Both equations checked on each of the 225 real basis columns. |
| Cancellation in the D-projection condition | trace(P_D H) is the sum of positive weights times squared D-projection norms; zero forces each generator into B. | Universal positivity argument, strengthened by the PSD support proof. |
| Higher-rank complex mixed bivectors | A simple nonzero mixed bivector has one-dimensional U and Z projection lines and is x wedge y. The mixed wedge-square coefficients are minus twice the 2 by 2 tensor minors. | Projection-line proof plus nine exact universal minor identities; explicit rank-two tensor rejection. |
| Wrong real separability or norm | T:U tensor_C Z to U wedge Z is unitary; its simple mixed vectors are exactly complex rank-one tensors. A unit bivector has factor norm product 1 and can use unit factors. | Algebraic proof and nonreal rational product-generator control. |
| Illegitimate global nonnegativity of Q | Q is nonnegative only on the Kähler face. A reversed pure-U generator has Q=-1 in C. | Exact negative control; simultaneous section argument never requires Q>=0 on all C. |
| Ambient hyperplanes silently treated as separability | An entangled rank-one mixed projector satisfies trace=1 and Q=0, but its image is outside C. Membership in C is essential. | Exact rank-two bivector construction and rank-one PSD range argument. |
| Inverse not ambient linear, or lifts not preserved | The inverse extends linearly; more explicitly the certificate gives G^(-1) A^T on the whole real exterior space. Additional affine equations and composition of projections preserve finite spectrahedral lifts. | Exact 25,425 Gram entry checks and direct lift construction in the derivation. |

## Reproducible exact certificate

`coordinate_checker.py` uses only Python's standard library and no floating
point. It constructs exterior products by antisymmetric index multiplication,
Gaussian integer pairs, exact rational elimination, and sparse formal
polynomials. It does not import or execute the submitted checker. The pinned
input inventory is revalidated at every run.

The complete run establishes:

- All 225 map columns are real and rational and have rank 225.
- Phi and Q match the corresponding traces on all 225 basis vectors.
- All 25,425 upper-triangular entries of A^T A equal the explicit diagonal G
  with 15 ones and 210 twos.
- In all 495 exterior coordinates, all 11,760 nonzero monomial coefficients
  in A((a wedge b)(a wedge b)*) = a wedge Ja wedge b wedge Jb agree exactly.
- All nine universal mixed wedge-square/minor equations agree, with the
  orientation coefficient -2.
- All 16 hostile or boundary controls pass.

This coefficient comparison is an exhaustive symbolic identity, valid for
all a,b, and is stronger than testing finitely many vectors. The finite
hostile planes are implementation controls. They do not establish the
universal geometric convex-hull equality, which is supplied separately by
the complete derivation.

The submitted determinant-based validator also returns PASS with the pinned
certificate. The independently constructed map agrees in every coordinate
of each of its 225 columns. The submitted certificate hash is
`e13728df67604942d969f9c7d8fcf9490ce09a85954f92bf04c14d2d44fd50a5`;
the independent certificate hash is
`02cb36e1464a613c389a6d57b39e8176c27badd887e31c0d09338d90bacf037b`.

The checker uses unconditional checks rather than Python assertions. Ordinary
and optimized execution return identical verdicts apart from the optimization
flag. Three actual corrupted checker copies were rejected: changing the u
eigenspace convention fails the universal projector identity, doubling the
embedding fails the trace test, and reversing the minor sign fails the mixed
identity. This makes the negative controls nonvacuous. Exact diagnostics and
exit codes are recorded in `MUTATION_AND_OPTIMIZATION_CHECK.json`.

Run from this directory:

    python3 coordinate_checker.py

The full coordinate matrix, explicit Gram inverse convention, machine verdict,
input pin check, output pins, stdout/stderr, and mutation artifacts are saved
alongside this report.

## Remaining gap and disposition

There is no remaining geometric gap under the stated conventions. The route
does not transfer its geometric difficulty to an unsupported claim: its face,
section, and map equalities have direct proofs. Its use to exclude a lift of
C(4,12) still depends on the independently audited external obstruction for
complex Sep(3,3), and the deduction of a failing support function depends on
the separate moment/SOS argument. The full target theorem and novelty must be
assessed by combining those separate obligations. This family supplies no
coefficient-level failing calibration or SDP infeasibility certificate.

Completion estimate for this assigned geometric audit: 100%. This is not a
percentage estimate for the full research problem or its publication status.
