# Invariant/no-history routing for the separated carrier

**Standalone proof-first audit, 2026-08-12 PDT.**  This note audits the
invariant/no-history alternative used by the separated completed-return
theorem.  It gives an analytic characterization for every strong orientation
of the support family; it does not enumerate supports, orientations, reaction
words, or population boxes.

The clean completed-base input is
`proof_first_separated_clean_base_green_audit.md`, SHA-256
`96c72e11a6105013b8d7b6e2309da7c2dbebccfa0b72640bfb3cfe6cf1608b36`.
The duration lemma and its independent audit have respective SHA-256 hashes
`504b87e600c382e9c82b88cf0ea88f87a6a4b6c7783202cc9cc2faa79fefc640`
and
`c9be124327288bbb45f42cbb005c9b96d854cfb629f94dd4c7cc61cc456ccb56`.
None of those targets is edited here.

**Verdict: STRICT PASS.**  The routed branch is exhaustive and classwise
sound.  Its two alternatives are an exact stoichiometric invariant and a
physically frozen face.  Neither can contain a divergent separated entrance
reachable in one fixed closed irreducible class.  The complementary branch
has the uniform compact killing/active-loss cut assumed by the clean Green
and duration arguments.

## 1. Exact setting

Put

\[
 q=A+C,
 \qquad
 \{q\}\subseteq {\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,q\},                       \tag{1.1}
\]

and let the directed reaction graph on \({\cal C}\) be strong after
zero-displacement edges are deleted.  Split the lower support into

\[
 {\cal F}={\cal C}\cap\{0,B,2B\},
 \qquad
 {\cal P}={\cal C}\cap\{C,2C,B+C\}.                  \tag{1.2}
\]

At a cofactor-free population \(x=(a,b,0)\), write

\[
 {\cal F}(b)=\{cB\in{\cal F}:b\ge c\}                 \tag{1.3}
\]

for the enabled base sources.  The source \(0\), when present, is enabled
for every \(b\).  All members of \({\cal P}\cup\{q\}\) are disabled at
\(C=0\).

The physical clean trace starts a macro with an \({\cal F}\)-sourced
reaction and, while \(C>0\), retains only \(q\)-sourced reactions.  A lower
source firing while open is a mark and is killed from the clean kernel.  A
completed return with

\[
                         k=A_0-A_\tau\ge1              \tag{1.4}
\]

is strict active service and is also killed.  Included localization
endpoints are killed.  The zero-service completed-base kernel retains only
clean \(k=0\) returns; literal population returns are contracted.

There are two notions which must not be conflated.  When \({\cal P}) is
absent, a physical lower clock can still remove a small amount of mass from
the clean kernel by causing a mark.  What fails is a scale-uniform strong cut:
on a bounded spectator set that mark probability may be only \(O(a^{-1})\).
The exact structural obstruction is absence of strict active loss, not
literal stochasticity of the finite-\(a\) physical kernel.

## 2. The analytic trichotomy

> **Theorem 2.1 (frozen, invariant, or uniformly killed).**  Fix the support,
> strong graph, and positive rate vector in (1.1).  At every cofactor-free
> state \(x=(a,b,0)\), exactly one of the following ordered alternatives
> applies.
>
> 1. **Frozen/no-history:** \({\cal F}(b)=\varnothing\).  No physical
>    reaction is enabled at \(x\), so \(x\) is absorbing.
> 2. **Active invariant:** \({\cal F}(b)\ne\varnothing\) and
>    \({\cal P}=\varnothing\).  The linear functional \(A-C\) is an exact
>    stoichiometric invariant.  Starting from \(x\), the process never has
>    \(A<a\), and every later cofactor-free state has active population
>    exactly \(a\).  In particular strict completed active service is
>    impossible.
> 3. **Physical active-loss branch:** \({\cal F}(b)\ne\varnothing\) and
>    \({\cal P}\ne\varnothing\).  From \(x\), for \(a\ge1\), there is an
>    executable graph-forced history of length at most \(|{\cal C}|\) which
>    reaches \(A=a-1\).  On every fixed spectator compact, that history has a
>    probability bounded below independently of \(a\).  Once its final
>    \(q\)-reaction fires, the zero-service clean kernel must be killed at
>    service, at a mark, or at the included boundary before it can make
>    another \(k=0\) return.
>
> Consequently, failure of the compact uniform killing/active-service cut
> implies Alternative 1 or 2.  Conversely, absence of any strict active-loss
> history from a nonfrozen base is equivalent to \({\cal P}=\varnothing\).

The alternatives are ordered only to remove the harmless overlap between a
frozen state and a support possessing the invariant in Alternative 2.

## 3. Frozen and invariant branches

If \({\cal F}(b)=\varnothing\), every complex in \({\cal F}\) lacks the
required spectator population, and every complex in
\({\cal P}\cup\{q\}\) lacks the required carrier.  Hence every propensity is
zero.  This proves Alternative 1.

