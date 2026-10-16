# Scoped independent audit: coefficient bridge, traces, graphs, rough companions

Checkpoint: 2026-10-06 PDT / 2026-10-07T05:33:38Z. No external individuals
contacted; upstream clone read only; no Git mutations. Assigned-audit completion
estimate: 90%. This is **not certification of the full pointwise 2-converse**.
No decisive counterexample or material gap was found in the mechanisms checked
below. The distinction between positively verified algebra and remaining deeper
dependencies is essential.

## Exact reviewed inputs

All paths below are under
/Users/alec/Desktop/math/preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026/build/.

| File | Reviewed scope | SHA256 |
|---|---|---|
| sections/coefficients.tex | Entire file, including weighted bridge, finite precision, traces and omission | 6e2266b43cdada2d63df5c0d5bba8b42e6dd24ea6cc9b230e3d52e9dbc5f213d |
| sections/graphs.tex | Entire file | 2a030319f3fd3f7c357dfb6af3fe6b05bc4ca486daa30d246bad220556b2924f |
| sections/nonvanishing.tex | Entire file | b5c0209d2202cc798c3fc7896432c0c534f51284447df7bd6b84f59243c69963 |
| sections/pointwise.tex | Bounded-companion argument, lines339–425 | 66717dc63cf7821281f988386a24a99f65113cfa1fa97419f8ebd752a78056d3 |

Definitions of L_* and the filters were also checked in preliminaries.tex
lines80–125. No Lean verification claim is made.

## Weighted theta bridge: actual checks

The construction is not merely an appeal to an unnamed weighted theta theorem.
The proof gives finite local Schwartz functions, a finite supersingular function,
and the actual weighted orbit sum. The following calculations were reconstructed.

1. For B=(-a,-b), Q on trace-zero elements is
   aX²+bY²+abZ². Its determinant is (ab)². Thus the extra diagonal Hilbert
   character relative to the ordinary theta multiplier cubed is trivial.
2. At p^e||N, the selected root r on the cyclic quotient scales to ur under
   x→ux. At 2, e_x=(1+x)/2 changes by an invertible affine transformation;
   its two summands remain distinct because the eigenvalue difference is odd.
   This avoids confusing root selection with eigenvalue parity modulo2.
3. At p|h_*, the centralizer of nonzero nilpotent X_0 has square determinant.
   Therefore epsilon(gX_0g^-1)=(det g/p) is well defined, transforms by
   (det u/p) under conjugation and by (a/p) under scalar multiplication.
4. At the detector prime ell≡3 mod4, the trace-zero residue line in
   F_(ell²) has basis beta with beta² nonsquare. The local Legendre weight
   changes sign under the uniformizer's residue automorphism beta→-beta;
   Q(t beta)=-t² beta² is a square. The extraction consequently enforces
   (D/ell)=1. These signs match the norm character chi_(h_*)(ell)=-1 and
   the chosen +1 Frobenius functional.
5. The global scaling parity is even because the level-root parity product
   is the +1 functional sign of E^(h_*), and the h_* and ell signs cancel.
   The local characters away from ell are fixed; the ell character is quadratic.
   Thus their value field need not grow with M or ell.
6. Finite order-unit groups inject into GL4(Z) by their action on the order.
   Their orders are uniformly bounded, so one fixed integer c_0 clears every
   stabilizer denominator. Changing an integer lift P_M(z) by2^M then changes
   every coefficient by2^M O, without a precision loss.
7. A primitive trace-zero element with norm divisible by p² has one invariant
   reduction line. After conjugating its reduction to X_0, its lower-left
   entry is divisible by p². Exactly the corresponding neighbor makes y/p
   integral. The semisimple/nonzero reduction has 1+(-n/p) invariant lines.
   These are the local counts used in the three-term Hecke recurrence.

For the comparison, an embedding stabilizer is O_(K_D)^×={±1}; an orbit has
|R_z^×|/2 elements. There are2^(omega(N)+1) local orientation tuples, and the
Schwartz and norm-weighted parametrization signs agree under each reversal.
Thus the displayed rational multiplier is c_0·2^omega(N), independent of D,
ell,M. This calculation would fail if one divided by a class number; the
manuscript does not do so. The integer L killing cusp constants and bounded
degree torsion is fixed before the detector varies.

