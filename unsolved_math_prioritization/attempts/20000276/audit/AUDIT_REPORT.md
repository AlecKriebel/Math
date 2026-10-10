# Independent audit of the graded family F pure threshold result

Problem 20000276 / AIM-ALGEBRAIC_GEOMETRY-0276. Audit date: 2026-10-05 UTC.

## Verdict and exact scope

**PASS for the explicit mathematical claims in the frozen candidate.** No
fatal proof gap was found. This is an independent machine-assisted mathematical
audit, not human peer review or certification of historical novelty.

The accepted theorem is:

Let `(R,m)` be an F-finite Noetherian regular local ring of characteristic
`p>0`. Let every `I_n`, `n>=1`, be nonzero and proper, and assume
`I_a I_b ⊆ I_(a+b)` for all positive `a,b`. Then

`lim_n n fpt_R(I_n) = sup_n n fpt_R(I_n)`

in the extended positive reals. Descendingness and a Noetherian Rees algebra
are unnecessary. The fixed-factor lemma and the singular counterexample
also pass, with their stated hypotheses and definitions.

**The original AIM target is not certified resolved.** Its full primary
context was not recovered: the primary problem page again returned HTTP 502.
The public imported statement and complete imported prior report were read
independently; they do not supply the missing original ring conventions.
The affirmative theorem and negative singular example answer different precise
interpretations. Neither can silently choose the original interpretation.
An unqualified `verified_solved` disposition remains unsupported.

The first obstruction to that broader disposition is source-scope verification,
not a failed step of the regular-local proof. Global thresholds, singular
strongly F-regular rings, non-F-finite rings, and definitions allowing zero
terms have not been settled by this packet. Finite real convergence also
must not be claimed: the constant family `(x)` in `F_p[x]_(x)` has infinite
normalized limit.

## Frozen input and audit method

The input ZIP has 18,061 bytes and SHA-256
`0f9cd51c761719c5e4458a314df1a43f7032a6c05270383b9529fd230aea6db5`.
The author manifest has SHA-256
`af41972b5888f937ac69d53a823207f4736064edb6c289eaf1e002fa1acb8b4f`.
Every ZIP member agrees byte-for-byte with the corresponding frozen file,
and all eight manifest entries verify. The frozen input was not modified.

The audit read the complete proof, report, source metadata, research log,
README, verifier, and manifest. It reconstructed the argument without using
the finite tests as proof; attacked Frobenius module conventions, the
quantifier order, every residue class, infinite suprema, and singular
threshold definitions; and independently compared the source corpus and
relevant primary literature. No remote writes or external communications
were performed by this audit.

The author's 282,118 exact finite assertions replay successfully. A separately
written verifier, with no import from the author's code, passes 52,161 exact
assertions. Its principal new control constructs the unit-coordinate inverse
and resulting Frobenius projection explicitly in truncated polynomial rings.
The other main independent control uses the hypersurface Fedder colon rather
than the author's enumeration of Cartier maps. Neither finite count proves
an arbitrary-ring or unbounded-index theorem.

## The regular local argument

### Frobenius freeness and separation

Kunz flatness together with F-finiteness makes `F_*^f R` a finite flat module,
hence free over the local ring. This conclusion does not require a perfect
residue field or a chosen coefficient field. The relevant two equalities are

`m F_*^f R = F_*^f(m^[Q])`,

`m^[q] F_*^f R = F_*^f(m^[qQ])`.

They use the scalar action `a F_*^f b = F_*^f(a^Q b)`, with `Q=p^f`.
These are module equalities, not informal identifications of ordinary
products with Frobenius products.

If `v` avoids `m^[Q]`, its coordinate vector in a free basis is not in the
maximal ideal multiple of the module. At least one coordinate is a unit.
Coordinate projection followed by multiplication by the inverse unit gives
an R-linear map sending `F_*^f v` to 1. Applying it to an assumed membership
`u^Q v in m^[qQ]` forces `u in m^[q]`, a contradiction. Thus the separation
lemma is correct. The map can depend on `Q` and `v`; the proof never needs
one map valid at every level.

The hypothesis of regularity is substantive. In the node ring, with
`q=Q=2`, the elements `u=y` and `v=x` each avoid `m^[2]`, but `u^Q v=0`.
Also, even in a regular ring, an ordinary same-level product need not
preserve noncontainment: `x` avoids `(x^2)`, while `x*x` does not.

### Ordinary thresholds and positivity

The maximum defining `nu_J(q)` exists because `J` is proper, so `J⊆m`,
and a regular system of `d` parameters gives
`m^(d(q-1)+1)⊆m^[q]`. Faithful flatness gives
`nu_J(pq)>=p nu_J(q)`. Hence the normalized exponents increase to a finite
limit at most `d`.

