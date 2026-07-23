# The restricted-witness collision program

This note isolates the exact probabilistic/combinatorial estimate suggested by
the protected construction. It is a research target, not a theorem.

## 1. Witnesses and fibers

Fix \(m\ge2\) and \(P\subseteq[2m]\) with \(1\in P\). A signed index
\(b\in J_m\) is *safe* when its generator \(G_{m,P}(b)\) avoids \(-m\).
Equivalently,

\[
|b|<m
\qquad\text{and}\qquad
m+b\notin P.
\]

A restricted witness chooses, independently for each \(1\le t<m\), either
no sign, the safe sign \(+t\), or the safe sign \(-t\), but never both signs.
For a central signature \(C\), let

\[
d_{P,C}
=
\#\{B:B\text{ is restricted and }\Phi_{m,P}(B)=C\}.
\]

Define

\[
W_m=\sum_{\substack{P\subseteq[2m]\\1\in P}}\sum_C d_{P,C},
\qquad
Q_m=\sum_{\substack{P\subseteq[2m]\\1\in P}}\sum_C d_{P,C}^2,
\]

and let

\[
D_m=\sum_{\substack{P\subseteq[2m]\\1\in P}}
\#\{C:d_{P,C}>0\}.
\]

Every restricted output avoids \(-m\), so

\[
D_m\le
\sum_{\substack{P\subseteq[2m]\\1\in P}}R_m(P).
\]

## 2. Exact witness count

For each \(t<m\), the availability of \(+t\) is determined by
\(m+t\notin P\), while the availability of \(-t\) is determined by
\(m-t\notin P\). The special condition \(1\in P\) suppresses the sign
\(-(m-1)\).

Summing the number of choices over all \(P\) gives

\[
W_m=12\cdot8^{m-2}=\frac{3}{16}8^m.
\]

## 3. What a collision estimate would give

Global Cauchy--Schwarz gives

\[
W_m^2
\le D_m Q_m.
\]

Consequently, an absolute constant \(K\) for which

\[
Q_m\le K mW_m
\]

holds for all \(m\) would imply

\[
\sum_{\substack{P\subseteq[2m]\\1\in P}}R_m(P)
\ge D_m
\ge \frac{W_m}{Km}
=\frac{3}{16K}\frac{8^m}{m}.
\]

would prove the desired trace scale. Exact data below rule out this particular
second-moment estimate. The Cauchy--Schwarz implication remains useful for
diagnosing why the method fails, but is no longer the primary conjecture.

Even a direct bound

\[
D_m\gg\frac{8^m}{m}
\]

would suffice for the trace scale. It does **not**, by itself, prove a lower
bound on \(E_m\): a separate trace-to-excess lemma is still required.

## 4. Exact data and the first failed constant

The exact reference computation gives:

| \(m\) | \(W_m\) | \(Q_m\) | \(D_m\) | \(\max d_{P,C}\) | \(Q_m/W_m\) |
|---:|---:|---:|---:|---:|---:|
| 2 | 12 | 12 | 12 | 1 | 1.000000 |
| 3 | 96 | 108 | 90 | 2 | 1.125000 |
| 4 | 768 | 1,056 | 658 | 4 | 1.375000 |
| 5 | 6,144 | 11,852 | 4,622 | 10 | 1.929036 |
| 6 | 49,152 | 143,940 | 32,430 | 24 | 2.928467 |
| 7 | 393,216 | 1,846,940 | 228,390 | 62 | 4.697011 |
| 8 | 3,145,728 | 26,055,940 | 1,558,256 | 162 | 8.282960 |
| 9 | 25,165,824 | 392,088,996 | 10,641,362 | 445 | 15.580217 |
| 10 | 201,326,592 | 6,117,877,500 | 72,968,176 | 1,088 | 30.387826 |

The attractive sharp conjecture \(Q_m\le mW_m\) first fails at \(m=8\):

\[
Q_8-8W_8=890{,}116.
\]

The ratio \(Q_m/W_m\) then nearly doubles at each of \(m=9,10\).
Consequently, even the weaker estimate \(Q_m=O(mW_m)\) is empirically
implausible. High multiplicities have enough witness mass to destroy the
unweighted second moment.

The distinct-output count behaves very differently:

| \(m\) | \(mD_m/8^m\) | \(W_m/D_m\) |
|---:|---:|---:|
| 2 | 0.375000 | 1.000000 |
| 3 | 0.527344 | 1.066667 |
| 4 | 0.642578 | 1.167173 |
| 5 | 0.705261 | 1.329295 |
| 6 | 0.742264 | 1.515634 |
| 7 | 0.762334 | 1.721687 |
| 8 | 0.743034 | 2.018749 |
| 9 | 0.713559 | 2.364906 |
| 10 | 0.679569 | 2.759101 |

Through \(m=10\), the desired direct inequality \(D_m\gg8^m/m\) remained
numerically plausible even though the second moment was the wrong instrument.
Larger sampled diagnostics through \(m=20\) show continued decay in
\(mD_m/8^m\), while conditional witness entropy grows roughly linearly.
Accordingly this route is now secondary: neither an \(O(\log m)\) decoding
loss nor a uniform positive lower bound for \(mD_m/8^m\) is well supported.

## 5. Current proof questions

1. Determine whether the observed decay in \(mD_m/8^m\) is polynomial or
   exponential; do not assume the direct bound remains true.
2. Does a truncation of high-multiplicity fibers retain
   \(\Omega(8^m)\) witness mass while having multiplicity \(O(m)\)?
3. Is the conditional Shannon entropy loss of a random witness at most
   \(\log m+O(1)\), despite its exponentially worse Rényi-2 loss?
4. Can one choose a canonical representative from each fiber and encode every
   witness by that representative plus \(O(m)\) possibilities on average?
5. Can trace signatures be injected, after averaging over \(P\), into the
   union-shadow excess counted by \(E_m\)?
