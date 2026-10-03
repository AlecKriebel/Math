# Independent audit: prescribed second coefficient and minimum area

Audit date: 2026-10-03 UTC.

## Verdict

**The prior-publication attribution is supported. The frozen packet does not pass a complete proof-verification audit.**

The proposed value and its attaining maps are consistent with Aharonov, Shapiro and Solynin's later Theorems 3–4 (2006), which explicitly credit their 1999 paper. The local analytic calculation for typically-real functions is sound at its stated classical representation-theorem level. However, the replacement argument for passage to the whole univalent class has an unresolved source-level inequality discrepancy. Consequently, the claim that this comparison route has been checked must be qualified. This is not a counterexample to the published minimum-area theorem.

The frozen manifest's SHA-256 is `9819afddd984e59a57973ab3f467cc842570d7f05220191ea248db537fc3d276`. All eight frozen input hashes were verified before and after the review. No frozen input was edited.

## 1. Blocking source discrepancy

The comparison in Section 3 of PROOF.md follows the author-posted OCR of [the 2001 paper](https://www.academia.edu/31230876/A_minimal_area_problem_in_conformal_mapping_II), printed pp. 267–268, equations (2.3)–(2.6). In its notation:

- Assuming `|f(r)| >= F(r)`, the symmetrized biangle is included in the comparison biangle: `A*(r) subset B(r)`.
- Equation (2.4) identifies the reduced moduli of `A(r)` and `B(r)` through the normalized conformal maps.
- The OCR of (2.5), attributed to Solynin's Lemma 1.3, says `m(A(r)) > m(A*(r))`.
- The OCR of (2.6) says `m(A*(r)) >= m(B(r))`.

These directions would give the stated contradiction. They are essential, not cosmetic.

The cited [1993 Solynin paper](https://www.mathnet.ru/eng/znsl5788) was independently obtained through Math-Net's openly available full-text link. Its printed p. 120, Lemma 1.3 and equation (1.9), were inspected as a page image. The printed inequality is instead

`m(D; e1,e2) <= m(D*; e1*,e2*)`.

The construction immediately preceding that lemma is specialized: both biangle vertices lie at zero; locally there are exactly two domain components; the two components of the complement with zero removed are circularly symmetrized about opposite rays; and the new domain is the complement of those transformed sets and zero. The lemma assumes the stated local boundary condition (**), and equality is restricted to a rotation. This is not merely ordinary circular rearrangement of the biangle as an open set.

The other cited reference, [Solynin's 1999 modulus survey](https://www.mathnet.ru/rus/aa1040), was also obtained through its open Math-Net PDF. Lemma 1.1 on printed p. 13 was inspected as a page image. For strict inclusion of biangles with corresponding equal vertex angles, it gives `m(D1)>m(D2)` when `D1 subset D2`. That agrees with the inclusion direction used in the 2001 OCR; it does not supply a simple convention reversal resolving the preceding discrepancy.

A printing error, a translation correction, or a different applicable symmetrization theorem may explain the conflict. None was verified. It would be unjustified to silently replace the printed sign, announce that the foundational theorem was checked, or infer that the published area theorem is false.

### Access limit and required repair

The 2001 publisher page is subscription content. In the cloud browser, the author-posted page's “See full PDF” control opened an authentication/terms prompt. No account access or agreement was attempted. Thus the exact 2001 page images were not available in this audit. The same source-quality limitation remains for the 2006 displays; their elementary identities were independently recomputed rather than visually authenticated.

To remove this blocker, provide an accessible authoritative version resolving the relevant biangle inequality and its conventions, or a different fully stated and applicable coefficient comparison theorem with verified provenance. Alternatively, remove the full-proof-verification claim and retain an explicitly attributed literature result plus the verified extremal and typically-real calculation. Merely rerunning symbolic checks does not repair this issue.

## 2. Scope of the 2001 argument

The surrounding Lemma 3 assumes extremality, but the isolated comparison block uses normalization, the slit-adjusted symmetrized domain, conformal invariance, inclusion and the reduced-modulus theorem. The extremality hypothesis is used outside that block to obtain a contradiction with monotonicity of the point-evaluation minimum. I found no additional use of extremality inside the comparison block. Hence an extremal-only hypothesis is not the identified obstruction.

The construction still requires the standard geometric inputs: simple connectedness of the symmetrized/slit domain, strict conformal-radius increase unless already symmetric up to rotation, and continuous variation of the slit endpoint to restore conformal radius one. For radial approximants of an arbitrary univalent function, the original domain has analytic boundary; near the two marked vertices the slit images are analytic, so the local regularity condition is not an evident obstruction. The unresolved sign and precise specialized symmetrization remain material.

## 3. Verified mathematical parts

### Explicit maps, range and endpoints

With `tau=2(2-a)/3`, the nontrivial range `1/2<a<2` corresponds exactly to `0<tau<1`. The inverse-Koebe branch in (2) exists on the indicated slit plane, sends zero to zero, and maps the disk to a disk slit along its negative radius. Composing it with `q(w)=w+w^2/2` and dividing by `tau` gives an injective normalized map with second coefficient `2-3tau/2=a`.

The removed line segment and its polynomial image have area zero. Thus the attained area is `3pi/(2tau^2)=27pi/[8(2-a)^2]`. In particular, the denominator seven in the 1999 HTML abstract cannot be the sharp lower bound: at `a=1`, the explicit map has area `27pi/8`, less than `27pi/7`.

For `0<=a<=1/2`, `z+az^2` is injective in the open disk, including the endpoint `a=1/2`. The coefficient area identity proves the minimum and uniqueness for fixed coefficient there. At `a=2`, the classical second-coefficient equality theorem gives a Koebe rotation, of infinite area; `a>2` is excluded by the same classical theorem. As `a` decreases to `1/2`, the nontrivial construction becomes `q`; its value joins the polynomial branch. As `a` increases to two, the value diverges.

### Typically-real lower bound and limiting kernel

The proof correctly uses a probability measure on `[0,pi]` with first cosine moment `a/2`. This accounts for the factor of two relative to the paper's symmetric-circle convention. Its finite-radius inner-product kernel has the required factor `r^2` and argument `r^2 exp(it)`.

The displayed derivative formula is valid with the analytic branch fixed at zero. At the two Pick-branch endpoints, multiplication by `1+p` cancels the derivative singularity; at `1` and `-1`, the derivative has analytic continuation for fixed `0<tau<1`. Those facts justify uniform convergence of the kernels, including the removable endpoint quotients. Finite Dirichlet energy then permits the inner-product limit; infinite energy needs no limiting argument for the lower bound.

For typically-real functions that are not univalent, the minimized quantity here must mean Dirichlet energy (area counted with multiplicity), not ordinary image area. The packet's use of the symbol `A(f)` in (9) should make this convention explicit or restrict that statement to the univalent typically-real functions, which suffices for the intended application.

Both boundary-kernel branches and the remainder factorization in (8) check exactly. The remainder is nonnegative because `s=sqrt(y^2-tau)>=0` and `4y^2-tau>0` on the slit arc. The moment integral equals the extremal area. The final Hilbert-space identity proves the typically-real bound and uniqueness in that class.

### Coefficient limit and exhaustion

Conditional on (10), `|f(r)|=r+a r^2+O(r^3)` after making the second coefficient real and nonnegative, whereas `G(r)=r+b r^2+O(r^3)`. Division by `r^2` and passage to zero yield `b>=a`. This does not yield a strict coefficient inequality.

The piecewise minimum function is continuous and increasing on `[0,2)`. The normalized radial approximants have second coefficient `r a2` and area `pi sum(n |a_n|^2 r^(2n-2))`, increasing to the original area. Consequently, once the bounded-domain comparison is established, this passage to arbitrary univalent functions is legitimate. No unjustified interchange of the symmetrization construction with a kernel limit is needed.

## 4. Equality and attribution boundaries

The packet independently proves uniqueness for the polynomial range and for the typically-real problem. Its non-strict comparison does not independently classify every equality case in the full univalent class: strict pointwise comparison does not imply a strict second-coefficient gap, and two domains can have equal area without being identical. The full-class equality assertion should therefore remain explicitly attributed to the published theorem or receive a separate rigidity argument.

The public [2006 author-posted text](https://www.academia.edu/31230874/Minimal_area_problems_for_functions_with_integral_representation), Section 4, identifies Theorem 4 as the full univalent-class result and credits the 1999 paper. Its proof explicitly imports coefficient Lemma 9 from that earlier paper. The unavailable 1999 proof cannot be described as independently read or replaced by a fully checked reconstruction on the present evidence.

## 5. Reproducible checks

`audit_controls.py` verifies the freeze, independently performs 16 exact identities/negative controls, and reruns the author's 14-check script. All algebra checks pass. The checks include normalization, the prescribed coefficient, derivative cancellation, the area constant, the support remainder, monotonicity, the branch join, and deliberate wrong-denominator/wrong-coefficient controls.

These checks are not a formal analytic proof and do not establish the symmetrization inequality, representation theorem, source transcription accuracy, or full-class equality classification. `audit_controls.json` records both the successful algebra and the non-passing full-class proof audit.

## Primary source fingerprints

- Solynin (1993), original Russian paper, openly served by Math-Net: SHA-256 `9f012a2a435fd07df393b91997aa10b189c4dce3d5b1a96231bb6100db0b6cb1`; read the relevant text on printed pp. 117–120 and visually inspected pp. 118 and 120, especially Lemma 1.3 on p. 120.
- Solynin (1999), original Russian modulus survey, openly served by Math-Net: SHA-256 `c7a3e9e054d95846ecf11818b51c54b4e97c8a0066f9e93567b9d5c36d9f64d5`; inspected definitions and printed p. 13, Lemma 1.1.

The audit does not redistribute either complete source paper.
