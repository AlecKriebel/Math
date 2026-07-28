# Research log: inactive odd-cycle induction

## 2026-07-28

- Read the accepted C-108 target-response propagation theorem, C-112
  inactive suspension theorem, and C-115 private-star and distance-two
  results.  Fixed the scope target: exclude arbitrary inactive odd cycles,
  without claiming the still-open global deletion-coloring extension.
- Tested the proposed scalar two-edge recurrence.  It is false under the
  purely local hypotheses: `probe_recurrence.py` has a seven-vertex
  \(\gamma=2\) control in which the two endpoint states disagree.  This
  prevented an unsound local recurrence from entering the proof.
- Tested exact finite equality controls and witnessed paths.  These
  supported odd path parity but were retained as observations only.
- Built `dead_state_saturation.py`, a sound backward one-guard deletion
  calculus that treats every unspecified graph edge optimistically as an
  available move.  With only the two inactive successor states per witness
  edge forbidden, its surviving local triples were exactly those meeting
  both rim parities.  Forbidding the endpoint triple killed the complete
  kernel at odd path lengths and preserved named states at even lengths.
- Extracted a length-independent human proof from that pattern.  The
  parity-support lemma is a leaf induction with five
  blocked-or-absent-response layers.  The induction uses only the final two
  witness triangles and the prefix parity-support assertion.
- Proved a neutral-replacement lemma and a short endpoint propagation.
  On an odd witnessed path, absence of \(\{r_0,r_n,x\}\) propagates to
  every triple with one rim vertex of each parity and one witness/target
  vertex, contradicting every named witness state.
- Audited repeated witnesses.  Splitting every repeated witness into one
  adjacent true-twin clone per occurrence and lifting every family state
  by all clone choices preserves domination, one-guard closure, named
  independent states, and absent endpoint successors.  Hence the
  distinct-witness proof covers every witness partition.
- Combined the endpoint theorem with the accepted distance-two exclusion.
  For an odd cycle of length \(\ell\), distance two at \(r_{\ell-1}\)
  forbids \(\{r_0,r_{\ell-2},x\}\), while the path
  \(r_0\ldots r_{\ell-2}\) has odd length \(\ell-2\) and forces that same
  state.  This excludes every witnessed inactive odd cycle.
- Derived the equality-critical consequence: under
  \(\alpha(G)=\gamma^\infty(G)=3\) and \(\gamma(G-x)\ge3\), the C-108
  inactive graph \(\overline{G-x}[R_x]\) is bipartite.
- Wrote `verify_induction.py`, independently encoding the five human
  layers rather than importing a search transition core.  The completed
  audit covers all 265 required abstract leaf states, exact path kernels
  through length 25, and product-family parity controls through length 12.
  The canonical result payload hash is
  `26b4b16174f150ac87b97b5b9e48e26b0aca3f66cdfa88f8ae580d2ea931d06f`.
- Scope frozen: inactive bipartiteness does **not** supply a global
  three-coloring of \(\overline{G-x}\) using only two colors on \(R_x\).
  The precoloring/gluing obstruction, the complete \(k=3\) theorem, and
  the universal conjecture remain open.
- Next required action: independent hostile audit of the human induction,
  true-twin lifting, exact cycle-to-path indices, checker independence,
  and non-gluing disclaimer before global claim-ledger promotion.
