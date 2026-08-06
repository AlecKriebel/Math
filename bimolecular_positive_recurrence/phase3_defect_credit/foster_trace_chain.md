# Foster and trace-chain conclusion

This section gives the countable-state Markov-chain argument used after the
network certificate has been constructed.

## Theorem

Let \(X\) be a nonexplosive irreducible continuous-time Markov chain on a
countable state space \(E\). Suppose there are a finite nonempty set \(K\), a
proper function \(V:E\to[0,\infty)\), and

\[
\mathcal LV(x)\le-1,
\qquad x\notin K.
\]

Assume \(V\) is in the local domain of the generator: on every finite set the
jump sum defining \(\mathcal LV\) is finite. Then every state is positive
recurrent.

## Proof

### 1. Finite expected hitting time of K

Let

\[
\tau_K=\inf\{t\ge0:X_t\in K\},
\qquad
\tau_R=\inf\{t\ge0:V(X_t)\ge R\}.
\]

Stop at \(T_{t,R}=t\wedge\tau_K\wedge\tau_R\). Before this stopping time the
chain lies in the finite sublevel set \(\{V<R\}\), so the stopped Dynkin
martingale is integrable. Therefore

\[
\mathbb E_xV(X_{T_{t,R}})
=
V(x)+\mathbb E_x\int_0^{T_{t,R}}\mathcal LV(X_s)\,ds
\le
V(x)-\mathbb E_xT_{t,R}.
\]

Since \(V\ge0\),

\[
\mathbb E_xT_{t,R}\le V(x).
\]

Let \(R\to\infty\). Nonexplosion excludes infinitely many jumps accumulating
before finite time, and properness excludes escape through infinitely many
finite sublevels without \(V\to\infty\). Monotone convergence gives

\[
\mathbb E_x(t\wedge\tau_K)\le V(x).
\]

Then \(t\to\infty\) yields

\[
\mathbb E_x\tau_K\le V(x)<\infty.
\]

### 2. Finite return time to K

For \(k\in K\), let \(T_1\) be the first genuine jump time. Its expectation is
finite because the total rate at a fixed state is finite and positive unless
\(K=\{k\}\) is an absorbing singleton, in which case the result is immediate.
Only finitely many states can be reached from \(k\) in one jump. Hence

\[
\mathbb E_k\tau_K^+
\le
\mathbb E_kT_1+
\max_{y:q(k,y)>0}\mathbb E_y\tau_K
<\infty.
\]

Taking the maximum over the finite set K gives a uniform finite bound on the
mean duration of one K-to-K excursion.

### 3. Irreducibility of the trace chain

Observe the successive return states in K. For \(k,\ell\in K\), irreducibility
of \(X\) supplies a finite state path from \(k\) to \(\ell\). Deleting the
intermediate visits to K decomposes that path into trace transitions with
positive probability. Thus the trace chain on K is irreducible.

Fix \(k_*\in K\). Because K is finite and the trace chain is irreducible,
for every \(k\in K\) choose a trace path to \(k_*\). The product of its
positive transition probabilities is positive. Taking the minimum over K
gives \(p>0\); taking the maximum path length gives \(m<\infty\). In each
block of m trace transitions, conditional on the past, the chance to hit
\(k_*\) is at least p. The number of blocks is therefore dominated by a
geometric random variable of mean \(1/p\). The expected number of K-excursions
before hitting \(k_*\) is finite.

Each excursion has mean duration bounded by the uniform constant from Step 2.
Consequently

\[
\mathbb E_{k_*}\tau_{k_*}^+<\infty.
\]

Thus \(k_*\), and hence every state by irreducibility, is positive recurrent.
\(\square\)

## Random-time version

The same trace-chain conclusion applies to episode stopping times. If outside
K an episode rule satisfies

\[
\mathbb E_x[V(X_{\sigma_x})-V(x)]\le-g(x),
\qquad
\mathbb E_x\sigma_x\le Cg(x),
\]

and every episode contains a genuine jump unless K is reached, then summing
up to the nth episode gives

\[
\mathbb E\sum_{j<n}g(Y_j)\le V(x),
\qquad
\mathbb E T_n\le CV(x).
\]

Monotone convergence and nonexplosion rule out accumulation of infinitely
many genuine-jump episodes in finite time. Hence K is reached in finite mean
time, and Steps 2-3 apply unchanged.
