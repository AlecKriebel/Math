# Review 4: independent HWW and all-ideal mathematical audit

Audit checkpoint: 2026-10-07 06:07 UTC (2026-10-06 23:07 America/Los_Angeles).
Delegated downstream mathematical audit completion: 100%. This is not an
estimate of completion of the central upstream EGH proof or publication goal.

## Verdict and scope

**No substantive mathematical gap was found in the downstream theorem,
scope reductions, or all-ideal passage in the reviewed manuscript.** The
required full-length EGH interface agrees with the cited family-200 source
statements. This audit does not certify their central construction: a separate
primary-source EGH reconstruction was assigned elsewhere. The strongest result
independently verified here is the complete, arbitrary-field implication from
that exact EGH interface to the all-ideal Sperner formula, including linear and
degenerate cases.

Reviewed manuscript:
`manuscript/main.tex`, SHA-256
`88bcd2d8c620011eca8732ce30cd77f3322ae993403cf45aff0fb93729f1cf4f`.
Line references below refer to that exact version.

I first read the governing `AGENTS.md`, original `PROJECT_BRIEF.txt`, the
manuscript, and the primary HWW full text, and reconstructed the proof and its
failure modes before reading `notes/downstream_proof.md` and
`DEPENDENCY_LEDGER.md`. I did not read root `README.md`, `THEOREM_STATUS.md`,
`RESEARCH_LOG.md`, existing complete-package reviews, review JSON records,
response records, or prior verdicts. An additional history-free internal
skeptic independently checked filtration and annihilator claims without
reading the manuscript or packaged audits. Its proofs agreed with the
reconstruction below. No external individual was contacted; no source edit,
Git operation, publication action, or tracker operation was performed.

## Primary source and precise interface

