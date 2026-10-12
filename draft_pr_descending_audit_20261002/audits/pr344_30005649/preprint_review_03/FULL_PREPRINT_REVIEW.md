# Independent full-preprint adversarial review 03

Actual report-writing UTC: 2026-10-04T08:02:23.474180+00:00. Scientific review completion: 100%; custody completion: 95%, pending the final read-only rehearsal and complete namespace manifest. This is a new automated adversarial review, not external human peer review. No merge, publication, deposit, release, installation, or external contact was performed or authorized by this report.

## Verdict and strongest verified result

**No mandatory mathematical, source-scope, disclosure, or package correction remains in the frozen revision04 eight-input candidate.** The theorem gives, for every prime p>3 and every n>=3, a p-killed finite flat commutative group scheme over W(algebraic closure of F_p), of rank p^(2n), with quasi-supersingular special fiber, and both objects fail Cartier self-duality. This reaches the exact unnumbered higher-n question following Takao Proposition2, printed2479, rather than the surrounding Coleman conjecture or the separate higher-genus question.

The main finite-module proof is independently valid. The more elaborate supplemental integral supersingular flag is also valid within its stated algebraically closed characteristic-p scope. The corrected public generic semilinear helper is valid; its historical bare-transpose predecessor is false, and the packet discloses and repairs that error with substantive regression controls. I did not treat historical sealed/closed/accepted/100-percent assertions as evidence for any mathematical conclusion.

This verdict is tied to `candidate_inputs.json`: all EIGHT author inputs, including the two real formula-correction builder dependencies, have been read and pinned. `public_members.json` binds all33 ZIP members, including modes, CRCs, byte sizes, and SHA256. It cannot be transferred to later candidate bytes. Exact file and source inventories, rather than a shortened list in this prose, are authoritative.

## Early independence and custody

I first read and visually inspected the Takao contribution in the original OWR PDF100–104 (printed2476–2480), and Hoshi's operative revised original §§2/3 and Definition4.8/Lemma4.9. I froze the target, hypotheses, boundaries, and falsification mechanisms at actual 2026-10-04T07:37:27.942650+00:00 in `SOURCE_ONLY_FREEZE.md`, size5122, mode0644, SHA256 d8e1c89543fc6523726a3217d9f27b9c54c3fb0bac28c8a93c150e4f319421b0. No candidate or prior verdict had been opened.

The candidate snapshot began at actual07:37:57.438906 UTC. I then read the complete TeX and metadata, the complete extracted PDF text, and all four original PDF pages visually. Before opening the ZIP, I froze `FIRST_MATHEMATICAL_ASSESSMENT.md` at actual07:39:00.874111 UTC, size4193, mode0644, SHA256 c04abb142e74560d1bad5b93d870cd697170ce9ca26eaa5374b37c405dac85c2. The ZIP extraction began only at actual07:39:28.734252 UTC. Native receipts and the two pin records establish these actual execution/write relations; filesystem modification times have not been represented as execution receipts.

Only then did I copy the specifically permitted original controls and raw primary PDFs/PS/metadata from the old namespace. I opened no other old-review files and no prior/root acceptance narratives. Embedded packet acceptance assertions were read because the full public packet was under review; they remained claims, not premises. All work and every mutation occurred in this owned namespace.

## Exact target, categorical assumptions, and finite construction

Takao fixes p>3, perfect residue field k, and W=W(k). The finite flat W-object is killed by p and has rank p^(2n). Proposition2's qss hypothesis concerns its **special fiber**, and its conclusions are self-duality of both special fiber and lift for n<=2. The question asks about n>=3. Choosing k to be the algebraic closure of F_p is a permitted counterexample to that universal assertion; descent to every perfect field is not required. Takao's qss factors are actual supersingular elliptic E_i[p] over the base, not merely slope-half vector spaces or alpha_p factors.

