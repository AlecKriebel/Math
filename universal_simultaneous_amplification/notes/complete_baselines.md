# Complete-graph baselines derived from the count chain

Let `n >= 2`, let `k` be the current number of mutants, and write
`phi_k` for the probability of eventual fixation from that count.  Self-loops
do not enter the standard increment calculation.  If `p_k^+` and `p_k^-` are
the probabilities of moving to `k+1` and `k-1`, respectively, then

\[
 p_k^+(\phi_{k+1}-\phi_k)=p_k^-(\phi_k-\phi_{k-1}).
\]

Thus, with `gamma_k=p_k^-/p_k^+` and
`Delta_k=phi_k-phi_{k-1}`,

\[
 \Delta_{k+1}=\gamma_k\Delta_k,
 \qquad
 \phi_1=\left(1+\sum_{j=1}^{n-1}\prod_{k=1}^j\gamma_k\right)^{-1}.
\]

## Birth--death

Directly from the update rule,

\[
 p_k^+=\frac{rk}{rk+n-k}\frac{n-k}{n-1},\qquad
 p_k^-=\frac{n-k}{rk+n-k}\frac{k}{n-1}.
\]

Consequently `gamma_k=1/r` and

\[
 \boxed{\rho_{\rm Bd}(K_n,r)=\frac{1-r^{-1}}{1-r^{-n}}.}
\]

In particular,

\[
 \rho_{\rm Bd}(K_n,r)
 =\frac1n+\frac{n-1}{2n}(r-1)+O((r-1)^2),
 \qquad
 \lim_{r\to\infty}\rho_{\rm Bd}(K_n,r)=1.
\]

## Death--birth

If a resident dies, there are `k` mutant and `n-k-1` resident
competitors.  If a mutant dies, there are `k-1` mutant and `n-k`
resident competitors.  Hence

\[
 p_k^+=\frac{n-k}{n}\frac{rk}{rk+n-k-1},\qquad
 p_k^-=\frac{k}{n}\frac{n-k}{r(k-1)+n-k}.
\]

Put `A_k=n-1+(r-1)k`.  The ratio telescopes:

\[
 \gamma_k=\frac{A_k}{rA_{k-1}},\qquad
 \prod_{k=1}^j\gamma_k=\frac{A_j}{(n-1)r^j}.
\]

The finite sum simplifies to

\[
 \sum_{j=0}^{n-1}A_jr^{-j}
 =\frac{nr}{r-1}\bigl(1-r^{-(n-1)}\bigr),
\]

so

\[
 \boxed{
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}\frac{1-r^{-1}}{1-r^{-(n-1)}}.}
\]

For `n >= 3`, its endpoint expansions are

\[
 \rho_{\rm dB}(K_n,r)
 =\frac1n+\frac{n-2}{2n}(r-1)+O((r-1)^2),
\]

and

\[
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}-\frac{n-1}{nr}+O(r^{-2}).
\]

For `n=2`, dB fixation is exactly `1/2` for every `r`: after a death,
the unique neighbor must reproduce.

