# A 2-adic and causal-mate formulation of the order-668 seed

## Status

No Hadamard matrix is constructed here.  This note replaces the local
Hamming-ball view of Eliahou's 64-modular seed by two exact algebraic
formulations:

1. a finite 2-adic lifting tower whose first layer reduces the 334 signs to
   251 parameters globally, and whose second layer leaves 169 parameters on
   the full-rank branch containing Eliahou's seed; and
2. a split-at-42 polynomial formulation in which the 42 high-lag equations
   are linear causal-orthogonality equations.

The identities were derived independently in this project.  No claim of
literature priority is made.  In accordance with the independent-research
policy, no outside communication is proposed or prepared.

All finite claims in this note are checked by:

```sh
python3 verify_novel_lifting_64.py
```

The intended use is construction, not another unrestricted SAT run.  The
most promising target is a nonlinear "comb secant" on the modular variety,
combined with a causal mate for the split-at-42 equations.  The published
seed cannot be lifted by a first-order Boolean Newton step, so a genuinely
nonlocal algebraic switch is required.

## 1. The active-edge form

Write the special pair as two sign words

```text
s = a || c,       |a|=84, |c|=83,
q = g || h,       |g|=84, |h|=83.
```

The corresponding base sequences are

```text
A=a,  B=a*g,  C=c,  D=c*h.
```

For `1 <= k <= 83`, define `E_k(q)` to contain:

- `(i,i+k)` in the long block whenever `g_i=g_(i+k)`; and
- `(i,i+k)` in the short block whenever `h_i=h_(i+k)`.

Let

```text
T_k(s,q) = sum_(ij in E_k(q)) s_i s_j.
```

Then, coefficient by coefficient,

```text
R_k(A,B,C,D) = 2 T_k(s,q),
F_k(s,s',sq,(sq)') = 4 T_k(s,q).
```

This is just

```text
a_i a_j + a_i g_i a_j g_j
    = a_i a_j (1+g_i g_j),
```

and similarly in the short block.  Thus the construction problem is:

> Choose a two-colouring `q` of the two intervals and one common sign cut
> `s` so that the cut divides the edges of every distance graph `E_k(q)`
> exactly in half.

If `m_k=|E_k(q)|` and `x_i` is the bit indicating `s_i=-1`, put

```text
c_k(x,q) = sum_(ij in E_k(q)) (x_i xor x_j).
```

The exact integer identity is

```text
T_k = m_k - 2 c_k.                         (1)
```

Consequently `T_k=0` if and only if the common cut crosses exactly `m_k/2`
active edges.

This has two advantages over signed residual repair:

- `q` controls only which edges exist;
- after `q` is fixed, every term has unit weight and the unknown `s` is a
  simultaneous exact half-cut.

## 2. First lift: all admissible q words have 84 parameters

An exact zero sum of `m_k` signs requires `m_k` even.  Surprisingly, these 83
parity requirements solve completely.

### Theorem 1 (reciprocal q skeleton)

Every exact special quadruple must have

```text
g = (g_0,g_1,...,g_41,g_41,...,g_1,-g_0),
h = (h_0,h_1,...,h_40,h_41,h_40,...,h_1,h_0).       (2)
```

Conversely, every `q` of this form makes every `m_k` even (and makes
`E_83(q)` empty).

Therefore this first lifting layer has exactly 84 free signs: 42 from `g`
and 42 from `h`.

### Proof

Use bits for the signs of `q`.  Modulo two, the indicator that two bits are
equal is

```text
1 + q_i + q_j.
```

Thus `m_k=0 mod 2` is a linear equation.  Row reduction has an especially
simple closed form.  If `e_k` denotes the equation at lag `k`, then:

```text
e_83                 gives g_0 + g_83 = 1;
e_j + e_(83-j)       gives g_j + g_(83-j) = 0, 1<=j<=41;
e_(j+1) + e_(83-j)   gives h_j + h_(82-j) = 0, 0<=j<=40.
```

These are 83 independent equations and are precisely (2).  Reversing the
row operations proves the converse.  The checker compares the two reduced
row spaces exactly.

This is the sign-pair content of the usual base-sequence quad parity, but the
active-edge proof shows why it is the first 2-adic digit of the special
construction and exposes `q` itself as the natural lifting variable.

### Group-ring and finite-field form

There is a useful equivalent form.  Work in

```text
F_2[C_167] = F_2[z]/(z^167-1).
```

Let `Q(z)` be the negative-position mask of `q`, let

```text
H(z)=z^84+z^85+...+z^166
```

be the half-mask, put `P* = P(z^-1)`, and let

