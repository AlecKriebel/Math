# Independent audit of the full separated joint-return theorem

**Hostile composition audit, 2026-08-12 PDT.**  The exact target is

`proof_first_separated_full_all_clock_joint_return_theorem.md`

at SHA-256

`389e3b446006e9313238a0b4b0029f39e0f1cee0c2d90faf6e63cccf38a581e1`

(576 lines, 21154 bytes).  The target was not edited during this audit.
No support, orientation, reaction-word, or population enumeration was
used.

**Verdict: STRICT PASS.**  The frozen theorem correctly composes the
clean completed-return Green theorem, normalized all-clock terminal
transform, included-boundary estimate, physical duration estimate,
fixed-class invariant routing, and raw fourth-power lift.  The physical
stopping time is almost surely finite; its labels are disjoint and
exhaustive; and neither its endpoint nor duration claims assume the false
unweighted spectator moment associated with a critical carrier genealogy.

## 1. Frozen dependency replay

Every dependency hash cited by the target matches the current exact file:

\[
\begin{array}{c|c}
\text{component}&\text{SHA-256}\ \hline
\text{invariant/no-history routing audit}&
\texttt{cef9030583f0856a9243b93abece2a3f3eb3bb28912e438774d75946c24af1b1}\\
\text{clean base Green audit}&
\texttt{96c72e11a6105013b8d7b6e2309da7c2dbebccfa0b72640bfb3cfe6cf1608b36}\\
\text{open phase audit}&
\texttt{5286d3fbd5d57e92047f8db1339130c228498215bdd23d4d3ebcb1946db26114}\\
\text{first-mark resolvent}&
\texttt{d4c4baff29ffda942798f28fc69d4b30ab25ee2c8e13d1960a4ee20b6d772506}\\
\text{normalized terminal theorem}&
\texttt{149c2edd9a8427a442a66e4f99c026be96313bfc4e5072f96d0aa380502ffa77}\\
\text{normalized terminal audit}&
\texttt{5dd855cbb52bd84b83886209b9a0dd96cb91229275037f759be7cdac85d6a0b1}\\
\text{physical duration theorem}&
\texttt{504b87e600c382e9c82b88cf0ea88f87a6a4b6c7783202cc9cc2faa79fefc640}\\
\text{physical duration audit}&
\texttt{c9be124327288bbb45f42cbb005c9b96d854cfb629f94dd4c7cc61cc456ccb56}\\
\text{raw fourth-power lift}&
\texttt{3badb799468f6912659916ab2bc4ee556f5c113f00fbea01d106c88449cc0134}\\
\text{raw fourth-power audit}&
\texttt{3cf72b58a328bb493aa48f9b1fd11ec164f49c4504f7a40c0dcc3a1d6062326e}.
\end{array}
\]

The target is also free of control characters and renders successfully
with Pandoc.

## 2. Common scale, tube, and stopping rule

The theorem uses one scale throughout:

\[
 h=\log\frac{a}{m(b)},\qquad
 \bar\delta=e^{-h/2}=\sqrt{m(b)/a}.                         \tag{2.1}
\]

Its included open boundary is the first endpoint crossing of

\[
 A\in[a/2,2a],\qquad
 C<c_0\bar\delta a,\qquad
 1+B^p<c_0\bar\delta a                                   \tag{2.2}
\]

with the spectator inequality omitted for (p=0).  This is the same tube
used by the normalized transform and, after taking (c_0) sufficiently
small, the duration lemma's source-ratio tube.  The completed-base guard is
tested only after a continuing, unmarked, clean (k=0) return.  The exact
priority

\[
                         B_O>S\text{ or }E>B_0              \tag{2.3}
\]

therefore agrees in every component.  A boundary-causing reaction is
included even if it is simultaneously a first mark or lands at (C=0).
A clean service or marked return is terminal before the narrower base
guard is tested.  A marked path keeps all physical clocks until the next
actual base return and never starts another base macro.

## 3. Exact fixed-class routing and exhaustiveness

