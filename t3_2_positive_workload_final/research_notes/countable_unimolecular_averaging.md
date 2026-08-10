# Countable unimolecular averaging for a one-active physical phase

## 1. Scope

This note replaces a false finite-box step in the one-active repair. A fast
cofactor phase can be positive recurrent with a product-Poisson law and still
leave every fixed box before a slow service reaction occurs. The correct
object is the full countable phase on physical time.

The result below is a quantitative averaging lemma for exactly the processes
obtained after stripping one copy of a large active species from

\[
 X+\{0,U,V\}.
\]

It proves the analytic clock estimate needed by an actual-target carrier. It
does **not**, by itself, prove the complete one-active recurrence theorem: the
finite marked return graph, unresolved-arrival accounting, and tube-to-global
Foster composition must still be supplied.

## 2. Stable linear phases

Let \(Y\) be a continuous-time Markov chain on \(\mathbb N_0^d\),
\(d\le2\), whose reactions have the forms

\[
 0\longrightarrow e_i,\qquad e_i\longrightarrow0,\qquad
 e_i\longrightarrow e_j.                              \tag{2.1}
\]

Its generator is \(Q\). Fix one closed irreducible class. There are two
stable cases relevant here.

1. The class is conservative. Its total particle number is fixed, so the
   class is finite.
2. Every species component fed by immigration has a directed path to a
   death edge. The independent-particle construction then gives an open
   stable linear network. Its stationary law \(\pi\) is a product of
   Poisson laws (zero means are allowed for absent components), and it has
   all exponential moments.

The third condensation-graph possibility is an immigrated closed species
component with no drain. Particle number then diverges on the fast clock; in
the tier proof this is an inactive-coordinate promotion, not a tight
environment.

For a polynomial \(f\), write \(\bar f=\pi f\). In a conservative class the
same notation means expectation under its finite stationary law.

### Lemma 2.1 (polynomial Poisson equation)

In either stable case, for every falling-factorial polynomial \(f\) of degree
at most two there is a function \(\chi_f\), polynomial of degree at most two
in the open case and bounded in the fixed conservative class, such that

\[
 Q\chi_f=f-\bar f.                                    \tag{2.2}
\]

The solution is unique after imposing \(\pi\chi_f=0\), modulo quantities
constant on the chosen class.

#### Proof

For an open stable linear network, particles move independently on the
finite type graph until death and immigration is Poisson. The first- and
second-factorial moment semigroups are finite-dimensional. Stability of the
single-particle traffic matrix makes every nonconstant mode on the chosen
class exponentially decaying. Hence

\[
 \chi_f(y)=-\int_0^\infty
       \bigl(\mathbb E_y f(Y_s)-\bar f\bigr)\,ds        \tag{2.3}
\]

converges. The integrand is a polynomial of degree at most two in \(y\), so
the integral is a polynomial of the same degree. Differentiating the
semigroup integral gives (2.2). On a finite conservative class the centered
generator is invertible on the complement of constants. \(\square\)

## 3. Acceleration with all slow reactions retained

Let \(Y^N\) have generator

\[
 \mathcal A_N=NQ+S,                                   \tag{3.1}
\]

where \(S\) is any finite collection of bounded-jump bimolecular
mass-action reactions. No slow reaction is deleted. Molecularity two has an
important consequence: a reaction which increases total particle number has
a source of molecularity zero or one and therefore an affine rate. A
quadratic slow reaction can only conserve or decrease total particle number.

### Lemma 3.1 (uniform fixed-time and occupation moments)

For every \(T,p<\infty\) and fixed finite set of initial phases \(K\), there
is \(C=C(T,p,K)\), independent of \(N\ge1\), such that

\[
 \sup_{y\in K}\left[
   \sup_{0\le t\le T}\mathbb E_y(1+|Y_t^N|)^p+
   \mathbb E_y\int_0^T(1+|Y_s^N|)^p\,ds
 \right]\le C.                                        \tag{3.2}
\]

