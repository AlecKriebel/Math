# Quadratic algebra for the two dense order-three profile shells

## Status

The first genuinely quadratic lambda-adic response of the order-three
profile problem has an exact six-dimensional algebra

```text
F_27 x F_27.
```

On one channel its 364 projective nonzero pencils have only two ranks:

```text
rank 12: 338 pencils,
rank  6:  26 pencils.
```

More strikingly, the sum of the six reversal-independent polar matrices is

```text
M_0+M_1+...+M_5 = 2 I_12                       over F_3.       (1)
```

Thus the all-ones pencil is nonsingular on every support, without exception.
This applies to both remaining dense type sectors

```text
h=n_9=1: (n_9,n_3,n_0)=(1,15,8),
h=n_9=0: (n_9,n_3,n_0)=(0,18,6).
```

After imposing the actual local phase rows and the two channel-aggregate
rows, the restriction of (1) still has rank at least five in the
15-medium shell and at least six in the 18-medium shell.  Exact quadratic
Gauss-sum bounds then show that **every** value in `F_3` is attained on
every nonempty affine fiber:

```text
15-medium shell: at least  2,025 points for each right-hand side,
18-medium shell: at least 54,675 points for each right-hand side.          (2)
```

Consequently the universal nonsingular pencil is not an exclusion by
itself.  Its role is a lossless character-sum compression of the complete
six-coordinate quadratic system.  This checkpoint neither excludes a
dense shell nor produces an exact profile or an `H(668)`.

## 1. The correction variables

Put

```text
lambda=1-omega,             omega^2+omega+1=0.
```

A signed medium letter is

```text
sigma lambda omega^u,       sigma in {+1,-1}, u in F_3.
```

Relative to phase zero,

```text
sigma lambda(omega^u-1)=lambda^2 x,
x=-sigma u                         modulo lambda.          (3)
```

The change of variable `u -> x` is a bijection on `F_3`; it absorbs every
signed skeleton coefficient.

For one opposite quartet, exact division of the four origin/medium
responses by `lambda^2` gives the same nonzero coefficient in all four
positions:

```text
A_j, A_(j+6), B_j, B_(j+6):       -x modulo lambda.        (4)
```

The channel aggregate response is `+x`.  Therefore, after harmless row
scaling, the lower phase constraints have the literal incidence form

```text
sum_(i in quartet q) x_i = c_q             (q nonempty),
sum_(i in channel A) x_i = c_A,
sum_(i in channel B) x_i = c_B.                            (5)
```

The sum of the two channel rows is the sum of the nonempty quartet rows.
Both dense shells necessarily have a quartet containing medium letters in
both channels: otherwise every quartet would contain at most two media and
the total would be at most twelve.  Hence, if `r` quartets are nonempty,
(5) has exact rank

```text
r+1.                                                       (6)
```

In the one-high shell the high insertion is already fixed modulo `lambda`
at this digit; its phase occurs later.  It changes constants and linear
terms but not the medium-variable polar matrices below.

## 2. Six quadratic forms

Write the correction word in one channel as twelve class values
`x_0,...,x_11`.  For a representative `t_j` of `C_j`, `0<=j<6`, the
quadratic correlation term modulo `lambda` is

```text
q_j(x)=sum_(c in F_37^*) x(c+t_j)x(c),                    (7)
```

where the `H`-invariant class value is expanded to all physical elements.
Eisenstein conjugation is trivial modulo `lambda`.  Let `T_j` be the
physical transition matrix in (7).  The polar matrix is

```text
M_j=T_j+T_j^T in Mat_12(F_3).                             (8)
```

For two channels the matrix is simply `M_j direct_sum M_j`.

Direct cyclotomic counting proves (1).  In quadratic-form language,

```text
q_0+q_1+...+q_5 = sum_i x_i^2.                            (9)
```

This is a radial Hamming-weight congruence: over `F_3`, `x_i^2` is zero or
one.

## 3. The `F_27 x F_27` algebra

The six matrices in (8) are independent, symmetric, mutually commuting,
and closed under multiplication.  Their span contains the identity with
coordinate vector

```text
(2,2,2,2,2,2).
```

It has exactly four idempotents:

```text
0,
e_+=(2,0,2,0,2,0),
e_-=(0,2,0,2,0,2),
1  =(2,2,2,2,2,2).                                      (10)
```

The two nontrivial idempotents are orthogonal and sum to one.  Their
principal ideals each:

- contain exactly 27 elements;
- have dimension three over `F_3`;
- have no zero divisors;
- act with rank six on the twelve-dimensional class space.

Thus each component is the field `F_27`, proving

```text
span_F3{M_0,...,M_5} ~= F_27 x F_27.                     (11)
```

