# Metropolis relaxation: counterexamples and a decreasing upper bound

**Scoped partial result; source-endpoint hold; independent review pending.**
This concerns Aldous's *Metropolis on Cayley graphs*, record 9700008.
The well-defined monotonicity question has a negative answer under the
standard Metropolis and relaxation-time conventions. A comparison with the
uniform endpoint also fails uniformly over Cayley graphs. An elementary
decreasing bound is proved below. The source's separate expression
\(\tau(\infty)\) is undefined in its stated parametrization, so the full
bundled source question is not declared solved.

## 1. Exact source and conventions

[The original problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/cayley.html)
specifies \(0<p<1\), takes \(T_p\) geometric with success probability
\(p\), and sets \(\mu_p=\mathcal L(X(T_p-1))\), with the walk started
at the identity. It explicitly defines \(\mu_0\) to be uniform. It then
asks whether relaxation decreases in \(p\), for a universal comparison
with \(\tau(\infty)\), and for decreasing bounds involving familiar graph
parameters. The infinity notation occurs twice and is not defined on
that page. We do not silently replace it by either endpoint.

Use a connected undirected Cayley graph with \(N\ge2\) vertices and a
symmetric generating set of size \(d\ge1\), without the identity.
Write \(P(x,y)=1/d\) for neighbors and zero otherwise. More generally,
the decreasing bound below holds on any finite connected simple regular
graph. With \(q=1-p\), the geometric convention is explicitly

\[
\mathbb P(T_p=t)=p q^{t-1}\quad(t\ge1),\qquad
\mu_p=p\sum_{t\ge0}q^t\delta_e P^t.
\tag{1}
\]

The Metropolis transition matrix is

\[
K_p(x,y)=P(x,y)\min\{1,\mu_p(y)/\mu_p(x)\}\quad(x\ne y),
\tag{2}
\]

with the remaining probability on the diagonal. The measure is strictly
positive for \(0<p<1\), and detailed balance holds. We use

\[
\tau(p)=\frac1{1-\lambda_2(K_p)},
\tag{3}
\]

where \(\lambda_2\) is the second largest eigenvalue in algebraic order.
These are the conventions in Aldous--Fill's
[Metropolis definition](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch11.S2.html)
and [relaxation-time definition](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch4.S4.html).
The explicit four-vertex counterexample below also works if one uses the
absolute nontrivial eigenvalue instead, and after fixed lazification.

## 2. Exact complete-graph calculation

Take the cyclic group \(\mathbb Z/N\mathbb Z\) with every nonzero element
as a generator. Its Cayley graph is \(K_N\). By symmetry let
\(a=\mu_p(e)\) and \(b=\mu_p(x)\) for \(x\ne e\).
The resolvent equation \(\mu_p=p\delta_e+q\mu_pP\), together with
\(a+(N-1)b=1\), gives

\[
a=\frac{1+(N-2)p}{N-p},\qquad
b=\frac{1-p}{N-p},\qquad
r=\frac ba=\frac{1-p}{1+(N-2)p}.
\tag{4}
\]

From the identity the chain moves to each other vertex with probability
\(r/(N-1)\) and stays with probability \(1-r\). From a nonidentity
vertex it moves to every other vertex with probability \(1/(N-1)\).
The subspace of functions vanishing at \(e\) and summing to zero on the
other vertices has dimension \(N-2\) and eigenvalue \(-1/(N-1)\).
On the remaining two-dimensional subspace, constant on nonidentity
vertices, the matrix is

\[
\begin{pmatrix}
1-r&r\\
1/(N-1)&(N-2)/(N-1)
\end{pmatrix}.
\tag{5}
\]

Its eigenvalues are \(1\) and
\(\lambda_*=(N-2)/(N-1)-r\). Since
\(\lambda_*-(-1/(N-1))=1-r\ge0\), this is the second largest
eigenvalue. Consequently

\[
\boxed{\quad
\tau_{K_N}(p)=\frac{(N-1)(1+(N-2)p)}{N-p}.
\quad}
\tag{6}
\]

Its derivative is

\[
\tau_{K_N}'(p)=\frac{(N-1)^3}{(N-p)^2}>0.
\tag{7}
\]

Thus the proposed nonincreasing behavior fails, even on complete Cayley
graphs. This uses the stated success-probability parameter, not its inverse
or the expected stopping time.

For a concrete example unaffected by the distinction between the ordinary
and absolute spectral gap, take \(N=4\). At \(p=1/2\), the stationary
weights are \((4,1,1,1)/7\) and the nontrivial eigenvalues are
\(5/12,-1/3,-1/3\), giving \(\tau=12/7\). At \(p=3/4\), the weights
are \((10,1,1,1)/13\), with nontrivial eigenvalues
\(17/30,-1/3,-1/3\), giving \(\tau=30/13>12/7\).
In both cases the displayed positive eigenvalue is largest in absolute
value as well. Replacing \(K_p\) by \((1-\theta)I+\theta K_p\), with
fixed \(0<\theta\le1/2\), multiplies relaxation times by \(1/\theta\)
and preserves the strict inequality.

## 3. A conditional endpoint comparison is false

If the source's undefined endpoint were intended to mean \(p=0\), no
universal constant \(C\), independent of the graph and \(p\), could give
\(\tau(p)\le C\tau(0)\). Indeed, (6) gives

\[
\tau_{K_N}(0)=\frac{N-1}{N},\qquad
\frac{\tau_{K_N}(1/2)}{\tau_{K_N}(0)}
=\frac{N^2}{2N-1}\longrightarrow\infty.
\tag{8}
\]

