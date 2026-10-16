# FIRST NEW whole-manuscript adversarial review — PR210 / 5100033

Review date: 15 October 2026 UTC. Completion: **100% of this assigned review**. This is a new review of the entire concrete preprint/package, separate from the five earlier source/mathematical/priority families and supporting preparation audit.

**Verdict: FIX before the second new whole-manuscript review. The universal odd least-period theorem and both stated alternative mathematical bridges survive independent scrutiny; no central proof gap or true-domain counterexample was found. Required repairs concern the categorical even-boundary statement, an unsupported authorship sentence in the native presentation, and a contradictory current result limitation. Optional pointer/notation/history clarity repairs are also listed below. This report grants no publication authorization.**

## 1. Exact version, independence and coverage

This report binds the ZIP SHA256 **6324b31294ed313e523f85454ba4c4b82b412d0942432e7cae7ef611140bea6b** (577419 bytes,169 entries), manuscript.tex **326f6913193c29142e1f197e91fa7551de8b804be953d4c50a39f4a52bc61a32** (18984 bytes), and manuscript.pdf **d97403942641892ef91573e9cae04d0d8d09d596a5f8f9448e63d00a15288a52** (88803 bytes). The metadata hash is **3b382df7e7ecc4f4b5d91a3945c0a6704675ba649c5796da62a0b24e73ff4909**. Full inventories and individual entry hashes are in INPUT_AND_INTEGRITY_RECEIPT.json.

Before reading preceding mathematical/priority verdicts, I read only AGENTS.md and this concrete manuscript, then froze INDEPENDENT_RECONSTRUCTION.md. The initial reconstruction identified the exact target, domain, proof mechanism and adversarial failure points. Subsequently I inspected all six rendered manuscript pages; the complete current native PROOF/SOURCES/README/status/readiness/turn/verification presentation; package and native manifests; both builders; the harness, integrity checker, payload validator and PDF adapter; the original scientific and inherited checkers; scoped reports and complete exact bicentric/inversion bridges; decisive primary-source passages; and every archive entry's name, bytes and manifest coverage. This is not a claim to have reread every unrelated page of the bounded literature corpus.

Root's later matching exact N4/source-typo message arrived only after my fresh exact control had already failed on that source's printed square twice. The overlap is disclosed, as are the failures and correction. My fresh script imports no archived scientific checker. Mathematical independence rests primarily on the frozen reconstruction and universal derivations, not a count of PASS flags.

No reviewed byte changed. No Git/index/ref, PR/provider, Queue/SQLite, deposit/tracker or publication action occurred. No external individual was contacted. All authored files are here; a private source-page JPEG is excluded from publication/manifests.

## 2. Target and success criteria

The original boundary ellipse is E:x²/a²+y²/b²=1 with a>b>0 and original foci F±=(±c,0), c²=a²−b². The fixed inner caustic has α>β>0, α²−β²=c², and is strictly nested. For an ordered primitive billiard orbit P_j, let l_j be the boundary tangent at P_j, V_j=l_j∩l_(j+1), and Q_(±,j) the perpendicular foot of the ORIGINAL F± on the ordered outer side line V_(j−1)V_j=l_j. Areas are signed shoelace sums in trajectory order, including stars. The claim is phase constancy of B+B− for every odd LEAST N≥3 and every admitted coprime winding. It is not original-chord pedal area, a finite-segment clamped projection, inverse area, unsigned face-union area, or a derived ellipse's own-focus construction.

Fixed repetitions multiply each area by s and the product by s², for any positive integer s. This can produce an even list with odd least period; even negative controls must refer to even primitive families. Circle boundaries have their own direct rotation argument. Hyperbolic, collapsed and grazing caustics are excluded. No unproved limiting passage to k=0 or1 is needed.

Success means an all-period derivation under these assumptions, exact checks of crucial geometry and actual source statements, explicit uncertainty about priority, strict reproduction/binding of current data, and no false certification claims. Numerical residuals do not establish universal identities or rigorous error bounds.

## 3. Independent universal proof audit

### Canonical coverage and actual outer sides

For an arbitrary pair in the domain, β/b∈(0,1), so a unique v∈(0,K) satisfies cn(v,k)=β/b with modulus k=c/α and k'=β/α. Confocality gives α²dn²v=a²β²/b², hence a=αdn(v)/cn(v), b=β/cn(v). Stachel's actual Theorem4.3 then gives P(w)=(-a snw,b cnw), step δ=2v. Real injectivity modulo4K turns least-period closure into Nδ=4Kτ with gcd(τ,N)=1. Orientation can be chosen so0<τ<N/2. This covers each stated physical family, rather than merely constructing selected examples.

