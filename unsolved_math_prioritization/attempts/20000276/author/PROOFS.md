# Asymptotic F-pure thresholds of graded families

## 1. Precise regular-local theorem

Let `(R,m)` be an F-finite Noetherian regular local ring of characteristic `p>0`.
Let `I_n`, for every integer `n>=1`, be a nonzero proper ideal, and assume only

`I_a I_b ⊆ I_(a+b)` for all `a,b>=1`.

Then, in the extended interval `(0,+infinity]`,

`lim_(n→infinity) n fpt_R(I_n) = sup_(n>=1) n fpt_R(I_n)`.

Neither descendingness, finite generation of the Rees algebra, monomiality,
primaryness, nor a linear bound on the ideals is assumed. The proof below
establishes this theorem; it does not identify the unspecified ring in the
original AIM question with a regular local ring. Section 8 gives a singular
counterexample to an unrestricted-ring reading, even with nonzero ideals
containing nonzerodivisors.

## 2. Frobenius conventions and elementary facts

Put `q=p^e`, and write `m^[q]=(x^q : x in m)`. For a nonzero proper ideal `J`, set

`nu_J(q)=max{a>=0 : J^a is not contained in m^[q]}`,
`c(J)=lim_e nu_J(p^e)/p^e`.

This is the usual local F-pure threshold in the regular setting. Here are all
properties of it used in the proof.

By Kunz's flatness theorem, Frobenius is faithfully flat on a regular local
ring. Thus `u^p in K^[p]` if and only if `u in K`. It follows that
`nu_J(pq)>=p nu_J(q)`. If `d=dim R`, a regular system of parameters generates
`m`, and the pigeonhole principle gives
`m^(d(q-1)+1) ⊆ m^[q]`. Consequently `0<=nu_J(q)<=d(q-1)`.
The displayed ratios are nondecreasing and bounded, so their limit exists
and equals their supremum.

The limit is positive. Indeed choose nonzero `f in J`. The Krull intersection
theorem and `m^[q] ⊆ m^q` give a power `q` with `f notin m^[q]`.
Then `nu_J(q)>=1`, hence `c(J)>=1/q>0`.

If `J⊆K`, then `nu_J(q)<=nu_K(q)` and `c(J)<=c(K)`.
For every positive integer `s`,

`nu_(J^s)(q)=floor(nu_J(q)/s)`, so `c(J^s)=c(J)/s`.

There is no endpoint ambiguity in that floor identity. These facts also
cover `s=1`. We separately put `I_0=R` when useful and use `c(R)=+infinity`;
the proof never divides by that value.

## 3. Frobenius separation lemma

**Lemma.** If `q=p^e`, `Q=p^f`, `u notin m^[q]`, and `v notin m^[Q]`, then

`u^Q v notin m^[qQ]`.

**Proof.** The module `F_*^f R` has scalar action
`a · F_*^f b = F_*^f(a^Q b)`. F-finiteness and regularity make this a finite
free R-module. Moreover,

`m(F_*^f R)=F_*^f(m^[Q])`.

Thus `F_*^f v` is outside the maximal-ideal multiple of a finite free module.
In a free basis it has a unit coordinate. Project to that coordinate and
multiply by its inverse to obtain an R-linear map `phi:F_*^f R→R` with
`phi(F_*^f v)=1`.

If `u^Q v` belonged to `m^[qQ]`, then
`F_*^f(u^Q v)` would belong to `m^[q](F_*^f R)`, whose image under `phi`
is contained in `m^[q]`. But R-linearity gives
`phi(F_*^f(u^Q v))=u`. This contradicts the hypothesis. QED.

This lemma must not be replaced by the false assertion that two arbitrary
Frobenius-noncontained elements have a noncontained ordinary product at the
same scale. The asymmetry `u^Q v` and the larger scale `qQ` are essential.

## 4. Fixed-factor lemma, including its quantifiers

**Lemma.** For fixed nonzero proper ideals `I,J`,

`lim_(k→infinity) k c(I^k J)=c(I)`.

More precisely, fix `q=p^e` and an integer `a>=1` with
`I^a notsubseteq m^[q]`. Choose `0≠f in J`, and put `delta=c((f))>0`.
For every integer `k>a/delta`,

`k c(I^k J) >= a/q`.

**Proof.** Select `u in I^a \ m^[q]`. Keep `q,a,f,k` fixed. For `Q=p^f'`
let `h_Q=floor(aQ/k)`. Since `a/k<delta` and
`nu_(f)(Q)/Q→delta`, for all sufficiently large `Q` one has
`h_Q<=nu_(f)(Q)`. Hence `f^h_Q notin m^[Q]`.
The separation lemma yields

