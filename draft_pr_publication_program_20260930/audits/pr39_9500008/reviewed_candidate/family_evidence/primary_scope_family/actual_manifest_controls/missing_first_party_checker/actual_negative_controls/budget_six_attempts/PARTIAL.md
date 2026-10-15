# Bounded Brownian pieces and the missing random time shift

**Outcome: unresolved.** The exact question allows a random choice of time origin. A fixed-junction counterexample therefore does not answer it. The partial result below couples every bounded-piece concatenation to a genuine two-sided Brownian motion with error \(O(\sqrt{\log R})\) on \([-R,R]\). This is an asymptotic approximation, not the exact random-shift representation being asked for. The piece-rotation mechanism is already present in Burdzy–Scheutzow; no priority claim is made.

## 1 Exact source and existing results

[Burdzy's author-maintained problem page](https://sites.math.washington.edu/~burdzy/open_mathjax.php), Problem 8, defines two-sided Brownian motion by the existence of an almost surely finite random time \(S\) such that
\[
(X_{S+t}-X_S)_{t\ge0}
\quad\hbox{and}\quad
(X_{S-t}-X_S)_{t\ge0}
\]
are independent standard Brownian motions. The definition does not require \(S\) to be a stopping time or a concatenation junction. The pinned statement omits this essential definition.

The pieces \((T_k,B^k_{[0,T_k]})\), \(k\in\mathbb Z\), are independent but need not be identically distributed. Each \(T_k\) is a stopping time for a filtration relative to which \(B^k\) is Brownian. The sums of durations diverge in both directions. Zero durations are permitted. The question assumes a common deterministic finite bound \(T_k<c\) almost surely and asks for the random-shift conclusion above.

[Burdzy–Scheutzow, *Forward Brownian motion*](https://arxiv.org/abs/1302.6958v4), published in Probability Theory and Related Fields 160 (2014), 95–126, uses precisely this distinction in Definition 2.1: the fixed-origin law is denoted \(2BM(0)\), and the random-origin property is \(2BM\). Theorem 5.1, preprint pages 18–19, proves \(2BM\) for identically distributed independent pieces with finite mean duration. Theorem 5.3 gives nonidentical counterexamples with any prescribed uniform finite-moment bound; their durations are not uniformly bounded. Problem 7.7 asks a related bounded-duration/backward-Brownian question with different quantifiers.

The relevant definitions, complete proofs of Theorems 5.1 and 5.3, the piece-rotation portion of Theorem 5.2, and the open-problem section were inspected. [Pitman–Tang (2015), page 3](https://www.columbia.edu/~wt2319/Slepian.pdf) also distinguishes the known iid result from the nonidentical setting. The current author page still lists Problem 8; the bounded current-literature search located no resolution. This is not an exhaustive literature certificate.

## 2 A pathwise approximation for the full bounded-piece class

Let \(X\) be the concatenation anchored by \(X_0=S_0=0\), as in the source. Define
\[
A_0=0,\qquad A_j=\sum_{i=1}^j T_{-i}=-S_{-j},\qquad j\ge1.
\]
These times tend to infinity almost surely. Let \(R(t)=X_{-t}\), \(t\ge0\).

**Proposition.** On the same probability space one can construct a standard Brownian motion \(W\), independent of \((X_t)_{t\ge0}\), such that, for all \(R_0>0\),
\[
\sup_{0\le t\le R_0}|X_{-t}-W_t|
\le
2\,\omega_W(c;R_0+c),
\tag{1}
\]
where
\[
\omega_W(c;L)=
\sup\{|W_s-W_t|:0\le s,t\le L,\ |s-t|\le c\}.
\]
Consequently there exists a \(2BM(0)\) process \(Z\) on this space with \(Z_t=X_t\) for \(t\ge0\), and
\[
\sup_{|t|\le R_0}|X_t-Z_t|
=O(\sqrt{\log(2+R_0)})
\quad\hbox{almost surely as }R_0\to\infty.
\tag{2}
\]
The almost-sure constant may depend on the sample and on \(c\).

**Proof of the exact bound.** Run the negative-index pieces in the order \(-1,-2,\ldots\), without reversing each piece internally, and change their signs:
\[
W_{A_{j-1}+u}
=
-\sum_{i<j}B^{-i}_{T_{-i}}-B^{-j}_u,
\qquad 0\le u\le T_{-j}.
\tag{3}
\]
The values agree at endpoints. Independent stopped Brownian pieces concatenate to a Brownian motion by the strong Markov restart property, even when their laws differ. Applying that fact to the independent pieces \(-B^{-j}\) proves that \(W\) is standard Brownian motion. This is the same concatenation fact used after Definition 2.2 in the source. No terminal conditioning is imposed. Divergence of \(A_j\) excludes explosion; zero-length pieces can be discarded.

At each junction, \(R(A_j)=W(A_j)\). In a piece beginning at \(a=A_{j-1}\) and having duration \(T=T_{-j}\), direct substitution yields
\[
R(a+u)=W(a)+W(a+T)-W(a+T-u),\qquad 0\le u\le T.
\tag{4}
\]
Thus
\[
R(a+u)-W(a+u)
=[W(a+T)-W(a+T-u)]-[W(a+u)-W(a)].
\tag{5}
\]
Each increment in brackets has duration at most \(c\). If \(a+u\le R_0\), all its endpoints lie in \([0,R_0+c]\). Inequality (1) follows. Formula (3) uses only the negative-index pieces, whereas the positive half of \(X\) uses the nonnegative-index pieces. These families are independent. The positive half of \(X\) is itself standard Brownian motion, again by concatenation.

**Proof of the modulus estimate.** Since the duration sums diverge, the deterministic bound can be taken with \(c>0\). Let \(R_m=c2^m\), \(m\ge1\). An increment of length at most \(c\) in \([0,R_m+c]\) lies inside some interval \([jc,(j+2)c]\), with \(0\le j\le2^m+1\). If its absolute value exceeds \(r\), then
\[
\sup_{0\le u\le2c}|W_{jc+u}-W_{jc}|>r/2.
\]
The reflection principle and the Gaussian tail bound imply
\[
\mathbb P\{\omega_W(c;R_m+c)>r\}
\le 4(2^m+2)\exp(-r^2/(16c)).
\tag{6}
\]
Take \(r=8\sqrt{cm}\). The right side is summable in \(m\). Borel–Cantelli and monotonicity between successive dyadic radii give
\[
\omega_W(c;R_0+c)=O(\sqrt{\log(2+R_0)})
\quad\hbox{almost surely}.
\]
Define \(Z_t=X_t\) for \(t\ge0\), and \(Z_t=W_{-t}\) for \(t\le0\). The two halves are independent Brownian motions and agree at zero. Combining the modulus estimate with (1) proves (2). ∎

**Corollary.** For every fixed \(L<\infty\),
\[
\left(r^{-1/2}X_{rt}\right)_{-L\le t\le L}
\ \Longrightarrow\ 2BM(0)|_{[-L,L]}
\quad\hbox{as }r\to\infty
\]
in the uniform topology. Indeed, (2) makes the difference from \(r^{-1/2}Z_{rt}\) tend to zero almost surely on that interval, while Brownian scaling gives the latter process the required law for every \(r\).

This proof adapts the reflection/rotation of individual pieces used in Burdzy–Scheutzow's proof of Theorem 5.2. The bounded-duration modulus consequence is recorded here as a partial estimate, with novelty unconfirmed.

## 3 Why a fixed-junction example is insufficient

Take iid pieces with
\[
T_k=\min\{\tau_k,1\},\qquad
\tau_k=\inf\{t\ge0:B^k_t=-1\}.
\]
They obey the strict bound \(T_k<2\), are positive almost surely, and have a finite positive mean, so their duration sums diverge almost surely.

On the positive-probability event \(\{\tau_{-1}<1\}\), the reversed final negative piece satisfies
\[
X_{-u}=B^{-1}_{T_{-1}-u}-B^{-1}_{T_{-1}}>0,
\qquad 0<u<T_{-1}.
\]
A standard Brownian motion starting at zero has probability zero of staying positive on any initial interval: use the reflection principle on intervals of length \(1/n\), then a countable union. Therefore this concatenation does not have law \(2BM(0)\).

Nevertheless, the pieces are iid with finite mean. Theorem 5.1 proves that the process **does** have the \(2BM\) random-origin property. This explicitly shows why fixed-origin bias cannot be promoted to a counterexample to Problem 8.

A further immediate known-theorem corollary is that periodically varying piece laws also suffice: if the stopped-pair law has period \(m\), group \(m\) consecutive independent pieces into one block. The resulting stopped Brownian blocks are iid, their durations are bounded by \(mc\), and Theorem 5.1 applies. This grouping observation does not cover arbitrary nonidentical laws.

## 4 Where the full proof still fails

The approximation (2) changes the path inside every negative piece. It does not say that \(X\) is exactly a single time-shifted \(Z\). A small error relative to diffusive scale is not an exact distributional identity.

Another tempting compactness argument is also insufficient. Since the positive half of every such \(X\) is Brownian, for every deterministic \(a\ge L\) the centered window
\[
(X_{a+t}-X_a)_{-L\le t\le L}
\]
already has the law of \(2BM(0)\) on that window. This holds even for decomposable counterexamples without the boundedness hypothesis. Sending \(a\to\infty\) therefore produces Brownian windows without producing any finite random origin on the original whole path.

The iid proof uses a stationary shift-coupling of a renewal process and identical conditional laws for the stopped path given its duration. For arbitrary nonidentical pieces, those conditional laws may depend on the piece index. A deterministic upper bound on durations does not itself establish the required stationary marked-process law or an exact finite shift-coupling. No replacement for that step was proved here.

Thus the residual target is unchanged: construct one finite random time giving two independent exact Brownian half-paths for every independent bounded-piece sequence, or exhibit a bounded-piece example for which every random time fails. The asymptotic coupling and the fixed-junction diagnostic do neither.

## 5 Verification and disposition

The accompanying verify.py checks 12,288 exact finite stopped-walk configurations, the piece-rotation identity at every grid point, agreement at junctions, the modulus bound, and 48 exact four-step marginal laws. It also checks a rational summable majorant for the dyadic tail series. These finite analogues test the algebra and indexing; the Brownian-law and almost-sure arguments are proved above, not inferred from simulations.

Two substantive routes were recorded: the iid/finite-window extension attempt, which stops at an exact-shift gap, and the rotation estimate, which gives the partial theorem. The full problem remains unresolved. No candidate full solution, priority claim, or unreviewed PR is made.