Consecutive vertices are distinct and nonantipodal because0<δ<2K. Their tangents therefore meet finitely. A collapsed outer side would give three distinct tangents through one point; duality/Bézout for a nonsingular conic excludes that. Thus the literal outer side lines exist for every real phase, including stars and N3.

Projection using n=(-snw/a,cnw/b), n·X=1, gives

Q_+(w)=(a(c−a snw)/(a−c snw), ab cnw/(a−c snw)).

The canceled factor a+c snw in n·n is legitimate as an identity of meromorphic functions; on the real family the final denominator is at least a−c>0. Direct algebra gives Q·Q=a² using a²−b²=c². The original opposite-focus map is Q_-(w)=−Q_+(w+2K); global negation preserves area. All complex products used here are bilinear.

### Every pole, every simultaneous endpoint and the true period lattice

sn has degree2 on its own torus (4K,2iK'). The vector Q requires the common lattice(4K,4iK'); treating2iK' as its period would be false. Write p=iK', r=K+p. The actual quarter shifts are

sn(r+z)=dnz/(k cnz), cn(r+z)=−i k'/(k cnz), dn(r+z)=i k' snz/cnz.

At common sn/cn poles, Q is removable because its denominator has a nonzero simple principal term. Every other pole solves snw=a/c; the two roots on the sn torus are r±v, with nonzero derivative. The vector torus has exactly their2p translates as well. At r±v the numerator equals(−ab²/c,−iab²/c) and denominator derivatives oppose. For example at r−v the residue is R=−a/(k snv)(1,i), and at r+v it is−R. Translation by2p reflects both vectors and preserves their collinearity.

At a singular phase, precisely two orbit indices are singular and they are adjacent. Coprimality makes all N classes modulo4K distinct; a real step cannot join the two imaginary rows. The adjacent determinant has nominal coefficient det(R,−R)=0 at orderε^−2. Every other edge contains at most one singular endpoint. For N3 the two singly singular edges share a single regular vertex C; their combined simple coefficient is det(R,A+B−2C)/2, still no double term. An index-cut edge is legitimate because Nδ=4Kτ is a true vector period.

The cyclic trace T has periodsδ and4K. Bézout gives L=4K/N. On C/(LZ+4pZ), all possible poles are K−v+p and K−v+3p, each at most simple. The two imaginary classes remain distinct. Nothing about this counting assumes winding1 or prime N.

### Reflection and complementary zeros

Let J=diag(1,−1). Q(w+2p)=JQ(w) and Q(2K−w)=JQ(w). The first negates T. In the second, planar reflection and reversal of the cyclic order each supply a minus sign, so T(2K−w)=T(w). Sinceδ=2v is a period, F(z)=T(K−v+z) is even. It has periodsL,4p, antiperiod2p, and possible simple polesp,3p.

At the regular point z=p+L/2, evenness and real periodicity give F(−p+L/2)=F(p+L/2), whereas the antiperiod gives its negative. Therefore F vanishes there, and also at3p+L/2. These zeros cancel every possible simple pole of F(z)F(z+L/2), from either factor. Compactness makes that product constant. No zero-degree count is required, no nonzero area is assumed, and no division through an area is used. If all poles disappear, compactness and the antiperiod force F=0 directly.

For odd N,2K=(N/2)L≡L/2 moduloL, exactly the original-focus switch. Thus B+B− is the constant just proved. For even primitive N the focus switch is a full period and yields B+=B−; it does not prove constancy of their square. This is a complete universal argument in the stated domain.

## 4. Independent checking of both related-work transfers

### Bicentric geometry and old dn identity

I checked the full EXACT_BICENTRIC_DN_BRIDGE.md, not merely its final citation. The projectivity

T_+(x,y)=(a²(x+c)/(a²+cx),a²y/(a²+cx))

has positive denominator on the original closed ellipse interior and restricts to the focal foot on E. Its inverse has x=a²(X−c)/(a²−cX), y=b²Y/(a²−cX). Substitution gives the displayed image caustic. Its x/y quadratic coefficient gap is−c²λ²/(α²β²); the conic is an ellipse with focus atO, not already a circle. Polarizing with the actual line q·R=a² produces the genuine outer circle centered at d=−cλ/β² with radiusR=αb²/β² and incircle radiusr=a. The negative sign is essential and agrees with the offset-ellipse control. The preserved positive-sign intermediary is forensic only.