`u^Q f^h_Q notin m^[qQ]`.

As `aQ>=k h_Q`, the ideal-power containment and membership `f in J` give

`u^Q f^h_Q in I^(aQ) J^h_Q ⊆ I^(k h_Q) J^h_Q = (I^k J)^h_Q`.

Therefore `nu_(I^k J)(qQ)>=h_Q`. Let `Q` tend through powers of `p` with
`q` and `k` fixed. The product `qQ` is a cofinal sequence of Frobenius
powers, so

`c(I^k J) >= lim_Q h_Q/(qQ)=a/(kq)`.

This proves the precise bound. On the other hand `I^k J⊆I^k`, so
`k c(I^k J)<=c(I)`. Given any `epsilon>0`, first choose fixed `q` with
`a=nu_I(q)>=1` and `a/q>c(I)-epsilon`; only then choose `k>a/delta`.
Thus the lower bound tends to `c(I)`, and the upper bound proves the lemma.
No exchange of two uncontrolled limits is used. QED.

The same conclusion for `J=R` is exactly the power formula and requires no
choice of `f`. The proof also works if `J` is replaced by a fixed positive
power of itself.

## 5. All residue classes: proof of the theorem

Set `A_n=n c(I_n)` and `L=sup_n A_n`. Multiplicativity gives
`I_n^k⊆I_(kn)` and therefore `A_(kn)>=A_n`. In particular
`limsup A_n=L`, with the same statement when `L=+infinity`.

Fix one positive integer `r`. For each `s=1,...,r-1`, write an index in the
residue class as `n=kr+s`. Multiplicativity gives

`I_r^k I_s ⊆ I_(kr+s)`.

The fixed-factor lemma, applied separately to the finitely many fixed
ideals `I_s`, gives

`liminf_k (kr+s)c(I_(kr+s)) >= r c(I_r)`.

For `s=0`, the same conclusion follows directly from
`c(I_r^k)=c(I_r)/k`. Every sufficiently large integer belongs to one of
these finitely many residue classes. A finite union of sequences each with
liminf at least `r c(I_r)` has the same lower bound for its full liminf.
Consequently

`liminf_n A_n >= r c(I_r)` for every `r>=1`.

Taking the supremum in `r` proves `liminf A_n>=L`. The opposite inequality
against the limsup is automatic, so the claimed extended limit exists and
is `L`. If `L=+infinity`, the argument says that for every real bound `B`
choose `r` with `r c(I_r)>B`; then all sufficiently large `A_n>B`.
This explicitly proves convergence to infinity, not just unboundedness. QED.

## 6. Descending filtrations need no Noetherian hypothesis

There is a much shorter argument when `I_(n+1)⊆I_n`. It uses only inclusion
monotonicity and the power formula, so it applies to any nonnegative
threshold invariant having those two properties.

For a fixed `r`, let `k=ceil(n/r)`. Then

`I_r^k ⊆ I_(kr) ⊆ I_n`,

whence `n c(I_n)>= (n/k)c(I_r)`. As `n→infinity`, `n/k→r`.
Thus `liminf A_n>=r c(I_r)` for every `r`, and the supremum argument proves
convergence. In particular, the finite factor-p gap left in the imported
prior attempt is unnecessary; the liminf equals the full supremum.

If a standard Veronese exists, meaning `I_(dr)=I_d^r` for all `r>=1`, the
limit is consequently `d c(I_d)`. For a finitely generated graded Rees
algebra such a `d` exists. The regular-local theorem shows that descendingness
is not needed for this last conclusion either, provided every positive
family term is nonzero proper. Finite generation is needed for the
standard-Veronese formula, not for existence of the general limit.

## 7. Crossing indices are a different definition with the same value here

For `q=p^e`, define

`b_e=sup({r>=1 : I_r notsubseteq m^[q]} union {0})`,

allowing `+infinity`. Faithful flatness and `I_r^[p]⊆I_r^p⊆I_(pr)` give
`b_(e+1)>=p b_e`. Thus `Gamma=lim_e b_e/p^e` exists in `[0,+infinity]`.
For any fixed `r`, `I_r^nu_(I_r)(q)⊆I_(r nu_(I_r)(q))` gives
`b_e>=r nu_(I_r)(q)` (the zero exponent is trivial). Hence
`Gamma>=r c(I_r)`.
Conversely, every index `r` outside `m^[q]` satisfies `c(I_r)>=1/q` and
therefore `r/q<=sup_n n c(I_n)`. Take the supremum over those indices and
then the limit in `e`. It follows that