At a base, if no member of \({\cal F}\) is enabled, every remaining source
contains (C), so the state is absorbing.  If such an endpoint were
reachable from the fixed closed irreducible class \(\Gamma\), it would
belong to \(\Gamma\), and irreducibility would force \(\Gamma\) to be that
singleton.  Hence a distinct no-\({\cal F}\) base endpoint cannot occur on
the nonfrozen physical-loss branch.

If \({\cal P}=\varnothing\), every complex has the same value of (A-C).
At (C=0), this invariant fixes (A) within one class and excludes a
sequence with (h\to\infty).  If \({\cal P}\ne\varnothing\), a simple
directed path from an enabled base source to its first
\({\cal P}\)-vertex, followed by a nonself (q)-exit, is executable and
lowers (A).  On bounded spectator sets it supplies the compact killed
cut; at large spectator population the maximal-source ledger supplies the
exterior cut.

These observations prove both that the duration lemma is invoked only on
its certified active-loss branch and that no fifth terminal label is
missing.  On that branch the stopped sample space is exactly

\[
                         \Omega=S\mathbin{\dot\cup}E
                                    \mathbin{\dot\cup}B.     \tag{3.1}
\]

## 4. Clean and marked raw terminal transforms

For a completed clean macro, exact balance gives

\[
                     k=T-e\ge0,\qquad
                     \Delta B\le pk+(d-c).                  \tag{4.1}
\]

When (k=0), the macro is only
(cB\to jB) or (cB\to q\to jB).  Thus its displacement is bounded;
a maximal-source nonself return decreases (B); a positive move uses a
lower source degree and pays its same-exponent factorial tilt.  Literal
returns have the uniform directed-cut inverse.  Together with the compact
active-loss cut, this gives the clean Green bound at the same exponent.
For (k\ge1), (4.1) pairs the positive spectator cost with the source
degree and active factorial loss, yielding

\[
                \mathbb E[e^{\theta\Delta G_\ell};S]
                         \le C\bar\delta^\theta.             \tag{4.2}
\]

At open states, the normalized phase weight is

\[
 V_\theta(x,s)=e^{\theta G_\ell(x)}
       \left\{\frac{M_x(dB)}{M_x(s)}\right\}^{\theta},      \tag{4.3}
\]

and is defined to equal the raw exponential at every base.  The sourcewise
phase table gives one free (q)-exit and a small factor before it can
recur.  The first-mark operator is restricted by boundary priority and
split into a direct-base part (R_B) and an open part (R_O).  Hence the
exact (E)-kernel is

\[
       (I-Q)^{-1}\{R_B+R_O(I-K_{OO})^{-1}T_{OE}\},          \tag{4.4}
\]

while the complementary crossing exits belong to (B_O).  Both endpoints
of (4.4) are bases, so (4.3) converts to raw without a divisor moment:

\[
                \mathbb E[e^{\theta\Delta G_\ell};E]
                      \le C\bar\delta^{1-\theta}.           \tag{4.5}
\]

Thus the target never appeals to an unweighted terminal (B)-moment;
arbitrary later marks and arbitrary carrier branching are already summed
inside the physical open resolvent.

## 5. Included boundary and endpoint moments

Put

\[
 L=\min\{a,\bar\delta a,
                    (\bar\delta a)^{1/p}:p\ge1\}.           \tag{5.1}
\]

The separated premise implies (L\ge ca^{1/4}).  A continuing base path
to (B_0) needs \(\Omega(L)\) bounded, contracted (k=0) returns and has
same-exponent mass (C\rho^{cL}).  An open path to (B_O) starts below
the half guard, needs \(\Omega(L)\) bounded reactions, and has corrected
mass (C(C\bar\delta^\eta)^{cL/2}).  The endpoint conversion costs only a
fixed power of (a); at a (C=0) landing it costs one.  Consequently,
for every fixed polynomial (P) and (N),

\[
 \mathbb E[e^{\theta\Delta G_\ell}P(X_\tau);B]
                               \le C_{N,P}a^{-N}.            \tag{5.2}
\]

