#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess

HERE=Path(__file__).resolve().parent
N=HERE.parent
clock_argv=["/bin/date","-u","+%Y-%m-%dT%H:%M:%SZ"]
clock=subprocess.run(clock_argv,capture_output=True,check=True)
utc=clock.stdout.decode().strip()
body=r'''# FIRST CANDIDATE ASSESSMENT - independent whole-preprint reviewer 02

Written UTC: {UTC}

## Status and exposure boundary

This is my first independent assessment, frozen before any verification ZIP, qualification object, supporting root report/gate, original PR mathematics, previous review, or agent status snippet. It is not a clean verdict, publication approval, or self-seal. I have not read the optional root source gate. The root's release message reported its external source-only check; that message is procedural permission, not proof of the candidate. The source-only baseline remains a prior statement of independent scope and standards.

The only newly exposed candidate files were the three expressly released files. They were copied with /bin/cp -p into phase2, and native shasum/stat receipts verify exact bytes and matching 0644 modes:

| Candidate input | Bytes | SHA-256 |
|---|---:|---|
| manuscript.tex | 22848 | 3338be58c5c6250a826f2a2af772db5a3838dad1d45c6c4a847c62cc00b4f9df |
| manuscript.pdf | 92256 | 0325be9bc4b754ad1d94baadf2f1b88af587e9443b9d242a2d7af7b2dda79420 |
| zenodo-deposit.json | 3244 | b4d99b620320f9a0a46eac60f9e61308cbc859364fadd632fd9976e9e942b863 |

I read the complete 482-line TeX, all seven physical PDF pages in order, their complete extracted text, and the entire JSON deposit metadata. Native pdfinfo counted seven pages before rendering; all seven full-page PNGs were visually inspected. No PDF/TeX discrepancy was found on that reading. The candidate's seven-page PDF is legible and has no observed clipped formula, obscured text, or broken table. That observation is visual QA, not proof that every formula agrees with an intended source or that the candidate compiles reproducibly.

Completion at this checkpoint: initial candidate-reading/claim-ledger stage 100%; complete requested independent paper/package audit 35%. The original problem's resolution is provisionally claimed by the candidate, not independently certified here. No external individual has been contacted, and no Git, publication, or tracker mutation was made.

## Comparison with the independently frozen original target

The source asks for the 5-torsion of the regular-pentagon quintic pencil. The candidate chooses an equation over K=Q(sqrt(5)), explicitly homogenizes the circle-square term by T, and chooses the smooth point [0:1:0] as origin. It purports to compute all 25 geometric points of the normalization's kernel, not only the five infinity points: a Tate model supplies four nonzero marked points, and a degree-ten residual polynomial with both ordinate branches supplies twenty more. It also claims the exact elliptic parameter domain, division field, Galois groups/action, and field-rational subgroups. If its proofs hold, this addresses the full natural characteristic-zero interpretation in the source-only baseline and adds arithmetic information.

The source's four remarks remain distinct. The candidate proves an infinity subgroup claim and discusses a quadratic twist/full-level modular description. It does not claim a Sha construction, local solubility, nontrivial torsor, nonregular polygon classification, or star-pentagon extension. It explicitly says those arithmetic/variant objectives are excluded and explains that this model already has a rational origin. Ellenberg's conference-connection question is not given an independent theorem-level answer; none is claimed. These scope qualifications are consistent with the manuscript title, abstract, and deposit description.

The candidate does not claim every plane fiber is smooth or nodal. It excludes finite lambda=0,-5sqrt(5),-phi^5 and the infinite member, and includes an allowed plane member with five cusps because its normalization is elliptic. It fixes scale instead of treating numerical lambda as coordinate-free. Field/origin choices resolve ambiguities left by the workshop statement. They do not establish a claim over Q, in characteristic 2 or 5, or for a different normalization of the pencil.

## Evidence labels used in the stable ledger

- **TEXT**: exact candidate claim identified by reading; not independently verified merely by identification.
- **ALG**: the displayed polynomial identity passed my independent exact standard-library Q(sqrt(5)) checker. This establishes that identity only, subject to the checker's transparent implementation; it does not establish every geometric inference drawn from it.
- **DED**: the indicated elementary consequence was independently checked at the conceptual level in this first read, conditional on the stated upstream model/field claims.
- **OPEN**: substantive verification remains, including actual cited-primary-source applicability, unchecked identities, geometry, or package claims.

Every ledger entry remains a claim to be tested in the complete audit. IDs are stable and will be retained even if a claim is withdrawn or repaired. Page locators below are physical PDF pages; equation numbers refer to the rendered candidate.

## Complete stable mathematical claim ledger

| ID | Location | Claim and its actual boundary | First-stage evidence / exact remaining obligation |
|---|---|---|---|
| C001 | pp.1-2, (1) | P is the scaled product of the five side lines of a regular unit-circle pentagon, over K, with the stated cyclotomic factors. | TEXT/OPEN: independently expand the cyclotomic product and verify consecutive vertices, scale, and K descent. |
| C002 | p.1 | Gamma=P+lambda*T*Q^2 is the specified projective pencil; T is degree-five homogenization; origin is [0:1:0]. | DED on degrees; origin's smoothness and map identification are C028. |
| C003 | pp.1-3, Thm.1, (2) | Geometrically integral genus-one normalization iff finite lambda avoids exactly 0,-5r,-c, for any characteristic-zero extension of K. | OPEN central geometric theorem; dependencies C011-C028 must cover every specialization. |
| C004 | pp.1-2, Thm.1 | On every allowed member the formulas give all 25 geometric fifth-torsion points. | OPEN main completeness claim; dependencies C029-C043 and C003. |
| C005 | p.2, (3) | For lambda in K, K(E_lambda[5])=K(delta,zeta,theta), theta^5=lambda+c. | OPEN central field claim; dependencies C044-C059. |
| C006 | p.2 | Degree is 4 iff lambda+c is a fifth power in K, otherwise 20. | DED conditional on C005,C055-C056 and Kummer input; field theorem still OPEN. |
| C007 | p.2 | Respective groups are C2 x C2 and D10 x C2 with D10 of order 10. | DED conditional field/disjointness proof; C057 still to verify. |
| C008 | p.2, (4) | No nonzero K-rational fifth-torsion point. | DED conditional on C005,C059; not certified before field equality. |
| C009 | p.2, (4) | K(delta)-rational fifth torsion is exactly the five infinity points. | DED conditional on geometric subgroup and real-field proof C042-C043,C060. |
| C010 | p.2 | Generic field over K(lambda) has degree twenty. | DED of non-fifth-power valuation, conditional on generic version of C005. |
| C011 | p.2 | Affine equation equals AY^4+BY^2+C for the displayed A,B,C. | TEXT; coefficients inspected; full coefficient comparison to (1) to run. |
| C012 | p.2, (5) | B^2-4AC=h^2(20X^2-aX+b), with displayed h,a,b. | ALG: exact cleared identity passes. |
| C013 | p.2, (5) | V,t give the conic field and X=(b-t^2)/(a+4rt). | DED formal conic parametrization plus ALG conic discriminant; degree-two/global consequences OPEN. |
| C014 | p.2, (6) | The displayed z,s,w substitutions give the two double-cover equations. | TEXT/OPEN: check rational identities independently, including canceled factors and dense-chart nonemptiness for each allowed lambda. |
| C015 | pp.2-3, (7) | Displayed a0,a1,a2,a3 are exactly the coefficients after the shift in F. | ALG: mF(s-alpha*lambda)=a0*s^3+a1*s^2+a2*s+a3 passes. |
| C016 | p.3, (8) | xi=a3/s, eta=xi*w give the monic cubic W. | DED algebra from C015 when a3 nonzero; full normalization is C003. |
| C017 | p.3, (9) | Displayed inverse formulas recover s,z,t,X,Y. | TEXT/OPEN: both compositions on the actual function fields, not an assumed selected component. |
| C018 | p.3 | b-t^2-X(a+4rt)=-4AG/h^2, and the reverse map recovers the same conic branch. | TEXT/OPEN: exact identity and branch/composition verification remain. |
| C019 | p.3 | Dense-chart maps extend uniquely between the smooth projective normalizations. | DED standard curve principle conditional on inverse function-field isomorphism and correct global source curve. |
| C020 | p.3, (10) | Four discriminant/branch identities hold; the two successive quadratic extensions imply irreducibility and genus one. | ALG: all four polynomial identities pass; OPEN: extension degrees, branch count at infinity/cancellation, and full curve inference. |
| C021 | p.3 | No vertical component: only A-root has displayed B value, and its extra B-zero has C=-1; quartic is primitive. | ALG: displayed B(X0) and exceptional C(X0) pass. DED of primitivity conditional on A,B,C correctly representing (1). |
| C022 | p.3 | Nonzero T=0 restriction rules out an extra line component at infinity; W normalizes the entire projective curve. | DED no T factor; whole normalization remains conditional on C011-C021. |
| C023 | p.3 | lambda=0 is the five side lines. | DED conditional on C001. |
| C024 | p.3 | lambda=-5r is a conjugate five-line product obtained by phi -> (1-r)/2. | TEXT/OPEN: exact coefficient comparison and distinct line factors. |
| C025 | p.3 | lambda=-c has nonsingular conic, exactly one double F-root, no triple root, stated gcd, and genus-zero normalization. | TEXT/OPEN: gcd, primitive/integral curve, square-free part, two odd branch points and absence of hidden extra component. |
| C026 | p.3 | Infinite pencil member is TQ^2=0. | DED homogeneous pencil boundary; no elliptic normalization is asserted for it. |
| C027 | p.3 | At lambda=-(25+10r)/4 all five vertex nodes become cusps, while normalization remains elliptic. | ALG local jet at (1,0): tangent=-25*v^2, kernel cubic=5*u^3. DED this lambda avoids all three exclusions (lambda+c=-3/4). OPEN complete five-vertex/global statement via verified rotation. |
| C028 | p.3 | Cubic origin maps to [0:1:0], valuation/order calculations and nonzero denominators hold; plane X-partial is ten. | TEXT/OPEN direct inverse limiting valuations, finite X value, and plane derivative; no origin identification assumed merely from notation. |
| C029 | p.4, (11)-(12) | beta,k,q parameter definitions and Tate discriminant are as displayed; beta gives nonsingular Tate curve on allowed domain. | TEXT; OPEN verify beta^5(beta^2-11beta-1) correspondence and no extra fiber exclusions. |
| C030 | p.4, (13)-(14) | Actual origin-preserving Tate-to-W equation isomorphism over K(delta), every allowed fiber including j=0,1728. | ALG cleared equation identity passes. DED scales nonzero away from lambda=-5r; OPEN origin/global and precise field interpretation. |
| C031 | p.4, (15) | Four displayed Tate points are nonzero multiples of P0=(0,0), with 2P0=(beta,beta^2), 3P0=(beta,0), exact order five. | TEXT/OPEN independently execute chord law and ensure nonzero beta/nonsingularity. |
| C032 | p.4 | Residual polynomial is Morton's D5 under b=-beta. | TEXT/OPEN primary Morton reading and every coefficient/version/sign comparison. |
| C033 | p.4, (16) | All eleven coefficient rows are the degree-ten residual factor. | ALG full coefficient identity with independently assembled psi5 passes. Its characterization as division polynomial depends on C035-C039. |
| C034 | p.4, (17) | Both ordinate signs solve the Tate equation at each residual root. | DED completing the square; distinctness requires C037-C040. |
| C035 | p.5 | Displayed psi3,H6,psi5=T^2*H6-psi3^3 are classical division polynomials and psi5=x(x-beta)R. | ALG factorization passes; OPEN independently derive recurrence/chord meaning, rather than assume the same formulas. |
| C036 | p.5 | Three displayed direct chord identities give an independent generic derivation. | TEXT/OPEN rational group-law derivation with every denominator tracked. |
| C037 | p.5 | Res(psi5,T)=Delta_beta^6 and Res(psi5,psi3)=Delta_beta^8. | TEXT/OPEN resultants, signs, leading constants, and no specialization loss. |
| C038 | p.5 | R(0)=5*beta^8 and R(beta)=5*beta^12. | ALG both exact polynomial evaluations pass. |
| C039 | p.5 | Nonzero finite psi5-roots are exactly fifth torsion; resultants justify chord denominators; equality x(2P)=x(3P) yields 3P=-2P. | DED group implication conditional on C035-C037; OPEN full converse/denominator proof. |
| C040 | pp.4-5, Lemma1 | [5] separable degree 25, twelve distinct nonzero abscissae; removing x=0,beta leaves ten simple roots and twenty distinct ordinate points, on every allowed fiber. | DED characteristic-zero elliptic kernel structure; OPEN cited theorem and linkage to candidate polynomial/model. |
| C041 | p.5 | No extra inverse-chart exclusion for twenty residual points; displayed identities show only marked abscissae can create poles. | TEXT/OPEN reproduce z+gamma*lambda and a+4rt identities; check all inverse denominators, including special parameters and singular plane images. |
| C042 | p.5 | Infinity slopes are 0,+/-sqrt(5+2r),+/-sqrt(5-2r), smooth and K(delta)-rational. | DED factor of homogeneous restriction and sqrt(5-2r)=r/delta; smoothness matches independently frozen baseline. Rotation correspondence still OPEN. |
| C043 | p.5 | Rotation preserves pencil, cycles infinities, induces order-five translation since Aut(E,O) has no element of order five; orbit is the marked subgroup. | DED elliptic automorphism argument conditional on genuine rotation/order and normalization; OPEN direct subgroup identification through maps. |
| C044 | p.5 | Over a field with zeta, choices Q with e5(P,Q)=zeta form a fine finite etale degree-five full-level cover, because marked order-five automorphisms are trivial. | DED count/freeness over smooth char-zero curves; OPEN actual Fisher statement and precise moduli base/marking/pairing convention. |
| C045 | p.5 | Fisher's full-level map is beta=tau*f/g with displayed f,g. | TEXT/OPEN actual cited map's convention and moduli interpretation; rational identity alone cannot certify it. |
| C046 | p.5, (18) | epsilon and iota involutions; tau*f/g=iota(epsilon^5) and iota(beta)=-1/(lambda+c). | ALG displayed rational cross identities pass; DED involutions from their matrix squares. |
| C047 | pp.5-6 | u^5=-1/(lambda+c) is exactly that cover, including every allowed split/nonsplit and exceptional-j specialization by normalization/finite-etale uniqueness. | OPEN central cited/geometric specialization step; check shared generic cover, identical normal base and finite-etale extension, not only matching fractions. |
| C048 | p.6 | u=-1/theta gives same radical field, with Kummer class inverse rather than falsely equal fixed class. | DED exact fifth-power relation and inversion; correctly states convention. |
| C049 | p.6 | Morton's radical becomes c*(lambda+c), so u_M=phi*theta. | ALG displayed fraction transformation passes; OPEN actual Morton input/version. |
| C050 | p.6 | Verdure's iff full-torsion criterion on all nonsingular specializations is (beta-c)/(beta+c^-1) fifth power; this equals -c*(lambda+c). | ALG displayed ratio identity passes; OPEN primary theorem hypotheses, curve/sign conventions, exceptional values and claimed universal scope. |
| C051 | p.6 | With zeta and marked P, extension degree one/five and Verdure criterion prove exact K(D_beta[5])=K(zeta,theta), not merely inclusion. | DED representation/degrees conditional on the actual universal iff criterion; central external input unverified here. |
| C052 | p.6 | L(E[5])=L(theta) both directions through a basis/cover point and Tate isomorphism. | OPEN on C030,C044-C051; no generic-only inference is accepted without specialization justification. |
| C053 | p.6 | Image of P0 has xi=-q*beta and eta=-k^3*d*delta*beta/2 with nonzero K coefficient, forcing delta into full field. | DED substitution and lambda exclusions conditional P0 exact order; verify nonvanishing and coordinate field intrinsic meaning. |
| C054 | p.6 | Nondegenerate Weil pairing forces zeta into full torsion field, so it contains L and C005 follows. | DED characteristic-zero Galois-equivariant pairing conditional full elliptic kernel; cited theorem to verify. |
| C055 | p.6 | M=K(delta) quadratic by Norm(d)=5; M real, K(zeta)/K imaginary quadratic, so [L:K]=4. | DED elementary norm and real/imaginary argument independently checked; base fields/embedding fixed. |
| C056 | p.6 | A K-element becomes fifth power in L iff already one in K, using norm degree four. | DED explicit identity (a/N(v))^5=a independently checked. |
| C057 | p.6 | Nonsplit K(zeta,theta)/K is D10 with unique quadratic K(zeta), disjoint from M; split case gives C2xC2 after adjoining delta. | DED standard Kummer/dihedral structure conditional field equality and degree 5; verify chosen real root and all negative a. |
| C058 | p.6 | Generic lambda+c has valuation one at -c, giving non-fifth-power generic field and degree twenty. | DED valuation is checkable; generic cover identity still conditional. |
| C059 | p.6 | Independent delta sign involution fixing Tate field acts as -I, yielding zero K-rational fifth torsion. | DED from eta scale sign once independence/field equality is proved. |
| C060 | p.6 | E(R)[5] has exactly five points; real M contains marked subgroup, so M-rational fifth torsion is exactly it. | DED odd-order real elliptic torsion argument, conditional known M subgroup and chosen real embedding. |
| C061 | p.6 | With explicitly adjustable basis/generators, Galois matrices are -I, diag(1,-1), and [[1,1],[0,1]], omitting transvection in split case. | DED expected conjugation/transvection structure; OPEN exact actions and compatibility with declared infinity generator and chosen primitive root. |

## Complete source, provenance, disclosure, and metadata ledger

| ID | Location | Claim / boundary | First-stage assessment |
|---|---|---|---|
| S001 | pp.1,7 | Source Question17 attributed to McCallum, known infinity subgroup credited; 2002 workshop and 2004 version/p.51 identified. | Matches independently retrieved original source and all four remarks. The source itself contains no proof of its genus/torsion assertions. |
| S002 | p.2; JSON description | No Sha/local-solubility construction or nonregular/star variant solved; this model has rational origin. | Accurately delimits the stated theorem and original remarks. |
| S003 | pp.1,7; JSON | No first-priority claim; contribution is explicit bridge to classical family and resulting full computation. | TEXT verified; actual novelty/remaining originality not certified. Absence of priority claim does not substitute for correct prior-attribution comparison. |
| S004 | pp.1,6,7; refs | Fisher, Verdure, Morton, division theory and pairing are credited; Morton residual/radical prior to current note, v4 operative, v1 earlier. | TEXT verified; primary references and page/version matches remain OPEN, particularly Verdure all-specialization scope and Fisher full-level convention. |
| S005 | p.7; JSON | Earlier repository partial infinity/quotient work acknowledged as input. | TEXT verified; identity, exact scope, authorship and historical correctness unavailable in this phase. |
| S006 | pp.6-7; JSON | Supplement has symbolic/chord checks, independent finite group enumeration, arithmetic controls, mutants, dependencies/outputs/sources, and a bounded priority audit. | Entirely OPEN; supplement deliberately unread. Cannot infer reproducibility or audit quality from assertions about it. |
| S007 | p.7; JSON | Finite tests are falsifiable implementation checks, not proof by sampling; no absence-of-hits argument establishes discovery/openness. | Appropriate stated standard; actual supplement practice OPEN. |
| S008 | abstract,p.7; JSON | Extensive AI use in derivation, computation, literature, writing/reproduction/review; author responsibility; unrefereed; no external human peer review or proof-assistant certification claimed. | TEXT consistent in all released outputs. Actual history not independently reconstructed here; no automatic review treated as mathematical evidence. |
| S009 | title/p.1; JSON | Author Alec Kriebel, independent-researcher affiliation, ORCID 0009-0001-9320-500X, date 2026-10-04. | Agrees with AGENTS.md author identifier and current date. No unsupported coauthor/reviewer identity is stated. |
| M001 | deposit JSON | Title, description, preprint type, open access, CC-BY-4.0, version1.0 and publication date accompany creator metadata. | Structural fields/values read completely. Scope and formula descriptions match manuscript. No live Zenodo API validation/deposit/publication performed or claimed. |
| M002 | deposit JSON files | Intended files are pentagonal-torsion-note.pdf and pentagonal-torsion-verification.zip. | These are intended upload names, not present-copy filenames. Actual mapping, contents, hashes, ZIP safety/metadata and license packaging OPEN until full release. |
| M003 | deposit related identifiers | DOI/URL references include Fisher, AIM, Morton, Verdure and Morton v1. | Links agree textually with manuscript bibliography; DOI resolution, primary content, dates and bibliographic exactness OPEN. Omission of Sutherland from related identifiers is not a mathematical contradiction. |
| M004 | deposit description | Covers every elliptic normalization, cuspidal member, full field/splitting/Galois, portable supplement and prior credits; excludes variants/Sha. | Matches theorem's advertised scope, so inherits all pending proof/package obligations rather than being independently verified by agreement. |

## First-read findings and exact unresolved gaps

No definitive mathematical counterexample was found in this restricted first reading. That is not a cleanliness verdict. Selected formal identities pass an independently written checker; the principal geometric and arithmetic conclusions remain conditional on the complete proof chain and actual cited inputs. The manuscript is materially stronger than merely displaying an infinity orbit: it explicitly supplies a residual division polynomial, twists rather than only compares j, gives a primitive-quartic argument, and states a finite-etale/all-specialization justification. These are claims to audit, not accepted answers because they are present in prose.

The most important unresolved mathematical obligations are:

1. **C003/C014/C017-C025: global normalization at all parameters.** Verify the two quadratic extensions really have degrees two, that rational identities do not lose a component, and that every canceled denominator/chart pole is handled on the actual normalization. Independently derive the genus-zero excluded member, line-product member and all-plane cusp statement. The already verified primitivity identities close an obvious vertical-component route, but do not alone prove every branch/genus inference.
2. **C004/C035-C043: full kernel and coordinate coverage.** Independently derive the chord identities/recurrence, recompute resultants and show the polynomial iff argument without circularly importing a full division-polynomial conclusion. Check origin preservation and identify the Tate marked subgroup with infinity points, not just two unrelated five-point subgroups. Check the inverse denominators universally. At singular plane vertices, distinct normalization points may share a plane image; any coordinate presentation must be understood on W/normalization rather than silently counted as distinct plane coordinates.
3. **C005/C044-C052: exact extension and specialization.** Actual Fisher and Verdure primary statements have not been read in this phase. A fractional identity identifying a degree-five algebraic cover is insufficient by itself to label it the torsion-basis cover. Conversely, if the stated Verdure universal iff theorem applies exactly to this sign convention, the unipotent degree-one/five argument is a meaningful independent route to equality. Both routes need primary-source hypotheses and all-specialization verification. This is the central presently unverified imported machinery, rather than a claim shown false or unsupported by the eventual complete record.
4. **C053-C061: arithmetic field/group action.** Norm descent is correct as written, and the proposed real/imaginary disjointness mechanism is coherent. Still verify all field containments, split/nonsplit examples, negative fifth-root values, Galois action/basis conventions, and CM specializations against the exact field result. Do not transfer a generic irreducibility statement to every fiber.
5. **S003-S007/M002-M004: attribution, reproducibility and public claims.** The candidate responsibly narrows priority and discloses extensive AI use, but actual prior sources, supplement receipts/coverage, earlier input attribution, licenses, package mapping and emitted outputs remain unopened. A complete priority audit must test the specific bridge contribution against earlier work, not merely confirm that the universal Tate ingredients were already known.

No new scientific assumptions about char2/char5, Q-rationality, torsors/Sha, arbitrary polygons, or scale-independent lambda are introduced. The arithmetic theorem is only for lambda in K (plus its generic K(lambda) statement), while the geometric 25-point formula is stated after algebraic closure for allowed finite lambda in any characteristic-zero extension of K. Metadata's abbreviated description should be read with that theorem boundary; it does not justify extending the degree-four/twenty claim to all larger coefficient fields.

## Independent checks actually executed, including failures

The exact initial checker is phase2/independent_initial_exact_checks.py. It uses only Python standard-library Fraction arithmetic, Q(sqrt(5)) represented by pairs, and sparse bivariate polynomials. It was written from the released equations without reading supplement code. The successful native receipt is phase2/native_receipts/independent_initial_exact_checks_v02.json and its complete .stdout/.stderr streams.

It checks sixteen zero polynomial differences: quartic discriminant factor, conic discriminant, vertical-component B and exceptional C values, F(-alpha*lambda), F discriminant, shifted-F coefficients, W discriminant, cleared Tate-twist identity, iota(beta), Morton radical transform, Verdure radical transform, displayed Fisher fractional identity, all eleven residual coefficients, and both marked residual evaluations. It also checks the exact cusp local jet at (1,0). These are universal polynomial identities over Q(sqrt(5)), not numeric samples. It explicitly prints its limits; it does not certify any cited theorem, full normalization, resultants, division-kernel interpretation, all-fiber field theorem, priority, or package.

Contemporaneously preserved failures: bundled-Python import of sympy failed at 2026-10-04T12:17:45Z, system-Python import failed at 12:17:52Z; both native error streams and exit1 receipts remain. No library was installed. The first exact checker failed at 12:20:09Z because its scalar Q5 addition did not dispatch polynomial operands. Before fixing that implementation bug, the exact failed program was preserved as independent_initial_exact_checks.failed_v01.py with a real native cp receipt at 12:20:32Z. The corrected checker completed at 12:20:32Z with exit0 and empty stderr. These are reviewer implementation/dependency failures, not candidate mathematical counterexamples. No timestamp was retrospectively invented.

## Adversarial strategy for the full release

The following distinct families use the stable IDs and frozen independent source baseline. They will not accept a shared pivotal claim merely because another reviewer or a package reports PASS.

| Family | Mechanism and falsifiable checks | Current evidence / exact gap |
|---|---|---|
| Projective/local geometry | Independently expand side product; derive full birational map and singular/branch loci; exact specialize at 0,-5r,-c,cusp,a=0,vertical exception and every map-denominator event. Challenge integral/smooth-normalization claims with full factorization and branch valuations. | Selected identities and one cusp jet pass; C001,C003,C014,C017-C028 not closed. |
| Intrinsic divisors/group law | Compute infinity translation action and divisor classes; verify origin and distinguish marked subgroup from orbit; derive actual [5] identities and kernels with group law. | C028,C031,C036-C043 OPEN beyond conditional conceptual checks. |
| Exact polynomial/computation | Rebuild division-polynomial factor/resultants independently; then enumerate finite groups without using candidate division polynomial as the oracle. Compare all coefficients, both signs, all edge charts and actual outputs. | Residual coefficient identity passes; resultants and independent kernel enumeration not done. |
| Moduli/Kummer specialization | Read Fisher/Verdure/Morton primary sources independently, compare every sign/parameter/marking, identify fine cover as basis choices, prove normalization/finite-etale equivalence across the entire base. Seek a valid fiber contradicting field equality or source-hypothesis application. | Formal transformations pass; C044-C052 central external premise unverified. |
| Arithmetic/Galois | Check degrees, disjointness, fifth-power descent and explicit split/nonsplit/negative-a controls, complex conjugation and transvection matrices, exceptional j; avoid testing only semisimplification. | Norm/disjointness mechanism coherent; exact field dependence remains. |
| Source/priority/disclosure | Independently retrieve actual cited sources with native receipts, verify operative versions/theorems; compare bridge against prior work. Audit historical limitations separately from current deductions; require honest reporting of actual AI/automated review scope. | AIM source independently verified; other citations and priority history unavailable. |
| Package/publication consistency | Inspect safely only after release; rebuild expected mathematical outputs, test deliberate mutants and coverage; inspect metadata/file mapping, licenses, code/proof/output consistency and contents. Failures remain preserved. | All package claims S006/M002 OPEN; metadata wording matches current paper scope. |

A route is blocked if it merely renames the central unproved assertion or relies on equivalent unsupported machinery. It may reopen only with a materially new mechanism or evidence. No such route is being promoted here as a proof. The complete audit will distinguish elementary deductions, algebra certificates, external theorem applicability, reproducibility checks, historical/procedural limitations, and unresolved gaps.

## Held conclusion

This first independent reading produces a complete stable ledger, a scope comparison, an adversarial strategy, selected successful exact algebra checks, and preserved real failures. It does not approve the main theorem or publication. The next action is a complete namespace freeze, followed by HOLD until root external validation and an explicit full-packet release. Existing source-only evidence is preserved; the root research log is append-only, and its exact source-only prefix is separately retained in phase2/source_only_log_prefix.md.
'''
(N/"FIRST_CANDIDATE_ASSESSMENT.md").write_text(body.replace("{UTC}",utc))
with (N/"RESEARCH_LOG.md").open("a") as log:
    log.write(f"\n- {utc}: First-candidate assessment written after complete TeX, seven-page PDF, and deposit metadata reading. Exact released bytes/modes preserved. Stable ledger C001-C061, S001-S009, M001-M004; sixteen selected exact identities and one cusp jet passed an independently written standard-library checker. Two missing-library failures and the first checker failure are preserved with actual native clocks/program/streams. Initial-reading stage 100%; complete requested audit 35%; original-problem resolution not independently certified. No ZIP/qualification/supporting gates/previous reviews/PR math exposure. Pending freeze and HOLD for full-packet release; no clean verdict or publication approval.\n")
(HERE/"assessment_write_clock.json").write_text(json.dumps({"argv":clock_argv,"utc":utc,"stdout":clock.stdout.decode(),"stderr":clock.stderr.decode(),"exit_status":clock.returncode},indent=2)+"\n")
print(json.dumps({"written_utc":utc,"assessment":"FIRST_CANDIDATE_ASSESSMENT.md","initial_stage_complete_percent":100,"complete_requested_audit_percent":35},indent=2))
