# Research log: bridge-chain propagation

## 2026-07-28 (PDT)

- Read the accepted C-079 side-purity theorem, C-124 free-component
  polarization, hostile-passed C-129 first-cross-clause theorem, and the
  hostile-passed anchor-only bridge note and review.
- Tested the tempting claim that the retained shared-color bridge directly
  contracts or continues the original one-clause obstruction.  It does not:
  the C-079 positive witnesses are the opposite terminal singletons, and
  they force every bridge neighborhood in an original supporting component
  onto the marker side.  This gives a proof that all bridge vertices are
  graph-adjacent to both original ports and that an active next clause must
  enter a fresh component.
- Derived the independent turning-ridge lemma.  For a two-list bridge
  \(L(z)=\{u,w\}\), failure of the pair \(\{w,z\}\) produces a retained
  \(G\)-clique
  \(N_{\overline G}(w)\cap N_{\overline G}(z)\).  Outside ridge lists are
  exactly \(\{v\}\) or \(\{u,v\}\).  Both forced edge types are inactive
  under the bridge orientation \(z=w\).
- Exhaustively inspected connected unlabeled equality graphs through order
  nine using the greatest eternal triple-family as a discovery aid.  This
  found the sharp equality controls `FCXfO` and `HEhbtjK`, realizing the
  external singleton and external exact-two turning-ridge alternatives.
  The scan found no full C-129 anchor-only bridge geometry in the greatest
  families tested.  That zero was **not promoted**: a proper eternal
  subfamily may have smaller response lists than the greatest family.
- A separate near-host scan found a gamma-two graph `HCzfRt}` realizing the
  permitted marker-side incidence.  It was useful diagnostically but is not
  needed for the theorem or frozen candidate.
- Implemented `verify.py` without importing any campaign evaluator.  It
  checks both equality controls with ordinary frozensets, explicit
  one-guard successors, greatest-fixed-point deletion, exhaustive graph
  parameters, exact response lists, and all ridge exchanges.

## Frozen candidate boundary

The candidate proves a local propagation gate and a retained turning-ridge
dichotomy.  It does not exclude a shared-color clause entering a fresh
projection component, arbitrary unit chains, lollipops, bicycles, complete
\(k=3\), or the universal gamma--theta conjecture.

## 2026-07-28 hostile-review correction

- The first hostile review returned `PASS_WITH_REQUIRED_LOCAL_CORRECTION`.
- Corrected Theorem 2.1 equation (2.2) to quantify only distinct pairs:
  \(q\in(K_1\cup M_1)-\{z\}\).  The former display accidentally included
  a possible loop when a bridge vertex itself belongs to an opposite side.
- Added the missing proof needed before applying the corrected display to
  the original ports.  If \(z=x\), the literal edge \(xy\in E(H)\)
  contradicts the \(M\)-side purity conclusion because \(y\in M_1\);
  symmetrically \(z=y\) contradicts \(K\)-side purity because \(x\in K_1\).
- Audited downstream uses.  Corollary 2.2 already assumes the literal edge
  \(zr\in E(H)\), hence \(r\ne z\).  The turning ridge uses open
  neighborhoods and explicitly distinct exchange vertices.  No further
  scope correction was required.
- A revised-byte audit found the same self-pair ambiguity once more in the
  informal Section 5 summary.  Replaced “graph-complete to the two original
  sides” by the exact theorem statement: each bridge vertex is
  \(G\)-adjacent to every distinct vertex of those sides, and in particular
  to both original ports.  No theorem display or downstream argument
  changed.
- Reran the standalone verifier byte-for-byte successfully.  The theorem,
  controls, and mathematical scope are unchanged.

Reproduction from the campaign directory:

```text
python3 -I -B -W error math/working/bridge_chain_propagation/verify.py
```
