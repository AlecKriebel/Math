# Repaired normalized-phase marked-terminal theorem

**Proof-first candidate, 2026-08-12 PDT.**  This note repairs the two
endpoint-bookkeeping defects in the earlier normalized-phase draft.  A
first marked reaction which itself returns to (C=0) is terminal, and the
completed-base spectator guard applies only to a continuing clean
zero-service return.  The proof is orientation-free and uses no population
or reaction-word enumeration.

## 1. Setting and stopping rule

Put

\[
 q=A+C,\qquad
 \{q\}\subseteq{\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,q\}.                         \tag{1.1}
\]

The directed graph is strong and all rate constants are fixed and
positive.  Work in one fixed closed irreducible population class and delete
zero-displacement edges.  This theorem concerns the physical active-loss
branch: at least one cofactor-free complex in
({\cal F}={\cal C}\cap\{0,B,2B\}) is enabled at the entrance, and
({\cal P}={\cal C}\cap\{C,2C,B+C\}) is nonempty.  The complementary
frozen and (A-C)-invariant branches are routed separately.  At a base
(x=(a,b,0)), let

\[
 d=\max\{c:cB\in{\cal C}\},\qquad
 p=\max_{y\in{\cal C}\setminus\{q\}}y_B,                  \tag{1.2}
\]

where the maximum defining (d) is over cofactor-free complexes.  Put

\[
 \epsilon={1+b^p\over a}=e^{-h},\qquad
 \bar\delta=\sqrt\epsilon=e^{-h/2},\qquad h\longrightarrow\infty. \tag{1.3}
\]

For (p=0), read (1+b^p) as (1); then no complex contains (B), so (B) is
constant on the fixed class.  Fix a sufficiently small constant
(c_0>0).  Stop and include the first reaction fired from an open state
whose endpoint crosses

\[
 A\notin[a/2,2a],\qquad
 C\ge c_0\bar\delta a,
 \qquad 1+B^p\ge c_0\bar\delta a\quad(p\ge1).             \tag{1.4}
\]

Call this the open boundary (B_O).  At (C=0), a clean macro begins
with a cofactor-free source and thereafter retains only (q)-sourced
reactions until the first return to (C=0).  If its active loss is
(k=A_0-A_\tau), repeat only clean completed macros with (k=0).  A clean
return with (k\ge1) is terminal service (S).

If a reaction sourced below (q) fires while open, mark the first such
reaction and retain every physical clock thereafter until the next actual
(C=0) return or (B_O).  A return after a mark is terminal (E),
including when the first marked reaction itself lands at (C=0).

Finally, for (p\ge1), a continuing unmarked clean (k=0) return is
terminal base boundary (B_0) if

\[
                  1+B^p\ge {c_0\over2}\bar\delta a.        \tag{1.5}
\]

The priority is: (B_O) first, irrespective of whether its causing reaction
is also a first mark or would complete service; then (S) or (E); only
otherwise apply (B_0).  Thus
(B=B_O\mathbin{\dot\cup}B_0), (S), and (E) are
disjoint, and the base guard never reclassifies a service or marked
endpoint.

## 2. Normalized phase weight

For a complex (y), write

\[
 M_x(y)=\prod_i(x_i+1)^{y_i},\qquad
 {\cal M}(x)=M_x(dB)=(1+B)^d.                              \tag{2.1}
\]

At an open state attach a phase (s): a lower target (z) sets (s=z),
and a lower-to-(q) reaction sets (s=q).  For fixed
(0<\theta<1/2), define

\[
 V_\theta(x,s)=e^{\theta G_\ell(x)}
       \left({{\cal M}(x)\over M_x(s)}\right)^\theta
       \quad(C>0),
 \qquad
 V_\theta(x)=e^{\theta G_\ell(x)}\quad(C=0).               \tag{2.2}
\]

One reaction changes (B) by at most two, so the numerator
({\cal M}) changes by a bounded factor.  If
(r_y=M_x(y)/M_x(q)), the factorial quotient and embedded source
probability give

