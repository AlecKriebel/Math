# Hostile review: all-\(k\) reverse endpoint domination

## Verdict

Date: 2026-07-28 (PDT)

**UNCONDITIONAL PASS.**

The revised all-parameter theorem is correct in the literal
one-guard-moves model:

> Let \(k\ge1\), let \(i(G)=\alpha(G)=k\), and let \(\mathcal F\) be
> any eternal family of dominating \(k\)-sets.  If
> \(u\mathrel{\triangleright_{\mathcal F}}x\), then
> \(J-x+u\) dominates \(G\) for every maximum independent \(k\)-set
> \(J\) containing \(x\).

Under \(\gamma(G)=\gamma^\infty(G)=k\), equality collapse supplies
\(i=\alpha=k\), so every omitted reverse endpoint of an active
greatest-family exchange has positive finite deletion rank.

The theorem proves domination, not greatest-family retention.  It does
not prove exchange reciprocity, any parameter case of the gamma--theta
conjecture, or the universal conjecture.

## Frozen candidate and dependency

The reviewed candidate is manifest version 2, which explicitly
supersedes the earlier parameter-three draft.

| File | SHA-256 |
|---|---|
| `math/working/reverse_state_domination/NOTE.md` | `3255bcc3d75b8538d6c8e3288f8106b553194bbac1fc3ac590d18ba6d6f81de3` |
| `math/working/reverse_state_domination/RESEARCH_LOG.md` | `108c2d4bf3845ac08dccac45a01b77b99f64023f1c174135167d151d00685c2d` |
| `math/working/reverse_state_domination/MANIFEST.json` | `0f559e88be7653879bb0c7acdc1db6b572e5b96f6819162a9cffe021d1f63375` |
| `math/working/reverse_state_domination/local_core_result.json` | `56db84dcc286534db3a45e72ede337d3cc97e8e865d950a68c9f80650ccda984` |
| `math/working/reverse_state_domination/verify_local_core.py` | `8b8cbb82b6290a4702295d3ed53f9456eaddd8081e86dd4990053e777b891b32` |

The only nontrivial imported theorem is accepted C-108.  Its source
`math/lemmas/general_target_response_propagation.md` has SHA-256
`d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8`.
The candidate uses exactly C-108's family-relative vertex-star
propagation, with target \(x\), shared vertex \(u\), and two retained
independent \(k\)-states avoiding \(x\).

## Independent proof reconstruction

### 1. Every maximum independent state is retained

Let \(M\) be an independent \(k\)-set and start from any state of the
nonempty eternal family \(\mathcal F\).  While some member of \(M\) is
unoccupied, attack it.  Every guard already installed on \(M\) is
nonadjacent to the new target because \(M\) is independent.  Such a
guard cannot move, so eternal closure installs one additional guard on
\(M\) without removing any guard already there.  After at most \(k\)
legal unoccupied attacks, the retained state is \(M\).

Thus every independent \(k\)-set belongs to every eternal \(k\)-family
when \(\alpha(G)=k\).  Greatestness is not used.

### 2. Activity has the required edge and quantifiers

A source \(S\) witnessing
\(u\mathrel{\triangleright_{\mathcal F}}x\) avoids \(x\), the attacked
vertex, and the guard moves along \(ux\in E(G)\).  Equivalently, the
retained successor \(S-u+x\) must dominate the vacated vertex \(u\);
the other guards in the independent source all miss \(u\), again
forcing \(ux\).

Consequently, every independent set containing \(u\) avoids \(x\), and
every independent set containing \(x\) avoids \(u\).  C-108 propagates
the response from \(S\) to every retained independent \(k\)-set
containing \(u\).  This validates the candidate's “some, hence every”
activity language without any occupied-target attack.

### 3. A missed reverse endpoint produces the completion state

For \(k\ge2\), take an arbitrary maximum independent set

\[
J=\{x\}\mathbin{\dot\cup}Q,\qquad |Q|=k-1.
\]

Assume the reverse state \(O=\{u\}\cup Q\) misses \(r\).  Closed
domination makes \(r\notin O\), and

\[
ru\notin E(G),\qquad rq\notin E(G)\quad(q\in Q).
\]

Since \(ux\) is an edge, \(r\ne x\).  The maximum independent set \(J\)
is maximal and hence dominates \(r\).  All members of \(Q\) miss \(r\),
so \(xr\in E(G)\).

Extend the independent pair \(\{u,r\}\) to a maximal independent set.
The exact hypothesis \(i(G)=\alpha(G)=k\) says that its size is \(k\):

\[
I=\{u,r\}\mathbin{\dot\cup}A,\qquad |A|=k-2.
\]

The state \(I\) is retained by Step 1 and avoids \(x\), since \(x\) is
adjacent to both \(u\) and \(r\).  Applying C-108 to the original source
and \(I\), which share \(u\), retains

\[
D=\{x,r\}\mathbin{\dot\cup}A.
\]

No identity has been silently excluded.  The sets in the displayed
disjoint union make \(A\cap\{u,r,x\}=\varnothing\), but \(A\) may
overlap \(Q\) arbitrarily.  The proof tracks that overlap exactly.

### 4. Sequential attacks consume the only possible movers

Let

\[
t=|A\cap Q|,\qquad
m=|A-Q|=k-2-t.
\]

There are

\[
|Q-A|=k-1-t=m+1
\]

unoccupied target vertices.  Attack them in any fixed order.  After
\(j\) successful responses, where \(0\le j\le m\), the state has the
form

\[
\{x,r\}\ \mathbin{\dot\cup}\ (A\cap Q)\
\mathbin{\dot\cup}\ P_j\
\mathbin{\dot\cup}\ B_j,
\]

