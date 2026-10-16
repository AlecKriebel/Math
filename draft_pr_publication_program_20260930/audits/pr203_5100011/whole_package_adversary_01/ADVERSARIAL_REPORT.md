# First independent whole-publication-package adversarial review

PR203 / problem5100011 / k203,a. Review began 2026-10-16 08:27:58 UTC. This report concerns the exact sealed `publication_package_v1`, not merely a proposed route, a diff or a previous favorable verdict.

**Verdict: CLEANPASS for the stated, attributed publication package. No substantive mathematical, source-credit, privacy, integrity or reproducibility issue remains in the reviewed scope.** Two optional P3 clarity improvements are recorded below; neither changes the theorem or constitutes a required mathematical repair. This is an AI adversarial audit, not conventional human peer review or proof-assistant certification. Publication/integration actions are outside my assignment and were not performed.

## Frozen object and independence

The independently frozen attack plan is INDEPENDENT_PLAN.md. The mathematical reconstruction in MATHEMATICAL_RECONSTRUCTION_FROZEN.md was created at actual UTC 08:31:03.355671 before earlier favorable derivations or Root gates were read. Its initial handwritten 08:35 timestamp was a typo; the correction explicitly records the real creation mtime and did not alter mathematical content. The plan preceded reading the current manuscript. After reconstructing it, I read the archived original proof, relevant source/audit/provenance records and earlier mathematical reports to reconcile their claims with the current package. Their verdicts were never substituted for proof.

Supplied and independently recomputed seal: 21091 bytes, SHA256 d8bf1dbb37175a2b8799f81564d2f742f04f942628d6463f32af30adb0db0bd6. Current PDF: 87468 bytes, SHA256 1527058699ee47605314d6e25622d6e49c9f8123e7ae1038ca3e52b70f47a984. Current standalone TeX: 22349 bytes, SHA256 c4d8b60befd30aa22072ca150e37f15a37061e93986008e836e50a366a0e6065. TeX inside materials is byte-identical.

## Exact verified claim and exclusions

For a>b>0 and 0<lambda<b², fix the noncircular outer ellipse E and its proper nested confocal elliptical caustic C. Suppose the physical family has least period N=2m, where m>=2 is even. Let A be the signed shoelace area of the actual ordered vertices and B_M that of the perpendicular feet of one fixed finite real M on the successive complete original side lines. Then A B_M is independent of phase. Every admitted coprime winding, both traversal orientations and zero/negative signed pedal areas are covered.

This does not extend to arbitrary padded list lengths, moving M, clipped segment projections, unsigned filled-face areas, nonconfocal pairs, hyperbolic or degenerate caustics, or the circle by substitution into singular charts. These are material hypotheses, all retained in current paper/README/metadata. The strongest verified result is the complete universal theorem in that scope, not a finite-computation extrapolation. No remaining mathematical gap was found.

## Independent mathematical reconstruction and attacks

### Curve, charts and translations

Write c=a²-b², D=u²+v² and H=a²u²+b²v². On C*: alpha²u²+beta²v²-w²=0 one has H-w²=lambda D. Substitution of

    eta²=a²b² lambda D,
    P=[-a²uw-v eta : -b²vw+u eta : H]

verifies both incidence and the outer conic; my independent symbolic controls check these identities. The endpoint discriminant is proportional to D. Its four zeros are exactly [1:epsilon i:delta sqrt(c)]. In u=1, w is nonzero and v is a coordinate, and dD/dv=2epsilon i is nonzero. A simple discriminant zero gives a smooth simple ramification point. Away from them the two endpoint roots are simple local sections. This includes the canceled displayed triples: at H=0, D and eta are nonzero, the line is not an outer tangent, and its finite and infinite intersections remain distinct. Thus there is no hidden singularity or identified pair at those charts.

As an additional global check, parameterize the dual conic by [beta(1-r²):2alpha r:-alpha beta(1+r²)]. The cover quartic is q(1-r²)²+4pr², p=alpha²>q=beta²>0. Its independently computed discriminant is 4096 p²q²(p-q)², nonzero; its nonzero leading coefficient also excludes an unlisted branch at r=infinity. A disconnected degree-two cover would have two unbranched degree-one components, impossible here. Projectivity gives compactness; Riemann-Hurwitz gives genus one. The other projection branches at the four finite transverse E/C intersections printed in the paper, hence is unramified at both outer infinities.

The two deck involutions have genus-zero quotients and negate the holomorphic differential. T=tau sigma preserves it and is a genus-one translation. Its least real orbit length is exactly its global translation order. No nonidentity power has a fixed point. The reversal equations follow directly from the involution identities.