The complete seven-page [HWW arXiv v1 PDF](https://arxiv.org/pdf/1601.06928v1)
and [HTML full text](https://arxiv.org/html/1601.06928v1) were read directly.
The PDF retrieved during this audit has 127971 bytes and SHA-256
`b66c69b4c9e901ddb2b9fc6e655a9d4a7c276558638014ee5bb0075fbf453172`.

HWW Definition 2, PDF p. 2, defines the Dilworth maximum over all ideals.
Theorem 11, PDF pp. 4–5, assumes EGH for the fixed graded complete intersection
and concludes its Sperner property. The proof uses ordinary degree-one
polynomial variables. Their field convention, PDF p. 2, is unrestricted.
Proposition 7 gives monomial matching; Proposition 8, PDF p. 4, combines
unimodality and Gorenstein duality and expressly cites Watanabe's graded-ideal
reduction. Sublemma 9 supplies the truncation inequality. Thus the attribution
in manuscript lines 63–73 is accurate. The new note need not infer that an EGH
counterpart preserves generator counts.

The necessary input is exactly: every homogeneous polynomial ideal containing
the fixed full regular sequence has one homogeneous pure-power overideal with
the same entire quotient Hilbert function. It is enough that this hold after
elimination of linear generators. No Betti inequality, lex order, or
partial-length version is needed.

The source clone's HEAD was independently read as
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The pinned local source copies and
read-only upstream originals have identical hashes for the interface files:

| Source interface | Exact lines | SHA-256 of `build/sections/01-introduction.tex` |
|---|---|---|
| `sources/upstream/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026` | 33–56 construction; 65–72 full complex EGH; 92–110 characteristic-zero corollary | `840e99d516c388a3a759fb9a780cb263e8dcf0138a5dbd3ba2c187841fc99acf` |
| `sources/upstream/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026` | 11–32 setup; 41–53 complex theorem; 68–94 characteristic-zero corollary | `dfc850d732642e92630818e23513e84d03659b9ce3c3b85a5ae666af6427288a` |

Both sources allow all additional homogeneous generators, of arbitrary degree
and number; both assume ordered degrees at least two. The companion's
Corollary 1.2 directly supplies the full complex monomial EGH counterpart.
The full-length portion of its Corollary 1.3 agrees with manuscript lines
79–109. Invoking the smaller Hilbert-function consequence prevents an
unnecessary dependency on the stronger Betti transfer.

## Independent reconstruction and falsification attempts

### Algebra and reduction boundaries

For the target quotient, positive-degree relations imply `A_0=k`; the positive
graded ideal is nilpotent and its quotient is `k`, so it is the unique maximal
ideal. Every ideal is a finite module. Therefore
`mu_A(I)=dim_k I-dim_k mI`, including `I=0` and `I=A`. The set of possible
generator counts is a nonempty finite set of integers bounded by `dim_k A`,
so its maximum exists even if the field or set of ideals is infinite.

A full regular sequence of length `n` in `n` polynomial variables has height
`n` and an Artinian quotient. If its `r` linear members were dependent, the
same ideal would have fewer than `n` generators, contradicting the height
theorem. A linear coordinate change identifies their ideal with `r`
variables. The other images are homogeneous of their original degrees and
none can vanish: otherwise fewer than `n-r` equations in `n-r` variables
would have height `n-r`. Their Artinian quotient makes them a homogeneous
system of parameters, hence regular by Cohen–Macaulayness. The graded
isomorphism preserves *all* ideals, `m`, each generator count and every
Hilbert dimension. Eliminated Hilbert factors are exactly one. This checks
manuscript lines 111–123 without changing the target quantifier.

Sorting degrees is legitimate because a permutation of this homogeneous
system of parameters is regular in the polynomial ring. The pure-power
variables can then be relabeled. No assertion about arbitrary permutations
of regular sequences in a general nonlocal ring is needed (lines 87–89).

When `n=0`, or all degrees are one, `A=k`; its ideals are zero and the unit
ideal. Thus the maximum is one, attained by `A=m^0`. The empty product is
one. A one-variable degree-`d` quotient has Hilbert function consisting of
`d` ones, last maximum `p=d-1`, and `m^p` has one generator. These cases also
test the long-plateau choice of `p`, rather than silently replacing `p` with
a middle degree. The statement in lines 45–61 handles them correctly.

### Field scope

Fix a homogeneous overideal `Q`; polynomial rings are Noetherian, so take
finitely many homogeneous generators. The coefficients of these generators
and the regular sequence generate a finitely generated field `k_0` over `Q` inside
`k`. Include the regular sequence explicitly in the ideal generators. The
successive multiplication maps over `k_0` become injective over `k`; faithful
flatness therefore makes them injective already over `k_0`. A finitely
generated characteristic-zero field embeds abstractly into `C` by choosing
algebraically independent images of a finite transcendence basis and then
extending across its finite algebraic extension. Regularity persists under
the extension to `C`.

The complex interface yields a monomial counterpart. Its exponent set
defines an ideal over `k_0` and over `k`; graded dimensions remain unchanged
under either field extension. This proves the exact input over arbitrary
`k`, without assuming that the whole field `k` embeds into `C`. The argument
is per overideal `Q`; it does not require one common finitely generated field
for every ideal. Manuscript lines 97–109 are sound.

The separate generator-bound descent in lines 244–252 is also valid:
`m_K=m tensor_k K`, the extended algebra is still local with residue field
`K`, and flatness identifies the generator quotient with
`(I/mI) tensor_k K`. Only ideals extended from `k` need be compared; every
ideal over `K` need not descend.

### Hilbert series and monomial matching

Successive nonzerodivisor multiplication exact sequences give
`Hilb A=product_i(1+t+...+t^(d_i-1))`. The Koszul resolution gives canonical
module `A(c)`, where `c=sum_i(d_i-1)`, hence one-dimensional socle and perfect
graded multiplication pairings. This checks lines 125–136 independently of
EGH.

The rectangle chains in lines 147–153 are saturated, disjoint, exhaustive,
and symmetric. For a point `(i,j)` in a rectangle with `a<=b`, it lies in
the row portion of chain `i` if `j<=b-i`, and otherwise in the column
portion of chain `b-j`. Multiplying an old symmetric chain starting in rank
`s` and of length `a` by a new factor preserves symmetry, because
`2s+a` is the old total rank. Factors may be exchanged when necessary.

Below the middle, each chain meeting rank `j` reaches rank `j+1`. At or
above the middle, no chain can begin at `j+1`; any ending at `j` would force
a strict rank-size decrease. Therefore `h_j<=h_(j+1)` excludes such an
ending, including plateau degrees. Chain successors inject every rank-`j`
set into its upper shadow.

For an arbitrary subspace of the monomial quotient, echelonized leading
monomials have cardinality equal to its dimension. A surviving variable
multiple of a leading monomial remains the leading term of the product:
multiplicativity keeps every other surviving term smaller. The possible
death of other terms does not change this conclusion. The upper shadow is
therefore contained in the leading set of the product subspace. This proves
monomial matching in lines 162–171 over any field without a Lefschetz map.

For `V subset A_j`, standard grading gives `(AV)_j=V` and
`(AV)_(j+1)=A_1 V`. The EGH counterpart ideal `J` in the pure-power quotient
has these two dimensions because the ambient algebras and the quotient
Hilbert functions agree. Its ideal property gives
`dim V=dim J_j <= dim B_1 J_j <= dim J_(j+1)=dim A_1 V`.
Extra generators in degree `j+1` only support the second inequality; there
is no assumed equality of generator counts. `V=0` is harmless and expressly
handled. This verifies lines 173–186.

### Truncation and Gorenstein bound

For a homogeneous ideal, standard grading gives `(mI)_j=A_1 I_(j-1)`.
Removing its initial degree `alpha<p` loses `dim I_alpha` generator classes
and gains `dim A_1 I_alpha` at the next degree; other pieces agree.
Matching makes the difference nonnegative. Iteration gives
`mu(I)<=mu(I intersect m^p)` (lines 188–199).

Let now `I subset m^p` be homogeneous and `H=Ann(mI)`. With the perfect
total pairing obtained by projecting multiplication to `A_c`, the
orthogonal complement of an ideal `U` is exactly `Ann(U)`: orthogonality
to every multiple of each element of `U` and nondegeneracy force actual
annihilation. Hence `dim Ann(U)=dim A-dim U`. Since
`mH subset Ann(I)`, this yields `mu(H)>=mu(I)`.

For `0<=u<=c+1`, degree considerations give
`m^(c-u+1) subset Ann(m^u)`. If an element has lowest nonzero degree
`e<=c-u`, perfect pairing supplies a multiplier in degree `c-e>=u` with
nonzero product; all higher components vanish in that product. This proves
the reverse inclusion even for a nonhomogeneous element. The endpoints
are `Ann(A)=0=m^(c+1)` and `Ann(0)=A=m^0`.

Symmetry and unimodality make the last maximal degree satisfy `c-p<=p`.
Thus `H` contains `Ann(m^(p+1))=m^(c-p)`, which contains `m^p`. Its
truncation at `p` is exactly `m^p`. Applying the prior inequality to `H`
gives `mu(I)<=mu(H)<=mu(m^p)=h_p`. Annihilators of homogeneous ideals are
homogeneous, so this use of truncation is legitimate. This independently
checks all inclusions and inequality directions in lines 201–222 and
avoids needing the auxiliary Dilworth lattice theorem.

### Arbitrary ideals: decisive filtration check

Use `F^j A=m^j=A_(>=j)`, with the **intersection** filtrations on both
`I` and `mI`. Standard grading identifies `gr_m A` with `A`. The associated
graded of `I` embeds as the homogeneous ideal `J` of lowest-degree initial
parts. For a homogeneous positive-degree element `a` and a representative
`f in I intersect m^j`, the product class is represented by `af in mI`.
If the expected initial product vanishes, its class is zero and creates
no problem. Thus `mJ subset gr_F(mI)` as subspaces of the same graded
algebra. Finite associated grading preserves total vector-space dimension,
and consequently

`mu(I)=dim J-dim gr_F(mI) <= dim J-dim mJ=mu(J)<=h_p`.

This verifies lines 225–240 with the correct direction. Using the intrinsic
filtration of the module `mI` instead would not justify this exact proof.
The manuscript specifies the required filtration.

A strict-inclusion stress case, independently checked by the additional
skeptic and by this reviewer, is
`A=k[x,y]/(x^2,y^5)`, `I=(x+y^2)`. A filtered vector-space basis is
`x+y^2, xy+y^3, xy^2, y^4, xy^3, xy^4`; hence
`J=(x,y^4)`, `mu(I)=1`, and `mu(J)=2`. The identity
`y^4=y^2(x+y^2)-x(x+y^2)` places `y^4` in `mI`, while
`mJ=span{xy,xy^2,xy^3,xy^4}` excludes it. Thus
`mJ` can be strictly smaller than `gr_F(mI)`, precisely in the useful
direction. The manuscript explicitly avoids the false equality.

Finally `m^p/m^(p+1)=A_p` proves the equality witness in lines 58–60 and
241–242. The unit ideal covers `p=0` and `A=k`.

## Computation, interpretation and documentation observation

Independent enumeration of bounded exponent vectors reproduced every
coefficient list and maximum in lines 260–265, including the empty product.
For degrees `(1,2,4)`, the last maximum is degree 3; for `(2,2,2)`, it is
degree 2; these plateau cases exercise the theorem's actual convention.
For eight quadrics the verified list is
`1,8,28,56,70,56,28,8,1`, with last maximum degree 4. The all-quadric
binomial formula follows from `(1+t)^n`. These computations illustrate the
theorem and do not validate the central EGH proof, as the manuscript states.

Lines 274–279 correctly restrict the promoted assertion to standard graded
Artinian characteristic-zero complete intersections. The downstream proof
works under its EGH premise in any characteristic; it does not establish
general positive-characteristic EGH, weak or strong Lefschetz, or a
nongraded complete-intersection theorem. The inherited nature of the
implication and the dependence on an external unrefereed EGH result are
explicit. No mathematical scope repair is required within this audit.

One lower-severity documentation observation for the complete-package
reviewer: `notes/downstream_proof.md:59–61` calls the HWW PDF project-local
at `sources/priority/HWW_arxiv1601.06928v1.pdf`, but this file was absent
during the fresh audit. The live primary PDF has exactly the stated hash,
so the source text was fully reproducible and this is not a mathematical
obstruction. If removal was intentional for redistribution reasons, change
the local-copy wording to a retrieval record or explain the exclusion.

The exact remaining dependency outside this audit is the validity of the
companion's complex, full-length EGH construction. A material gap there
would block the unconditional headline, despite the sound downstream
argument. This review is evidence for the entire implication and scope;
it is not a substitute for that independently assigned upstream audit.
