# Research log

## 2026-07-25T09:00Z–09:42Z

- Reconstructed the raw \(E_7\) matrix and full kernel in PARI/GP.
- Verified five independent legal gauge directions and a thirteen-vector
  normal complement.
- Rebuilt the constant-pivot \(E_6\) split and every \(K/M\) branch.
- Found that the generic aligned \(E_5\) pivot vanishes at
  \(9A=2K\).  Recomputed the zero-end leaf and found a rank-four exit
  through two \(E_4\) squares and a \(2\times2\)-minor relation.
- Found that the \(r=0\) left relation was localized at \(B_3\).
  Recomputed \(B_3=0\) and found the exact pivot \(144B_4s^2\) and
  \([y^4]E_4=4s^4/27\).
- Found that the terminal generic \(E_5\) pivot was localized at \(B_1\).
  Replaced it with global literal \(E_5\) rows and an exhaustive split on
  \(a_4\).
- Re-audited all three repairs after they were added to the primary note
  and SymPy verifier.
- Ran the primary SymPy verifier successfully and confirmed that
  `python -O` exits with status \(2\).
- Ran the strict PARI verifier and both fail-closed injections
  successfully.
- Final hostile verdict: **PASS**.
