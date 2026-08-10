# A suppressed dormant carrier and its fast-shell repair target

## 1. Claim boundary

This note records an exact regression inside the 1,416 two-active promotion
incidences. It does not prove recurrence. Its purpose is to rule out a false
local argument and isolate the smallest quantitative shell lemma which
repairs that argument.

Up to the four species relabellings realized in the ordered residual table,
consider

\[
 L_0=\{U,I+V\},\qquad
 L_1=\{0,I,2I,I+U\},                                  \tag{1.1}
\]

where \(I\) is the inactive coordinate. Give \(L_0\) both directions and,
for the displayed regression, orient \(L_1\) as

\[
 0\longrightarrow I+U\longrightarrow2I
  \longrightarrow I\longrightarrow0.                 \tag{1.2}
\]

All displayed rates are arbitrary and strictly positive.

The exact promotion table contains four no-whole-top copies of (1.1) with

\[
 w_I=0,\qquad 2w_U-w_V=3>0.                            \tag{1.3}
\]

Their fingerprint is

```text
53911b366b023cfdc4e76f3bf8df99cd5a502252fb9df552268ea03ee7fae465
```

## 2. The isolated-block warning

Take the canonical copy \(I=A,U=B,V=C\), \(w=(0,4,5)\), and

\[
 x_N=(0,N^4,N^5).
\]

After the constant-rate reaction \(0\to A+B\), the rates of the two
load-bearing clocks are

\[
 \lambda_{A+C\to B}=\mu N^5,\qquad
 \lambda_{A+B\to2A}=\kappa(N^4+1).                    \tag{2.1}
\]

Every other newly enabled clock has rate \(O(N^4)\). Therefore

\[
 \mathbb P\{A+C\to B\hbox{ fires next}\}=1-O(N^{-1}). \tag{2.2}
\]

On this event the inactive coordinate returns to zero and the population
increment is

\[
 (\Delta A,\Delta B,\Delta C)=(0,2,-1).                \tag{2.3}
\]

For every fixed factorial-linear potential

\[
 {\cal F}_\ell(x)=\sum_i\log(x_i!)+\ell\cdot x,
\]

the increment is exactly

\[
 \Delta{\cal F}_\ell
 =\log\frac{(B+1)(B+2)}{C}+2\ell_B-\ell_C
 =3\log N+O(1).                                       \tag{2.4}
\]

Thus “create the inactive species and immediately follow a return prefix”
is not a valid common-entropy episode. The lower clock is kinetically
suppressed, and the dominant two-reaction endpoint is neither strict
factorial descent nor genuine promotion.

## 3. Why this is not a CTMC counterexample

The top linkage in (1.1) has two exact invariants

\[
 M=I+U,\qquad K=U+V.
\]

Writing \(i=I\) and \(D=K-M\), its one-dimensional shell is

\[
 U=M-i,\qquad V=D+i,                                   \tag{3.1}
\]

with birth and death rates

\[
 b_i=\alpha(M-i),\qquad d_i=\mu i(D+i).                \tag{3.2}
\]

At the canonical initial state, recurrent \(U\to I+V\) excursions start at
rate \(\Theta(U)\). During an excursion at \(I=1\), the lower source \(I+U\)
has rate \(\Theta(U)\), while the top return has rate \(\Theta(V)\). Hence
the interruption probability per excursion is \(\Theta(U/V)\), and the
effective interruption rate is

\[
 r={U^2\over V}.                                      \tag{3.3}
\]

For \(U=N^4,V=N^5\), this is \(N^3\), vastly larger than the constant
zero-source activation rate. If the interruption is \(I+U\to2I\) and the
two subsequent top returns fire, the net population increment is

\[
 \Delta V=-1,\qquad \Delta I=\Delta U=0,               \tag{3.4}
\]

and therefore

\[
 \Delta{\cal F}_\ell=-\log V-\ell_V.                  \tag{3.5}
\]

The other two possible targets of an \(I+U\)-sourced reaction are also
explicit. A target \(I\), followed by one top return, has net increment
\(-U\) and reward \(-\log U+O(1)\). A target \(0\) has net increment
\(V-2U\) and reward \(-\log r+O(1)\). Thus every outgoing edge from the
sole active-bearing lower vertex is a genuine source-tier exit; what varies
is whether its reward already diverges or whether the subsequent strong
path through \(\{0,I,2I\}\) must be retained.

The bad isolated word is therefore not the natural physical trace. The
repair has to average the recurrent top excursions before evaluating the
lower clock and then complete the actual lower target's cleanup.

## 4. The exact ratio dichotomy

The same shell suggests a complete local dichotomy. Put \(r=U^2/V\).

1. If \(r\to0\), the isolated block (2.3) already has reward
   \(\log r+O(1)\to-\infty\).
2. If \(r\ge\varepsilon>0\), use a window of order \(1/r\). There are
   order \(V/U\) top excursions, each has interruption probability order
   \(U/V\), and hence a successful interruption has probability bounded
   away from zero. Its favorable targets have rewards (3.5) or
   \(-\log U+O(1)\), while the expected number of constant-rate zero-source
   firings is \(O(1/r)\). When \(r\to\infty\), the latter contribution is
   \(o(1)\); when \(r\) stays bounded, its factorial reward is only \(O(1)\).

The missing proof is a **transient killed-shell lemma**, uniform over exact
tier subsequences and arbitrary strong orientations of \(L_1\):

\[
 \mathbb P_0\{\hbox{some }(I+U)\hbox{-sourced edge
      interrupts by time }T/r\}\ge p>0,                \tag{4.1}
\]

together with

\[
 \mathbb E\bigl[(\Delta{\cal F}_\ell)^+\bigr]=O(1),
 \qquad
 \sup_N\mathbb E(1+I_{\tau})^m<\infty                 \tag{4.2}
\]

for every fixed \(m\). Equation (3.2) gives the required exponential
cofactor drift. Strong connectivity then supplies a path from a possible
target \(0\) to \(I\) or \(2I\), but the proof must retain its clocks rather
than silently replacing the first neutral \(I+U\to0\) interruption by the
favorable \(I+U\to2I\) case. No fixed cofactor box may be inserted; leaving
a bounded set must be reclassified by its exact source-rate ratio.

## 5. Separation from the certified 36-pair branch

After removing the four already certified disjoint branches (151 affine,
fourteen rank-two, 51 all-active-only, and 141 rank-one no-promotion pairs),
exactly 36 promotion pairs have no affine-feasible one-active failure. They
split as

\[
 20\text{ seeded}+16\text{ dormant},\qquad
 32\text{ positive}+4\text{ signed}.                  \tag{5.1}
\]

All their feasible failures are two-active. Their pair fingerprint is

```text
f2ad8cbe4b9ca7f36c39bed4bfe5aaafc6a9152eaf300390b5c25ba546519137
```

The four suppressed-regression pairs have zero overlap with this selector.
The 36-pair common-potential theorem has now passed two independent audits
and is certified at its exact scope. That result does not settle the four
suppressed flags in Sections 1--4: their killed-shell cleanup remains a
separate open promotion mechanism, and the full promotion analytic flag
remains false.
