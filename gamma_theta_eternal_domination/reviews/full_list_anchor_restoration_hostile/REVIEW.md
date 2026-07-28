# Hostile review: rank-zero full-list anchor restoration

## Verdict

\[
\boxed{\textbf{UNCONDITIONAL PASS}}
\]

Candidate reviewed: commit `7a0c7a86`, especially
`math/working/full_list_anchor_restoration/NOTE.md` at SHA-256

```text
fc407cb436bfd48f1eb26123cbe02ad1318f4a8a3a8cdee02a48064362261b9d
```

I find Lemma 2.1, Theorem 2.2, Propositions 3.1 and 3.2, and the stated
sharpness control correct at their exact scope.  The proof uses only
unoccupied attacks and exactly one adjacent moving guard.  It never
converts absence from a family-response palette into a graph nonedge.

This verdict approves a local rank-zero classification and a sharp
obstruction.  It does **not** approve any claim that the full-list branch,
complete \(k=3\), or the universal gamma--theta conjecture has been
settled.

## Frozen inputs and dependency audit

| object | reviewed SHA-256 |
|---|---|
| candidate `NOTE.md` | `fc407cb436bfd48f1eb26123cbe02ad1318f4a8a3a8cdee02a48064362261b9d` |
| candidate `COLLISION_AUDIT.md` | `a5800450e9a6472beaed52c8e99208f5bab8a4933e5903f779d7e65906885bbb` |
| candidate `MANIFEST.json` | `897d092ebbcbd4c2b20fef90789226417a91591dc72b7a3c9487d26192776dce` |
| candidate verifier | `42c204b43f50438d6fae80f23bfbc2e681bc04e80d4ba880d311638accf0de61` |
| C-149 source | `a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d` |
| C-163 source | `e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0` |
| arbitrary-state restoration source | `3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68` |

C-149 and C-163 use the same restricted universe as the candidate:

\[
 \Omega_0=\{\text{dominating triples outside }\mathcal B_u(x)\},
\]

followed by synchronous greatest-fixed-point deletion.  Rank zero means
\(T\in\Omega_0-\Omega_1\).  Thus a deletion-witness attack at a rank-zero
state has no legal successor that is both dominating and unbanned.  It may
still have a retained **banned** successor in the unrestricted greatest
family.  This distinction is preserved throughout the candidate and in the
control.

## 1. Lemma 2.1: primary color and mover externality

Write

\[
 S=\{u,a,c\},\quad
 T=\{c,r,q\},\quad
 E=\{a,c,r\}=S-u+r .
\]

The collision bookkeeping is sufficient:

- \(u,a,c\) are distinct and pairwise nonadjacent because \(S\) is
  independent;
- fullness puts every root anchor adjacent to \(x\), whereas
  \(r\in N_{\overline G}(x)\), so
  \(r\notin S\cup\{x\}\);
- the fact that \(T\) is a three-set gives \(q\ne c,r\);
- the attack at \(a\) is unoccupied, so \(q\ne a\).

Because retained \(E\) dominates its unoccupied vertex \(u\), and \(a,c\)
both miss \(u\), the edge \(ru\) is forced.  Together with
\(E=S-u+r\in\mathcal F^\star\), this is exactly \(u\in Q(r)\).

The only remaining root collision is \(q=u\).  Under that assumption,

\[
 S-T=\{a\},\qquad T-S=\{r\}.
\]

The accepted arbitrary-state restoration lemma therefore gives
\(a\in Q(r)\), including both the edge \(ar\) and retention of
\(S-a+r=T\).  On the named rank-zero attack at \(a\), the move
\(r\to a\) reaches the independent retained root \(S\), which is
dominating and unbanned.  This contradicts the definition of a rank-zero
deletion witness.  Hence \(q\notin S\).

The proof neither states nor needs \(q\ne x\).  This is important: no
unproved collision exclusion is hidden later.

## 2. The attacked/shared palette split

The hypotheses now give \(u\in Q(r)\) and \(|Q(r)|\ge2\), with
\(Q(r)\subseteq\{u,a,c\}\).  Therefore either \(a\in Q(r)\), which is the
attacked-secondary branch, or

