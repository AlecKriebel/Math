# Directed complete-support dB strong-selection audit

**Date:** 2026-08-01 (America/Los_Angeles)
**Convention:** `w_uv` is the weight from reproducing source `u` into dead
target `v`.  Thus a dB competition at target `v` uses the incoming column
`(w_uv)_{u != v}`.  No literature search was used.

## Verdict

The proposed directed defect

\[
 E_{\rm dir}
 =\sum_v\sum_{\substack{u<z\\u,z\ne v}}
 \frac{(w_{uv}-w_{zv})^2}{w_{uv}w_{zv}}
\]

and comparison

\[
 \rho_{\rm dB}(K_n,r)-\rho_{\rm dB}(G,r)
 =\frac{E_{\rm dir}}{n^2(n-2)r}+O(r^{-2})
\]

are correct for every fixed directed loopless graph of complete positive
support on `n >= 3` vertices.  Equality holds exactly when every incoming
column is constant off the diagonal,

\[
 w_{uv}=c_v>0\qquad(u\ne v),
\]

where the constants may vary independently with the target.  Such a matrix
is obtained from the unit complete graph by independent incoming-column
scalings, which leave every dB transition probability unchanged.  It
therefore ties `K_n` for every `r`, not merely through first order.

I tried to falsify the coefficient using exact asymmetric `2^n`-state chains.
The proposed expression survived all checks.  A row-based analogue fails:
an explicit matrix with constant incoming columns but highly nonconstant rows
has exact complete-graph fixation, while its row defect is positive.

## Claim-status table

| Claim | Status | Decisive check |
|---|---|---|
| Full-support extinction vector is analytic at `x=0` | Proved | `I-Q(0)` is invertible because the limiting finite chain absorbs |
| Derivatives vanish for states with at least three mutants | Proved | Backward triangular first-step system |
| Directed doubleton coefficient uses `a_ji+a_ij` | Proved | Separate loss-at-target calculations |
| Uniform-singleton graph coefficient is `A_dir/[n^2(n-2)]` | Proved | Differentiated singleton equations and exact averaging |
| `A_dir-n(n-1)(n-2)=E_dir` | Proved | Termwise incoming-column square identity |
| Equality permits independent target-column constants | Proved | Zero squares plus exact column-scaling invariance |
| A row-oriented defect could replace `E_dir` | Falsified | Column-uniform, row-nonuniform exact negative control |
| Extension of the `1/(n-2)` formula to `n=2` | Not applicable | Separate exact value `rho=1/2` is required |

## Theorem

Let `n >= 3`, let `w_vv=0`, and suppose

\[
 w_{uv}>0\qquad(u\ne v).
\]

Put

\[
 d_v^-:=\sum_{u\ne v}w_{uv},\qquad
 a_{uv}:=\frac{d_v^- - w_{uv}}{w_{uv}}\quad(u\ne v),
\]

and

\[
 A_{\rm dir}:=\sum_v\sum_{u\ne v}a_{uv}.
\]

For fixation probability averaged uniformly over singleton initial mutants,

\[
 \boxed{
 \rho_{\rm dB}(G,r)
 =\frac{n-1}{n}
 -\frac{A_{\rm dir}}{n^2(n-2)}\frac1r+O(r^{-2}).}
\]

Moreover,

\[
 A_{\rm dir}=n(n-1)(n-2)+E_{\rm dir}.
\]

Since

\[
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}-\frac{n-1}{n}\frac1r+O(r^{-2}),
\]

the proposed comparison follows.  In particular, any nonconstant incoming
column makes the directed graph strictly dB-suppressing relative to `K_n`
for every sufficiently large finite `r`.

All big-O constants here are for one fixed weight matrix.  No uniformity over
a family whose weights vary with `n` is asserted or needed.

### Complete-graph coefficient from the count chain

For completeness, the baseline coefficient also follows directly from the
dB rule.  With `k` mutants on the unit complete graph, the gain and loss
probabilities are

\[
 U_k=\frac{n-k}{n}\frac{rk}{rk+n-k-1},\qquad
 D_k=\frac{k}{n}\frac{n-k}{r(k-1)+n-k}.
\]

Their ratio is

\[
 \gamma_k:=\frac{D_k}{U_k}
 =\frac{rk+n-k-1}{r\{r(k-1)+n-k\}}.
\]

If `B_k=r(k-1)+n-k`, then

\[
 \gamma_k=\frac{B_{k+1}}{rB_k},\qquad
 \prod_{k=1}^j\gamma_k
 =\frac{rj+n-j-1}{(n-1)r^j}.
\]

Solving the one-dimensional absorption recurrence by summing successive
differences gives

