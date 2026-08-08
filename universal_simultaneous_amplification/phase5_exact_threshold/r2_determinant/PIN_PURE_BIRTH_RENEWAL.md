# A pure-birth inverse and Markov-renewal factorization for pin words

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note proves an exact all-population algebraic factorization for the
distinguished-pin versus other-pin-average operators.  The alternating
generalized block is the inverse of a stochastic pure-birth kernel.  After
the physical `O`-boundary residual is retained, every binary pin word
containing the distinguished pin factors into nonnegative stochastic gap
kernels on `2N` states.

This is a new structural reduction.  It does **not** yet prove the required
shuffle-summed ballot sign.  Three stronger shortcuts are exactly false:
pointwise positivity after applying the inverse pure-birth block, local
gap-split positivity, and log-convexity of the conditional reward sequence.

## 1. Operators and quotient categories

Put `n=N+1`.  Let `A` be the active operator of the distinguished pin and
let `B` be the average of the other `N` pin operators.  In the stabilizer
quotient, active states have the categories

\[
 X_k:\ v=x,\qquad I_k:\ v\ne x, x\in B,qquad
 O_k:\ v\ne x, x\notin B,                                  \tag{1}
\]

with `1<=k<=N` for `X,I` and `1<=k<N` for `O`.  The exact transition rows
are those in `STANDARD_PIN_VARIATION.md`, evaluated at

\[
 (\alpha,\beta)=(1,0)\quad\hbox{for }A,qquad
 (\alpha,\beta)=\left({1\over N^2},{N+1\over N^2}\right)
 \quad\hbox{for }B.                                           \tag{2}
\]

The determinant factorization already proves that `B` is invertible.  Put

\[
 D=B^{-1}A.                                                    \tag{3}
\]

## 2. Exact pure-birth inverse

Define the `N`-state upper-bidiagonal kernel `U` by

\[
 U_{k,k}=u_k={{(N+1)k-N}\over N^2},\qquad
 U_{k,k+1}=v_k={{(N+1)(N-k)}\over N^2}.                       \tag{4}
\]

Thus `u_k+v_k=1`, with `u_N=1`; `U` is a stochastic pure-birth kernel.
Let `T=U^{-1}`.  Its entries are

\[
 T_{k\ell}=
 \begin{cases}
 (-1)^{\ell-k}{N^2(N+1)^{\ell-k}(N-k)!\over
 (N-\ell)!\displaystyle\prod_{j=k}^{\ell}((N+1)j-N)},
 &k\le\ell,\\
 0,&k>\ell.
 \end{cases}                                                  \tag{5}
\]

For a quotient function `f`, write

\[
 X_k=f(X_k),\qquad Z_k=f(I_k),\qquad
 W_k=f(O_k)-f(I_{k+1}).                                      \tag{6}
\]

Then the exact action of `(3)` is

\[
 \boxed{
 (Df)(X_k)=X_k,qquad (Df)(I_k)=(TZ)_k,qquad
 (Df)(O_k)=(TZ)_{k+1}.}                                      \tag{7}
\]

Equivalently, in `(X,Z,W)` coordinates,

\[
 \boxed{D=\operatorname{diag}(I_N,T,0).}                     \tag{8}
\]

### Direct all-`N` proof

Let `A_I` denote the `I`-column block of `A`, and aggregate the `I/O`
columns of `B` by

\[
 \widehat B_{r,j}=B_{r,I_j}+1_{\{j\ge2\}}B_{r,O_{j-1}}.       \tag{9}
\]

Direct substitution of the quotient transitions gives

\[
 \boxed{\widehat B=A_IU.}                                    \tag{10}
\]

Indeed, row by row, the right side is

\[
\begin{array}{c|c}
 r&\widehat B_{r,\bullet}\\ \hline
 X_k&\tfrac12 U_{k,\bullet},\\
 I_k&{k-1\over2k}U_{k-1,\bullet}+\tfrac12U_{k,\bullet},\\
 O_k&\tfrac12U_{k,\bullet}+\tfrac12U_{k+1,\bullet},
\end{array}                                                   \tag{11}
\]

with absent boundary rows deleted.  The `X` columns of `A,B` are identical,
while `A` has no `O` columns.  Multiplying `(10)` by `T=U^{-1}` therefore
gives `BD=A`, and `(7)--(8)` follow.  Formula `(5)` is the elementary inverse
of the upper-bidiagonal matrix `(4)`.  This proof does not infer the pattern
from finite matrices.

## 3. The physical reset residual

Let `R` embed `(X,Z)` into the full quotient by

\[
 (R(X,Z))(X_k)=X_k,quad (R(X,Z))(I_k)=Z_k,quad
 (R(X,Z))(O_k)=Z_{k+1},                                      \tag{12}
\]

and let `C` select the `X,I` coordinates.  Then `CR=I` and

\[
 D=R\,\operatorname{diag}(I,T)\,C.                            \tag{13}
\]

The complementary projection

\[
 P_W=I-RC                                                     \tag{14}
\]

