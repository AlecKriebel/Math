# Independent adversarial audit of the optional global supplement

Audit completed 2026-10-01T05:22:16Z. Completion estimate: **100% of this scoped audit**. This estimate concerns verification of the supplemental argument, not discovery of a new theorem.

## Verdict and scope

**PASS: the proposition and Steps 1–5 are correct under their stated hypotheses. No mathematical repair is required.** In particular, Classical input A is a genuine global theorem; it is not an invalid extrapolation from local Horrocks or from an extended-projective conclusion.

The audited claim is: for a proper ideal of positive finite colength in `C[x_1,...,x_d]`, if `r=mu_{R/I}(I/I^2)>=2`, then `mu_R(I)=r`. The proof constructs new representatives, so it does not promise that any prescribed conormal generating list lifts without modification. The `d=1` case is separately principal; `d=0` does not produce an instance with `r>=2`. The lower-bound argument `r>=d` is an external input to the final application, not needed for the proposition conditional on `r>=2`.

This verdict concerns only `homology_global_family/SPECIALIZED_GLOBAL_PROOF.md`, SHA256 `81eeb556c83e0111f658593707efff1c9760da089d52776ce9eb7d9a2764b959`. It does not reopen or alter the canonical candidate, whose accepted global bridge is the directly inspected original Mohan Kumar theorem.

## Primary-source check of the freeness inputs

I independently downloaded [Quillen, *Projective modules over polynomial rings* (1976), original GDZ scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0036/LOG_0016.pdf) and visually inspected printed pp.167–171. Theorem 3 on p.169 states that a finitely generated projective `A[T]`-module free after inverting all monic polynomials is free. The paper's p.167 convention allows arbitrary commutative rings with identity. Hence freeness after one monic denominator also suffices, with no local-base restriction. Theorem 2 gives extension from the base; Theorem 3 additionally compares a finite fiber with the trivial fiber at infinity to obtain freeness. Theorem 4, also p.169, supplies polynomial-ring freeness over a field (and, more generally, a PID).

I separately inspected [Mohan Kumar, *On Two Conjectures About Polynomial Rings* (1978), original printed pp.234–235](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0046/LOG_0020.pdf). Its p.235 uses Quillen Theorem 3 for the monic-entry kernel on the overlap and Theorem 4 for the final projective module. This agrees with the supplement's attribution. Download hashes and inspected pages are recorded in `source_manifest.json`; source PDFs and renders remain in ignored scratch directories.

## Step-by-step adversarial reconstruction

**Step 1: PASS.** Let `N=dim_C(R/I)>0`. Multiplication by `X` on the regular quotient algebra has characteristic polynomial `h` of positive degree `N`; applying Cayley–Hamilton to the unit proves `h(X) in I`. Because `h` is monic, the strict degree inequality makes `a_1+h^m` monic without cancellation. Since `m>=2`, the modification is in `I^2`. The injection `B/J -> R/I` proves finite dimension over `C`; quotienting `(B/J)[X]` by a positive-degree monic polynomial is finite free over `B/J`. Thus the candidate set of bad maximal ideals is finite, including when the quotients are nonreduced. A zero first representative causes no obstruction: choose a sufficiently large exponent and regard its degree as negative infinity.

**Step 2: PASS.** For a bad maximal ideal `p`, some `u in I` is outside `p`, so `u^2 in I^2` is also outside `p`; consequently `I^2+p=R`. Distinct maximal ideals are pairwise comaximal. The CRT map from `R` onto their product of residue fields is surjective, and the image of `I^2` is an ideal of that product. Every projection is the entire field, so the ideal is the entire product (multiply by the coordinate idempotents). Thus the simultaneous prescribed values are attained by one `b in I^2`. At every bad point the modified second generator has residue 1. The empty bad set permits `b=0`. The use of a second generator is the exact place where `r>=2` enters.

**Step 3: PASS.** The set `S=1+J` is multiplicative and avoids zero. Here is a direct Jacobson-radical proof: if a maximal ideal of `S^{-1}B` avoids some `j in J`, write the inverse of its residue as `b/u`. Then `u-bj` vanishes in the residue field and belongs to `1+J`, contradicting that all elements of `S` are units. Monicity makes `S^{-1}R/(f_1)` finite integral over `S^{-1}B`. A maximal ideal of the target contracts to a maximal ideal of the base, and hence contains the image of `J`.

A maximal ideal `q` of `S^{-1}R` containing `F` contains `f_1`; its image in the finite integral quotient therefore contains `J`. Its contraction to `R` contains `JR+(f_1)` and is maximal because that quotient is Artinian. Step 2 then places `I` in that contraction. At this maximal ideal, `I=F+I^2` gives `(I/F)_q=I_q(I/F)_q`; local Nakayama applies because `I_q` is contained in the maximal ideal. Away from `F`, both ideals localize to the unit ideal. Equality at all maximal ideals implies `S^{-1}I=S^{-1}F`. Finite generation of `I/F` allows a product of finitely many denominators from `S` to annihilate the whole quotient. This gives `g=1+s` with `s in J`, genuinely in `B`. If `s=0`, the quotient already vanishes globally.

