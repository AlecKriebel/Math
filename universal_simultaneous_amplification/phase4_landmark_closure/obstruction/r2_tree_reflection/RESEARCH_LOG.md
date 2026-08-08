# Research log: `r=2` fair-geometric tree reflection

## 2026-08-08 01:41 PDT — cycle opened

- Opened a new global cycle on the exact stationary mean target
  `E_Pi |A| <= m_K`; deliberately did not reuse the stronger posterior/Brier
  split.
- Chose the Markov-chain tree theorem and complement/path reversal as the
  primary route.

## 2026-08-08 02:02 PDT — exact tree polynomial reduction

- Derived the exact burst edge probability
  `Q(C+v,C union D)=Gamma_v(C,D)/n` by inclusion-exclusion against
  `F(x)=x/(2-x)`.
- Proved that complement plus edge reversal exchanges the redundant sets
  `C` and `R=V\(C union D union {v})` while preserving `v,D`.
- Applied the directed Markov-chain tree theorem.  With
  `Z_P(t)=sum_A tau_A t^|A|`, the target is exactly

  ```text
  (n-1) 2^(n-2) Z_P(1) - (2^(n-1)-1) Z_P'(1) >= 0.
  ```

- Re-expressed this as a complement-reflected positive out-arborescence
  root-rank inequality.  This is an exact equivalent, not a sufficient
  strengthening.

## 2026-08-08 02:11 PDT — collapsed root-moving is exactly false locally

- On unweighted `K_3`, exactified an in-tree rooted at mask `3` with weight
  `4/59049`; its complement-and-arrow-reversed out-tree has weight
  `1/59049`.  Thus individual path-likelihood domination fails by factor 4
  even at the completely symmetric graph.
- Exactified a fixed state-star skeleton for which mask `6` is the only
  supported in-root.  Its conditional root mean is `2>4/3`.  Therefore
  grouping/rerooting within one undirected state-tree skeleton is impossible.
- Complementing without reversing arrows creates a zero-rate state edge;
  original vertex reversibility does not make the subset chain bidirected.

## 2026-08-08 02:24 PDT — labelled burst-history lift screened

- Expanded each burst into its target, fair-geometric length, and ordered
  vertex sample sequence.  At regular `K_3`, all degree factors in microscopic
  path reversal disappear.
- Direct exact enumeration of labelled histories by total sample length `M`
  gives

  ```text
  [z^9]  (T_1-2T_2) =   22248,
  [z^10] (T_1-2T_2) = -197532.
  ```

- Rational simplification gives the exact global cancellation

  ```text
  T_1(z)-2T_2(z)
    = 18 z^5 (1-4z) (4z^2-10z+5)^2
      / ((1-z)^5 (1-2z)^5).
  ```

- It vanishes at the fair value `z=1/4`, but is not coefficientwise
  nonnegative.  Hence no two-copy high-to-low labelled-history injection can
  preserve total microscopic-arrow count.  Any viable lift must mix geometric
  lengths or use nonlocal signed cancellation.

## 2026-08-08 02:32 PDT — verifier and note completed

- Added `verify_tree_reflection.py` using exact `Fraction` arithmetic.
- Verified the directed tree cofactors independently on `P_3` and regular
  weighted `K_4`; verified the complete root polynomial on `K_3,K_4`.
- Checked every burst/complement edge formula on `P_3`, regular weighted
  `K_4`, and the frozen six-vertex split witness.
- The actual mean bound passed exactly on those witnesses, four stored
  complementary-level graphs, all 54 connected triangles over
  `{0,1,2,5}`, all 624 connected four-vertex graphs over `{0,1,2}`, and 24
  deterministic sparse/extreme five-vertex graphs.
- **PROVED:** exact transition, tree polynomial equivalence, complement
  out-tree equivalence.
- **EXACTLY FALSIFIED:** edgewise complement domination, same-skeleton
  rerooting, length-preserving labelled-history injection.
- **OPEN:** the global fair-geometric arborescence root-rank inequality, hence
  the universal actual stationary mean bound.
- No external search or contact was performed.  No commit was made.