\[
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 {V_\theta(x+z-y,s')\over V_\theta(x,s)}
 \le
 \begin{cases}
  C r_y^{1-\theta}r_s^\theta,&y\ne q,\\
  C r_s^\theta,&y=q.
 \end{cases}                                               \tag{2.3}
\]

If the reaction lands at a base (jB), then (j\le d).  Resetting to
the raw base weight removes the factor
({\cal M}(x')/M_{x'}(jB)\ge1), so (2.3) remains an upper bound.

Before (1.4), checking the six possible lower monomial ratios gives

\[
        \max_{y\ne q}r_y\le C\bar\delta.                   \tag{2.4}
\]

From a lower phase, the corrected open row is
(O(\bar\delta^\theta)).  From phase (q), one (q)-exit can be free,
but it sets a lower phase; every recurrent lower-to-(q) competitor costs
(O(\bar\delta^{1-\theta})).  With
(eta=\min\{\theta,1-\theta\}), the full physical open kernel (K_{OO}),
killed on its next base return or (B_O), therefore satisfies

\[
 \|K_{OO}^2\|_{V_\theta}\le C\bar\delta^\eta,
 \qquad
 \|(I-K_{OO})^{-1}\|_{V_\theta}\le C.                    \tag{2.5}
\]

This sums arbitrary later lower-source reactions and arbitrary carrier
branching.

## 3. Exact marked-return operator

Let (Q) be the clean physical kernel, killed at (S), (B_O), and
(B_0).  It includes all clean prefixes before the first mark.  The clean
completed-base theorem and the open bridge give

\[
                         \|(I-Q)^{-1}\|_{V_\theta}\le C.   \tag{3.1}
\]

Restrict first to marks whose causing reaction does not cross (B_O), since
a crossing mark belongs to (B_O) by the priority in Section 1.  Split such
a first lower-source mark by its actual endpoint:

\[
                         R=R_B+R_O,                          \tag{3.2}
\]

where (R_B) lands directly at (C=0), while (R_O) remains open.  Let
(T_{OE}) be the physical exit kernel from an open state to its next base
return without first crossing (B_O), and let (T_{O\partial}) be the
complementary included open-boundary exit.  The complete (E)-terminal
operator is

\[
       (I-Q)^{-1}\{R_B+R_O(I-K_{OO})^{-1}T_{OE}\}.          \tag{3.3}
\]

Formula (3.3) is an identity of positive physical kernels for the label
(E).  The crossing-mark kernel and
(I-Q)^{-1}R_O(I-K_{OO})^{-1}T_{O\partial} belong to (B_O) and are
estimated in Section 5.  Thus (3.3) neither drops the causing mark nor
starts a later base macro.  Equation (2.3)
charges the first mark by (C\bar\delta^{1-\theta}); (2.5) controls every
later open reaction.  Both ends of an (E)-path are bases, where (2.2) is
exactly raw.  Therefore

\[
 \boxed{
 \mathbb E_x[e^{\theta(G_\ell(X_\tau)-G_\ell(x))};E]
            \le C\bar\delta^{1-\theta}
            \le C e^{-\eta h/2}.}                          \tag{3.4}
\]

The term (R_B) proves the same estimate without an open resolvent, so a
marked reaction (C\to0) is included exactly.

## 4. Clean service

A clean service has (k\ge1).  If its base target is lower, the first
(q)-step starts from a lower phase and costs
(O(\bar\delta^\theta)).  If its base target is (q), the first exit is
the single free (q)-step, while (k\ge1) forces at least one further
(q)-step from a lower phase and again costs
(O(\bar\delta^\theta)).  Summing the preceding clean base Green and all
intermediate open branching via (2.5) gives

\[
 \boxed{
 \mathbb E_x[e^{\theta(G_\ell(X_\tau)-G_\ell(x))};S]
            \le C\bar\delta^\theta
            \le C e^{-\eta h/2}.}                          \tag{4.1}
\]

More explicitly, the exact completed-return ledger gives
(B_\tau-b\le pk+(d-c)) and the active factorial quotient contributes
(a)_{\underline{k}}^{-1}.  Below the moving tube, after the base
source-degree factor is included, their product is at most
(C e^{-\theta k h/2}).  This is the audited clean service-marked estimate,
and (k\ge1) yields (4.1).  No separate divisor moment is needed because
the normalized weight is raw at the completed endpoint.

## 5. Included boundary

Put

\[
 L=\min\{a,\bar\delta a,
              (\bar\delta a)^{1/p}:p\ge1\}.                 \tag{5.1}
\]

Since (epsilon\ge a^{-1}), one has (L\ge ca^{1/4}).  The entrance is
an (o(1)) fraction of the base guard.  After literal returns are
contracted, every continuing clean (k=0) return changes (B) by at most
two.  The same-exponent clean base kernel has a strict killed contraction
(\rho<1): a maximal-degree nonself return decreases (B), so its raw
factorial ratio costs (O((1+B)^{-\theta})); a positive return sourced at
degree (c<d) has probability (O((1+B)^{c-d})) and bounded rise at most
(d-c), so its probability times raw factorial ratio is
(O((1+B)^{-(1-\theta)(d-c)})).  Literal self-returns have the uniform
strong-cut inverse, and the finite compact killed kernel is absorbed into a
bounded corrector.  Hence reaching (B_0) requires (Omega(L)) continuing
contracted returns and has raw endpoint-weighted mass at most

\[
                              C\rho^{cL}.                    \tag{5.2}
\]

This argument makes no assertion about a long service or marked genealogy:
such paths terminate as (S) or (E) before the base guard is tested.

Every excursion opened below the half guard starts a fixed distance from
the open spectator boundary.  Reaching any component of (1.4) requires
(Omega(L)) bounded open reactions.  Pairing transitions in (2.5), and
summing the bounded clean pre-opening Green, gives corrected endpoint mass

\[
                    C(C\bar\delta^\eta)^{cL/2}.             \tag{5.3}
\]

At the included crossing endpoint every dynamic coordinate is (O(a)).  If
(p=0), the absent spectator (B) is constant on the fixed class, so the same
statement holds with a class-dependent constant.  Moreover

\[
 {e^{\theta G_\ell(X_\tau)}\over V_\theta(X_\tau,s_\tau)}
 =\left({M_{X_\tau}(s_\tau)\over{\cal M}(X_\tau)}\right)^\theta
 \le Ca^{2\theta}.                                         \tag{5.4}
\]

Any fixed polynomial endpoint mark costs only another fixed power of
(a).  Equations (5.2)--(5.4) and (L\ge ca^{1/4}) imply, for every fixed
(N) and fixed nonnegative polynomial (P),

\[
 \boxed{
 \mathbb E_x[e^{\theta(G_\ell(X_\tau)-G_\ell(x))}
              P(X_\tau);B]
                  \le C_{N,P}a^{-N}.}                       \tag{5.5}
\]

The open priority includes a crossing reaction which also lands at
(C=0); its pre-jump path is counted in (5.3), and the raw reset only
improves (5.4).

## 6. Inputs and scope

The proof uses the clean completed-base Green audit at SHA-256
`96c72e11a6105013b8d7b6e2309da7c2dbebccfa0b72640bfb3cfe6cf1608b36`,
the phase-table audit at
`5286d3fbd5d57e92047f8db1339130c228498215bdd23d4d3ebcb1946db26114`,
and the first-mark resolvent at
`d4c4baff29ffda942798f28fc69d4b30ab25ee2c8e13d1960a4ee20b6d772506`.
The normalized multiplication by ({\cal M}(x)^\theta), the direct-base
mark split (3.2)--(3.3), and the terminal priority in Section 1 are proved
here.

This theorem establishes only the raw terminal transforms (3.4), (4.1),
and (5.5).  Physical duration, the invariant/frozen routing, and the
one-sided fourth-power lift are separate audited components.
