# Independent adversarial audit: 30002711

Date: 5 October 2026. Supplied rank 725; descriptor OWR-13351-010.

## Controlling verdict

**QUALIFIED PASS for the retained partial mathematics, with one required completeness qualification. Recommended problem status: unsolved, five of five approaches used.** This audit is not an unconditional endorsement of every standalone sentence in the frozen record. The final nonzero-section translation sentence of Proposition 3.1 needs a complete coefficient DVR; without that hypothesis it is false as a generally available change of coordinates. The exact replacement, counterexample, and complete dependency sweep appear below. Every intended application already has the required completeness. No retained conclusion, counterexample scope, approach count, or unsolved disposition changes.

No universal cyclotomic-ring lifting theorem, general counterexample, verified prior complete solution, novelty claim, human peer-review claim, or certification of current worldwide openness is established. The five approaches remain partial approaches. Their finite computations do not resolve the unrestricted question.

The author files and author archive were not edited. All mathematical checks in this audit were implemented independently; no author module was imported. The author scripts were separately replayed. No additional worker or remote write was used.

## 1. Immutable binding and exact scope

Author manifest SHA-256:

`362a6ed1502b421e00efab914b4f02d125e7788a906f7273cb25cf074a83f177`

Author archive SHA-256:

`ae4193f1e0c8a555b5d46ec59ae3aacea615a2536d578eaf4aa9a97e0a5ee9c0`

The archive is 20,745 bytes. Its ten members are the nine payload files and MANIFEST.json. Every member was compared byte-for-byte against the frozen publication directory; CRCs, names, duplicate-member absence, encryption flags, and symlink absence were checked. The directory inventory, file types, sizes, and hashes match the independently supplied manifest pin. The originals were rechecked after testing.

The target is the universal prescribed-coefficient-ring assertion for algebraically closed k of characteristic p: a specified faithful cyclic local action should lift smoothly over W(k)[zeta_|G|]. The record studies the p-power form over R_n = W(k)[zeta_(p^n)]. It does not replace universal sufficiency with existence over some finite extension, existence of one lift for each group order, existence at the generic point alone, or necessity of this ring for every individual unmarked lift. No equivalence proof between arbitrary cyclic groups and the p-power version is claimed as a new result here.

The exact current catalogue text was not inspected. The author reported HTTP 403; this audit's fresh web extraction also failed. Raw upstream AI corpus records were not inspected. The rank/ID/descriptor association is supplied context, not an independently verified verbatim catalogue statement.

## 2. Source verification and inference boundaries

Six supplied public-source PDF byte streams were independently hashed and sized. All match the frozen SOURCE_VERIFICATION.json metadata. Fresh text extraction was performed from those bytes; OWR PDF page 45 and Obus PDF page 36 were freshly rendered and visually inspected. No PDF, extract, image, or raw retrieval record is included in this audit bundle.

