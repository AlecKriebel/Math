# Completed-return ledger for the separated carrier

**Proof component, 2026-08-12 PDT.**  This note isolates the algebra which
survives all counterexamples to the earlier first-exit constructions.  It is
not a stopped theorem by itself.  Its purpose is to make the remaining
operator estimate exact and orientation-free.

## 1. Setting

Put

\[
 q=A+C,
 \qquad
 \{q\}\subseteq {\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,q\},                    \tag{1.1}
\]

and consider a cofactor-free base state \(x=(a,u,0)\).  Let

\[
 {\cal F}={\cal C}\cap\{0,B,2B\},
 \qquad
 p=\max_{y\in{\cal C}\setminus\{q\}} y_B,
 \qquad
 d=\max_{y\in{\cal F}}y_B .                         \tag{1.2}
\]

Thus \(0\le d\le p\le2\).  If \(p=2\), then \(2B\in{\cal F}\) and
\(d=2\).  If \(p=1,d=0\), the only lower complex which can produce a
spectator molecule is \(B+C\).  Define

\[
 m_p(u)=1+u^p,
 \qquad h_u=\log{a\over m_p(u)}.                     \tag{1.3}
\]

The separated regime is \(h_u\to\infty\).  A **clean macro** consists of
one reaction whose source lies in \({\cal F}\), followed, while \(C>0\),
only by reactions sourced at \(q\), and ending at its first return to
\(C=0\).  It is stopped earlier at a declared population localization.

## 2. Exact factorial tilt

For a population \(x\) and a complex \(y\), write

\[
                         M_x(y)=\prod_i(x_i+1)^{y_i}.          \tag{2.1}
\]

For every fixed \(0<\theta<1\), every enabled binary reaction
\(y\to z\), and every fixed factorial-linear correction \(\ell\),

\[
 \begin{split}
 \lambda_{yz}(x)&\asymp M_x(y),\\
 \exp\{\theta[G_\ell(x+z-y)-G_\ell(x)]\}
   &\le C_{\theta,\ell}
        \left({M_x(z)\over M_x(y)}\right)^\theta .   \tag{2.2}
 \end{split}
\]

The constants are uniform in the population.  This is an exact bounded-
degree factorial comparison: in each coordinate the factorial quotient is
a product of at most two consecutive integers, and an enabled falling
factorial is uniformly comparable with the corresponding power of
\(x_i+1\).

At a localized open state with \(C\ge1\), \(A\asymp a\), and

\[
 {1+B^p\over a}+{C\over a}\le\delta_a=o(1),          \tag{2.3}
\]

the \(q\)-clock gives a lower bound on the total rate.  If
\(r_y=M_x(y)/M_x(q)\), then every lower complex has \(r_y\le C\delta_a\),
and the one-edge embedded Feynman--Kac contribution satisfies

\[
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 e^{\theta\Delta G_\ell(x;y,z)}
 \le C r_y^{1-\theta}r_z^\theta .                   \tag{2.4}
\]

Equation (2.4) is sourcewise.  In particular, a lower-to-\(q\) entry and
its later \(q\)-exit must be retained in the same completed operator; their
two factors multiply to at most \(C\delta_a\).  Stopping between them is
invalid when \(h_u\) diverges slowly.

## 3. Clean completed-return ledger

Suppose the base source is \(cB\), and a clean macro returns to \(C=0\).
Let

\[
                         k=A_0-A_\tau .                       \tag{3.1}
\]

Then \(k\ge0\).  Indeed the base reaction can enter \(q\) at most once,
while every subsequent \(q\)-reaction lowers \(A\) once.  More precisely,
if \(e\in\{0,1\}\) says that the base target is \(q\), and \(T\) is the
number of \(q\)-reactions before return, then

\[
                              T=e+k .                         \tag{3.2}
\]

The spectator displacement obeys the orientation-free inequality

\[
                       B_\tau-u\le pk+(d-c).                 \tag{3.3}
\]

For \(p=0\) this is immediate.  For \(p=1,d=1\), every lower target
contains at most one \(B\), and the initial source consumes \(c\) of them.
For \(p=1,d=0\), a target can contain \(B\) only if it is \(B+C\).  Carrier
balance at the completed return shows that the number of such targets is
at most \(k\).  For \(p=2\), molecularity and carrier balance give the same
bound; the case \(k=0\) is a direct return to \({\cal F}\), whose target
degree is at most \(d=2\).

Consequently, below a moving cutoff on which
\((1+B)^p/a\le e^{-h_*/2}\), the embedded base-source factor and the
factorial endpoint factor satisfy

\[
 { (u)_c\over 1+(u)_d}
 e^{\theta[G_\ell(X_\tau)-G_\ell(x)]}
 \le
 C(1+u)^{-(1-\theta)(d-c)}e^{-\theta k h_*/3}.        \tag{3.4}
\]

The harmless loss from \(1/2\) to \(1/3\) absorbs bounded jumps, the fixed
linear correction, and the variation of the monomial along the localized
path.  In particular:

* if \(c=d,k=0\), a nonexact clean return strictly lowers \(B\);
* equality in that case is a literal population self-return and may be
  deleted from the embedded trace while retaining its elapsed time; and
* every clean service return \(k\ge1\) carries an exponential factor
  \(e^{-c\theta h_*}\).

Strong connectivity supplies a fixed cut from the two-node exact-return
set \(\{dB,q\}\) (or \(\{0,q\}\) when \(d=0\)).  The first edge leaving
that set is sourced at one of its two nodes, so its conditional probability
is bounded below using identical-source competition.  Therefore the
diagonal inverse of literal clean self-returns is uniformly bounded.

