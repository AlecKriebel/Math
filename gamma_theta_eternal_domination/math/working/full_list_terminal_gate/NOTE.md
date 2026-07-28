# A palette-thin terminal class is impossible

## Status and exact scope

Date: 2026-07-28 (PDT)

This note attacks only the single-full-target terminal gate left by C-149.
It uses the standard one-guard-moves model: an attack is made at an
unoccupied vertex, exactly one occupied guard moves along one edge of
\(G\), and every retained successor lies in the same eternal family.

The new conclusion is:

> If all three color-restricted kernels are empty, their three C-149
> descent certificates cannot all end at link vertices having singleton
> greatest-family root palettes.

This eliminates one complete terminal-pattern class.  It applies
uniformly to direct-root corridors, nonroot corridor diamonds, and
anchor-restoration gates.  Equivalently, among any three terminal traces,
one per color, at least one terminal ban state has a second root response.

It does **not** prove that a restricted kernel survives.  The class in
which all three terminal palettes are non-singleton remains open, as does
the gate-only class in which all three colors have corridor-only descent.
The complete \(k=3\) case and the gamma--theta conjecture remain open.

No literature-priority claim is made.

## 1. Setup

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,\qquad H=\overline G,
\tag{1.1}
\]

let \(\mathcal F^\star\) be the literal greatest eternal family of
dominating triples, and fix an independent triple

\[
 S=\{a,b,c\}\in\mathcal F^\star.
\tag{1.2}
\]

Fix a full target \(x\notin S\):

\[
 S-u+x\in\mathcal F^\star
 \qquad(u\in S).
\tag{1.3}
\]

Put

\[
 B=N_H(x)
\tag{1.4}
\]

and retain the C-141 root-palette notation

\[
 P(z)=L_S^{\mathcal F^\star}(z)
 =\{u\in S:uz\in E(G),\ S-u+z\in\mathcal F^\star\}.
\tag{1.5}
\]

For \(u\in S\), let

\[
 \mathcal B_u(x)=\{S-u+z:z\in B\}
\tag{1.6}
\]

and let \(\mathcal K_u(x)\) be the greatest eternal triple-family outside
this ban.  For one full target, these are exactly the three cumulative
kernels associated with the assignments \(f(x)=u\).

Assume for the terminal analysis that

\[
 \mathcal K_a(x)=\mathcal K_b(x)=\mathcal K_c(x)=\varnothing.
\tag{1.7}
\]

C-149 then gives, for each \(u\), a retained strictly decreasing-rank
trace from \(S-u+x\) whose final state is

\[
 E_u=S-u+r_u\in
 \mathcal F^\star\cap\mathcal B_u(x),
 \qquad r_u\in B.
\tag{1.8}
\]

The final entry can be a direct-root corridor, a nonroot corridor diamond,
or anchor restoration.  The proof below uses only the common terminal
state (1.8), so it covers all three gate forms at once.

## 2. Every retained terminal ban is a positive palette incidence

### Lemma 2.1 — PROVED

For every terminal state in (1.8),

\[
 u\in P(r_u).
\tag{2.1}
\]

#### Proof

The state \(E_u=S-u+r_u\) belongs to \(\mathcal F^\star\) and therefore
dominates the omitted anchor \(u\).  The two anchors in \(S-u\) are
nonadjacent in \(G\) to \(u\), because \(S\) is independent.  Hence
\(r_u u\in E(G)\).  Together with the retained state (1.8), this is
exactly \(u\in P(r_u)\). \(\square\)

This inference uses positive family membership.  No missing response is
converted into a graph nonedge.

## 3. The palette-thin triple is impossible

### Theorem 3.1 (singleton-terminal exclusion) — PROVED

There do not exist three terminal traces as in (1.8), one for each
\(u\in S\), such that

\[
 P(r_a)=\{a\},\qquad
 P(r_b)=\{b\},\qquad
 P(r_c)=\{c\}.
\tag{3.1}
\]

Consequently, if all three kernels in (1.7) are empty, then for every
choice of one C-149 terminal trace per color,

\[
 \boxed{\max_{u\in S}|P(r_u)|\ge2.}
\tag{3.2}
\]

In fact, at least one color has no decreasing-rank terminal trace ending
at a singleton palette of its own color.

#### Proof

Suppose (3.1) holds.  Lemma 2.1 makes the three vertices
\(r_a,r_b,r_c\) distinct.  The three direct states

\[
 D_a=\{r_a,b,c\},\qquad
 D_b=\{a,r_b,c\},\qquad
 D_c=\{a,b,r_c\}
\tag{3.3}
\]

belong to \(\mathcal F^\star\).  Every \(r_u\) lies in
\(B=N_H(x)\), so

\[
 \{r_a,r_b,r_c\}
\tag{3.4}
\]

does not dominate \(x\).

Consider

\[
 D_{ab}=\{r_a,r_b,c\}.
\tag{3.5}
\]

First suppose \(D_{ab}\notin\mathcal F^\star\).  Attack the unoccupied
vertex \(r_b\) from \(D_a\).  The \(b\)-successor is the absent state
\(D_{ab}\).  A response by \(r_a\), if its move edge exists, has successor

\[
 \{r_b,b,c\}=S-a+r_b,
\]

which is absent from the family because \(a\notin P(r_b)\).
Eternal closure therefore forces the \(c\)-successor

\[
 Q=\{r_a,b,r_b\}\in\mathcal F^\star.
\tag{3.6}
\]

