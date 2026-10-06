# Independent whole-preprint adversarial review 02 — PR305 / 5100034

**Verdict: PASS within the expressly stated mathematical and preprint scope. Mandatory findings: none.** This is an independent AI review of the frozen revision, not human peer review, formal proof-assistant certification, or permission to publish, merge, change a tracker, or contact anyone. I made no candidate repairs.

## 1. Independence, acceptance criteria and inspection scope

I froze `acceptance_criteria_frozen.md` at **2026-10-05T01:19:38.808608+00:00**, before reading the candidate or any earlier verdict/report. Its SHA256 is `8f8fd90419b5acc0263f61952d1db1db3c5656d1644d87c94fdd9acc18048931`. I reconstructed the argument and wrote `independent_reconstruction.md` before consulting the original author proof, companion proofs, author source gate, imported record, or earlier capture provenance. No earlier preprint-review verdict or adversarial PASS was used as a premise.

I read the complete candidate TEX and supplement, all seven Python source files, pinned requirements, licenses, metadata, provenance and packaged result text. I then ran the six packaged checkers. I authenticated all candidate/submission/ZIP bytes, inspected all six supplied final rendered pages, independently reconstructed all main proof steps, inspected exact primary headers and relevant historical statements, and added distinct exact and numerical adversarial controls.

The complete mode/path/size/permission/hash inventory is `INPUT_AND_NAMESPACE_INVENTORY.json`. `source_reads.jsonl` retains timestamped read operations. `read_scope_notes.md` distinguishes full byte reads from selected primary sections and truncated tool displays; I do not turn a loaded or hashed file into a claim that every paragraph of every primary paper was cognitively inspected. The whole candidate itself was read. All new files are within this review folder. No candidate, native paper, Git state or external application was changed.

## 2. Exact identity of the reviewed package

The candidate has **23 payload files plus MANIFEST.json**. Its manifest is SHA256 `b82312f47046c9a530fea5050c4ab3771195fa31cf42d5e3537691d532df47bc`. Every advertised size/hash and the complete file-set equality passed. The ZIP has **24 distinct file members**, exactly the candidate files including its manifest; all members were decompressed, compared byte for byte, checked for duplicate/path-traversal entries and tested for ZIP CRC integrity. `authenticated_zip_members.json` gives every member's SHA256, uncompressed/compressed size and CRC.

| Submission input | Bytes | SHA256 |
|---|---:|---|
| focal-pedal-ratios-note.pdf | 73905 | `426e2f9809b6f02bf03ee564cad40ae41cc0cee68dfafb907257bd17c6f04686` |
| focal-pedal-ratios-verification.zip | 106547 | `08194099e1c287c8c71fd6693c8070d4db73d2fe43db7447de5924aaa919de8f` |
| zenodo-deposit.json | 3817 | `85b16b561dacb6a393f0ec40a4c88e54e8482aa5c41cd3e21a74f63b3cf6fcc1` |

The submission PDF is identical to the frozen candidate PDF. The original PDF used in the supplied final render receipt is also byte-identical to it. A final consistency run verified that candidate and submission bytes remained unchanged throughout this review. Neither submission identity nor a PASS string alone was treated as proof correctness.

## 3. Claim, assumptions and boundary cases

The quantities are the ordered **signed shoelace areas** of perpendicular feet on supporting lines: A± on original billiard chords and B± on boundary tangents, which are the outer polygon's sidelines. They are not ordinary original/outer areas, antipedal areas, segment-clamped projections, or unsigned lobe sums.

The theorem's primitive domain is a noncircular boundary ellipse, a strictly nested nondegenerate confocal **elliptical** caustic, N≥3, gcd(τ,N)=1 and 0<τ<N/2. These include convex and admitted star traversals. The explicit reversal/repetition extension is valid by signed area scaling. Hyperbolic/collapsed caustics, diameter walks and clamped/unsigned variants are excluded rather than silently included. The separate circle formula C0=sec²(πτ/N) is correct for the admitted regular stars.

The theorem distinguishes:

- **E:** A+/A− = B+/B−.
- **M:** B±=C0 A± with the same positive phase-independent C0 at both foci.
- **C:** phase constancy of that common focal ratio.