The tangent intersection is V(z)=(-a² snz/α,b² cnz/β), z=w+v+jδ. Direct substitution in T_+ gives the recorded circle coordinates. The quadratic transform uses PARAMETER m_b=4k/(1+k)², K_b=(1+k)K, u=(1+k)(z−K)/2. Its dn identity can be checked by the displayed second-order ODE and initial conditions; there is no remembered shift imported without verification. The tangent length is t_j=t_M dn(u+jσ,m_b)>0 withσ=2K_bτ/N. For stars, each chord leaves the image caustic and its interior pointO on its left, so det(Q_j,Q_(j+1))>0, the selected contact-angle increment is in(0,π), and the tangent-length sign is fixed.

The local Jacobi addition identity, cyclic reindexing byσ, and Nσ=2K_bτ give

B_+/A(R)=r²/(R²−d²),
B_+=r³t_M/(R²−d²) Σ_j dn(u+2jK_bτ/N,m_b).

The real denominators are strictly positive. Coprimality reorders the sum. Khare–Sukhatme's ACTUAL published Eq7,p923 gives the arbitrary-integer-order dn sum, not merely a generic method reference. Its scale follows independently by averaging the classical dn Fourier series: only frequencies divisible by N survive, the new nome is q_b^N, and the scale is NK_N/K_b. Uniform absolute convergence on the real axis justifies the finite filtering. Original focus exchange is exactly u→u+K_b; for oddN the reduced argument changes by NK_N≡K_N. The old dn half-period product finishes the target. Units agree: the area prefactor has length² and the product length⁴.

This exact bridge proves a current application of old analytic identities. It does not establish whether the complete geometric application was printed earlier. No generic projective preservation of area has been assumed. My fresh controls test the actual outer intersections, the negative circle center, positive tangent length, contact ratio, dn area trace, old sum scale and phase alignment independently.

### Original inverse-area theorem and opposite focus

I read the complete six-page Ferudun0062 paper, including its proof, in the reused primary copy. For unit inversion of original vertices about F−, the translated inverse vector is R_−=(c−a snw,b cnw)/(a−c snw)², so Q_+=a(a−c snw)R_− pointwise. That variable factor alone does not transport area.

The printed inverse proof actually supplies the needed trace facts: Lemma2 locates at-most-double inverse-vector poles; Lemma3 first bounds the area order by2 because both negative Laurent coefficients are parallel to a common nonzero isotropic vector, then reversal about the pole phase removes the even term; Eq7 supplies the imaginary antiperiod; §4 supplies the reduced real period. Positivity for real forward orbits follows because both original foci lie strictly inside the caustic and each directed chord leaves it on the left. Thus the inverse area is a nonzero meromorphic function.

The outer-foot trace and opposite-focus inverse trace belong to the same space of functions with at most simple poles at r−v and its2p translate and antiperiod2p. That space has dimension at most1: matching one residue matches the other; their difference has no poles, is constant by compactness, and is zero by the antiperiod. Consequently B_+=γD_− and B_−=γD_+, without dividing through zeros. The inverse product theorem then gives the current target. The needed outer-foot pole bound is additional geometry and is not printed in0062; its inverse label alone neither excludes relevance nor establishes prior literal target publication. The main proof above is independently sufficient.

## 5. New exact boundary control and source correction

The manuscript's categorical statement that the odd hypothesis is essential should be supported by an exact counterexample. The current package labels its even samples as uncertified diagnostics. The following independent exact calculation closes that presentation gap.

On E:x²/4+y²=1 with λ=4/5, the diamond D=((2,0),(0,1),(−2,0),(0,−1)) and rectangle C=((4/√5,1/√5),(−4/√5,1/√5),(−4/√5,−1/√5),(4/√5,−1/√5)) both satisfy boundary incidence, unit specular reflection and tangency to x²/(16/5)+y²/(1/5)=1. Both are primitive4-cycles. Actual outer intersections and orthogonal feet give

B±(D)=4, B+B−(D)=16;
B±(C)=5, B+B−(C)=25.

For the diamond, the plus-focus feet are explicitly(2,0),(√3,1),(−2,0),(√3,−1), whose area is4; the minus case follows by reflection. fresh_controls.py verifies the rectangle equally exactly. This proves nonconstancy in the even primitive class. Fixed even repetitions of an odd primitive orbit remain covered by the repetition corollary.

