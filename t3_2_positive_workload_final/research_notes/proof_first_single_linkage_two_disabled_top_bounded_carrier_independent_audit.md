# Independent hostile audit: bounded carrier with two disabled mixed tops

**Audit date:** 2026-08-12 PDT  
**Frozen target:**
`proof_first_single_linkage_two_disabled_top_bounded_carrier.md`  
**Target SHA-256:**
`6e560b7bdf6a749aee8b929b9e2fb347a8daa9b0209a40dc5ff173eca7dcdd0f`

## Derivative transfer

The required wording repair in the verdict below has now been applied.  A
full render also exposed the same purely mechanical `amsmath` tag-placement
issue: display (1.5) put its tag on a row inside `aligned`.  The
header-identical publication derivative is frozen at

```text
afd696d3b28709619759936cfb6e4536859300985bb6e594cff840fb4c7db7f9
    research_notes/proof_first_single_linkage_two_disabled_top_bounded_carrier.md
```

The exact diff against the audited target consists only of:

1. adding \(0\in\mathcal C\) to item 2, so items 1--3 are disjoint exactly as
   prescribed below; and
2. moving `\\tag{1.5}` from the third row of the inner `aligned` environment
   to the surrounding display.

Reversing these two changes recovers target SHA `6e560b7b...`.  The
derivative compiles successfully to a four-page PDF with Pandoc and
Tectonic.  No stochastic estimate, stopping rule, event, equation, or proof
step changed, so the mathematical PASS transfers verbatim to SHA
`afd696d3...`.

## Verdict

**MATHEMATICAL PASS.**  The stopped service theorem is valid for every
strongly connected orientation of the stated support and every fixed
positive rate vector.  The proof uses an exact carrier identity, a finite
directed-cut inverse, and exponential-clock races.  It does not require a
support, orientation, or population enumeration.  I found no countergraph,
unpaid physical clock, endpoint-weight failure, or fourth-power sign error.

There is one required publication edit which does not change the
mathematical result.  The words "exactly one" in Theorem 1.1 are literally
false when both \(0\notin\mathcal C\) and
\(\mathcal C\cap\mathcal P=\varnothing\), because the hypotheses of items
1 and 2 then overlap.  The alternatives become disjoint by writing item 2
as

\[
 0\in\mathcal C,qquad \mathcal C\cap\mathcal P=\varnothing,
\]

or by saying that the cases are applied in their displayed order.  Both
conclusions are already true on the overlap, so this is a logical wording
repair rather than a gap in the service argument.

## 1. Exact clean-carrier identity

Write \(L=\{0\}\cup\mathcal P\) and
\(Q=\{q_B,q_C\}\).  At \(x_n=(n,0,0)\), a clean attempt begins with a
\(0\)-source reaction.  If its target is \(y\in Q\), then the state is

\[
                              X=x_n+y.                         \tag{A.1}
\]

As long as the next source is the current \(y\in Q\), a reaction
\(y\to z\) changes (A.1) to \(x_n+z\).  Induction therefore proves the
identity throughout the top phase.  In particular,

\[
 q\to0\quad\Longrightarrow\quad X=x_n,
 \qquad
 q\to p\in\mathcal P\quad\Longrightarrow\quad X=x_n+p.       \tag{A.2}
\]

Thus a failed clean attempt resets *exactly*.  There is no population debt
hidden in the geometric repetition.

Because the complex graph is strong and \(\mathcal P\ne\varnothing\), a
simple path from \(0\) to its first \(\mathcal P\)-vertex exists.  Its
interior vertices lie in \(Q\); after the launch, each next source is
physically present by (A.1).  At a state \(x_n+q_i\), all outgoing
\(q_i\)-clocks share the factor

\[
 (x_n+q_i)^{\underline{q_i}}=n+1.
\]

Their conditional marks hence depend only on the fixed labelled rates.
The simple path has a fixed positive probability.  More generally, the
top-to-top transition matrix on \(Q\) is substochastic, and strong
connectivity rules out a closed class inside \(Q\).  Its absorption time in
\(L\) is phase type and has moments of every order.

Every clean visit to \(x_n\) restarts with an exponential holding time of
fixed rate

\[
 \lambda_0=\sum_{0\to z}\kappa_{0z}>0.
\]

The success probability of one clean attempt is a fixed
\(s\ge p_*>0\).  Consequently the attempt count is geometric and the sum
of the empty-face holding times has every fixed moment.  This verifies the
simple-path/geometric part for arbitrary orientations and rates.

## 2. The post-target top service is uniformly absorbing

Suppose a clean attempt first reaches \(p\in\mathcal P\).  By (A.2), the
state is \(x_n+p\), and \(m=p_B+p_C\in\{1,2\}\).  Until the first
top-to-lower exit, a transition \(q_i\to q_j\) preserves \(A=n\) and
replaces one inactive molecule of type \(i\) by one of type \(j\).  Hence
the top-only dynamics lives on the finite set

\[
 S_m=\{(b,c):b+c=m\},\qquad m\in\{1,2\}.                     \tag{A.3}
\]

At each state in \(S_m\), at least one of \(q_B,q_C\) is enabled and the
aggregate top rate is at least \(cn\).  It remains to check that the finite
chain cannot be trapped by an orientation.  Choose an enabled \(q_i\).
Strong connectivity gives a simple complex path from \(q_i\) to its first
vertex in \(L\).  Before that exit the path uses only \(q_B,q_C\).  Each
top-to-top edge on the path converts the source inactive molecule into the
next source molecule, so the whole path is physically executable from the
current composition.  Since (A.3) is finite and all labelled rates are
positive, the minimum probability of one such bounded exit word is a
strictly positive graph-dependent constant.