The relevant primary geometric sources were actually opened:
[Jetchev–Kane arXiv0908.3905v1](https://arxiv.org/pdf/0908.3905v1), Sections1.1–1.2
and2, permit general N prime to ell and describe enhanced supersingular curves;
[Cornut–Jetchev](https://webusers.imj-prg.fr/~christophe.cornut/papers/liftings.pdf),
Corollary4.1 and Remark6, gives the correspondence with **conjugate pairs** of
optimal embeddings, for conductor prime to ell N. The companion uses conductor1
and split level primes. One must retain that conjugate-pair convention: counting
individual embeddings is twice the pair count. The companion's stabilizer1/2
and extra ell-orientation factor accommodate this distinction. I did not infer
the weighted equality from modularity alone.

Limits: the full adelic reduction/class-action compatibility and the cited
Gross–Zagier formula were not independently reproved from their foundations.
Their required geometric hypotheses were checked, and no mismatch was identified.
This audit does not supply a computed example of the complete CM-weighted sum.

## Finite precision, traces, and whole-prime omission

The odd source does not assert an infinite-precision characteristic-zero lift.
Its minimum argument ranges over bounded-weight sequences with visible
coefficients; integral valuations, a uniform lower bound and a fixed witness
give a discrete attained minimum. For any fixed weight cutoff, violation on an
ultrafilter-large set would give a violating bounded-weight sequence. This
establishes a uniform divisibility statement for **all indices at that weight**,
not merely a selected finite list of discriminants.

The potentially unbounded Fourier-index issue is explicitly handled at
coefficients.tex720–734. For fixed w(U)≤W, the normalization powers are bounded.
Large squarefree weights use the coarse min(M,w(D)-C) bound to pay the
normalization plus the requested truncation R; bounded weights use the attained
minimum. Integral Hecke multipliers retain precision at every square shell.
Calling this passage absent would be inaccurate; its input arithmetic lower
bound remains a separate dependency proved elsewhere in the manuscript.

The trace lattice argument is coherent: finitely many coefficients inject the
finite-dimensional space into O^r, so an integral Hecke/diamond-generated
submodule is finite and closed. Chebotarev approximation then preserves that
lattice. The diamond correction is an undivided unary term because its
character difference is0 or twice a unit. A fresh trace kills this correction
on reduced expansions. Thus the determinant-removal trace identity is justified
on the stated reduced trace orbit, without assuming saturation of the lattice.

At a new p, a conductor-one constituent with ramified quadratic determinant
has inertia diag(1,-1) and Frobenius diag(lambda,mu). Both sides of the
inertia identity equal -2z lambda mu, where z is the lower-right entry of
rho(g). Old constituents give zero on both sides. The local classification
and arithmetic-Frobenius convention are the external local-compatibility input.

The contraction normalization exponents were independently checked:

| Removed p | U parity | 1+n_V-n_U-m_U+m_V |
|---|---|---:|
| split, weight1 | either |0|
| simple, weight1/2 | matching |0|
| simple, weight1/2 | opposite |1|

The last row is the zero simple–simple derivative. More importantly, the
omitted source is B_V or H_V from the **same original form and minimum**, with
V=U\{p}. Its support is S∪V. In the odd case S includes the stationary detector
ell. The original character is unramified at p, and only V introduces new
characters. Therefore **both places over the removed rational prime** are
unramified, and both oriented inertia bits disappear. This is explicit at
coefficients.tex977–998. The second oriented derivative vanishes for this
reason; it is not an assumption that omitting one oriented ideal suffices.

## Graph detector: independent algebra and executed checks

The ray-class realization proof preserves support valuations and signs, so
the rational S-unit norm correction of a product template is the same as that
of its fresh representative. It does not leave an untracked arbitrary S-unit.
Independent residues at old split places can be prescribed by weak
approximation; reverse residues then follow from reciprocity. The finite
prime-ideal theorem supplies degree-one representatives. No fixed infinite
array of representatives is required.

The network expansion uses finite differences, not a heuristic determinant
analogy. Cycles vanish by the whole-prime omission rule; isolated primary
components vanish by isolation. The grounded determinant and adjugate pair
coefficient follow from Cauchy–Binet on incidence matrices. For the singular
program T=I+P, proper restrictions are invertible, while the full matrix has
radical sum(u_i); hence exactly the selected pair survives in degree1. For the
nonsingular program T=I+L, changing B at(bb) changes the u_1 self-pair by
((T_J^-1)_(b1))², which is1 only when the whole path survives.

Executed reproduction:

    python3 verification/check_two_converse_programs.py

The standard-library script independently constructs physical matrices,
coincident anchor/terminal roles and balancing terminal activations. For
b=1,...,5, **62 active-group restrictions and three programs each** passed
the grounding row sums, constant determinants, singular selected-pair tests,
and nonsingular degree-one pair differences. This is finite evidence for
those formulas, not a proof of the entire arithmetic interface. Script SHA256:
580ce6af8d71f9bc6175e96b097cc146168073b59ce03d9bdc75d8f27638567e.

The two-symbol degree budget also checks formally: singular programs force
one difference in each target factor; each nonsingular choice sum requires at
least one difference somewhere. Their total minimum cost is exactly the sum
of the terminal polynomial degrees. Any excess kills a factor. Thus only
prescribed first-degree pieces survive, and the remaining allocation is the
coefficient of a chosen monomial in the ordinary product of the two top forms.
Using the ordinary polynomial ring before Boolean reduction is necessary and
correct (e.g. z·z=z² allocates one difference to each factor).

## Bounded-factor negative companions

The rough completion needs more than a named nonvanishing theorem: an absolute
prime-count bound survives varying curves/moduli only if its distribution
exponents eta,B are absolute. The manuscript provides a proof of a divisor
moment with precisely this quantifier order; implied constants may depend on
the curve and progression.

The algebraic local factors were checked: the zero-frequency density is
beta_p=(p-1)/(p² H_p-1)=1/(1+p F_p^ev). Since |lambda(p)|≤2 and
F_p^ev=1+O(1/p), this is1/p+O(1/p²) with an absolute error constant.
The prime-power Gauss-sum cases are the usual Ramanujan sum at even exponent
and primitive Gauss sum at odd exponent; away from HJnu they leave the factor
1+lambda(p)xi(p)p^-s. The resulting correction product is holomorphic for
Re(s)>1/2. Thus the stated contour mechanism is internally consistent.

Given its moment bound, choosing (B+1)theta<eta makes the total divisor
remainder o(X/log X). The lower dimension-one sieve with z=X^(theta/s), s>2,
then leaves positive weight. Its supported n<2X has fewer than a fixed
integer exceeding2s/theta prime factors. This count is independent of the
curve/filter, while the threshold X may depend on them. No prime-twist
nonvanishing theorem is smuggled into this deduction.

For pointwise.tex355–425, absorbing h and the bounded dummy product changes
the curve and size threshold, not that factor-count bound. The final negative
k', square at2Nh and coprime to2Nh, changes the root number of E^(h) by
chi_(k')(-N_(E^(h)))=-1. The reduced local progression is nonempty by CRT.
However the bounded dummy/reserve supply and partitionability estimate depend
on other pointwise lemmas outside this assigned audit; this report does not
certify them. The analytic second-moment, strip-bound and sieve inputs were
reviewed for consistency, but their full published proofs were not reproduced.

## Honest remaining gap in this audit

There is no demonstrated material proof failure in the above scoped mechanisms.
Full certification would still require the remaining pointwise/ring-class/
cyclotomic arguments, the uniform arithmetic lower bounds used by the symbol
normalization, and complete validation of the external analytic inputs.
Neither the executed matrix checks nor this favorable local audit resolves
those tasks, proves H10(Q) undecidability, or licenses an unconditional follow-on
claim. If a separate audit finds a substantive upstream gap, the geometric
conditional theorem remains valid and publication must respect that gap.