This includes a (q\to2B) crossing which lands directly at a base: its
pre-jump path has already traversed the required distance, and its label is
(B_O) by (2.3).

The separate endpoint assertion (1.8) does not infer an unweighted moment
from a possibly critical clean genealogy.  An (S)- or (E)-endpoint is
the completed return of the unique terminal open excursion and occurs
before (B_O); its coordinates are therefore deterministically (O(a)).
A (B_O)- or (B_0)-endpoint is the included first crossing by a bounded
reaction and obeys the same deterministic polynomial cap.  When (p=0),
(B) appears in no complex and is constant on the fixed class.  Combining
this pathwise endpoint cap with the duration moments proves (1.8).

## 6. Almost-sure termination and duration

Before an open endpoint, the next source is (q) with probability
(1-O(\bar\delta)).  A (q)-firing lowers (A) by one, while a lower
firing raises it by at most one.  A fixed exponential supermartingale
therefore gives

\[
                  \mathbb P\{\nu>n\}\le e^{Ca-\gamma n}    \tag{6.1}
\]

for the reaction count in any open excursion.  Thus it terminates almost
surely, independently of whether the untruncated carrier offspring law is
subcritical, critical, or supercritical.  Its holding rate is at least
(cAC\ge ca), so the unique terminal long open excursion has bounded
fixed physical-time moments.

Before it, the contracted (k=0) base trace has

\[
 \mathbb P\{N_B>n\}\le Ce^{tb-\gamma'n},\qquad
 \mathbb E N_B^r\le C_r(1+b)^r.                            \tag{6.2}
\]

Literal returns expand into uniform geometric blocks, and every nonfrozen
base has a fixed positive rate.  Restoring all holding times gives

\[
                           \mathbb E\tau^r\le C_r(1+b)^r.   \tag{6.3}
\]

Equations (6.1)--(6.2), together with the reachability exclusion in
Section 3, prove almost-sure termination under the exact labels (3.1), not
merely under a related killed kernel.  Moreover (m(b)=o(a)), while
(G_\ell(a,b,0)\ge ca\log a), so

\[
                         \mathbb E\tau=o(G_\ell^3h).        \tag{6.4}
\]

## 7. Raw fourth-power composition

For one fixed \(0<\theta<1/2\), (4.2), (4.5), and (5.2) imply

\[
 \mathbb E[e^{\theta\Delta G_\ell};S]
 +\mathbb E[e^{\theta\Delta G_\ell};E]\le Ce^{-ch},
 \qquad
 \mathbb E[e^{\theta\Delta G_\ell};B]\le C_Na^{-N}.      \tag{7.1}
\]

Here (h\to\infty), (h\le\log a), and (h=o(G_\ell)).  Exponential
Markov gives \(\Delta G_\ell\le-c'h\) with probability (1-o(1)).  On
that event, monotonicity of (t^4) over the attainable range
(G_\ell\ge1) gives descent of order (G_\ell^3h).  The positive
exceptional part obeys

\[
 ((G_\ell+u)^4-G_\ell^4)^+
       \le C_\theta(1+G_\ell^3)e^{\theta u/2},\qquad u\ge0,
                                                                    \tag{7.2}
\]

and Cauchy--Schwarz with (7.1) makes its expectation
(o(G_\ell^3h)).  Adding (6.4) preserves a strict negative multiple of
(G_\ell^3h), proving the target's stopped Foster estimate.  This step
uses the raw transforms directly and never reintroduces the obsolete phase
divisor.

## 8. Publication disposition

The target explicitly retires both failed predecessor constructions, at
their exact hashes, and replaces them by the completed physical
joint-return rule.  Its conclusions are fixed-class, orientation-free,
all-clock after the first mark, exact at direct-base marks and included
crossings, almost surely finite, and expressed with the common workload
(W_\ell=G_\ell^4).

Every load-bearing composition seam has therefore been proved.  Within the
target's exact separated-support scope, no counterexample or missing
hypothesis remains.
