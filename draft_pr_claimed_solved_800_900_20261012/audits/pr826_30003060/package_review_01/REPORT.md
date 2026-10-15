# Fresh independent package review 01 — PR826 / problem30003060

**Decision: CLEAR for the exact R1 seal, with no mandatory repair identified.** This accepts the package as an explicit elementary classical specialization refuting the literal unrestricted-field equivalence. It does not certify novelty, historical firstness, worldwide current openness, external human peer review, or formal proof-assistant verification. It does not resolve the characteristic-zero or general vanishing-to-Koszulness converse.

Review date: 2026-10-15 UTC / 2026-10-14 Pacific. The inputs are PACKAGE_SEAL_R1.json and prepared commit `16093447d41585cec65315332fdb7daea21057c9`, with original head `286cc67c0727b4decfd4f261a0591cd8823ebce9`. Trusted outer manifest SHA256: `c43861f2fe0e0282f49833dcd26b3d28cbee0e202653dbeb2b154a6cc86b027b`. Portable index SHA256: `e5122815c93723664c499a2c8c90d1bf01423f4ab522998416fb2effaa950181`.

I reconstructed the proof and source formulation before reading prior audit verdicts. INDEPENDENT_RECONSTRUCTION.md records that stage. Prior reports/ledgers were subsequently used as adversarial leads and checked against their primary anchors and actual bytes. I wrote only inside this review folder, used disposable replay copies, stayed on main, and made no Git, queue, PR, tracker, release, Zenodo, or external communication write.

## Exact mathematical result and independent derivation

The literal hypothesis being tested is: for a quadratic algebra over an unrestricted field, Koszulness is equivalent to vanishing of positive homological-degree higher Koszul homology, with coefficients A and fundamental e_A. The complete cached target, including its dated background and empty prior report, asks that iff. The title and background emphasize a converse, but they cannot turn a two-way written claim into a one-way statement without saying so. The complete OWR contribution printed479–481 states the same iff without a characteristic hypothesis; its front matter supplies no common field convention for independent talks. This supports the deliberately qualified literal reading, not a uniquely established historical intention.

Take A=T_k(V) with finitely many degree-one generators and R=0. Every W_j intersection for j>=2 has zero terms, so W_j=0. The ordinary coefficient-A complex is precisely

    0 -> A tensor V --b--> A -> 0,  b(a tensor v)=av-va.

It is different from the exact left-module resolution using multiplication mu(a tensor v)=av. Every nonempty word has a unique last letter, so mu maps the word/letter basis bijectively onto the augmentation ideal. That resolution is linear and free, proving Koszulness over every field.

There is also a direct check of the precise bimodule definition used by BLS. In each word w of length n, the n+1 cut positions give basis e_0,...,e_n for the w-block of A tensor A, and its n marked letters give basis f_0,...,f_(n-1) for A tensor V tensor A. The bimodule Koszul differential sends f_i to e_(i+1)-e_i and multiplication sends each e_i to w. These consecutive differences are independent and span the coefficient-sum-zero subspace over any field. This proves exactness of the augmented bimodule complex, including n=0, without relying on an unmentioned convention about Koszulness.

BLS final (28) with p=q=1 gives left cap e_A(a tensor v)=va with sign+1. Right cap gives -av. For an ordinary cycle z=sum a_i tensor v_i, b(z)=0 implies sum va=sum av even before quotienting. Thus the higher map is

    delta : ker b -> coker b,  z |-> [sum a_i v_i].

No ordinary boundary enters degree one because C2=0; no higher boundary enters it because HK2=0. A degree-zero ordinary boundary that kills the cap image is not a degree-one boundary killing z. This distinction is essential and is preserved by the proof and code.

For total word weight n>0 identify C1 and C0 separately with the word space E_n, by concatenation. The differential is I-rho, with rho moving the final letter to the front. In an orbit O of d distinct words, equality of neighboring coefficients gives ker(I-rho)=k*s_O, where s_O is their sum. The coinvariant block is k*[w]: all words agree there, and the coefficient-sum functional evaluates [w] to1. Neither fact divides by d. Cap induces

    k*s_O -> k*[w],  s_O |-> d*[w].

Its kernel and cokernel are each one-dimensional precisely when char(k)=p>0 divides d; otherwise they vanish. This proves the complete proposition in both higher degrees0 and1. No higher degrees occur. Weight0 contributes just k in degree0 and nothing in degree1. For V=0 there are no positive-weight words; for one generator every orbit has d=1, so none survive. The matrices and all deductions extend to any field with the same characteristic and commute with field extension. No finite-field, perfect-field, algebraic-closure, or characteristic-not-two assumption has slipped in.

For each prime p, w=x^(p-1)y has p distinct rotations, since its sole y occupies p different positions. Splitting these distinct words into prefix and final letter gives a nonzero chain z_p. Its b-boundary telescopes and delta[z_p]=p[w]=0. With no incoming boundaries of either kind, z_p gives a nonzero higher-H1 class in total weight p. For p=2 this is x tensor y+y tensor x. The same orbit adds a positive-weight higher-H0 class, so adding HK0^hi=k to the unrestricted iff cannot rescue it.

