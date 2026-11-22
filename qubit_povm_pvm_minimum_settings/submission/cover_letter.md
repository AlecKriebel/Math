# Cover letter for Physical Review A

Dear Editors,

Please consider the manuscript **“Minimum Bell-Setting Complexity for Qubit
POVM–PVM Separation”** for publication as a Regular Article in the Quantum
Information Science section of *Physical Review A*.

**The question.** Gisin asked whether a Bell inequality can require
generalized measurements (POVMs), rather than projective ones, at fixed local
dimension. Vértesi and Bene answered this for qubits with three settings on
one side and two on the other [Phys. Rev. A 82, 062115 (2010)]. Whether two
settings per party can suffice has remained open. Navascués, Feix, Araújo and
Vértesi recorded the conjecture that POVMs do not improve the qubit bound of
the two-setting CGLMP inequality and reported that their hierarchy could not
confirm it [Phys. Rev. A 92, 042117 (2015)]. Two 2026 preprints treat the
two-setting case as an open program (arXiv:2603.26875, arXiv:2608.01317).

**The result.** With two settings per party and any finite number of outcomes
per setting, every behavior of a bipartite qubit POVM strategy is a finite
shared-randomness mixture of projective qubit strategies. One mixture
reproduces the complete table for all input pairs. Together with a
three-setting witness this fixes the minimum input architecture for a qubit
POVM advantage at three settings against two, up to exchanging the parties.

**Consequences in the manuscript.**

- The qubit bound of every two-setting Bell functional, with any number of
  outcomes, is the largest eigenvalue of a real 4 × 4 matrix maximized over
  two angles and finitely many label assignments.
- A value above that bound certifies Schmidt number at least three in any
  finite-dimensional realization.
- A rational three-by-two Bell functional has an explicit qubit POVM strategy
  with value (16 + 8√7813)/25 ≈ 28.9252, while a rational sum-of-squares
  certificate printed in the appendix bounds every projective qubit strategy
  by 289/10.

**Verification.** The two-setting equality, the common-mixture simulation,
the three-by-two separation and the resulting minimum are formalized in
Lean 4 from a matrix model of states, effects and the Born rule. Appendix I
of the manuscript states which results are machine-checked and which are
proved only in prose. The two corollaries on the two-angle bound and the
Schmidt number are short manuscript deductions and are not formalized. The
proof sources, exact witness data and verification records are public at the
pinned revision cited in the Data Availability statement.

**Use of AI tools.** Generative AI tools were used substantively for
mathematical exploration, derivations, literature review, programming, Lean
formalization, writing and pre-submission review. The manuscript's AI Use
Disclosure names the tools and describes their use and the checks applied.
I directed the work, selected the claims, and take full responsibility for
the manuscript.

**Prior posting.** An earlier version is public as a preprint
(https://doi.org/10.5281/zenodo.21699161). The manuscript has not been
published and is not under consideration elsewhere.

Sincerely,

Alec Kriebel  
Independent Researcher  
`me@aleckriebel.com`  
ORCID 0009-0001-9320-500X
