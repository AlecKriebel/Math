# Research log: hostile audit of the \(a=0,\ W_0\ne0\) leaf

## 2026-07-25T22:10:20Z — independent reconstruction started

- Created a dedicated audit folder.  The candidate note and its selected
  coefficients have not been used for the reconstruction.
- Scope fixed to the vertical companion
  \(H_4=(z^4,zq,0)^T\), \(H_3=(\frac43zW,V,z^3)^T\),
  \(H_2=(A,B,W)^T\), with \(W_0=W|_{z=0}\ne0\).
- The audit will rebuild the coefficients of
  \(\det(L+tJH_2+t^2JH_3+t^3JH_4)\) directly, prove or refute the
  advertised \(E_6\) factorization, audit every division in the subsequent
  elimination, and check that the only survivor is precisely the
  nonminimal binary boundary.
- Best-guess completion toward this local audit: **15%**.

## 2026-07-25T22:22:58Z — raw identity and divisor audit complete

- Reconstructed the literal weighted determinant with dense generic
  \(q,W,A,B,V\) and all nine entries of \(L\).  Its \(t^6\)-coefficient
  has 186 sparse terms and SHA-256 fingerprint
  `66315d214e861b16738ae96b840e1c857a794e21367d445e21cc7ba3536cb625`.
- Independently obtained
  \[
  3E_6=z\bigl(4W\{q,W\}+9z^2\{A,q\}+12z^3\{q,L_3\}\bigr)
      =z\{q,2W^2-9z^2A+12z^3L_3\}.
  \]
  The \(B,V,L_1,L_2\) terms cancel structurally; no specialization was
  made.
- On \(W_0\ne0\), the binary face gives
  \(\{q_0,W_0\}=0\).  Euler's identities and unique factorization give
  \(q_0=\kappa L^3,\ W_0=\gamma L^2\), with
  \(\kappa,\gamma\ne0\).
- After sending \(L\) to \(x\), independently recovered the six
  triangular coefficients.  Their exact ideal combinations force
  \(\chi=\beta=v=a_{02}=\epsilon=a_{11}=0\).  The only divisions are by
  the already-known units \(\kappa,\gamma\) and by nonzero integers; no
  free jet coefficient, discriminant, or linear-matrix entry is divided.
- The survivor is
  \(q=\kappa x^3+\alpha x^2z+\delta xz^2+\phi z^3\), exactly the binary
  nonminimal boundary.  No minimal-pencil counterexample was found.
- Added a standalone dependency-free certificate and strict mutation
  harness.  The strict run passes, and wrong-\(U\), bracket-sign,
  omitted-\(\chi\), missing-unit-scope, and optimized-Python mutations
  all fail through named guards.
- The supplied candidate strict suite also passes unchanged.
- Best-guess completion toward this local audit: **85%**.  Remaining work
  is the written hostile report and final clean rerun.

## 2026-07-25T22:25:43Z — hostile audit closed

- Wrote `REPORT.md` with verdict **PASS, unchanged**, the independent raw
  derivation, the complete divisor ledger, the exact nonminimal-boundary
  argument, and sharp out-of-scope counterexamples.
- Final independent and candidate strict suites both pass.  The final
  independent terminal markers are
  `A0_W0_NONZERO_INDEPENDENT_PASS_7C2E19` and
  `A0_W0_NONZERO_INDEPENDENT_STRICT_PASS_94A60D`.
- No minimal \(a=0,\ W_0\ne0\) survivor, root-type omission, or scope
  leak was found.  The \(W_0=0\) and nonminimal binary witnesses confirm
  that both stated boundaries are necessary.
- Per task instruction, no commit or push was made.
- Best-guess completion toward this local audit: **100%**.
