# Research log: exact-\(\delta=3\) construction search

All timestamps are UTC.

## 2026-07-26T08:24:39Z — program opened

- Opened a dedicated construction/search track for the frozen
  exact-\(\delta=3\), Hilbert--Burch \(\{2,1\}\) strata.
- Priority representatives are:
  \[
  \begin{array}{c|c|c}
  \text{ID}&h&R\\ \hline
  \texttt{D3-BB-21}&pq&p^2q\\
  \texttt{D3-BS-N2-Z}&p^2&p^2q.
  \end{array}
  \]
- The fixed quartic top is
  \(H_4=(hp^2,hq^2,0)\), the fixed third cubic component is
  \(R=(H_3)_3=p^2q\), and the Keller equations are the homogeneous
  coefficients of
  \[
  \det(L+zJH_2+z^2JH_3+z^3JH_4)=\det L.
  \]
- The canonical denominator source is
  `audit_delta_ge3_denominator/DENOMINATOR.json`.  This track will bind
  its exact SHA-256 and its 26-family count in the final verifier.
- No BCW reduction will be used.  Every calculation will either retain
  all lower coefficients at its stated stage or carry an explicit
  sparse-ansatz label.
- No commit or push is authorized for this task.

## 2026-07-26T08:41:51Z — exact tangent loci and ansatz obstructions

- Reconstructed the full \(E_7\) syzygy spaces for both targets.  Their
  nullities are \((r^2,r^1,r^0)=(0,1,3)\), as required on the frozen
  exact-\(\delta=3\), \(\{2,1\}\) row.
- With binary lower summands initially zero, computed the complete
  \(E_6\) compatibility ideals.  Their reduced loci are:
  \[
  \begin{aligned}
  \texttt{D3-BB-21}:&\quad
  x=0,\ y_2=0,\ 3y_0^2-8y_0y_1+12y_1^2=0,\\
  \texttt{D3-BS-N2-Z}:&\quad
  x=0,\ y_1(y_0-y_2)=0.
  \end{aligned}
  \]
- Proved an exact \(E_4\) obstruction for the zero-binary-nonlinear
  tangent on both targets while retaining arbitrary first quadratic
  components \(A,B\) and arbitrary linear part \(L\).  The decisive
  squares are \(24\ell_8^2/5\) and \(8\ell_8^2\), respectively, after
  the complete \(E_6/E_5\) solve.
- Proved an exact \(E_4\) obstruction for the nonzero branch-square
  tangent \(U=0,V=2kpqr,T=kpr\), localized at \(k\ne0\), again with
  arbitrary \(A,B,L\).
- Proved an exact \(E_5\) obstruction for both conjugate nonzero
  `D3-BB-21` tangents over \(\mathbf Q(\tau)\), \(\tau^2=-5\).  The
  fixed coefficient is
  \[
  [p^2qr^2]E_5=\frac{24}{5}k^3(25+8\tau),
  \]
  whose coefficient norm is \(108864/5\).
- Ran the broadened deterministic modular portfolio at
  \(\mathbf F_{23}\) and \(\mathbf F_{29}\), sampling all eleven binary
  coefficients of \(U_0,V_0,T_0\) while solving \(A,B,L\) completely at
  \(E_6/E_5\).  The frozen seed was `20260726`; 42 binary samples and
  3,072 lower affine points produced no full modular Keller hit.
  This is recorded only as reconnaissance, not an obstruction.
- Added a fail-closed strict wrapper with five exact mutations, an
  optimized-Python bypass test, and a bad-prime test.  Terminal marker:
  `D3_CONSTRUCTION_SEARCH_STRICT_PASS`.

## 2026-07-26T08:49:13Z — arbitrary-binary BB branch and origin audit

- Restored independent symbols for all eleven binary coefficients
  \(U_0,V_0\in S_3\) and \(T_0\in S_2\) on the two displayed nonzero
  `D3-BB-21` branches.  Also retained all twelve coefficients of
  \(A,B\) and all nine entries of \(L\).
- Direct exact expansion of the original weighted determinant, followed
  by polynomial reduction modulo \(\tau^2+5\), left
  \[
  [p^2qr^2]E_5=\frac{24}{5}k^3(25+8\tau).
  \]
  Its free-symbol set is exactly \(\{k,\tau\}\); the coefficient is
  independent of every restored lower coefficient.  This is therefore
  an arbitrary-binary exact obstruction on the two displayed conjugate
  branches, not a sparse or modular inference.
- Separately audited the \(E_7\)-origin with arbitrary binary
  \(U_0,V_0,T_0\).  The complete \(E_6\) solve has rank six and leaves
  only the degree-one syzygy:
  \[
  (A_r,B_r,\ell_{33})=
  \begin{cases}
  (\frac85\ell_{33}p,0,\ell_{33})&\texttt{D3-BB-21},\\
  (0,2\ell_{33}q,\ell_{33})&\texttt{D3-BS-N2-Z}.
  \end{cases}
  \]
  At \(\ell_{33}=0\) all nonlinear terms are binary.  At
  \(\ell_{33}\ne0\), the third component is a degree-at-most-three
  triangular coordinate.  The corresponding plane degrees are at most
  \(4\) and \(12\), so the established plane low-degree exit makes every
  Keller map at the origin an automorphism.