For nonzero `f in J`, Krull intersection and `m^[q]⊆m^q` give a Frobenius
power with `f` outside `m^[q]`. Thus the limit is positive. There is no
dimension-zero exception to handle: a regular local ring of dimension zero
has no nonzero proper ideals and the theorem's premise is empty there.

Because powers of an ideal are nested, the formula
`nu_(J^s)(q)=floor(nu_J(q)/s)` is exact, including when the right side is
zero. Inclusion monotonicity has the correct direction. In the regular-local
ring, the same free-module argument identifies splitting elements with
elements outside `m^[q]`. The usual pair definition with exponents
`floor(t(q-1))` has the same threshold as the limit with denominator `q`:
for `t` strictly below or above the limit, the defining inequalities hold
or fail eventually. No endpoint assertion is required for this equality.

### The fixed factor and its limits

Fix `q`, a positive integer `a` with `I^a` not contained in `m^[q]`,
an element `u` witnessing that fact, and a nonzero `f in J`. Positivity gives
`delta=fpt((f))>0`. For a fixed integer `k>a/delta`, choose
`h_Q=floor(aQ/k)`. Since `a/k<delta`, eventually
`h_Q<=nu_(f)(Q)`. Therefore `f^h_Q` avoids `m^[Q]`, and separation yields
a witness at level `qQ`.

The necessary ideal containment is in the correct direction:

`u^Q f^h_Q in I^(aQ) J^h_Q ⊆ I^(k h_Q) J^h_Q`.

The last ideal is `(I^k J)^h_Q`. Possible early values `h_Q=0` cause no
problem; the limit uses arbitrarily large `Q`. For fixed `q` and `k`, the
values `qQ` form a cofinal tail of the Frobenius powers and
`h_Q/(qQ)` tends to `a/(kq)`.

For any accuracy `epsilon>0`, first select a single sufficiently large `q`
and `a=nu_I(q)` approximating `fpt(I)`. Then all sufficiently large integers
`k` satisfy the strict condition above. The inner `Q` limit is taken for
each such fixed `k`. This gives a bound for every sufficiently large `k`,
not merely a specially chosen subsequence. Together with
`I^k J⊆I^k`, it proves `k fpt(I^k J) -> fpt(I)`.

The proof does not exchange `q` and `Q` limits or presume a uniform bound
as `q` varies. The strict margin matters for this witness construction:
for a linear `f` and `k=a`, one obtains `h_Q=Q`, which no longer avoids
`m^[Q]`. The case `J=R` is handled separately by power scaling, as stated.

### Residues and extended limits

For a fixed positive `r`, multiplication gives
`I_r^k I_s⊆I_(kr+s)` in every nonzero residue `s<r`. Applying the fixed-factor
lemma separately in each of the finitely many residue classes gives the
lower asymptotic bound `r fpt(I_r)`. The zero residue uses the power formula.
The finitely many necessary starting indices have a maximum; thus this is
a bound for the full sequence. No uniform control over infinitely many
residues is being assumed.

Taking the supremum over `r` proves the desired equality. If that supremum
is infinite, for any finite bound `B` one first chooses a single `r` with
`r fpt(I_r)>B`; the finite-residue argument then puts the entire tail above
`B`. This proves divergence to positive infinity, not just unboundedness.

## Auxiliary statements

- The descending-family ceiling squeeze is valid and only uses threshold
  monotonicity and power scaling. It also works with zero threshold values
  when the invariant has those properties.
- A standard Veronese gives the asserted finite value through the accepted
  theorem and its exact-power subsequence. The finite-generation statement
  is the usual existence of a standard Veronese for a finitely generated
  positively graded algebra; no particular least-common-multiple bound is
  asserted or needed.
- The crossing-index identity handles zero crossings, gaps, unbounded
  crossing sets, and infinite suprema correctly. Its all-family construction
  is mathematically valid. For citation precision, the Koley–Kumar attribution
  should explicitly be restricted to descending filtrations with finite
  limit, which is their definition of the named invariant. At infinity the
  equality is with their common extended upper and lower limits. For a
  non-descending graded family it is an extension of that crossing
  construction. This is a nonblocking clarification, not a failed equality.
- The irrational ceiling example is multiplicative since ceiling exponents
  are subadditive. Its normalized limit is irrational even though every
  individual one-variable threshold is rational. The constant-ideal and
  zero-term examples have the claimed extended and oscillatory behavior.

## Singular counterexample checked independently

Let `S=F_p[x,y,z]_(x,y,z)` and `R=S/(xy)`. The candidate uses
`h=x+y`, `I_(2a)=(z^a)` and `I_(2a+1)=(h z^(a+1))`. Even-even and even-odd
products have the required degree; odd-odd products gain enough powers of
`z`. The Rees algebra is exactly generated by `hzT` and `zT^2`: these
generate each displayed ideal, and any other monomial in these generators
lies in the same displayed ideal. This is a finitely generated example.

