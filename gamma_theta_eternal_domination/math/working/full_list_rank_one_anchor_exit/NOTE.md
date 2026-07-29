# The rank-one completion fan exits only through anchor restoration

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem awaiting independent hostile review**.  It
continues the trapped rank-zero full-list corridor of accepted C-171 and
the tight-shell normal form in
`math/working/full_list_rank_rebound_iteration/NOTE.md`.

The new conclusion eliminates one of the two anchor attacks left by that
normal form.  If a minimum-rank state in the second completion fan has
rank one, its deleting attack cannot be the secondary anchor \(v\).  It
must be the third anchor \(t\), and the only retained response is
\(y\to t\).  The resulting rank-zero state is exactly an
attacked-anchor restoration of accepted C-165.

This is a local reduction.  It does not eliminate the surviving anchor
restoration, force a restricted kernel, prove complete parameter three,
or resolve the gamma--theta conjecture.

## 1. Setup

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{1.1}
\]

and let \(\mathcal F^\star\) be the literal greatest eternal family of
dominating triples.  Use the accepted C-171 notation

\[
 S=\{u,v,t\},\qquad B=N_{\overline G}(x),
\tag{1.2}
\]

where \(S\) is independent and \(x\) is full at \(S\).  For source color
\(u\), the restricted peeling bans

\[
 \mathcal B_u(x)=\{\{v,t,b\}:b\in B\}.
\tag{1.3}
\]

The trapped rank-zero corridor has retained states

\[
 T=\{v,t,q\},\qquad E=\{v,t,r\},
\tag{1.4}
\]

where \(r\in B\), and C-171 supplies vertices \(w\in B\) and
\(y\notin B\) with

\[
\begin{array}{c|c}
\text{\(G\)-edges}
&xq,qr,ur,uw,vw,tr,yu,yt,yx,vr,\\
\text{\(G\)-nonedges}
&xw,qw,tw,rw,yv,yq,yr,xr .
\end{array}
\tag{1.5}
\]

The states

\[
 Y=\{v,t,y\},\qquad J=\{v,r,y\}
\tag{1.6}
\]

are retained.  The first is the C-171 escape; the second is uniquely
retained by attacking \(y\) from \(E\) and moving \(t\to y\).
Moreover \(u,v\in Q(r)\): the retained terminal \(E=S-u+r\) and the
edges \(ur,vr\) put both colors in the terminal root palette.  Thus the
rank-zero restoration reached below has the nonsingleton palette required
by C-165.

Let

\[
 C_{ry}=V(G)\setminus\bigl(N_G[r]\cup N_G[y]\bigr).
\tag{1.7}
\]

Under (1.1), this is a nonempty \(G\)-clique.  For every
\(e\in C_{ry}\), domination of \(e\) by \(J\) forces \(ve\in E(G)\),
and the unique response

\[
 J\xrightarrow[\text{attack }e]{v\to e}
 K_e=\{r,y,e\}
\tag{1.8}
\]

retains the maximum independent triple \(K_e\).

Assume the color-\(u\) restricted kernel is empty and choose \(e\) with
minimum second-fan rank.  The tight-shell theorem gives the conditional
normal form used below:

> If \(\rho_u(K_e)=1\), every deletion-witness attack at \(K_e\) is
> \(v\) or \(t\), and every retained response to that attack has
> source-color rank zero.

The proof below also uses only the elementary rank-zero fact that a
retained state is not rank zero when every unoccupied attack has a
retained dominating unbanned response.

## 2. One-anchor states with an escape response survive round one

### Lemma 2.1 (escape barrier) — PROVED CANDIDATE

The retained state \(J=\{v,r,y\}\) is not of source-color rank zero.

#### Proof

The state \(J\) contains \(v\) but not \(t\).  For every unoccupied
attack \(a\ne t\), every one-guard successor still lacks \(t\), so no
successor can belong to the ban (1.3).  Unrestricted eternal closure
supplies a retained dominating successor, hence an initial-universe
response.

At the remaining attack \(t\), the edge \(rt\) and (1.6) give the
retained response

\[
 J\xrightarrow{r\to t}Y=\{v,t,y\}.
\tag{2.1}
\]

This response is unbanned because \(y\notin B\).  Thus every attack at
\(J\) has a dominating unbanned response, so \(J\) survives the first
restricted deletion round. \(\square\)

Two analogous states will be needed in the main proof.

### Lemma 2.2 (the other two \(t\)-responses cannot have rank zero)

For \(e\in C_{ry}\), if either

\[
 A_e=\{t,y,e\}
 \quad\text{or}\quad
 C_e=\{r,y,t\}
\tag{2.2}
\]

belongs to \(\mathcal F^\star\), then it is not of source-color rank
zero.

#### Proof

Each displayed state contains \(t\) but not \(v\).  Hence every attack
other than \(v\) has every successor outside the ban, and unrestricted
eternal closure supplies a retained dominating unbanned response.

At the attack \(v\), the state \(A_e\) has the legal response

\[
 e\to v,\qquad
 A_e-e+v=\{v,t,y\}=Y,
\tag{2.3}
\]

