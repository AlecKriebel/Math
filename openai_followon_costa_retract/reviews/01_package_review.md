# Independent complete-package adversarial review 01

Checkpoint: 2026-10-07 04:41:49 UTC / 2026-10-06 21:41:49 PDT. This bounded complete-package review is 100% complete. Best-guess project completion from the evidence reviewed: mathematical resolution 95%; publication package 75%. These are process estimates, not evidence of truth, publication, or peer review.

## Verdict

**REVISE for a precise source-reference correction; no substantive mathematical gap found.** The frozen v1 paper twice cites the upstream result as “Theorem 1,” whereas its exact pinned PDF and TeX number it **Theorem 1.1**. Correct both references, regenerate the PDF/archive and hashes, and give the revised complete package to a new independent reviewer. This review is not a clean final approval of revised files that it has not inspected.

No defect was found in the split maps, the inverse compositions, the image/idempotence deductions, the parameter-zero fiber, the direct smoothness proof, or the reconstructed written nonpolynomiality argument. The inherited theorem is explicitly attributed, the classical reduction is not advertised as new, ambient dimension four is excluded, and the unreproduced Lean kernel build is disclosed consistently.

## Exact version and custody

The reviewed release candidate was frozen throughout this review:

| File | Bytes | SHA-256 |
|---|---:|---|
| `publication/upload-kit/paper.pdf` | 74423 | `3fd17ac91b2f640931988bbd65ae8d8b48cc9b6253c2befa17b4c47171441f52` |
| `publication/upload-kit/source-and-verification.zip` | 150707 | `646723cd3a3bd20d6a862a9db06d7720a13ff94368c1d12937b1666fa101d19f` |
| `zenodo-deposit.json` | 2131 | `e3785367073600f672b90f66cb8a419084d97c3b11312c5cad2dff2b31bd1452` |
| `manuscript/main.tex` | 16720 | `db130ebf5e09d79e5cad18855f1c0eaee42e416d31943abecd4fd0bee4d2a48e` |

These release hashes match `publication/PACKAGE_HASHES.json`. The archived `main.tex` is byte identical to the current manuscript. All manifested archive payload hashes and sizes pass, as do all manuscript-source and formal-source provenance hashes against the read-only upstream clone.