\[
 \begin{aligned}
 \rho_{\rm dB}(K_n,r)^{-1}
 &=1+\sum_{j=1}^{n-1}\prod_{k=1}^j\gamma_k\\
 &=\frac{n}{n-1}\sum_{m=0}^{n-2}x^m.
 \end{aligned}
\]

Therefore

\[
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}\frac{1-x}{1-x^{n-1}}
 =\frac{n-1}{n}-\frac{n-1}{n}x+O(x^2),
\]

as used above.

## 1. Exact transition equations in the source-target convention

Set `x=1/r` and divide every reproduction competition by mutant fitness.
For mutant set `S` and target `v`, define the incoming mutant and resident
masses

\[
 M_v(S):=\sum_{u\in S}w_{uv},\qquad
 R_v(S):=\sum_{u\notin S}w_{uv}.
\]

The zero diagonal automatically excludes the dead target from reproduction.
If resident `v notin S` dies, the probability of the gain
`S -> S union {v}` is

\[
 g_v(S,x)=\frac1n\frac{M_v(S)}{M_v(S)+xR_v(S)}.
\]

If mutant `v in S` dies, the probability of the loss
`S -> S setminus {v}` is

\[
 \ell_v(S,x)=\frac1n\frac{xR_v(S)}{M_v(S)+xR_v(S)}.
\]

For a singleton `S={v}`, `M_v(S)=0` and the last probability is exactly
`1/n` after cancelling its common factor `x`.  Complete support implies
`M_v(S)>0` in every other gain or loss formula.  All transition probabilities
therefore have analytic extensions to a neighborhood of `x=0`.

Let `q_S(x)` be extinction probability, with `q_empty=1` and `q_V=0`.  After
cancelling holding terms, its exact first-step equation is

\[
 0=
 \sum_{v\notin S}g_v(S,x)\{q_{S\cup\{v\}}(x)-q_S(x)\}
 +\sum_{v\in S}\ell_v(S,x)\{q_{S\setminus\{v\}}(x)-q_S(x)\}.
 \tag{1}
\]

This equation fixes the direction of every index: the target is always the
second index of `w_uv`.

## 2. Why differentiation at `x=0` is legitimate

Let `Q(x)` be the one-step transition matrix restricted to nonempty proper
mutant sets, including holding probabilities.  Its entries are analytic near
zero by the preceding case analysis.  At `x=0`:

* singleton `{i}` goes to extinction if `i` dies and to a doubleton if any
  other target dies;
* a set with at least two mutants never loses a mutant, and every resident
  target becomes mutant when it dies.

Thus every transient state reaches extinction or fixation almost surely in
the limiting finite chain.  Equivalently, `Q(0)` has spectral radius less
than one, so `I-Q(0)` is invertible.  Hence

\[
 q(x)=(I-Q(x))^{-1}b(x)
\]

is analytic near zero.  Termwise differentiation of (1) is therefore valid,
and all remainders below are genuine Taylor remainders.

At order zero,

\[
 q_{\{i\}}(0)=\frac1n,\qquad
 q_S(0)=0\quad(|S|\ge2).
 \tag{2}
\]

Write a dot for `d/dx` evaluated at zero.

## 3. States with at least three mutants

For a proper state `S` with `|S|>=3`, differentiate (1).  Every term
containing a derivative of `g_v` or `ell_v` is multiplied by a difference of
order-zero extinction probabilities.  Those differences vanish by (2),
including after one loss because `|S setminus {v}|>=2`.  Since
`g_v(S,0)=1/n` and `ell_v(S,0)=0`, the remaining equation is

\[
 0=\frac1n\sum_{v\notin S}
 \left(\dot q_{S\cup\{v\}}-\dot q_S\right).
\]

Backward induction from `dot q_V=0` gives

\[
 \boxed{\dot q_S=0\qquad(|S|\ge3).}
 \tag{3}
\]

This differentiated equation is the rigorous version of the statement that
extinction from three or more mutants requires at least two rare losses.

More explicitly, the differentiated system is triangular when states are
ordered by decreasing mutant-set size.  The boundary derivative at size `n`
is zero.  At each size `k>=3`, the derivative for `S` is the average of the
already determined derivatives at sets `S union {v}` of size `k+1`.  The
doubleton equations then use those zero tripleton derivatives and known
order-zero singleton values; finally, the singleton equations use the known
doubleton derivatives.  No derivative at a smaller mutant-set size enters an
earlier stage, because every loss probability is zero at `x=0`.  This gives a
direct nonsingular recursive solution independently of the matrix-inverse
analyticity argument.

## 4. Doubletons: the source-target index check

Let `S={i,j}`.  If mutant target `i` dies, the only mutant source is `j`, so

