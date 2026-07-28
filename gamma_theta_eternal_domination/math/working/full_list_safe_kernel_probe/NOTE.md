# Color-restricted full-list safe kernels

Status: **bounded exact probe complete; equality-case lemma open**.

This note tests a possible intermediate invariant for the parameter-three
proof lane.  It neither resolves the gamma--theta conjecture nor raises the
certified finite frontier.

## Definition

Let \(\mathcal F^\star\) be the greatest one-guard-safe family of dominating
triples of \(G\).  Let \(S\in\mathcal F^\star\) be an independent triple and
let \(x\notin S\) have the full response list
\[
 L_S(x)=S.
\]
Write \(H=\overline G\).  For \(u\in S\), ban
\[
 B_u(S,x)=\{\,S-u+y:y\in N_H(x)\,\},
\]
and let \(\mathcal K_u(S,x)\) be the greatest one-guard-safe family among the
dominating triples outside \(B_u(S,x)\).  Call \(u\) *safe* if both
\(S\) and \(S-u+x\) lie in \(\mathcal K_u(S,x)\).

The candidate equality-case lemma is:

> If \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), every full-list incidence
> \((S,x)\) has a safe \(u\in S\).

The probe does not prove or refute this lemma.

## One proved implication

**Proposition.** If \(\theta(G)=3\), every full-list incidence \((S,x)\)
has a safe \(u\).

**Proof.** Fix a partition of \(V(G)\) into three cliques.  Because \(S\) is
independent, its three vertices occupy distinct cliques.  Let \(u\in S\) be
the anchor in the clique containing \(x\).  The family of all triples having
one vertex in each clique is eternal: an attack is answered inside its
clique by the unique guard there.  This family contains \(S\) and \(S-u+x\).
If \(y\in N_H(x)\), then \(x\) and \(y\) are nonadjacent in \(G\), so \(y\)
cannot lie in the clique of \(x\).  Consequently \(S-u+y\) is not in this
family.  The family therefore avoids every state in \(B_u(S,x)\), and hence
is contained in the greatest restricted kernel \(\mathcal K_u(S,x)\).
Thus \(u\) is safe. \(\square\)

## Exact findings

The positive order-12 control is
`K{eYptMJynEn`, with
\((\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3)\).
At \(S=\{1,2,3\}\), \(x=0\), all three guards are legal responses in
\(\mathcal F^\star\).  Colors 1 and 2 give empty restricted kernels, while
color 3 gives a 64-state kernel containing both required states and exactly
one compatible anchored clique coloring.  Thus the proposed color selection
works nontrivially on this control.

The fixed 56-graph MMV 2022 Table 9 catalog supplies a decisive
counterboundary outside the equality hypothesis.  Among its 55 graphs with
\(\alpha=\gamma^\infty=3\), 54 graphs have 581 full-list incidences:

- 33 incidences have at least one safe color;
- 548 incidences have none;
- all 33 successes occur despite \(\theta=4\).

In particular, MMV-021, graph6 `JEhbtj{rv~?`, has
\((\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,4)\).
For \(S=\{0,1,2\}\), \(x=10\), color 2 yields a 128-state restricted kernel
containing both required states, but the restricted response lists have zero
compatible anchored 3-colorings.  Hence safe-kernel survival does **not**
imply \(\theta=3\) in the natural ambient class
\(\alpha=\gamma^\infty=3\).  The invariant is genuinely weaker than
3-colorability, rather than a disguised coloring assertion.

Conversely, MMV-001, graph6 `IEhbtj{ro}`, has the same parameter pattern
\((2,3,3,4)\), but at \(S=\{0,1,2\}\), \(x=8\), every restricted kernel is
empty.  Safe-kernel survival is therefore not automatic from eternal
domination and a full response list.  These two examples show that
\(\gamma=3\) is potentially the essential extra mechanism.

The remaining named controls reproduce as follows:

| graph | parameters \((\gamma,\alpha,\gamma^\infty,\theta)\) | exact behavior |
|---|---:|---|
| `HCQebjw` | \((3,3,3,3)\) | the advertised static full list contracts to the singleton \(\{1\}\) in \(\mathcal F^\star\); color 1 survives in a 27-state kernel |
| `FDzro` | \((2,3,3,3)\) | both tested full targets admit all three safe colors |
| `G@~~fc` (canonical form of `GFznc{`) | \((2,3,3,3)\) | one greatest-family incidence is full and admits all three safe colors; the second has a singleton list and only that color survives |
| `IFjLBXiow` | \((3,3,4,4)\) | static-only order-10 control; the eternal 3-family is empty, so the candidate lemma does not apply |

An exact scan of all 273,193 connected unlabeled graphs through order 9
found 15 graphs with \(\gamma=\alpha=\gamma^\infty=3\) among the
static-full candidates and 24 static-full incidences.  None remains full in
the greatest eternal family.  Thus the equality-case test is vacuous through
order 9; “no countermodel” there is not evidence for the lemma.

## Assessment

The direction is mathematically live but not yet a proof route.  It has three
useful features:

1. \(\theta=3\) rigorously implies the invariant.
2. The invariant is strictly weaker than \(\theta=3\) once \(\gamma=3\) is
   removed, so proving it in the equality case would not be circular.
3. The order-12 equality control selects one distinguished color exactly as
   hoped.

Two gaps remain.  First, the equality-case candidate lemma itself is open.
Second, even that lemma would not color the remaining restricted family:
MMV-021 demonstrates the precise obstruction.  Repeatedly choosing a
greatest restricted kernel is not a monotone elimination procedure, because
recomputation may reintroduce states banned at earlier choices.  A decisive
proof needs an additional equality-specific argument, likely one using
\(\gamma=3\) to rule out the MMV-021-type obstruction.

All machine-checkable detail is in `result.json`; `probe.py` is an
ordinary-`frozenset` implementation independent of the campaign transition
core.
