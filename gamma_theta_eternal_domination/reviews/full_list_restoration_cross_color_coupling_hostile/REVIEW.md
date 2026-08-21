# Hostile review: rebound after attacked-anchor restoration

## Verdict

**UNCONDITIONAL PASS.**

The candidate at commit

```text
e2e8809d0b397bff64d38f70e9ce93f38a1cc75e
```

is correct as stated.  The completion-clique claims, collision handling,
two cross-color survival barriers, and the source-color rank-one exclusion
all follow from the literal one-guard model.  The exact control also
replays independently.

This verdict promotes only the local theorem package.  It does not
eliminate attacked-anchor restoration, prove the full-list branch, prove
complete parameter three, improve the certified finite frontier, or
resolve the gamma--theta conjecture.

The frozen candidate hashes are:

```text
NOTE.md       3abeac165f1ad0830cbced17012d2ef7b2435fc4486a663dc7160d87cf27aeea
MANIFEST.json ebbc2c06c116052a8e1e90d32bd1e7c3d9c39489d7a7c84f2d3ccb87a58cd2fd
```

The candidate strict replay passes byte for byte.

## 1. Model and dependency audit

Every attack used in the proof is made at an unoccupied vertex.  Every
response replaces exactly one occupied guard by the attacked vertex, and
the relevant guard--attack edge is established before the move is used.
Whenever a response is called retained, its membership in the literal
greatest eternal triple-family is either imported from the accepted setup,
forced by eternal closure from a retained predecessor with a physically
unique response, or follows because the endpoint is a maximum independent
triple.

The dependency hashes in the candidate manifest match the repository:

```text
C-165 fc407cb436bfd48f1eb26123cbe02ad1318f4a8a3a8cdee02a48064362261b9d
C-168 3d0e38493159d69b6d790b9614253e02f92ab7acbf5acf7a54dc003f7f10bb87
C-173 4eb6944a766ccb56c0260ad14bfbcdf6ea9b765d371b293f302f35b4519057c4
C-175 378633621b759c31d1b747b0f1a7bd657f17d8b60da9b8356488640e8fbb8f19
C-176 b3aeccda5f44540510559712ee18840560e82646062b1be279afe4f03791d1df
C-176 hostile manifest
      c2096408b4ab4b7ca87fee7bd387d4b528935f1954baee6a30e6589e646e71f5
```

C-171 enters transitively through the fully frozen and hostile-passed
C-176 setup.  C-173 supplies only the Johnson-distance floor, and C-175
supplies only the tight-shell statement for a state attaining that floor.
No new conclusion is hidden in a dependency.

For completeness, the standard maximum-independent-set fact used twice
is valid in the exact attack model.  Starting from any member of an
eternal \(k\)-family, attack the as-yet-unoccupied vertices of an
independent \(k\)-set.  A guard already on that independent set cannot
answer a later such attack, so each response increases its occupancy by
one.  The process ends at the independent \(k\)-set itself.  Hence every
maximum independent triple belongs to every eternal triple-family when
\(\alpha=\gamma^\infty=3\).

## 2. Role and collision audit

The named setup supplies exactly the edges and nonedges used by the new
arguments.  In particular:

- \(r,e\) are nonadjacent because \(e\in C_{ry}\);
- \(p\) missed by \(\{v,t,e\}\) is distinct from \(v,t,e\) and misses all
  three;
- domination of \(p\) by \(D_e=\{r,t,e\}\) forces \(pr\);
- \(p=r\) is therefore impossible, while \(p=u\) remains possible;
- a noncolliding \(f\in C_{pe}-\{t\}\) is distinct from \(p,e,t\);
- \(f\ne v\), because \(ve\) excludes \(v\) from \(C_{pe}\); and
- the named attacks at \(p,v,t,f\) are consequently unoccupied.

No proof step silently assumes \(p\ne u\).  The edge \(pu\) is derived
only after explicitly entering the external branch \(p\ne u\).  In the
collision branch the two-attack ladder ends at \(Z_p=S\), and no loop
\(uu\) is asserted.  Theorem 3.3 remains valid for \(p=u\), because its
extra premise \(p\notin B\) holds for every root color at a full target.

## 3. Audit of the \(e\in B\) branch

Theorem 2.1 is sound.

Since \(r,e\in B=N_{\overline G}(x)\), the target \(x\) misses both.
The definition \(e\in C_{ry}\) says that \(y\) also misses both.  Thus
\(x,y\in C_{re}\), proving nonemptiness without a domination argument.

