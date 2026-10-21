# PR #1150: independent differential-symbol and coefficient review

**Verdict: main counterexample passes this review family; one ancillary exponent-one shortcut required repair. The exact replacement in `../../REVIEWED_PROOF.md` was checked and resolves this issue.** This is a mathematical review, not a priority decision or a complete publication-package approval.

## Inputs and independence

I read the complete immutable `../../inputs/COUNTEREXAMPLE.md`: 12,061 bytes, SHA256 `b1533a032e031d82a0d124cdb410e86e5ee59af477dd711d2157a5d72f36e2ca`. I did not read the historical audit, acceptance material, source-audit conclusions, root or sibling review conclusions, or another shard. The task briefing identified the desired symbol calculation and two counterfactual variants; it did not supply an independently established verdict. Thus this is an adversarial check of a known candidate, not a blind rediscovery of its construction.

I independently obtained primary bodies for the definition of the differential operator, the differential-symbol/Brauer identification, and the characteristic-two norm criterion. I derived the fixed-basis exact-differential correction, checked the rational-field coefficient obstruction, and discovered the ancillary exponent-one gap before the parent supplied any correction. I notified the parent. The parent then agreed and supplied a revised proof; only after my core findings did I inspect its exact diff. That post-core exposure is disclosed below and was not used as evidence for the main counterexample.

The initial local diagnostics also used the letter beta on both sides of the exponent-one comparison, which obscured the base/extension distinction. Before sealing any outputs I replaced that diagnostic by an explicit base `u` differentiation check and a separately labelled extension-level certificate. No initial draft output is being represented as an independent proof of a base identity.

## Primary bodies actually inspected

