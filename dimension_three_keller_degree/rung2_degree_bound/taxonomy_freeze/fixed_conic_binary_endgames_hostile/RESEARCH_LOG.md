# Research log: hostile fixed-conic binary endgames

## 2026-07-26T03:17:55-07:00 — setup and frozen inputs

- Scope: independently audit the binary fixed-conic endgames for
  `Q2-E2-A1-B2-D2-N1`.
- Information boundary: do not inspect
  `taxonomy_freeze/fixed_conic_binary_endgames_sympy/`.
- Read the frozen-row hostile `REPORT.md`, its pre-legacy Phase A derivation,
  and the completed independent PARI top repair.
- Confirmed starting certificates:
  - both \(E_8\) maps have rank 12 and 18-dimensional cubic kernels;
  - both \(E_7\) maps have rank 7 in the 18 \(H_2\) coefficients;
  - the common pivot set is
    \(w_4,w_5,w_6,w_{10},w_{12},w_{16},w_{18}\);
  - the common free set has 11 entries
    \(w_1,w_2,w_3,w_7,w_8,w_9,w_{11},w_{13},w_{14},w_{15},w_{17}\);
  - the constant pivot determinant is \(-524288=-2^{19}\);
  - the certified tangent stratification contains 3 split-root and 4
    double-root strata, including zero-field specializations.
- Next: derive complete lower-degree fibres before consulting legacy
  families (13)--(36).
- Best-guess completion: 20%.

## 2026-07-26T03:25:00-07:00 — first complete branch and support orbits

- Split opposite-weight tangent:
  - \(E_6\) rank 3 in \(L\), constant minor \(-128\);
  - eight compatibility generators reduce division-free to legacy (11);
  - the resulting 13-parameter \((V,H_2)\)-fibre has an \(E_5\)
    left-null constant \(64\).
- All four nonzero zero-tangent support orbits:
  - \(E_6\) rank 3 and minor \(-128\);
  - compatibility counts \(3,4,3,2\);
  - terminal constants \(8\), \(8,-16,8\), \(8\), \(8\).
- No mismatch or omitted branch found.
- Best-guess completion: 55%.

## 2026-07-26T03:32:00-07:00 — semisimple and nilpotent fibres

- Double semisimple tangent:
  - successive \(L\)-ranks \(3,4,2\);
  - constant minors \(-128,-32,-8\);
  - full fibre dimensions \(21\to14\to10\);
  - unique solved \(L\) has determinant zero.
- Double nilpotent tangent:
  - \(E_6\) rank 3, minor \(-128\), fibre dimension 17;
  - \(E_5\) rank 3, minor \(128\), recovers the essential product
    \(K w_3=0\);
  - on \(K\ne0\), \(E_4\) minor is \(-16K^3\), its residual conditions
    are exactly legacy (32), and \(\det L=0\);
  - on \(K=0\), the full \(E_5\) fibre has the column proportionality
    in (33).
- Best-guess completion: 80%.

## 2026-07-26T03:39:03-07:00 — scalar rank-drop and final checkpoint

- Both scalar tangents were propagated from their full \(E_7\) fibres:
  - \(E_6\) rank 3, minor \(-128\);
  - \(E_5\) rank 4, minor \(32\);
  - complete pre-\(E_4\) fibre dimension 10.
- Raw \(E_4\) square certificates force exactly the five relations in
  (15)--(16) and (25).  The two remaining \(L\) entries stay free on the
  forced rank-drop locus; no generic-rank division is used.
- Verified \(E_4=E_3=0\), both claimed \(E_2\) squares, both determinant
  squares, and the division-free ideal identities relating their linear
  factors.
- Final terminal branch count: 12 (10 contradiction branches and 2
  plane-plus-shear automorphism exits).
- Strict PARI replay passes.
- Verdict: PASS; no omitted family (13)--(36).
- Best-guess completion: 100%.