An explicit integral check makes the quotient step transparent: if b(e_i)=w_i-w_(i+1), then

    b(sum i*e_i, i=0,...,d-1)=sum w_i-d*w_0.

For p dividing d this shows that the cap image is an ordinary degree-zero boundary while its degree-one source remains nonzero. For x^p, d=1, so cap is nonzero; listing p repeated rotations instead gives a zero proposed chain. At weight6, (xy)^3 has d=2 and (xxy)^2 has d=3. The characteristic-two and characteristic-three behaviors consequently differ exactly as claimed.

## Source validity, classical credit and scope

All mathematical equations, assertions and four references in the three-page note were checked; CLAIM_CHECKLIST.md gives an assertion-by-assertion map. I read the complete original OWR contribution and the relevant original BLS/Loday–Quillen/Goodwillie contexts, rather than relying on audit summaries or a finite test output.

BLS final §2 allows R=0 and uses coefficient-A HK(A)=HK(A,A). Its §5.2 explicitly defines this fundamental-cocycle higher homology in every characteristic. The preceding arbitrary-derivation characteristic-not-two restriction does not apply. Final Theorem6.4 and contemporaneous v1 Theorem6.4 explicitly assume characteristic zero; the preceding discussion of displayed Conjecture6.5 considers removing that assumption and motivates a converse. The source supports the note's literal qualification, but not an unqualified statement that the intended characteristic-zero conjecture has been solved. The nearby low-weight vanishing result in final §6.3 also expressly assumes characteristic not2; it does not refute the exhibited characteristic-two class. BLS Proposition7.4 concerns higher cohomology, and modified duality changes coefficients; neither silently supplies the same coefficient-A higher homology statement.

Loday–Quillen §5, Lemmas5.1–5.2 gives the very small complex and explicitly unsigned invariants/coinvariants over the commutative ground-ring setting. Over a field the necessary flatness holds. Goodwillie II.4 works for a flat associative unital algebra over a commutative ground ring and (II.4.8) gives exactly e_D(a tensor v)=D(v)a=va for the Euler derivation. Its TheoremII.4.2 gives e_DB+Be_D=L_D on homology. These statements do not require characteristic zero; division-by-weight consequences later do. BLS supplies the named higher-invariant identification. This fully assembles the central mechanism from classical sources, with no unsupported bridge.

Loday–Quillen Lemma5.3 gives B in the opposite direction as the length-n norm. On an orbit of d distinct words, B has scalar n/d, whereas Euler cap has scalar d. Both composites multiply by n. On the primitive weight-p orbit, B has scalar1 and cap scalar0 in characteristic p. On x^p their behaviors reverse. The note does not conflate Connes homology with higher Euler-cap homology.

The current note, abstract, metadata, priority guide, repository README and prepared queue findings consistently credit an elementary classical application and preserve the converse/intent/priority limits. The prepared queue row remains exactly claimed_solved1/5 with qualified findings; all other queue bytes match the prepared base. The mechanism is not a newly discovered substantial homological theorem. Its explicit correction to the literal field scope is defensible as written even though first publication of the exact observation is unestablished.

I inspected the complete classical/recent/root source and query ledgers, rehashed21 primary-PDF ledger rows (all14 recent-lane primary PDFs included), and independently reread the closest later-work passages listed in SEARCH_AND_SOURCE_COVERAGE.md. Nine additional bounded fresh public searches found no identified earlier exact statement. None of these negative searches certifies worldwide absence. The recent package correctly updates Berger–Maillard to JPAA230(7),July2026,108303, DOI10.1016/j.jpaa.2026.108303. A fresh publisher result confirms this metadata; the complete final body remains inaccessible. I read the available v1 relevant passages and cached public introduction, not a nonexistent complete-final comparison. Other final/preprint and citation-index gaps remain explicit. The nearest general monomial paper already supplies the ordinary orbit basis, which reinforces the classical-credit requirement.

## Actual PDF and metadata

The accepted PDF is exactly74386 bytes, SHA256 `5d6e06baa81d5e50397354e48495f74800ccd8b8d4092cf4564caf43ca2c6e3b`. I rendered that included PDF at110dpi and visually inspected every page; it was not regenerated. Page1 includes the title, author, independent-researcher affiliation, exact ORCID, October14 date/version, abstract, scope and proposition. Page2 contains the full proof and witness/counterexample. Page3 contains the operators, verification/priority limits and complete four references. Equations, subscripts, footnote disclosures, references and page numbers are legible, with no clipping, overlaps or missing glyphs. PDF metadata title/author also agree. The page1 footnote expressly discloses extensive OpenAI use in development, solving, drafting, coding and adversarial verification, unrefereed status, and absence of completed external human peer review or formal proof-assistant verification.

Exact parsed metadata equality holds among canonical metadata.json, zenodo-deposit.json.metadata, portable metadata and PUBLICATION_METADATA.json. All ten canonical core files match both the seal and prepared assembly. The deposit wrapper names the intended accepted PDF and verification ZIP. Licenses/disclosures are consistent with authored content; underlying downloaded publications are excluded.

