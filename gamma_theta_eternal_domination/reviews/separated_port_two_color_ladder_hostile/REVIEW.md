# Hostile review: separated-port two-color ladder

## Verdict

**PASS on the reviewed bytes.**

The proofs in the target note are valid under their stated hypotheses, the
order bounds are correctly scoped to the **exact nine-vertex induced core
and exact response lists**, and the finite control is independently
reproduced in the standard one-guard-moves model.

This review does not promote the result to a global order bound.  In
particular, it does not eliminate the exact pattern at order thirteen or
higher, does not prove the full \(k=3\) case, and does not resolve the
gamma--theta conjecture.

## Reviewed target

Target commit:

```text
21f5042e6a010db53f759177a0f36d90016cc0ba
```

The target working directory matched that commit byte for byte during the
review.  The pinned source hashes were:

```text
6b9f39e443e99894ffb7490c572149a9ae220ed1d6c445e66df7e0796eec36ff  NOTE.md
abbd420c38d7dc4c851ef888d76f120151f5d5a1047567e42f68d1120c588e00  RESEARCH_LOG.md
a2f5a63f15f6c2808cd190b83fcc07b172eddcca385b679c0cbf92eacb4fb059  verify.py
4faceb740ee28d22db17c8544e21b80e6720a858f637df996250c7859169a1e0  result.json
```

The machine-readable clean-room replay is `evidence.json`; its SHA-256 is

```text
0c66e111583e06404d98e001be5c081e883fe0f5afb72e4bf2b13d38a911a586
```

## Independent proof reconstruction

Throughout, \(H=\overline G\), \(S=\{a,b,c\}\) is an independent
three-guard state, and \(L(v)\) is defined by actual retained direct
responses from \(S\).  I used the accepted C-079, C-082, C-083, and
full-link results only in the directions stated in their source notes.

### 1. Positive-tail link independence

Suppose \(p\in P_a\), \(pq\in E(H)\), and two distinct vertices
\(u,v\in N_H(q)\cap W_a\) satisfy \(uv\in E(H)\).  Then

```text
positive vertex = p
hub            = q
odd W_a path  = u-v
```

is exactly the length-one C-079 fan, with all four vertices distinct.
Hence \(H[N_H(q)\cap W_a]\) is edgeless.

For the exact old core, \(r\in P_a\) and \(rx\in E(H)\), so
\(H[N_H(x)\cap W_a]\) is edgeless.  This step uses list membership
\(r\in P_a\), not an inferred graph edge from a list omission.

### 2. Bow-tie normal form

The full-link no-isolate theorem gives a link neighbor \(p\) of the escape
\(w\):

\[
xp,pw\in E(H).
\]

Because \(w\in W_a\) and the \(W_a\) portion of the link is independent,
\(p\in P_a\).  The previously forced cap \(z\) is \(G\)-complete to every
other \(P_a\)-vertex, so \(zp\in E(G)\).  Also \(xz\in E(G)\).

Since \(\gamma(G)=3\), the pair \(\{z,w\}\) misses some vertex \(t\), so
\(zt,wt\in E(H)\).  The graph edges from \(a\) to \(z\) and from \(x\) to
\(z\) exclude \(t=a,x\).  If an outside \(t\) were in \(P_a\), cap
completeness would contradict \(zt\in E(H)\); hence every outside
completion lies in \(W_a\).

For such an outside \(t\):

- \(xt\in E(H)\) would place the \(W_a\)-edge \(wt\) inside
  \(H[N_H(x)\cap W_a]\), impossible;
- \(pt\in E(H)\) would make the length-one C-079 fan with positive vertex
  \(x\), hub \(p\), and path \(w-t\), impossible.

Thus the only complement edges on \(\{x,p,w,z,t\}\) are

\[
xp,xw,pw,\quad zw,zt,wt.
\]

This is exactly two triangles sharing \(w\).  The five vertices contain no
complement \(K_4\), and every pair among the five has a common complement
neighbor.  The note correctly describes this as a local safe form, not as
a global equality realization.

The anchor-completion subcase is also sound.  Both \(b\) and \(c\) cannot
be common complement neighbors of \(z,w\), because they would form a
complement \(K_4\) with \(z,w\).  If exactly one, say \(h\), is common,
then \(a,h\notin L(w)\), closure at the attack \(w\) from \(S\) forces
the remaining anchor \(d\) into \(L(w)\), and the attack at \(d\) from
the maximum-independent state \(\{h,z,w\}\) forces \(w\to d\).  All
attacks here are unoccupied.

### 3. Exact second-color attack proof

The key Lemma 4.1 was reconstructed without assuming any response list for
the hypothetical vertex \(y\).  Assume

\[
yr,ys,yq\in E(H).
\]

Fullness gives \(D_0=\{b,c,x\}\in\mathcal F\).  The forced attack chain is:

1. Attack the unoccupied \(v_0\) from \(D_0\).  Moving \(x\) gives the
   absent direct state \(S-a+v_0\); closure therefore retains
   \(D_1=\{h,x,v_0\}\) for some \(h\in\{b,c\}\).
2. Attack the unoccupied \(v_1\) from \(D_1\).  The guard \(v_0\) cannot
   traverse the complement edge \(v_0v_1\).  Moving \(x\) gives the
   C-079 dead state \(\{h,v_0,v_1\}\).  Hence closure forces
   \(D_2=\{x,v_0,v_1\}\).
