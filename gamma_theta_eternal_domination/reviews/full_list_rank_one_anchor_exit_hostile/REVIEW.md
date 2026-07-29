# Hostile review: rank-one completion-fan anchor exit

## Verdict: unconditional PASS

Date: 2026-07-28 (PDT)

Frozen candidate: commit `ffb16daa`, directory
`math/working/full_list_rank_one_anchor_exit/`.

The local theorem is correct.  The review reconstructs every restricted
rank-zero survival argument, distinguishes physical successors from
retained successors, verifies that the \(v\)-exit is impossible, proves
that \(y\to t\) is the sole retained response at the surviving exit,
checks the next forced attack and complete alternate table, and verifies
the exact identification with C-165.

The conclusion remains local: it reduces a rank-one second-fan exit to
attacked-anchor restoration.  It does not eliminate that restoration,
produce a safe color, prove complete \(k=3\), or resolve the gamma--theta
conjecture.

## Frozen scope and dependency

The frozen candidate hashes are:

| File | SHA-256 |
|---|---|
| `NOTE.md` | `b3aeccda5f44540510559712ee18840560e82646062b1be279afe4f03791d1df` |
| `RESEARCH_LOG.md` | `3a8594767ec76cca76af3a62fe0b885177b48803f1401ae957069dd4de28092c` |
| `verify_strict.sh` | `07c7c6f3b9f42e1ff690b6ab02367c5d6dee841f13545515b4f2769f0de101f5` |

The candidate invokes the rank-one normal form that is now accepted C-175.
The exact dependency is:

- every deleting attack at \(K_e\) lies in \(\{v,t\}\); and
- every response retained at such an attack has restricted rank zero.

C-175 source SHA-256:
`378633621b759c31d1b747b0f1a7bd657f17d8b60da9b8356488640e8fbb8f19`.
Its hostile-review manifest SHA-256:
`8c4449ca53a0243830750abdad0fc7e67e2b529de9086b6b454c15487a68f0c0`.

No other part of the new forced-move argument is hidden inside C-175.

## Proof audit

### 1. Rank-zero survival barriers

For \(J=\{v,r,y\}\), the state contains \(v\) and lacks \(t\).  At every
unoccupied attack other than \(t\), every one-guard endpoint still lacks
\(t\), hence cannot be one of the banned triples \(\{v,t,b\}\).
Unrestricted closure supplies a retained dominating response, which is
therefore in the restricted initial universe.

At the attack \(t\), the physical move \(r\to t\) reaches the retained
state \(Y=\{v,t,y\}\).  It is unbanned because \(y\notin B\).  Thus \(J\)
survives round one and cannot have rank zero.

Exactly the same argument applies conditionally to the two unwanted
\(t\)-response endpoints:

\[
A_e=\{t,y,e\},\qquad C_e=\{r,y,t\}.
\]

Each contains \(t\) and lacks \(v\).  If retained, every non-\(v\) attack
has a retained unbanned response.  At \(v\), respectively \(e\to v\) and
\(r\to v\) reach the retained unbanned state \(Y\).  Hence neither can be
retained with rank zero.

These arguments use family membership only where stated.  In particular,
they do not infer nondomination or a graph nonedge merely because a
physical endpoint is omitted from the greatest family.

### 2. The \(v\)-attack is impossible

C-175 restricts a deleting attack at the rank-one state
\(K_e=\{r,y,e\}\) to \(v\) or \(t\), and makes every retained response
rank zero.

At attack \(v\), the edge \(ve\) gives the physical response
\[
e\to v,\qquad K_e-e+v=J.
\]
The state \(J\) is retained, but the preceding barrier proves it is not
rank zero.  This contradicts C-175.  Therefore \(v\) cannot delete
\(K_e\).

The attack is unoccupied: \(e\ne v\) because \(vr\) is an edge while
\(e\in C_{ry}\); also \(r,y\ne v\) by the setup.

### 3. The only retained \(t\)-response

At attack \(t\), the guards \(y\) and \(r\) are eligible by \(yt,tr\in
E(G)\); \(e\) may also be eligible.  The three possible endpoints are
exactly
\[
\begin{array}{ccl}
y\to t&:&D_e=\{r,t,e\},\\
r\to t&:&A_e=\{t,y,e\},\\
e\to t&:&C_e=\{r,y,t\}.
\end{array}
\]

They are distinct: \(r,y,e\) are distinct members of the triple \(K_e\),
and \(t\notin K_e\).  Eternal closure retains at least one endpoint.
C-175 assigns rank zero to every retained endpoint, while the two barrier
lemmas rule out retained \(A_e,C_e\).  Therefore \(D_e\) is retained,
has rank zero, and is the unique **retained** response.

