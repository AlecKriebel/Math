# Independent review: finite-dimensional ground-state uniqueness

**Verdict: PASS_SCOPED_FINITE_DIMENSIONAL_PARAMETER_AND_ENSEMBLE_CRITERIA.** No mandatory mathematical correction was found. The complete finite-dimensional criteria and the seven-dimensional diagnostic example are valid. The original infinite-dimensional extension and the dataset's unspecified general pure-state classification remain outside the result. Recommended campaign status: **unsolved, 2/5 substantive approaches**. This is an independent adversarial AI review, not human peer review or a priority determination.

Reviewed artifact: `PARTIAL.md`, SHA-256 `e72f9e5a0f08cf1190b578b307dd9f19ef8825a2d30d7645da4d37470c83b9af`. Its mathematics remained unchanged during this review. The author verifier and receipt are preserved in `author_replay/`.

## 1. Source scope and attribution

The complete Penz–van Leeuwen contribution in [OWR 15/2025, printed pp.626–629](https://ems.press/content/serial-article-files/51359?nt=1) was checked, including the rendered parameter-uniqueness statement on p.628. Its hypotheses are a finite-dimensional complex Hilbert space, Hermitian observables, pairwise commuting constraint observables, and linear independence of the identity and those observables. Its regular-value parameter theorem is already proved in the source. The expressly open extension on p.629 is infinite dimensional. The dataset's additional demand for a unique ground-state representation does not specify pure versus ensemble representation; it cannot silently be identified with parameter uniqueness.

The [published degeneracy-geometry paper](https://quantum-journal.org/papers/q-2023-02-09-918/) is prior work. The publisher explicitly identifies Appendices A and B as additions to [arXiv version 3](https://arxiv.org/abs/2206.12366), absent from the journal article. Their complex-Hamiltonian and arbitrary-observable extensions were checked; the artifact correctly distinguishes versions. The relevant Appendix A of [Constrained Search in Imaginary Time](https://arxiv.org/abs/2504.05332) was also checked: its regular-value argument is finite dimensional and its discussion distinguishes pure states from an ensemble extension. These sources support attribution and scope; this review does not claim to re-certify every geometric proof in those papers.

Theorem 2.11 in [Ye's Conic Linear Programming notes, §2.5](https://web.stanford.edu/class/msande310/sdpmain.pdf) supplies the credited real-semidefinite maximal-support uniqueness framework. The artifact proves the complex-Hermitian version it needs rather than assuming that a real-symmetric statement automatically covers it.

## 2. Representing parameters and pure/ensemble quantifiers

The variational proof of Theorem 1 is correct. For a feasible expectation vector, the optimal ensemble set is nonempty and compact. A representing parameter has ground energy equal to the constrained optimum plus the parameter pairing, so its shifted Hamiltonian is positive semidefinite. Conversely, zero trace pairing of two positive semidefinite matrices annihilates the product. This identifies the entire optimal ensemble fiber with the density matrices supported in the shifted Hamiltonian's kernel, independently of the representing parameter.

The pure-state qualification in equation (4) is also exact. If an optimal ensemble fiber contains a rank-one state, that state represents the expectation vector for every representing parameter. Conversely, a representing pure state must minimize over ensembles as well: a lower-energy ensemble with the same expectations would contradict the ground-energy variational inequality. The proof does not assert that every ensemble-representable vector has a pure ground-state representative.

For commuting observables, simultaneous diagonalization gives the common pure/ensemble expectation domain as the convex hull of the joint eigenvalue vectors. Any convex combination is realized by the squared moduli of a pure vector's coordinates. Independence with the identity makes this domain full dimensional. Interior subgradients of the finite convex constrained energy give parameter attainment with the correct negative-subgradient sign. No boundary attainment is assumed; the displayed determinant-minus-one example correctly disproves it.

## 3. Exact radial positive-semidefinite criterion

Theorem 2 is a finite-dimensional radial feasibility test, not merely a tangent-cone test. Write the kernel compression of a Hermitian direction as C. Necessity requires C positive semidefinite, and every vector in its nullspace has zero quadratic form for the positive perturbed matrix. Such a vector must be annihilated by that matrix, forcing the claimed coupling condition to the complement of the original kernel.

For sufficiency, the direction annihilates the nullspace of C. On its orthogonal complement inside the original kernel, C is positive definite; on the complement of the original kernel, the original matrix is positive definite. The displayed Schur complement is therefore positive for sufficiently small positive step size. Both positive smallest eigenvalues are essential and available in finite dimensions. The cases of an empty positive-compression block, an empty complementary block, a zero original matrix, and a trivial original kernel all agree with the criterion. The off-diagonal two-by-two control correctly shows why compression positivity alone is insufficient.

The nondegenerate-ground-state corollary uses the same spectral-gap argument. Its conversion from complex to real linear dependence is justified because the Gram matrix of the ground vector and its commuting-Hermitian observable images is real. This is a property of the source's commuting hypotheses; the artifact does not apply this conversion to arbitrary noncommuting observables. A regular expectation value quantifies over every pure vector in that fiber and is correctly distinguished from regularity of one ground vector.

An additional scope diagnostic confirms why this proof must remain finite dimensional. On a Hilbert space with orthonormal basis e_0,e_1,..., let M e_0=D e_0=0, M e_n=n^{-1}e_n, and D e_n=(-1)^n e_n for n≥1. Both operators are bounded and self-adjoint. Kernel compression and coupling vanish, but every nonzero real t makes M+tD negative on a sufficiently large basis index of the appropriate parity. Thus the finite-dimensional radial sufficiency statement cannot simply be exported without a spectral-gap hypothesis. This is a review diagnostic, not a solution to the original infinite-dimensional classification.

## 4. Ensemble support and the seven-dimensional example

The maximal-rank argument in Theorem 4 is valid. If another optimal density matrix had range outside the maximal-rank state's range, their average would have larger rank, using the kernel-intersection identity for sums of positive matrices. A Hermitian perturbation supported on that maximal range and annihilated by the trace/observable constraints also annihilates the energy constraint, by a representing Hamiltonian's kernel identity. Both signs of a sufficiently small perturbation remain positive on that range. Conversely, two distinct optimal density matrices yield exactly such a perturbation. This proves the real-linear injectivity criterion and the necessary dimension bound.

I independently reconstructed the seven-by-two frame and its Pauli compressions. The frame is an isometry, all three original observables are diagonal and commute, and they are independent together with the identity. The Hamiltonian is the orthogonal projection away from the frame range and the seventh coordinate. The prescribed zero expectation lies in the interior of the source's octahedral domain.

For a ground vector Vξ+ze_7, the Bloch identity gives the squared norm of its expectation as ||ξ||^4/9. Thus its only pure zero-expectation projector is e_7e_7*. Nevertheless VV*/2 is a distinct optimal mixed state, and their nontrivial mixtures have full rank on the three-dimensional ground space. The compression of a nonzero parameter direction is the Pauli combination d·σ/3 together with a zero block, so it is indefinite. Hence the parameter is uniquely zero, despite ensemble nonuniqueness. The seventh-coordinate state is critical, as claimed. The real constraint map on Hermitian matrices on that three-dimensional support has rank four and kernel dimension five, consistent with the ensemble criterion.

All four additional critical/boundary examples have the claimed parameter and state fibers. In particular, a unique parameter does not imply a unique pure state, and a unique state does not imply a unique parameter. The artifact does not conflate uniqueness inside the prescribed expectation fiber with uniqueness of the whole ground eigenspace.

## 5. Reproducibility and limits

The **7,589 submitted assertions** replayed with a byte-identical receipt. The independent checker passed **1,259 exact assertions**, including complex and noncoordinate kernel controls, nullspace-coupling failures, empty blocks, the independently constructed commuting-observable example, support ranks, boundary nonattainment, and bounded-operator scope controls. An initial assertion in the independent checker compared differently factored symbolic expressions structurally; normalizing their difference corrected the test, with no change to the mathematical artifact.

From this review directory, with Python and SymPy available:

```sh
(cd author_replay && python verify.py)
python independent_checks.py
```

The scripts regenerate deterministic receipts. Exact finite checks supplement the universal arguments; they do not replace them.

The finite-dimensional parameter criterion is complete once the constrained optimum is supplied. The ensemble criterion is complete once a maximal-support optimum is supplied. General pure-state uniqueness still involves a rank-one feasibility condition, and no infinite-dimensional extension is established. The conservative unresolved status, prior-mathematics attribution, and absence of a novelty claim should be retained.