It follows that the number \(K\) of cleanup top events is dominated by a
fixed-block geometric variable.  In particular,

\[
                 \mathbb E(1+K)^r\le C_r,
 \qquad
                 \mathbb E T_{\rm top}^r\le C_r n^{-r}.      \tag{A.4}
\]

This supplies the finite-state argument implicit in Section 4 of the
target and verifies its claim for the potentially delicate initial carrier
\(B+C\), where both mixed-top sources are enabled.

At the first top-to-lower reaction \(q_i\to z\in L\), the endpoint has

\[
 A=n-1,qquad
 B+C=m-1+|z|\le2-1+2=3.                                     \tag{A.5}
\]

This also proves directly that all intervening top-to-top conversions leave
the asserted clean endpoint unchanged in the only coordinate relevant to
the entropy gain.

## 3. Restoration of all lower clocks

During a pre-success top phase, (A.1) gives inactive population one.
During cleanup, (A.3) gives inactive population at most two.  Every source
outside \(Q\) is \(0\) or a member of \(\mathcal P\), so throughout every
open top window its aggregate propensity is bounded by a constant \(M\)
depending only on the fixed graph and rates.  The enabled top aggregate is
at least \(cn\).  At one exposed top race,

\[
 \mathbb P\{\hbox{lower source wins}\mid\mathcal F\}
       \le {M\over cn+M}\le {C\over n}.                      \tag{A.6}
\]

Use the clean carrier skeleton only to index the actual races, and stop at
and include the first lower-source winner.  If \(N\) is the geometric
attempt count and \(K_1,\ldots,K_N,K_{\rm cl}\) are the phase-type event
counts, conditioning on this skeleton and applying (A.6) gives, for every
fixed \(r\),

\[
 \mathbb P(E_n)\le {C\over n},
 \qquad
 \mathbb E[(1+N+K_1+\cdots+K_N+K_{\rm cl})^r;E_n]
       \le {C_r\over n}.                                    \tag{A.7}
\]

This weighted form follows because a geometric sum of phase-type variables
has moments of every order.  It is stronger than an unweighted union bound
and is the needed input for the endpoint-and-time estimate.

Neutral attempts reset to \(x_n\).  Before a causing lower jump, the state
therefore differs from \(x_n\) by a single top complex or by an inactive
composition of size at most two.  Both source and target of the included
jump are binary.  Thus \(|X_{\tau_n}-x_n|\) is bounded by a
graph-independent molecularity constant on \(E_n\); it does not grow with
the number of attempts.

The physical elapsed time is a geometric sum of
\(\operatorname{Exp}(\lambda_0)\) empty-face waits and top-window waits.
The latter have the bounds (A.4), and stopping on a competitor only
shortens the corresponding exponential race.  Combining these facts with
(A.7) proves

\[
 \mathbb E(1+\tau_n)^r\le C_r,
 \qquad
 \mathbb E[(1+|X_{\tau_n}-x_n|+\tau_n)^r;E_n]
       \le {C_r\over n}.                                    \tag{A.8}
\]

Hence the target retains every physical clock: the initial \(0\)-clock and
all top-source clocks are designated transitions, while the first firing of
any other enabled clock is the actual included endpoint \(E_n\).

## 4. Entropy and the common fourth power

On \(E_n^c\), (A.5) and the bounded inactive endpoint give

\[
 \Delta G_\ell=-\log n+O_\ell(1).                           \tag{A.9}
\]

On \(E_n\), the endpoint is a bounded displacement from \(x_n\).  A bounded
change of the \(A\)-coordinate changes its factorial entropy by
\(O(\log(n+e))\), while the inactive factorial and linear terms are
bounded.  Equations (A.7)--(A.8) therefore imply

\[
 \mathbb E[|\Delta G_\ell|^r;E_n]
       \le {C_{r,\ell}\log^r(n+e)\over n}.                  \tag{A.10}
\]

Using \(\mathbb P(E_n)=O(n^{-1})\), (A.9), (A.10), and
\(\mathbb E\tau_n=O(1)\) gives

\[
               \mathbb E[\Delta G_\ell+\tau_n]
                    \le-\tfrac12\log n                     \tag{A.11}
\]

for all sufficiently large \(n\).

Let \(G=G_\ell(x_n)\asymp n\log n\).  From (A.9)--(A.10),
\(\mathbb E|\Delta G_\ell|^j=O(\log^j n)\) for
\(j=2,3,4\).  Applying the exact identity

\[
 (G+z)^4-G^4=4G^3z+6G^2z^2+4Gz^3+z^4
\]

and (A.11), the leading term is at most
\(-2G^3\log n+O(G^3)\), whereas the absolute value of all higher terms is

\[
 O(G^2\log^2 n+G\log^3 n+\log^4 n)
       =o(G^3\log n).                                       \tag{A.12}
\]

The additional \(\mathbb E\tau_n=O(1)\) is also lower order.  Thus the
claimed common \(W_\ell\) drift follows with a fixed \(c>0\).

## 5. Frozen and invariant branches

If \(0\notin\mathcal C\), every possible source contains \(B\) or \(C\),
so no reaction is enabled at \(x_n\); its communicating class is an
absorbing singleton.

If \(\mathcal C\cap\mathcal P=\varnothing\), the value of
\(H=A-B-C\) is zero on every complex and is therefore invariant under every
reaction.  On the cofactor-free face \(H(n,0,0)=n\), so a fixed population
class contains at most one such state.  These conclusions remain true on
the harmless overlap noted in the verdict.

## 6. Certification scope

This audit certifies only the frozen bounded two-top theorem at the SHA
above.  It does not certify the separate mesoscopic carrier theorem, the
full single-linkage composition, or the global \(T3\)-\((2)\) theorem.  No
pair-level or global completion flag follows from this audit alone.