## 4. Why incomplete prefixes cannot be estimated

Take \(p=1,d=0\), \(u=a/\log a\), and suppose the graph contains
\(0\to q\), \(q\to B+C\), and \(B+C\to q\).  The incomplete word

\[
                         0\to q\to B+C\to q                  \tag{4.1}
\]

has raw tilted mass of order \(a^\theta/\log a\), which diverges.  The
next \(q\to B+C\) firing makes the last two reactions an exact physical
self-loop with probability of order \(u/a\), and a completed return later
supplies the missing service or lower-source factor.  Thus neither a
first-entry stop nor a base-launch times one-step open norm proves (3.4).
The operator must sum completed words, or equivalently introduce a phase
corrector which contracts (4.1) together with its next exit.

## 5. Remaining operator statement

The incomplete-prefix obstruction has an exact phase correction.  Augment
every open physical state by a label \(s\): after a reaction with lower
target \(z\), set \(s=z\); after a lower-to-\(q\) entry, set \(s=q\).
At a cofactor-free base use the artificial phase \(dB\).  Define

\[
 \Psi_\theta(x,s)
       ={e^{\theta G_\ell(x)}\over M_x(s)^\theta}.             \tag{5.1}
\]

At an open state put \(r_y=M_x(y)/M_x(q)\).  Direct substitution in
(2.2) gives the following complete transition table:

\[
\begin{array}{c|c}
 \hbox{physical source}&
 \displaystyle {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
             {\Psi_\theta(x+z-y,s')\over\Psi_\theta(x,s)}
 \\ \hline
 y\ne q & \le C r_y^{1-\theta}r_s^\theta,\\
 y=q,\ s\ne q&\le C r_s^\theta,\\
 y=q,\ s=q&\le C .
\end{array}                                                   \tag{5.2}
\]

The first line is independent of the target.  In the third line the free
\(q\)-exit changes the phase from \(q\) to a lower complex.  Therefore it
cannot repeat for free.  A lower \(s\to q\) entry followed by a \(q\to s\)
exit has total corrected factor \(O(r_s)\), exactly as its physical
probability.  This is the phase-harmonic cancellation missing from (4.1).

At a base, a reaction sourced at \(cB\) and entering an open phase has
corrected factor

\[
       { (u)_c\over 1+(u)_d}
       {\Psi_\theta(X_1,s_1)\over\Psi_\theta(x,dB)}
       \le C(1+u)^{-(1-\theta)(d-c)}.                         \tag{5.3}
\]

If an open reaction lands directly at \(C=0\), the new divisor is
\(M_{X'}(dB)^\theta\).  Its extra target-to-base-divisor factor is bounded
because every cofactor-free target has degree at most \(d\).

Let \(Q\) be the completed clean base-return kernel after deleting literal
self-returns, killed when the cumulative active displacement first becomes
negative.  Positive active displacement, which can only be created by an
open lower-source reaction, is carried as a debt coordinate \(D=A-a\).
Equations (3.3)--(3.4) and the strong
cut imply, for sufficiently small fixed \(\theta>0\), a same-weight killed
Green bound

\[
       (I-Q)^{-1}\Phi_\theta(u,D)\le C\Phi_\theta(u,D),
       \qquad
       \Phi_\theta(u,D)
        ={\exp\{\theta G_\ell(a+D,u,0)\}
           \over M_{(a+D,u,0)}(dB)^\theta}.           \tag{5.4}
\]

with polynomial additive-functional versions.  Positive \(B\)-moves from a
source of degree \(c<d\) contribute
\((1+u)^{-(1-\theta)(d-c)}\); maximal-source nonexact moves descend or are
killed.  Compact populations use the finite strong-cut corrector.

For the full physical kernel, mark the first lower-sourced reaction while
\(C>0\), but do not stop there.  Use (5.2) to run through the following
free \(q\)-exit, and continue to a completed return or localization.  Every
such marked block contributes at least one factor
\(C\delta_a^\eta\), \(\eta=\min(\theta,1-\theta)>0\), after its phase
correction.  The desired
load-bearing estimate is

\[
 \left\|(I-Q)^{-1}R_{\rm completed}\right\|_{\Phi_\theta}
       \le C\delta_a^\eta=o(1),                       \tag{5.5}
\]

where \(R_{\rm completed}\) contains **all** completed words with at least
one open lower-source reaction.  Once (5.2) is written as an ordered-word
sum, its Neumann series is same-exponent and retains arbitrary nested
carrier branching.

The corrected base weight differs from the raw factorial exponential by
only the maximal-source polynomial.  A polynomial ratio moment for
\(M_{X_\tau}(dB)/M_x(dB)\), followed by Hölder with
\(0<\theta'<\theta\), converts the corrected estimate back to the raw
terminal transform.  Thus (3.4), (5.4), and (5.5) yield

\[
 \mathbb E_x\!\left[
   e^{\theta'(G_\ell(X_\tau)-G_\ell(x))};\ {\rm service}
 \right]
       \le C e^{-c\theta' h(a,u)},                    \tag{5.6}
\]

up to included localization endpoints.  Equation (5.6), rather than a
symmetric Taylor expansion, is the right interface to the fourth power:
outside an exponentially small positive-overshoot event the actual
factorial-linear potential drops by \(ch\), while large negative spectator
moves remain favorable.

The proof still has to supply the ordered-word summation in (5.5), the
unweighted duration recursion, and endpoint-weighted localization.  Those
are analytic kernel estimates; no orientation or population enumeration is
part of them.
