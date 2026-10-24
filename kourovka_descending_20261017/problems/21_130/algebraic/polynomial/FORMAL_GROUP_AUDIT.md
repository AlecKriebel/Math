# Independent audit of the Lubin–Tate transfer

Timestamp: 2026-10-24 19:43 UTC. Completion of this assigned audit:
**100%**. Verdict: the proposed transfer from a unit reduced-polynomial
coefficient to finite abelian `p`-groups is valid, subject to the precise
unit hypothesis below. No all-`n` coefficient assertion is assumed.

## Exact transfer statement

Let `n>2` and let `Q_n` be the reduced adjacent-sum polynomial defined in
`SLACK_AUDIT.md`. Suppose some coefficient `[x^t]Q_n` is not divisible by
`p`, with `0<=t_i<=n-1` and `sum(t_i)=d=n(n-2)`. Then every `n`-element
subset of every finite abelian `p`-group admits a cyclic ordering with
pairwise distinct adjacent sums.

Consequently the independently checked coefficient witnesses for
`3<=n<=9` prove this conclusion in every finite abelian `p`-group for
every odd prime `p`. This transfer alone does not cover abelian groups
with several different prime divisors.

## Source check and embedding

The supplied original text `../LubinTate1965.txt` was read directly.
Lubin–Tate, *Formal Complex Multiplication in Local Fields*, Annals of
Mathematics 81 (1965), 380–387, constructs an integral commutative
one-dimensional formal group `F(X,Y)=X+Y+terms of degree >=2`.
On p.383 it defines its group/module operations on the maximal ideal of
an algebraic extension by convergent series. Theorem 2(b), pp.383–384,
states that its `pi^k`-torsion is isomorphic as an `O_K`-module to
`O_K/pi^k O_K`. The paper is [JSTOR 1970622](https://www.jstor.org/stable/1970622).

For a finite abelian `p`-group of exponent at most `p^k` and generator
rank `r`, choose an unramified extension `K/Q_p` of degree `h>=r`.
Here `pi=p`, and the additive group `O_K/p^k O_K` is
`(Z/p^k Z)^h`, which contains the given group. Its Lubin–Tate torsion
realizes this embedding by coordinates in the maximal ideal. A finite
extension `L/K` contains the finitely many torsion coordinates needed.
Thus the elements of the set in question have distinct coordinates
`b_1,...,b_n` in the maximal ideal `m` of `O_L`, with original group
addition represented by `F` on these coordinates.

## Convergent finite-free substitution

Set `g(X)=product_(b in A)(X-b)`. It is monic of degree `n` and
`g(X) congruent X^n mod m`. Therefore

`R=O_L[x_1,...,x_n]/(g(x_1),...,g(x_n))`

is finite free over the complete DVR `O_L`, with basis the monomials
having every exponent below `n`. In particular it is complete and
torsionfree. Every `x_i^n` lies in `mR`. Hence
`x^alpha` lies in `m^(sum_i floor(alpha_i/n)) R`; this exponent tends
to infinity as total degree tends to infinity. It follows that every
integral formal series admits a convergent substitution into `R`.
This justifies the proposed element

`Q_F=V(x) product_(nonadjacent i<j)(F(x_j,x_(j+1))-F(x_i,x_(i+1)))`.

No interchange of divergent sums, denominator inversion, or passage
to a noncomplete infinite algebraic extension is needed.

## Why the additive coefficient survives

There is a graded identification

`R/mR = k_L[x_1,...,x_n]/(x_1^n,...,x_n^n)`.

The reduction of `F` need not equal `X+Y`. This is harmless: its linear
homogeneous part is `X+Y`, so the least total degree of `Q_F` is `d`,
and its degree-`d` homogeneous part is exactly `Q_n` reduced modulo `p`.
The quotient on the right is homogeneous, so higher-degree terms cannot
alter a degree-`d` coefficient. Since the selected `t_i` are below `n`,
the selected nonzero coefficient survives in the quotient. Thus the
image of `Q_F` in `R/mR`, and therefore in `R`, is nonzero.

## From a nonzero remainder to an ordering

Freeness injects `R` into `R tensor_(O_L) L`. Since the roots of `g`
are distinct and all lie in `L`, the usual characteristic-zero Chinese
remainder isomorphism identifies that scalar extension with
`product_(a in A^n) L`. The coordinate maps are evaluations; they are
continuous, so the evaluation of the substituted formal series agrees
with its convergent series evaluation at the torsion coordinates.
Nonzero `Q_F` therefore has a nonzero evaluation on `A^n`.

At such an evaluation, `V` forces all coordinates to be distinct, hence
to enumerate `A`. All nonadjacent edge sums are distinct by the retained
factors. Adjacent edge sums cannot be equal by cancellation in the
embedded group: equality of the sums of `(a_i,a_(i+1))` and
`(a_(i+1),a_(i+2))` would imply `a_i=a_(i+2)`, impossible for `n>2`.
Thus all edge sums are distinct.

## Adversarial checks and exact limits

* Closely spaced torsion coordinates cause nonunit Vandermonde
  denominators over `O_L`, but no interpolation over that ring is used.
  The nonvanishing test occurs modulo `m`, followed by CRT over `L`,
  where all distinct differences are invertible.
* Nonzero reduction modulo `m` suffices; no additive coefficient is
  asserted to equal the corresponding full remainder coefficient.
* The unit condition means `p` does not divide the integer coefficient;
  this is unchanged by the residue-field extension or ramification of `L`.
* The construction permits zero among the torsion coordinates.
* The proof uses abelian group addition and proves no nonabelian result.
* The checked range is `3<=n<=9`. Extending the range requires additional
  unit coefficient certificates or a general theorem about `Q_n`.

No Git or external communication actions were taken by this audit.
