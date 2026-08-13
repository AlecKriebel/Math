# Pending-entry ledger audit for the frozen nested-carrier candidate

**Audit note, 2026-08-12 PDT.**  This note audits only the pathwise ledger in
Section 2 of
`proof_first_single_linkage_full_all_clock_nested_carrier.md`.  The candidate
itself remains frozen at SHA-256

```text
490f42487ec5045e17a7fa0dc1e69f61f836d17d0ee5ae3ce6af304fc7c230ac
```

No assertion about the later Schur-kernel estimates is made here.

## 1. Exact convention

Write

\[
 q=A+C,
 \qquad
 L={\cal C}\setminus\{q\}
   \subseteq\{0,B,2B,C,2C,B+C\}.
\]

Every complex in \(L\) has \(A\)-coefficient zero, whereas \(q\) has
\(A\)-coefficient one.  Ignore a formal self-loop \(q\to q\), if one is
present: it has zero reaction vector and is neither an entry nor an exit.

Start the episode at \(X_0=(a,b,0)\) with \(D_0=0\).  At each nonterminal
jump update the nonnegative integer ledger by

\[
 D_s=
 \begin{cases}
 D_{s-}+1,&Y_s\in L,\ Z_s=q,\\
 D_{s-}-1,&Y_s=q,\ Z_s\in L,\ D_{s-}>0,\\
 D_{s-},&Y_s,Z_s\in L
              \text{ (or the reaction vector is zero).}
 \end{cases}                                                   \tag{1.1}
\]

Define the surplus-service time by

\[
 \tau_{\rm srv}
 =\inf\{s>0:Y_s=q,\ Z_s\in L,\ D_{s-}=0\}.                    \tag{1.2}
\]

The reaction in (1.2) is included in the physical stopped chain, but the
ledger is **terminated before its update**.  Equivalently, set
\(D_{\tau_{\rm srv}}=\dagger\), not \(-1\).  This convention removes the
ambiguity in the third line of the frozen display (2.1).  It also makes
nonnegativity literal: \(D_s\in\mathbb Z_{\ge0}\) throughout the life of
the ledger.

If \(\sigma\) is an earlier moving-localization terminal time, use
\(\rho=\tau_{\rm srv}\wedge\sigma\).  The same ledger is defined through
the last non-surplus jump at \(\sigma\); no service conclusion is asserted
there.

## 2. Transition-by-transition audit

The possibly delicate lower complexes give the following reaction vectors
and ledger changes:

\[
\begin{array}{c|c|c}
\text{reaction}&\Delta(A,B,C)&\Delta D\text{ before }\tau_{\rm srv}\\ \hline
C\to q &(+1,0,0)&+1\\
2C\to q &(+1,0,-1)&+1\\
B+C\to q &(+1,-1,0)&+1\\ \hline
q\to C &(-1,0,0)&-1\quad(D_{-}>0)\\
q\to2C &(-1,0,+1)&-1\quad(D_{-}>0)\\
q\to B+C&(-1,+1,0)&-1\quad(D_{-}>0).
\end{array}                                                    \tag{2.1}
\]

Thus neither preservation, creation, nor consumption of cofactor \(C\)
affects the active-coordinate ledger.  The remaining entry reactions
\(0,B,2B\to q\) also have \(\Delta A=+1\), and the reverse-direction exits
have \(\Delta A=-1\).  Every lower-to-lower reaction has \(\Delta A=0\)
and leaves \(D\) unchanged.  These categories exhaust the support.

For a \(q\)-exit with \(D_{s-}>0\), (1.1) is well defined even if its target
contains \(C\) and leaves \(q\) immediately enabled.  If that update makes
\(D_s=0\), a later \(q\)-exit is simply the terminal event (1.2).  Therefore
successive enabled exits cannot drive the live ledger below zero.

## 3. Pathwise identity and endpoint

Let \(A_s\) denote the physical active count.  Initially
\(A_0-a-D_0=0\).  Each of the three nonterminal cases in (1.1) leaves
\(A_s-a-D_s\) unchanged.  Induction over jump times therefore proves

\[
                         A_s=a+D_s
 \quad\text{for every }s<\tau_{\rm srv},                    \tag{3.1}
\]

and also at any earlier localization endpoint \(\sigma<\tau_{\rm srv}\)
after its ordinary non-surplus update.

At the service jump, (3.1) gives
\(A_{\tau_{\rm srv}-}=a\), because \(D_{\tau_{\rm srv}-}=0\).  Every
nontrivial \(q\)-exit removes exactly one \(A\), hence the included physical
post-jump state satisfies

\[
                         A_{\tau_{\rm srv}}=a-1.             \tag{3.2}
\]

One may introduce a separate *signed* terminal bookkeeping value
\(\widetilde D_{\tau_{\rm srv}}=-1\) to extend (3.1) algebraically through
the endpoint, but that variable must not be confused with the live
nonnegative pending-entry queue.

Consequently the active factorial increment on a service episode is exactly

\[
 \log(A_{\tau_{\rm srv}}!)-\log(A_0!)=-\log a,               \tag{3.3}
\]

provided \(a\ge1\), as is automatic eventually along a separated sequence.

## 4. Verdict and proposed frozen-file correction

The identity and nonnegativity claim **pass** for all allowed lower sources
and targets, including \(C,2C,B+C\), with one wording correction: a
\(q\)-exit at debt zero is a terminal marked reaction, not an update
\(D^+=0\).  If the frozen candidate is later reopened, replace its third
ledger line by the stopping definition (1.2) and state explicitly that the
physical post-jump endpoint is retained while the ledger is sent to a
cemetery mark.

