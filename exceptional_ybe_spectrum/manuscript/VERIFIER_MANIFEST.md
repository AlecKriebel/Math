# Exact verifier manifest

## Purpose and boundary

This manifest identifies the deterministic exact-arithmetic programs used to
replay the finite calculations supporting *Low-Schmidt Rigidity and
Tensor-Local Constraints in the Exceptional Unitary Hecke Yang--Baxter
Class*.  The manuscript proofs remain the primary mathematical arguments.
A successful replay means that the
listed finite identities, ranks, enumerations, and calibration examples passed
their assertions; it does **not** turn a scoped ansatz theorem into a theorem
about arbitrary exceptional solutions.

Run the central suite from the project root with

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/run_frontier_paper_verifiers.py
```

The checked-in transcript is
`results/frontier_paper_verifier_suite_exact.txt`.  The runner itself is
read-only: it neither changes that transcript nor writes any other evidence
file.  It excludes random and numerical searches.

## Environment

- Recorded replay environment: CPython 3.9.6.
- Required third-party package: SymPy 1.14.0.
- Standard-library-only programs are marked below.
- NumPy and SciPy are not used by this suite.
- Child processes run with Python assertions enabled, bytecode writing
  disabled, a fixed hash seed, and the `C` locale.

All matrix and polynomial calculations use integers, rational numbers, or
exact SymPy algebraic expressions.  There are no floating-point tolerances.

## Central suite

| Suite name | Program | Exact calculation replayed | Theorem supported and scope boundary |
|---|---|---|---|
| `tower-multiplicities` | `scripts/hecke_multiplicity_spectrum.py` | Admissible Young-lattice paths, integer quantum dimensions, Markov-weight sums, and simple-block multiplicities through the requested levels. Standard library only. | Supports the all-level formula \(m_{\lambda,n}=D_\lambda(d/2)^n\) and the conclusion that this abstract multiplicity arithmetic permits every even \(d\). It does not construct a tensor-local \(R\)-matrix and does not test repeated use of one common two-site operator. |
| `two-projection-blocks` | `verifiers/verify_two_projection_blocks.py` | The exact \(2\times2\) generic block at principal-angle parameter \(1/3\), the central block values, and the \(d=6\) Markov multiplicities \(27,81,27\). | Calibrates the canonical two-projection decomposition. The classification of all abstract blocks and its tensor-local interpretation are human arguments. |
| `controlled-leg-divisibility` | `verifiers/verify_controlled_leg_divisibility.py` | Both compression orientations, common-one/common-zero ranks, the arithmetic \(8\mid r d^2\), the published \(d=4\) calibration, and an exact local-equivalence counter-audit. | Supports the leg-commutant projection theorem. It does not claim that either one-sided leg commutant is always nontrivial. |
| `low-schmidt-obstruction` | `verifiers/verify_low_schmidt_control_obstruction.py` | The conversion from four-unitary controlled equivalence to a valid sitewise twisted-control form, the crucial off-diagonal cubic coefficient, and exact \(d=4\) and \(d=6\) calibrations. | Supports the operator-Schmidt-rank-at-most-three theorem together with the cited rank-two/rank-three controlled-unitary classification theorems. It says nothing about unrestricted Schmidt rank at least four. |
| `osr4-joint-sandwich` | `verifiers/verify_osr4_joint_sandwich_degeneracy.py` | Dimension-five \(C^*\)-types, quotient/sandwich calibrations, exact ranks and kernels for the published solution and limitation models, and the Hermitian-traceless kernel extraction. | Supports the finite parts of the unrestricted OSR-four joint-sandwich theorem. The all-dimension quotient argument and the implication from injectivity to a five-dimensional \(C^*\)-algebra are human proofs. The script explicitly does not prove \(4\mid d\) for every OSR-four solution. |
| `restrictable-four-strand` | `verifiers/verify_restrictable_four_strand_obstruction.py` | The two one-dimensional four-strand Hecke idempotents, their arbitrary-parameter Markov traces, the unique common zero \(1/2\), and all nine mixed-color operator-word equations. | Supports balanced inheritance by a square-invariant local subspace and the no-restrictable-\(d=6\) theorem. It does not turn a one-sided \(4+2\) square restriction into a two-sided restriction. |
| `d6-common-leg-intersection` | `verifiers/verify_d6_two_block_leg_types.py` | Two-block relative intersections, endpoint cubic blocks, determinant-gap propagation, and the \(d=6\) multiplicity arithmetic. | Supports \(\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb C I_6\), using the independently established emptiness of the \(d=2\) exceptional class. It does not assert \(\mathcal C_L(P)=\mathbb C I_6\) or \(\mathcal C_R(P)=\mathbb C I_6\) separately. |
| `primitive-weyl-bell` | `verifiers/verify_weyl_bell_diagonal_divisibility.py` | The exact primitive \(d=6\) Weyl/Bell basis, zero marginals, the common three-site Weyl action, and the forced spectral multiplicities at \(d=4,6\). | Supports four-divisibility for reflections diagonal in the generalized Bell basis of a **primitive** Weyl pair. It does not cover arbitrary maximally entangled bases or arbitrary exceptional solutions. |
| `fixed-d4-bell-exhaustion` | `verifiers/verify_d4_bell_diagonal_exhaustive.py` | All \(12{,}870\) balanced sign tables in one fixed \(d=4\) generalized Bell basis, using Gaussian-integer arithmetic after clearing denominators, plus a direct matrix calibration. | Supplements the primitive-Weyl theorem. The exhaustion is only for the specified fixed Weyl/Bell basis and makes no claim about all \(d=4\) solutions. |
| `four-product-clifford-frame` | `verifiers/verify_osr4_clifford_frame_parity.py` | All 64 four-vertex complement graphs, finite Pauli-word algebra, and an exact nonexceptional \(d=4\) calibration. Standard library only. | Supports four-divisibility only for the stated four-product frame with pairwise-anticommuting product terms and the manuscript's local-factor hypotheses. It is not an unrestricted OSR-four classification. |

## Human-proof and external-theorem dependencies

Some central statements are not computational conclusions and therefore do
not have a separate program in this suite.

- Automatic scalar partial traces use the no-opposite-spectrum/irreducibility
  result and the standardness propositions in Lechner's classification,
  followed by an explicit affine calculation and tensor reversal.  No
  irreducibility hypothesis is silently added: it is derived under the
  exceptional-class hypotheses.
- Faithfulness means faithfulness of the induced representation of the
  Jones--Wenzl **trace quotient**
  \(H_n(q)/\operatorname{Ann}\mu_{1/2}=H_n(3,6)\).  It does not mean
  faithfulness of the raw specialized Hecke algebra, braid group, or group
  algebra.
- The low-Schmidt theorem uses Cohen--Yu's rank-two and Chen--Yu's rank-three
  local controlled-unitary classifications.  The exact verifier checks the
  tensor-local conversion and cubic step, not those external classification
  theorems themselves.
- The \(d=6\) common-leg-intersection and restrictability consequences use the
  previously established emptiness of the \(d=2\) exceptional class.

The bibliography and theorem statements in the manuscript give the precise
citations and hypotheses.

## Deliberate exclusions

The suite does not run any Grassmann, Riemannian, alternating-projection,
least-squares, random-seed, or other numerical search.  It also omits the
one-sided fixed-\(d=4\) extension search, optimizer traps, and the longer
catalogue of symmetry-specific no-go programs.  Those computations cannot
prove unrestricted \(d=6\) nonexistence and are not needed to verify the
paper's central theorem package.

The second exact \(d=4\) family is likewise outside the central suite.  Its
equivalence status is discussed separately and is not used in any dimension
obstruction.
