# Exact canonical trigger-and-drain lemma

Consider

\[
0\xrightarrow{\alpha}A+B,
\qquad A+B\xrightarrow{\beta}B,
\qquad B\xrightarrow{\gamma}0,
\]

with \(\alpha,\beta,\gamma>0\).  Start from \((A,B)=(n,0)\).  Let
\(\sigma\) be the first firing of \(0\to A+B\), and let \(\tau\) be the
first time after \(\sigma\) at which \(B=0\).

## Lemma

Put

\[
\delta=\frac{\beta}{\alpha+\beta+\gamma}.
\]

Then

\[
\mathbb E_n A(\tau)
 \le (1-\delta)(n+1)+e^{\alpha/\gamma}-1,
\]

and

\[
\mathbb E_n\tau=\frac{e^{\alpha/\gamma}}{\alpha}.
\]

Consequently, for all

\[
n>\frac{1-\delta+e^{\alpha/\gamma}-1}{\delta},
\]

the complete episode has strictly negative mean \(A\)-reward.

## Proof

The marginal \(B\)-process during the busy period is the immigration-death
chain with immigration rate \(\alpha\) and death rate \(\gamma b\).  The
reaction \(A+B\to B\) does not change \(B\).

Label any one of the \(n+1\) particles of type \(A\) present immediately
after the trigger.  Conditional on the path of \(B\), that label has killing
hazard \(\beta B(t)\).  At the initial state \(B=1\), the first event relevant
to the pair consisting of \(B\) and the tagged particle is one of:

* a new immigration, rate \(\alpha\);
* the loss of the sole \(B\), rate \(\gamma\);
* killing of the tag, rate \(\beta\).

Firings that kill a different \(A\)-particle are self-transitions of this
marginal process and can be deleted.  Hence the tag is killed before either
of the other relevant events with probability exactly \(\delta\).  Its
survival probability to the end of the busy period is therefore at most
\(1-\delta\).  Linearity of expectation bounds the survivors among the
initial \(n+1\) particles by \((1-\delta)(n+1)\).

Each later immigration creates one additional \(A\)-particle.  Bounding its
survival probability by one shows that their total contribution is at most
the expected number of immigrations during the busy period.

For the immigration-death chain, \(\rho=\alpha/\gamma\) and the stationary
mass at zero is \(e^{-\rho}\).  A regenerative cycle consists of a mean
\(1/\alpha\) holding time at zero followed by a busy period.  The mean total
cycle length is therefore \(e^\rho/\alpha\), so

\[
\mathbb E T_{\rm busy}=\frac{e^\rho-1}{\alpha},
\qquad
\mathbb E(\#\text{ busy-period immigrations})=e^\rho-1.
\]

Adding the initial mean waiting time \(1/\alpha\) proves the duration formula
and completes the endpoint bound.

## Scope

This lemma is exact for the canonical cycle.  It does not by itself prove the
universal theorem: in a general network the trigger population need not be a
one-dimensional immigration-death process, and fast conservative binary
motion can change the relevant excursion phase.
