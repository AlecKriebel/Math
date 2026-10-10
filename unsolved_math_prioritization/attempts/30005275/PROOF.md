# Fourier magnitudes of complete polynomial sums: a degree-three classification

## Scope and status

This is a bounded result for OWR 50/2022, Problem 4 (problem 30005275). It does **not** classify arbitrary-degree integral polynomials. It proves a complete classification when both reduced polynomials have degree at most three, with the explicit sufficient bound `p >= 11`, and its all-sufficiently-large-primes counterpart over the rationals. All statements below distinguish an identity over a finite field from an identity over characteristic zero. No novelty claim is made.

For `f in F_p[X]`, write

\[
 S_f(a)=\sum_{x\in\mathbb F_p}\zeta_p^{af(x)},\qquad W_f(a;p)=p^{-1/2}S_f(a),
\]

where `zeta_p = exp(2 pi i / p)`. A constant includes the zero polynomial. Degrees in the finite-field theorem mean degrees **after reduction**. For fixed rational/integral polynomials, only finitely many primes reduce the degree or meet a denominator.

## Theorem A: complete finite-field classification through degree three

Let `p >= 11` be prime and let `f,g in F_p[X]` have degree at most three. The conditions `|W_f(a;p)| = |W_g(a;p)|` for every nonzero `a`, and for just one nonzero `a`, are equivalent. They hold exactly in the following cases:

1. Both polynomials are constant.
2. Both polynomials are nonconstant linear.
3. Both polynomials are quadratic.
4. Both polynomials are cubic, and
   \[
   g(X)=f(uX+v)+w \quad\text{for some }u\in\mathbb F_p^*,\ v,w\in\mathbb F_p.
   \]
5. One is nonconstant linear and the other is cubic; the cubic has the form `A(X-r)^3+C`, with `A != 0`, and `p = 2 mod 3`.

There are no further cross-degree cases. In case 5 all the nontrivial sums vanish.

A practical coefficient version of case 4 is as follows. Translate inputs and discard output constants so the cubics become
\[
 h(X)=AX^3+BX,\qquad k(X)=CX^3+DX,\quad AC\ne0.
\]
Then equality holds if and only if either:

- `B,D != 0` and `B^3/A = D^3/C`; or
- `B=D=0` and `C/A` is a cube in `F_p^*`.

In particular, when `p = 2 mod 3`, every nonzero `C/A` is a cube. If exactly one of `B,D` is zero, equality fails.

### 1. Exact cyclotomic and difference-count reductions

For any function `f:F_p -> F_p`, let
\[
 n_f(t)=\#\{x:f(x)=t\},\qquad
 D_f(t)=\#\{(x,y):f(x)-f(y)=t\}.
\]
Then
\[
 |S_f(a)|^2=\sum_t D_f(t)\zeta_p^{at},\qquad \sum_t D_f(t)=p^2. \tag{1}
\]

Consequently magnitude equality at a single nonzero `a` implies `D_f=D_g`: the rational polynomial
`sum_t (D_f(t)-D_g(t)) Z^t`, of degree at most `p-1`, vanishes at the primitive root `zeta_p^a`. It is a constant multiple of `Phi_p(Z)=1+...+Z^{p-1}`. Its coefficient sum is zero, so that constant is zero. The converse follows from (1). This also proves equivalence with magnitude equality at every nonzero frequency. It is an exact algebraic argument; it uses no numerical tolerance.

The same cyclotomic argument shows `S_f(a)=0` for one nonzero `a` if and only if `n_f(t)=1` for all `t`, that is, `f` is a permutation of the field.

If `h,k` are odd functions, `S_h(1)` and `S_k(1)` are real. Magnitude equality gives `S_h(1)=epsilon S_k(1)` for one fixed `epsilon in {1,-1}`. The coefficient argument, now applied to `n_h-epsilon n_k`, gives the exact dichotomy
\[
 n_h=n_k\quad\text{or}\quad n_h+n_k=2\mathbf 1. \tag{2}
\]
Indeed the constant coefficient difference is `1-epsilon`, because both fiber-count vectors sum to `p`. This is valid for arbitrary odd functions and every odd prime. The second possibility cannot simply be discarded in general.

For `1 <= j < p-1`, put `T_j(h)=sum_x h(x)^j in F_p`. Equation (2) implies
\[
 T_j(h)=\epsilon T_j(k), \tag{3}
\]
because `sum_t t^j=0`. We will use only two explicit values of `j`.

### 2. Cubic moments

Input translation and output translation preserve magnitudes. Every cubic in characteristic greater than three is therefore reduced to `h(X)=AX^3+BX`, with `A != 0`. The formula `sum_x x^e=0` unless the positive integer `e` is divisible by `p-1`, in which case the sum is `-1`, gives the following identities.