If \(d,d'\in C_{re}\) were distinct and nonadjacent, then
\(\{r,e,d,d'\}\) would be independent, contrary to \(\alpha=3\).
Therefore \(C_{re}\) is a clique.  Each \(\{r,e,d\}\) is a maximum
independent triple, so it is retained.  At a distinct completion \(d'\),
the guards \(r,e\) miss the attack and only the clique edge \(dd'\) can
answer.  The exchange \(d\to d'\) is physically unique and retained.

The source-ban distance is exactly two, not merely at least two.
The edges \(vr,tr\) exclude the two fixed anchors from \(C_{re}\), so
\(\{r,e,d\}\) contains neither.  A banned triple contains those two
anchors and only one vertex of \(B\), hence it meets the completion state
in at most one token.  It meets the particular banned state
\(\{v,t,r\}\) in \(r\), so the maximum intersection is exactly one and
the Johnson distance is exactly two.  C-173 then gives rank at least one
unless the state lies in the restricted kernel.

The two states at \(d=x,y\) are literally connected in both directions by
the unique completion exchange.  Thus the “reciprocal completion bow tie”
does not rely on interpreting an omitted response as a missing edge.

## 4. Audit of the \(e\notin B\) witness ladder

Let \(p\) be missed by \(R_e=\{v,t,e\}\).

At \(D_e=\{r,t,e\}\), the guards \(t,e\) miss \(p\).  Since \(D_e\)
dominates, \(r\) hits \(p\); consequently \(r\to p\) is the unique
physical answer and eternal closure retains
\(P_e(p)=\{p,t,e\}\).  From this state, \(p,t\) miss \(v\), while \(e\)
hits \(v\), so \(e\to v\) is again physically unique and retains
\(Z_p=\{p,t,v\}\).

When \(p=u\), this is exactly the root.  When \(p\ne u\), domination of
\(p\) by the independent root and the two nonedges \(pv,pt\) force
\(pu\).  The already retained state \(Z_p=S-u+p\) certifies the
\(u\)-palette entry.  The graph nonedges \(pv,pt\), rather than family
omissions, exclude the other two entries.  Therefore the external palette
is exactly \(Q(p)=\{u\}\).

For the color-\(v\) ban, \(Z_p\) contains \(t\) and lacks \(u\).
Every non-\(u\) attack leaves every successor outside that ban.
At \(u\), the only physical responder is \(p\), and it returns to \(S\).
The root is unbanned because the full target is adjacent to \(v\), so
\(v\notin B\).  This proves survival of the first deletion round.  The
color-\(t\) proof is identical, using \(t\notin B\).  These are two
separate positivity statements; no numerical ranks from different bans
are compared.

## 5. Audit of \(C_{pe}\) and the unconstrained \(te\) edge

The pair \(p,e\) is independent.  It cannot dominate because
\(\gamma=3\), so \(C_{pe}\) is nonempty.  Two nonadjacent completions
would create an independent four-set with \(p,e\), so \(C_{pe}\) is a
clique.

The retained state \(P_e(p)=\{p,t,e\}\) dominates every completion.  The
guards \(p,e\) miss each completion by definition.  Hence every
noncolliding completion \(f\ne t\) is adjacent to \(t\), and \(t\to f\)
is the unique response.  The endpoint \(\{p,e,f\}\) is maximum
independent and retained.  This proves both
\(C_{pe}\subseteq N_G[t]\), with the closed-neighborhood convention, and
the claimed fan exchange.

The proof correctly refuses to infer \(te\).  From the independent state
\(\{v,t,p\}\), an attack at \(e\) always has the retained response
\(v\to e\), but \(t\to e\) is an additional physical response exactly
when \(te\) is present.  No theorem step calls this reverse attack unique.
The clean-room control realizes both possibilities: among nineteen
witness incidences, seven reverse attacks have one physical response and
twelve have two.

## 6. Audit of Theorem 3.3

Fix \(p\notin B\) and \(f\in C_{pe}-\{t\}\).  The state
\(I_f=\{p,e,f\}\) contains neither fixed anchor.  The vertices \(p,e\)
are outside \(B\).

If \(f\notin B\), \(I_f\) has no token in common with any source-banned
triple, so its Johnson distance is three.  C-173 directly gives rank at
least two unless it is in the restricted kernel.

Suppose \(f\in B\) and, for contradiction, \(\rho_u(I_f)=1\).  Its
distance is exactly two, so the C-175 tight-shell theorem applies.  A
deletion-witness attack must add one of the fixed anchors \(v,t\), and
every retained response to that attack must have rank zero.

For an attack at \(t\), the fan edge \(ft\) gives the retained response
\[
I_f-f+t=P_e(p).
\]
That endpoint cannot have rank zero: all non-\(v\) attacks have retained
unbanned responses, and the attack at \(v\) uniquely moves \(e\to v\) to
the retained unbanned \(Z_p\).  Thus \(t\) cannot delete \(I_f\).

For an attack at \(v\), the edge \(ev\) gives the physical endpoint
\[
B_f=\{p,f,v\}.
\]
If \(B_f\) were retained, it could not have rank zero.  At every
non-\(t\) attack it has a retained unbanned response, while at \(t\) the
only physical responder is \(f\), and \(f\to t\) reaches retained
unbanned \(Z_p\).  Tight-shell descent therefore rules out retention of
\(B_f\) at the deleting attack.  Importantly, the candidate does **not**
call the omitted \(B_f\) nondominating.

Unrestricted eternal closure of \(I_f\) still requires a retained
response.  The guard \(p\) misses \(v\), so the only remaining possible
responder is \(f\).  Hence \(fv\) is forced and
\[
A_f=\{p,e,v\}
\]
is retained with rank zero.  If \(et\) is absent, \(p,e,v\) all miss
\(t\), contradicting domination of \(A_f\).  If \(et\) is present, then
at \(t\) the unique response \(e\to t\) reaches retained unbanned \(Z_p\);
all other attacks also have retained unbanned responses.  This contradicts
rank zero.  Thus \(v\) cannot delete \(I_f\) either.

Both possible fixed-anchor deletion witnesses are excluded.  The assumed
rank one is impossible, establishing the claimed rank at least two or
kernel alternative.  This argument remains valid when \(p=u\).

## 7. Independent exact replay

`verify_clean.py` imports no campaign code and shares no transition core
with the candidate.  It uses adjacency sets and `frozenset` guard
configurations, constructs the colored configuration graph by direct set
exchange, and recomputes every fixed point and rank synchronously.
Clique cover is checked by direct clique-part assignment rather than the
candidate's complement-coloring routine.

For

```text
OYifur}UO]}iTij]tpo]v
```

the clean-room verifier independently obtains:

- order \(16\), size \(71\);
- \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\);
- literal greatest eternal-family size \(304\);
- \(B=\{5,7,9,11,13\}\);
- restricted kernels \(0,150,0\), with deletion-round sizes
  \((28,81,132,62)\), \((31,74,49)\), and
  \((32,81,128,62)\);
- twelve local outside-\(B\) restoration rows and nineteen witness
  incidences;
- twelve \(p=u\) collisions and seven external singleton palettes;
- for the thirty-eight recipient-color checks, nineteen finite
  positive-rank endpoints and nineteen kernel endpoints;
- nineteen noncolliding completions, all of source rank three;
- eight distance-two completions with their fan vertex in \(B\), and
  eleven distance-three completions with it outside \(B\); and
- seven one-response and twelve two-response reverse attacks, directly
  checking both values of the unconstrained \(te\) edge.

The clean enumerator deliberately recognizes only the restoration-local
rows used in Section 3.  It neither searches for nor asserts the upstream
C-176 rank-one corridor ancestry.  This matches the candidate's stated
scope exactly.

## 8. Scope and frontier

The candidate has found a genuine next layer:

- the \(e\in B\) exit expands to a retained positive-rank completion
  clique;
- an \(e\notin B\) witness returns in two forced attacks to a root swap;
- external witnesses have exact singleton source palette and positive
  status under both recipient bans; and
- outside-\(B\) witnesses cannot immediately reproduce source rank one
  on a noncolliding completion.

None is a contradiction.  The live branches listed by the candidate
remain live: \(C_{pe}=\{t\}\), witnesses \(p\in B\), cross-ban coupling,
and higher-rank fan exits.

Best-guess review completion: **100%**.  Best-guess contribution of this
package toward normalizing attacked-anchor restoration: **55%**.
Best-guess contribution toward a complete parameter-three proof:
**22%**.  These are workload estimates, not probabilities.