**Important source error, not a counterexample to the cited odd theorem:** Ferudun0062 printedp6 literally uses(±2/√5,±2/√5). Its first horizontal edge hasλ=1/5, its vertical edgeλ=16/5. With the purportedλ=4/5 the unnormalized tangency residual is48/25. It lies on the boundary but is not a billiard rectangle. At the upper-right corner the reflected outgoing unit vector differs from the actual leftward vector by(9/17,−15/17). The printed inverse products1 and25/16 instead fit the correct rectangleC. I independently reproduced this failure before root's matching message and visually verified the actual source page after extracting the text. This is a fixture typo in a cited primary source. Its all-odd proof and H/V triangular inputs survive; do not propagate the square or silently attribute the corrected rectangle as the source's literal coordinates.

Other new exact controls expose false domain widening: an affine image of rotating regular triangles on x²/9+y²=1, tangent to its homothetic half-sized ellipse, has focal-foot products2187/784 and27/16 at phases0 andπ/6. It is a Poncelet family but not the strict confocal billiard family. A radius2 circle triangle gives foot-area product27 by a direct exact calculation. These finite constructions support the stated boundaries; no unrelated generalization is asserted.

## 6. Sources, credits and exact priority limits

Primary-source checks were about actual objects/passages, not inherited labels:

| Source | Passage independently checked | Conclusion and coverage boundary |
|---|---|---|
| RGK arXivv11 | §2 signed sum; §§3.4,3.7; Table7 printedp9, visually inspected | k605,a is the primed outer focal-pedal product; oddN, historical proof column?. |
| RGK published AMJ7(2021) | Table7/§3.7 printed349, visually inspected; construction and signed convention in adjacent sections | Same target is k606; publishedk605 is original-chord product. |
| RGK arXivv1 | Actual Table5 printedp6, visually inspected; official v1 record freshly browsed | Literal primed product is k604, submitted26April2020. This establishes occurrence within this source series, not first discovery worldwide. |
| Stachel published | Printed1613 context and1614 Theorem4.3/Eq4.9; exact page image inspected | Correct canonical phase and coprime windings. Nearby prose's false dn2K sign is not used. |
| NIST DLMF | Tables22.4.1/22.4.3, Eqs22.8.1–3 and22.11.3 freshly browsed | Correct full-vector lattice/quarter shifts, addition rules and dn Fourier filtering. |
| KS Pramana63(2004) | Exact published-text copy Eq7–9 printed923 and §2.1 | Real arbitrary-order old sum theorem; no printed focal-area application established in the read passage. |
| Ferudun0062 | Entire six-page primary PDF/text; Thm1, Lemmas2–3 pp3–4, Eq7, §4, §6 | Material all-odd inverse result and exact additional transfer above; p6 negative fixture typo separately recorded. |
| Ferudun0014v1.1 | Theorems1–2, canonical/pedal definitions and method | N≡2mod4 arbitrary-point product and odd center result; close parallel-residue precedent, distinct target. |
| AST authorv2 | Theorem3 and relevant complex-method context | Odd concentric original/tangent area ratio; not a generic projective area transfer to displaced-center conics. |
| Chávez-Caliz final | Theorem6 and full proof printed104 | Earlier complementary area-pole/zero mechanism for even original/tangent areas; not this focal pair. |
| RGR authorv3 | Theorem2 proof/Corollary1 | Earlier bicentric limiting-point pedal/focal inverse PERIMETER and pole-removal mechanism; no area theorem silently imported. |
| KLS-II authorv2 | §2 principal-part/Fourier master-identity development | Established cyclic elliptic reconstruction framework, correctly credited. |

The source ledgers further distinguish title-only screening, selected passages, whole proofs and inaccessible sources. I checked that the current manuscript does not turn their bounded negative finding into firstness, absolute novelty or current-world-open claims. The inaccessible Stachel Triple full text and incompletely compared final Talented journal edition remain genuine coverage gaps; open author versions and source question marks do not close them. Videos without inspected proof/transcript provide no absence evidence. This review does not independently repeat every search or certify exhaustive historical priority.

The manuscript's contribution framing is appropriately a source-specific proof/application with substantial old-method/current-work credit. Its derivability from an old identity and related recent theorem neither proves earlier publication of the exact application nor establishes novelty. Historical priority remains undetermined.

## 7. Reproducibility, integrity and presentation

INPUT_AND_INTEGRITY_RECEIPT.json records all169 ZIP entries with uncompressed size/hash/CRC and exact on-disk equality. It independently validates all168 SOURCE_MANIFEST payload rows plus the manifest itself, all117 verification payload rows, native current-packet41 rows and both active top-level manifests. No duplicate/traversal/encrypted/symlink/private/cache entries were accepted. Only manuscript.pdf is a PDF payload; there are no third-party fulltexts or rendered-source pages in the source ZIP.

