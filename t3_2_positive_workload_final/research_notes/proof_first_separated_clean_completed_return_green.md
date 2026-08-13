# Clean completed-return Green theorem for the separated carrier

**Proof-first clean-kernel theorem, 2026-08-12 PDT.** This note proves the
clean completed-return estimate used by the first-mark resolvent. It does
not restore open lower-source clocks, estimate physical duration, or lift
to \(W_\ell=G_\ell^4\). No support, orientation, or population enumeration
is used. No certification flag is changed.

The proof corrects two earlier shortcuts. A long \(q\)-branch is paid using
the largest localized spectator scale along the branch, not its entrance
value. Also, no unweighted scale-relative terminal \(B\)-moment is claimed;
such a moment is false for critical branching examples. Divisor powers are
instead carried as service marks and absorbed by the service exponent.

## 1. Clean macros

Let

\[
 q=A+C,\qquad
 \{q\}\subseteq{\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,q\}.                              \tag{1.1}
\]

Put

\[
 {\cal F}={\cal C}\cap\{0,B,2B\},\qquad
 d=\max_{cB\in{\cal F}}c,\qquad
 p=\max_{y\in{\cal C}\setminus\{q\}}y_B.                     \tag{1.2}
\]

If no member of \({\cal F}\) is enabled, the cofactor-free state is
frozen. Otherwise \(0\le d\le p\le2\). Binary molecularity gives

\[
                         p=2\quad\Longrightarrow\quad d=2,   \tag{1.3}
\]

because \(2B\) is the only binary complex of \(B\)-degree two.

At a cofactor-free base write

\[
                  X_0=(A,u,0),\qquad A=a+D,\quad D\ge0.       \tag{1.4}
\]

A clean macro consists of one reaction sourced at \(cB\in{\cal F}\),
followed, while \(C>0\), only by \(q\)-sourced reactions, and ending at the
first return to \(C=0\). It is killed instead if service or a declared
localization occurs. Throughout a completed localized macro assume

\[
 A_t\ge a/2,\qquad B_t\le L,\qquad
       {C_0(1+L)^p\over a}\le e^{-h_*},\qquad
                              h_*\longrightarrow\infty,      \tag{1.5}
\]

where \(C_0\) absorbs fixed rates, bounded reaction increments, and the
fixed linear correction. In the moving separated chart \(L\) is chosen so
that \(h_*\ge c h(a,u)-C\).

The ideal clean law normalizes the \(q\)-clock after suppressing open lower
clocks. The substochastic physical clean kernel is pointwise dominated by
this law, so an upper Green estimate for the ideal law also applies to the
physical clean kernel in the decomposition \(K=Q+R\).

## 2. Exact stoichiometric ledger

Let \(z_0\) be the target of the base reaction. Put \(e=1\) if
\(z_0=q\), and \(e=0\) otherwise. If the macro opens, let \(T\) be the
number of nontrivial \(q\)-reactions before the cofactor-free return. Put

\[
                         k=A_0-A_\tau=T-e.                    \tag{2.1}
\]

### Lemma 2.1 (completed-return balance)

Every completed clean macro obeys

\[
                         k\ge0,\qquad
                         B_\tau-u\le pk+(d-c).                \tag{2.2}
\]

#### Proof

If the base target is cofactor-free, \(T=e=0\), \(k=0\), and its
\(B\)-degree is at most \(d\), so (2.2) is immediate.

Suppose the macro opens. The base reaction creates one \(A\) exactly when
its target is \(q\), whereas every later nontrivial \(q\)-reaction consumes
one \(A\). A completed return has \(T\ge1\), hence \(T-e\ge0\).

For each lower target \(z\neq q\), let \(n_z\) count the \(q\to z\)
reactions. Cofactor and spectator balance give

\[
 0=(z_0)_C+\sum_z n_z(z_C-1),\qquad
 B_\tau-u=-c+(z_0)_B+\sum_z n_zz_B,                           \tag{2.3}
\]

