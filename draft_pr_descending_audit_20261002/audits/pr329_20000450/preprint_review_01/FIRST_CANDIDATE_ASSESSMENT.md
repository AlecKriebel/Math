# First-candidate assessment freeze: exactly three released inputs

This assessment precedes archive, supplement, qualification contents, root
mathematical/priority gates, inherited author reviews, and original-PR
scientific files. None has been opened. It preserves the independent
SOURCE_ONLY_BASELINE unchanged. This is an initial inventory and falsification
plan, not a scientific verdict, seal or publication clearance.

## Exact input pins and complete reading

The acquisition at native UTC 2026-10-04T11:01:59Z copied only the released
manuscript.tex, manuscript.pdf and zenodo-deposit.json. The source bytes were
read before/after copying and matched the own-folder copies. Pins are in
`evidence/candidate_stage1/exact_three_input_pins.json`; the native acquisition
stdout/stderr/argv/time evidence is `acquire_01.*`.

| Input | Bytes | SHA256 |
|---|---:|---|
| manuscript.tex | 22852 | d29598eca6bcee12d498dfe6bed5a91112bc89acc217ead458e91c655a170dd4 |
| manuscript.pdf | 92263 | 791b06f03f93586e66ca6e150a4f6b5b2d4ea2e02ef036c83f9d4fdb7d27a23a |
| zenodo-deposit.json | 3244 | b4d99b620320f9a0a46eac60f9e61308cbc859364fadd632fd9976e9e942b863 |

I read the entire 482-line TeX source, complete seven-page PDF text, all seven
rendered pages, and complete deposit JSON. Extraction/render native records
are retained. The PDF's visible equations, proof structure, tables, boundaries
and six references agree with the source on this inspection. No clipped text, unreadable mathematical table, broken citation, or visible missing page was
seen. The mathematical accuracy of the render is distinct from formula proof.

## Complete body/definition/theorem claim inventory

Locations below are lines of the own-copy TeX. Every section of the body,
including its front matter and research-status statements, is covered. A row
can contain several tightly connected equalities, all of which must be tested.
Unless explicitly stated, these claims are not yet independently verified.

