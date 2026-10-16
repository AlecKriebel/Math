# PR563 / Problem 2306072: commentary and rational/two-functional trail

## Decision

**The bounded audit is complete. Brickman1984 and Goh1994 are now fully compared and do not supply the target negative answer. The unseen Duren2014 commentary remains a material, specifically bounded priority gap. Apparent-new-resolution and publication acceptance remain held under the unchanged acceptance criteria.** No earlier construction proving the exact polar/radial reversal was found in the inspected primary texts. No claim of historical firstness, novelty certification, or present-day openness follows.

This decision concerns originality and attribution. It does not reject the candidate's mathematical theorem or reopen its independently audited analytic proof. A reviewable draft may state its exact theorem with these limitations, but qualifying the wording does not close a material comparison gap. I have not contacted any person, modified canonical artifacts, committed, pushed, or changed remote/index state. The parent owns integration and publication decisions.

## Exact target and independent scope

Hayman-Lingham2018 printed p143 / PDF p144 asks about monotonicity of the polar argument and the angle between radius and tangent of an actual support slit. The problem and its dated update were visually inspected. The update is evidence of what the compilers had been told, not an openness certificate for 2026.

The candidate defines epsilon=10^-24 and globally maximizes Re L over normalized schlicht S, where

`L(f)=a2(f)+i*epsilon*(a4(f)-3*a3(f))`.

It claims that every maximizer's actual omitted slit has nonmonotone continuous argument, signed outward radial angle, and ordinary unsigned outward radial angle. Compactness gives actual maximizers; the tip-radius bound and local positive-trajectory uniqueness identify the tested coordinate arc with their omitted slit. No arbitrary-trajectory extremality converse is used. Its reversal test is for theta=arg w and beta=arg(-W'/W), with increasing t directed inward. A turn of tangent direction alone is a different claim.

I read the complete candidate manuscript and derived the source mechanisms before consulting old priority02/03 reports. The freeze is recorded in INDEPENDENT_MECHANISM.md and the timestamped log. After acquiring Goh1994 and Brickman1984, their independently derived scopes were added to that freeze before reading those earlier reports. No other agents' new reports were used as mathematical evidence.

## Complete primary texts and exact comparisons

### Brickman1984: a rational functional is not a rational extremizer