All20 original files match submitted/, verification/original_submission/ and native history/original_submission_20261015/ byte-for-byte, with independently recomputed Git blob SHA1 plus SHA256. Original-current author/review hashes and the deliberately superseded V1 source hash are preserved. The top native verification.json correctly labels its inherited original-proof binding and embeds the original result; it does not claim to bind the edited proof. Current native manifests bind the edited presentation. The old positive-polarity script/result is explicitly forensic and absent from the live JOBS table. Earlier pending/preparation receipts are dated; no actual DOI, tracker, final clearance or merge is invented in the dated ZIP.

I inspected the strict equality mechanism: normalization deletes only the named top-level interpreter/timestamp fields, type/key/list ordering remain exact, and scientific residuals/counts/hashes/precision/version fields are compared without tolerances. The adapter executes the unchanged scientific program and replaces only digest calls for the exact3 known PDF paths, validates those hashes and substitution usage, and explicitly disclaims fresh PDF verification. It does not replace the mathematical outputs or code. Genuine-primary mode freshly hashes/copies PDFs and bypasses the adapter entirely. The observed preparation receipt's113-file earlier inventory is historical; my genuine replay validates the actual current117-file seal.

My two isolated current-package replays succeeded:

- GENUINE_MEROMORPHIC_REPLAY.json: fresh genuine3-PDF hashes, zero substitutions, exact scientific JSON, raw inequality only from named timestamps. It independently reran11 symbolic checks,3503 finite primitive cases,354690 pole-phase checks,88 selected Bézout certificates and11 high-precision families/33 pole rows. Its current before/after manifest is f64fc9ad80fa2520fcdb7bc6f0ee6017b5c6328ae981b8519c2429991001bc83.
- CLASSICAL_REPLAY.json: exact scientific JSON and raw byte equality for15 symbolic zero identities and11 cases/55 phases, including the area/dn bridge and wrong-parity controls.

FRESH_CONTROL_RESULTS.json is independently authored,110-digit numerical falsification across7 families/28 phases, including N51τ25, k3e−6 and0.9999999. It checks actual side feet, caustic tangency, physical unit reflection, transformed circle/tangent lengths, contact ratio/dn/KS trace, opposite inverse ratio, quarter shifts, imaginary character, forced zeros and near-pole order. Maximum odd normalized product spread is about3.992e−110; largest other residual excluding finite-ε order is about1.003e−92; finite-ε²T scale is at most1.413e−27. Its even primitive8τ3 normalized product spread is about5.344e−5. These are observed residuals, not intervals or certified error bounds. Exact parity/nonconfocal/source-typo controls are separate.

I visually inspected all6 provided rendered pages, including formulas split across pp2–3, main cancellation proof, long archive paths on pp4–5, and complete references onp6. No clipped content, unreadable formulas, overlap or broken symbols was found. PDF metadata independently says6 letter pages, title and Alec Kriebel, unencrypted, no form or JavaScript. The LaTeX log has6-page output and no overfull warning. Root's successful editor/Tectonic compilations are recorded but were not rerun here. The current metadata has the required ORCID0009-0001-9320-500X, cc-by-4.0, preprint/open/version1.0/date2026-10-15, and exactly equals deposit.json metadata. Extensive AI use, unrefereed status, no independent human review and no formal-proof-assistant claim are explicit. One inherited authorship sentence still needs correction below.

## 8. Complete finding register and precise repairs

**R1 — Required scientific boundary substantiation.** manuscript.tex after Corollary3 says the even countercontrols show oddness is essential, while the offered even evidence is labelled uncertified numerics. Keep the correct categorical boundary claim by adding the exact D/C products16 versus25 above, with verified commonλ/reflection. Record the Ferudun0062 printed-square correction with an actual primary locator in the supporting source notes/ledger, so a reader does not reuse the false fixture. No change to the odd proof is needed. If any exact fixture is attributed to0062, explicitly distinguish its printed wrong coordinates from the corrected independently checked orbit.

**R2 — Required authorship/independence correction.** Current pr_update/5100033/PROOF.md §7 retains “The present author did not coauthor those candidates” about k203,b/k804,a. The public package presents a human author Alec Kriebel; this unsupported sentence appears to speak for internal agent authorship and is not evidence of human authorship or discovery independence. Remove it from the CURRENT presentation or replace it with a narrowly documented internal-review independence statement. Preserve it byte-exact only in original history. Do not infer a public-priority or human-independence fact from independent AI approaches.

