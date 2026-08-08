# Shannon target reflection: exact reductions and the limit of path reversal

Date: 2026-08-02 (America/Los_Angeles)

## Status

The Shannon reflection inequality

\[
 I(V;B)\le M:=E_\Pi h_2(|B|/n)                       \tag{1}
\]

remains **OPEN**.  This note gives three exact reformulations, constructs the
normalized reverse channel forced by the fair-geometric Cayley identity, and
shows exactly why three standard information-theoretic proofs do not close
(1).  No numerical observation is used as a theorem.

## 1. Membership experiment and entropy reflection

Let `A~Pi`, let `V` be uniform and independent of `A`, let `B` be the output
of the `V`-update, and put

\[
 J=1_{\{V\in A\}}.                                    \tag{2}
\]

Conditional on `A`, the bit `J` has success probability `|A|/n`; hence

\[
 I(V;A,J)=I(V;J\mid A)=E_\Pi h_2(|A|/n)=M.            \tag{3}
\]

Stationarity gives `A` and `B` the same law.  If `k=|B|`, `h=n-k`, and

\[
 \tau_v(B)=\Pr(V=v\mid B)={1+e_v(B)\over n}
 \quad(v\notin B),                                    \tag{4}
\]

then

\[
 \boxed{M-I(V;B)=H(V\mid B)-H(V\mid A,J).}            \tag{5}
\]

Equivalently,

\[
 \boxed{
 M-I(V;B)=E_\Pi\left[
 {k\over n}\log{h\over k}
 -D\bigl(\tau_B\,\|\,{\rm Unif}(B^c)\bigr)
 \right].}                                            \tag{6}

Thus (1) says that the actual stationary output is no more informative
about the update target than the pre-update set together with its one-bit
membership answer.

There is also a useful mixture form.  Given `B`, the null-history target is
uniform on `B^c`, the effective-history target has law

\[
 s_v(B)=e_v(B)/k,
\]

and their mixing weights are `h/n,k/n`.  Therefore

\[
 M-I(V;B)
 =I(J;V\mid B)
 +{E_\Pi k\over n}
   E_{\widehat\Pi}\{H(s_B)-\log|B|\},                 \tag{7}

where `widehat Pi(B)=|B|Pi(B)/E|B|` is the effective-event law.  The second
term in (7) can be negative, even on reversible kernels; its compensation by
the first term is essential.

## 2. The two likelihood-ratio experiments

Let `C_0` be the channel from `V` to `(A,J)` and `C_1` the channel from `V`
to `B`.  Under a uniform target, their output laws are

\[
 q(A,1)=\Pi(A){|A|\over n},\qquad
 q(A,0)=\Pi(A){n-|A|\over n},\qquad q_1(B)=\Pi(B).
\]

Relative to the product of input and output marginals, let `L_0,L_1` be the
two likelihood ratios.  Conditional on a set of size `k`, `L_0` has the
three-point law

\[
 \begin{array}{c|ccc}
 \text{value}&0&n/k&n/(n-k)\\ \hline
 \text{probability}&2k(n-k)/n^2&k^2/n^2&(n-k)^2/n^2.
 \end{array}                                          \tag{8}
\]

For `C_1`, conditional on `B`, its `n` equally weighted values are

\[
 0\quad(v\in B),\qquad 1+e_v(B)\quad(v\notin B).       \tag{9}
\]

Consequently

\[
 \boxed{
 M=E[L_0\log L_0],\qquad I(V;B)=E[L_1\log L_1],
 \qquad E L_0^2=2.}                                   \tag{10}

The Shannon conjecture and the chi-square conjecture are therefore the same
likelihood comparison for the convex functions `x log x` and `x^2`.

Full convex-order domination is nevertheless false.  On the symmetric
triangle with weights `(w_01,w_02,w_12)=(7,1,1)`, at threshold `t=3/2`,

\[
 \boxed{
 E(L_0-t)_+-E(L_1-t)_+=-{8\over327}<0.}               \tag{11}

Thus no proof may simply invoke `L_1 <=_cx L_0`.

## 3. Exact normalized Cayley reverse channel

Fix `v` and use the submeasures from `RESOLVENT_IDENTITIES.md`:

\[
 \sigma_v(C)=\Pi(C+v),\qquad
 \nu_v=\hbox{effective `v`-output},\qquad
 \lambda_v={\sigma_v+\nu_v\over2}.                   \tag{12}

All three have total mass `p_v=Pi(v in A)`.  Let `A_v` add one labelled
sample `i~P_v*`.  The midpoint resolvent is

\[
 \lambda_vA_v=\nu_v.                                  \tag{13}

It therefore defines the normalized reverse step

\[
 \boxed{
 R_v(B;C,i)=
 {\lambda_v(C)P_{vi}1_{\{B=C\cup\{i\}\}}\over\nu_v(B)}.} \tag{14}

After drawing `(C,i)` from (14), declare `stop` with probability

\[
 {\sigma_v(C)\over\sigma_v(C)+\nu_v(C)}               \tag{15}

and `continue` with the complementary probability.  Under `C~lambda_v/p_v`,
the stop bit is marginally fair.  Conditional on continuation, `C` again
has law `nu_v/p_v`, so (14)--(15) recurse and terminate almost surely.

This is not merely a formal reverse kernel.  For every labelled forward
path

\[
 C_0\xrightarrow{i_1}C_1\xrightarrow{i_2}\cdots
 \xrightarrow{i_m}C_m,
\]

its forward probability conditional on an effective `v`-event is

\[
 {\sigma_v(C_0)\over p_v},2^{-m}
 \prod_{j=1}^m P_{vi_j}.                               \tag{16}

Multiplying (14)--(15) backward from `C_m` telescopes to exactly (16).
Hence the Cayley reverse construction is the exact Bayesian reversal of the
geometric sample path.

### Consequence

The most natural path-space entropy production is identically zero.  The
Cayley identity supplies a normalized reverse channel, but comparing the
actual forward path with this actual reverse path gives equality of path
measures, not the positive quantity in (1).  A successful KL proof would
need a second comparison reverse law and a new normalization estimate.

## 4. Blackwell garbling is too strong

If `C_1` were obtained by a target-independent garbling of `C_0`, (1) would
follow immediately by data processing.  This is false even for the
unweighted path `0-1-2`.

For target rows `v=0,1`, the total variation of the membership-experiment
rows is

\[
 \|C_0(0,\cdot)-C_0(1,\cdot)\|_{TV}={7\over9},         \tag{17}
\]

whereas the output rows satisfy

\[
 \|C_1(0,\cdot)-C_1(1,\cdot)\|_{TV}={5\over6}.         \tag{18}

The increase is exactly `1/18`, contradicting total-variation contraction
under every garbling.  Thus (1), if true, is a uniform-prior entropy
comparison rather than a Blackwell ordering of experiments.

## 5. What remains

The exact surviving target is narrow:

* exploit the specific integral representation of `x log x`, rather than
  all convex functions;
* retain the cancellation between null and effective histories;
* use stationary rank transport, since (6) has negative pointwise terms on
  upper ranks even for the complete graph;
* compare against a non-Bayesian reverse path whose normalization produces
  the rank term in (6).

Directed uniform-subset enumeration through order four and random or
continuous searches through order six found no negative Shannon gap.  This
is diagnostic evidence only.