Hoshi Definition2.1 requires finite-dimensional k-module M, F Frobenius-semilinear, V inverse-Frobenius-semilinear, FV=VF=0. Deformability is the two exact image/kernel equalities in Definition3.4. Remark3.5.1 spells out the finite Honda system: finite-length W-module, semilinear F,V, FV=VF=p, V injective on the Honda submodule J, J→M/imF factoring through J/pJ, with the resulting map an isomorphism. All these conditions, not only a dimension count, are satisfied here. Proposition3.11 gives the **full** anti-equivalence for p!=2, reduction compatibility, and duality compatibility. The connected anti-equivalence is additionally available; the candidate does not need to weaken the full statement. Fontaine–Laffaille original printed602 §§9.4–9.5 independently agrees with the underlying finite Honda definition/equivalence.

For the six-dimensional M, the arrows are F:e0→e1→e2, e3→e4 and V:e0→e5→e4, e3→e2, with all terminal images zero. Therefore FV=VF=0, F^3=V^3=0,

    imF=kerV=<e1,e2,e4>, imV=kerF=<e2,e4,e5>.

These equalities hold with semilinear coefficients because Frobenius is an automorphism of the perfect field. The finite Dieudonné anti-equivalence produces an actual p-killed commutative k-group of rank p^6. The rank is the exponential of the module dimension, not the rank of F or V.

The ordered basis u=e1+e3+e5, v=e2+e4, w=2e1+e3, z=e2, a=e0, b=e1 has explicit inverse e0=a,e1=b,e2=z,e3=w−2b,e4=v−z,e5=u−w+b. Its determinant is1. The flag <u,v>⊂<u,v,w,z>⊂M is stable under BOTH operators. Its three quotient pairs satisfy Fx=Vx=y and Fy=Vy=0 exactly. The first two pairs are (u,v),(w,z), and the final pair is (a,b); quotienting removes the extra Fu/Fw/Va terms as claimed. The rank-two object I is deformable and has imF=imV, so Hoshi Lemma4.9 over algebraically closed k identifies it with actual supersingular elliptic p-torsion. No arbitrary height-two object is assumed elliptic without an identification theorem.

Exact contravariance reverses the flag: the group subobjects H_i have modules M/M_(3-i); the corresponding increasing group factors are the module factors in reverse order. This is an actual subgroup filtration with quotient E[p], and hence proves qss in Takao's definition. Confusing module subobjects with group subobjects would invalidate the argument; the manuscript gets the reversal right.

For the Honda complement L=<e0,e3,e5>, pM=pL=0, length_W M=6, and FV=VF=p because both sides vanish. The images Ve0=e5,Ve3=e2,Ve5=e4 are independent, so V|L is injective as a semilinear map. L is a direct complement of imF, so L/pL→M/imF is an isomorphism and the factorization condition is automatic. Hoshi's p-torsion finite Honda anti-equivalence produces an actual finite flat p-killed W-object, whose reduction has exactly module M. Over the local base finite flat rank is constant and equals the special-fiber rank p^6. This is not inferred from an integral Dieudonné lattice for a p-divisible group over k.

Appending n−3 copies of I, each with Honda complement kx, preserves every Honda condition and extends the qss flag. The resulting W-rank is p^(6+2(n−3))=p^(2n). This symbolic direct-sum argument establishes all n, rather than extrapolating from finitely tested sizes.

## Universal duality and intrinsic obstruction

The invariant delta(T)=dim(imF^2∩imV^2) is invariant under k-linear Dieudonné isomorphisms, since such an isomorphism commutes with both iterates. For M, the squared images are ke2 and ke4, giving delta0. Hoshi's actual dual definitions are F^D(phi)(t)=sigma(phi(Vt)), V^D(phi)(t)=sigma^-1(phi(Ft)). The prime-field basis matrices can therefore use transposed V,F with the specified semilinearity. Squaring gives im(F^D)^2=im(V^D)^2=ke0*, hence delta1. This proves nonselfduality of H; Cartier duality and base change imply nonselfduality of every finite Honda W-lift with this special fiber. Extra I blocks have both squared operators zero, including on their duals, so the obstruction persists for every n>=3.