and \(T=\sum_zn_z\). Every displayed \(B\)-degree is at most \(p\).

If \(p=d\), then for \(e=0\),

\[
 (z_0)_B+\sum_zn_zz_B\le d+pT=p(T-e)+d,                      \tag{2.4}
\]

while for \(e=1\), \(z_0=q\) has \(B\)-degree zero and

\[
                 \sum_zn_zz_B\le pT=p(T-e)+d.                \tag{2.5}
\]

These give (2.2). By (1.3), the only possible case \(p>d\) is
\(p=1,d=0\). Then \({\cal F}=\{0\}\), and \(B+C\) is the only possible
target containing \(B\). The last \(q\)-reaction of every completed return
has target \(0\), so it creates no \(B\). If \(e=1\), at most
\(T-1=k\) targets are \(B+C\). If \(e=0\), the base target and the first
\(T-1\) nonterminal \(q\)-targets contain at most \(T=k\) copies of
\(B+C\) in total. Thus (2.2) also holds in the last case. \(\square\)

This balance retains arbitrary \(q\)-branching and uses only binary
molecular degree.

## 3. Source normalization and the completed tilt

At a large base, the total base rate is comparable with \((1+u)^d\).
Thus a macro sourced at \(cB\) has probability at most

\[
                         C(1+u)^{c-d}.                        \tag{3.1}
\]

For fixed \(0<\theta<1/4\), put

\[
 \Phi_\theta(A,u)
       ={e^{\theta G_\ell(A,u,0)}\over(1+u)^{d\theta}}.       \tag{3.2}
\]

### Lemma 3.1 (completed-macro tilt)

For a completed macro sourced at \(cB\), with active loss \(k\),

\[
 { \mathbb P\{\text{macro outcome}\}\,
        \Phi_\theta(A-k,B_\tau)
       \over \Phi_\theta(A,u)}
 \le C(1+u)^{-(1-\theta)(d-c)}e^{-\theta k h_*}.              \tag{3.3}
\]

If \(c=d,k=0\), and the endpoint is not the initial population, then

\[
 { \mathbb P\{\text{macro outcome}\}\,
        \Phi_\theta(A,B_\tau)
       \over \Phi_\theta(A,u)}
                         \le C(1+u)^{-\theta}.                \tag{3.4}
\]

The estimates remain valid after summing any collection of clean
branching words with the same \(c,k,B_\tau\).

#### Proof

The active factorial quotient satisfies

\[
             {(A-k)!\over A!}= {1\over(A)_{\underline k}}
                         \le(2/a)^k.                          \tag{3.5}
\]

Lemma 2.1 bounds the positive spectator displacement by
\(pk+d-c\). Since every intermediate and terminal spectator population is
at most \(L\), its factorial-linear positive cost is at most

\[
                         C^{k+1}(1+L)^{pk+d-c}.               \tag{3.6}
\]

The divisor in (3.2) is favorable when \(B\) increases and costs only a
fixed bounded-jump power when \(B\) decreases. Multiply
(3.5)--(3.6) by (3.1) and use (1.5). This proves (3.3). This is precisely
where the path maximum \(L\), not the entrance \(u\), is required.

If \(c=d,k=0\), Lemma 2.1 gives \(B_\tau\le u\). A nonidentical endpoint
has \(B_\tau\le u-1\). The spectator factorial quotient then loses a
factor comparable with \(1+u\), while the divisor and linear correction
cost only a bounded factor. This gives (3.4). \(\square\)

## 4. Literal returns and the strong cut

### Lemma 4.1 (exact-return classification)

After zero-vector reactions are deleted, a clean macro is a literal
population self-return if and only if its word is

\[
                         cB\longrightarrow q\longrightarrow cB
                                                                    \tag{4.1}
\]

for some enabled \(cB\in{\cal F}\), with no nontrivial intermediate
\(q\)-reaction.

#### Proof