- Obus's OWR 49/2014 passage on printed page 2801 states the algebraically closed local lifting setup and distinguishes general cyclic existence from a prescribed cyclotomic coefficient ring, with p-adic order at most two already known. The notation in that passage must be read as a coefficient DVR; the later formulation removes any potential field-versus-ring ambiguity. [Original OWR report](https://doi.org/10.4171/owr/2014/49)
- Obus's Question 8.6 explicitly gives the universal p-power ring-of-definition question. Section 8.2 credits the known order-p and order-p-squared results, and distinguishes existence of at least one liftable extension for each order from the universal assertion. Proposition 6.2 supplies the standard different criterion. This audit separately reconstructs only its necessary direction. [Obus survey, v2](https://arxiv.org/abs/1703.01191v2)
- The February 2026 Kummer–Artin–Schreier–Witt paper constructs group-scheme isogenies and describes unramified covers of flat local algebras. The introductory construction removes the ramification divisor; its Section 5 normalization calculation concerns the displayed localized affine group-scheme coordinate rings. It does not assert smooth normalization after arbitrary pole substitutions across the missing point of a ramified local disc. That distinction is an inference from the inspected hypotheses, not a criticism or disproof of its theorems. The v3 date and public preprint status were freshly checked; no current acceptance claim is inferred. [Dang–Nguyen-Dang, v3](https://arxiv.org/abs/2410.21224v3)
- Dang's published Theorem 1.2 extends deformations in equal characteristic p and permits a finite extension of the deformation DVR. Its mixed-characteristic refined lifting problem is posed separately. Neither statement identifies the coefficient ring required here. The supplied publisher PDF was freshly extracted; this audit's publisher web fetch timed out. [Deforming cyclic covers in towers](https://doi.org/10.14231/AG-2026-010)
- Pop's Theorem 1.1 gives more than unspecified individual existence: a coefficient extension can be chosen uniformly for bounded different degree. It still does not identify that extension with R_n. [Pop's Oort theorem](https://doi.org/10.4007/annals.2014.180.1.6)
- Obus–Wewers' existence results, including the p-adic-order-at-most-three case, must not be restated as prescribed-ring sufficiency through order p cubed. [Cyclic extensions and the local lifting problem](https://doi.org/10.4007/annals.2014.180.1.5)

The author's repository prior-attempt search was reviewed for its stated scope and limitations. This audit did not repeat its remote branch/PR/history searches and does not independently certify their completeness. The record appropriately excludes renamed, unindexed, deleted, unpublished, and differently located work from any no-prior-attempt inference. No worldwide literature exhaustion is claimed.

## 3. Required qualification: nonzero-section translation

### Location and correction

The origin-fixed portion of Proposition 3.1 is valid over a characteristic-zero DVR without completeness. Its final sentence also invokes translation to an arbitrary R-valued fixed section. That invocation is valid in the intended complete setting but is not justified for an arbitrary DVR.

The following exact replacement for the standalone proposition's statement controls this audit:

> Let R be a complete DVR of characteristic zero, and let a faithful cyclic group of order q act continuously by R-algebra automorphisms on R[[Z]]. If the action fixes Z = 0, the derivative of a generator is a primitive qth root of unity in R. The conclusion also holds for an R-valued fixed section Z = b with b in the maximal ideal of R, after the continuous R-algebra change of coordinate Z to Z - b.

For complete R, substitution by Z + b or Z - b is defined coefficientwise by convergent sums in R. For a section fixed by f, the translated action is X mapped to f(X+b)-b and fixes zero. The standard derivative argument then applies. R-linearity is made explicit to avoid any unintended semilinear interpretation.

### Explicit counterexample to unrestricted translation

Let R = Z_(3), the localization of Z at the prime 3, which is not complete. There is a unique formal series H(Z) in R[[Z]] with H(0)=1 and H(Z)^2=1+2Z: solve recursively for each coefficient, dividing only by the unit 2. If translation Z to Z+3 were an R-algebra endomorphism of this power-series ring, applying it to that identity and taking constant terms would give a rational number a with a^2=7. No such a exists. Thus even translation by an element of the maximal ideal need not exist over a noncomplete DVR. The opposite translation similarly would force a square root of -5. This does not contradict convergence over the completion Z_3.

This counterexample concerns the unqualified coordinate-change step, not the valid origin-fixed derivative theorem and not the cyclic local lifting problem.

### Complete use sweep

1. Lemma 2.1 assumes R complete explicitly. Its Weierstrass preparation and elimination of T are legitimate in the complete local topology.
2. Proposition 2.2 uses k[[z]], k[[t]], and W(k)[zeta_p]. The equal-characteristic power-series rings are complete; W(k) is a complete DVR for perfect k; adjoining the cyclotomic root gives a finite module and hence a complete ring. All root extractions and substitutions used there are valid.
3. Proposition 3.1's origin-fixed proof has no nonzero translation. Its extension to a nonzero section is exactly the qualified statement above. The cyclotomic divisibility conclusion only uses the origin-fixed argument after a permitted change of coordinates.
4. Proposition 3.2 uses R=W(k), so its nonzero constant term and substitution are valid in the (3,Z)-adic topology. Its inverse is explicitly the second iterate. It asserts no R-valued fixed section and makes no prohibited translation.
5. Proposition 4.1 uses R_n=W(k)[zeta_(p^n)], which is complete as a finite extension of W(k). Its substitutions fix the origin, so no hidden nonzero shift is involved.
6. Proposition 5.1 uses the complete ring W(k)[zeta_3]. At the coefficient valuation it explicitly localizes and then completes before using the displayed integral equation. This intermediate localization is not used to translate arbitrary formal series by nonzero constants; the change W=1+lambda Y is polynomial. Weierstrass preparation is used only under the hypothetical smooth complete model.
7. Lemma 6.1 assumes a complete target DVR. Its compatible inverse limit relies on that stated assumption.
8. Proposition 6.2 assumes R complete. The Eisenstein extension is finite over R and therefore complete; its defining change is polynomial, not an unsupported translation.

No downstream application to an ordinary noncomplete DVR was found. Accordingly the qualification does not invalidate any of the five partial approach conclusions, the C3 example, the bad birational model, or the recommended unsolved status. The author freeze is preserved; this audit must accompany it unless a separately identified corrected version is produced.

## 4. Finite-flat invariant quotient lemma

**Verdict: pass under its stated complete-DVR hypotheses.**

Let B=R[[T]], A=R[[Z]], and let the reduction of F have Z-order d. In B[[Z]], the reduction of F(Z)-T modulo the coefficient maximal ideal (pi,T) is Z^d times a unit. Weierstrass preparation applies over the complete local ring B, even if F has a nonzero constant term in pi R. Division yields a free B-module of rank d with basis 1 through Z^(d-1). Eliminating T is valid because F is topologically nilpotent in A; the quotient identifies with A. Freeness makes the structural map injective and gives fraction-field degree d.

If d distinct R-automorphisms fix F, the fixed-field theorem shows that their fixed field is Frac(B). Every element of A^H is integral over B and lies in Frac(B); regularity and normality of B force it into B. This proves the invariant ring assertion without averaging by d, which would be impermissible in wild residue characteristic.

The special-fiber conclusion needs faithful reduction and uses the same degree comparison over k. The audit does not infer a general invariants-commute-with-base-change theorem. If reduction loses faithfulness, this comparison fails exactly as in Approach 3. Finally A=R[[Z]] is formally smooth over R; flatness of an unrelated normalization would not establish that conclusion.

## 5. Approach 1: explicit order-p lift

**Verdict: pass; known positive case only.**

The Artin–Schreier representative is reduced correctly. The regular part is removed using algebraic closure for the constant term and Hensel's lemma for the remaining series. Perfectness removes p-divisible negative exponents. A nontrivial reduced representative must have a pole; its largest pole m is prime to p. Writing it as t^(-m)h(t), the coordinate t'=t h(t)^(-1/m) indeed gives t'^(-m), with the sign of the exponent correct.

The extension valuation gives v(y)=-m. Algebraic closure supplies the needed leading-unit root, and m invertible supplies Hensel uniqueness, so y^(-1)=z^m for a uniformizer z. For the selected generator, sigma(y)=y+1 implies sigma(z)^m=z^m/(1+z^m). The derivative of the characteristic-p action is one because its pth power is one and k has no nontrivial pth roots of unity. This singles out sigma(z)=z(1+z^m)^(-1/m), rather than an unspecified root differing by an mth root of unity.

Over R=W(k)[zeta_p], H=(1+Z^m)^(-1/m) is integral by the formal implicit-function argument: its defining equation has derivative m at H=1, a unit. An explicit coefficient recursion divides only by m. No inference from factorial denominators is needed. For alpha=zeta_p^a with am=1 modulo p, Sigma(Z)=alpha ZH induces U mapped to zeta_p U/(1+U). Its q-iterate formula, specialized to q=p, has denominator 1+S_p U=1. Thus Sigma^p(Z)^m=Z^m. The ratio Sigma^p(Z)/Z has constant one and is the unique mth root of one with that constant, so Sigma^p is the identity as a formal series. Its nontrivial reduction establishes exact order p. The origin is fixed and the linear coefficient is a unit, so the inverse power-series automorphism exists; the finite order supplies its explicit inverse iterate.

The norm product has reduction of exact order p. The quotient lemma applies both integrally and after reduction. Identification with the original specified action is through the constructed source coordinate isomorphism. A requested original invariant parameter is recovered by lifting its invertible change of parameter coefficientwise. This does not require a canonical multiplicative section of k into R.

Remaining gap: the classification by a single m and the one-parameter action do not extend to all cyclic p-power actions. The proof does not address the unknown orders or provide a new order-p-squared theorem.

## 6. Approach 2: fixed sections and the unmarked C3 lift

**Verdict: pass with Section 3's controlling qualification.**

For an origin-fixed characteristic-zero finite-order series with derivative one, the first nonzero nonlinear coefficient is multiplied by the number of iterations. Since the ring has characteristic zero, the iterate cannot be the identity. Therefore the derivative homomorphism is injective; a cyclic generator has derivative of exact group order. For q=p^n, the shifted cyclotomic polynomial has constant p, all nonleading coefficients divisible by p, and leading coefficient one. It is Eisenstein, giving cyclotomic ramification degree p^(n-1)(p-1). The divisibility conclusion applies when the coefficient ring contains the resulting root and is the relevant finite extension. It cannot be applied to an unmarked disc merely because fixed points appear after enlarging the field.

For the unmarked example, M=[[1,-3],[1,-2]] has determinant one and M^3=I, with neither earlier positive power scalar. Thus Sigma(Z)=(Z-3)/(Z-2) has exact order three and inverse Sigma^2(Z)=(2Z-3)/(Z-1). Its constant 3/2 lies in the maximal ideal and its derivative is a unit. Completeness of W(k) makes substitution legitimate; Z-adic continuity alone would not justify this nonzero constant.

The orbit product is T=Z(Z-3)(2Z-3)/((Z-2)(Z-1)); its reduction is z^3/(1-z^2). Its defining cubic has unit leading coefficient and is distinguished. The quotient lemma proves the invariant ring and finite freeness, not only a rational invariant identity. The reduced automorphism z/(1+z) is nonidentity of order three, so the special action is faithful.

The fixed points satisfy Z^2-3Z+3=0. Eisenstein implies their normalized 3-adic valuations are 1/2, so there is no W(k)-valued fixed section and W(k) contains no primitive cube root of unity. As an additional exact positive control, differentiation of the norm gives

T'(Z)=2(Z^2-3Z+3)^2 / ((Z-2)^2(Z-1)^2).

Its generic different has degree four; reduction also gives degree four. This independently corroborates smoothness of this particular lift and distinguishes it from the bad model below.

The example disproves only an extra necessity claim for every unmarked lift. It cannot disprove universal sufficiency of the larger cyclotomic ring: a lift over W(k) can itself be base changed there.

## 7. Approach 3: generic order versus faithful special reduction

**Verdict: pass as a failure diagnosis.**

Replacing p by q=p^n in the same formula gives exact generic order q: the qth iterate is the identity by the root-uniqueness argument, and the derivative alpha is a primitive qth root, excluding all smaller positive orders. After reduction, the U-action is U/(1+U), with jth iterate U/(1+jU). The Z-action also has pth iterate equal to the identity and has nonzero coefficient -j/m at Z^(m+1) for 0<j<p. Thus its reduced order is exactly p, not just a divisor of p.

For n>1, the norm product reduces to the p-orbit norm raised to p^(n-1). Its image defines a further purely inseparable power step; the invariant field of the reduced C_p action has degree p rather than q. The integral quotient lemma still gives a rank-q quotient upstairs, but its faithful-special-fiber clause cannot be used. This is a precise example of why generic group order alone is insufficient.

A compositum of order-p cyclic extensions, when formed independently over one common base, has Galois group embedded in a product of C_p groups and hence exponent p. It cannot furnish a cyclic p-squared tower. This statement does not exclude genuinely nontrivial sequential Witt-vector constructions; those carry terms and cyclic extension data remain necessary.

## 8. Approach 4: birational C3 model and different obstruction

**Verdict: pass; the normalization is not a smooth lift of the specified extension.**

Let lambda=zeta_3-1. Its relation lambda^2+3lambda+3=0 implies 3/lambda=-lambda-3 and 3/lambda^2=lambda+2. After W=1+lambda Y, the proposed equation becomes the stated monic cubic in Y. Localizing at (lambda) makes T a unit; completing there gives a complete coefficient DVR with residue k((t)). The reduced equation y^3-y=t^(-1) is irreducible because an Artin–Schreier coboundary with a pole has pole order divisible by three. Its derivative is -1. The displayed algebra is therefore the unramified degree-three DVR extension, with one residue field and ramification index one at this coefficient valuation.

The polynomial is irreducible after that completion and hence over the original fraction field. Since the constants contain zeta_3, the field extension is cyclic of degree three. The action on Y is Y mapped to zeta_3 Y+1 and reduces to y mapped to y+1.

The base R[[T]] is complete, Noetherian, and excellent. Its integral closure in this finite field extension is finite. It is local because a finite algebra over a complete local ring is a product of local algebras and this integral closure is a domain. Normality in dimension two gives Cohen–Macaulayness. There is one height-one prime over lambda, generically reduced by the unramified coefficient extension. Quotienting by the nonzero divisor lambda gives a Cohen–Macaulay one-dimensional ring with no embedded primes. Generic reducedness therefore gives reducedness; the unique minimal prime makes the quotient a domain. Its residue fraction field is exactly the desired Artin–Schreier extension, and its normalization is k[[z]]. This justifies the birational assertion, including the residue-domain condition, rather than assuming that an equation alone proves good reduction.

The three generic branch points are T=0 and the two zeros of T^2+lambda^3 T+lambda^4. Their nonzero discriminant is lambda^4(lambda^2-4). The Newton polygon has the single lower slope -2 in the normalization v(lambda)=1, so both roots lie strictly inside the open disc and have valuation two. The branch orders -2,1,1 are all prime to three. Each contributes 3-1 to the geometric different, totaling six. Splitting those geometric points for this computation makes no coefficient-descent assertion.

For the special extension, z=1/y is a uniformizer and t=z^3/(1-z^2). The derivative has exact order four. If a smooth model A=R[[Z]] existed with T=F(Z), its finite monogenic presentation would identify the different ideal with (F'(Z)). Reduction of F' has order four. Weierstrass preparation would factor F' into a distinguished polynomial of degree four times a unit. Its zeros in the generic open disc, with multiplicities, would therefore have total degree four. A unit in R[[Z]] has no zeros in that disc. This contradicts the computed degree six.

All prerequisites for this necessary-direction argument are present: complete coefficient ring, finite normalization, separable special extension, geometric generic branch count, and a hypothesized smooth source. Mere R-flatness is not used to infer smoothness. Conversely, the audit does not assume that an arbitrary equality of two sampled numbers proves smoothness without the full different-criterion hypotheses.

The 2026 isogeny results concern a smooth open group scheme and its unramified covers. A pole vector is not a morphism from the entire local disc into that open affine base. Smoothness is stable under an actual base change; this missing morphism and the ramified boundary cannot be supplied by the isogeny theorem alone. The example demonstrates this logical gap and is not a counterexample to that theorem or to the original universal lifting conjecture.

## 9. Approach 5: formal smoothness and coefficient descent

**Verdict: pass as a conditional criterion and a logical obstruction model.**

With the residue-compatible local R-algebra map understood, the map R/pi^(r+1) onto R/pi^r has square-zero kernel for every r>=1. Formal smoothness in the stated local infinitesimal category supplies a compatible lift at each stage. Their inverse limit is an R-algebra map to the complete ring R. Each map is local, hence the resulting map sends the maximal ideal of B into that of R and is continuous for the maximal-ideal topologies. The premise remains unproved for the general cyclic-action deformation chart. A point on a finite extension is not a replacement for this premise.

For B=R[[X]]/(X^r-pi), r>1, Weierstrass division gives finite freeness of rank r. Eisenstein irreducibility and the principal maximal ideal generated by X show that it is a DVR, finite and complete over R. It has its stated special point and point over the finite extension adjoining an rth root of pi. An R-point would require an integer-valued valuation satisfying r v(a)=1, impossible. Indeed the special point fails to lift already to R/pi^2: its possible image a lies in pi(R/pi^2), so a^r=0 while pi is nonzero. This stronger first-infinitesimal obstruction independently corroborates the argument.

This B is an abstract descent countermodel. Neither the frozen packet nor this audit identifies it with the deformation ring of a cyclic local action. The example therefore does not become a counterexample to prescribed cyclotomic lifting. Pop's bounded-different coefficient extension and Dang's equal-characteristic tower result leave the required R_n-valued point unestablished.

## 10. Independent exact checks, negative controls, and replay

The fresh `independent_controls.py` uses only the Python standard library and imports no author code. Its 1,987 checks include:

- coefficient-by-coefficient Hensel recursions, p-integrality, finite power-series compositions, exact reduced orders, leading terms, and two-sided inverses;
- cyclotomic quotient-ring matrix arithmetic for all proper iterates in the tested orders, plus the chosen linear coefficients;
- independent derivation of the C3 norm and its rational derivative factorization;
- lambda arithmetic, a nonzero bad-model discriminant, Newton polygon slopes, and the different mismatch;
- sampled elementary-abelian exponents and exhaustive modulo-p-squared descent checks within the stated finite ranges;
- the noncomplete-translation counterexample's coefficient recurrence.

The six mathematical negative/control families expose order loss under a changed Mobius constant, the excess different and its necessary-degree positive control, failure of descent modulo p squared, nonintegrality when m=p, the noncomplete translation failure, and reduction-order collapse. The full unrestricted versions are justified in the written arguments; the tests have explicitly finite coverage.

The author wrapper was run four ways: original normal, original optimized, relocated normal, and relocated optimized. Every wrapper internally runs both normal and optimized mathematics. Thus eight mathematical replays each reproduced the identical 6,527-check result, with all six author integrity controls exercised per wrapper. All four wrapper outputs were byte-identical. Fresh independent controls also produced byte-identical normal and optimized outputs matching the saved result.

Eleven independently created directory challenges were rejected both by the fresh binding checker and the optimized author wrapper: same-length payload corruption, missing payload, extra file, manifest byte change, payload symlink, wrong external pin, a self-consistent payload-plus-manifest rewrite under the old pin, missing manifest, manifest symlink, extra directory, and renamed payload. A twelfth challenge, an appended archive byte, was rejected by the independent archive guard. No execution from the changed archive was attempted.

These tests establish reproducibility and sensitivity within their scopes. They neither prove a universal mathematical assertion nor establish the historical correctness of every source-search narrative. No assertion-based test was allowed to disappear under Python optimization.

## 11. Final disposition and publication boundary

Retain the unsolved disposition and five-of-five approach count. Do not promote this packet as a complete solution, a general counterexample, a newly established theorem of universal sufficiency, or a globally exhaustive novelty/openness finding.

A presentation of the unchanged freeze must carry the qualification in Section 3. The standalone noncomplete translation wording is not approved unconditionally. A later corrected author packet would require a new manifest and explicit new binding; silently modifying the frozen author files is not permitted.

This audit package contains authored analysis, original verification code, deterministic outputs, public-source bibliographic verification metadata, and cryptographic bindings only. It excludes source PDFs, their text extracts and rendered images, dataset contents, raw source records, private sources, and private coordination files. No remote publication was performed by this audit.