Brickman, *Functionals of rational type over the class S*, Proc. AMS92 (1984), pp372-376, DOI [10.1090/S0002-9939-1984-0759655-5](https://doi.org/10.1090/S0002-9939-1984-0759655-5), was acquired by the ordinary public AMS DOI page's observed PDF control. The public page explicitly describes its older archive as freely available. All five pages were read, with complete key pages374-376 inspected visually.

Theorem1 identifies four equivalent properties: rationality of Phi(w)=L(f^2/(f-w)) for one univalent f, rationality of L's Toeplitz kernel, finite sums of derivative evaluations at disk points, and rationality of Phi for every f in S. The Cauchy-integral duality in the lemma and residue computation prove the equivalence. None of these properties says that a maximizing f is a rational function.

Theorem2 preserves finite derivative-evaluation type under composition with a disk self-map. Section4 applies this to truncation of an already established support slit. The new support functional is J(h)=L(h composed with phi), where phi is the subordination map from that actual slit truncation. It does not make an arbitrary Schiffer trajectory extremal, assert polar/radial monotonicity, or construct a negative example. The complete paper contains no target reversal construction.

For this candidate, exact composition through degree4 gives the h4 coefficient `i*epsilon*p1^4`, where `phi(z)=p1*z+p2*z^2+...`. A conformal subordination map has p1 nonzero. Thus this preservation result does not lower the candidate to a degree3 positive-monotonicity functional. The other transformed coefficients depend on phi; equality of the transformed functional to the original is not asserted.

### Goh1994: conditional rational-f rigidity and two derivative functionals

Goh, *Support points and double poles*, Proc. AMS122 (1994), pp463-468, DOI [10.1090/S0002-9939-1994-1197537-4](https://doi.org/10.1090/S0002-9939-1994-1197537-4), was acquired through the same ordinary AMS control. All six pages were read; complete key pages465-466 were inspected visually.

Section2 begins with a support function f already assumed rational. Srebro's rational-slit classification gives a Marty transform of Koebe, hence a half-line. Theorem1 then uses a pole-order obstruction to force a rotation of Koebe when Phi(0) is finite nonzero and Phi has no poles of order2. If a nonrotation Marty transform has a second simple zero outside the disk, the reflected Schiffer equation would have a double pole there, contradicting its allowed pole pattern.

Remark(iii)(a) on p465 extends that same conditional argument: if Phi has an order m>=1 pole at0 and no poles of order m+2 elsewhere, a rational support f must again be a Koebe rotation. This is directly applicable **conditionally** to the candidate's Phi, which has m=3 and no other finite pole. The original rational-f hypothesis persists in the remark. Dropping it would incorrectly force every finite coefficient support point to be Koebe and contradict the paper's own setup and classical non-Koebe coefficient examples.

Section3's Theorem2 requires simultaneous global maxima for two first-derivative evaluation functionals `exp(-i*sigma_j)*f'(zeta_j)` at nonzero distinct disk points. Division of their independent reflected differential equations produces a common algebraic continuation. The proof forces its branches to coincide, establishes rationality, and excludes nonrotation Marty transforms. The candidate supplies one coefficient functional and no second independently maximized first-derivative evaluation. The theorem therefore has no applicable trigger here. The complete paper contains no theta or beta sign-reversal construction and no exact mixed fourth-coefficient perturbation of the target type.

There is a bibliographic distinction worth preserving: Goh1994 ref3 is Goh's **1992 doctoral thesis**, whereas the commentary's G1 is the **1992 journal article**, pp197-206. They are not interchangeable complete sources. The primary journal abstract says the article concerns coefficient functionals. A search result that reproduces the thesis's broader abstract must not be treated as the journal article's full scope.

### Duren-Leung-Schiffer1983 and Zhang-Ma1991: tip saturation

The user-supplied complete DLS1983 article, DOI [10.1080/17476938308814018](https://doi.org/10.1080/17476938308814018), was read through pp263-277 (PDF pages2-16; page1 is a publisher wrapper). Complete key pages264,268,272-274 were visually inspected. Its second differential equation arises from the saturation `|beta_tip|=pi/4`, equivalently Re Phi(tip)=0. A Mobius transform of f then also maximizes the same real functional. The algebraic-continuation arguments use that additional equation. Theorem3 excludes tip saturation for every finite coefficient functional with nonzero highest coefficient, including this candidate. Theorem4 concerns rational f; Theorem5 concerns rational-type L together with tip saturation and, originally, no double zeros of Phi. Those distinct hypotheses must remain distinct.

The user-supplied complete Zhang-Ma1991 article, DOI [10.1016/0022-247X(91)90330-3](https://doi.org/10.1016/0022-247X(91)90330-3), was read through all four pages598-601; key pages599-601 were inspected visually. Its sole theorem removes DLS Theorem5's no-double-zero restriction while retaining rational-type L **and maximum tip-angle saturation**. The reciprocal map g=1/f, simultaneous algebraic continuation, and local inverse at the infinite preimage yield rationality and a half-line. Its full text provides no separate interior reversal construction or fourth-coefficient perturbation.

These comparisons close the original DLS1983 and Zhang1991 gaps for this target. They do not close a later commentary merely because it reprints the older article.

## Checkable consequences and boundary cases

Coefficient extraction independently gives

`Phi(w)=-a/w-b/w^2-c/w^3`,

`a=1+i*epsilon*(2*a3+a2^2-6*a2)`, `b=i*epsilon*(3*a2-3)`, `c=i*epsilon`.

Phi has an order3 pole at0; Q=Phi/w^2 has order5. A double pole of Phi means exactly order2, as Goh1994 p464 explicitly specifies. Confusing Phi with Q or a pole with a zero changes the hypotheses. These identities and the transformed functional are checked symbolically with exact rational Gaussian coefficients in exact_checks.py. Ten checks pass; they supplement the written derivations and do not prove the classical inputs.

The inspected rational-f classification in fact supports a useful conditional deduction: **assuming the standard classical support theorem and Goh1994's proved rational-f classification, every candidate global maximizer is nonrational.** Here is a direct check that does not use the fine reversal expansion. The candidate's coefficient bound gives |a2-2|<8*eta, eta=10^-12. If a maximizer were rational, Goh1994 Remark(iii)(a) with m=3 would force `f(z)=z/(1-u*z)^2`, |u|=1. Then a2=2u, so |u-1|<4*eta and |u^3-1|<12*eta. Its slit is w=-r/u, r>=1/4. The necessary positive trajectory condition would make

`Phi(-r/u)=a*u/r-b*u^2/r^2+c*u^3/r^3`

real for every r in that interval, so its imaginary polynomial coefficient Im(c*u^3) must vanish. But it equals epsilon*Re(u^3)>epsilon*(1-12*eta)>0. This contradiction excludes rational f. It shows precisely why rational-type-functional rigidity cannot dispose of the candidate by claiming its slit is a ray. This is an authored consequence of inspected classical results, not a historical novelty claim.

The candidate's first-order sign function is `q(t)=t^2-(2/5)*t^4`. Its exact values q(1)=3/5 and q(7/4)=-441/640 exceed the certified error 2000*eta in opposite directions. The finite checks reproduce those margins only; the uniform analytic remainder bounds and actual-slit identification remain the candidate's separate proof obligations. At epsilon=0 the degree4 term, Phi's order3 pole, and the reversal margin disappear, as expected. A limiting picture at epsilon=0 is not evidence of reversal.

The functional is supported at the origin:

`L(h)=h''(0)/2+i*epsilon*(h''''(0)/24-h'''(0)/2)`.

Its unique rational Toeplitz kernel is `z^-3-3*i*epsilon*z^-4+i*epsilon*z^-5`. Finite derivative evaluations at nonzero points have kernels with poles at those nonzero points and analytic continuation at0. Rational-function uniqueness excludes an identical finite representation with all evaluation points nonzero, including up to functionals constant on normalized S. This excludes identity with the **advertised** Goh1998 class. It does not certify that every remark and construction in that unread paper is irrelevant, or that different functionals cannot share a support point.

## Remaining source materiality

The public Springer chapter for DOI [10.1007/978-1-4614-7949-9_22](https://link.springer.com/chapter/10.1007/978-1-4614-7949-9_22), pp499-516, was inspected both by HTTP and ordinary browser DOI navigation. It explicitly offers subscription/institutional access. No chapter prose or original page was acquired. The primary Crossref JSON hash agrees with the parent's supplied hash. Its14 reference records represent13 bibliographic entries because the Russian/English Bakhtin1981 entry is split. The actual public page labels these entries B1,B2,Br,Bw1,Bw2,D,G1,G2,G3,P,SS,Sch,ZM and supplies the keyword Two-functional conjecture.

The references include post1983 items Brickman1984, Bakhtin1986, Zhang1991 and Goh1992/1994/1998. This is positive evidence of a later discussion/citation trail, not proof of a particular new theorem. It prevents assuming that the unseen material simply repeats 1983. The title and keyword suggest tip-angle and two-functional mechanisms, but that suggestion does not exclude an additional global geometric example or retrospective attribution. The parent separately reports that the ordinary GoogleBooks preview disables the target chapter; that is an inherited access observation, not a local full-text inspection.

| Missing item | Current evidence and exact residual gap | Materiality for this target |
|---|---|---|
| Duren2014 commentary | Primary chapter identity, complete public refs and keywords; zero chapter-text coverage. Need the commentary prose, its statement of later progress, and any examples/claims beyond tip saturation. | **Material unresolved priority/attribution gap.** Closely connected primary retrospective with a later coefficient/rational trail. No established adverse theorem, but no complete exclusion. |
| Goh1992 journal article, pp197-206, DOI10.1080/17476939208814600 | Ordinary primary abstract explicitly concerns coefficient functionals and two-functionals; Read this article leads to an explicit login/purchase page. Need all10 pages, coefficient hypotheses, intermediate constructions and remarks. | **Material unresolved coefficient-family comparison.** Simultaneous-maximization conclusion alone does not apply; intermediate single-functional geometry remains uninspected. |
| Goh1998, pp111-126, DOI10.1112/S002461079800636X | Primary Wiley/Cambridge abstract; ordinary Wiley ePDF explicitly denies full access. Nonzero derivative-evaluation class differs from origin jets. | Advertised main theorems do not trigger; **secondary uninspected trail**, not an independently established exact adverse lead. Full16 pages needed to close subsidiary construction scope. |
| Bakhtin1981, Russian pp154-159 / English pp122-126, DOI10.1007/BF01086066 | Primary Springer identity, references, subscription page; no article text. | **Uninspected background/coefficient trail**, not a proved global reversal. Exact materiality cannot be promoted from title alone. Need original theorem and constructions. |
| Bakhtin1986 preprint25 | Primary commentary reference only; no reliable complete copy or theorem statement obtained. | **Uninspected trail**, with no established overlap or exclusion. Need actual preprint scope, not a theorem inferred from citation adjacency. |
| Goh1992 thesis | Positively identified as a different source by Goh1994's complete ref3; no thesis text. | Background to the complete Goh1994 proof, not a substitute for the missing journal article; no new target-negative evidence. |

This classification deliberately avoids turning every unread classical reference into a publication blocker. The two material gaps are the immediately relevant commentary and coefficient two-functional article; the others remain disclosed uninspected background or subsidiary scope. Conversely, lack of an inspected adverse example does not establish that a directly relevant unread source is harmless. A defensible bounded comparison can say the inspected corpus supplies no earlier target reversal. It cannot yet certify an apparent-new resolution under the unchanged requirement to resolve material prior constructions, even without a global-firstness claim.

The next decisive evidence is a lawful complete chapter/commentary copy and a lawful complete Goh1992 journal copy. Check any explicit mixed coefficient perturbation or actual support-family slit against `theta'=Im(w'/w)` and the signed/unsigned radial angle with its infinity limit and tip domain. If those texts only give the saturation/two-functional mechanisms identified here, they can be downgraded to background with a complete-text receipt. If they identify an earlier actual polar reversal, the candidate needs attribution and repositioning. No author, librarian, publisher support service, or other individual has been contacted, and no outreach is prepared.

## Coverage, reproducibility and limits

SOURCE_COVERAGE.json records source identities, SHA256 values, complete-page coverage, visual page coverage, and explicit access failures. ACCESS_LEDGER.json records HTTP status/content-type/magic checks and the successful observed browser controls. Raw copyrighted PDFs, extracted text and rendered images are only in ignored .cache or the preexisting user-supplied source area. They are not included in the authored seal. The initial failed downloads named .pdf were HTML, detected by magic and content-type; the later verified AMS acquisitions replaced those cache slots and have different recorded hashes.

The authored seal enumerates every present inner authored file, including .gitignore. Re-running exact_checks.py and seal.py reproduces the finite checks and verifies identity/completeness of the authored package. This is integrity evidence, not an exhaustive priority proof or a formal validation of classical support theory. Prior priority02/03 reports were read after the independent mechanism freeze only to identify which older gaps were superseded; their unsupported full-source exclusions were not inherited.

Final estimate: **100% of this bounded audit assignment; about80% of source-based clearance for this commentary/citation family**, with the percentage expressly non-certifying. The strongest verified result is the complete exclusion of the inspected Brickman1984/Goh1994/DLS1983/Zhang1991 constructions as the exact target precedent, together with the rational-L/rational-f distinction and the explicit nonrational-maximizer deduction. The remaining material gap is the unseen commentary and coefficient two-functional journal article. Overall novelty and publication acceptance remain held.