Attack the unoccupied anchor \(a\) from \(Q\).  The guard at \(b\) cannot
move because \(ab\notin E(G)\).  The other two possible successors are

\[
 S-c+r_b,\qquad S-c+r_a,
\]

and both are absent from \(\mathcal F^\star\) by (3.1).  Thus \(Q\) has no
retained response, a contradiction.

It remains to suppose \(D_{ab}\in\mathcal F^\star\).  Attack \(r_c\).
Moving the guard at \(c\) gives (3.4), which is not dominating.  Closure
must therefore retain a response by \(r_a\) or by \(r_b\).

If \(r_a\) responds, the successor is

\[
 Q_a=\{r_b,c,r_c\}.
\]

Attack the unoccupied anchor \(b\).  The guard at \(c\) cannot move
because \(bc\notin E(G)\), while the other two candidate successors are

\[
 S-a+r_c,\qquad S-a+r_b.
\]

Both are absent by (3.1), so \(Q_a\) is impossible.

If \(r_b\) responds, the successor is

\[
 Q_b=\{r_a,c,r_c\}.
\]

Attack the unoccupied anchor \(a\).  Again the guard at \(c\) cannot move,
and the remaining candidate successors are

\[
 S-b+r_c,\qquad S-b+r_a,
\]

both absent by (3.1).  Thus \(Q_b\) is also impossible.  Every possible
response to the attack at \(r_c\) has been excluded, a contradiction.

This proves that (3.1) cannot occur.  Equation (3.2) follows by applying
the result to the terminal states of any three selected traces.  If every
color admitted some own-color singleton terminal, selecting one such
trace for each color would recreate (3.1); hence at least one color admits
none. \(\square\)

The only graph nonedges used in this attack tree are the anchor pairs from
the independent state \(S\), and the pairs \(xr_u\) from
\(r_u\in N_H(x)\).  Missing palette entries are used only to exclude
states from \(\mathcal F^\star\).

### Corollary 3.2 (all gate labels covered) — PROVED

Classify each final entry as

\[
 \mathsf D=\text{direct-root corridor},\qquad
 \mathsf C=\text{nonroot corridor diamond},\qquad
 \mathsf A=\text{anchor restoration}.
\tag{3.7}
\]

For every labeled gate triple in

\[
 \{\mathsf D,\mathsf C,\mathsf A\}^3,
\tag{3.8}
\]

the subclass in which the three terminal vertices have respective
palettes \(\{a\},\{b\},\{c\}\) is empty.

#### Proof

Every one of the three gate forms has the same retained terminal state
\(S-u+r_u\).  Theorem 3.1 is independent of the predecessor and final
move, so it applies to all \(3^3\) choices. \(\square\)

This is the promised complete terminal-pattern elimination.  It is a
palette-thin class, not a gate-only class.

## 4. Exact equality sharpness control

The graph

```text
Ksv`f\knJVis
```

with root \(S=\{1,2,3\}\) and target \(x=0\) has

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3).
\tag{4.1}
\]

The independent checker in this directory reconstructs the graph, all
four parameters, the 127-state greatest family, all three restricted
kernels, synchronous deletion ranks, and every terminal entry reachable
from each selected start through a deletion-witness attack and a retained
rank-decreasing response.

For colors \(1\) and \(2\), the kernels are empty.  Their complete
reachable terminal data are

\[
\begin{array}{c|c|c|c|c}
u&\text{predecessor}&r_u&\text{terminal state}&P(r_u)\\ \hline
1&\{2,3,4\}&10&\{2,3,10\}&\{1,2\}\\
1&\{2,3,5\}&11&\{2,3,11\}&\{1,3\}\\
2&\{1,3,7\}&6&\{1,3,6\}&\{2,3\}\\
2&\{1,3,9\}&8&\{1,3,8\}&\{1,2\}.
\end{array}
\tag{4.2}
\]

All four entries are nonroot corridors, and each induced quartet is the
C-149 diamond.  Color \(3\) leaves a 64-state kernel.

Thus equality does not exclude corridor-only annihilation for one color,
or even for two colors simultaneously.  The nonsingleton conclusion in
Theorem 3.1 is also sharp at the two-color boundary.  The control does not
realize three annihilated colors and therefore says nothing against the
open three-color survival statement.

Replay:

```text
python3 -I -B -W error \
  math/working/full_list_terminal_gate/verify_equality_control.py
```

## 5. Separation from C-141 and C-142

C-141 supplies a nonempty global reverse-color set on every physical link
edge and the exact response-row formula in terms of \(P\).  C-142 shows
that reverse membership is insufficient for future safety: in the control
above all three colors are reverse, but colors \(1\) and \(2\) have empty
restricted kernels.

Theorem 3.1 therefore does not select a reverse color and does not infer
kernel survival from one-step incidence.  It uses a different fact: three
annihilation traces would each supply a **retained terminal ban state**.
The attack tree rules out the case in which these three positive terminal
incidences are all palette-singleton.

## 6. Remaining candidate

### CANDIDATE, not proved

The next genuinely gate-sensitive class is:

> all three restricted kernels are empty, and all three selected starts
> have decreasing-rank traces whose reachable terminal entries are
> nonroot corridors with non-singleton terminal palettes.

The equality control realizes exactly two simultaneous colors of this
form, so any proof must use a three-color interaction.  The present note
does not supply that interaction.

### OBSERVED

No computational observation is used as a universal premise.  The finite
control in Section 4 is classified as an exact checked control, not as
evidence that the third kernel must survive in every equality graph.