M and strict nonvanishing imply E. C is false. The text, supplement, README and deposit description consistently maintain this distinction, including acknowledging both the old invariant framing and the explicit erroneous imported constancy assertion. The primary printed question marks do not establish present-day open status or priority.

## 4. Independent reconstruction of the main theorem

### 4.1 Coverage of the geometric domain and actual feet

After uniform caustic normalization its axes are 1,k′ and the shared foci are (±k,0), with 0<k<1. Stachel's published Theorem 4.3, equation (4.9), printed p1614, explicitly supplies P(u)=(-a sn u,b cn u), v=2Kτ/N, a=dn(v)/cn(v), b=k′/cn(v), and the vertex shift 2v. Its first part supplies the shift for any fixed confocal pair; closure of the injective real boundary parametrization forces Nδ=4Kτ. Thus this is not merely use of a sufficient construction while overlooking other admitted closed orbits. Since 0<v<K, cn(v)>0, a>1, b>k′ and a²−b²=k².

The chord midpoint parameter is u, with endpoints u±v. Substitution of the Jacobi addition formulas gives the caustic tangent line (-sn u,cn u/k′)·X=1. The boundary tangent at P(u) is (-sn u/a,cn u/b)·X=1. Consequently the original chord at index j has phase w+v+jδ, while the outer sideline has w+jδ. Omitting the half-step would compare different traces; the candidate retains it correctly.

Substitution into F+(1−n·F)n/(n·n) yields both displayed focal-foot maps. The common conic relation cancels the apparent opposite-sign focal denominator, so the continued maps are rational meromorphic maps with just the displayed remaining denominators. On the real line these denominators have positive lower bounds 1−k and a−k. Complex dot products are explicitly bilinear. Consecutive outer normals cannot be parallel: their real angular difference is in (0,π); equivalently distinct consecutive boundary points are not antipodal because δ<2K. The actual outer intersections are finite.

Central inversion sends u to u+2K, commutes with projection while exchanging the two foci, and has determinant +1. This proves A−(w)=A(w+2K), B−(w)=B(w+2K) with no extra sign or missing index shift.

### 4.2 Periods, degree and pole completeness

Cyclic reindexing and the point period give periods δ=τ(4K/N) and 4K for each trace. Bezout and gcd(τ,N)=1 give the common real period L=4K/N. The argument does not require L to be the least analytic period. Under 2iK′, sn is fixed and cn is negated, so each foot vector is reflected in the horizontal axis and each area trace is negated. Hence both traces are meromorphic on C/(L Z+4iK′ Z).