1. Aravire–Laghribi–O'Ryan, *Cohomological kernels of mixed extensions in characteristic 2*, author manuscript dated **15 August 2019**, [author PDF](https://laghribi.perso.math.cnrs.fr/cohom-kernels.pdf): abstract/introduction and the definition and conventions in §2.1, printed pp.1–6, with selected following material in §2.2 on pp.6–7. In particular I read the coefficientwise definition with respect to a 2-basis and its dependence on the basis only modulo exact forms. I visually inspected PDF p.6. I did not read its entire later proof or infer the candidate from Theorem 1.4.
2. Chapman–Quéguiner-Mathieu, *Minimal quadratic forms for the function field of a conic in characteristic 2*, [arXiv PDF](https://arxiv.org/pdf/2111.15251), retrieved version **v3, 13 December 2022**: pp.1–3, in particular the cyclic algebra convention on p.2 and the differential-symbol/Brauer isomorphism and additivity identities on p.3. I visually inspected p.3. I also saw the beginning of p.4 in the extraction but did not use its later theorem. This is not an inspection of the 2024 final publication.
3. Voight, *Quaternion Algebras*, 2021 official open-access [Chapter 6](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_6): selected definitions in §§6.1–6.2 from the publisher HTML and Theorem 6.4.11 on **printed p.92/PDF p.8**, including equivalence with the quadratic norm criterion, from the downloaded chapter. I visually inspected that page and read adjacent context. I did not inspect the whole book. The initially guessed author-hosted book URL returned 404; the official chapter PDF succeeded.

The original Oberwolfach question and its precise permitted data were not independently fetched by this family; original-target/source verification belongs to the parent's separate family. All source PDFs, extracts and rendered pages are confined to ignored `sources/private/`; public records retain URLs, versions and hashes only. No external individual was contacted. `SOURCE_RETRIEVAL.json` records actual retrievals, including the failed URL.

## Independent reconstruction of the differential identity

Work in `L=F₂(beta,z,s,t)`, with `beta⁴=b`, and later in `M=F₂(beta,z,s,gamma)` with `gamma²=t`. Set

\[
x=\beta^2z,\qquad f=1+x,\qquad h=x/(1+x).
\]

The variables beta, z, s and gamma constitute a 2-basis of M. In absolute characteristic-two differentials, `d(beta²)=0`, whereas `d beta` and `dz` are nonzero. Therefore

\[
d\log f=h\,d\log z,\qquad
h^2=\frac{\beta^4z^2}{1+\beta^4z^2}.
\]

Let `a=s⁻² h dlog z`, `c=s⁻¹ h dlog z`, and let `W` denote coefficientwise Artin–Schreier in this fixed logarithmic 2-basis. Then the following are actual identities of differential representatives:

\[
\xi_M+a=W(a),
\]

\[
(s^{-2}+s^{-1})d\log f+W(c)=d(s^{-2}h),
\]

and consequently

\[
\boxed{\xi_M+s^{-1}d\log f
 = W(a)+W(c)+d(s^{-2}h).}
\]

For the second identity, `dh=beta²/(1+beta² z)² dz`, and `h²+h=x/(1+x)²`. Also `d(s⁻²)=0`. These formulas give exactly the required correction.

This matters because the coefficientwise square operator is not an F-linear map on arbitrary presentations in Ω¹. The correction is generally nonzero before quotienting by exact differentials. After quotienting it vanishes, so the candidate's conclusion

\[
\xi_L=[s^{-1},1+\beta^2z)_L
\]

is correct. No extra powers of s or beta are missing. In `LK`, `s⁻¹=theta²+theta`, so this symbol is zero. The extra square root of the independent slot t does not kill `dz`, while adjoining `sqrt(z)` does. Thus the Pfister-slot counterfactual in the candidate is valid.

The primary Brauer identification sends precisely `u dlog v` to the cyclic algebra with `i²+i=u`, `j²=v`, `ji=(i+1)j`; it has no reciprocal or slot reversal in this convention. Multiplying second slots is valid. The relative cyclic-kernel description applies to the genuine separable quadratic field extension without a perfection assumption.

For clarity, the norm criterion also follows directly in this setting. If a quaternion algebra `(D/E,c)` is split, its two-dimensional simple E-module becomes a one-dimensional D-module. Its generator j acts as an invertible sigma-semilinear map `x ↦ a sigma(x)`, so `j²=N(a)=c`. Conversely a solution `N(a)=c` gives that semilinear split representation. This checks the norm use without assuming a perfect field or confusing a purely inseparable extension with D/E.

## Square-class coefficient obstruction

Put `a=beta²` temporarily, to keep the two purely inseparable levels visible. Then

\[
S=F_2(a,z^2,\gamma^2),\quad
R=F_2(a^2,z^2,\gamma^2),\quad
k=R(z),\quad [k:R]=2.
\]

The rational independence of a, z and gamma gives `z notin S` and `a notin R`. This is a statement about rational function fields, not about finite-field specializations. For example, the derivation with respect to a annihilates R but sends a to 1. Similarly the derivation with respect to z annihilates S but sends z to 1.

Every residue `c₀ in k*` has a unique expansion `u+vz` with u,v in R. If `(1+az)/c₀` were in S, coefficient comparison in the S-linearly independent pair 1,z would imply `qu=1` and `qv=a`. Thus u is nonzero and `a=v/u in R`, a contradiction. The zero cases u=0 or v=0 are not loopholes: the first contradicts `qu=1`, and the second contradicts `qv=a`.

Equivalently, differentiating the quotient in z gives

\[
\frac{\partial}{\partial z}\frac{1+az}{u+vz}
 =\frac{au+v}{(u+vz)^2}\ne0.
\]

This gives an independent formulation of the coefficient obstruction: the denominator is nonzero and `au+v` cannot vanish for nonzero `(u,v)` in R². It excludes every residue c₀, including rational rather than polynomial coefficients. It also confirms that replacing the independent t-slot by z destroys this particular obstruction, as the target form's `dz` is killed.

I checked the restriction step `xi=x+y+w` to M: the L-kernel and the F(B)-kernel both vanish there, leaving a single cyclic symbol with a base-field second slot. Division by c rather than multiplication by c is harmless because the Brauer classes have exponent two. The normalizations `N(pi)=s`, unit norm residues are squares, and Laurent leading coefficient `c₀ in k*` are consistent. This family does not independently replace the complete-valued-field proof assigned to the other family.

## Required repair and its verification

The original §6 first bullet says that if `b=u²` already in the base field then the same calculation gives **in the base** `xi=[s⁻¹,1+uz)`. The supporting differential shortcut drops the extra term in

\[
d(1+uz)=u\,dz+z\,du.
\]

The fact that u becomes a square in L does not make `du=0` in the base. I therefore flagged the justification as invalid. My diagnostic proves the proposed base differential identity fails; it is **not a cohomology decision procedure and I do not claim it alone proves the full base symbol classes unequal**.

The minimal sufficient correction is:

> If `b=u²` is in the base and `beta²=u`, then L/F has exponent at most one. Over L, `du=0`, so the original calculation gives `xi_L=[s⁻¹,1+uz)_L`. Since `f=1+uz` is in the base, `xi-[s⁻¹,f)` belongs to the L-kernel and `[s⁻¹,f)` belongs to the K-kernel. Thus xi lies in their sum.

After this finding the parent supplied `../../REVIEWED_PROOF.md`, **12,322 bytes, SHA256 `7f63c1f6e4f79a78b979903db59e8030a8222266a65d296a4a6fc1a29a6e2e1b`**. I read the exact complete diff against the pinned original. Its only change is this first §6 bullet. It implements the preceding repair, expressly mentions the base `z du` term, and does not make the unsupported single-symbol claim. **The repair is adequate.** Immutable original input bytes were not modified by this family. No issue in the main exponent-two counterexample needed repair.

## Exact diagnostics and actual failing alternatives

`verify_symbols.py` is dependency-free. It implements GF(2) multivariate polynomials as parity sets of monomials, rational arithmetic by cross multiplication, the quotient derivative, standard-coordinate one-forms, and Artin–Schreier in a fixed logarithmic basis. It contains no Python `assert`, so `-O` does not suppress checks.

Each positive mode checks 13 displayed symbolic identities/inequalities; 1,023 bounded pairs of R-polynomial coefficients; 143 actual quotient derivatives; 24 additional pairs with genuinely rational R-coefficients; two derivation tests distinguishing the nested fields; and 49 exact quadratic-algebra norm formulas, including `Norm(pi)=s`. These are algebra diagnostics and exact certificates of the displayed rational identities, **not finite evidence substituting for the universal field, cohomology, norm-residue or coefficient argument**.

`run_checks.py` starts real processes in normal and optimized Python modes. The positive outputs are byte-identical: **1,313 bytes, SHA256 `2c15e49d6e392649b56c1044e8dc914fa60f8c0584f22d319b79ead6cdb0845a`**. It separately runs nine deliberately wrong representative/algebra assertions in both modes, yielding **18 actual nonzero process exits** with the expected check failure: differentiating a square incorrectly, the wrong beta Frobenius power, wrong s power, omitting the exact correction, killing dz with the independent gamma, putting a in R, swapping the quotient numerator, preserving dz after adjoining sqrt(z), and dropping the base du term in the exponent-one check. These are wrong-result controls, not arbitrary algorithm-mutation coverage or a proof of full class inequality for each variation.

The script's limited arithmetic machinery is inspectable and only removes common monomial factors; it does not depend on computer algebra simplification. `EXECUTION_RECEIPT.json` records actual exit codes and diagnostic hashes. The reproduction command is `python3 run_checks.py` from this folder; this intentionally rewrites its execution timestamp/output files. `RECEIPT.json` authenticates the sealed files and the private primary bodies read during this review. Do not mistake a rerun timestamp change for a change in mathematical output.

## Remaining limits and disposition

Within this family's assigned scope, the main universal construction and differential/coefficient mechanism pass. The one ancillary proof shortcut is repaired in the specified reviewed proof. I found no further repair necessary after checking that exact diff. The original-target statement and priority classification still require the parent's other reviews. I did not certify historical acceptance, publication readiness, global novelty, or completeness of the literature. The standard Kato/Brauer theorem and cyclic Brauer-group theorem are used as established results, not formally reproved from foundations here.