The proof correctly leaves \(r\to t\), and possibly \(e\to t\), as
physical moves with omitted endpoints.

### 4. The next attack is forced to \(v\)

The rank-zero state \(D_e=\{r,t,e\}\) contains \(t\) and lacks \(v\).
For any attack other than \(v\), every successor still lacks \(v\), so
every retained response supplied by unrestricted closure is unbanned and
dominating.  Such an attack cannot delete \(D_e\) in round zero.

Since a rank-zero state has at least one deletion-witness attack, that
attack is exactly \(v\).

All occupancies are valid.  The completion definition and named edges
exclude \(e=v,t,r,y\); \(v\) is unoccupied in \(D_e\).

### 5. Exact physical alternate table

At \(v\), the \(t\)-guard is ineligible because the root \(S\) is
independent.  The two and only two eligible guards are \(e,r\), using
\(ve,vr\in E(G)\):
\[
\begin{array}{ccl}
e\to v&:&E=\{v,t,r\},\\
r\to v&:&R_e=\{v,t,e\}.
\end{array}
\]

The first endpoint is retained and banned because \(r\in B\).  The second
is banned exactly when \(e\in B\).  If \(e\notin B\), it is a physical
unbanned endpoint at a rank-zero deleting attack, so it cannot dominate.
This is exhaustive; there is no third mover and no inference from family
omission.

When \(e\in B\), C-175's already reviewed target-fan split applies because
\(e\in C_{ry}\cap B\), giving the reciprocal \(xy\) hinge.  When
\(e\notin B\), the nondominating alternate is the correct conclusion.

### 6. Exact C-165 mapping and palette provenance

The identification
\[
(a,c,r,q)=(v,t,r,e)
\]
maps C-165's rank-zero state \(\{c,r,q\}\) to \(D_e\), its banned endpoint
\(\{a,c,r\}\) to \(E\), its attacked anchor to \(v\), and its selected
mover \(q\to a\) to \(e\to v\).

The terminal palette is nonsingleton:

- \(u\in Q(r)\) follows from \(ur\in E(G)\) and
  \(E=S-u+r\in\mathcal F^\star\);
- \(v\in Q(r)\) is part of the accepted C-171 setup, which chooses
  \(v\in Q(r)-\{u\}\).

The candidate's sentence saying that “the retained terminal \(E\) and the
edges \(ur,vr\) put both colors in the palette” compresses these two
different sources too aggressively: \(E\) certifies the \(u\)-entry, while
the \(v\)-entry comes from C-171's explicit palette choice.  The needed
hypothesis is present, so this is an attribution clarification, not a
proof gap.

Also \(e\notin S\): membership in \(C_{ry}\) excludes \(v,t\) using
\(vr,tr\), and excludes \(u\) using \(ur\).  Thus every C-165 occupancy
condition is met.

## Independent bounded audit

`verify_clean.py` imports no campaign code.  It uses integer masks and
reconstructs domination, one-guard successors, greatest eternal families,
restricted peeling, ranks, and deletion witnesses.

It exhausts:

- every labeled graph of orders three through five;
- every ordered fixed-anchor pair and every nonempty ban region there; and
- the deterministic order-six target-derived slice
  `graph code == 7 (mod 16)`.

The audit covers 162,122 restricted bans, 42,724 distance-two rank-one
states, 83,600 rank-one deleting attacks, 111,772 retained tight-shell
responses, 657,436 one-anchor escape barriers, and 110,846 rank-zero
one-anchor states.

Every rank-one witness was a fixed anchor, every retained response landed
at distance one/rank zero, and every rank-zero \(t\)-only state's deleting
attack was \(v\).  No retained rank-zero endpoint had an escape barrier.
The audit separately found 520 physical but omitted endpoints with an
escape return, directly exercising the crucial physical-versus-retained
distinction.

No full six-role C-171 row occurred in this small bounded census.  That
absence is not used as evidence for the theorem; the theorem is established
by the proof audit above.

## Reproduction

Run:

```sh
./gamma_theta_eternal_domination/reviews/full_list_rank_one_anchor_exit_hostile/verify_strict.sh
```

This replays the frozen candidate, the accepted C-175 review, the
independent census, and every review-file hash.

Best-guess review completion: **100%**.  Best-guess contribution toward
eliminating the full-list rank-preserving escape branch: **35%**.  These
are workload estimates, not probabilities.
