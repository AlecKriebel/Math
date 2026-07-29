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

## Rules

- A numerical residual, however small, cannot upgrade a claim to
  `EXACT_COMPUTATION`.
- A finite search can support nonexistence only after its search space,
  symmetry reduction, and case coverage are proved complete.
- Every status upgrade must be dated in `RESEARCH_LOG.md` and linked to a
  proof, certificate, or verifier.