\[
 Q(r)=\{u,c\}.
\]

In the latter branch the now-literal set differences are

\[
 S-T=\{u,a\},\qquad T-S=\{r,q\}.
\]

Arbitrary-state restoration says

\[
 \{u,a\}\subseteq Q(r)\cup Q(q).
\]

Since \(a\notin Q(r)\), it follows that \(a\in Q(q)\).  This is a retained
root incidence and therefore also supplies the move edge \(qa\).

The proof uses \(a\notin Q(r)\) only as absence of a family incidence.  It
does not infer \(ar\notin E(G)\); Proposition 3.1 deliberately splits on
that physical edge separately.

## 3. Exact physical alternate and ban test

At the attack \(a\) from \(T\), the root anchor \(c\) cannot move because
\(ca\notin E(G)\), and \(q\) is the selected mover.  The only other
possible guard is \(r\), whose endpoint is

\[
 R=T-r+a=\{a,c,q\}=S-u+q.
\]

Consequently:

- \(R\) is a legal successor exactly when \(ar\in E(G)\);
- because Lemma 2.1 proved \(q\notin S\), \(R\in\mathcal B_u(x)\)
  exactly when \(q\in B=N_{\overline G}(x)\);
- if \(ar\) is an edge and \(q\notin B\), then a dominating \(R\) would
  lie in \(\Omega_0\), contradicting that the named attack deletes \(T\)
  at rank zero.

This proves the three-row table in Proposition 3.1 with no omitted mover
or off-by-one rank convention.

## 4. Proposition 3.2: the two-attack witness ladder

In the shared-secondary branch, \(a\in Q(q)\) gives the retained state

\[
 U=S-a+q=\{u,c,q\}.
\]

Let \(w\) be missed by \(R=\{a,c,q\}\).  The closed-neighborhood
condition already makes \(w\notin\{a,c,q\}\).

- If \(w=u\), then \(uq\) is a graph nonedge directly from the missed
  witness condition.
- If \(w\ne u\), the attack at \(w\) from \(U\) is unoccupied.  Guards
  \(c,q\) miss \(w\), so domination and eternal closure force the unique
  move \(u\to w\) and retain \(\{w,c,q\}\).
- The next attack at \(a\) is also unoccupied.  The guards \(w,c\) miss
  \(a\), while \(qa\) is the edge supplied by \(a\in Q(q)\).  Hence
  \(q\to a\) is unique and retains \(\{w,c,a\}=S-u+w\).

The first move supplies \(uw\in E(G)\); the final family membership then
gives \(u\in Q(w)\).  This is an exact two-attack one-guard ladder.

The externality clause is also exact.  A missed witness is already outside
\(\{a,c,q\}\); fullness makes \(x\) adjacent to \(a\), and the optional
edge \(ar\) makes \(r\) adjacent to \(a\).  Therefore, when \(ar\) is an
edge and \(w\ne u\), the witness lies outside
\(\{u,a,c,q,r,x\}\).  When \(ar\) is absent, the candidate correctly
permits \(w=r\).

## 5. Independent reconstruction of the control

The clean-room checker in this review uses integer masks and imports no
candidate or campaign code.  It decodes and re-encodes

```text
OYifur}UO]}iTij]tpo]v
```

and obtains:

| datum | independent result |
|---|---:|
| order, size | \(16,71\) |
| connected | yes |
| \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \((3,3,3,3,3)\) |
| unrestricted kernels at \(k=1,2,3\) | \(0,0,304\) |
| greatest-family unoccupied attacks | \(3952\) |
| retained response edges | \(4866\) |
| \(B=N_{\overline G}(6)\) | \(\{5,7,9,11,13\}\) |
| restricted kernels for colors \(0,1,10\) | \(0,150,0\) |
| color-0 ranks \(0,1,2,3\) | \(28,81,132,62\) |
| \(Q(6),Q(5),Q(7)\) | \(\{0,1,10\},\{0,10\},\{1,10\}\) |