These characters and quarter shifts agree with [DLMF §22.4](https://dlmf.nist.gov/22.4); the chord calculation agrees with its [addition identities](https://dlmf.nist.gov/22.8). The cited sn torus has periods 4K,2iK′ and degree two. cn need not descend to that smaller sn torus: the proof correctly restores the second imaginary row on the common 4iK′ torus.

At a common sn/cn pole, each rational foot-map component has at most a simple numerator pole and a denominator with a nonzero simple leading coefficient. Dividing makes it holomorphic. Thus common Jacobi poles do not leave unlisted poles.

For the original foot, sn u=1/k is the unique double root r=K+iK′ on the sn torus. Using the quarter shift, cn z−dn z=−k′²z²/2+O(z⁴), whence q(r+z)=(2/k)(1,i)z⁻²+O(1). The map is even about r. At its singular phase only one original-foot vertex is singular, since the primitive orbit has N distinct points modulo 4K. Its neighbors are regular; even when a neighbor is a common Jacobi pole (the N=4, δ=K situation), the earlier removability argument applies. The two incident determinants combine to half det(q(r+z),q(r+z+δ)−q(r+z−δ)). The second vector is holomorphic and odd, therefore O(z); the result has at most a simple pole. This excludes an otherwise real double-pole possibility without relying on parity.

For the outer foot, the two roots are r−v,r+v. They are distinct for 0<v<K and exhaust the degree-two sn fiber. At each root cn u=−ib/k, the common numerator vector is −ab²(1,i)/k, and the denominator derivatives are +b²sn v and −b²sn v respectively. They are nonzero. The residues are −R,+R, R=a(1,i)/(k sn v). Adjacent outer-foot vertices are genuinely singular together because the roots differ by δ. Their common-edge double coefficient is det(−R,R)=0. The other incident edges have at most one singular endpoint. Primitivity supplies exactly two singular vertices; N≥3 rules out the two-vertex pathology. This accounts explicitly for the cyclic closing edge and for N=3, rather than treating the sum as an open chain.

All original candidates are r−v−jδ; the outer candidates are r−v−jδ and r+v−jδ. Since δ is an integer multiple of L and r+v=(r−v)+δ, these reduce to exactly the possible pair r−v and r−v+2iK′, each of order at most one. There is no transfer of the main difficulty to an unsupported pole-cancellation assertion.

### 4.3 Signed positivity, including stars and closing edge

For either support ellipse (R,S)=(1,k′) or (a,b), n(u)=(-sn u/R,cn u/S) has det(n,n′)=dn u/(RS)>0 on the real axis. Its continuous angle lift increases by exactly π over 2K. Therefore a positive increment δ<2K gives a direction increment strictly between 0 and π at every real phase. This includes large coprime star windings, even when the polygon crosses itself.

The focus is strictly interior to each support ellipse. Its foot relative to that focus is a positive multiple of the outward normal. Every individual consecutive focus-relative determinant is therefore positive. The closing edge uses the same lifted increment because Nδ=4Kτ closes the direction after τ complete turns. Translation of the shoelace origin to the focus telescopes, so the actual signed areas A(w),B(w) are strictly positive. The other focus follows by central inversion. This proves the needed denominator nonvanishing; convexity of the foot polygon or unsigned lobe counting is not assumed.

### 4.4 Residue uniqueness and conclusion

If either possible pole of a trace were removable, antiperiodicity would make the other removable. The trace would then be holomorphic on the compact torus, hence constant; antiperiodicity would force zero, contradicting real positivity. Thus both traces have genuine simple poles at both locations, and their first residues are nonzero.

Choose C0=Res(B)/Res(A) at one pole. The difference B−C0 A has no principal part there, and antiperiodicity cancels the other one. No poles remain. Compact-torus holomorphy makes the difference constant, and its negative imaginary character makes it zero. Real evaluation gives C0=B/A>0, proving realness and positivity after, rather than before, the justified residue division. Applying the identity at w+2K supplies the identical constant for the other focus. The proven nonzero real areas now permit the two focal ratios. Reversal negates all four signed areas; a positive repetition scales each equally.

**Main mathematical judgment:** this is a complete argument under the stated domain and standard credited inputs. I found no hidden circularity, parity borrowing, missed pole, star-sign exception or unjustified division. Finite numerical tests are corroboration, not an essential premise.

## 5. Exact triangular nonconstancy certificate

The boundary squared axes are 21,16 and the caustic squared axes 189/25,64/25; their differences are both 5 and the caustic is strictly nested and nondegenerate. The displayed vertices lie on the boundary. The vertical and oblique support lines satisfy the exact caustic tangency equations. The packaged exact checks verify strict interior segment contacts and normalized-vector reflection, not just conic incidence.

Direct projection/shoelace computation gives A±=84(7√21±√5)/625 and B±=7(7√21±√5)/10. These are positive, B±/A±=125/24, and the focal ratio R=(7√21+√5)/(7√21−√5)>1. The centrally inverted triangle is in the same fixed caustic family, is a different positively oriented phase, and exchanges the foci, giving 1/R<1. This is an exact counterexample to C, not to E or M. There is no empirical assumption in this finite certificate.

I additionally checked an even-length repetition of this odd primitive orbit exactly: a six-entry repeated list doubles both focal areas and retains their unequal ratio. Thus one cannot import a primitive-even symmetry assertion merely from listed even length. The candidate explicitly makes the necessary distinction.

The classical attribution is appropriate. Querret's original printed p284 visibly gives the coefficient T/(4R²); his text discusses signed areas, and Sturm's pp287 and 290–291 explicitly treat signs and the circumcenter's quarter-area case. Fierobe's v5 header is 22 July 2019 and Lemma 4.1 on p9 distinguishes the two axial circumcenters. With central symmetry they are unequal opposite centers, so the signed pedal formula already gives unequal reciprocal focal ratios. The note responsibly claims a current exact certificate, not a new negative theorem or first correction.

## 6. Conditional triangular deduction from older geometry

I inspected the actual IMPA imprint (July 2021; ISBN 978-65-89124-43-6), Theorem 2.1 on printed pp13–15, and Theorem 2.3 on p17. The old incenter axes are m/a,n/b and rho=r/R=2mn/(X−Y)². The Helman–Laurain–Garcia–Reznik v4 header is **16 April 2021**, and §§3.4–3.5 on pp6–8 give the circumcenter axes n/(2a),m/(2b), original power D, and Bevan power X+Y+2D. The package's scalar checker reproduces the supplied side-length algebra modulo its declared w² relation and displays denominators.

The supplement does not simply synchronize two ellipse loci by their shapes. Euler plus the two powers gives |I|²+4rho|O|²=X+Y−4rhoD and 4O·I−|I|²=X+Y−2D. Substitution of the two locus equations yields alpha(Ix²−4m²Ox²/n²)=0. Independently reducing in t=m/n gives alpha=2(t−1)(t+1)/(t(2t+1))>0. Its alternative radical positivity derivation is also correct.

The oriented tangent branches vary real analytically because the normalized boundary point is strictly exterior to the caustic circle; its two contact directions never merge. Their second boundary intersections have positive quadratic denominators. Centers of the nondegenerate triangle are consequently real analytic on a connected phase circle. The product of the two analytic factors vanishes identically, so one factor is globally zero; branch switching at an isolated coordinate zero is not allowed. At the symmetric phase containing (a,0), the original power yields Ox=n/(2a)>0 and the second metric identity forces Ix=−m/a. Hence the global relation is Ix=−2mOx/n and Hx=(2+2m/n)Ox.

Set U=D−(X−Y)>0 and V=2(Y+D). The relation 2+2m/n=V/U makes the signed original/excentral pedal formulas proportional. The resulting multiplier V/(2rho U)=(t+1)³/(2t) is correct. The positive focal margin U²−(X−Y)n²/X=Y²(2t+1)/(t(t+2)) is correct. The circle limit is 4, while the noncircle manipulations do not divide by vanishing circle quantities. The eccentric endpoint is excluded rather than assigned a finite multiplier.

The literal isosceles example in the inspected triangular-orbits v3 primary is defective; the manuscript expressly excludes it from its deduction. Its header is 12 December 2021 despite an internal July 2020 date. The older generic vertex-CAS locus/rho arguments were not independently recertified in this review or claimed to have been recertified by the candidate. Accordingly the old-result implication is properly **conditional on the identified older theorems**, separate from the self-contained main all-period proof. I found no remaining synchronization gap or inappropriate triangular novelty claim.

## 7. Primary source fidelity, attribution and bounded priority

The actual RGK primary bodies support the exact edition map: v1 (26 April 2020), Table 5 p6 k605; v11 (29 October 2020), Table 7 p9 k606; journal Table 7 p349 k607. Definitions and the signed convention agree with the candidate's construction. The journal's primitive-even symmetry explanation is already prior proof of E in that case. The imported source record actually adds the explicit family-constancy assertion and dates the question too late; the candidate corrects those points without blaming only the dataset.

Stachel's actual published header gives European J. Math. 8 (2022), 1602–1622 and the cited DOI. Fierobe and Center version/date citations agree with actual PDF headers. The IMPA authors, title, year and ISBN agree with the imprint. KLS's actual arXiv primary body §4.1, equations (39)–(42), uses matched characters/principal parts plus Liouville; its primary arXiv abstract metadata binds DOI 10.1007/BF02704435 to Pramana 62:1201–1230 (2004). Roitman's published header binds its title/authors/pages/DOI, and its body explicitly uses meromorphic pole cancellation and Liouville in Poncelet problems. These sources justify the credits to established methods.

The companion proof bytes and held native retrieval receipts match the cited public commit URLs and hashes. PR261 §§5,7 contain the original-foot germ/neighbor cancellation and positivity; PR210 §§2–4 contain the actual tangent-foot map and adjacent collinear residues. Their final conclusions are parity restricted; the candidate explicitly rederives the local mechanisms and the common lattice instead of importing those final parity claims. The original TURN_1 proof bytes match SOURCE_PROVENANCE. I did not use the earlier reviewers' PASS verdicts to certify this all-period extension.

The three Ferudun primary PDFs were checked against actual public Zenodo API captures, including complete PDF byte size and advertised MD5. Their printed title/author/date and API title/version/creation fields agree: focal pedal-antipedal v1.0, record 23079799 (1 October 2026); Steiner-centroid v1.0, record 23089778 (1 October); outer-pedal v1.1, record 23088516 (1 October). All precede the recorded original submission on 2 October. I read their actual primary bodies. The focal paper's headline domain is least N divisible by four and its quantities are original pedal/antipedal; the outer paper's arbitrary-point headline domain is least N=2 mod4, with an additional centered odd theorem; the Steiner paper is an original/own-Steiner ratio for odd N. Their incompatible headline domains do not directly combine into full E/M. The manuscript avoids asserting new even-M priority where a general scalar bridge has not been separately closed.

The bounded non-location formulation is appropriate. No specific full-domain prior E/M theorem was identified in the inspected material, but this is not a proof of global firstness or a certification of originality. The six listed unavailable journal finals, uninspected video contents and unreproduced older generic CAS proofs remain coverage limits. Two held files named as unavailable finals are in fact HTML, not PDF, confirming that filenames alone do not provide those missing editions. Nothing in this review enlarges finite searches into universal literature coverage.

## 8. Code, native checks and reproducibility

All packaged source was read before execution. The scripts import only their declared local sampler or pinned SymPy/mpmath and standard libraries, make no network requests, and have no concealed candidate edits. `reflection_geometry.py` was imported by its safe asserting wrapper; its writing `__main__` was **not** executed.

Actual interpreter/library versions were Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0. Every fresh packaged checker exited 0 with empty stderr, and all six stdout files reproduce the packaged output bytes and SHA256 exactly:

| Fresh checker | Observed coverage/result |
|---|---|
| verify_exact | 3133 exact assertions; 89 finite lattice pairs; two exact triangle phases |
| verify_numeric | 1226 comparisons; 120 real configurations; 22 complex pole configurations at 70 digits |
| verify_triangle | General signed triangle formula and exact rational-parameter/excentral/reflection identities |
| verify_triangle_phases | 54 directly constructed cases at 90 digits; maximum normalized residual 1.23942909938361e−75 |
| verify_historical_power | Five exact reductions, all zero modulo the declared root relation; denominators shown |
| verify_reflection | 18 direct-reflection configurations across nine families at 100 digits; all stated predicates asserted |

`PROGRAM_PROVENANCE.json` was authenticated against the actual held original programs. Six origins match their recorded hashes. All are byte-identical except verify_exact, whose sole adaptation is exactly TURN_1.md→focal_pedal_ratios.pdf in its scope string. The newly authored reflection wrapper's public hash also matches. Original proof/dependency hashes match the held proof files. The public package contains no third-party PDF, text extraction or facsimile.

Saved native receipts retain actual argv, cwd, UTC start/end, exit, stdout/stderr paths/bytes/SHA256 and executed driver/input/import hashes. End times were measured after execution, never preinvented. The launcher records loaded modules; imported reflection source is hashed, and candidate bytecode writes are suppressed with -B and PYTHONDONTWRITEBYTECODE=1. The final consistency run checked **27 already completed saved native receipts** plus executed module/program hashes; including that final run there are **28** native capture receipts, all with stable output bindings. Sixteen are fresh PDF text-extraction subprocess captures. Existing primary extraction files are byte-identical to the new native extractions.

An initial exploratory reader selected the wrong author-supplied metadata schema; `read_scope_notes.md` records that source-navigation failure honestly. It was not a failing mathematical test or fabricated native receipt. The saved corrected recent-metadata checker verifies actual API/file bindings. Failed web publisher access is likewise retained as a limitation, not dressed up as a retrieved source.

Numerical outputs are explicitly finite **NONINTERVAL** diagnostics. Their tolerances and dps are not certified error bounds, nor do printed small residuals establish an all-period theorem. The paper, supplement, output text and deposit metadata all state this accurately.

## 9. Additional materially distinct adversarial controls

`independent_checks.py` supplies exact leading-germ reconstruction from Jacobi differential-equation Taylor data, an independent exact reduction of the historical synchronization coefficient, the even repeated-odd countercontrol, and the circular radius-squared multiplier calculation.

It also constructs feet directly from bilinear normals and projection, rather than importing the packaged q/Q formulas, for six 100-digit configurations:

| k | (N,τ) | Purpose | Smallest individual cyclic determinant observed |
|---|---|---|---:|
| 0.000001 | (3,1) | near-circle triangle | 0.86602463359578 |
| 0.000001 | (11,5) | near-circle large star | 0.2817324766679 |
| 0.3 | (4,1) | δ=K removable Jacobi neighbor | 0.588265569062578 |
| 0.3 | (29,14) | high primitive turning number | 0.092973047678575 |
| 0.999999 | (5,2) | near-degenerate star | 1.48624805623129e−9 |
| 0.999999 | (8,3) | near-degenerate even star | 3.81139549608133e−10 |

Each test checks individual determinants including the cyclic closing edge, real-phase multiplier constancy, reduced real periods, imaginary antiperiodicity, and bounded removable Jacobi-pole values. Circular Fourier sampling around the complex pole independently recovers the two residues; their ratio agrees with the geometrically computed C0. Two approach radii check the simple-pole asymptotic. All passed; the largest aggregate normalized diagnostic discrepancy was about 1.05e−20, dominated by finite-distance local asymptotics, not a claimed numerical error certificate. These tests strengthen falsification coverage but are not a replacement for §4's analytic argument.

## 10. Exact PDF visual QA and metadata

The supplied page-1 through page-6 images were each inspected completely. The held render receipt records successful rendering of the PDF byte-identical to the submission; no fresh render was needed. All equations (1)–(19), theorem/proof boundaries, source names, dates, links, formulas and references are legible, without clipping, overlap, missing glyphs or broken layout. The page-1 theorem continuation on page 2 and the page-3/4 proof continuation are coherent. The reference list continues cleanly onto page 6. Image hashes/modes are in the inventory.

The TEX, PDF and deposit metadata agree on title, author, ORCID, date and version 1.0. The metadata identifies a preprint, credits E's April 2020 observation and prior cases/methods, states the exact ellipse/caustic and signed-area scope, differentiates M from C, avoids absolute firstness and independently new-method claims, and gives conspicuous extensive AI-use/non-human-review/non-formal-verification disclosures. Text CC BY 4.0 and original code MIT licenses are present. The package does not claim that a DOI has already been assigned to this proposed deposit or that submission preparation is publication authorization.

## 11. Findings, strongest conclusion and remaining gap

### Mandatory findings

**None. No P0, P1 or P2 correction is required for the reviewed preprint/package.** No candidate file was repaired by this reviewer. This verdict supplies review evidence only; it does not replace the human's iterative-review or release decision.

### Optional precision improvements

- **P3, optional:** a separate Sturm bibliography entry would make the named Querret–Sturm attribution easier to follow; the current Querret primary citation already supports the formula, and the supplement credits Sturm explicitly.
- **P3, optional:** add “printed p17” beside IMPA Theorem 2.3 in the supplement. Its neighboring “pp13–15” correctly describes Theorem 2.1, but an explicit second page locator would remove possible ambiguity. The formula and attribution are already correct.

Neither optional item changes the theorem, source assessment or PASS and neither is a publication-blocking repair.

**Strongest verified result:** under the explicitly stated noncircular/confocal-elliptical primitive convex/star domain, the main written proof establishes a positive common phase-independent multiplier at the two foci, strict real signed-area nonvanishing and E. Reversal and positive repetitions preserve the identities. The exact triangle disproves C. The separate circular formula and the explicitly conditional old N3 deduction are consistent and correct within their stated scopes.

**Exact remaining limits:** this review does not prove absolute historical priority or exhaustive literature absence; it does not recertify the older generic locus/rho CAS proofs, unavailable final journal editions, or video contents; it is not interval-certified computation, formal verification or external human peer review. These limits are disclosed in the candidate and do not leave a gap in the reconstructed main proof under its credited assumptions. Hyperbolic/collapsed caustics, diameter walks, clamped feet and unsigned lobe sums remain outside the theorem.

Review completion estimate at final checkpoint: **100% of this assigned whole-preprint review**, with the foregoing bounded historical limitations. After the final report/inventory hash handoff, this reviewer stops all file writes. No outreach, candidate modification, Git operation, publication, merge or tracker action was performed.