Suppose now that \({\cal P}=\varnothing\).  Every complex lies in
\({\cal F}\cup\{q\}\), and the complex values of

\[
                              H=A-C                         \tag{3.1}
\]

are

\[
                       H(y)=0\qquad(y\in{\cal C}).          \tag{3.2}
\]

Therefore for every reaction \(y\to z\),

\[
                       H(z-y)=H(z)-H(y)=0.                  \tag{3.3}
\]

This is an exact pathwise stoichiometric invariant, independent of rates and
orientation.  Starting at \((a,b,0)\), (3.3) says

\[
                              A_t-C_t=a.                    \tag{3.4}
\]

Since \(C_t\ge0\), one has \(A_t\ge a\) at every physical time; at every
later return to \(C=0\), \(A_t=a\).  This proves Alternative 2, including
the stronger assertion that no marked or unmarked physical history can
produce completed active service.

It also explains why a vanishing lower-clock kill cannot substitute for the
invariant routing.  Such a clock may terminate an artificially clean episode,
but the full physical continuation still obeys (3.4) and cannot lower the
active population on the cofactor-free face.

## 4. The graph-forced active-loss history

Assume \({\cal F}(b)\ne\varnothing\) and \({\cal P}\ne\varnothing\).  Choose
an enabled \(f\in{\cal F}(b)\).  Strong connectivity gives a simple directed
path

\[
                    f=y_0\longrightarrow y_1\longrightarrow
                    \cdots\longrightarrow y_r=p,             \tag{4.1}
\]

stopped at its first vertex \(p\in{\cal P}\).  Thus every earlier vertex is
in \({\cal F}\cup\{q\}\), and \(r\le|{\cal C}|-1\).

A directed complex path is a literal executable population history.  After
the first \(i\) reactions in (4.1), telescoping gives

\[
                              x_i=x-f+y_i.                    \tag{4.2}
\]

Because \(f\) is enabled, \(x-f\ge0\), and (4.2) contains the next source
\(y_i\).  Every edge in (4.1) can therefore fire in order.  At its endpoint,

\[
                              x_r=x-f+p,
 \qquad A_r=a,\quad C_r=p_C\ge1.                              \tag{4.3}
\]

The complex \(q\) is enabled at (4.3).  Since the graph is strong and has
more than one vertex, it has a nonself outgoing edge \(q\to z\), with
\(z\ne q\).  Fire that edge.  Only \(q\) contains species \(A\), so

\[
 (x-f+p-q+z)_A-a
        =(p_A-f_A)+(z_A-q_A)=0-1=-1.                         \tag{4.4}
\]

The endpoint is nonnegative: it has \(a-1\) active molecules and carrier
population \(p_C-1+z_C\ge0\).  This proves existence and the length bound in
Alternative 3.  It also proves the converse in the last sentence of Theorem
2.1: when \({\cal P}\) is present an active-loss history exists, whereas
(3.4) forbids one when \({\cal P}\) is absent.

The path (4.1) may cross \(C=0\) several times.  Such crossings simply split
it into a bounded number of completed base trials; they do not affect
executability or the telescoping identity.

## 5. Uniform compact cut for the completed-base kernel

Fix \(R<\infty\) and restrict temporarily to \(b\le R\).  Along (4.1), every
state whose current complex lies in \({\cal F}\) is cofactor-free and has
bounded spectator population.  The chosen edge then has propensity bounded
below by a positive constant, while the total base rate is bounded above by
a constant depending only on \(R\), the graph, and the rates.

At a path state carrying \(q\), (4.2) has \(C=1\), bounded \(B\), and
\(A=a+1\).  Every selected \(q\)-edge has rate of order \(a\); all lower
clocks have bounded aggregate rate.  At (4.3), \(C\le2\), \(B\) is bounded,
and the appended selected \(q\)-edge again has rate of order \(a\).  Thus,
for all sufficiently large \(a\), the conditional probability of every
selected edge in (4.1)--(4.4) is bounded below.  Multiplying at most
\(|{\cal C}|\) fixed factors gives

\[
 \inf_{\substack{a\ge a_R,\ b\le R\\{\cal F}(b)\ne\varnothing}}
 \mathbb P_{(a,b,0)}\{\text{the active-loss gate (4.4) is reached}\}
                         \ge\epsilon_R>0.                    \tag{5.1}
\]

If an open lower source fires instead of a selected \(q\)-edge, the clean
kernel is killed even earlier, so it can only improve the absorption bound.

After (4.4), the accumulated active loss is one.  Every later reaction
retained by the clean open kernel is \(q\)-sourced and lowers \(A\) by one
more.  A lower-to-\(q\) reaction could replenish \(A\), but it is precisely a
mark and is killed.  Therefore the next completed base return has \(k\ge1\),
or a mark/localization occurs first.  If neither a return nor a mark occurs,
repeated \(q\)-firings reach the included lower active boundary after at most
order \(a\) steps.  Hence no continuation of the event in (5.1) can return
mass to the zero-service kernel.