`Gamma=sup_n n c(I_n)=lim_n n c(I_n)`.

A bounded set of such indices has an attained integer maximum; an unbounded
set gives infinity on both sides of the preceding estimate. Thus gaps in
the index set and infinite crossings are covered. This identifies, in our
regular-local setting, the termwise invariant with the maximal-ideal
filtration F-threshold of Koley--Kumar. Their definition must not simply be
substituted for the termwise limit before proving this identification.

## 8. Boundary: a singular F-pure ring with a finite oscillation

The wording “a ring R” is insufficient for the affirmative theorem above.
Here is an explicit F-finite F-pure local counterexample to the unrestricted
reading, with every ideal nonzero proper and containing a nonzerodivisor.

Let `k=F_p`,

`R=(k[x,y,z]/(xy))_(x,y,z)`, `h=x+y`.

Set `I_0=R`, `I_(2a)=(z^a)` for `a>=1`, and
`I_(2a+1)=(h z^(a+1))` for `a>=0`.
The family is multiplicative: even-even and even-odd products are exactly
the required ideal, while

`I_(2a+1) I_(2b+1)=(h^2 z^(a+b+2))⊆(z^(a+b+1))=I_(2(a+b+1))`.

It is not descending: `I_2=(z)` is not contained in `I_1=(hz)`.
Its Rees algebra is generated over R by `hzT` and `zT^2`, hence is Noetherian.
Both `z` and `h` avoid the two minimal primes `(x)` and `(y)` of this reduced
hypersurface. They and their products are nonzerodivisors.

We use the usual splitting definition of the F-pure threshold in this
singular ring. For `q=p^e`, an element `a` splits when there is an R-linear
`phi:F_*^e R→R` with `phi(F_*^e a)=1`.

Every R-linear `phi` sends `F_*^e(xR)` into `(x)`:
`y · F_*^e(xb)=F_*^e(y^q xb)=0`, so
`y phi(F_*^e(xb))=0`, and `ann_R(y)=(x)`. Similarly it sends
`F_*^e(yR)` into `(y)`. Hence every element of `(x,y)` is nonsplitting,
at every Frobenius level. Every positive power of `h z^(a+1)` belongs to
`(x,y)`, so `fpt_R(I_(2a+1))=0`.

For completeness, `fpt_R((z))=1` can be checked without an unproved Fedder
calculation. In the polynomial quotient before localization, take the k-basis
of monomials `x^a y^b z^c` with `a b=0`. For `0<=r<q` define a k-linear map
on Frobenius twists that sends such a monomial to
`x^(a/q) y^(b/q) z^((c-r)/q)` when `q|a`, `q|b`, and `c≡r (mod q)`, and
sends it to zero otherwise. Nonnegative `c` with this congruence has `c>=r`.
The map respects multiplication by q-th powers of `x,y,z` and the relation
`xy=0`, so is R-linear after localization. It sends `F_*^e z^r` to 1.
Taking `r=0` also proves that the ring is F-pure. For `r>=q`, `z^r` belongs
to `m^[q]`, so no R-linear map can send it to a unit.
Thus the splitting crossing exponent for `(z)` is `q-1` and the threshold
is 1. For `(z^a)` it is `floor((q-1)/a)`, and the threshold is `1/a`.

It follows that

`n fpt_R(I_n)=2` when `n` is positive and even,
`n fpt_R(I_n)=0` when `n` is odd.

This is an exact bounded nonconvergent sequence. It does not contradict the
regular-local theorem. It also does not refute an original problem that had
regularity or strong F-regularity implicitly understood: source scope must
be established separately before choosing a global status label.

## 9. Zero ideals and existence versus realizability

Even in `k[x]_(x)`, allowing `I_(2a)=(x)` and `I_(2a+1)=0` produces a
multiplicative family with normalized thresholds growing on even indices
and zero on odd indices, under the convention `fpt(0)=0`. This was already
recorded in the imported prior attempt and is not a new result.

The regular-local existence theorem does not assert rationality of the
limit, attainment of its supremum by one finite index, or realization as
the threshold of one ideal. For example, in `F_p[x]_(x)` let
`I_n=(x^ceil(alpha n))` for any fixed positive irrational real `alpha`.
Ceiling subadditivity makes this a descending multiplicative filtration,
and `n fpt(I_n)=n/ceil(alpha n)→1/alpha`, an irrational number. Every
individual threshold is rational. Taking `I_n=(x)` for every `n>=1` gives
an infinite limit. These examples distinguish existence from arithmetic or
single-ideal realization questions.