## Integrity and executed evidence

All executable programs in the invoked chain were inspected before execution, including the archived Python members and historical bootstrap differences. The current gates and current algebra/operator diagnostics contain zero AST Assert nodes. The intentionally preserved original author and second-review optimized refusals are correctly described as fail-closed controls, not optimized mathematical successes.

Independent read-only Git inspection checked all65 original blobs against frozen head and all217 prepared target blobs/modes against the assembly. Both prepared parents match; non-target queue bytes are unchanged. Independent archive inspection checked all four original archives, unique safe regular paths and all55 member byte/hash bindings. The140-member portable ZIP exactly matches the extracted portable tree. All114 JSON files in the prepared assembly parse without duplicate keys; archived JSON members were also checked. The historical replay independently applied all three patches with zero fuzz and checked exact derivatives/proof bindings.

Actual executions used Python3.14 standard library and the available compatible system patch program. They occurred in disposable copies; the documented normal and optimized commands passed:

| Replay | Verified result / receipt |
|---|---|
| Repository outer entrypoint, normal and -O, --full |217 files;140 ZIP members;65 originals; metadata/PDF/current-vs-historical identity. `receipts/OUTER_NORMAL*`, `OUTER_OPTIMIZED*`. |
| Portable entrypoint, normal and -O, --full |140 regular files;14 historical child runs;4 archives/55 members;3 exact patch derivatives. `receipts/PORTABLE_NORMAL*`, `PORTABLE_OPTIMIZED*`. |
| Each complete arithmetic replay |2110 explicit checks,234 matrix/necklace cases,14 prime witnesses,10 negative controls; corrupted expectation rejected before acceptance output. |
| Each complete classical-operator replay |21 cases/604 orbit blocks; wrong Euler scalar rejected before acceptance output. |
| Documented builder from assembled preprint directory, normal and -O |Both package_index.json and verification.zip rebuilt byte for byte. `receipts/BUILDER_NORMAL.json`, `BUILDER_OPTIMIZED.json`. |
| Provided root integrity suite on disposable copies |34 cases:2 baseline acceptances and32 expected rejections. Full generated receipt copied to `receipts/ROOT_INTEGRITY_34_CASES.json`. |
| Fresh independent extra controls |36 cases:34 expected rejections plus2 complete extracted-ZIP replays safely accepted amid hostile cwd/PYTHONPATH/PYTHONHOME/PYTHONOPTIMIZE. `receipts/ADVERSARIAL_CONTROLS.json`. |
| Complete original provenance |All three full original corpora, unique problem/full-pair/catalog binding and seven primary PDF pins pass; raw material not copied. `receipts/FULL_ORIGINAL_PROVENANCE.json`. |

The extra controls include hidden files, empty descendant directories, root/member symlinks, wrong external pin, same-size replacement checker with a spy marker, duplicate nested JSON keys, boolean byte counts, unsafe dot/absolute paths and duplicate inventory paths. They also omit each required startup flag from both gates. The spy payload never executes. Structural fixtures explicitly use derived pins to reach inner validation branches; those are not replacement authorizations under the original release pin. A fresh extraction of the actual ZIP in a path containing spaces passes the full portable interface in both modes. Inputs remain unchanged after all runs.

The only promised complete portable interface is the documented verifier. The package correctly labels root_evidence scripts and older wrappers as dated contextual evidence that may need the original layout. Deterministic rebuilding preserves the accepted PDF bytes. Startup code itself requires independently trusted verifier bytes/pins as documented; a program cannot authenticate arbitrary replacement startup code. No operating-system-sandbox or malicious-system-Python guarantee is being inferred.

The parent later supplied corroborating builder-negative-control results; this review's decision does not rely on their verdict. My independent command, source, integrity, archive, replay and rebuilt-byte checks supply the evidence above.

## Findings, remaining gaps and disposition

**Mandatory defects: none identified. Required repairs: none.** This conclusion applies only to the exact reviewed seal. The finite diagnostics and hash gates supplement the independent unlimited algebraic argument; they are not proof-assistant or priority certificates.

The exact remaining gaps are unchanged: characteristic-zero/general converse; unique historical intended field scope; historical explicit first statement and worldwide current openness; complete final-body comparisons for inaccessible related journal articles; completed external human peer review and formal proof-assistant verification. These are limitations openly excluded from the submitted claims, not missing steps in the literal counterexample proof.

The package is still explicitly staged awaiting its release workflow. Before distribution, the external final acceptance receipt referenced by the README must carry the accepted pins and verifier hash, and publication must use these reviewed bytes; that is the already documented trust/release step rather than a defect in this review-stage seal. This review creates no deposit, publication, push or merge.

`receipts/INPUTS_AFTER.json` verifies all ten core hashes and all217 assembly entries exactly unchanged from `INPUTS_BEFORE.json`; all65 source files still match the original manifest and branch remains main. Review completion estimate:100% for this requested independent review, without implying a newly established novelty result. DECISION.json records the machine-readable disposition; MANIFEST.json lists this review's public authored outputs and receipts, excluding raw private material and disposable copies.