| ID | Location | Exact claim or definition to review | Mode / main obligation |
|---|---|---|---|
| F01 | 15-38 | Title, author/ORCID/date; abstract asserts full 25-point computation, maps, residual table, exact field, degree 4/20, all elliptic fibers including cusp, credited classical method and reproducible supplement | Metadata and theorem-summary consistency |
| S01 | 40-59 | Source Q17 is the side-line/circle normalization; infinity subgroup is already known; parameter scaling fixed; no priority claim; Verdure/Morton already supply universal criterion and nonmarked Tate torsion; bridge to this plane family is the contribution | Source/attribution/novelty, primary source needed |
| D01 | 61-70 | r=sqrt(5), K=Q(r), phi=(1+r)/2, c=phi^5=(11+5r)/2, d=5+2r, delta^2=d; Q=X^2+Y^2-T^2; displayed quintic P; Gamma=P+lambda TQ^2; E is normalization with O=[0:1:0] | Definitions, scaling, origin convention |
| T01 | 72-77 | For finite lambda over any char-0 extension of K, whole member has geometrically integral genus-1 normalization iff lambda excludes 0,-5r,-c | Global all-fiber geometry, not just selected component |
| T02 | 78-80 | Tate map, ten-root table and both ordinates, four marked points and O compute all 25 geometric 5-torsion points on every allowed member | Completeness and specialization |
| T03 | 80-86 | For allowed lambda in K, K(E[5])=K(delta,zeta,theta), theta^5=lambda+c | Exact upper and lower field inclusions |
| T04 | 87-90 | Degree4 iff lambda+c is a fifth power in K, otherwise20; groups C2xC2 / D10xC2 with D10 order10 | Kummer specialization and intersections |
| T05 | 90-95 | E(K)[5]=0; E(K(delta))[5]=Z/5 is exactly infinity subgroup; generic K(lambda) field degree20 | Rational subgroup and generic exact field |
| S02 | 97-101 | No Sha/local/star/nonregular construction asserted; model has rational O | Source-scope exclusions, no arithmetic overclaim |
| G01 | 104-114 | In Z=X+iY,W=X-iY, five displayed linear factors through successive unit-circle vertices multiply exactly to P; regular pentagon scaling | Independent factorization and real geometry |
| D02 | 116-132 | A,B,C quartic coefficients; h,a,b,V,t,X formula; alpha,gamma,m,z,s,w and cubic F(z) definitions | Exact formulas and domains |
| G02 | 123-125 | B^2-4AC=h^2(20X^2-aX+b) and X=(b-t^2)/(a+4rt) | Algebraic identity and conic branch |
| G03 | 133-139 | Y^2=m z^2 F(z)/(400(z+gamma lambda)^2(z+alpha lambda)); w^2=mF(s-alpha lambda)/s | Double-cover identity and lost factors |
| D03 | 140-146 | a0..a3 displayed; xi=a3/s, eta=xi w; monic cubic eta^2=xi^3+a2 xi^2+a1 a3 xi+a0 a3^2; explicit inverse s,z,t,X,Y | Exact coefficient and map definitions |
| B01 | 149-158 | Function-field maps inverse; b-t^2-X(a+4rt)=-4AG/h^2; Y cancels; reverse cubic recovers branch; poles extend uniquely on smooth models | Both compositions, nonempty charts, origin/branch |
| G04 | 160-168 | Four discriminant/evaluation identities: a^2-80b, F(-alpha lambda), disc(F), Delta_W with precise constants and powers | Exact symbolic identity, normalization factors |
| G05 | 169-175 | Conic sqrt nontrivial outside0,-5r; field rational in t; four odd branch points outside exclusions; quartic irreducible in kbar(X), genus1 | Field degree4 argument and Riemann-Hurwitz |
| G06 | 177-188 | A root X0; B(X0) exact factorization; only additional possible common root at lambda=-5(phi+1) gives X0=1/2,C=-1; primitive quartic; no T component; whole curve geometrically integral | Vertical-component adversary and Gauss lemma |
| G07 | 190-198 | lambda0 and -5r are five lines (conjugate phi); -c gives exactly one double/no triple F root, gcd s-1-3r/5, genus0; infinity TQ^2; cusp lambda=-(25+10r)/4 is elliptic | Boundary negative controls and cusp local type |
| B02 | 200-205 | Cubic O has ord xi=-2,eta=-3; inverse Y simple pole/X finite; denominators nonzero; X=-(5phi+lambda)/10; image O plane smooth with X partial10 | Origin compatibility |
| D04 | 208-217 | beta=(11-5r)lambda/(2(lambda+5r)), k=4(lambda+5r)/r, q=dk^2; Tate equation and Delta_beta=beta^5(beta^2-11beta-1) | Exact change of family and sign conventions |
| B03 | 218-231 | xi=q(x-beta), eta=(k delta)^3(y+((1-beta)x-beta)/2) gives origin-preserving isomorphism over K(delta) on every allowed fiber; cubic RHS=q^3 T_beta/4; no j0/1728 exclusion | True twist, not j-match; nonsingular locus equivalence |
| T06 | 233-239 | Four marked coordinates; P0=(0,0), tangent horizontal,2P0=(beta,beta^2),3P0=(beta,0)=-2P0; exact order5 | Independent generalized group law |
| D05 | 241-264 | Degree-ten residual coefficients r10..r0; equal Morton D5 with b=-beta; both ordinate signs; mapping instructions | Every coefficient, ordinate identity, prior formula |
| L01 | 266-270 | Lemma1: ten simple roots and two distinct signs give exactly twenty outside marked subgroup on every allowed fiber | Separate count/order/completeness proof |
| T07 | 272-289 | b2,b4,b6,b8; psi3,H6,psi5=T_beta^2 H6-psi3^3=x(x-beta)R; three direct chord identities; exact resultants Delta^6/Delta^8 and R(0),R(beta) | Own chord derivation, coefficients, resultants |
| T08 | 291-300 | Nonzero resultants justify chord denominators; x2=x3 implies3P=-2P; converse; [5] separable degree25; 24 nonzero points pair to12 simple abscissae; signs distinct and twenty remain | Logical completeness and cited isogeny theorem |
| B04 | 303-310 | z+gamma lambda=(gamma-alpha)lambda x/(x-beta), a+4rt=4r(z+gamma lambda); only excluded inverse-chart abscissae0,beta; none residual | Plane-coordinate coverage of all twenty |
| T09 | 310-317 | Infinity slopes0,+/-sqrt(5+2r),+/-sqrt(5-2r), all smooth; rotation preserves/cycles; order5 translation; exactly subgroup T05 | Independent infinity check; source baseline not novelty |
| M01 | 320-327 | zeta chosen1+zeta+zeta^-1=phi; five complementary vectors for fixed Weil pairing; finite etale degree5 full-level cover over cusp complement; automorphism fixing order>=4 point trivial/fine | Fine moduli hypotheses and actual cover |
| M02 | 328-341 | Fisher cover beta=tau f/g with stated f,g; epsilon/iota involutions; tau f/g=iota(epsilon^5), iota(beta)=-1/(lambda+c) | Exact identities plus primary cover attribution |
| M03 | 342-349 | Full-level cover u^5=-1/(lambda+c); every smooth specialization determined by equal normal finite-etale function-field cover; split and exceptional-j fibers included | Central all-specialization bridge |
| M04 | 351-359 | u=-1/theta; fields coincide; Kummer fixed classes inverse, not equal; Morton uM^5=c(lambda+c),uM=phi theta; old universal mechanism | Inversion, conventions, literature formula |
| M05 | 361-376 | Verdure criterion over char0 field containing zeta iff(beta-c)/(beta+c^-1) fifth power; quotient=-c(lambda+c)=(-phi theta)^5; all nonsingular specialization; torsion field degree1/5; exact K(D[5])=K(zeta,theta) | Read full primary proof and base-field assumptions |
| A01 | 378-389 | L=K(delta,zeta); L(E[5])=L(theta) both ways; mapped P0 eta=-k^3d delta beta/2 with nonzero K coefficient forces delta; Weil pairing forces zeta; exact field | Lower inclusion and pairing, no circularity |
| A02 | 391-397 | Norm(d)=5 implies M quadratic; M real, K(zeta) imaginary quadratic, L/K degree4; norm descent v^5=a proves fifth-power criterion unchanged in L | Elementary independent field proof |
| A03 | 397-403 | Nonsplit K(zeta,theta)/K=D10,unique quadratic K(zeta); distinct M gives product group; valuation1 at lambda=-c gives generic degree20 | Irreducibility/normality and field intersection |
| A04 | 405-419 | Independent delta involution acts-I, eliminates K-rational5 torsion; M real gives only5 real5-torsion; basis choices produce -I,diag(1,-1),nonzero transvection; split omits transvection | Exact Galois representation and basis scope |
| C01 | 421-430 | Package has exact symbolic geometry/chord checks, independent finite-field enumeration, field controls, mutants; all-fiber proof not sampling; standard-library arithmetic portability; dependencies/outputs/references; no third-party primary PDF redistribution | Not yet inspectable package/replay claims |
| S03 | 432-442 | Known ingredients and previous partial input credited; bounded priority audit records actual limits, no first-discovery/openness certification | Read audit only after release; attribution evidence |
| F02 | 444-450 | Extensive AI use, author responsibility, unrefereed, automated reviews not external human peer review, no formal certification | Disclosure and consistency |
| R01 | 452-458 | AIM title/date/version/Q17 physical51 URL | Verified original independently |
| R02 | 459-461 | Fisher 2001 JEMS3,169-201, DOI10.1007/s100970100030 and precise in-body cites | Native independent primary retrieval required |
| R03 | 462-465 | Verdure 2006 IJPAM33(1),75-92,Thm5 pp84-88,URL | Native independent primary retrieval required |
| R04 | 466-473 | Morton JNT200(2019),380-396 DOI; operative v4 June11,2018; table/radical already v1 Dec19,2016 pp3-5 | Retrieve both primary versions and verify dates/pages |
| R05 | 474-477 | Sutherland lecture5 September26,2023 secs5.5-5.6 URL | Primary theorem/version/date check |
| R06 | 478-480 | Sutherland lecture23 December5,2023 sec23.5 URL,Thm23.29 in body | Primary theorem/version/date check |