A literal return has \(k=0\). If the base target is lower, \(e=0\), so
(2.1) forces \(T=0\); equality of the endpoint forces a deleted
zero-vector reaction. If the target is \(q\), then \(e=1,T=1\), and
equality of the spectator coordinate forces the sole \(q\)-target to be
\(cB\). The converse is immediate. \(\square\)

For large \(u\), only \(dB\to q\to dB\) can have nonvanishing leading
probability. Lower-degree exact loops have total probability
\(O((1+u)^{-1})\).

### Lemma 4.2 (uniform diagonal inverse)

Unless the relevant class is in the exact invariant/frozen alternative,
the probability of a literal clean self-return at every sufficiently
large base is at most \(1-\epsilon\), for some \(\epsilon>0\). A finite
corrector handles compact bases.

#### Proof

If \(\{dB,q\}\) is a proper subset of the strong complex graph, a directed
edge leaves it. If sourced at \(dB\), its conditional probability among
the \(dB\)-sourced edges is fixed because their factorial factor is common.
If sourced at \(q\), its conditional probability is likewise fixed because
all \(q\)-sourced edges share the factor \(AC\).

A leaving edge to \(jB\) has \(j<d\) and descends in \(B\). A leaving edge
to a positive-cofactor lower complex either completes with \(k\ge1\) or
reaches localization. Thus it cannot be a literal return. If
\(\{dB,q\}\) is the whole graph, the clean trace has only exact levels and
belongs to the invariant alternative. At compact bases, replace \(d\) by
the largest locally enabled degree and use the same finite directed cut,
or a finite path to the large-base region. \(\square\)

Literal returns therefore sum to a diagonal factor at most
\(\epsilon^{-1}\). No cap is put on their number.

## 5. Same-exponent clean Green