Upstream HEAD and read-only remote-main query both returned `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The manuscript PDF hash is `91a1a2f28c960cba25dd268e0f5515f0cff31463e4342098bbd89f857dd82023`; §§3–6 source hashes are, respectively:

- `01c8fba41829052c46ae2e1c34ace91283808c3bcd5a6adcfa58cdca1ad7424c`;
- `37097f3689e0d41315a623c7d94e362141526f642ca8515682751f47a0ea5ae7`;
- `8c6e5470bfc09d98f6cca44b461d3894034cc7b90f2bd379e47990753192f6b2`;
- `a15737c05af4fe6ec7f4af2552250bb9366c19f7c47dea3e13f492529fd50bf8`.

No manuscript, verification source, upstream file, git state, publication state or tracker was changed. Temporary extractions, environments, rendered pages and independent transcripts are confined to `reviews/reviewer01/`. No external individual was contacted. Internal agents are automated auditors, not human referees.

## Actual scope

I read the original attached research/publication brief and root AGENTS.md; the complete candidate TeX and six-page deposited PDF; README, theorem/dependency ledgers, approach table, research log, source manifests, licensing and notices; all scoped stabilization, nonpolynomiality, bundle, formal-scope and priority audits; priority search/provenance material and verified bibliography; both certificate scripts and their fixture outputs; and the intended deposit manifest.

I read the actual pinned upstream manuscript's introduction, construction, degeneration, bundle, extraction, rigidity and affine-fibration sections, bibliography, preamble, manuscript-specific citation, root README and `lean/docs/047.md`. I also independently compared the actual Lean Model/Main declarations with the comparator, read the equivariant-lift and highest-weight/determinant-rigidity mechanisms, checked all 55 archived OAI module bytes against the pinned sources, and verified the recorded formal-source manifest. This was **not** a line-by-line proof certification of all 55 Lean modules and did **not** execute a Lean kernel build, an axiom report, or the comparator.

A separately delegated packaging auditor reviewed the frozen release independently, ran its source reproduction and PDF comparison, and recorded evidence in `reviews/reviewer01/packaging/PACKAGING_REPRODUCIBILITY_AUDIT.md`. That subaudit excludes mathematical correctness and does not substitute for the reconstruction below.

## Finding requiring correction

**R01 — upstream theorem number, manuscript lines 57 and 275.** Both `\\cite[Theorem 1 ...]{OAI}` references are inaccurate for the pinned version. The source uses section-numbered theorem environments, and the actual PDF page 2 explicitly prints “Theorem 1.1” for the exact algebra and cylinder/nonpolynomiality theorem. Its final proof is also labelled as the proof of Theorem 1.1. Use `Theorem 1.1` in both candidate references and any corresponding numbered-source claims. This is a source-traceability defect, not a change to the mathematical dependency or conclusion. The archive and PDF currently reproduce the inaccurate references faithfully, so all intended publication files must be regenerated after repair.

No other substantive correction was identified.

## Independent reconstruction of the new explicit argument

The equation is exactly the upstream equation, over complex scalars, with unital algebra maps throughout. After inverting p the inverse coordinate expressions recover s,F,J from independent x,y,z,u. The identity `xy-z(z+1)=p²(H+pu)` makes H a coordinate with unit u-coefficient −p. Since p does not divide H, irreducibility descends through the polynomial UFD; this establishes that A is a domain with nonzero p without nonpolynomiality or stabilization. The fraction field is C(p,x,y,z), hence transcendence degree four.

The displayed Phi formulas preserve x,y,z, send H to H+p³w, and have both polynomial inverse orders using w→−w. A restriction of the localized locally nilpotent derivation to a preserved polynomial subalgebra is locally nilpotent, so the exponential explanation is valid as well. The direction `A[w]→P[w]/(H+p³w)` is correct because Phi sends the defining ideal to the target ideal.

The determinant-one F,J→L,M frame really has the specified polynomial inverse. The Q, C, q1,q2 expressions and the H(L) expansion are consistent. The e0 identity shows L=L*+p³e0 in the target quotient, and the explicit W satisfies the equation identically. Thus gq fixes e polynomially and all other B-generators via the frame. For qg, L,M,p,s,u are fixed; its w difference is killed by p³. The domain/nonzero-p argument is already independently established, so cancellation is legitimate and not circular. This is a global quotient equality that includes the fiber p=0, rather than an isomorphism asserted only on D(p).

The generator retraction formula is evaluation of Phi inverse at w=0, where all exponential corrections vanish. The inclusion is gPhi with w substituted as W, with the sign of D consistent with that direction. Consequently `ri=epsilon theta^-1 theta j=1`, and `rho²=i(ri)r=rho`. Since r is onto and i is injective, `im(rho)=i(A)`. The algebra maps reverse on spectra: the closed embedding is Spec(r), the projection is Spec(i), and the affine-five-space point endomorphism is their composite in the stated order. Its scheme-theoretic image algebra is B/ker(r)≅A. No confusion of point-map image and algebra-map image remains.

At p=0 the formulas reduce to `(0,s,u,m+3u²W,−u kappa(m+3u²W))`, with W=−e−u kappa m. The new W is identically zero, giving idempotence without localization and without exceptions at u=0, s=0, x0=0 or m=0. The only displayed quotient q1/m is explicitly defined as the bracketed polynomial, so it introduces no division.

Smoothness follows directly on D(p) from the Laurent polynomial presentation. At p=0 the F,J partials are x0² and −(1+2sx0); their displayed Bezout identity gives the unit ideal. The complex hypersurface Jacobian criterion covers every point. Smoothness is not inferred merely from the unreproduced Lean statement.

## Independent reconstruction and attempted falsification of §§3–6

The central inherited input is a mathematical proof rather than a numerical experiment. I reconstructed the following chain directly from the pinned source before accepting the scoped audit conclusions.

1. **Exact degeneration.** S is a domain, pS is prime, and S_(pS) is a DVR. Primality makes positive valuation imply global p-divisibility; repeated division gives valuation coefficients in R itself. The initial-generator map has exactly the prime, p-saturated kernel `(Htop)`. When a representative's top weight cancels, subtracting a homogeneous multiple of H reduces its maximum weight, bounded below by the actual valuation degree. This proves the entire associated graded presentation, including negative presentation weights. It does not simply guess a Rees algebra or assume generator initials suffice. The exact-representative result bounds derivation shift and makes the top induced derivation nonzero and locally nilpotent. Polynomial coordinates cannot all lie in F0 because F has degree two; a different partial derivative supplies the required positive invariant.

2. **Bundle and lift.** The z,z+1 charts cover, their transition functions are base units, and the determinant algebra is the line-bundle complement. The global principalization identities make I principal and faithful flatness embeds the actual pullback in the Laurent ring. Tau-regularity proves the single-relation presentation. G is a smooth domain, so its Picard group is invariant under adjoining a variable: horizontal divisors become principal over Frac(G)[t], and remaining height-one primes are pulled-back divisors. The normalized lift is unique because G[t]*=G*, and the cocycle follows from G[s,t]*=G*. The degree-torus lift extends to the total line bundle, so uniqueness proves the additive lift's valuation homogeneity. The additive derivation need not preserve R or Rt. I specifically tested this possible hidden assumption: the source's own homogeneous derivation moves u out of R, and the proof does not use its preservation.

3. **Signed extraction.** The exact homogeneous pieces of the pullback algebra force every positive-degree invariant to have factor V; factorial closure makes V invariant. If tau is invariant, invariant localization allows removal of tau's power and yields a weight-zero LND E fixing v. If tau moves, its LND value cannot be divisible by tau, forcing odd positive shift j=2l+1. Its values on Rt have multiplier tau V^(l+1), so removing that multiplier yields an honest Rt-derivation of fiber shift −2(l+1). LND order drops by m+1 on each nonzero E iterate, proving local nilpotence without localizing at a moving tau. Since nu(v)=2m, a second nonzero E(v) iterate would have order −2. Thus E²(v)=0, and E is nonzero in both cases.

4. **Rigidity.** The auxiliary grading is actual and commutes with fiber weight. A finite highest component of an LND remains an LND even if its shift is negative. The auxiliary-degree gap of nine makes its square kill N=d²+a²u³. Exponentiation gives nonzero orbit polynomials in the original field K=C(a,d,b)(u). A common root of the two summands would have multiplicity at least two in their nonzero degree≤1 sum; hence the abc inputs are coprime. Mason–Stothers then forces u to be constant on the orbit, and leading-term cancellation would make −u³ a square in K, contradicted by its odd u-order. Algebraic closure is used only for root counting, not for that nonsquare conclusion. The highest derivation fixes a,d,u; the determinant identity gives E'(b)=a h and E'(c)=d h. Invariant localization and the one-variable LND fact put h in C(a,d,u). Comparing a and d charts, with coprime denominators, puts h in C[a,d,u]. Its required fiber weight e−2<0 is impossible there.

The positive-root LND of fiber shift +2 really satisfies E+²(v)=0, confirming that the nonpositive sign is essential; the negative-root LND has nonzero second value. The computation of those boundaries reproduced exactly. Characteristic zero, domain hypotheses, smoothness for Picard invariance, the exact coefficient inclusion, and odd exponent three are all used at identified steps and all hold for this example. I found no unsupported equivalent-conjecture transfer, circularity, or material mathematical gap.

## Computational and PDF reproduction

I extracted the exact ZIP under `reviews/reviewer01/main_extract`, created a new venv under `reviews/reviewer01/venv`, and installed the archive's exact requirements. Python was 3.14.6, SymPy 1.14.0 and mpmath 1.3.0. Both archived scripts ran successfully, including the optional read-only upstream construction-hash check. Independent transcripts are `stabilization_run.json` and `nonpolynomiality_run.txt`.

The first script passed 32 integer polynomial identities plus 7 rational regression cases. It proves inverse-map certificates and supports the compositional proof, rather than proving idempotence or nonpolynomiality from finitely many points. The second passed the graded relation, four determinant principalization certificates, the positive-root square check and negative-root nonvanishing check. Its role is accurately limited to identities and examples.

I rendered and visually inspected all six exact deposited PDF pages. Formulas, references, page breaks and glyphs are legible, with no clipping or overlap. PDF metadata has the intended title and Alec Kriebel author; all fonts are embedded, the file is unencrypted and contains no forms or JavaScript. The separate packaging auditor's Tectonic 0.16.9 clean build matched deposited text and all six rendered pages byte for byte. Rebuilt PDF bytes differ because creation metadata differs; the package makes no byte-deterministic PDF-build promise.

## Provenance, novelty, formal scope and publication metadata

I independently reopened the relevant primary arXiv texts. [Nagamine v2](https://arxiv.org/html/1811.04153v2) contains the exact Costa formulation and Proposition 1.4, with the cylinder-to-retract proof and characteristic-zero three-variable result. [CDDG v1](https://arxiv.org/html/1910.11023v1) Theorem 5.8 applies to transcendence-degree-two retracts for arbitrary ambient n, as stated in the candidate. [Chakraborty–Pal v2](https://arxiv.org/html/2504.14382v2) has the cited current title and records the characteristic-zero n≥4 question as open in August 2026. [Epstein–Nguyen v1](https://arxiv.org/html/1301.3967v1) already records polynomial-extension retracts and Costa's stronger question. I inspected saved Crossref and GitHub records; bibliographic fields and the October 6 public-availability observation agree with the candidate.

The original Costa full text was not read in this review and the package correctly says its formulation was corroborated by primary reproductions. The September 23 manuscript date is not claimed as a verified public-disclosure date. Independent corpus searches produced seven Costa-name matches, all unrelated, and sixteen polynomial-retract/idempotent adjacency matches, none an exact duplicate. Fresh bounded web queries found no exact counterexample/transport duplicate. Logs are under `reviews/reviewer01/`; these searches cannot establish exhaustive priority. The new contribution is the explicit transport and verification presentation of a corollary already deductively available from the public upstream theorem and classical reduction. The candidate says this clearly and makes no independent-cancellation or first-priority claim.

The actual Lean model and MainStatement match the algebra, scalar-preserving equivalences, finite type, domain and Krull-dimension claims. The comparator's sorry is separate. The actual equivariant lift permits an invariant replica cD and then a highest component, while the determinant conclusion uses the independently proved sl2 highest-weight argument; the package does not silently equate those with every written intermediate lemma. All 55 archived modules are unchanged and the import closure is complete. Kernel compilation, axiom audit, comparator execution, smoothness formalization, transcendence-degree conversion and the follow-on retract formalization remain unverified/excluded as disclosed.

Title, sole creator, ORCID, date, preprint classification, exact two-file set, upstream relationship and descriptions match the reviewed paper. AI use and absence of conventional human peer review are disclosed. No unknown affiliation or coauthor is invented. No actual publication, DOI or tracker entry was checked or claimed by this review.

## Nonblocking package limitations and suggested housekeeping

- The source license copy is byte identical to the upstream Apache 2.0 license; the upstream root and Lean license copies agree, and no relevant NOTICE file was found. Original-artifact CC BY and upstream Apache scopes are documented, with attribution and no redistributed third-party research PDFs. Because the minimal `lean/lakefile.lean` is described as adapted but has no file-level modification header, adding a prominent header stating its adaptation would remove ambiguity about Apache §4(b). I do not infer a demonstrated license breach from generic functional configuration text.
- Metadata's single CC BY license field could mention the Apache upstream-file exception in its description, and LICENSES.md could map exact archive prefixes. Existing archive notices already distinguish the scopes; this is clarity rather than a missing attribution finding.
- Older scoped audit prose uses working-tree paths such as `verification/lean_copy` and references raw local mechanical logs not shipped in the archive. Root README and lean/README give the actual archived build location, and the mechanical receipt states the failures. This is a minor navigation/evidence-completeness limitation, not a claim that a successful build occurred.

Strongest checked conclusion: the written upstream nonpolynomiality proof and the displayed polynomial inverses support a smooth nonpolynomial complex algebra of transcendence degree four as a retract of C^[5], with the specified idempotent. The exact remaining publication gate is correction of R01 and a fresh complete-package review of regenerated files, followed by the separately authorized publication and tracker operations.