I independently derived the generic formula for arbitrary perfect k. If F=A sigma and V=B sigma^-1, put C=A sigma(A), D=B sigma^-1(B). Then

    (F^D)^2 has linear part sigma^2(D)^t,
    (V^D)^2 has linear part sigma^-2(C)^t.
    ker(F^2)=sigma^-2 ker(C), ker(V^2)=sigma^2 ker(D).

Consequently delta(T^D)=rankC+rankD−rank[sigma^2(D)^t | sigma^-2(C)^t], equivalently dimT−dim(kerF^2+kerV^2). The opposite twists are essential. This derivation uses evaluation of the dual pairing and actual semilinear kernels, rather than accepting a transpose mnemonic. It is valid for all perfect fields, without assuming Frobenius has finite order two or three.

The disclosed minimal shear over F125 makes the old bare-row expression0 while the true dual invariant is1; the twists restore the common row. The corrected public derivative incorporates exactly this correction and fresh actual-kernel checks over F125,F343 and F32. The characteristic-two sample is explicitly generic algebra only and does not extend the p>3 group theorem. The dense-lower example can give old formula1 by coincidence; the packet honestly marks that individual old-formula mutant as not rejected. There is no false claim that every coordinate change detects the error.

My separate arithmetic uses tuples of polynomial coefficients and independently programmed elimination, with a DIFFERENT F125 modulus, F27 (generic characteristic-three only), and Frobenius-order-five F32. It checks a shear and fully nontriangular bases made from a permutation and24 elementary changes, direct evaluation of40 dual pairings per case, actual twisted squared kernels, basis invariance, and12 unrelated random4-by-4 operator pairs per field. All positive pairings succeed; the plain-transpose pairing mutant fails in all40 sampled pairs for each transformed case. An additional degree-four F625 coefficient has sigma^6(t)!=t and rejects treating the six-step identity as scalar p^3 on arbitrary coefficients. These finite controls corroborate the universal derivation; they do not prove the classification inputs.

## Supplemental integral construction and exact flag

The W-free lattice D has F weights(0,0,1,0,1,1) on the forward six-cycle, V=pF^-1 on the backward cycle. Both preserve D and FV=VF=p. The integral equivalence gives a p-divisible group **over k**, of height6 and dimension3, with p-kernel module D/pD=M. It gives no p-divisible lift over W. Six iterations give F^6(c_i e_i)=p^3 sigma^6(c_i)e_i; retaining the coefficient Frobenius establishes slopes1/2 without falsely trivializing sigma^6 on W(k).

I checked Oort's covariant conventions in the original author manuscript. The contravariant forward string ffvfvv corresponds through D_cov(G)=D_contra(G^D) to covariant vvfvff. Pries–Ulmer's written order and dual complement rule agree after explicit comparison. Complement and reversal coincide for this word only. Oort §§2.5–2.6 cover d=c=3 with gcd3: the original statement uses full height d+c, although its short proof misprints h=m+n after dividing by the gcd. The full-cycle F^6=p^3 sigma^6 identity independently resolves the example, without a coprime-only inference.

The trace-zero Witt coefficient construction is exact. The trace F_(p^6)/F_(p^2) has two-dimensional kernel because trace1=3!=0. For nonzero trace-zero abar, take t=[abar] and a=t−(t+sigma^2t+sigma^4t)/3. Witt Frobenius is additive, fixes3, and sigma^6t=t; thus a+sigma^2a+sigma^4a=0 exactly. Its reduction is abar, so a and all a_i=sigma^i(a) are units. This avoids the false assertion that Teichmüller lifting preserves sums. It supplies a_(i+6)=a_i and both even/odd trace identities with every denominator a_i a unit.

D1 generated by m1=e1+e3+e5,m0=pe0+e2+e4 is exactly standard S (FA=VA=B, FB=VB=pA), and is saturated through a unit minor. For the displayed quotient pi, the twelve commutation identities have respective right/left common values