**R3 — Required current result/interpretation correction.** The live scope_controls/root_priority_projective_control.py and ROOT_PRIORITY_PROJECTIVE_CONTROL.json still have a limits string denying a “bicentric circle/circle reduction,” although their current algebra and the exact bridge identify the polar circle pair. This is contradictory current scientific interpretation, rather than merely an archived wrong-sign result. Change the active limitation to say that the script proves the geometric circle/conic/polar-circle correspondence but alone does not prove the area invariant or historical priority. Replay the changed current program and update every active binding coherently; keep prior dated receipts/forensic payloads as historical evidence rather than silently representing old hashes as current.

**O1 — Optional, real navigation defects.** Top preprint README.md points to history/original_submission_20261015/ as though it were a top-level package path; use pr_update/5100033/history/original_submission_20261015/ (and/or verification/original_submission/). verification/forensic_history/polarity_sign_intermediate_20261015/HISTORICAL_STATUS.json has current_correction='../../ROOT_POLARITY_SIGN_CORRECTION.json', which resolves to a nonexistent verification-root file. The relocated correct path is ../../audit_receipts/ROOT_POLARITY_SIGN_CORRECTION.json. Fix these active portable pointers without modifying the historical wrong script/result bytes.

**O2 — Optional parameter clarity.** EXACT_BICENTRIC_DN_BRIDGE.md §6 writes K_N=K(m_N) for a quantity named parameter, while §1 uses K(k) for modulus and the current manuscript carefully writes K_b=K(sqrt(m_b)). The formula is correct under parameter convention and both independent numeric reductions agree. Add a current explanatory convention K_N=K(sqrt(m_N)) in modulus notation, or explicitly label the parameter convention. If preserving the sealed earlier family bytes, make this clarification in the current companion/verification README rather than rewriting historical authored artifacts invisibly.

**O3 — Optional primitive-parity wording.** In verification/README.md's concise domain paragraph, say “even primitive-period products” rather than “even-period products,” matching the main theorem and avoiding confusion with an even repeated list of an odd primitive orbit. The detailed package already distinguishes them; this is clarity, not a counterexample to the corollary.

**O4 — Optional native historical-manifest clarity.** A copy of the original MANIFEST_V1.json still sits at native top level beside changed current files. Active CURRENT_PACKET/MANIFEST/PUBLICATION_MANIFEST bindings are correct, and history preservation is documented, so no integrity failure is concealed. Explicitly identify this top-level V1 copy as evaluated against history/original_submission_20261015/; alternatively remove the redundant current-root copy while preserving its original in history. This prevents a reader from trying its historical hashes against the edited current files.

No other mandatory or optional finding remains withheld. The exact mathematical target is proved within its scope. Remaining gaps are historical-priority coverage, the above current presentation/package repairs, and the required independent second new whole-manuscript review of the revised final bytes. Final administrative release receipts are future actions outside this review.

## 9. Failure and correction transparency

The first fresh exact N4 run used the cited paper's literal square and failed the common-caustic assertion. A speculative Python-type explanation led to an exact-coordinate coercion rerun, which failed identically; coercion did not fix the scientific issue. Both failed script versions are retained. The corrected rectangle was derived by enforcing the two common-caustic support distances; it then passed boundary, reflection, tangency and outer-foot tests, and the literal false fixture remains an explicit exact negative control. No assertion/tolerance was weakened. Root's matching independent discovery and later message are disclosed. The final current fresh script was rerun successfully after adding explicit circle/boundary checks.

One PNG source-page rendering attempt failed with libpng exit134; the invalid own temporary image was rejected by view_image and removed. A small JPEG render from the same existing source PDF succeeded and was actually inspected. It remains private, excluded. Other failed read-only path probes had no effect on scientific evidence. No dependencies installed, venv symlinks resolved, source PDFs downloaded, or bytecode created.

## 10. Recommendation

The proof is sound under the precise theorem; the source-specific application is checkable and responsibly qualified. Apply R1–R3 and the listed optional repairs globally, retain historical originals and failures, regenerate/replay active seals, and assign a DIFFERENT second new whole-manuscript adversary to the revised concrete package. This first report binds its original169-entry input and must not be relabelled as reviewing later bytes. Publication, DOI/tracker/native-state readbacks and any merge remain the parent's separate authorized workflow.
