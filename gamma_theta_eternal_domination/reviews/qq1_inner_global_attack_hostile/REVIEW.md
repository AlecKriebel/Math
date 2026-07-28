# Hostile review: QQ1 cross-layer bridge

Date: 2026-07-28 PDT

## Verdict

**UNCONDITIONAL PASS.**

The cross-layer bridge theorem, its two corollaries, the two fixed
16-vertex controls, their stated parameter data, and the candidate's
scope labels are correct.  I found no mathematical, model, certificate,
or attribution defect.  The result remains a local structural advance:
it does not eliminate QQ1, prove complete \(k=3\), or resolve the
gamma--theta conjecture.

Reviewed candidate commit: `d6302f5a`.

Candidate note SHA-256:
`35c0805312433450a80ebedc33f49ff53d13c6220517639cf9d0f5fa72c84f90`.

Candidate manifest SHA-256:
`fa37576870df738e811f147858febce046ef450510bb1018bfab2e57b0bb716b`.

## Proof audit

### Dependencies and setup

The uses of accepted C-108, C-143, and C-158 have the required
hypotheses.  The equality assumption gives \(i=\alpha=3\).  Thus
\(I=\{x,r,d\}\) is a maximum independent triple and C-143 applies to
the active edge \(u\triangleright x\), proving that
\(O=I-x+u=\{u,r,d\}\) dominates.  C-108 and
\(x\not\triangleright u\) put \(O\) outside the greatest family.  The
proof uses that omission only as a family obstruction; it never turns
it into a graph nonedge.

All possible label collisions were checked:

- \(d\) is distinct from the seven core vertices.  Its nonedges to
  \(x,r\) conflict respectively with the named \(x\)- or \(r\)-edges
  of \(u,p,q,b,c\).
- A hot witness \(w\) is distinct from the core and \(d\): it misses
  \(u,d\), whereas each potential core collision hits one of them.
- A \(W_{ux}\)-witness \(z\) is distinct from the core and from \(w\).
  The only permitted collision is \(z=d\), necessarily in the
  \(ud\)-nonedge branch, and the proof handles it separately.

### Retention of \(A=\{u,x,d\}\)

The attack at the unoccupied vertex \(d\) from retained
\(U=\{u,b,c\}\) has the two side successors
\(\{u,d,c\}\) and \(\{u,b,d\}\).  If \(u\to d\) is graph-eligible, its
successor \(\{d,b,c\}\) misses \(r\); otherwise that branch is absent.
Closure therefore retains a side successor.  From either side
successor, the attack at the unoccupied \(x\) has:

- \(d\) ineligible;
- the \(u\)-successor non-dominating because it misses \(r\); and
- the remaining side guard moving along the named \(bx\) or \(cx\)
  edge to \(A\).

This exhausts all movers and proves \(A\in\mathcal K\).

For \(w\in W_{ud}\), domination by \(A\) forces \(wx\).  Hence the
unoccupied attack at \(w\) from \(A\) has the unique mover \(x\) and
retains \(K_w=\{u,d,w\}\).

### Cross-layer bridge

When \(z=d\), the claimed state is literally \(K_w\); no attack or
distinctness assumption is needed.  Suppose \(z\ne d\).  Domination of
\(z\) by \(A\), together with \(zu=zx=0\), forces \(zd=1\).
At the unoccupied attack \(z\) from \(K_w\):

- \(u\) is ineligible;
- \(d\to z\) gives the desired \(D_{w,z}=\{u,w,z\}\); and
- the only optional alternative is \(w\to z\), giving
  \(C_z=\{u,d,z\}\).

If the desired state were absent, closure would therefore force
\(C_z\) to be retained and would in particular supply the mover edge
\(wz\).  At the unoccupied attack \(r\) from \(C_z\), the complete
response list is:

- \(d\) is ineligible because \(dr=0\);
- \(u\to r\) gives \(\{r,d,z\}\), which misses \(x\); and
- \(z\to r\), when graph-eligible, gives the omitted state
  \(O=\{u,d,r\}\).

Thus \(C_z\) cannot be retained.  Every attack is unoccupied and every
transition replaces exactly one guard along a graph edge.

### Corollaries

The retained bridge dominates \(b,c\), while \(u\) misses both, so each
side vertex is hit by \(w\) or \(z\).  This proves the side-coverage
corollary without asserting a cross edge \(wz\).

In the \(ud\)-edge branch, \(z\ne d\).  If \(wz\) is an edge, the five
cycle edges are
\[
ud,\ dz,\ zw,\ wx,\ xu,
\]
and the five chords \(uz,uw,dw,dx,zx\) are all nonedges.  Hence the
cycle is induced.  If \(wz\) is absent, all three pairs in
\(\{u,w,z\}\) are nonedges, so the bridge is independent.

## Independent fixed-control replay

`independent_verify.py` is a clean-room integer-bitmask implementation.
It imports neither the candidate verifier nor any campaign evaluator.
It independently decodes and re-encodes graph6, exhausts all subsets
for \(\gamma,i,\alpha\), performs literal synchronous one-guard kernel
deletion for \(k=1,2,3\), and obtains \(\theta\) from the exact
\(\alpha=3\) lower bound plus an independently searched three-clique
partition.

For `OslallyN]z~r|^{~|^|~^` it recomputes:

- order \(16\), size \(90\);
- \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3)\);
- greatest kernel sizes \(0,0,371\) for \(k=1,2,3\);
- \(\rho(B)=1,\rho(O)=3\);
- \(W_{ux}=\{9\}\), \(W_{ud}=\{8\}\), and
  \(W_{pw}=\varnothing\);
- outer completion sets \(\{5\}\) and \(\{11\}\), with
  \(\{5,8,11\}\) retained; and
- all 29 dominating pairs, including \(\{2,8\}=\{p,w\}\).

For `OslallyN]fv|y~v^}n}{n` it recomputes:

- order \(16\), size \(87\);
- \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3)\);
- greatest kernel sizes \(0,0,347\);
- \(\rho(B)=1,\rho(O)=3\);
- \(W_{ux}=\{9\}\), \(W_{ud}=\{8\}\), and
  \(W_{pw}=\{15\}\);
- outer completion sets \(\{5\}\) and \(\{15\}\), with
  \(\{5,8,15\}\) retained; and
- all 21 dominating pairs, including \(\{3,14\}=\{q,14\}\).

The output also lists every independent root used to check
\(u\triangleright x\) and \(x\not\triangleright u\), every named
retained state, both complete dominating-pair lists, both clique
partitions, the three rank-one deleting successors and their private
witnesses, side coverage, and the induced \(C_5\).

## Manifest, replay, and scope

Every hash in `CANDIDATE_MANIFEST.json` matches the committed bytes.
Both graph6 string hashes match.  The candidate strict replay succeeds
unchanged.  Discovery SAT and CEGAR traces are consistently labeled
`OBSERVED_DISCOVERY_ONLY`; no UNSAT trace or order coverage is promoted.
The controls are correctly described as \(\gamma=2\) boundary controls,
not conjecture counterexamples.

Reproduce this review from the campaign directory with:

```text
sh reviews/qq1_inner_global_attack_hostile/verify_strict.sh
```