The real-component construction is complete: q(phi) lies strictly inside E, so P=q+s d has two distinct roots s of opposite sign. They form two circles, both mapped homeomorphically onto E(R). At a fixed outer vertex the two tangent solutions have derivative s/(alpha beta) with opposite signs. Thus each of sigma,tau exchanges the circles and T preserves one. I sends phi to phi+pi with s unchanged, is orientation preserving and commutes with T. The finite group they generate acts faithfully on that circle. Averaging a metric makes its orientation-preserving elements rotations, with a unique nonidentity involution. Consequently I=T^m, for all primitive stars as well as convex traversal. Reversal gives the other orientation.

I specifically checked the physical-to-flag identification discussed below: a reflected side is the other caustic tangent unless there is normal retracing. At P=(a cos(theta),b sin(theta)), tangency of the outer normal line to C would require lambda=a²sin²(theta)+b²cos²(theta)>=b², excluded. Therefore physical steps are T steps. The real projection homeomorphism then equates the vertex and flag least periods. No circular invocation of the target invariant is involved.

### Exhaustive pole orders and complementary zeros

Outer affine coordinates have simple poles at their two infinities, and their pullbacks remain simple. Consecutive vertices cannot both be infinite: distinct infinities would require z=0, not tangent to C, while coincident infinities require an outer infinity tangent that fails the dual-caustic equation by lambda(1/b²-1/a²). Thus every area determinant has at most one simple-pole factor. Multiple nonadjacent infinite vertices in the same phase do not raise the order of their sum. At x above infinity, tau x=I x, so sigma x=T^(m-1)x.

For arbitrary fixed finite M,

    Q=M-(u Mx+v My+w)(u,v)/D

is homogeneous and rational, regular whenever D is nonzero, including w=0. No point on C* has u=v=0. Therefore the four D zeros exhaust possible foot poles. At a branch point, t=eta is a uniformizer and D=t²/(a²b²lambda); v(t), w(t) and Q(t) are even Laurent functions. Individual pulled-back feet can have order two, not merely one. Vanishing numerators for special M only remove poles.

At a sigma-fixed flag the singular indices are precisely 0,m, since T^(2j)x=x iff N divides 2j. Other feet are regular. Reversal Q_j(sigma y)=Q_-j(y) makes each adjacent difference odd and O(t). Grouping the incident edges leaves det(Q_i,Q_(i+1)-Q_(i-1)), of order at most one. These groups have disjoint edges, even for N=4: the two groups expand into all four edges exactly once, despite sharing regular neighbors. Simultaneous branch feet and every special M are therefore included. Independent formal Laurent and finite-index controls check the grouping.

An intersection of the two translated supports would require 2j=m-1 mod 2m. It is impossible for even m. Conversely, for odd m this congruence has a solution, confirming the specific parity obstruction rather than assuming it. At the branch support, P_j=P_(1-j) gives a regular original-area zero. At the infinity support, Q_j=Q_(m-1-j) gives a regular pedal-area zero with the same fixed M. A cyclic signed sum satisfying W_j=W_(k-j) changes to its negative under index reversal and is zero, without convexity or distinctness assumptions. These zeros cancel the other's at-most-simple poles. The complete product is holomorphic on connected compact X and hence constant. There is no division by an area or a coefficient depending on M.

### Radiality, N4 and signed boundary controls

The general side-normal projection formula expands into B_0+ell dot M+C_2|M|². The anisotropic quadratic terms telescope; the stated coefficients and the 1/8 sine factor are correct. Independently arbitrary normal signs do not change the expression. A zero quadratic coefficient alone leaves the linear term for a general crossing list; central opposite-side pairing separately cancels it here. Evaluating the theorem at M=0 and a unit point justifies phase-independent K_0,K_2.

For N4 central symmetry makes a parallelogram. The axis diamond follows from reflection and central pairing, and its tangency forces lambda=a²b²/(a²+b²). Direct areas yield 8a⁴b⁴/(a²+b²)²=8alpha²beta². For P=(U,V,-U,-V), the separate formula 8det(U,V)^4/(|V-U|²|V+U|²)=8 times the product of origin-to-side distances is correct, and the cited Bialy-Tabachnikov theorem supplies the prior implication.

