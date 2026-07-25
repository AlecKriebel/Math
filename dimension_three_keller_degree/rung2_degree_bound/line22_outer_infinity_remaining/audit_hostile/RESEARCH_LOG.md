# Hostile-audit research log

All times are UTC.

## 2026-07-25T06:43:00Z — scope and orbit audit

- Reconstructed the pencil stabilizer from rank and factorization.
- Confirmed that its only action on \(u=p/q\) is nonzero scaling, hence
  that \((a,c)\) is classified by the fixed origin plus
  \(\mathbb P^1_{[a:c]}\).
- Checked that the five strata in the note are disjoint and exhaustive,
  including both projective endpoints.
- Verified that the two target shears have determinant one, preserve
  \(H_4\), and only relabel unrestricted lower coefficients.

## 2026-07-25T06:48:00Z — raw \(E_7\) reconstruction

- Independently expanded the general raw \(E_7\) system.
- Reproduced ranks/nullities \(18/8,14/12,14/12,16/10,18/8\).
- Reproduced the symbolic generic maximal minor and all four specialized
  maximal minors exactly.
- Compared the ranks of the parameter-direction matrices with the raw
  nullities after restoring the two shear directions.  All five displayed
  kernels are complete.

## 2026-07-25T06:54:00Z — lower converses and exceptional leaves

- Rebuilt the lower coefficient matrices after each square constraint.
- Obtained \(E_6\) ranks \(10\) on the generic, \(c=0\), and \(a=0\)
  leaves, and rank \(8\) with exactly two declared free variables at each
  resonance.
- Obtained \(E_5\) rank \(4\) on every leaf.  Exact witness minors were
  \(144(2t-3)^2,1296,5184,1296,576\).
- Reproduced both complete \(K_i\) residuals and all four \(K_i=0\)
  degree-four squares.
- Confirmed every determinant exit as a division-free proportional-column
  identity, including zero column factors.

## 2026-07-25T07:01:00Z — executable and scope closure

- Ran the SymPy, strict PARI/GP, and supplied fault-injection tests; all
  passed.
- Added hostile cases consisting of a diagnostic followed by the correct
  sentinel and correct sentinel followed by extra output; both failed
  closed.
- Checked the separate hostile audit for \((a,c)=(0,0)\) and confirmed
  that it has exactly the scope needed for the final finite-companion
  conclusion.
- Corrected the raw-rank table's generic row to state \(a\ne0\); without
  that qualifier its condition overlapped the separately listed
  \(a=0,c\ne0\) endpoint despite using the normalization \((1,t)\).
- Recorded PASS.  No global document was edited and no commit was made.
