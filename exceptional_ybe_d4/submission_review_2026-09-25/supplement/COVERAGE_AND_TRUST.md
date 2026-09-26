# Computational coverage and trust boundaries

Companion to **A five-word Pauli–Clifford normal form for an exceptional unitary Hecke Yang–Baxter operator**, Alec Kriebel, submitted to *Algebras and Representation Theory*. Contact: me@aleckriebel.com; affiliation: Independent researcher, San Francisco, USA; ORCID: https://orcid.org/0009-0001-9320-500X.

## Claims checked by each route

| File | Finite claim established by successful execution |
| --- | --- |
| `verify_exact.py` | Sparse exact matrices: H Hermitian/involutive/traceless; cubic reflection relation; R unitary, Hecke and Yang–Baxter; projection rank/partial traces; both obstruction trace-square values 1/18; own active operator and sitewise-swap factorization; own active shift residuals squared (24,0), far commutativity; six independent three-strand Hecke word images. Also the separate auxiliary block-matrix diagnostics below. |
| `verify_tensor_words.py` | Matrix-free multiplication in the real Pauli algebra over rational polynomials in alpha,beta; the complete 18-word generic residual and its vanishing at alpha²=2/3, beta²=1/3; axis exclusion and the nondegenerate converse factor. |
| `verify_supplied.py` | SymPy reconstruction of the central matrix identities, projection rank, both partial traces and obstruction norms, sitewise-swap factorization and active generalized Yang–Baxter identity. |
| `verify_concurrent_equivalence.py` | Independent encoding of the intrinsic quaternionic generators, the Galindo–Rowell Family III local formula, the displayed local unitary, and the exact comparison after reversing the two local sites. |
| `verify_braid_link.py` | Rechecks the intrinsic factorization and local comparison; enhancement, inverse/skein constants, local order and selected two-/three-strand link values; eight-term standard-frame non-Clifford witness; ordered Pauli quarter-turns; reversal and Garside conjugacies for every generator at n=3,4. |
| `test_failure_modes.py` | 26 focused tests covering deliberate coefficient, scalar, tensor-placement, unitary, quarter-turn, writhe, skein, index and Garside mutations; optimization rejection; assertion-statement absence; generic converse branches; malformed/unsafe/mismatched manifest entries. |
| `verify_checksums.py` | All manifest entries have the stated SHA-256 digest; paths are canonical and package-local, with duplicates/escapes rejected. |

A successful computation does not by itself prove the all-n Markov-trace identification and tower faithfulness, the complete classification-based dimension-three exclusion, all-n conjugacy, cited finite-image/algorithmic theorems, or the branched-cover interpretation. Those depend on the manuscript proofs and external sources. Fixed n=3,4 checks are consistency checks, not induction or universal certification. The obstruction norms are computed in the concrete d=4 trace model; applying them to exclude a different dimension requires the manuscript's trace and classification arguments.

## Arithmetic and independence

All finite comparisons are exact. The custom arithmetic uses rational coefficients in `(1,sqrt(2),sqrt(3),sqrt(6))`, with a separate real/imaginary pair. The SymPy calculations use integers, rationals and radicals. No floating-point tolerances or random samples are used.

Five routes do not mean five fully independent implementations. The sparse standard-library and dense concurrent verifiers contain versions of the same field-arithmetic formulas. The braid/link verifier imports the concurrent verifier's arithmetic and matrix helpers and adds an exact Pauli-sum representation. The polynomial Pauli-word verifier and SymPy verifier supply different computational mechanisms for the core construction. These are readable executable checks, not machine-checked formal proofs.

The mutation helper requires both a nonzero process status and `AssertionError:` in stderr, so a syntax/import failure is not counted as detection of the mathematical mutation. Mutation rejection certifies inconsistency with the fixed displayed witness or certificate; it does not assert that every altered matrix fails the Yang–Baxter equation. In particular, the reflection circle includes other sign choices. The temporary-copy test harness uses a documented current-directory fallback to load the unchanged sibling arithmetic module. Normal execution loads that sibling directly.

## Auxiliary block-matrix definitions

Let q=(1+i sqrt(3))/2, zeta=(1+i)/sqrt(2), and let A and B be the two four-by-four arrays written explicitly in `verify_exact.py`. The separately defined common-prefactor matrix is

`K_common = (-conjugate(q)/sqrt(2)) A ⊕ (-conjugate(q)/sqrt(2)) B`.

It is also checked against the independent Pauli encoding

`K_common = -conjugate(q)/2 (III + i IXI - i ZZZ + ZJZ)`.

It is unitary, obeys `(K_common+I)(K_common-qI)=0`, has trace `4(q-1)` and spectral multiplicities 4+4, has unnormalized squared generalized Yang–Baxter residuals `(0,48)` at qubit shifts `(1,2)`, and satisfies the checked far-commutativity relation. These are properties of this explicit definition. It is not identified with a literal source display or an intended author correction.

The accessible GHR preprint [arXiv:1105.5048v1](https://arxiv.org/pdf/1105.5048v1), p. 26, Eq. (5.2), instead prints the mixed-prefactor display

`K_printed = (-conjugate(q)/sqrt(2)) A ⊕ (1/sqrt(2)) B`.

The code separately checks its trace `1+i sqrt(3)`, normalized Hecke residual squared Frobenius norm `18`, and generalized Yang–Baxter residual squared norms `(30,60)`. Thus the common-prefactor identities must not be attributed to that literal printed matrix. These observations concern the accessible display and its stated tensor convention; they do not adjudicate the intended correction or any later journal rendering. The revised manuscript does not use this auxiliary comparison.

## Curation boundary

The original release's 32-test suite was rerun before curation. Six historical-package tests are omitted here: preservation of the original unsupported attachment; original source-archive allowlist; inclusion of release records; old literal manuscript wording; original version metadata; and the old packager's output-directory behavior. The remaining 26 tests exercise the actual curated scientific package. No private review notes, correspondence, older papers, original discovery attachment, environment, cache or unrelated files are distributed.