| i | pi(F e_i)=F(pi e_i) | pi(V e_i)=V(pi e_i) |
|---|---|---|
|0|a1 B|a5 B|
|1|p a2 A|p a0 A|
|2|p a3 B|p a1 B|
|3|p a4 A|p a2 A|
|4|p a5 B|p a3 B|
|5|p a0 A|p a4 A|

These include both sigma and its inverse on coefficients. pi(e0/a0)=A and pi(e1/a1)=B prove actual surjectivity, so D2=kerpi is saturated, free rank4, stable for F,V, and D/D2=S. The exact trace identities place D1 in D2.

The four r-generators in the packet form a basis of D2; m0=r2+r4 and m1=r3+r5. In D2/D1 the quotient rules are Fr2=pr3, Vr2=p(a1/a5)r3, Fr3=(a0/a2)r2,Vr3=r2. For x=a1r3,y=a0r2, applying the correct coefficient twists gives Fx=Vx=y,Fy=Vy=px. The ordered full basis (m1,m0,x,y,e0/a0,e1/a1) has determinant1, so every quotient is integral and free. This is stronger than a finite-index inclusion or an isogeny-category flag. The public control checks71 formal Laurent identities, the full inverse, and both operators; my independent rational evaluations check the same displayed relations with separate arithmetic. Those evaluations are not a substitute for the symbolic trace and quotient calculations.

Actual elliptic existence is separately justified. The Legendre/Deuring polynomial Hp(lambda)=(-1)^m sum binom(m,i)^2 lambda^i, m=(p−1)/2, has positive degree, Hp(0)!=0 and Hp(1)=1 by Vandermonde modulo p. Over algebraically closed k it has a root away from0,1, giving a nonsingular supersingular Legendre curve by the criterion recalled in Auer–Top original §3. Yu Lemma4 is then applied to that ACTUAL elliptic module. Each arbitrary explicit quotient was already identified with S, so the argument is noncircular. Deuring/Igusa's original criterion proofs were not reread; the primary Auer–Top statement is the invoked classical input.

For a general supersingular integral lattice C, intersecting C with a rational rank-two flag gives saturated free F,V-stable lattices: clearing denominators establishes spanning; px in the intersection implies x lies in its rational subspace; V=pF^-1 preserves it. Rank-two quotients Q have length(Q/FQ)=length(Q/VQ)=1 by determinant valuation and pQ⊂FQ. Compare Q between p^rS and p^-sS; F^(2t)Q⊂pQ for sufficiently large t, so mod-p F is rank-one nilpotent. On a two-dimensional perfect-field space a rank-one nilpotent semilinear map has imF=kerF. Integral injectivity and FV=p give kerF modp=VQ/pQ, so a(Q)=1. Yu printed4's general maximal-a-number converse, not its elliptic-specific Lemma4, identifies Q integrally with S. This verifies the claimed general qss implication with named classical inputs. Nicole–Vasiu's rank-two exact sequence is an earlier instance, not an independently reread proof of every result in that paper.

Contravariance reverses the integral flag. In an exact sequence of p-divisible fppf sheaves, c in C[p] lifts locally to b; then pb lies in A and p-divisibility locally supplies a with pa=pb. Thus b−a lifts c inside B[p], proving right exactness. The kernel is A[p]. For finite0→Z/p→Z/p^2→Z/p→0 the middle p-kernel maps to zero, so unrestricted finite-group right exactness would be false. The packet uses exactly the necessary p-divisibility hypothesis. No rational isocrystal alone, k-point surjectivity, W p-divisible lift, polarization, Jacobian realization, or Coleman implication is claimed.

## Complete packet, derivations, code, and execution