If `p=6m+1`, let `r=2m=(p-1)/3`. Since `p>=11`, this case has `m>=2`. Then
\[
 T_r(h)=-A^r,\qquad
 T_{r+2}(h)=-\binom{r+2}{3}A^{r-1}B^3. \tag{4}
\]
To check (4), the exponents in `(AX^3+BX)^j` are `j+2i`, `0<=i<=j`. In the two expressions the only possible positive multiple of `p-1` is `p-1`, and it occurs respectively at `i=r` and `i=r-1`. The largest exponent in the second expression is `p+5 < 2(p-1)`.

If `p=6m+5`, let `r=2m+2=(p+1)/3`; here `m>=1`. Then
\[
 T_r(h)=-rA^{r-1}B,\qquad
 T_{r+2}(h)=-\binom{r+2}{4}A^{r-2}B^4. \tag{5}
\]
The relevant exponents occur at `i=r-1` and `i=r-2`, respectively. Again the largest exponent `p+7` is less than `2(p-1)`. In both cases `r+2<p-1`, and every displayed binomial coefficient and `r` is nonzero modulo `p`, since its factorial arguments are less than `p`.

### 3. Comparison of two cubics

Write `h=AX^3+BX`, `k=CX^3+DX` and use (3).

If `p=6m+1`, the first equality from (4) gives `A^r=epsilon C^r`. Cubing gives `1=epsilon`, since `3r=p-1` and the characteristic is odd. Dividing the second moment equality by the first yields
\[
 B^3/A=D^3/C. \tag{6}
\]
If `B,D` are nonzero, set `u=D/B`. Then (6) gives `C=A u^3`, so `k(X)=h(uX)`. If one is zero both are zero; in this case `(C/A)^r=1`, which is precisely the condition that `C/A` is a cube in the cyclic group `F_p^*`. Choose a cube root `u` and again obtain `k=h(uX)`.

If `p=6m+5`, the first equality in (5) shows `B=0` if and only if `D=0`. If both vanish, the cube map permutes `F_p`, and every `C/A` has a cube root, so once more `k=h(uX)`. If they are nonzero, divide the second equality in (5) by the first. The sign cancels and gives (6). Setting `u=D/B` proves `k=h(uX)`. This identity also makes `T_r(h)=T_r(k) != 0`; hence (3) rules out a negative sign in this case.

Conversely `k=h(uX)` plainly has identical fiber counts. Undo the two input translations and output constants to obtain precisely case 4 of Theorem A.

### 4. Permutation and constant cases

A constant polynomial has `|W|=sqrt(p)`. If any other polynomial has that magnitude, equality in the triangle inequality for `S_f(1)` forces all its summands to be identical. It is therefore constant as a function; since its degree is less than `p`, it is a constant polynomial.

A nonconstant linear polynomial is a permutation and has every nontrivial sum zero. Formula (4) precludes any cubic permutation when `p=1 mod 3`, as its `r`-th power moment is nonzero. Formula (5) forces `B=0` for a cubic permutation when `p=2 mod 3`. Conversely `AX^3` is then a permutation, proving case 5 and all comparisons involving linears.

### 5. Quadratics and their exclusion from cubic magnitude classes

After input/output translations a quadratic is `AX^2`. For `t != 0`, the equation `A(x^2-y^2)=t` has `p-1` solutions: put `u=x-y`, `v=x+y`, so `uv=t/A`. For `t=0` it has `2p-1` solutions. Thus
\[
 D_{AX^2}(t)=(p-1)+p\mathbf1_{t=0},\quad |S_{AX^2}(a)|^2=p\quad(a\ne0). \tag{7}
\]
This proves case 3, with normalized magnitude one, and separates it from constants and linears.

Suppose a cubic `h=AX^3+BX` had these same magnitudes. If `p=2 mod 3` and `B=0`, it is a permutation and has magnitude zero, a contradiction. In every other case let `r` be as in (4) or (5). Then `T_r(h) != 0`, while `T_j(h)=0` for `0<=j<r` in `F_p`. For positive `j<r` this follows from `3j<p-1`; for `j=0` it follows from `T_0=p=0`. Also `0<2r<p-1`. By (1), (7), and the field power-sum identity,
\[
 \sum_t t^{2r}D_h(t)=0.
\]
On the other hand, expanding the left side directly as `sum_{x,y}(h(x)-h(y))^{2r}` leaves just the middle term, because every other term contains a moment with index less than `r`. It is
\[
 (-1)^r\binom{2r}{r}T_r(h)^2\ne0.
\]
Here `2r<p` makes the binomial coefficient nonzero. This contradiction excludes all cubic/quadratic comparisons and finishes Theorem A.

## Theorem B: the all-large-primes classification through degree three

Let `f,g in Q[X]` have degree at most three. Magnitude equality at every nonzero frequency for every sufficiently large prime holds if and only if exactly one of the following applies:

- both are constant;
- both are nonconstant linear;
- both are quadratic;
- both are cubic and `g(X)=f(uX+v)+w` for rational `u != 0,v,w`.

The sufficient direction follows by reduction away from finitely many denominators and leading coefficients, using Theorem A. For necessity, Theorem A rules out different degrees except possibly linear/cubic. Infinitely many primes are `1 mod 3`, and at every sufficiently large such prime a cubic is not a permutation, so this exception cannot persist.