The expectation cannot be moved outside the time supremum in (3.2). An
accelerated immigration--death process samples order \(N\) fast cycles on a
fixed physical interval, and its path maximum grows logarithmically with
\(N\).

#### Proof

The linear fast network is an immigration system of independent particles
with exponentially integrable lifetimes on a finite type graph. Accelerating
all particle and immigration clocks by the same factor leaves its
fixed-time population scale unchanged and only shortens its relaxation time.
A slow reaction can increase total population only at an affine rate.
Standard immigration--branching comparison, with the stable accelerated
particle semigroup retained rather than discarded, gives the fixed-time and
occupation moment bounds in (3.2). Slow quadratic conversions do not
increase total population. \(\square\)

A finite family of fast generators coupled by state-dependent slow mark
switches needs a joint polynomial Lyapunov estimate before (3.2) can be
used uniformly across marks. That calculation is not contained in this
lemma. The exact one-active phase isolated by the finite certificate has one
open immigration--death generator, so no such general extension is needed
there.

### Theorem 3.2 (quantitative countable-phase averaging)

Let \(f\) have degree at most two. For \(Y_0^N\) in a fixed finite set and
fixed \(T<\infty\),

\[
 \sup_{0\le t\le T}\mathbb E\left|
 \int_0^t\bigl(f(Y_s^N)-\bar f\bigr)\,ds
 \right|\le {C_T\over\sqrt N}.                         \tag{3.3}
\]

The supremum in (3.3) is outside the expectation; no uniform path-maximum
claim is made.

#### Proof

Use the solution from Lemma 2.1. Dynkin's formula gives

\[
\begin{aligned}
 \int_0^t(f(Y_s^N)-\bar f)\,ds
  ={}&{\chi_f(Y_t^N)-\chi_f(Y_0^N)\over N}
      -{M_t^N\over N}\\
    &-{1\over N}\int_0^t S\chi_f(Y_s^N)\,ds,           \tag{3.4}
\end{aligned}
\]

where \(M^N\) is the Dynkin martingale. Since \(\chi_f\) has degree at most
two, a bounded-jump difference of \(\chi_f\) has degree at most one. Its fast
carré du champ is a polynomial of finite degree multiplied by \(N\).
Lemma 3.1 therefore gives, uniformly for \(t\le T\),

\[
 \mathbb E|M_t^N|
 \le\bigl(\mathbb E\langle M^N\rangle_t\bigr)^{1/2}
 \le C_T\sqrt N.                                      \tag{3.5}
\]

The endpoint term and the integral involving \(S\chi_f\) are
\(O_{L^1}(1)\) before division by \(N\), again by Lemma 3.1. Equations
(3.4)--(3.5) prove (3.3).

This proves the assertion for the fixed fast generator \(Q\). A general
finite-mark version additionally requires a joint Lyapunov bound for the
mark-dependent correctors and compensator convergence for every competing
clock; it is deliberately not asserted here. \(\square\)

## 4. A physical slow clock has a uniform chance to ring

Let a retained slow channel have propensity \(\kappa f(Y)\), with
\(f\ge0\) and \(\bar f>0\). Construct its independent unit-exponential
threshold \(E\); the channel rings when

\[
 \kappa\int_0^t f(Y_s^N)\,ds\ge E.                     \tag{4.1}
\]

### Corollary 4.1 (no finite-box truncation)

There are \(T<\infty\), \(p>0\), and \(N_0\) such that, from every phase in a
fixed finite initial set,

\[
 \mathbb P\{\text{the channel rings by }T\}\ge p,
 \qquad N\ge N_0.                                     \tag{4.2}
\]

All other slow channels remain present.

#### Proof

Choose \(T\) so that \(\exp(-\kappa\bar fT/2)\le1/4\). By Theorem 3.2,

\[
 \mathbb P\left\{
 \int_0^T f(Y_s^N)\,ds<\bar fT/2
 \right\}\longrightarrow0.                            \tag{4.3}
\]