The counterexample keeps \(p=1/2\) fixed; no limiting stationary
distribution with zero weights is used. Degrees here grow with \(N\).
Thus it refutes a constant uniform over the finite Cayley graphs in the
source, not a separate bounded-degree formulation.

The same conclusion holds with the absolute-gap convention: for
\(N\ge4\), \(\tau_{\mathrm{abs}}(0)=(N-1)/(N-2)\), whereas at
\(p=1/2\) the ordinary and absolute relaxation times agree. Their ratio
is \(N(N-2)/(2N-1)\), again unbounded. Fixed lazification after forming
the chain leaves the ordinary-gap ratio in (8) unchanged.

For completeness, lazifying the *proposal* before both constructions does
not rescue monotonicity either. If its off-diagonal entries are
\(\theta/(N-1)\), \(0<\theta\le1\), then

\[
\frac ba=\frac{(1-p)\theta}{(N-1)p+(1-p)\theta},\qquad
\tau(p)=\frac1{\theta\{b/a+1/(N-1)\}}.
\tag{9}
\]

The ratio \(b/a\) strictly decreases, so \(\tau\) strictly increases.
For each \(N\), the ratio of its \(p\uparrow1\) limit to its value at
zero is \(N\). Equation (9) is an explicit variant; it is not needed
for the simple-random-walk counterexample.

## 4. A decreasing bound on every finite regular graph

For the conventions in Section 1,

\[
\boxed{\qquad \tau(p)\le\frac{d(N-1)}p,
\qquad 0<p<1.\qquad}
\tag{10}
\]

This is a coarse bound in terms of the requested graph parameters. Its
right-hand side decreases in \(p\). It does not require a definition of
\(\tau(\infty)\).

Write \(\mu=\mu_p\). Symmetry of \(P\) turns the resolvent equation into

\[
\mu(x)=p\mathbf 1_{\{x=e\}}+\frac{1-p}{d}\sum_{y\sim x}\mu(y).
\tag{11}
\]

The identity is the unique maximum of \(\mu\): a maximizing vertex
different from the identity would satisfy
\(\mu(x)\le(1-p)\max\mu<\max\mu\), a contradiction.

Orient each edge whose endpoint weights differ from the larger weight to
the smaller weight, and give it the nonnegative flow

\[
F(x,y)=\frac{1-p}{dp}\bigl(\mu(x)-\mu(y)\bigr)
\quad\hbox{when }\mu(x)>\mu(y).
\tag{12}
\]

Equal-weight edges carry zero flow. The outgoing minus incoming flow at
vertex \(x\) is, by (11),

\[
\sum_{y\sim x}\frac{1-p}{dp}(\mu(x)-\mu(y))
=\mathbf1_{\{x=e\}}-\mu(x).
\tag{13}
\]

The orientation has no directed cycle, since weights strictly decrease
along every positive-flow edge. Thus this finite flow decomposes into
weighted paths starting at \(e\) and ending at each \(x\ne e\), with
total terminal weight \(\mu(x)\). One precise way to see this is to
adjoin a sink, add an edge from each \(x\ne e\) to that sink carrying
\(\mu(x)\), and decompose the resulting acyclic source-sink flow.
Deleting the last edge gives the asserted paths. Every such path has at
most \(N-1\) edges. The remaining mass \(\mu(e)\) may be assigned to
the zero-length path.

If \(\mu(x)>\mu(y)\), then \(y\ne e\) and (11) gives
\(\mu(y)\ge(1-p)\mu(x)/d\). Therefore

\[
F(x,y)\le\frac{\mu(y)}p
=\frac1p\min\{\mu(x),\mu(y)\}.
\tag{14}
\]

For any real function \(f\), apply Cauchy--Schwarz along the paths and
then sum against their weights. The result is

\[
\begin{aligned}
\operatorname{Var}_{\mu}(f)
&\le \sum_x\mu(x)(f(x)-f(e))^2\\
&\le (N-1)\sum_{\mu(x)>\mu(y)}F(x,y)(f(x)-f(y))^2\\
&\le\frac{d(N-1)}p\,\mathcal E_{K_p}(f,f),
\end{aligned}
\tag{15}
\]

because the Metropolis Dirichlet form is

\[
\mathcal E_{K_p}(f,f)
=\sum_{\{x,y\}\in E}\frac{\min\{\mu(x),\mu(y)\}}d
                  (f(x)-f(y))^2.
\tag{16}
\]

The sums over edges in these formulas count each unordered edge once;
there is no extra factor of two. The
[variational characterization of relaxation time](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S6.html)
now proves (10). \(\square\)

## 5. Verification and precise remaining hold

The complete-graph spectral calculation and the flow argument are separate
substantive routes, using two of the five allowed attempts. Exact rational
checks verify the resolvent, detailed balance, invariant eigenspaces,
counterexample eigenvalues, and flow divergence and capacity inequalities
on finite examples. They supplement the proofs above and do not replace
the all-graph flow decomposition argument.

The mathematical conclusions are: nonincreasing relaxation is false;
a comparison with \(\tau(0)\) has no graph-independent constant; and
the explicit decreasing bound (10) holds. The universal comparison written
with \(\tau(\infty)\) has not been adjudicated, because that quantity has
no definition in the stated source model. An intended alternative
parametrization or endpoint could change the comparison question.
The package therefore retains a source-scope hold on the full bundled
record, rather than announcing a solution to an unstated correction.

The calculations use established Metropolis, resolvent and Poincaré
principles. Historical novelty is unconfirmed. A separate adversarial
review is required before publication of the claimed partial results.