\[
 M_i(S)=w_{ji},\qquad R_i(S)=d_i^- -w_{ji}.
\]

Therefore

\[
 \dot\ell_i(S,0)
 =\frac1n\frac{d_i^- -w_{ji}}{w_{ji}}
 =\frac1n a_{ji}.
\]

Similarly, loss of target `j` has derivative `a_ij/n`.  On differentiating
(1), the `n-2` gain terms lead to states covered by (3), while a loss leaves a
singleton of order-zero extinction probability `1/n`.  Hence

\[
 0=-\frac{n-2}{n}\dot q_{\{i,j\}}
 +\frac{a_{ji}+a_{ij}}{n^2},
\]

or

\[
 \boxed{
 \dot q_{\{i,j\}}
 =\frac{a_{ji}+a_{ij}}{n(n-2)}.}
 \tag{4}
\]

The loss of target `i` uses `w_ji`, not `w_ij`.  The symmetric-looking final
sum in (4) can conceal this orientation, so deriving the two loss events
separately is essential.

## 5. Singletons and uniform averaging

For singleton `{i}`, death of target `i` causes extinction with probability
`1/n`.  If resident target `v != i` dies, mutant source `i` supplies it with
conditional probability

\[
 f_{v|i}(x)
 :=\frac{w_{iv}}{w_{iv}+x(d_v^- -w_{iv})}
 =1-a_{iv}x+O(x^2).
\]

Multiplying the first-step equation by `n` gives

\[
 0=1-q_{\{i\}}(x)
 +\sum_{v\ne i}f_{v|i}(x)
 \{q_{\{i,v\}}(x)-q_{\{i\}}(x)\}.
 \tag{5}
\]

Set

\[
 C_i:=\sum_{v\ne i}a_{iv}.
\]

Differentiating (5), using (2) and (4), yields

\[
 \begin{aligned}
 \dot q_{\{i\}}
 &=\frac{C_i}{n^2}+\frac1n\sum_{j\ne i}\dot q_{\{i,j\}}\\
 &=\frac{C_i}{n^2}
 +\frac1{n^2(n-2)}\sum_{j\ne i}(a_{ij}+a_{ji}).
 \end{aligned}
 \tag{6}
\]

Now

\[
 \sum_i C_i=A_{\rm dir},\qquad
 \sum_i\sum_{j\ne i}(a_{ij}+a_{ji})=2A_{\rm dir}.
\]

Consequently

\[
 \begin{aligned}
 \frac1n\sum_i\dot q_{\{i\}}
 &=\frac{A_{\rm dir}}{n^3}
 +\frac{2A_{\rm dir}}{n^3(n-2)}\\
 &=\frac{A_{\rm dir}}{n^2(n-2)}.
 \end{aligned}
\]

Since uniformly averaged fixation is `1-(1/n)sum_i q_{\{i\}}`, the asserted
strong-selection expansion follows.

## 6. Exact defect identity

Write `m=n-1`.  For one target column `v`,

\[
 \begin{aligned}
 \sum_{u\ne v}a_{uv}
 &=d_v^-\sum_{u\ne v}\frac1{w_{uv}}-m,\\
 \sum_{u\ne v}a_{uv}-m(m-1)
 &=d_v^-\sum_{u\ne v}\frac1{w_{uv}}-m^2.
 \end{aligned}
\]

Expanding the last product pairwise gives the identity

\[
 \begin{aligned}
 d_v^-\sum_{u\ne v}\frac1{w_{uv}}-m^2
 &=\sum_{\substack{u<z\\u,z\ne v}}
 \left(\frac{w_{uv}}{w_{zv}}+
       \frac{w_{zv}}{w_{uv}}-2\right)\\
 &=\sum_{\substack{u<z\\u,z\ne v}}
 \frac{(w_{uv}-w_{zv})^2}{w_{uv}w_{zv}}.
 \end{aligned}
\]

Summing over targets proves

\[
 A_{\rm dir}-n(n-1)(n-2)=E_{\rm dir}\ge0.
\]

This is stronger than merely invoking Cauchy--Schwarz: it is a termwise exact
nonnegative certificate.

## 7. Equality and incoming-column scaling

The defect vanishes if and only if, for each fixed target `v`,

\[
 w_{uv}=c_v\qquad\text{for all }u\ne v.
\]

No relation between `c_v` and `c_z` is forced.  This differs essentially from
the undirected case: symmetry there couples incident weights, whereas a
directed dB competition normalizes each target column independently.

More generally, for arbitrary positive factors `lambda_v`, replace

\[
 w_{uv}\longmapsto \widetilde w_{uv}:=\lambda_v w_{uv}.
\]