3. Attack the unoccupied \(s\) from \(D_2\).  The three possible
   one-guard successors are all absent:

   - \(\{x,s,v_0\}\) misses \(r\);
   - if \(\{s,v_0,v_1\}\) were retained, attack \(y\): \(s\) cannot
     move, the \(v_0\)-successor misses \(q\), and the
     \(v_1\)-successor misses \(r\);
   - if \(\{x,s,v_1\}\) were retained, attack \(y\): \(s\) cannot move,
     the \(x\)-successor misses \(q\), and the \(v_1\)-successor misses
     \(r\).

The exact old induced edges ensure that \(y\) is unoccupied in both
secondary attacks: \(ys\in E(H)\) gives \(y\ne s\), while
\(sv_0,sv_1,sx\in E(G)\) exclude \(y=v_0,v_1,x\).  Every listed move
changes exactly one guard and every impossible successor is rejected
either because the move edge is absent, the state is known absent, or the
state fails domination.  Therefore no such \(y\) exists.

### 4. Distinct caps and counting

Applying C-082 with omitted color \(c\) to the dynamic complement edges
\(rs\) and \(sq\) gives nonempty outside \(P_c\) cap sets

\[
C_{rs}=N_H(r)\cap N_H(s),\qquad
C_{sq}=N_H(s)\cap N_H(q).
\]

Lemma 4.1 implies:

\[
C_{rs}\cap C_{sq}=\varnothing,\quad
C_{rs}\subseteq N_G(q),\quad
C_{sq}\subseteq N_G(r).
\]

Choose \(y_0\in C_{rs}\) and \(y_1\in C_{sq}\).  The exact old
complement has no old common neighbor for either edge, so both are new.
They are distinct from one another by the disjointness above.  They are
distinct from \(z\) because \(z\) is \(G\)-adjacent to \(r,s,q\).  They
are distinct from \(w\) because cap completeness for color \(c\), applied
to the full vertex \(x\in P_c\), gives \(xy_0,xy_1\in E(G)\), while
\(xw\in E(H)\).  Hence

\[
\{z,w,y_0,y_1\}
\]

is a four-element set disjoint from the exact old nine vertices, proving
the conditional floor \(n\ge13\).

For the final dichotomy, \(xy_1\in E(G)\) and \(\gamma(G)=3\) force a
common complement neighbor

\[
u\in N_H(x)\cap N_H(y_1).
\]

It is outside \(S\) because \(x\) is \(G\)-complete to \(S\).  It lies in
\(W_c\), since any outside \(P_c\)-vertex is \(G\)-adjacent to the cap
\(y_1\).  Among the old vertices, only \(r\) lies in \(N_H(x)\), and
\(ry_1\in E(G)\).  The vertices \(z,y_0\) are also \(G\)-adjacent to
\(x\).  Thus \(u=w\) or \(u\) is a fifth new vertex.  The latter gives
\(n\ge14\); the former gives

\[
L(w)\subseteq\{b\}.
\]

Closure at the unoccupied attack \(w\) from \(S\) makes \(L(w)\)
nonempty, so \(L(w)=\{b\}\).

All distinctness and counting claims therefore pass.  Their scope is
essential: they apply to a realization preserving both the exact induced
old complement (1.6) and the exact lists (1.5).  They do **not** imply a
global \(n\ge13\) or \(n\ge14\) theorem for arbitrary equality graphs.

## Dynamic-list audit

No step in the reviewed proof treats

\[
a\notin L(v)
\]

as \(av\in E(H)\).  The proof uses only the sound implications:

- \(a\in L(v)\Rightarrow av\in E(G)\);
- \(av\in E(H)\Rightarrow a\notin L(v)\);
- omission from a response list implies absence of the corresponding
  direct family state;
- C-079 dead-state consequences for omitted-color vertices.

The potentially delicate deduction \(u\in W_c\) in Corollary 4.3 is also
sound: it uses the actual complement edge \(uy_1\) together with cap
completeness, not the converse of list membership.

## Independent finite replay

The target verifier was first rerun under isolated Python with warnings
fatal.  Its output was byte-identical to the pinned `result.json`.

I then wrote `independent_check.py` without importing the target verifier
or any search implementation.  It uses integer bit masks and:

1. decodes `JFzvvn{~fM?` directly as a Graph6 record for \(G\);
2. reconstructs the fifteen stated complement edges;
3. enumerates dominating configurations;
4. computes the greatest one-guard fixed point after banning exactly the
   forbidden direct swaps;
5. checks every retained state and all unoccupied attacks;
6. independently computes unrestricted kernels for one, two, and three
   guards;
7. checks \(\gamma,\alpha,\theta\), the exact response lists, the bow-tie,
   the empty \(c\)-cap sets, and absence of any C-079 fan embedding.

The clean-room results are:

```text
restricted family states             109
simultaneous deletion rounds          20,4,5,5,2
unoccupied attack obligations         872 = 109*(11-3)
restricted-family SHA-256             34ad69cf11195558c2743fcb6332c2d4cef0750f7eb95be715aa892fd9733eb6
unrestricted kernel sizes k=1,2,3     0,0,148
(gamma,alpha,gamma-infinity,theta)     (2,3,3,3)
```

Each obligation explicitly verifies:

- the attack vertex is not occupied;
- one and only one occupied guard is removed;
- that guard traverses a \(G\)-edge to the attacked vertex;
- the successor belongs to the family and dominates \(G\).

The control is therefore a valid finite positive control for the bow-tie
return and is not a conjecture counterexample because
\(\gamma=2<3=\gamma^\infty\).

## Final assessment

No mathematical or certificate defect was found.  The note correctly
identifies a real stopping boundary: cap-and-escape iteration can close
locally into a parity-compatible bow-tie/even return, while domination
equality forces a second-color layer and the conditional
\(13\)-vertex floor.  The open singleton-\(b\) order-thirteen branch and
longer alternating cycles remain genuine, explicitly stated gaps.

