# PR49 actual current whole-package adversarial review

The frozen current package is consistent with the credited known solution of the exact selected unrestricted-limit problem. I found no mandatory mathematical or current-package correction. Recommend **already_solved**, with credit to Kraus, Roth and Ruscheweyh (2007), original0/5, new0, audit0, project_solved false and novelty false. No paper, new DOI or tracker row is warranted. This report supplies a reviewer verdict for the actual current package; it does not supply ROOT approval, future integration authority, or an independent certification of the full imported journal proof.

The reviewed manifest is `8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47`: 1,544 payloads plus self, 273 relative directories, all payload/self full0444. The scope is PR49 / integer id30000703 / OWR-1460-009. This is a different investigator from both prior mathematical families and the current SOURCE preparer/reviewer. I inherit unrelated PR46 SOURCE work and PR50 original preparation. I read the two prior PR49 mathematical reports before writing this derivation, so this is not a blind new mathematical family. My mechanism is a bounded whole-package audit with a complete analytic reconstruction of the application, a defining-function converse that covers arbitrarily tangential approaches, and a separate affine angular countercontrol. Early independence of the older mathematical families remains attributed to their own dated records.

## Exact claim and independently checked deductions

Let f be holomorphic from the open unit disk into itself, and set

\[
\Phi_f(z)=\frac{(1-|z|^2)|f'(z)|}{1-|f(z)|^2}.
\]

The hypothesis is the ordinary unrestricted limit \(\Phi_f(z)\to1\) as \(z\to1\) from inside the disk. The denominator is strictly positive. Constants in the disk have distortion zero and cannot satisfy the hypothesis; a constant unimodular map is outside the codomain assumption. Schwarz–Pick gives \(0\leq\Phi_f\leq1\).

Choose \(\delta>0\) such that \(\Phi_f(z)>1/2\) for every disk point with \(|z-1|<\delta\). Shrink delta below1 and take the open circle arc \(\Gamma=\{\xi:|\xi|=1,\ |\xi-1|<\delta/2\}\). For each fixed xi in Gamma, the positive distance \(\delta-|\xi-1|\) supplies a full interior neighborhood of xi in the original ball. Therefore its unrestricted liminf of Phi is at least1/2. This is a valid point-to-collar argument: it transfers one uniformly positive neighborhood bound, rather than exchanging pointwise and uniform limits on an arc. Endpoints are not used. A positive unrestricted liminf at1 would already suffice for this step.

The imported open-arc theorem applies precisely to those hypotheses and supplies a holomorphic extension across Gamma with unit-circle values there. This is the central established theorem being imported, not something the finite diagnostic counts prove. No prior boundary regularity, boundary derivative, injectivity, absence of interior critical points, or uniform convergence on a preassigned arc has been assumed to obtain its hypotheses.

Write eta=f(1), so |eta|=1. The extension is nonzero in a small neighborhood of1. The harmonic function q=−log|f| is positive on the disk side and zero on the arc. Nonvanishing of f'(1) can be proved without assuming it. Place a sufficiently small internally tangent disk of radius epsilon, centered at1−epsilon, within that neighborhood. On its inner concentric circle of radius epsilon/2, q has a positive minimum m. On the intervening annulus, comparison with

\[
h(z)=\frac{m}{\log2}\log\frac{\epsilon}{|z-(1-\epsilon)|}
\]

gives q≥h: the inner boundary has q≥m and the outer boundary has q≥0. Along z=1−t, \(h(z)/t\to m/(\epsilon\log2)>0\). Since q is smooth across the boundary, its inward derivative is strictly positive. Differentiating |f(e^{it})|²=1 at t=0 shows Im(conjugate(eta)f'(1))=0. The outward radial derivative of log|f| equals Re(conjugate(eta)f'(1)), which is positive by the barrier. Thus

\[
\overline\eta f'(1)=\alpha>0,
\qquad f(z)=\eta+\alpha\eta(z-1)+O(|z-1|^2).
\]

This proves local conformality by the inverse function theorem. Analytic continuity gives an unrestricted boundary value, rather than merely an angular value. At a general arc point xi, the oriented positive quantity is xi·conjugate(f(xi))f'(xi). The displayed alpha is correctly normalized for xi=1. Shrinking to avoid zeros also makes the reciprocal-conjugate circle reflection formula well-defined locally. It yields no whole-circle assertion.

For the converse, a radial l'Hopital argument alone would leave a serious tangential gap. Here is a uniform factorization. Put \(A(r,t)=1-|f(re^{it})|^2\) in a small polar rectangle around (1,0), using the extension. Since A(1,t)=0,

\[
A(r,t)=(1-r)\left[-\int_0^1 A_r(1-s(1-r),t)\,ds\right].
\]

Consequently \(A=(1-r^2)H\), where H is continuous throughout that rectangle and

\[
H(1,0)=-A_r(1,0)/2
=\operatorname{Re}(\overline\eta f'(1))=\alpha>0.
\]

For all nearby interior points, \(\Phi_f=|f'|/H\to\alpha/\alpha=1\). This remains valid when 1−r is arbitrarily small compared with |t|. No remainder is divided by an uncontrolled disk-boundary distance. This proves the application-level equivalence and consequences while leaving the deep arc-reflection theorem honestly imported.

## Attempts to falsify scope and weaker hypotheses

The affine map \(g(z)=(1+z)/2\) maps the disk strictly into itself and is entire. Write z=1−s+iy and Q=s²+y². Its exact distortion is

\[
\Phi_g(z)=\frac{4s-2Q}{4s-Q}.
\]

For every non-tangential approach, |z−1|≤C(1−|z|) for a fixed C, while 1−|z|≤s. Hence Q≤C²s², Q/s→0, and Phi tends to1. On the interior tangential path z=1−t²+it, 0<t<1, the disk deficit is t²(1−t²)>0 and Phi tends to2/3. Moreover, |g(e^{it})|²=cos²(t/2)<1 away from t=0 on a sufficiently small arc. Thus even a finite positive angular derivative, analytic extension itself, and angular distortion limit1 do not imply the required circle-mapping extension. This concrete countercontrol exposes exactly why the unrestricted quantifier is essential. It is a counterexample to a weakened claim, not to this package.

The earlier half-plane logarithmic example independently separates angular and unrestricted behavior more strongly; I did not need to repeat its large control set. The package accurately keeps it attributed to its existing mathematical family. The source's two full-hypothesis controls also remain correct:

* For f(z)=z², Phi=2|z|/(1+|z|²) tends to1 unrestrictedly at1, but f is not globally injective and f'(1)=2.
* For \(f(z)=\eta\exp[-a(1-z)/(1+z)]\), a>0 and |eta|=1, let u=Re((1−z)/(1+z))=(1−|z|²)/|1+z|²>0. Then Phi=au/sinh(au) tends to1 at1. Its derivative is a·eta/2, so alpha may be any positive number. The essential singularity at−1 excludes whole-circle continuation and finite Blaschke status.

The metric normalizations 1/(1−|z|²) and2/(1−|z|²) cancel in the distortion ratio. They do not change the theorem or introduce a factor2 into alpha. The adjacent conformal-metric boundary-regularity Problem2 is a separate question and is never included in the verified target.

## Primary sources and priority qualification

I freshly read browser-extracted text of [Roth's original OWR contribution](https://ems.press/content/serial-article-files/46093), printed528–530. Theorem1 gives the needed arc implication and Problem1 uses an unrestricted limit; Problem2 is distinct. I checked [the versioned 2024 PDF](https://arxiv.org/pdf/2410.13965v1), §8.2, printed31, eq8.3, which explicitly identifies the same single-point equivalence and credits the older result. These direct statements support already_solved; the weaker angular results do not replace the target.

The [publisher record](https://link.springer.com/article/10.1007/s11854-007-0009-x) verifies Daniela Kraus, Oliver Roth and Stephan Ruscheweyh, Journal d'Analyse Mathématique101(2007),219–256, DOI10.1007/s11854-007-0009-x. It offers subscription-preview text, so I did not inspect or independently certify the full journal proof. This is an exact credited theorem application, not a priority claim for new mathematics or an exhaustive absence-of-literature assertion.

Fresh primary checks here were browser text only. No new PDF-byte authentication or pixel inspection is claimed, and no foreign PDF/cache/SQL body was copied into this family. The two earlier mathematical families' authenticated PDF and9/12-page render inspections remain historical evidence under their own bindings. The initial guessed MFO URL and direct DOI resolver failed through the browser tool; the actual EMS and publisher URLs succeeded. The HTML endpoint labeled v1 displayed an August2026 date, while the versioned PDF displayed the 2024 header; only the PDF extraction was used for the version-specific confirmation. This discrepancy creates no replacement of the authenticated historical PDF evidence.

## Actual reproduction and whole-package accounting

Every current payload and dependency body was read in place and its byte count, SHA256 and full mode checked. `CURRENT_READ_LEDGER.json` contains3,087 unique body/mode rows, with the exact273-directory packet topology and 1,407 dependency rows. No unrelated15458-row SQL audit,4096-mode probe, repeated filesystem-mutant suite, or wholesale old evidence copying was performed. Existing closed records with different schemas remain intact and are handled according to their actual conventions.

Successful private inspector child62254 ran08:37:05.872310–08:37:07.158823UTC, exit0. It checked the complete actual final50 inner command records and100 streams against the frozen48-record prefix, which is honestly labeled a prepublication prefix. The original actual builder/operator sources, final split stdout/stderr, PIDs, exact argv and enclosing capture chronology match. Actual operator47574 encloses builder47575 and all inner commands. The genuine ROOT final inspector50553 ran after builder exit. Its preceding failed49453/49723 captures remain preserved and are not counted as successful inspections.

The complete new SOURCE record9b669194d6e083b0a55d062bb08718fde55869d866182e38476b9afeeebf07fd is bound separately from the packet. All74 closed SOURCE-adversary members, its actual self-only manifest53a1e404afcfd79aae8d222c682dde55dea009917e8ad0d7917a634a62876e30,1,312 external rows, and four actual SOURCE/adversary closure/readback capture sets match. ROOT prerequisite author47212 completed before the actual freeze. These are genuinely completed records, not child-authored approval substitutes. Their pending whole-review and false future-acceptance fields are preserved.

Fresh literal helper replays were confined to three private copies:

| Actual child | Literal helper | Result |
|---|---|---|
|60270|author verify.py|69 passed,0 failed|
|60400|duplicate submitted_verify.py|69 passed,0 failed|
|60399|historical independent_checks.py|187 passed,0 failed|

Child63339 checked byte-identical saved receipts, every recursively compared scalar type, and728 strict current JSON objects with duplicate-key and nonfinite-number rejection. SymPy1.14.0 matches the saved receipts. The duplicated69 program is not independent mathematical evidence. Child62256 passed13 additional exact symbolic controls for the affine tangential distinction, defining-function quotient, derivatives, singular-family limit and Hopf-barrier sign. These finite controls support the written deductions and do not prove the imported arc theorem or any future acceptance code.

All16 original source bodies remain literal in original_archive, and all11 designated operative science/helper/result/source/turn/checksum items are byte-exact. The plain original source id is an integer. prior_report.json is exactly null plus newline, distinct from the absent upstream report key and SQL importer fallback{}. turns.json is one object with count0 and empty substantive_attempts; it has no separate original source-response count. The closed boundary review's administrative source-response description does not create an original attempt or ledger entry. Full raw importer validation is attributed to ROOT's earlier actual record, rather than claimed as a fresh rerun here.

The local native4 proposals are genuinely local. Their frozen preimage copies match the dated input bytes; their current0444 modes are distinct from the original live0644 observation. Only the selected QUEUE row's allowed Status/Turns/Findings cells may differ. Chat, DOI, all other cells and all other rows are exact. State, history and inventory prospective bodies are unchanged. The stable nine live input bodies/modes matched. These checks do not certify mutable live native4 or a future main head. Fresh13/currentmain and independently reviewed acceptance source remain ROOT's later responsibility.

The current qualified metadata clearly credits the known full target while denying project novelty. Historical source assessments, model/deadline/PASS/source-access claims and old pending preparation sentences are retained as dated attributions. The actual successful freeze does not convert them into new runtime claims or ROOT native approval. Extensive AI use and unrefereed status remain explicit; no human peer-review or formal-verification claim appears.

## Retained private failures and exact remaining gate

Three private inspection failures remain with full prelaunch sources, complete split streams, args, PIDs and UTC: child59270 wrongly expected integer0 instead of the actual empty corrections list; child59973 wrongly compared typed SOURCE directory rows with a string directory list; child61152 wrongly equated a frozen0444 proposal copy with its historical live0644 observation. Distinct V2/V3/V4 source versions retain all prior text. The successful V4 corrects these checker assumptions only; it does not repair or modify the candidate. Necessary re-reads after those failures are disclosed and are not invented as independent evidence.

Whole-current review completion estimate100%, discovery0%. Mandatory corrections: none. The strongest verified result is the exact local reflection characterization as a credited established theorem application, together with the rigorous application-level quantifier, derivative, converse and scope checks above. The full2007 journal proof remains imported, not independently certified. ROOT must read this complete report/verdict, run the proposed self-only closer and separate read-only verifier in actual externally captured children, and reconcile the closed current review before any later integration. This family has not self-closed, authored genuine ROOT approval, written native/index/ref/remote state, merged a PR, published a paper, uploaded to Zenodo, or added a sheet row.
