# Independent audit of the cyclic CN coefficient

Audit timestamp: 2026-10-24 19:35 UTC. Scope: coefficient identity,
reflection obstruction, finite-field implication, and cautions about algebra
extensions. No external communication or Git actions were taken.

## Strongest verified conclusion

Put `N=n(n-1)/2`, `V(x)=product_(i<j)(x_j-x_i)`,
`s_i=x_i+x_(i+1 mod n)`, and
`C_n=[x_0^(n-1)...x_(n-1)^(n-1)] V(x)V(s)` over the integers.
If `A` is an `n`-element subset of a field of characteristic `p` and
`C_n` is nonzero in that field, some cyclic ordering of `A` has pairwise
distinct adjacent sums. In characteristic zero the corresponding condition
is `C_n != 0`. Every finite elementary abelian `p`-group can be identified
additively with a finite field, so the same implication applies to it.

No conclusion follows from this argument when `C_n` vanishes in the field.
In particular, even `n` is an obstruction to this coefficient method, not
a counterexample to the underlying cycle assertion.

## Exact antisymmetrization identity

Let `f(x)=V(s)` and define
`Alt(f)=sum_(sigma in S_n) sign(sigma) f(x_(sigma(0)),...,x_(sigma(n-1)))`.
This polynomial over the integers is alternating: each `x_j-x_i` divides
it. The factors are pairwise nonassociate primes in `Z[x]`, and its degree
is `N`, so `Alt(f)=kappa V(x)` for an integer `kappa`.

For a permutation `tau`, write `x^tau=product_i x_i^(tau(i))`, so that
`V(x)=sum_tau sign(tau) x^tau`. The coefficient of
`x_0^0 x_1^1 ... x_(n-1)^(n-1)` in `Alt(f)` is
`sum_tau sign(tau) [x^tau]f = kappa`. Complementing the exponents of a
permutation by `n-1` changes its sign by `(-1)^N`. Consequently

`C_n=(-1)^N kappa`.

Since `V(0,1,...,n-1)=product_(k=0)^(n-1) k!`, this proves the exact formula
used by `verify.py`. The division is performed over the integers (or
rationals) before reducing modulo `p`. Evaluating that ratio directly in
characteristic `p<n` would have zero denominator and is invalid.

## Reflection obstruction

The reflection `r(i)=-i mod n` permutes the `x` variables. It permutes the
sum variables by `q(i)=-i-1 mod n`. These permutations differ by a cyclic
shift, whose sign is `(-1)^(n-1)`. Therefore reflection multiplies
`V(x)V(s)` by `(-1)^(n-1)`. The target monomial is reflection-invariant,
so `C_n=0` over the integers for every even `n`. This integer result then
reduces to zero in every characteristic, including characteristic two.

Boundary cases: `C_1=1` with both Vandermonde products empty; `C_2=0`
because both adjacent sums are the same.

## Finite-field nonvanishing implication

For `g(t)=product_(a in A)(t-a)`, all `g'(a)` are nonzero in the field.
The multivariate Lagrange coefficient identity gives

`C_n=sum_((a_0,...,a_(n-1)) in A^n) P(a_0,...,a_(n-1))/product_i g'(a_i)`.

This holds because `deg(P)=n(n-1)`: in each monomial other than the
target, at least one exponent is below `n-1`, and the corresponding
one-variable weighted sum is zero. If `C_n` is nonzero, some evaluation
of `P` is nonzero. Its first Vandermonde forces the `a_i` to be distinct,
and its second forces the adjacent sums to be distinct. Since there are
`n` distinct `a_i` in the `n`-element set, this is the required ordering.

There is no requirement that `p>=n`; the actual denominators use distinct
elements of `A`, and a field extension can contain more than `p` elements.
The integer coefficient is reduced modulo `p` after it has been computed.

## Computational reproduction

The existing script reproduces

| n | C_n |
| --- | ---: |
| 3 | 6 |
| 4 | 0 |
| 5 | 980 |
| 6 | 0 |
| 7 | 2292864 |
| 8 | 0 |
| 9 | 87215071680 |

In addition to the script's independent direct factor multiplication for
`n=3,4,5`, this audit ran the direct expansion for `n=1,2,6,7` and found
`1,0,0,2292864` respectively. The `n=7` direct check took about 0.21 s.
The `n=9` value is verified by the proved alternating-sum formula and its
exact evaluation, but has not received an independent direct-expansion
check in this audit.

## Limits and possible hidden assumptions

* These computations do not prove `C_n != 0` for all odd `n`.
* A prime dividing `C_n` is an exception to the sufficient criterion,
  not evidence that a cycle does not exist. The supplied characteristic-7
  example for `n=5` correctly demonstrates this distinction.
* A general finite abelian group cannot be embedded additively in a field:
  positive-characteristic field additive groups have exponent `p`.
  Thus the argument does not automatically extend to higher prime powers,
  arbitrary products of different characteristics, or general nilpotent
  groups.
* Over a ring with zero divisors, the field interpolation proof needs
  pairwise differences in the interpolation set to be units. Merely being
  distinct is insufficient. A product of nonzero factors can also vanish.
* In the commuting truncated algebra
  `R[x_0,...,x_(n-1)]/(x_0^n,...,x_(n-1)^n)`, the image of `P` is exactly
  `C_n product_i x_i^(n-1)`. This is a coefficient reformulation; it does
  not by itself produce an evaluation or escape the even-`n` obstruction.
* Ordinary Grassmann generators anticommute and square to zero. Replacing
  commuting `x_i` by odd generators changes the polynomial identities.
  Encoding commuting variables by even Grassmann elements requires its own
  algebra homomorphism and nonvanishing proof; factorial coefficients can
  vanish in small characteristic. A Grassmann reformulation that only
  asserts the image is nonzero has transferred the central difficulty
  unless that nonvanishing is independently proved.

Audit completion estimate: 100% of this narrowly assigned verification;
this is not a completion estimate for the underlying research problem.

## Follow-up audit of RESULTS.md sections 4–5

The explicit exterior and connected-trace formulations in `RESULTS.md`
pass independent inspection. The exterior reversal sends the rooted edge
list to its full reversal, so the claimed `(-1)^(n(n-1)/2)` sign is exact.
The rotation and reversal actions have the stated cancellation orbits when
the vertex labels are distinct, as required here.

For the determinant, every permutation cycle of length at least three has
two orientations, giving multiplicity `2^c` for `c` unoriented components;
its permutation sign is `(-1)^(n-c)`. Squarefree colors eliminate
2-cycles but do not force one component.

For the connected replacement, an individual term in `tr(B^n)` is a closed
walk of length `n`, and its vertex-variable factor marks each source
vertex once per departure. Its full squarefree vertex coefficient can
therefore survive only if it visits every vertex exactly once. For `n>2`,
each unoriented Hamiltonian cycle contributes exactly `2n` copies. In the
commuting square-zero color quotient over `Q`, distinct squarefree
monomials form a basis; surviving positive coefficients cannot cancel.
Thus the stated nonzero-if-and-only-if assertion is correct. It is also
correctly labeled as an exact restatement rather than an existence proof.

The logarithmic identity is valid over this commutative `Q`-algebra as a
formal series: `[t^n](-log det(I-tB))=tr(B^n)/n`. Nilpotence of the vertex
ideal makes the series finite here. For literal clarity, the section's
display should state `n>2`, and a reference to the entire degree-`n` term
should include its factor `t^n`. These are presentational cautions only.