is the physical reset residual; it keeps only
`f(O_k)-f(I_(k+1))`.  It cannot be discarded.  For the inverse-rank reward,

\[
 H_X(k)=H_I(k)={1\over k},\qquad
 (P_WH)(O_k)={1\over k(k+1)}>0.                              \tag{15}
\]

If

\[
 K(p)=(1-p)B+pA,\qquad V_p=pI+(1-p)U,                         \tag{16}
\]

then `(8)` and

\[
 (1-p)I+pT=T\{pI+(1-p)U\}=TV_p                              \tag{17}
\]

give the exact mixture decomposition

\[
 \boxed{
 K(p)=A R\operatorname{diag}(I,V_p)C+(1-p)BP_W.}              \tag{18}
\]

The first term contains only the stochastic pure-birth kernel `V_p`; the
second is the indispensable `O`-reset boundary.

The complete initial row also has positive transformed coordinates.  With

\[
 \pi_k={\binom{N-1}{k-1}\over2^{N-1}},                       \tag{19}
\]

their respective `X,Z,W` masses are

\[
 {\pi_k\over N+1},\qquad { (2k-1)\pi_k\over N+1},\qquad
 { (N-k)\pi_k\over N+1}.                                    \tag{20}
\]

## 4. Nonnegative Markov-renewal factorization

The alternating entries of `T` disappear after a complete pin word is
grouped by its `B`-run lengths.  Consider a binary word with `c>=1` copies
of `A`:

\[
 B^{g_0}A B^{g_1}A\cdots A B^{g_c},qquad g_i\ge0.             \tag{21}
\]

Using `A=BR diag(I,T)C` at each distinguished-pin occurrence gives

\[
\boxed{
\begin{aligned}
 &\nu B^{g_0}A B^{g_1}A\cdots A B^{g_c}H\\
 &\quad=
 [\nu B^{g_0}AR]
 \prod_{i=1}^{c-1}[CB^{g_i}AR]
 [CB^{g_c}H].
\end{aligned}}                                                \tag{22}
\]

Every entry on the right is nonnegative.  More strongly,

\[
 G_g:=CB^gAR                                                   \tag{23}
\]

is row-stochastic, because `A,B` are stochastic and `R1=C1=1`.  Thus `(22)`
is a literal Markov-renewal representation on `2N` reduced states.

For fixed counts `(b,c)`, uniform word symmetrization is exactly the uniform
sum of `(22)` over the weak compositions

\[
 g_0+\cdots+g_c=b.                                            \tag{24}
\]

Equivalently, with the coefficientwise nonnegative series

\[
\begin{aligned}
 L(z)&=\sum_{g\ge0}\nu B^gARz^g,\\
 G(z)&=\sum_{g\ge0}CB^gARz^g,\\
 R_0(z)&=\sum_{g\ge0}CB^gHz^g,
\end{aligned}                                                  \tag{25}
\]

the unnormalized word sum is

\[
 [z^b]L(z)G(z)^{c-1}R_0(z).                                  \tag{26}
\]

Equation `(26)` is the sharp reduced target for a ballot or
variation-diminishing proof.  It incorporates the upper boundary exactly.

## 5. Hostile boundaries

The following stronger statements are false.

1. `T` does not preserve positivity on reachable `I` controls.  At `N=4`,
   for the exact control `A^2H`,

   \[
   \{T(A^2H)_I\}_1=-{2213\over9216}<0.                       \tag{27}
   \]

2. A local renewal split is not entrywise positive.  At `N=3`,

   \[
   (G_0^2-G_1)_{X_1,I_2}=-{2\over9}<0.                       \tag{28}
   \]

   Therefore the composition sum `(24)`, rather than each split, is the
   minimum possible grouping.

3. The one-versus-rest conditional rewards are not log-convex.  For
   `n=4,t=18`,

   \[
   \psi_{18,17}^2-\psi_{18,16}\psi_{18,18}
   ={392199485892499790434361171\over
   170435555370257609364945286201344}>0.                      \tag{29}
   \]

   The needed first-difference one-crossing and positive Bernstein quotient
   still hold on this instance.

Separately, for the literal two-label swap `M=(L_x+L_y)/2` and
`Delta=(L_x-L_y)/2`, even two-Delta excursions can be negative before
shuffling.  The smallest exact packet found is

\[
 \nu\Delta M\Delta M H=-{1\over24576}\qquad(n=3).             \tag{30}
\]

These counterexamples rule out pointwise cone, local split, Hankel, and
individual-excursion proofs.  They do not contradict the complete
shuffle-summed sign.

## 6. Remaining lemma

The unresolved step is now precise: prove the required adjacent-count or
lower-partial-mean sign for the full weak-composition sum `(24)`.  A valid
proof may use a ballot reflection on whole gap compositions or a
variation-diminishing theorem for the coefficient array in `(26)`.  It
cannot replace `(24)` by a pointwise claim refuted in Section 5.

The independent verifier checks `(3)--(23)` exactly for `2<=N<=8`, compares
988 binary words with `(22)`, and reproduces `(27)--(29)`.
