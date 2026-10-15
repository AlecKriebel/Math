# A sharp obstruction for one common sign sequence across all partition factors

**Public evidence note.** The finite obstruction below uses computer-assisted exhaustive enumeration. The complete recurrence, state domains, counts, explicit sharpness witnesses and substantive independent review are distributed in prose. The programs and raw frontier certificates used in the historical verification are not distributed in this appendix. This is not an executable public replay package; independent reimplementation is possible from the mathematical specification.


## Statement and scope

Let
\[
f(z)=1+\sum_{j\ge1}s_jz^j,\qquad s_j\in\{-1,1\},
\quad P_f(q)=\prod_{m\ge1}f(q^m).
\]
The signs \(s_j\) are completely arbitrary. There is no periodicity, rationality, digit-multiplicativity, or geometric-series assumption. The restriction is that **the same multiplicity-sign sequence is used in every original factor**: \(\epsilon_{m,j}=s_j\) for every \(m\).

**Theorem (computer-assisted, sharp in this class).** Every such product has a coefficient outside \(\{-1,0,1\}\) in degrees 1 through 81. There is exactly one sign prefix \((s_1,\ldots,s_{80})\) for which all coefficients through degree 80 lie in that set. Thus 81 is the first unavoidable obstruction degree in this common-factor class.

This is an authored partial result, not a solution of Newman's unrestricted problem. The unrestricted signs need not agree across factors. No novelty claim is made.

## 1. Complete finite recurrence

For a sign prefix \(s=(s_1,\ldots,s_N)\), put
\[
f_s(z)=1+\sum_{j=1}^N s_jz^j,
\qquad Q_s(q)=\prod_{m=1}^N f_s(q^m).
\]
Call \(s\) feasible if all coefficients of \(Q_s\) through degree \(N\) have absolute value at most 1. Terms and factors omitted here cannot affect that prefix of the product.

Start with the unique empty state. From a feasible prefix of length \(N-1\), let
\[
A_N=[q^N]\prod_{m=1}^N f_s(q^m).
\]
Append **each** \(e\in\{-1,1\}\) satisfying
\[
|A_N+e|\le1. \tag{1}
\]
The fresh sign \(s_N=e\) appears first as \(eq^N\) in factor \(m=1\). Its appearances in all other factors begin at degrees \(mN>N\). The new degree-\(N\) term only multiplies constants when computing the degree-\(N\) coefficient. Therefore (1) is the exact extension test, and no earlier coefficient changes.

Induction now proves completeness: every retained child is feasible, and every feasible child restricts to a feasible parent and passes precisely (1). There is no random search, depth budget, state merging, symmetry pruning, or heuristic truncation.

## 2. Arithmetic and exhaustive verification

The producer computes truncated products directly by convolution. For each factor \(m\), if the current array is \(u\), replace it by
\[
v_k=\sum_{0\le j\le\min(N,\lfloor k/m\rfloor)}s_j u_{k-mj},
\quad s_0=1,
\]
using the old array throughout that factor update. It records every feasible sign string at every degree, encoding \(-1\) by `0` and \(+1\) by `1`.

The full frontier counts, starting at degree zero and ending at degree 81, are

```
1,2,2,3,6,10,15,19,16,7,3,3,6,12,18,13,20,22,30,24,
27,15,10,14,18,10,8,7,3,5,5,4,6,10,9,14,22,28,40,62,
36,34,25,34,45,21,16,10,12,21,21,23,28,42,45,35,34,19,
14,10,12,14,13,19,10,6,4,6,6,10,6,9,9,4,4,3,4,5,5,3,1,0.
```

There are 1,227 nonempty states in total, counting the root. The largest frontier has 62 states, at degree 39. The historical independent review compared the complete state sets, not just their cardinalities. Those raw frontiers are not distributed here.

A separate verifier uses logarithmic derivatives instead of the producer's convolution. For any finite prefix, put missing \(s_j=0\) and define
\[
b_n=ns_n-\sum_{k=1}^{n-1}b_ks_{n-k}. \tag{2}
\]
Multiplication by \(f_s\) shows that \(\sum_{n\ge1}b_nz^n=zf_s'(z)/f_s(z)\). Hence
\[
h_n=\sum_{d\mid n}\frac nd b_d
\quad\text{and}\quad
\nu_0=1,\qquad n\nu_n=\sum_{k=1}^nh_k\nu_{n-k} \tag{3}
\]
reconstruct the coefficients of \(\prod_{m\ge1}f_s(q^m)\). The formal inverse exists because \(f_s(0)=1\); the polynomial may have zero coefficients beyond its prefix with no problem.

The verifier recomputes **all** possible children using (2)–(3), checks the certified sets exactly, and checks the root, domains, uniqueness, first-empty level, cardinalities, witness, and terminal residual. Every division by \(n\) in (3) is checked to be integral. Deliberate deletion of a feasible state, insertion of an infeasible state, an invalid sign, duplicate state, and wrong witness coefficient are all rejected. Normal Python and optimization levels 1 and 2 give the same acceptance; no proof check relies on a removable assertion.

## 3. The unique terminal prefix and sharpness

The unique length-80 sign string is

```
01001011010010110100101101001011010010110100101101001011010010101001010010011101
```

The constant coefficient is 1; the first character specifies \(s_1\). Exact multiplication produces the following coefficients of degrees 0 through 80:

```
1,-1,0,-1,-1,1,1,1,0,0,0,0,-1,1,-1,0,1,-1,-1,0,-1,
0,0,1,1,0,0,0,0,1,0,0,1,-1,0,-1,-1,1,1,1,0,-1,0,-1,
-1,0,0,0,1,-1,0,-1,-1,1,1,0,1,0,0,0,-1,1,0,1,0,0,0,
-1,1,1,0,-1,1,-1,0,0,1,-1,0,0,0.
```

Its degree-81 residual is \(A_{81}=-4\). The only two possible new coefficients are therefore \(-5\) and \(-3\), and neither is allowed. Completeness of the certified frontiers proves the universal obstruction at 81.

For sharpness, extend this prefix by any signs beyond 80, for example all +1. This defines one full series \(f\) and every original factor \(f(q^m)\). Later signs cannot affect degrees at most 80, so the displayed admissible prefix is achieved by an infinite product. This is not a claim that its later coefficients are bounded.

## 4. Context and limitations

[Newman's unrestricted problem](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions) permits independent signs in different factors. The theorem here adds a common-factor restriction, distinct from changing only finitely many original factors or imposing binary-digit multiplicativity separately in each factor.

[Andrews and Newman, *Binary Representations and Theta Function*, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf), obtain common-series identities over particular sets of dilates. In this theorem every positive integer dilation remains present. Their odd-dilate identities do not contradict this obstruction.

This calculation is not a search for an unrestricted degree record, and it proves no finite-degree impossibility for independently chosen arrays \(\epsilon_{m,j}\). It shows that a solution cannot use one identical sign sequence across all factors. There is no assumption that zero-free signed series must be geometric or binary-digit multiplicative.