The ring is reduced with minimal primes `(x)` and `(y)`. Both `h` and `z`
avoid them, so each ideal is nonzero, proper, and contains a nonzerodivisor.
It is genuinely non-descending. In particular `z` is not in `(hz)`, since
cancellation of the nonzerodivisor `z` would make the nonunit `h` a unit.

An independent Fedder calculation gives

`((xy)^[q]:(xy)) = ((xy)^(q-1))` in `S`,

`(x^q,y^q,z^q):(xy)^(q-1) = (x,y,z^q)`.

Consequently the level-e splitting ideal of `R` is exactly `(x,y,z^q)`.
In particular `R` is F-pure, `(z^a)^t` contains a splitting element exactly
when `a t<q`, and no positive power of `h z^(a+1)` contains one.
This uses the hypersurface Fedder criterion for pairs, not the false
identification of the splitting ideal with `m^[q]` in a singular ring.

The candidate's direct argument reaches the same conclusion. Every R-linear
Cartier map preserves `(x)` because its source elements are annihilated by
`y`; the annihilator of `y` is `(x)`. The corresponding statement holds for
`(y)`. Thus all such maps preserve `(x,y)`. The proposed monomial maps have
the correct scalar action: multiplication by each `q`th power of `x,y,z`
commutes with the map, including products killed by `xy=0`. Linearity over
`F_p` suffices for coefficients. Localization of these maps is legitimate
under `(F_*^e A)_m ≅ F_*^e(A_m)`.

There is also a direct check from the pair definition, avoiding reliance on
an unstated singular-limit theorem. For the ideal `(z^a)`, every `t<=1/a`
has `a floor(t(q-1))<=q-1`; its required element splits. For `t>1/a`, the
reverse obstruction holds for all sufficiently large `q`. For the odd ideal,
every positive real `t` eventually demands a positive power in `(x,y)`,
and hence fails. The zero exponent splits since the ring is F-pure. The
thresholds are therefore exactly `1/a` and `0` in the usual F-pure-pair
convention. A convention using sharp F-purity gives the same suprema.

Thus the normalized thresholds are exactly 2 on positive even indices and
0 on odd indices, at every characteristic `p`. This is a valid counterexample
to unrestricted F-finite F-pure local rings, including when every term
contains a nonzerodivisor. It cannot refute the regular-local theorem or
silently settle a source that implicitly required strong F-regularity.

## Source and historical checks

The primary foundations were checked against
[Blickle–Mustaţă–Smith](https://arxiv.org/abs/math/0607660v2), especially
the regular F-finite Frobenius-module setup. For singular definitions,
[De Stefani–Núñez-Betancourt](https://doi.org/10.1017/nmj.2016.65) was
checked at Definitions 3.2–3.5, and an additional independent check used
[Takagi–Watanabe](https://arxiv.org/abs/math/0312486), Definitions 1.3 and
2.1 and Lemma 1.8. The latter supports the pair-definition and Fedder
calculations above. These checks establish convention compatibility; none
is being cited as already proving the candidate theorem.

[Koley–Kumar v1](https://arxiv.org/abs/2312.07761v1) was inspected at the
filtration definition, crossing invariant, and Theorem 3.15. Its descending
filtration scope differs from the candidate's arbitrary graded-family scope.
The [2026 publication](https://doi.org/10.1016/j.jalgebra.2026.01.012) has
a verified publisher listing; its final full text was not audited here.
The [2026 differential-power preprint](https://arxiv.org/abs/2607.09028v1)
concerns a distinct crossing-index invariant. A further bounded search found
[Baily's manuscript](https://bbaily.github.io/classificationJune.pdf), whose
Definition 3.9 uses a liminf asymptotic singularity threshold; the inspected
material supplies no matching arbitrary-family convergence theorem.

The complete imported prior report was checked. It already contains the
divisibility/limsup and crossing identities, the Noetherian descending
Veronese result, and the monomial argument. The candidate correctly treats
those as prior work. Its fixed-factor step goes beyond that report's proved
claims, while its descending squeeze closes a gap the report left open.

These are bounded literature checks. Failure to locate an earlier identical
statement is not evidence of novelty. No comprehensive bibliographic database
review or expert historical confirmation was performed.

## Recommended disposition

Accept the frozen packet as a proved result under the expressly stated
regular-local assumptions, together with the proved singular boundary
example. Retain the original-target scope gate. If publishing a summary,
state both the F-finite regular-local/nonzero-proper hypotheses and the
extended-limit convention in the summary itself. Use a separate, clearly
qualified description for the singular example. The Koley–Kumar wording
clarification above can be added in an acceptance note without altering
the audited freeze.