**Step 4: PASS.** Since `s in I`, localization at `s` turns `I` into the unit ideal. The cover is valid because `g-s=1`. On the overlap, `F_g=I_g` and `I_s=R_s` make the row unimodular. Because `g,s in B`, the overlap is exactly `B_{gs}[X]`; the monic leading coefficient remains 1. The split kernel is a finitely generated projective module of rank `r-1`. After inverting `f_1`, an explicit basis is `e_i-(f_i/f_1)e_1` for `i>=2`. Quillen Theorem 3 therefore makes this kernel free on the overlap. A column `t` with `f t=1`, followed by a kernel basis, forms an invertible matrix `U` with `fU=(1,0,...,0)`.

For complete gluing precision, use the transition from the `s`-chart to the `g`-chart and define pairs by `v_g=U v_s`. Then `q_g(v_g)=q_g(Uv_s)=q_s(v_s)` on the overlap. Descent for quasi-coherent sheaves on the principal cover gives a finite locally free rank-`r` source module `P`. The two maps land in the restrictions of the same ideal sheaf, so they glue; their local surjectivity makes the glued map surjective. There is no assertion that `I`, or the kernel of `P -> I` near the support, is locally free. The use of a free source is precisely what avoids that false inference.

**Step 5: PASS.** Quillen–Suslin applies to the finite projective `P` over the original polynomial ring `R`, making it free of rank `r`. Its surjection onto `I` produces `r` ideal generators. Every ideal generating list generates `I/I^2` after reduction, giving the reverse inequality.

## Counterexample attempts and boundary checks

1. **A nonfree projective over a nonlocal base does not refute input A.** Global monic inversion is stronger than local Horrocks plus mere extension. The extra comparison with infinity in Quillen's proof specifically forces the extended base module to be free. No unsupported assumption that all projectives over `B_{gs}` are free enters the supplement.
2. **Removing monicity really does fail.** In `B=Z[sqrt(-5)]`, the invertible nonprincipal ideal `L=(2,1+sqrt(-5))` is projective of rank 1: its product with its conjugate is `(2)`. It is nonprincipal because an element of norm 2 would require integers solving `a^2+5b^2=2`. The module `L[X]` is nonfree (specialize `X=0`) but becomes free after inverting the constant 2. This constant is not monic. The supplement preserves monicity and hence avoids this boundary failure.
3. **Integrality is essential and is present.** In `B=C[x]_(x)`, the ideal `(x)` is in the Jacobson radical. It is not in the Jacobson radical of `B[Y]`: `(xY-1)` is maximal, with quotient `C(x)`, and avoids `x`. Step 3 correctly uses the finite monic quotient before drawing a Jacobson conclusion; it never draws that conclusion for all of `S^{-1}R`.
4. **Neither global Nakayama nor preservation of an arbitrary basis is being smuggled in.** The support containment is proved first; only then is Nakayama used in local rings. The CRT modifications are allowed and are in `I^2`.

## Exact stress certificates

`check_stress_cases.py` and `stress_results.json` give reproducible exact symbolic checks using SymPy 1.14.0. All identities pass; these examples supplement the universal argument rather than replace it.

For `I=(x,y)`, take `f_1=y+y^2`, `f_2=x+y^2`. The correction `b=y^2` removes the bad point `(0,-1)` over `J=(x)`, while `F` still has the extraneous point `(-1,-1)` away from `J`. The denominator `g=1+x` satisfies

`gx=(-x-y)f_1+(1+x+y)f_2`,

`gy=(1-y)f_1+y f_2`.

On the overlap, the checked matrix with columns `((-x-y)/(gx),(1+x+y)/(gx))` and `(-f_2,f_1)` has determinant 1 and completes the row. This checks both a nontrivial denominator and the gluing orientation.

For the non-complete-intersection ideal `I=(x,y)^2`, use the conormal representatives `(y^2,xy,x^2+x^4)`, characteristic polynomial `h=y^3`, and exponent 2. Then

`F=(y^2+y^6, xy-y^4, x^2+x^4)`.

The bad points over `J=(x^2)` have `y^4=-1`; `b=-y^4 in I^2` has value 1 there. The script contains explicit original-generator polynomial certificates for `y^2` and `xy` in `F`; `g=1+x^2` also gives `gx^2=f_3`. Thus `gI subset F` while the remaining extraneous points `(±i,0)` lie in `D(x^2)`. The independently computed reduced Groebner basis is `(x^4+x^2,xy,y^2)`. Here `r=3>d=2`; the example verifies that the argument is not confined to locally complete intersections.

## Required repairs

**None.** For source clarity only, the parent may prefer naming input A as “Quillen's global monic-inversion theorem (1976, Theorem 3, printed p.169)” and defining the transition orientation explicitly as above. Neither is a mathematical correction. No canonical, snapshot, or supplemental proof file was edited by this audit; no Git action or external communication occurred.
