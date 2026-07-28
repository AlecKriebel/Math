# Research log: QQ1 hot-layer endgame

Date: 2026-07-28 (PDT)

- Re-audited the accepted C-158 canonical QQ1 core and the
  completion-dynamics candidate without treating family omissions as
  graph nonedges.
- Found a shorter and stronger replacement for the cold-witness
  argument.  From \(U=\{u,b,c\}\), attack a completion \(d\).  The
  \(u\)-successor misses \(r\), so a side successor survives; its attack
  at \(x\) uniquely reaches \(A=\{u,x,d\}\).  Therefore \(A\) is
  retained.
- Used the forced attack \(A\xrightarrow{x\to w}\{u,d,w\}\) for every
  \(\{u,d\}\)-witness \(w\).  This makes the entire witness set a
  \(G\)-clique and forces one side witness \(b\) or \(c\) to be complete
  to it.
- Separated the \(ud\) branches carefully.  When \(ud\) is absent,
  \(\{u,d,w\}\) is independent and C-108 directly retains
  \(\{x,d,w\}\).  When \(ud\) is present, that shortcut is invalid.
  Instead, complete \(\{u,w\}\) to \(\{u,w,s\}\), move \(u\to x\), and
  use the resulting state's unique attack at \(d\).
- Derived five retained repair corners over every hot witness, with the
  original reverse state \(\{u,r,d\}\) as the sole omitted corner.
- Organized every maximum-independent completion of \(\{u,w\}\) and
  \(\{d,w\}\) into Cartesian bow-tie states.
- Initially found a row-column dichotomy in the \(ud\)-edge branch, then
  eliminated its omitted half by a shorter direct attack.  From
  \(U=\{u,b,c\}\), attack \(r,w,s,t\).  Both possible side branches at
  \(w\) merge at \(\{r,w,s\}\); an omitted mixed bow-tie leaves only
  \(\{r,w,t\}\), which misses \(d\).  Hence every mixed bow-tie is
  retained for either value of \(ud\).
- Audited the collisions \(s=b\) and \(s=c\) separately.  In either
  collision the ineligible side mover at \(w\) forces the opposite side
  mover, and its successor is already \(\{r,w,s\}\); the attack at
  \(s\) is skipped before the same terminal attack at \(t\).
- Derived reciprocal activity between every nondegenerate outer
  completion and its opposite anchor.  The only unsaturated corner is
  still the original reverse state \(\{u,r,d\}\).
- Checked the two C-159 controls independently.  Both stop before the
  new theorem because their pair \(\{u,d\}\) dominates and hence has no
  hot witness.
- Found and froze the exact order-16 retained-edge control
  `Oslally^v{zn{~y~nn~j~`.  It has
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3)\), a 439-state
  greatest triple family, \(W_d=\{w\}\), and every mixed bow-tie
  retained.  Its 34 dominating pairs show exactly why it is only a
  sharp boundary control.
- Remaining obstruction: eliminate the saturated \(ud\)-edge branch
  and the saturated outer layer of the exact \(ud\)-nonedge repair
  square using the full global \(\gamma=3\) condition, or couple either
  branch back to the original rank-one state.