All33 public member bodies were read, including complete inventories, supporting narratives, code, assertions, actual expected streams, metadata, and license. `audit_relations.py` checks every ZIP member against both its original archive bytes and extracted duplicate, all32 manifest payloads, the11 priority submanifest payloads, modes, and all declared control pins. It reconstructs the three exact original-to-public literal derivatives in sequence. `check_realization.py` and `construction.json` remain byte-identical to the allowed originals. The intrinsic inserted text is exactly the eighth-input regression dependency. Manuscript, metadata, verifier, and correction-note duplicates are exact.

The integral and semilinear document-reference edits leave their mathematical bodies unchanged. The intrinsic derivative deliberately changes mathematical code/assertions: opposite squared twists and added actual-kernel/minimal/dense regression tests; its provenance-output removal and two document-reference replacements are separately enumerated. The historical original's generic helper correctness is not inferred from any sealed status. Original inputs and original bytes are preserved.

I fully read the author builder but never ran it: it writes the shared candidate/archive and private execution workspace and consumes prior root decisions. Its declared curation and two additional dependencies agree with the package. I did not authenticate prior acceptance narratives, earlier HTTP execution receipts, or the literal origin of curated prose from prohibited prior report files. Instead I independently reviewed all resulting mathematical prose and the exact source/control derivatives that are available under the allowed read scope. Those limits do not create a mathematical gap in the self-contained main proof or the independently checked supplement.

Actual native replay used system `/opt/homebrew/bin/python3` **3.14.6** and bundled `/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` **3.12.14**. The actual captured version streams take precedence over an earlier promptly corrected message typo. Both use -B/no bytecode and unoptimized assertions. Public default, public --full, priority, Honda, semilinear, intrinsic, and integral controls exit0 with empty stderr. All complete positive stdout streams match across runtimes; the five individual streams also match the complete included expected output, not only a PASS token. Watched candidate, packet, and original-control snapshots stayed unchanged in size/mode/SHA before and after.

| Stream | bytes | SHA256 |
|---|---:|---|
|public default|730|3888dd21a98a3cda52423b524a03f3d20fe38d70d40165e88500bd12bfbfe1d8|
|public full|1605|70fda00dcd6036cfb8d724a3d3f6c8eb0613fc3d7d928a3d0e29d090ce19b9ce|
|priority|1673|72d2e655eb5f2596b019baebd35e56a63cecf5105cdc6f0d65b19205675896c3|
|Honda|2452|2dc82eb1f2e915325d5f2055605937d6bfda2c502107107bd90c11e0ab9fb0d5|
|semilinear|892|63c25b3aa86f6eb9c7d56a3f001c6dc4218363466f1a7e8ff11030f2bbb80c20|
|intrinsic|14594|bdcd06a4370d222bdc28decf52a65b4c5f708d900b769606b4452b3984f7974a|
|integral flag|796|d26330a5015595d128e5c725624933a29f561fdee0ed003d8ff2e86f8401191d|
|new independent arithmetic|5552|3433606115b13d8ed27759afb37cfc6b7dec923380df26255d1dd1f8acf64738|

The original suite ran actual07:42:35.351502–07:42:40.634386 UTC. The independent arithmetic produced3278 explicit requirements: 3.14 native07:46:32.340724–07:46:32.614292, 3.12 native07:47:34.362247–07:47:34.616889. Full stdout/stderr and command/cwd/start/end/status/pins are preserved in `receipts/`, not reconstructed from expected files.

Direct mathematical mutants, on BOTH runtimes, all exit1: old generic formula hits its minimal-shear assertion; inverse integral F coefficient twist reports integral flag unstable; scaling m1 by p reports integral basis inverse failed (independently determinantp is nonunit); changing Honda indices to[0,1,3] fails the complement/injectivity assertion. These execute mutated controls directly and never invoke a manifest verifier. The independent controls additionally reject plain-transpose duality, omitted V arrows, wrong trace coefficients, untwisted integral basis changes, the false sigma^6 identity, and finite p-kernel right exactness. Every rejection has actual native complete stderr or a positive control demonstrating the false identity; no test is credited merely for triggering a hash mismatch.

