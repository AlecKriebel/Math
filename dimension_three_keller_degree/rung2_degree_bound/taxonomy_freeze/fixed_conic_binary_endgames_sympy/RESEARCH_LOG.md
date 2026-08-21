# Research log: binary fixed-conic endgame composition

## 2026-07-26T10:14:42Z — kickoff

- Input is the complete E7 affine fibres retained in the sibling
  `fixed_conic_binary_repair_sympy` artifact.
- Required branches are split scalar/opposite/zero and double-root
  scalar/semisimple/nilpotent/zero.
- Each branch will begin before its first legacy specialization, retain
  every compatible coefficient of \(V\), all eleven free \(H_2\)
  coefficients, and all nine entries of \(L\), then solve weighted
  determinant equations in descending order.
- The first legacy family which does not span the exact surviving fibre
  will produce a concrete `FAIL-CLOSED` verdict rather than an inferred
  repair.
- Existing ledger and Git state will not be edited.
- Best-guess completion: 5%.

## 2026-07-26T10:41:51Z — all endgame fibres composed

- Split scalar was reconstructed from the complete E7 fibre.  E6 forces
  (13), E5 forces all of (14), E4 supplies the square certificates
  (15)--(16), and E2 reproduces (17)--(19).
- Split opposite E6 gives exactly (11); its complete E5 compatibility has
  constant magnitude \(64\).
- The two nonzero split zero-tangent support orbits reproduce constants
  \(8\) and \(8,16,8\).  The zero support is binary.
- Double scalar was reconstructed through the E5 \(Y^2\) boundary, all
  relations (23)--(25), and the square/determinant exit (26)--(27).
- Double semisimple E5 kills all three deviation parameters.  A constant
  \(9\times9\) minor \(32768\) gives the unique displayed solution (30),
  whose determinant is zero.
- Double nilpotent E5 gives
  \(J=0,\ w_{14}=G^2/4,\ w_8=GK/2,\ K(v_1-2K)=0\).
  The \(K\ne0\) chart has fixed minor \(-262144K^3\) and singular \(L\);
  the separately solved \(K=0\) chart gives the dependent-column
  relations (33).
- Both nonzero double zero-tangent Borel orbits reproduce (35)--(36) and
  constant obstruction \(8\); the zero support is binary.
- The strict checker passes under `python -O` with exact SymPy 1.14.0 in
  approximately eleven seconds and about 72 MB maximum RSS.
- No omitted branch or counterexample was found.
- Concrete verdict: **PASS**.
- Best-guess completion: 100%.