Since (4.1) crosses the base at most \(|{\cal C}|-1\) times, (5.1) is a
fixed-block substochastic contraction of the compact completed-base trace.
It is exactly the compact spectral-radius gap needed by the clean Green and
duration proofs.

## 6. Why there is no second obstruction at large spectator population

Let

\[
                 d=\max\{c:cB\in{\cal F}\}.                  \tag{6.1}
\]

For a clean \(k=0\) completion, the exact ledger gives only

\[
              cB\to jB
       \quad\hbox{or}\quad cB\to q\to jB,
       \qquad c,j\le d.                                      \tag{6.2}
\]

Thus a nonliteral maximal-source completion strictly lowers \(B\), while a
positive \(B\)-move must use a source degree \(c<d\) and has aggregate
probability \(O((1+B)^{c-d})\).  All such jumps are bounded.

The only leading literal block is \(\{dB,q\}\).  When \({\cal P}\ne
\varnothing\), this is a proper subset of the strong graph.  The first edge
leaving it is sourced at \(dB\) or \(q\), so identical-source competition
gives a fixed conditional probability for the cut.  Its target is either
\(jB\) with \(j<d\), which strictly descends, or a member of \({\cal P}\),
which enters the active-loss construction of Sections 4--5.  Literal returns
therefore have a uniform geometric inverse.

These observations give the exterior killed exponential drift recorded in
the clean Green audit: the trace descends toward a compact spectator set or
is absorbed, and lower-degree up-moves cannot form another recurrent leading
class.  If \(\{dB,q\}\) is the whole graph, then \({\cal P}=\varnothing\),
which is exactly the invariant branch already routed in Section 3.

This proves the promised characterization: every failure of the uniform
strong cut is contained in the invariant or frozen alternatives, and the
physical active-loss branch has both the exterior and compact cuts.

## 7. Fixed-class and historical exclusion

Let \(\Gamma\) be one fixed closed irreducible population class and let

\[
                         x_n=(a_n,b_n,0)\in\Gamma             \tag{7.1}
\]

be a separated sequence, so

\[
 h_n=\log{a_n\over m(b_n)}\longrightarrow\infty,
 \qquad m(b_n)\ge1.                                          \tag{7.2}
\]

In particular \(a_n\to\infty\).

On the invariant branch, (3.3) makes \(A-C=h_\Gamma\) constant on the
entire affine stoichiometric class containing \(\Gamma\).  At \(C=0\),

\[
                              a_n=h_\Gamma                   \tag{7.3}
\]

for every \(n\), contradicting (7.2).  Thus a divergent separated sequence
in one fixed class cannot lie in Alternative 2.

On the frozen branch, an absorbing state belonging to a closed irreducible
class forces that class to be its singleton.  Hence \(\Gamma\) cannot contain
two distinct frozen entrances, much less a divergent sequence.  This also
gives the literal no-history statement used in a reflected lift.  If the
lift starts from \((x^\circ,0)\) with

\[
 D_i^+=(D_i+\zeta_i)^+,
 \qquad 0\le D_i\le X_i,                                    \tag{7.4}
\]

then a frozen singleton admits no reaction history at all, so every debt
mark remains zero.  More generally, a fixed physical singleton has only
finitely many admissible marks under (7.4).  It cannot support a historically
reachable divergent positive-debt sequence.

Therefore every historically reachable divergent cofactor-free separated
sequence in one fixed closed irreducible class is eventually in Alternative
3.  No state requiring the separated service theorem is removed by the
invariant/no-history routing.

## 8. Sharpness and publication interface

The invariant exclusion is genuinely needed.  On the strong cycle

\[
                         0\longrightarrow B\longrightarrow q
                         \longrightarrow0,                   \tag{8.1}
\]

one has \({\cal P}=\varnothing\) and \(A-C\) is invariant.  At bounded
\(B\), an open lower-source mark can have probability only \(\Theta(a^{-1})\)
per clean cycle, while a base holding time is order one.  Waiting for that
mark can therefore take order \(a\) physical time.  A false attempt to apply
the killed-branch estimate uniformly would fail.  In one fixed class,
however, (3.4) fixes the cofactor-free value of \(A\), so this example cannot
generate the divergent entrances to which the separated chart is applied.

The exact publication-safe interface is consequently:

1. test whether an \({\cal F}\)-source is enabled at the actual base; if not,
   route to the absorbing/no-history alternative;
2. if \({\cal P}=\varnothing\), cite the exact invariant \(A-C\) and exclude
   separated fixed-class divergence; and
3. otherwise invoke the normalized terminal and physical-duration lemmas on
   the complementary killed branch, whose compact cut is (5.1).

No rate comparison, orientation selection, or historical reachability claim
is left implicit in this routing.
