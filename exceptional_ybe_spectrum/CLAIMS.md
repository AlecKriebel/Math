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

## Rules

- A numerical residual, however small, cannot upgrade a claim to
  `EXACT_COMPUTATION`.
- A finite search can support nonexistence only after its search space,
  symmetry reduction, and case coverage are proved complete.
- Every status upgrade must be dated in `RESEARCH_LOG.md` and linked to a
  proof, certificate, or verifier.
