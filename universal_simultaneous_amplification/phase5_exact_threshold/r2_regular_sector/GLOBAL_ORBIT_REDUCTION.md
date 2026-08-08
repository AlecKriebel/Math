# What the killed-sector method does and does not prove globally

Date: 2026-08-08 (America/Los_Angeles)

## Setup

Let \(M\in\mathcal P_n\) be invariant under a transposition \(U\), and let
\(D=D^{\mathsf T}\) have zero diagonal and row sums, with
\(UDU=-D\).  Put

\[
 P_t=M+tD,qquad \phi(t)=\rho_{\rm dB}(P_t,2).
\]

Uniform singleton initialization and conjugacy give \(\phi(t)=\phi(-t)\).
All statements below concern the interval on which every entry of \(P_t\)
is nonnegative.

## Exact center-sector curvature identity

Let \(L_t\) be the transient generator, \(g=h_0\) its fixation committor at
\(t=0\), and \(\mu=(-L_0)^{-T}\alpha\) the midpoint occupation measure.
Write

\[
 L_j=\left.\frac{d^jL_t}{dt^j}\right|_{t=0},qquad
 G_-=(-L_0|_{\mathrm{odd}})^{-1}.
\]

Because \(L_0\) commutes with \(U\), \(L_1\) switches parity, and \(L_2\)
preserves parity.  Differentiating the absorbing equations twice gives the
exact identity

\[
 \boxed{
 \phi''(0)=
 \langle\mu,L_2g\rangle
 +2\langle\mu,L_1G_-L_1g\rangle.}                 \tag{1}
\]

The first term is nonpositive.  Indeed, along every affected hypercube
edge, \(h''(x)=-4/(1+x)^3<0\), while the fixation committor is monotone.
The second term is the odd excursion feedback.  Thus local concavity at an
arbitrary transposition-invariant regular midpoint is equivalent to the
single scalar inequality

\[
 2\langle\mu,L_1G_-L_1g\rangle
 \leq-\langle\mu,L_2g\rangle.                       \tag{2}
\]

This is exactly the infinitesimal form of the phase-four finite-amplitude
sector inequality.  The odd Green operator has the inherited killing bound
because configurations containing exactly one swapped vertex are killed at
rate at least one.  The local theorem in
`LOCAL_COMPLETE_HESSIAN_THEOREM.md` proves (2) when \(M=J_n\), using the
additional rank/cut structure available there.

## Finite-amplitude midpoint identity

For a fixed amplitude \(t\), set

\[
 L_{\rm av}(t)=\frac{L_t+UL_tU}{2},\qquad
 B(t)=\frac{L_t-UL_tU}{2},\qquad
 C(t)=L_0-L_{\rm av}(t).
\]

Let \(g_t\) be the even part of the endpoint committor and let
\(G_-(t)=(-L_{\rm av}(t)|_{\rm odd})^{-1}\).  The exact phase-four identity
is

\[
 \phi(0)-\phi(t)=
 \left\langle\mu,
 \{C(t)-B_{+-}(t)G_-(t)B_{-+}(t)\}g_t
 \right\rangle.                                    \tag{3}
\]

Consequently, the global transposition-midpoint conjecture is reduced,
for each amplitude, to the same **type** of killed-sector comparison as
(2): finite concavity bonus versus finite odd feedback.  Coverage and odd
killing alone do not prove its sign; the phase-four exact coverage extreme
ray counterexample still applies.  The missing input is a bound using that
\(g_t\) is the averaged endpoint harmonic committor (or, dually, the
stationarity constraints on its coverage measure).

## Why orbit-wide differential concavity is a different problem

At a noncentral point \(t\ne0\), \(L_t\) does not commute with the
transposition.  Direct differentiation gives

\[
 \boxed{
 \phi''(t)=\langle\mu_t,L_t''h_t\rangle
 +2\langle\mu_t,L_t'(-L_t)^{-1}L_t'h_t\rangle,}      \tag{4}
\]

where \(h_t\) and \(\mu_t\) are the endpoint committor and occupation
measure.  The inverse in (4) is the full transient Green operator, not the
killed odd Green operator.  The transposition sends \(L_t\) to \(L_{-t}\),
not to itself, so parity no longer closes.  A two-layer lift carrying both
\(L_t\) and \(L_{-t}\) restores a formal involution, but each parity block
is unitarily equivalent to the full endpoint generator and acquires no
rate-one killing.  Thus orbit-wide concavity does **not directly reduce**
to the surviving killed-sector estimate.

This is a structural separation, not a counterexample to orbit-wide
concavity.  The efficient global route remains (3), which compares the
center directly with each conjugate endpoint and retains odd killing.

## Exact order-four check (evidence only)

For the inherited regular order-four endpoint

\[
 (a,b,c)=(7/10,1/5,1/10)
\]

and the transposition swapping the first two vertices, parameterize the
orbit from midpoint to endpoint by replacing \(b,c\) with
\(3/20\pm x/20\).  Exact labelled-chain solution simplifies to

\[
 \phi(x)=\frac{101x^2-71629}{2(69x^2-85241)},
\]

and hence

\[
 \phi''(x)=
 \frac{3666940(207x^2+85241)}{(69x^2-85241)^3}<0
 \qquad(|x|\leq1).
\]

So this hostile order-four test is globally concave.  It is an exact
example, not an all-graph theorem.