where \(P_j\subseteq Q-A\) is the set of the \(j\) already attacked
targets and \(B_j\subseteq A-Q\) is the set of \(m-j\) original mobile
guards that have not yet moved.

This invariant starts at \(D\).  For the next target
\(q\in(Q-A)-P_j\):

- \(q\) is unoccupied, because it was neither in \(A\) nor previously
  attacked;
- the guard at \(x\) cannot move, because \(J\) is independent;
- the guard at \(r\) cannot move, because \(r\) is missed by \(O\);
- guards in \(A\cap Q\) and \(P_j\) cannot move, because all lie in the
  independent set \(Q\); and
- there is no guard outside the displayed state, since it already
  contains exactly
  \(2+t+j+(m-j)=k\) guards.

Every legal response must therefore consume one guard from \(B_j\) and
land on \(q\), preserving the invariant with \(j+1\).  The argument does
not assume a unique choice inside \(B_j\): every possible response
decreases its size by exactly one, so branching strategies cannot evade
the count.  A previous responder cannot answer a later attack because
it now occupies a vertex of the independent set \(Q\).

After \(m\) successful attacks, one target remains but \(B_m\) is empty.
The \(k\) guards are \(x\), \(r\), and \(k-2\) vertices of \(Q\), all
nonadjacent to the final target.  The required one-guard response does
not exist, contradicting eternal closure.  Hence \(O\) dominates.

### 5. Boundary values \(k=1\) and \(k=2\)

For \(k=1\), the active source is the singleton \(\{u\}\).  It is a
maximum, hence maximal, independent set and therefore dominates.  For
the only maximum independent set \(J=\{x\}\) containing \(x\), the
reverse state is exactly \(\{u\}\).

For \(k=2\), the completion set \(A\) is empty.  The retained state is
\(D=\{x,r\}\), and \(Q\) has one vertex \(q\).  That vertex is
unoccupied, while both \(xq\) and \(rq\) are nonedges.  The first attack
already has no legal responder.  This is the \(m=0\) endpoint of the
general count, with no negative-size or empty-sequence ambiguity.

Since \(J\) was arbitrary throughout, the conclusion holds for every
maximum independent endpoint containing \(x\).

## Campaign corollary and deletion rank

Under \(\gamma(G)=\gamma^\infty(G)=k\), the accepted parameter chain
gives \(i(G)=\alpha(G)=k\), so the theorem applies to the literal greatest
family \(\mathcal K\).

If \(x\not\mathrel{\triangleright_{\mathcal K}}u\), then \(ux\in E(G)\)
makes every maximum independent set containing \(x\) avoid \(u\), and
C-108 makes every reverse state \(J-x+u\) absent from \(\mathcal K\).
The theorem proves each such state dominating.  The descending kernel
starts from all dominating \(k\)-sets and stabilizes after finitely many
rounds, so every one of these omitted states has positive finite deletion
rank.  The corollary uses greatestness only here.

## Independent computational sanity checks

`independent_local_check.py` imports no candidate or search code.

First, it redoes the complete \(k=3\) local graph audit for the only
possible completion identities \(a=p\), \(a=q\), and fresh \(a\).
The collision cases each leave two base edge assignments and no state
dominating both endpoint vertices.  The fresh case leaves 32 base
assignments; eight make \(D\) dominate both endpoints, and none admits a
one-guard successor at the unoccupied target that dominates the other
endpoint.

Second, it checks every admissible overlap \(0\le t\le k-2\) for
\(1\le k\le256\): 32,640 overlap cases for \(k\ge2\).  In each case the
target count exceeds the available \(A-Q\) guard count by one and guard
conservation leaves exactly \(k\) guards before the final attack.  This
bounded arithmetic loop is a sanity check only; the symbolic identity
\[
|Q-A|-|A-Q|=|Q|-|A|=1
\]
is the all-\(k\) proof.

The candidate's unchanged \(k=3\) checker also replays byte-for-byte to
its recorded result.

Replay from the campaign root:

```text
python3 -I -B -W error \
  reviews/reverse_state_domination_hostile/independent_local_check.py

python3 -I -B -W error \
  math/working/reverse_state_domination/verify_local_core.py
```

## Adversarial checklist

- **Every independent \(k\)-set retained:** pass; the monotone legal
  attack sequence is explicit and starts from the required nonempty
  family.
- **C-108 applicability:** pass; both states are retained, independent,
  avoid \(x\), and share \(u\).
- **Identity and overlap cases:** pass; arbitrary \(A\cap Q\) is tracked
  by \(t\), while all impossible collisions follow from disjoint-set
  statements or \(ux,xr\in E(G)\).
- **Targets unoccupied:** pass; targets lie in \(Q-A\), and prior moves
  land only on prior distinct targets.
- **Exactly one guard moves along one edge:** pass; each family response
  is a single replacement.  All possible movers outside \(A-Q\) are
  excluded by explicit nonedges.
- **Outside and previous responders:** pass; there are exactly \(k\)
  displayed guards, and previous responders lie in independent \(Q\).
- **Adaptive branching:** pass; every allowed branch consumes exactly
  one unused \(A-Q\) guard.
- **Small parameters:** pass; \(k=1\) is separate and \(k=2\) is the
  immediate no-responder case.
- **Graph/complement polarity:** pass; the proof works entirely in
  \(G\), with move edges and missed-state nonedges in the correct
  direction.
- **Greatest-family scope:** pass; unnecessary for the theorem and used
  only for the finite-rank corollary.
- **Resolution scope:** pass; no reverse retention or coloring theorem is
  inferred.