I independently recomputed the two primitive-six products 14000/729 and 14336/729 by side-vector projections; doubled lists give 56000/729 and 57344/729, with difference448/243. The packaged exact controls additionally check actual reflection signs and primitivity. This falsifies nominal-length-only scope and does not falsify the stated theorem. Independent arbitrary-M symbolic projection of the 3/8 star gives A=168sqrt(6)/5 and B_M=96sqrt(6)(13-|M|²)/245. Its zero at M=(sqrt(13),0) has first-three-feet wedge (2304sqrt(6)-1152sqrt(39))/1225, nonzero; the zero area is genuinely signed and need not mean collinear feet. At M=(4,0) B_M is negative. Reversal signs and product invariance agree.

## Sources, priority and original proof provenance

Direct primary inspection confirms RGK journal equation(1), Section3.3 and Table3 at pp343,344,346; arXivv11 equation(1) p3 and Table3 p6 agree. Both use signed area and original pedals, and neither table literally prints least period. Current paper says this explicitly. Historical proof question marks are not used as a current-openness claim.

I fetched the original Ferudun record and original PDF directly into memory: 183271 bytes, SHA256 5c54d3e2e525d794fec25be6ec1a929eaccc95e2332b0ae6ee0ed780e46098a0. Its definitions, Theorem A p2, conventions, Section4 pp9-11 and Table2 p14 establish exact scope overlap, stronger complex M, the same complementary-poles/reversal-zeros strategy, N4 value and the rescaled star. Current abstract, main text, bibliography, README and metadata credit these prominently and make no theorem/method novelty, first-disclosure or certified-independence claim. The attributed-alternative authorization is respected; absence of novelty is not invented as a rejection condition. [Original record](https://doi.org/10.5281/zenodo.23400541).

Steiner's primary e-rara OCR, SectionsXIV-XVI/reprintpp18-22, supports classical pedal radial dependence. I read it in memory; degraded formulas are not transcribed as an exact modern proof. The current independent signed derivation and linear-term caution avoid its zero-coefficient extension ambiguity. [Primary edition](https://doi.org/10.3931/e-rara-3816).

Schwartz-Tabachnikov Section3 directly gives the flag cover, involutions, translation and meromorphic compactness framework; Chavez-Caliz p92 acknowledges the centroid proof gap, which the current paper explicitly avoids using. Chavez Theorems3/6 pp93,104 concern the outer-tangent polygon, not the requested pedal, and support the original archived proof only after its explicit polarity transfer. Stachel Theorem4.3/(4.9) pp1614-1615 gives the canonical parameters used there. The printed p1613 dn shift typo is real; the archived proof uses correct DLMF shifts/poles/addition formulas. AST Sections4-5 also directly support established complexification/pole-cancellation attribution. Bialy-Tabachnikov Theorem4.3(2) supplies the N4 implication claimed. These references support their actual roles rather than an uncited universal pedal theorem. [Schwartz-Tabachnikov](https://arxiv.org/html/1607.04766), [AST](https://arxiv.org/html/2001.02934v2), [Bialy-Tabachnikov](https://arxiv.org/html/2001.08469v2), [DLMF22.4](https://dlmf.nist.gov/22.4), [DLMF22.8](https://dlmf.nist.gov/22.8).

I read the original 13058-byte submitted proof and all unique executable sources. Its contact-trace organization also closes: radial symmetries give the correct imaginary anti-period, branch-even singular feet reduce to simple poles, the reduced dn comparator has two genuine noncancelling residues, one scalar removes both principal parts, and compactness/anti-period forces the difference to vanish. The K shift is a cyclic trace period for N divisible by four. The credited outer-area theorem plus correct determinant polarity map gives the product. The disclosed sibling contribution is author input, not an independent reviewer. No method novelty is inferred from the different organization.

All18 original submission files/59989 bytes were independently fetched from raw GitHub at original immutable head8edca9d773c085adb4ed0611357a7a2957e3395d and matched both SHA256 and native Git blob identities. Direct original-commit API access confirms treea252862d17b9bebd2021d534cb18c310ae0a343f and sole parent42192ac11c85feb6b215c32e00f5ab2c2678b0a3. Current public PR API gives creation2026-10-01T05:24:27Z. Direct Zenodo metadata gives creation2026-10-15T16:11:42.588744Z. This verifies the manuscript's object chronology. It does not authenticate discovery times, historical visibility at every earlier instant, earliest disclosure or independent discovery. Current prose correctly makes none of those inferences.

## Complete package, code, privacy and reproduction

INTEGRITY_RECEIPT.json binds every outer file and every material/ZIP member. The outer seal pins111 files excluding itself (112 including it); materials has106 pins plus its own root manifest; ZIP has107 unique regular-file entries, exactly matching every material byte. No traversal path, symlink, archive comment, per-entry comment/extra data, unexpected binary, fulltext PDF/OCR, dependency implementation or installer is included. Total uncompressed ZIP content is565101 bytes. All107 material files are UTF8. Strict parsing validates43 JSON/JSONL files; nested authored/reviewer manifests and both Root gate allowlists match their actual contents. The self-exclusions are explicit, with no circular current-PDF/ZIP pin inside the archive.

Current metadata equals the metadata portion of zenodo-deposit.json exactly. Title, author/ORCID, scope, license, date, AI/unrefereed disclosures, bibliography references and proposed three upload files agree. Historical gate/status records openly describe earlier stages, not current publication clearance. Archived old source/search claims are preserved as dated records and are superseded by the prominently credited current exact overlap. Partial direct-Euclidean work is explicitly blocked at the two higher-period scalar invariants and is not counted as a second universal proof. Failed conditioning/transport attempts and correction receipts reconcile with final results; failures are not counted as successful evidence.

All executable source was inspected, including portable scripts, original author/reviewer checkers, analytical/flag controls and historical capture/materialization scripts. The supported runner uses standard libraries plus pinned SymPy1.14.0/mpmath1.3.0, copies working checks into a disposable temporary directory, inherits dependency availability in child processes and verifies the material manifest first. The only portable-source changes are exactly the declared removal of two repository-specific path-insertion lines from each main checker; signed_edge_checks.py is unchanged. Raw historical scripts retain historical paths and are archival evidence, not the supported portable entry point. No hidden executable/network operation occurs in the supported runner.

My fresh default runner passed ordinarily and under -O:282 explicit-exception exact geometry controls, seven N4 symbolic identities and actual8-to9 coefficient mutation rejection in each mode. Both deliberate-false guards exit nonzero with the stated message. My separate133 exact controls also pass in both modes, with additional chart/normal/noncollinear-zero controls saved separately. Complete-source bytecode inventories show both original checkers have two assertion sites ordinarily and zero under optimization; their actual unchanged check wrappers reject128/25=129/25 ordinarily and accept it optimized while incrementing the advertised counter. This bounded probe is explicitly distinguished from a full broad legacy rerun.

I checked archived full RAM mutation results and Root's fresh complete ordinary legacy replay receipts, including byte comparison of the original author/reviewer stdout against historical JSON. The24,110/20,578 ordinary enforced totals and zero optimized enforcement reconcile with actual code. The broad39-caustic107962-check and2000-check signed-edge results bind to their exact scripts and have the stated scope. They were not redundantly rerun or accepted as universal proof. High precision is correctly labeled noninterval diagnostic evidence. Unknown historical runtime settings remain uncertified.

Privacy/content inspection found no credential-like material, browser state, private keys, full third-party texts or executable dependencies. Historical tracebacks do contain benign author workspace paths; these are not secrets or copied operational caches. Public author identity, ORCID, URLs, hashes and curated record metadata are intentional. This is a content/inventory/pattern review, not a cryptographic guarantee of privacy.

## PDF visual and payload review

All seven current private page PNGs were individually viewed. Their hashes, PDF hash and TeX hash match the current Root render receipt. The visible theorem, charts, equations, controls, qualifications and references agree with the reviewed source. No clipping, overlapping text, broken glyph, unreadable formula, blank accidental page or unresolved citation is visible. PDF inspection reports seven letter pages, no encryption/form/JavaScript, zero embedded files, no custom metadata/metadata stream, and only the intended ORCID/source/PR URL annotations. No new render or UI tab was created.

## Nonblocking editorial observations

- **P3, optional:** README reproduction commands are consecutive plain Markdown lines, which collapse into one paragraph in normal rendering. A fenced text block would make copying clearer. The raw commands and actual supported runner are correct; reproduction succeeded.
- **P3, optional:** Add one explicit physical-to-flag sentence after T=tau sigma: normal retracing would require lambda>=b² and is excluded; hence the physical step is T. The following real-circle projection homeomorphism then identifies least periods. The standard Poncelet identification and stated proper-caustic hypothesis already justify the current argument, so this is an exposition improvement, not a substantive gap.

No mandatory repair is requested. Any change to the sealed manuscript/kit nevertheless creates a new object and should be re-pinned and checked in the next whole-package review. My CLEANPASS applies only to the seal identified above.

## Research completion and limits

Review completion estimate:100% of this assigned bounded whole-package audit. Universal theorem status: verified by the complete reconstructed proof under its stated hypotheses; no numerical certainty percentage is assigned. No global novelty/exhaustive-priority certificate is claimed. No Git/index/ref/branch/checkout operation, native/package/source modification, publication, upload, release, tracker change, UI operation, outside-person contact or outreach draft occurred. Only this review's small authored reports, scripts and receipts were written.