For all sufficiently large \(N\), the probability of no ring is at most
\(1/2\). Slow reactions are already part of \(S\) in (3.1), so none has
been suppressed. Take \(p=1/2\). \(\square\)

This is the precise replacement for the invalid assertion that tightness
can be turned into a fixed phase box. The process may visit arbitrarily
large cofactor states during \([0,T]\); the fixed-time and occupation
moments (3.2), not finite support, control those visits.

## 5. Finite marked return graphs: the remaining blueprint

The form needed by an actual-target return prefix is as follows, but it is
not a consequence of Theorem 3.2 without an additional marked-clock
tightness argument.
Let \(I\) be a finite set of path marks. In mark \(i\), the fast cofactor
generator is one of finitely many stable \(Q_i\). A slow marked edge
\(i\to j\) has rate \(f_{ij}(Y)\), of degree at most two, and makes a bounded
population jump. Averaging gives the finite generator

\[
 \bar q_{ij}=\pi_i f_{ij}.                             \tag{5.1}
\]

Every source enabled somewhere in the chosen closed phase class has positive
stationary average; a syntactically present edge whose source is absent from
that class can have zero average. To obtain finite-horizon convergence of
the competing marked clocks one must prove compensator convergence and
tightness jointly, not merely apply the scalar estimate (3.3) edge by edge.
Once that step is supplied, reachability of a service mark in the averaged
graph would give, from each mark in a fixed starting set, \(T,p>0\) such that

\[
 \mathbb P\{\text{service mark is hit by }T\}\ge p     \tag{5.2}
\]

for all sufficiently large \(N\). Endpoint cofactor populations would have
the required fixed-time polynomial moments under the corresponding joint
Lyapunov estimate.

For a one-active reaction network, fast top segments in the marked graph are
contracted with the actual-target carrier estimate. A successful entry and
its top exit have net active-coordinate reward zero. An interruption has
probability \(O(N^{-1})\) after its polynomial cofactor factor is averaged
using (3.2). Thus the remaining graph-theoretic obligations are finite and
exact:

1. show that every old-debt mark reaches an unpaired exit (service) in the
   averaged return graph, or else that active reward is a coboundary and
   hence a classwise affine invariant;
2. bound the total number of raw entry carriers launched before that hit;
3. combine the resulting \(p>0\) service probability with the
   \(O(N^{-1})\) unresolved-arrival mean; and
4. pay the entropy toll when an inactive coordinate leaves the one-active
   regime.

Items 1--4 are not consequences of Theorem 3.2 and remain the global
one-active gate. What is now removed is the earlier analytic obstruction: a
tight infinite-support environment supplies uniform physical slow clocks
through countable-phase averaging, never through an exact finite truncation.

## 6. Regression: why the fixed box is false

Consider

\[
 L_1=\{X,X+U\},\qquad
 L_2=\{X+V,U,V\},                                      \tag{6.1}
\]

with both directions on \(L_1\) and the strong cycle

\[
 X+V\longrightarrow U\longrightarrow V
       \longrightarrow X+V.                           \tag{6.2}
\]

At active level \(X=N\), the first linkage makes \(U\) an
immigration--death chain on the fast \(N\)-clock. A rare interrupted double
entry can leave one old unit of debt at \((U,V)=(1,0)\). Its service begins
with the slow edge \(U\to V\), after which \(X+V\to U\) is fast and lowers
\(X\).

Fix any box \(E_M=\{U,V\le M\}\). On the fast clock, the
immigration--death chain reaches \(U=M+1\) in an almost surely finite time
\(T_M\). Before that exit, the physical integrated \(U\to V\) hazard is

\[
 {\kappa\over N}\int_0^{T_M}U_s\,ds.
\]

Its expectation is \(C_M/N\), so the probability of service before leaving
the box tends to zero. In contrast, Corollary 4.1 applied on a fixed physical
interval gives a strictly positive service probability because the full
immigration--death law has positive mean \(U\).

Thus a stopped fixed-box kernel is false even in a stabilizing example. The
example is a regression against the proof method, not a counterexample to
T3-2.