For a death at target `v`, both mutant and resident incoming masses acquire
the common factor `lambda_v`, which cancels from the parent-selection ratio.
Thus the entire dB Markov chain is invariant under independent positive
incoming-column scaling.  If `w_uv=c_v`, scaling column `v` by `1/c_v`
produces the unit complete graph, proving

\[
 \rho_{\rm dB}(G,r)=\rho_{\rm dB}(K_n,r)
 \quad\text{for every }r>0.
\]

Conversely, equality in the first-order coefficient forces every square in
`E_dir` to vanish, so the column-uniform class is the complete equality class
for the strong-selection comparison.

## 8. The `n=2` exception

For `n=2`, each incoming column contains only one positive off-diagonal
weight, so column-uniformity is vacuous and `E_dir=0`.  The formula with
denominator `n-2` must not be used.  From a singleton, death of the mutant
causes extinction and death of the resident causes fixation, each with
probability `1/2`.  Hence every directed complete-support two-vertex matrix
satisfies

\[
 \rho_{\rm dB}(G,r)=\frac12=\rho_{\rm dB}(K_2,r)
\]

for every fitness and for arbitrary positive `w_12,w_21`.

## 9. Exact falsification attempts

The companion verifier `verify_directed_db_strong.py` constructs the full
directed dB chain directly from the update definition, solves all
`2^n-2` transient equations over `QQ(r)`, and extracts the coefficient by an
exact limit.  No floating-point fixation probabilities are used.

For the asymmetric three-vertex source-row matrix

\[
 W=\begin{pmatrix}
 0&1&2\\
 3&0&4\\
 5&6&0
 \end{pmatrix},
\]

the certificate and exact chain give

\[
 E_{\rm dir}=\frac{74}{15},\qquad
 \lim_{r\to\infty}r\left(\frac23-\rho_{\rm dB}(G,r)\right)
 =\frac{164}{135},
\]

and therefore

\[
 \lim_{r\to\infty}r\{
 \rho_{\rm dB}(K_3,r)-\rho_{\rm dB}(G,r)\}
 =\frac{74}{135}.
\]

For the asymmetric four-vertex source-row matrix

\[
 W=\begin{pmatrix}
 0&1&2&3\\
 4&0&5&6\\
 7&8&0&9\\
 10&11&12&0
 \end{pmatrix},
\]

the exact results are

\[
 E_{\rm dir}=\frac{4051}{165},\qquad
 \lim_{r\to\infty}r\left(\frac34-\rho_{\rm dB}(G,r)\right)
 =\frac{8011}{5280},
\]

and

\[
 \lim_{r\to\infty}r\{
 \rho_{\rm dB}(K_4,r)-\rho_{\rm dB}(G,r)\}
 =\frac{4051}{5280}.
\]

Finally, consider

\[
 W=\begin{pmatrix}
 0&5&7&11\\
 2&0&7&11\\
 2&5&0&11\\
 2&5&7&0
 \end{pmatrix}.
\]

Its incoming columns are constant, so `E_dir=0`, and the exact rational
fixation function equals the `K_4` baseline identically.  Its rows are not
constant; the analogous row-pair defect is `1131/77>0`.  Thus swapping source
and target in the proposed expression is decisively falsified, while the
incoming-column expression passes the test.

All three positive-defect tested matrices are genuinely asymmetric: `W` is
not equal to its transpose, and neither all rows nor all incoming columns are
constant.
The exact verifier output is stored verbatim in `verification_output.txt`.
Run it with

```sh
PYTHONDONTWRITEBYTECODE=1 python phase1_directed/verify_directed_db_strong.py
```

The reproducibility hashes at the time of this audit are

```text
951a88f1c7534228049e24a70239be193cdb00d3a6c07fe801ade2224d18e003  phase1_directed/verify_directed_db_strong.py
9f5e0cf0905adabbcaefccb82c77302659745f482d51857a27d107d2d31eb10a  phase1_directed/verification_output.txt
```

They are obtained with `shasum -a 256`.  The recorded output contains the
exact values

```text
n=3 E_dir=74/15 graph_coefficient=164/135 comparison_coefficient=74/135
n=3 E_dir=233/105 graph_coefficient=863/945 comparison_coefficient=233/945
n=4 E_dir=4051/165 graph_coefficient=8011/5280 comparison_coefficient=4051/5280
column-uniform negative control: exact baseline identity; wrong row defect=1131/77
independent incoming-column scaling: exact fixation identity
```

## Final audit conclusion

The proposed `E_dir` is not merely a plausible Cauchy defect.  It is exactly
the excess of the differentiated singleton-extinction coefficient over the
complete-graph value.  The source-target indices, factor `n^2(n-2)`, sign,
and equality class under independent incoming-column scaling are all correct.