## 2026-07-26T09:00:34Z — full BB parameter space and independent replay

- Upgraded from the two conjugate sample lines to the complete
  `D3-BB-21` \(E_7\) parameterization
  \[
  S=ap+bq+cr,\qquad
  U_r=\frac p5(8S-kp),\quad V_r=kq^2,\quad T_r=S,
  \]
  retaining arbitrary binary \(U_0,V_0,T_0\), arbitrary quadratics
  \(A,B\), and arbitrary \(L\).
- Exact \(E_6\) coefficients force
  \[
  c=0,\quad b=0,\quad
  C=12a^2-8ak+3k^2=0,
  \]
  with endpoint equations
  \(v_0(3a-k)=0\) and \(u_3(2k-a)=0\).
- Solved all ordinary \(E_6\) pivots and replayed the whole residual:
  \[
  E_6=\frac25Cp^3q^2r
      +\frac35v_0(3a-k)p^6
      +3u_3(2k-a)pq^5.
  \]
- After those pivots, the raw coefficient
  \[
  [p^2qr^2]E_5=\frac25ak(8a-k)
  \]
  is independent of every lower coefficient.  Its resultants with \(C\)
  are \(1680a^6\) and \(420k^6\), so \(E_6=E_5=0\) forces
  \(a=k=0\).  Combined with the structural origin audit, this excludes
  `D3-BB-21` as a counterexample family.
- Added an independent PARI/GP reconstruction of the full parameterization,
  \(E_6\) pivots, \(E_5\) coefficient, resultants, and both origin blocks.
  Its required-failure mutation negates the decisive \(E_5\) coefficient.

## 2026-07-26T09:21:33Z — full BS parameter space

- Restored the complete `D3-BS-N2-Z` \(E_7\) parameterization
  \[
  S=ap+bq+cr,\qquad
  U_r=-2kp^2,\quad V_r=2qS+kq^2,\quad T_r=S,
  \]
  with all eleven binary coefficients, arbitrary ternary quadratics
  \(A,B\), and arbitrary \(L\).
- Replayed the complete ordinary \(E_6\) pivots.  Exact \(E_6/E_5\)
  coefficients force
  \[
  c=0,\qquad b+k=0,\qquad a^2b=0,\qquad
  bu_2+6au_3=0.
  \]
- Verified directly that nonzero scaling of the source variable \(r\)
  normalizes the two non-origin components without changing the frozen
  top or losing linear invertibility.
- In the normalized chart \(a=1,b=k=0\), the exact \(E_5\) equations
  force \(u_2=0\) and \(2t_2=3v_3\).  A fixed \(E_4\) coefficient then
  forces \(v_3=0\), after which columns two and three of \(L\) are
  proportional.
- In the normalized chart \(a=0,b=1,k=-1\), \(E_5\) forces
  \(v_0=0\), \(u_0=4t_1-2v_2\), and
  \(u_3(t_1-v_2)=0\).  The \(u_3\ne0\) branch makes columns one and
  three of \(L\) proportional at \(E_4\).
- For \(u_3=0\), set \(d=t_1-v_2\).  The \(d\ne0\) branch has the
  lower-independent contradiction
  \([q^2r]E_3=12d^3\).  On \(d=0\),
  \([p^3]E_3=-4(-\ell_6+t_0v_2)^2\), and the same linear factor divides
  \(\det L\).
- Added a required-failure `bs_full` mutation to the primary verifier
  and strict wrapper.  Together with the structural origin exit, this
  promotes `D3-BS-N2-Z` to a full counterexample-family exclusion.
- No commit or push was made.

## 2026-07-26T09:30:11Z — fail-closed replay

- Added an explicit successful exit to the PARI/GP verifier so it cannot
  remain at an interactive prompt after printing its terminal marker.
- Refined the strict wrapper's PARI diagnostic filter to permit warning
  lines while still rejecting actual interpreter-error signatures.
- Strengthened the BS primary certificate so every \(u_3\)- or
  \(d\)-localized pivot is preceded by its exact factored coefficient,
  and every subsequent ordinary \(E_4\) pivot is checked before
  substitution.
- Replayed the complete strict suite, including the primary baseline,
  independent PARI baseline and fault injection, modular portfolio, six
  corrupted primary certificates, optimized-Python guard, and bad-prime
  guard.  Terminal marker:
  `D3_CONSTRUCTION_SEARCH_STRICT_PASS`.
- Wall time for the final complete strict replay was 73.24 seconds.
