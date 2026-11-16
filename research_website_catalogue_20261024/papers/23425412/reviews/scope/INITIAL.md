# Source-only initial freeze: 23425412

Frozen UTC: 2026-11-16 09:32:40. Completion estimate toward this scientific scope review: 45%.

## Exposure and custody

Read all three actual manuscript pages in newly rendered 135-dpi Poppler PNGs and the complete controlling `sources/published-source/container-001/tree/paper/main.tex` (230 lines). The manuscript necessarily supplied its proof before my derivation. No supplied scientific support/code/results, deposited review report, current other-family finding, or foreign mathematical body has been read. An early whole-file read of `sources/ACQUIRED.json` exposed the native public description, including claims about prior deposited reviews and finite checks; that metadata exposure is disclosed and those assertions are not treated as evidence. No scientific program was executed. No external human contact or prepared outreach occurred.

Native PDF SHA256: `f3b3f38a7f3a3a4be37482908b03ffa722879fc047925428c6bdedee83d882b6`, 60591 bytes. Controlling TeX SHA256: `bd04731bb1d998c94436cbe9e90ea84597e77722b57dd680100f699a6b7ad67c`, 9494 bytes. Own rasters `rasters/page-{1,2,3}.png` respectively have SHA256 `d82a6c7eb8beb64d4f744d8147c7e4e091fbceb85190e5ea0b5495080cef2e07`, `4a5567f2b20ed4e2ddd72eea7e8833d70b44460c02d346991ff769575527d20c`, `6282be07eb80d07279a41f7ff4feaed9661296e09cd39b84302448ed278c6f31`. Printed date/version: 16 October 2026 / Version 1.0. Native metadata states version `1.0`, publication date `2026-10-16`, creator Kriebel, Alec, ORCID `0009-0001-9320-500X`, affiliation Independent researcher, CC BY 4.0; full original fields/order/access transport are preserved by the source owner's ACQUIRED manifest, reused by reference rather than rewritten here.

## Exact target and success criterion

For the stated ordinary integral Habiro coefficient ring R and S = lim R[t]/(product from j=1 to m of (t-q^j)), the target is nonexistence of F with F(q^n) equal to standard unified sl_n homology-sphere invariant for n>=2 and F(q)=1 when the stated Casson convention is nonzero. It is a claim about matrix size n with one common q parameter. Success requires (a) the literal foreign conjecture really has this S and these evaluations, (b) the cited invariants' linear coefficient really equals n(n^2-1) times the same nonzero Casson normalization, and (c) the local algebraic contradiction. Part (c) can be checked here; (a)-(b), and the named surgery orientation, remain source dependencies.

## Actual independent derivation and controls

Work in D=Z[x]/(x^2). The substitutions q=1+x and q^{-1}=1-x respect qq^{-1}=1 and send (q-1)(q^2-1) to x(2x)=0. Thus projection R -> R/((q-1)(q^2-1)) followed by this substitution gives the required ring map T. Compatibility of finite coordinates makes every F(q^n) well defined: if m>=n, E_m(q^n)=0 exactly; any difference in representatives evaluates to zero, and higher coordinates reduce compatibly.

Take one coordinate m=3. It has a finite polynomial representative P(t)=sum_i a_i t^i (monic division can restrict i<=2, though that is unnecessary). Write T(a_i)=alpha_i+beta_i x. For n=1,2,3,

T(P(q^n)) = sum_i alpha_i + x[sum_i beta_i + n sum_i i alpha_i].

This is an exact identity in D, with finite sums. Constants agree and linear coefficients form an affine sequence. Hence v_3-2v_2+v_1=0. This argument uses no Taylor injectivity, limit differentiation, topology of formal infinite sums, division by q-1, or interpolation denominators. It works for arbitrary R coefficients because T is applied first. If F(q)=1 then v_1=0.

Conditionally on the manuscript's external coefficient identity, the triple is (0,6 lambda,24 lambda). Its second difference is 12 lambda, nonzero for any nonzero integer/rational Casson value in characteristic zero. The scalar cannot vanish through torsion because D has coefficient group Z. With sizes 2,3,4 the cubic values are 6,24,60 times lambda and the second difference is 18 lambda, independently confirming that omitting size 1 does not fix the obstruction. The constant sequence and lambda=0 are boundary cases: this obstruction supplies no nonexistence or existence statement there.

For the displayed Poincare-series expression only, cancellation yields the finite polynomial summand q^k(1+...+q^k) product_{j=k+2}^{2k+1}(1-q^j). There are exactly k factors in the product, each divisible by q-1, so every k>=2 term maps to zero under T. k=0 gives 1, and k=1 gives (1+x)(2+x)(-3x)=-6x in D. Thus the displayed series has first coefficient -6, provided it is the claimed invariant and the infinite sum is interpreted in its stated Habiro topology; eventual annihilation makes its first-jet computation finite. The coefficient identity would then force lambda=-1 and v_3=-24. The calculation does not itself identify the surgery orientation or establish the invariant-to-series identification.

## Falsifiers and remaining scope gap

The central falsifiers are a mismatch in the original completion, a rank/parameter rescaling in the transferred coefficient formula, a factor/convention mismatch between unified sl_n and the published PSU(n) perturbative invariant, or a wrong series/surgery identification. Any such mismatch affects the original theorem, not merely priority. No local algebraic counterexample was found. Neither exact arithmetic nor archive checks establish those topology inputs. Firstness/current openness is not asserted, and absence from a bounded search would not establish it.

This is an actual-result freeze, not a plan-only list. Provisional strongest result: the finite-jet obstruction is proved for the stated algebraic completion, and the displayed finite coefficient arithmetic is verified; the topological theorem and literal-conjecture application remain conditional until primary sources may be checked. Followup is null pending that gate; no repair or replacement theorem is proposed.
