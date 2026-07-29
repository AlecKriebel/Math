# Hostile review: higher-rank completion-fan descent

## Verdict

\[
\boxed{\text{UNCONDITIONAL PASS}}
\]

Date: 2026-07-28 (PDT)

Reviewed candidate:

```text
math/working/full_list_higher_rank_fan_descent/
```

The three candidate theorems are correct under their stated hypotheses.
No hidden claim of kernel survival, activity symmetry, complete
parameter three, or resolution of the gamma--theta conjecture was found.

## Proof audit

### Rank convention and deletion witnesses

The convention

\[
\rho(D)=j\iff D\in\Omega_j\setminus\Omega_{j+1}
\]

is used consistently.  If \(z\) witnesses deletion of a rank-\(h\)
state, no unbanned dominating response to \(z\) lies in \(\Omega_h\).
Every retained response in the theorem is dominating and remains
unbanned because a one-guard move from distance two has distance at
least one.  It therefore has a finite rank strictly below \(h\).

The proof does not confuse unrestricted retention in
\(\mathcal F\) with restricted-kernel survival.

### Exact distance formula

The source has neither fixed anchor, so a one-guard response contains at
most one of \(v,t\).  A ban state contains both anchors and one member of
\(B\).  Hence

\[
\delta_{\mathcal B}(D_g)
=3-\mathbf1_{\{z\in\{v,t\}\}}
  -\mathbf1_{\{D_g\cap B\ne\varnothing\}}.
\]

Multiple vertices of \(D_g\cap B\) still contribute only one to the
maximum intersection with a single ban state.  The candidate handles
this correctly.  The rank-two restriction follows immediately from the
Johnson floor: a distance-three retained endpoint would need rank at
least two, contradicting strict descent from \(h=2\).

### Reverse moves, collisions, and occupied attacks

For a response \(D_g=I-g+z\), the reverse attack is at the now
unoccupied vertex \(g\).  The two stationary guards come from the
independent source and miss \(g\); only the inserted guard \(z\) can
move, and it returns exactly to \(I\).  Thus the reverse is physically
unique.

In the minimum completion fan, an attack with neighbor set
\(\{e\}\) is an attack at another member of \(C_{ry}\).  Its unique
response reaches a fan state of rank at least the chosen minimum, so it
cannot delete \(K_e\).  Every other deletion attack is outside the
closed common-nonneighbor set and therefore hits \(r\) or \(y\).
This excludes precisely the empty set and \(\{e\}\), without attacking
an occupied vertex or assuming a fresh witness.

### The “at most 18” classification

The allowed physical neighbor sets are

\[
\{r\},\{y\},\{r,y\},\{r,e\},\{y,e\},\{r,y,e\}.
\]

Their nonempty retained-mover subsets number

\[
1+1+3+3+3+7=18.
\]

The wording “at most 18 formal labeled patterns” is conservative and
correct: the candidate does not claim all patterns are realizable.
For each retained mover, the endpoint contains exactly
\(|A|-1\) incident \(z\)-edges, and C-174 legitimately supplies their
complete retained fans.

### Target split

At \(x\), the \(r\)-guard is ineligible, \(y\) is always eligible, and
\(e\) is eligible exactly when \(e\notin B\).  If
\(C_{ry}\cap B\ne\varnothing\), the common state \(R_x\) is
nondominating, so closure forces every petal \(X_e\).  If the
intersection is empty, either retained \(R_x\) answers every fan state
or its omission forces every \(X_e\).  Domination is never promoted to
family membership.

The reverse attacks at \(y\) and \(e\) are unoccupied and have only the
guard at \(x\) eligible.  The rank conclusion is explicitly conditional
on \(x\) being the selected deletion-witness attack.  Both endpoints
then have distance exactly two because they contain \(r\in B\) and no
ban anchor.

## Independent finite audit

`review_check.py` was written without importing candidate code.  It:

- exhausts all 33,864 labeled graphs of orders three through six;
- independently reconstructs the 2,162 equality graphs, 469,486
  source-form bans, 33,660 higher-rank states, and 100,980 deletion
  exits;
- reproduces the singleton/multi-neighbor split
  \(67{,}140/33{,}840\);
- checks strict rank descent, all unique reverse moves, the distance
  formula, the Johnson floor, and every supported repair fan;
- symbolically checks all 19 unrestricted nonempty \((A,M)\) forms and
  the 18 forms surviving the completion-fan restriction; and
- exhausts the target membership truth table.

It independently decodes `LEhbtnm~D]xln{` and recomputes

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4),
\]

the 200-state greatest triple-family, empty restricted kernel, peeling
layers \(20,53,90,34\), the three deletion attacks, every rank-one
endpoint and repair fan, and target ranks \(3,2\).

The control has four dominating pairs and \(\gamma=2\).  It is used only
as boundary evidence.  It is not treated as an equality instance, a
counterexample, or evidence that the candidate theorem's equality
hypothesis can be dropped.

## Scope after review

The package proves a finite normal form, not an exclusion.  A descending
petal may return uniquely to its higher-rank source without contradicting
synchronous deletion.  The remaining step must couple a lower-rank
petal or hub to another color or to attacked-anchor restoration.