For the cubic case depress the polynomials over `Q`, obtaining `AX^3+BX` and `CX^3+DX`. If exactly one of `B,D` is zero, reduction contradicts Theorem A for all sufficiently large primes. If neither is zero, Theorem A gives `B^3 C=D^3 A` modulo every sufficiently large prime. A nonzero rational number cannot have numerator divisible by infinitely many primes, so this is a rational identity. Set `u=D/B` to get `C=A u^3` as before.

If `B=D=0`, Theorem A says `c=C/A` is a cube modulo every sufficiently large prime. We use the following standard consequence of the Chebotarev density theorem: a rational number which is a cube modulo all sufficiently large primes is a rational cube. For completeness, if `X^3-c` had no rational root, it would be irreducible. Its splitting-field Galois group is a transitive subgroup of `S_3`, so contains a 3-cycle. Chebotarev gives infinitely many unramified primes with that Frobenius cycle type, avoiding all coefficient denominators and the discriminant; reduction then has no linear factor, contradicting the existence of a cube root. Thus `c=u^3` in `Q`, completing the proof. The only external theorem needed in this paragraph is Chebotarev; a primary author exposition is Romyar Sharifi, *Algebraic Number Theory*, Theorem 7.2.2, https://www.math.ucla.edu/~sharifi/notes/algnum-ch07.html .

The required infinitude of primes `1 mod 3` may be proved elementarily: if a finite list contained them all, put `N=3` times their product and take a prime divisor `q` of `N^2+N+1`. It is neither 3 nor in the list, and `N` has order exactly 3 modulo `q`, so `q=1 mod 3`, a contradiction.

## Genuine limitations and counterexamples to stronger conclusions

### C. Fixed-degree, arbitrarily-large-prime obstruction to universal affine rigidity

Take the fixed integral pair `f=X^2`, `g=X^6`. For every prime `p=2 mod 3`, the cube map is bijective, so `S_g(a)=S_f(a)` for all `a`; for odd such primes their normalized magnitudes equal one. Their distinct degrees rule out affine equivalence even over `C`. These primes are arbitrarily large: if finitely many primes `2 mod 3` existed, `3P-1`, where `P` is their product, would have a new prime factor `2 mod 3`.

This is a permutation-composition obstruction, not a solution of the classification problem. It respects a fixed degree bound and arbitrarily large primes, and does not rely on a small-prime coincidence or on coefficients depending on `p`. It does **not** hold for all large primes: at `p=1 mod 6`,
\[
 D_{X^2}(0)=2p-1,\qquad D_{X^6}(0)=6p-5,
\]
so the magnitudes cannot agree at all nonzero frequencies.

### D. Rational weak-affine rigidity already fails in degree four

The fixed pair `f=X^4`, `g=-4X^4` has equal magnitudes for every odd prime. If `p=1 mod 4`, choose `i in F_p` with `i^2=-1`; then `(1+i)^4=-4`, giving a bijective input substitution. If `p=3 mod 4`, the image and fiber counts of `X^4` equal those of `X^2`: their nonzero kernels both have size two and their images are the squares. Thus `n_f(t)=1+chi(t)` and `n_g(t)=1-chi(t)` since `chi(-4)=-1`. Their nontrivial sums are negatives of one another.

Nevertheless `g` is not `+f(uX+v)+w` or `-f(uX+v)+w` with rational `u != 0,v,w`: the leading coefficient would require `u^4=-4` or `u^4=4`, neither possible in `Q`. This example **is** affine-equivalent over `C` and is not claimed to contradict the broader affine-equivalence relation with arbitrary output scaling. It limits extending Theorem B's stronger rational relation beyond degree three.

### E. Why the explicit prime bound is not cosmetic

At `p=5`, the cubics `h=X^3+2X`, `k=X^3+3X` have fiber-count vectors `(1,0,2,2,0)` and `(1,2,0,0,2)` in residue order `0,...,4`. They sum to `2` at every residue, so their magnitudes agree by (2). There is no `u in F_5^*` with `k=h(uX)`: the linear term would force `u=4`, whose cube is 4 rather than 1. More generally an input affine translation between depressed cubics forces its translation parameter to be zero. This small-prime example is used only to test the necessity of a largeness qualification, never as the full-target obstruction.

## Residual problem

The unrestricted-degree classification remains unresolved in this work, in **both** prime regimes. Equation (1) gives an exact homometry criterion, but translating equality of those difference distributions into a general algebraic classification of `f,g` is the substantive missing step. Theorems A and B do not handle arbitrary degrees, decompositions, nongeneric critical values, or all possible arithmetic twists. The counterexamples identify permitted phenomena but do not classify them.

The source's Sidon–Morse theorem is prior work, with squarefree derivative, distinct critical values, and its precise Sidon or odd/symmetric-Sidon hypotheses. It is not invoked to prove Theorems A or B. Equicritical quartic results for modulus `p^2` do not settle the prime-modulus problem considered here.