```text
J(z)=1+z+...+z^166.
```

The skeleton equations are equivalent to the single group-ring equation

```text
H Q* + Q H* = J + 1.                       (3)
```

The coefficient at every nonzero cyclic shift is one and the constant
coefficient is zero.

This becomes more informative at a primitive 167th root.  The order of 2
modulo 167 is 83, so over `F_2`

```text
Phi_167 = f f*
```

with two reciprocal irreducible factors of degree 83.  In the corresponding
CRT coordinates, conjugation exchanges the two copies of `F_(2^83)`.
Writing `H=(h_+,h_-)` and `Q=(q_+,q_-)`, equation (3) is

```text
h_+ q_- + q_+ h_- = 1.                     (4)
```

Neither component of `H` is zero: at a primitive root,
`H=z^84(1-z^83)/(1-z)`.  Hence arbitrary `q_+` determines

```text
q_- = (1+q_+ h_-)/h_+.
```

The quotient forgets the global complement `Q -> Q+J`, giving
`83+1=84` binary parameters, exactly as in (2).  Thus the first lift may be
generated either by reciprocal coordinates or by one field element in
`F_(2^83)` plus a complement bit.

## 3. Second lift: 82 linear equations in s

Assume `q` has skeleton (2), so `m_k` is even.  Reducing (1) modulo four
gives:

```text
T_k = 0 (mod 4)
  iff c_k = m_k/2 (mod 2)
  iff sum_(ij in E_k) (x_i+x_j) = m_k/2 (mod 2).    (5)
```

For fixed `q`, these are linear equations in the 167 bits of `s`.  Lag 83 is
empty, so there are at most 82 nontrivial rows.

For Eliahou's published `q`, the matrix in (5) has exact rank 82 and is
consistent.  Its solution fiber therefore has dimension

```text
167-82 = 85.
```

Combining the 84 `q` parameters with this 85-dimensional `s` fiber leaves
169 structural bits before imposing any higher lift on this full-rank
branch.  This is not merely a symmetry quotient: it is an exact
parameterization of the first two layers near the published `q`, and for any
other skeleton word whose lift matrix has rank 82.

For general skeleton words the rank can drop; consistency must then be
checked.  Low rank is not automatically beneficial, because some structured
`q` words make (5) inconsistent.  The published word has full row rank.
Rank-deficient consistent words, if present at length 167, form a separate
exceptional branch and are not covered by the 169-parameter count.

## 4. The finite Hensel tower

The half-cut equation admits a complete finite hierarchy over `F_2`.  For a
set of cut-edge bits `y_e=x_i xor x_j`,

```text
c_k = sum_e y_e.
```

Lucas' theorem says that bit `r` of this count is

```text
bit_r(c_k)
  = binomial(c_k,2^r) mod 2
  = sum_(S subset E_k, |S|=2^r) product_(e in S) y_e.     (6)
```

Because `m_k` is even,

```text
bit_r(m_k/2) = bit_(r+1)(m_k)
             = binomial(m_k,2^(r+1)) mod 2.               (7)
```

Equating (6) and (7) for `r=0,1,...,6` gives equations of degrees

```text
1, 2, 4, 8, 16, 32, 64.                                  (8)
```

They are exactly the successive requirements

```text
T_k = 0 mod 4, 8, 16, 32, 64, 128, 256.
```

Here `m_k<=164`, hence `c_k,m_k/2<=82`.  Congruence modulo 128 between
`c_k` and `m_k/2` is equality.  Equivalently, divisibility of `T_k` by 256
forces `T_k=0`.  The lifting tower is therefore finite and has no
completeness gap.

This suggests a construction method quite different from integer
correlation search:

1. generate `q` on the affine field layer (3);
2. eliminate 82 `s` bits using the linear equations (5);
3. solve the quadratic and quartic layers algebraically;
4. move between components of that modular variety to solve the degree-8
   layer;
5. continue through degrees 16, 32, and 64.

The large integer residual equations never need to be introduced directly.

## 5. What the 64-modular seed looks like in this tower

For the published seed, the gate correlations `T_k=R_k/2` are:

```text
k:   4    8   12   16   26  30  34  38  42  46  50  54  58
T: -128   96  -64   32  -16  32 -48  64 -80  64 -48  32 -16
```

Every `T_k` is divisible by 16.  Thus Eliahou's 64-modular special
quadruple is already a point on the degree-1, degree-2, and degree-4
varieties in (8).

The failures then appear in stages:

| required modulus for `T` | failing lags |
|---:|---|
| 16 | none |
| 32 | 26, 34, 42, 50, 58 |
| 64 | 8, 16, 26, 30, 34, 42, 50, 54, 58 |
| 128 | all residual lags except 4 |
| 256 | all 13 residual lags |

The next construction problem is therefore not initially a 13-lag repair.
It is a five-equation degree-8 lift.

### A Frobenius-square first obstruction

Modulo two, the first failed syndrome is

```text
sum_k (T_k/16) z^k
  = z^26(1+z^8+z^16+z^24+z^32)
  = [z^13(1+z^4+z^8+z^12+z^16)]^2.          (9)
```

This perfect square is not a numerical accident.  Over the integers, put

```text
P(z)=1-z^4+z^8-z^12+z^16.
```

The complete one-sided defect is

```text
D_+(z) = sum_(k>0) (T_k/16) z^k
       = -8z^4+6z^8-4z^12+2z^16 - z^26 P(z)^2.            (10)
```

If `N(P)=P P*`, `U=z^42 P`, and `V=P`, the symmetrized defect is

```text
D_+ + D_+*
  = 2(N(P)-5) - (U V* + V U*).                            (11)
```

Thus the first obstruction is carried by a five-point step-4 comb and one
interaction of two copies separated by 42.  A legal sign switch realizing
the negative of (11) has not yet been found, but (9)--(11) identify a very
small algebraic carrier for the nonlocal repair.

The natural reflection-closed support suggested by the square root in (9)
starts from

```text
{13,17,21,25,29}.
```

Toggling a `q` parameter also toggles its forced reciprocal mate, so a legal
comb move is automatically nonlocal.  This is qualitatively consistent with
the certified empty Hamming ball through radius 18, but it is not a proof of
a minimum trade size.

## 6. The published point has no first-order Boolean lift

The Hensel equations have algebraic normal forms over `F_2`.  Parameterize
`q` by its 84 skeleton bits and retain the 167 bits of `s`, for 251
independent coordinates.  At the published seed, form the Boolean Jacobian
of the successive bits of `T_k` for `k=1,...,82`.

The exact ranks are:

| layers included | Jacobian rank |
|---|---:|
| modulo 4 | 82 |
| modulo 8 | 163 |
| modulo 16 | 200 |
| modulo 32 | 200 |

More decisively, the affine Newton system

```text
J_(<=16) v = 0,
J_32 v = current degree-8 syndrome
```

is inconsistent: the coefficient rank is 200 and the augmented rank is 201.

This is a finite, exact computation over `F_2`, not a heuristic search.  It
does **not** rule out another point on the modulo-16 variety or a nonlinear
secant from the seed.  It does rule out the most naive Hensel idea: there is
no first-order tangent direction that preserves the three solved layers and
cancels the five next-layer defects.

Therefore the next move must be a genuinely nonlinear switching trade or a
jump to another component of the modular variety.

## 7. A causal-mate split at 42

There is a second exact reduction that explains both the separation by 42 in
(11) and a promising way to construct such a nonlinear jump.

Split each base polynomial at coordinate 42:

```text
X_r(z) = U_r(z) + z^42 V_r(z).
```

All four `U_r` have length 42.  The upper blocks `V_A,V_B` have length 42
and `V_C,V_D` have length 41.  Define

```text
W = sum_r (N(U_r)+N(V_r)),
K = sum_r V_r U_r*.
```

Then the complete base norm is

```text
sum_r N(X_r) = W + z^42 K + z^-42 K*.                    (12)
```

It follows coefficientwise that exact complementarity is equivalent to:

```text
[z^d]K = 0,                              0 <= d <= 41,    (13)
[z^k]W + [z^(k-42)]K = 0,                1 <= k <= 41.    (14)
```

For fixed lower blocks `U`, equations (13) are 42 **linear integer
equations** in the 166 upper signs `V`.  They say that `V` is a one-sided,
or causal, correlation mate of `U`.  Only after an exact causal mate is
chosen do the 41 low-lag equations (14) remain.

For Eliahou's seed, the nonnegative part of `K` is

```text
K_+(z) = -160 +128z^4-96z^8+64z^12-32z^16
       = -32(5-4z^4+3z^8-2z^12+z^16).                   (15)
```

The parenthesis is exactly the nonnegative autocorrelation of the comb
`P`.  Hence the five high-lag defects are a failed causal-mate condition
carried by one short autocorrelation block.