A pencil supported in exactly one field component has rank six.  There are
`13+13=26` such projective points.  A pencil with both components nonzero
has rank twelve, accounting for the other 338 points.

This is the ramified quadratic analogue of the two primitive spectral
coordinates in the previously established semisimple profile algebra.

## 4. Restriction to the actual affine phase spaces

For a medium-support mask, let `K` be the homogeneous kernel of (5).  The
universal form (9) has standard dot-product polar form.  If `R` is a
full-row-rank incidence matrix for (5), then

```text
rad(q_sum restricted to K)
  = K intersect row(R),

dim rad = (r+1)-rank(R R^T).                              (12)
```

Writing

```text
d   = dim K = n_3-(r+1),
rho = rank(q_sum restricted to K),
nu  = dim rad,
```

gives `rho=d-nu`.  Exhausting only the legal support masks—not signs and
not phases—gives the following exact census.

### Fifteen-medium shell (`h=1`)

```text
(r,d,rho,nu)       support masks
(4,10,10,0)               240
(5, 9, 5,4)             6,144
(5, 9, 7,2)            46,080
(5, 9, 9,0)            25,920
(6, 8, 6,2)           276,480
(6, 8, 8,0)           155,520
--------------------------------
total                  510,384
```

### Eighteen-medium shell (`h=0`)

```text
(r,d,rho,nu)       support masks
(5,12,11,1)             1,080
(5,12,12,0)                60
(6,11, 6,5)             4,096
(6,11, 8,3)            46,080
(6,11,10,1)            53,280
(6,11,11,0)             2,880
--------------------------------
total                  107,476
```

Every non-singleton local mask admits signed skeletons, so this is the
complete unsigned support census relevant to the lower phase row.

## 5. Why the universal form cannot exclude either shell

Let a quadratic polynomial on an affine `d`-space over `F_3` have
homogeneous rank `rho`.  If its linear part is nonzero on the radical, each
fiber has exactly

```text
3^(d-1)
```

points.  Otherwise completing the square and evaluating the ordinary
quadratic Gauss sum gives the uniform error bounds

```text
rho odd:
  |N_c-3^(d-1)| <= 3^(d-(rho+1)/2),

rho even:
  |N_c-3^(d-1)| <= 2*3^(d-rho/2-1).                      (13)
```

Applying (13) to every row of the two censuses yields (2).  In particular,
the sum of the six quadratic equations is never anisotropically
incompatible after the local and aggregate affine constraints.  Any
exclusion must use the other five directions jointly, a higher
lambda-adic digit, or an independent characteristic-37 condition.

This negative conclusion is useful: treating (1) as a hoped-for single
obstruction would spend time on a gate that is provably surjective with
large fibers.

## 6. Lossless character-sum compression

The complete six-coordinate quadratic layer can nevertheless be counted
without enumerating `3^d` phase assignments.  If

```text
Q: x_0+K -> F_3^6
```

is the actual affine quadratic map and `b` is its required right-hand side,
orthogonality of additive characters gives

```text
# {x in x_0+K : Q(x)=b}
 =
3^(-6) sum_(c in F_3^6)
  psi(-c dot b)
  sum_(x in x_0+K) psi(c dot Q(x)).                       (14)
```

Each inner sum in (14) is an exact quadratic Gauss sum.  Gaussian
elimination supplies:

- the rank of the restricted pencil;
- whether its linear term vanishes on the radical;
- its discriminant and phase.

Thus all six quadratic congruences can be counted using 729 small linear
algebra calculations.  A zero count discards the skeleton.  A positive
count can be self-reduced by fixing one trit at a time and reevaluating
(14), producing witnesses without scanning the full phase cube.

The `F_27 x F_27` split makes the ambient rank classification in these 729
calculations immediate; only restriction to the support/affine kernel
remains.

## 7. Reproduction

From `hadamard_668_search`:

```text
python3 verify_lp333_order3_dense_shell_quadratic_algebra.py

c++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  audit_lp333_order3_dense_shell_quadratic_pencil.cpp \
  -o /tmp/audit_lp333_order3_dense_shell_quadratic_pencil
/tmp/audit_lp333_order3_dense_shell_quadratic_pencil
```

The Python verifier independently reconstructs:

- the `F_37` cyclotomic transitions;
- the exact local and aggregate phase-row coefficients;
- closure, commutativity, identity, and idempotents of the pencil algebra;
- the `338/26` projective rank split;
- the two order-27 field ideals;
- every legal dense support mask;
- every affine restriction rank and radical dimension;
- the numerical Gauss-sum lower bounds.

The reference run used about 18 MB maximum resident memory.  The C++ rank
audit used about 3 MB.  Neither verifier enumerates a phase assignment,
invokes a solver, or mutates repository state outside this scratch folder.