## Deposit metadata claims

The JSON is valid on initial reading, and its title, author, ORCID, affiliation,
date, abstract-level theorem summary, scope exclusions, old-ingredient credits,
AI/unrefereed disclosure and no-priority statement agree with the paper. The
deposit declares open access, CC-BY-4.0, version1.0, publication/preprint type,
six topic keywords, references to Fisher/AIM/Morton/Verdure/Morton-v1, and two
file paths: pentagonal-torsion-note.pdf and pentagonal-torsion-verification.zip.
The actual presence, matching bytes, licensing consistency and archive
contents are gated and remain unverified. The metadata is a deposit plan,
not evidence of an actual DOI or publication event. The absence of Sutherland
related-identifiers is not itself a missing paper citation: both lectures are
in the manuscript bibliography.

## Assumptions and exact boundary inventory

Central geometric claims assume a nondegenerate regular unit-circle pentagon,
the displayed fixed P/C scaling, finite lambda, characteristic zero and an
extension containing K. Arithmetic degree/group/subgroup assertions specialize
to lambda in K; the generic degree claim uses K(lambda). The origin is an
explicit K-point on the normalization. The split test excludes a=0 through
lambda=-c. beta=0 and lambda=-5r are excluded; smoothness also excludes the
two nonzero roots of the Tate discriminant, one achieved at -c and the other
at the missing infinite lambda parameter. Formula charts are dense opens,
with smooth-normalization extensions at poles. Every exceptional factor must
be rederived rather than assumed from the displayed exclusions.