This suggests constructing the upper half as a polynomial syzygy/correlation
mate rather than flipping signs until the high residuals happen to vanish.
Skew-reversal mates provide an obvious starting family: for two vector
components, `(-Y*,X*)` is identically cross-orthogonal to `(X,Y)`.
The missing final entries of the two short sequences create a boundary
defect, so an unmodified skew-reversal ansatz reduces to a
`(42,42,42,41)` complementary problem and fails by parity at lag 41.  A
successful mate must include a nonzero strictly negative tail of `K` to
cancel (14); setting all of `K` to zero is too strong.

## 8. An independent folding reduction

At every 83rd root, fold the two long endpoints:

```text
A~ = (A_0+A_83,A_1,...,A_82),
B~ = (B_0+B_83,B_1,...,B_82).
```

Leave `C,D` unchanged.  For any base quadruple,

```text
PAF_sum(k) = R_k + R_(83-k),       1 <= k <= 82.          (16)
```

In an exact base sequence, the endpoint quad has

```text
(A_0 A_83)(B_0 B_83)=-1.
```

Thus one folded endpoint is zero and the other is `+2` or `-2`, while the
folded zero-lag energy stays 334.  Every `BS(84,83)` therefore gives a
periodically complementary length-83 quadruple with:

- two ordinary binary words;
- one zero folded coefficient;
- one doubled folded coefficient; and
- total periodic energy 334.

The converse needs the 41 independent aperiodic orientation equations and is
not automatic.  This is a useful Fourier screen, but the Hensel/causal-mate
route above appears more constructive.

## 9. Proved dead ends

### Keeping q fixed

The existing `FIXED_Q_OBSTRUCTION.md` reduction to the empty family
`TU(41)` proves that Eliahou's `q` cannot be retained.

### Keeping s fixed

This fails already at `z=1`, independently of search.  With the published
`s`, the fixed long and short first sequences have sums

```text
A(1)=-2, C(1)=3.
```

If only `q` changed, exactness would require

```text
B(1)^2+D(1)^2 = 334-(-2)^2-3^2 = 321.
```

But `3` divides a sum of two squares only when it divides both summands.
That would make the sum divisible by 9, whereas `321` is not divisible by
9.  Hence `s` must change too.

### Strictly alternating q

If `q` alternates in each block, only even-lag edges remain.  At lag 82
there are exactly three active edges: two long and one short.  Three signs
cannot sum to zero.  Equivalently, this word fails the first-lift skeleton.

### The simplest boundary-compatible skew-reversal mate

If the long pair is given its usual skew-reversed mate and the short pair is
made boundary-compatible by taking equal/opposite lower blocks before
dropping the two missing endpoint entries, `K` vanishes identically.  The
remaining equation collapses to a complementary problem with lengths
`(42,42,42,41)`.  Its lag-41 coefficient is a sum of three signs, so this
simple ansatz cannot work.  A more general causal mate should retain a
strictly negative tail of `K` and use (14), rather than annihilating all of
`K`.

### First-order Newton repair

The rank-201 augmented certificate in Section 6 rules out a tangent repair of
the five degree-8 defects.  Nonlinear trades remain possible.

## 10. Most promising actionable construction

The recommended next lane is:

1. **Use the 84-bit q skeleton exactly.**  Generate it by reciprocal pairs or
   by the field equation (4); do not search 167 unconstrained q signs.
2. **Eliminate the modulo-4 s layer.**  For each structured `q`, row-reduce
   (5) and parameterize its affine `s` fiber.
3. **Work on the modulo-16 variety.**  Impose the degree-2 and degree-4
   equations from (6), preferably in algebraic-normal-form or code form.
   This is the modular surface containing Eliahou's point.
4. **Construct a nonlinear comb secant.**  Use the square-root support
   `{13,17,21,25,29}` and its forced reciprocal partners as a template, but
   solve the lower three layers exactly rather than projecting linearly back
   to them.
5. **Impose the causal-mate equations simultaneously.**  In the split-at-42
   form, solve the 42 linear equations (13) by a polynomial syzygy or signed
   lattice construction.  The seed target (15) says exactly which comb
   autocorrelation must disappear.
6. **Lift successively to moduli 32, 64, 128, and 256.**  Modulus 256 is the
   unambiguous finish line: it forces every `T_k` to be zero, after which the
   existing verifier constructs and checks the full `668 x 668` matrix.

The central conjecture is:

> There is a second, nonlinearly separated point on the modulo-16
> `q`-skeleton variety whose degree-8 syndrome is zero and whose split-at-42
> upper block is a causal mate of its lower block.

The Frobenius square (9) and causal defect (15) indicate that this point
should be sought through a five-comb switching trade, not through a generic
Hamming-radius expansion.  This conjecture is concrete and falsifiable:
the lower layers, the five next-layer equations, and the 42 causal equations
are all exact finite algebra.