Let \(\widehat Q\) be the completed clean base kernel after literal returns
have been contracted, killed at active service or localization. A
continuing state has \(D'=D-k\ge0\).

### Theorem 5.1 (clean corrected Green)

There is a bounded positive corrector \(\chi(u)\), equal to one outside a
fixed compact set, such that

\[
 \widetilde\Phi_\theta(A,u)=\chi(u)\Phi_\theta(A,u)            \tag{5.1}
\]

satisfies

\[
 \widehat Q\widetilde\Phi_\theta
       \le\rho\widetilde\Phi_\theta,\qquad \rho<1.            \tag{5.2}
\]

Consequently

\[
 (I-\widehat Q)^{-1}\widetilde\Phi_\theta
       \le{1\over1-\rho}\widetilde\Phi_\theta.                \tag{5.3}
\]

The same estimate holds for the substochastic physical clean kernel.

#### Proof

Outside a fixed spectator compact, Lemmas 3.1--4.2 give

\[
 {\widehat Q\Phi_\theta\over\Phi_\theta}
 \le C\left\{(1+u)^{-(1-\theta)}
             +(1+u)^{-\theta}+e^{-\theta h_*}\right\}.       \tag{5.4}
\]

The terms are, respectively, lower-source moves, nonexact maximal-source
zero-service returns, and positive active losses. The right side tends to
zero.

On a fixed spectator compact, the clean transition probabilities are
independent of the active scale after the common \(q\)-factor is cancelled.
A closed zero-loss clean class could contain only literal pure/\(q\)
loops. Strong connectivity supplies a directed cut to strict loss or
localization unless the whole class is in the invariant alternative.
Hence the finite compact substochastic kernel has spectral radius below
one. Its finite Green potential supplies \(\chi\). Combining the compact
and exterior contractions proves (5.2), and summing the geometric Green
series proves (5.3). The physical clean kernel is dominated by the ideal
one because lower-clock competition only removes clean path mass.
\(\square\)

## 6. Polynomial hierarchy

Retain the nonnegative debt coordinate and put

\[
                         r=p\vee1,\qquad J=B+rD.               \tag{6.1}
\]

Since \(D'=D-k\), Lemma 2.1 gives

\[
                      J'-J\le(p-r)k+(d-c)\le d-c.             \tag{6.2}
\]

Thus a maximal-source macro never increases \(J\). If nonexact, it either
decreases \(J\), decreases \(D\), or is killed. A positive \(J\)-move is
bounded by two, loses at least one source degree, and has probability
\(O((1+B)^{-1})\) outside a compact set.

### Lemma 6.1 (lexicographic polynomial Green)

For every fixed integer \(m\ge0\),

\[
 (I-\widehat Q)^{-1}
       \{(1+J)^m+(1+D)^m\}
 \le C_m\{(1+J)^{m+1}+(1+D)^{m+1}\}.                         \tag{6.3}
\]

The killed macro count and terminal \(J,D\) therefore have every fixed
moment with a polynomial start factor.

#### Proof

Contract literal returns first. At large \(B\), a maximal-source cut has
fixed probability and gives a lexicographic descent of \((J,D)\): if
\(J\) does not decrease, (6.2) and nonexactness force \(k\ge1\), so
\(D'\le D-1\). Apply the bounded-jump Taylor expansion to

\[
 V_{m+1}(J,D)=(1+J)^{m+1}+C_m'(1+D)^{m+1}.                   \tag{6.4}
\]

Choose \(C_m'\) to pay the \(J'=J,D'<D\) case. Positive \(J\)-moves lose
a source degree, so their Taylor contribution is lower by
\(O((1+B)^{-1})\). On bounded \(B\), the finite strong-cut corrector,
uniform in \(D\), gives killing or strict lexicographic descent in a
bounded number of steps. Thus

\[
 (I-\widehat Q)V_{m+1}
 \ge c_m\{(1+J)^m+(1+D)^m\}-C_m\mathbf1_K.                   \tag{6.5}
\]

The compact Green corrector and optional summation prove (6.3). Standard
binomial induction for the additive reward \(1\) gives macro-count
moments. \(\square\)

No unweighted scale-relative \(B\)-moment follows from (6.3). Critical
\(q\)-branching can have heavy terminal \(B\) even when the corrected
Green estimate is valid.

## 7. Joint terminal divisor mark

Let \({\cal S}\) be the service kernel of a completed clean macro, and let
\[
        R_d={ (1+B_\tau)^d\over(1+u)^d}.                       \tag{7.1}
\]

### Lemma 7.1 (service-marked corrected estimate)

For every fixed \(s\ge0\),

\[
 {\cal S}\!\left[
   R_d^s\,\widetilde\Phi_\theta(A-k,B_\tau)\right]
 \le C_s e^{-c\theta h_*}\widetilde\Phi_\theta(A,u).          \tag{7.2}
\]

The same conclusion holds with any fixed polynomial in \(k\) inserted.

#### Proof

By Lemma 2.1,

\[
 {1+B_\tau\over1+u}
       \le C\left(1+{k\over1+u}\right)^p
       \le C(1+k)^p.                                         \tag{7.3}
\]

Thus \(R_d^s\le C_s(1+k)^{pds}\). Multiplying (3.3) by this factor and
using

\[
                  (1+k)^m e^{-\theta k h_*}
                     \le C_{m,\theta}e^{-\theta k h_*/2}      \tag{7.4}
\]

for all large \(h_*\) proves (7.2), since service has \(k\ge1\).
\(\square\)

Lemma 7.1 is the correct terminal interface. It replaces the false claim
that \(R_d\) has an unweighted scale-relative moment. In the full trace,
the preceding same-exponent corrected Green is composed with (7.2);
exponent slack pays the divisor accumulated before the last service macro.

## 8. Scope

The theorem proves the localized clean completed-return Green, the exact
arbitrary-branch ledger, the arbitrary-orientation strong-cut inverse, the
polynomial hierarchy, and the joint terminal divisor mark. Restoring open
lower-source reactions, using the joint mark to recover the raw terminal
transform, localization removal, and physical duration are separate
interfaces.