Frozen controls: lambda=0,-5r,-c,infinity; lambda=-5(phi+1) for hidden vertical
components; lambda=-(25+10r)/4 for allowed cusp; special j0/1728; split
lambda+c fifth power and nonsplit values; signs/choice of delta/zeta/theta;
Kummer inverse class; h=0,A=0,z=0,s=0,xi=0,x=0,x=beta and all map
denominators; repeated residual roots and zero ordinate square-root; rational
versus geometric torsion; base-extension norm argument; omitted
nonregular/star/Sha/local-construction variants; finite-field reductions where
p=2,5 or bad discriminant are outside their sensible control domain.

## Independent falsification families after full release

1. Rebuild the real pentagon side product from vertices without importing
   package polynomial definitions. Reconstruct quartic, conic and field-degree
   proof, then test vertical and projective components. Recompute all four
   discriminants and the excluded genus0 fiber. Derive a local cusp tangent
   cone and next nonzero term rather than inferring cusps from smooth cubic.
2. Compose forward/inverse maps as rational functions modulo the independently
   reconstructed equations; track every cancelled factor. Prove origin and
   inverse-chart coverage independently. Deliberately perturb a coefficient
   or map sign to ensure the tests do reject incorrect maps.
3. Derive psi5 from a generalized Weierstrass group law rather than invoking
   imported psi5 or supplied assertions; independently compare all eleven
   residual coefficients and both resultant constants. Enumerate full torsion
   over selected finite fields with a separate group law and negative controls.
4. Verify the exact quadratic twist identity including delta's sign/power.
   Inspect all-field smoothness equivalence, j0/1728 and cusp controls.
5. Retrieve Fisher, Verdure, both Morton versions and both MIT lectures
   independently with complete native logs and failed attempts retained.
   Read cited theorem context/proofs, not inherited excerpts. Independently
   decide whether each supports the claimed full-level field and every smooth
   specialization, and check the asserted chronology and exact table signs.
6. Derive Kummer transforms and the norm/intersection/group argument from
   scratch. Check lower field inclusion, matrices and rational subgroups;
   use independent standard-library finite-field controls for split/nonsplit
   behavior without treating reductions as proof in characteristic zero.
7. After inventory of all released archive payloads, read every mathematical,
   computational, provenance, priority, dependency and packaging claim;
   replay scripts from own copies with native UTC clocks and complete actual
   streams. Compare assertions with obtained outputs, run mutants and test
   portability without any package installation. Retain failures.
8. Cross-check PDF/TeX/README/deposit/CITATION/license/manifests/expected outputs
   and stated boundaries, versions, file names and byte hashes. Imported
   author/root reviews may be examined as claims or historical provenance
   after release, never used as independent mathematical validation.

## Plausible failures and first-reading assessment

The strongest potential blocker is a mismatch between the actual primary
full-level cover/specialization hypotheses and M01-M05. A generic rational
identity cannot by itself establish the exact field on every fiber. The
candidate supplies a finite-etale normalization argument and a second cited
specialization theorem, both requiring direct verification.

Other concrete risks are a lost affine/projective component despite the
function-field map, a cusp label with a different local singularity, a wrong
division-polynomial coefficient or resultant constant, a cancelled chart
factor hiding a claimed torsion point, an arithmetic field intersection or
Galois-matrix assumption that fails on split fibers, bibliography pinpoint or
chronology errors, and archive portability/provenance statements broader than
their native evidence. Each has an independent check planned above.

On first reading, the paper's scope agrees with the original main question:
it acknowledges the known infinity subgroup and targets the additional twenty
points. Its characteristic-zero and explicit-origin conventions avoid the
source's torsor ambiguity. It explicitly excludes the remarks' open-ended
shape/Sha/local extensions and makes no first-priority claim. The body appears
internally coherent; this is not verification. No blocker is yet established,
and no inherited output has been relied upon. The finite-field and package
claims, primary citations, exact formulas and universal proof steps remain
open obligations.

## Freeze and gating

The complete own first-candidate bodies/modes and exact three input pins are
frozen in this document plus the pinned source copies. The original source
baseline/evidence remain unchanged. The native freeze command records this
document's hash, pins hash and all three byte hashes. Await root's explicit
release before opening the other five inputs or qualification contents.
