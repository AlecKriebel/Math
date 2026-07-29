# Claim ledger

Statuses used here:

`SPECULATION`, `NUMERICAL_EVIDENCE`, `EXACT_COMPUTATION`, `PROVED`,
`INDEPENDENTLY_REPRODUCED`, `EXTERNALLY_REVIEWED`.

| ID | Claim | Status | Evidence / dependency |
|---|---|---|---|
| C0 | The \(d=4\) published witness satisfies all defining relations. | INDEPENDENTLY_REPRODUCED | E1 reran three exact routes, including direct matrices and abstract tensor words. |
| C1 | Solutions exist for every \(d\) divisible by four. | PROVED | Tensor the \(d=4\) witness with spectator identity factors and reorder tensor factors. |
| C2 | No solution exists for \(d=2\). | PROVED | Lechner classification, subject to source-normalization audit in this project. |
| C3 | For abstract projections \(p,q\) obeying (YB-P), every nontrivial Halmos two-projection block has squared principal cosine \(1/3\), and unmatched \(p=1,q=0\) or \(p=0,q=1\) blocks are impossible. | PROVED | Human proof in `notes/track_structural_projection.md`; exact block verifier replayed. |
| C4 | Every exceptional matrix-class solution has scalar partial traces \(\operatorname{Tr}_1P=\operatorname{Tr}_2P=(d/2)I\). | PROVED | Lechner Propositions 2.3--2.4 plus explicit affine calculation and tensor reversal. |
| C5 | Every matrix-class solution induces the \(\eta=1/2\) Markov trace at all levels. | PROVED | No-opposite-spectrum theorem applies automatically; finite-level propagation also follows directly from C4. |
| C6 | The complete Hecke-tower multiplicity arithmetic imposes exactly \(2\mid d\), not \(4\mid d\). | INDEPENDENTLY_REPRODUCED | Formula \(m_{\lambda,n}=D_\lambda(d/2)^n\); Young-lattice and two independent fusion-graph implementations. |
| C7 | A \(d=6\) solution exists. | SPECULATION | Independent falsifier track. |
| C8 | The complete spectrum is exactly \(4\mathbb N\). | SPECULATION | Primary candidate, not a working assumption. |
| C9 | Every exceptional matrix-class solution faithfully represents \(H_n(3,6)\) for every \(n\). | PROVED | C5 identifies the trace; faithful matrix trace makes the representation kernel equal its trace radical. |
| C10 | One-sided faithful tensor-tower representations with the required Markov character exist abstractly for every even \(d\); any stronger obstruction must use both spatial shifts. | PROVED | `notes/track_coherence_parity.md`, Proposition 1.1. |
| C11 | No non-scalar monomial unitary Hecke Yang--Baxter matrix exists in any dimension. | PROVED | Cycle/minimal-polynomial reduction followed by the diagonal Yang--Baxter equation; `notes/track_additive_constructions.md`. |
| C12 | A spectator-form \(d=6\) solution is equivalent to a rank-six \(12\times12\) heterogeneous shifted operator on \(\mathbb C^2\otimes\mathbb C^3\otimes\mathbb C^2\). | PROVED | Heterogeneous blocking lemma in `notes/track_additive_constructions.md`. |
| C13 | The cyclic Gaussian-functional, scalar-cross gluing, controlled-middle, graph-phase/product-flip, diagonal \(SU(2)\), central \(S_4\), ice-rule, and monomial ansätze do not contain a \(d=6\) witness. | PROVED | Precisely scoped human proofs and exact verifiers in the additive and Gaussian notes. The noncentral \(S_4\) branch is excluded from this claim. |
| C14 | Current unrestricted and structured \(d=6\) numerical searches produced no candidate. | NUMERICAL_EVIDENCE | Calibrated Grassmann and shifted-\(K\) searches in `notes/track_d6_falsifier.md`; this is not evidence of global nonexistence. |
| C15 | The equal-sector color/face equations contain an exact one-parameter \(d=4\) family \(s^2+2t^2=1\). | EXACT_COMPUTATION | Human formula and symbolic factor certificate in `notes/track_color_face_search.md`; replayed by `scripts/verify_color_face_d4_family.py`. Equivalence and novelty are unaudited. |
| C16 | No rank-one Bloch-controlled reflection on \(\mathbb C^2\otimes\mathbb C^3\) satisfies the exceptional cubic relation. | PROVED | Human compression/Gram proof in `notes/face_rank_one_control_no_go_d6.md`; exact sign, leg-orientation, and Gram checks in `verifiers/verify_face_rank_one_control_no_go.py`. |
| C17 | If a rank-\(r\) projection lies in either one-leg commutant of an exceptional solution, then \(8\mid rd^2\); its restricted common-one and common-zero multiplicities are both \(rd^2/8\). Hence a \(d\equiv2\pmod4\) solution has no odd-rank leg-commutant projection and cannot be controlled on either leg. | PROVED | Invariant restriction proof in `notes/controlled_leg_divisibility.md`; fast independent exact orientation and \(d=4\) sector replay in `verifiers/verify_controlled_leg_divisibility.py`. |
| C18 | The complete diagonal-regular group-relative ansatz is empty in every \(d\equiv2\pmod4\); in particular neither \(C_6\) nor \(S_3\) gives a \(d=6\) witness. | PROVED | C17 applies to the full arbitrary-\(h\) ansatz. `notes/group_relative_ansatz_exact.md` also gives an independent exact dual-Fourier exclusion for all \(C_6\) choices and an exact \(V_4\) skew-conference calibration. |
| C19 | The Evans--Pugh \(D^{(6)}\) cells reconstruct an exact exceptional Hecke/Yang--Baxter operator on the 20-dimensional composable-path space, but this is not an ordinary \(d=6\) local operator; zero and scalar Hecke completions on the 100-dimensional edge square fail exactly. | EXACT_COMPUTATION | Two independent cell/connection implementations in `scripts/audit_evans_pugh_d6_connection.py` and `verifiers/verify_evans_pugh_d6_from_cells.py`; interpretation in `notes/track_d6_ocneanu_cells.md`. This does not exclude a nontrivial vertex--face conversion. |
| C20 | The presently derived canonical-channel constraints, even augmented by commutation, isospectrality, the observed paired polynomial, both affine CP conditions, and the required traceless-Hermitian Kraus geometry, admit an exact abstract \(d=6\) model. | PROVED | Weyl-diagonal countermodel in `notes/track_channel_identities.md` and `verifiers/verify_channel_d6_abstract_model.py`. It is deliberately not a shared projection realization, so it closes only a proposed obstruction route. |
| C21 | Pairing the Schmidt legs of the \(d=6\) channel countermodel identically produces an exact Hermitian traceless solution of the cubic relation with minimal polynomial \(3x^2+2\sqrt3x-3\), but not an involution: its eigenvalue multiplicities are \(9\) and \(27\). | EXACT_COMPUTATION | Exact construction and \(216\times216\) cubic replay in `verifiers/verify_channel_d6_abstract_model.py`. The unique affine involution has trace \(18\), so this is not a class witness. |
| C22 | The cyclic three-color mixed low-operator-Schmidt family and its pure-product boundary contain no \(d=6\) exceptional solution, while the analogous two-color equations contain the exact published \(d=4\) family. | PROVED | Human contraction/Fourier proof in `notes/track_color_low_schmidt_exact.md`; independent symbolic certificate in `verifiers/verify_color_low_schmidt_no_go.py`. Scope is only the explicitly defined color/face family. |

## Rules

- A numerical residual, however small, cannot upgrade a claim to
  `EXACT_COMPUTATION`.
- A finite search can support nonexistence only after its search space,
  symmetry reduction, and case coverage are proved complete.
- Every status upgrade must be dated in `RESEARCH_LOG.md` and linked to a
  proof, certificate, or verifier.