The exact theta value is certified independently by the exhaustive
calculation \(\alpha=3\), which gives \(\theta\ge3\), together with direct
verification that the three displayed parts in the candidate partition all
are \(G\)-cliques and partition all 16 vertices.

The graph6 round trip succeeds, and the independently serialized edge list
has SHA-256

```text
33c88ce52a0a118df3215fb00507c36da755a6ae9bfa7a812f8b4f2a063ec38b
```

### Attacked-secondary row

For \(u=0,a=10,c=1,r=5,q=7\), the predecessor
\(\{1,5,7\}\) is retained, unbanned, and has restricted rank zero.  At
attack 10 the physical movers are exactly 5 and 7:

- \(7\to10\) reaches the retained banned state \(\{1,5,10\}\);
- \(5\to10\) reaches \(R=\{1,7,10\}\).

Here \(10\in Q(5)\), \(7\in B\), and \(R\) is dominating and banned but
absent from the unrestricted greatest family.  The clean-room peeling
also finds that \(R\) is deleted at unrestricted round zero; this last
rank is additional audit information, not needed by the candidate.

### Shared-secondary row

For \(u=0,a=1,c=10,r=5,q=7\), the predecessor
\(\{5,7,10\}\) is retained, unbanned, and has restricted rank zero.  At
attack 1, the only physical mover is 7:

- \(7\to1\) again reaches \(\{1,5,10\}\);
- \(1\,5\notin E(G)\), so the set \(R=\{1,7,10\}\) is not an alternate
  successor in this row.

The palettes are exactly
\(Q(5)=\{0,10\}\) and \(Q(7)=\{1,10\}\).  Thus the attacked anchor 1 is
absent from the terminal palette and present in the mover palette, exactly
as Theorem 2.2 predicts.  The nonedge \(1\,5\) is decoded directly from
the graph.

The shared predecessor has

\[
 S-T=\{0,1\},\qquad T-S=\{5,7\},
\]

and \(Q(5)\cup Q(7)=\{0,1,10\}\), independently replaying the restoration
inclusion on the control.

## 6. Scope audit

The control proves the advertised sharp boundary:

> Under exact equality, a physically legal, dominating, banned alternate
> at a rank-zero anchor-restoration terminal may be absent from the literal
> greatest eternal family.

It therefore blocks the purely local promotion of that banned alternate.
It does not show that an unbanned lower-rank alternate can fail under the
same conditions, except insofar as earlier C-163 results delimit that
separate branch.

The control has a 150-state safe kernel for color 1.  It is deliberately
not an all-three-empty-kernel example.  Nothing here proves:

- that a restricted kernel survives in every equality graph;
- that rank-zero anchor restoration is impossible;
- that the three color traces are globally incompatible;
- complete \(k=3\); or
- the universal gamma--theta conjecture.

The appropriate next target is exactly the candidate's simultaneous
three-color coupling problem, not a claim of local closure.

## Adversarial checklist

| check | verdict |
|---|---|
| exact C-149/C-163 synchronous rank convention | PASS |
| rank zero distinguished from unrestricted-family deletion | PASS |
| all named vertices and set differences audited | PASS |
| all attacks unoccupied | PASS |
| exactly one adjacent guard moves per transition | PASS |
| Lemma 2.1 proof that \(q\notin S\) | PASS |
| arbitrary-state restoration used in exact family form | PASS |
| attacked/shared secondary split exhaustive | PASS |
| \(R\) banned iff \(q\in B\) | PASS |
| no palette-omission-to-nonedge inference | PASS |
| Proposition 3.2 ladder uniqueness and externality | PASS |
| independent graph6 reconstruction and parameter tuple | PASS |
| unrestricted and restricted greatest kernels | PASS |
| both control rows and common omitted state | PASS |
| scope limited to a sharp local obstruction | PASS |

## Reproduction

Run:

```text
gamma_theta_eternal_domination/reviews/full_list_anchor_restoration_hostile/verify_strict.sh
```

The clean-room JSON output SHA-256 is

```text
20aebfc24690b09c1cede0858d797bdb6c071dd9353e8ea4b40d2a3aaa898d86
```

and the strict runner also replays the candidate's own frozen checker.