The owned `verify_review.py` public mode checks frozen custody/relations then freshly replays both default verifiers. Full mode replays26 actual subprocesses: versions, both defaults/fulls, each five individual controls, independent controls, and four direct mutants on each runtime. It reads only owned source snapshots; historical external-source paths are documentary fields. It checks complete namespace inventory/bytes/file+directory modes before and after, requires no optimization, and compares full fresh streams. It retains the frozen scientific verdict even when integrity is PASS; integrity is not a mathematical acceptance theorem. The recorded full preflight ran actual07:55:43.969740–07:55:50.836015 with unchanged namespace and no external-source reads. Its `UNFINALIZED_PREFLIGHT_PASS` is explicitly not final custody clearance.

## Source versions, historical gaps, metadata, and observations

`READING_LEDGER.md` specifies my own actual scopes; the packet's MECHANISM_SOURCES or older report full-reading claims are not silently adopted as my reading ledger. The operative Hoshi source is the March2021 revised author manuscript; no published JNT body collation is claimed. The inspected Oort body is the author PS/local PDF, not the final2005 journal body. Yu metadata establishes v1 submission12March2026. Nicole metadata establishes v2 dated6July2007 and a2007 journal reference, but its actual PDF says27August2018 internally. I independently checked those conflicting fields and do not assign these exact bytes unqualified2007 chronology. Pries–Ulmer's2024 correction concerns other arithmetic/de Rham arguments; the inspected §3 word construction and §4.1 complement duality rule remain the operative statements.

I reviewed every public source/search/version/gap entry as an inventory and claim:62 source rows,15 bounded search rows, the full version inventory including19 Zenodo records, and all14 named gaps. I did not reread all62 original works, reproduce the historical searches, authenticate their old network receipts, or prove absence of earlier combinations. Kraft's original, distinct Hecke drafts/exact-word leads, final-body collations, inaccessible Chai2025 material, unread background references, and legacy incomplete query receipts remain bounded historical limits. G07's mechanism can independently be closed mathematically by the derivations above; metadata/hashes cannot close a global priority search.

The manuscript explicitly attributes its cyclic module, duality classification, and balanced supersingular completion to classical theory and presents the explicit question-specific calculation without first-discovery/first-priority language. Its metadata, packet README, license and disclosure agree: Alec Kriebel, provided ORCID, date4October2026/version1.0, publication type preprint, CC BY4.0 for author material, extensive AI use, unrefereed status, automated reviews not external human peer review. Primary full text is omitted from the public ZIP and not relicensed. The four PDF pages have been visually checked; formulas, bars, attribution, references and disclosure are legible, without missing or clipped mathematical content. The short fourth bibliography page is acceptable.

Nonmandatory observations: the public verifier's generic integrity claims are bounded by its declared checks; my additional custody layer checks all file and directory modes. Historical acceptance strings are not scientific certificates. Finite tests cannot prove cited classification theorems or universal historical novelty. These observations are already consistent with the candidate's express qualifications and require no author repair. I found no concealed claim of W-qss, arbitrary-perfect-field descent, principal polarization, Jacobian realization, or Coleman resolution.

## Required repairs and root closure plan

Mandatory findings: **none**. Actionable author repairs: **none for these exact frozen inputs**. The earlier generic-helper error has already been correctly repaired in the submitted public revision and its historical qualification is adequate.

Root must read this report, the actual ledger, inventories, code and complete native receipts; independently pin the final namespace manifest externally; run `python3 -B verify_review.py --full` read-only with native stdout/stderr/UTC/command captured OUTSIDE this namespace; confirm the scientific verdict remains clean and the complete namespace is unchanged; and compare the current shared eight author inputs against `candidate_inputs.json` without changing this owned namespace. Any new input or scientific change invalidates this clearance and requires a fresh new adversary under the user's successive-review requirement. No self-seal or final runtime addendum will be created here after `FINAL_NAMESPACE_MANIFEST.json`. Merge and publication decisions remain root/user workflow actions, not actions performed by this review.