because \(ve\in E(G)\).  The state \(C_e\) has the legal response

\[
 r\to v,\qquad
 C_e-r+v=\{v,t,y\}=Y,
\tag{2.4}
\]

because \(vr\in E(G)\).  In both cases \(Y\) is retained and unbanned.
Thus every attack has an initial-universe response, and neither retained
state has rank zero. \(\square\)

No conclusion here treats a nonretained state as nondominating.  The
lemmas apply only under the displayed family-membership hypothesis.

## 3. Exact rank-one exit

### Theorem 3.1 (rank-one fan exit is anchor restoration) — PROVED CANDIDATE

Assume

\[
 \rho_u(K_e)=1
\tag{3.1}
\]

and let \(z\) be a deletion-witness attack at \(K_e\).  Then:

1. the attack is
   \[
   \boxed{z=t};
   \tag{3.2}
   \]
2. among retained responses, the unique response is
   \[
   K_e\xrightarrow{y\to t}D_e=\{r,t,e\};
   \tag{3.3}
   \]
3. the endpoint \(D_e\) has source-color rank zero;
4. every deletion-witness attack at \(D_e\) is \(v\);
5. at that attack, the selected response
   \[
   D_e\xrightarrow{e\to v}E=\{v,t,r\}
   \tag{3.4}
   \]
   is retained and banned, while the only other physical response is
   \[
   D_e\xrightarrow{r\to v}R_e=\{v,t,e\}.
   \tag{3.5}
   \]
   This alternate is banned when \(e\in B\), and is nondominating when
   \(e\notin B\).

Consequently the only rank-one second-fan exit is precisely the
attacked-anchor restoration of C-165 with

\[
 (a,c,r,q)=(v,t,r,e).
\tag{3.6}
\]

If \(e\in B\), the target-crossing theorem additionally makes the edge
\(xy\) reciprocal.  If \(e\notin B\), the restoration has the explicit
nondominating alternate \(R_e\).

#### Proof

The tight-shell normal form restricts \(z\) to \(\{v,t\}\) and says
that every retained response has rank zero.

Suppose first that \(z=v\).  The edge \(ve\) makes

\[
 K_e\xrightarrow{e\to v}J
\tag{3.7}
\]

a retained response.  Tight-shell descent would therefore give
\(\rho_u(J)=0\), contradicting Lemma 2.1.  Hence \(z=t\), proving
(3.2).

At the attack \(t\), the guards \(y,r\) are graph-eligible by (1.5);
the guard \(e\) may also be eligible.  Their possible endpoints are,
respectively,

\[
 D_e=\{r,t,e\},\qquad
 A_e=\{t,y,e\},\qquad
 C_e=\{r,y,t\}.
\tag{3.8}
\]

Eternal closure retains at least one.  Tight-shell descent says every
retained endpoint has rank zero.  Lemma 2.2 rules out retention of
\(A_e\) and \(C_e\).  Therefore \(D_e\) is retained, is the unique
retained response, and has rank zero.  This proves (3.3) and item 3.
The word “unique” concerns retained responses; \(r\to t\) and possibly
\(e\to t\) remain physical moves whose endpoints are not retained.

The state \(D_e\) contains \(t\) but not \(v\).  At every attack other
than \(v\), every successor still lacks \(v\), hence is unbanned.
Unrestricted eternal closure supplies a retained dominating response,
so such an attack cannot witness rank-zero deletion.  Therefore every
deletion-witness attack at \(D_e\) is \(v\).

At \(v\), the guard \(t\) is ineligible because \(S\) is independent.
The guards \(e,r\) are eligible by \(ve,vr\in E(G)\), and their
endpoints are exactly (3.4)--(3.5).  The first endpoint is the retained
banned terminal \(E\).  The second contains the two fixed anchors
\(v,t\), so it is banned exactly when its third vertex \(e\) lies in
\(B\).  If \(e\notin B\), it is an unbanned physical successor.  Since
the attack deletes the rank-zero state \(D_e\), no unbanned dominating
successor exists; hence \(R_e\) is nondominating.

This is exactly C-165's anchor-restoration form under the identification
(3.6).  Finally, \(e\in C_{ry}\cap B\) gives the reciprocal \(xy\)
hinge by the already proved target-crossing exchange, whereas
\(e\notin B\) is the nondominating-alternate case just obtained.
\(\square\)

## 4. Exact frontier

### PROVED in this candidate

- The nominal \(v\)-exit from a rank-one second completion fan is
  impossible.
- The only retained \(t\)-response is \(y\to t\), and it lands at rank
  zero.
- The next deletion is forced at \(v\), giving exactly an
  attacked-anchor restoration.
- The restoration ends either in a banned alternate with a reciprocal
  \(xy\) hinge, or in an unbanned nondominating alternate.

### OPEN

- Eliminate the attacked-anchor restoration itself.
- Couple the reciprocal \(xy\) branch or the nondominating-alternate
  branch across all three source colors.
- Prove a surviving restricted kernel, complete parameter three, or the
  universal gamma--theta conjecture.
