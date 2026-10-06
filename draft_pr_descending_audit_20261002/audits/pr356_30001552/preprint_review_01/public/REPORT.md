# Independent adversarial review: PR356 preprint

Dated 2026-10-04 UTC. Internal research subagent preprint_review_01. **PASS; mandatory findings: 0.** No mathematical, original-target, attribution, package or presentation correction is required. Completion estimate at this checkpoint: 96%; root's concrete read and explicitly authorized closure are pending. This is an internal AI-assisted review, not external human peer review, global novelty certification or external publication.

## Source-first independence and exact target

I confirmed the actual original OWR source at root_sources_private/owr2010-37.pdf, read the complete Nowotka contribution joint with Bischoff (printed 2219–2222 / PDF 25–28), and visually inspected all four pages. I froze a source-only baseline and gate before candidate or prior-audit exposure. They contain exact definitions, hypotheses, boundary cases, attribution limits and independently designed falsifiers. The source alone does not catalogue-map the task. Root subsequently explicitly mapped Target A and released the candidate.

Target A is the unnumbered antimorphic alternating-period conjecture immediately after Theorem 23 on printed 2220. It differs from the morphic unbordered-factor Conjecture 27 on printed 2222. An alternating period p means that w is a prefix of u theta(u) u theta(u) ..., for a nonempty initial p-block u. Partial final blocks are allowed. The theorem assumes arbitrary antimorphic involution theta, positive p,q and L=|w|>=p+q-gcd(p,q), and concludes alternating period gcd(p,q).

The original PDF is463460 bytes, SHA256 `e88f211c5be990a68a967f3a9549f5db042279e8473e2cb126ea1e3caaebf98c`. Baseline SHA `49ea2de9377630aa59ab03f6a3a7a5bae93b2dafc83fd14966233530e3e37db7`; gate SHA `bf908d2eb291b42f2c02aafe448583e376250b6aa1c4b77639fa4dc00929eab1`. All eight original gate payloads remain unchanged, with the growing research log checked through its immutable gate-time backup.

After explicit release I read all TEX/PDF content and visually inspected all three candidate pages. I froze my independent analytic verdict and falsifier design before opening ZIP content, prior audit verdicts, included control code or deposit metadata. Analytic verdict SHA `13662305961cc3488ae736dd4e2ab71c21b13f6400f74e5d3ab2533e1a5c046e`. Dated exposure declarations are preserved. Later comparison with the included audits did not substitute for independent reasoning.

## Universal mathematics and sharpness

The proof is valid. Involutivity gives bijectivity; a bijective (anti)morphism preserves atoms of the free monoid. Thus theta is a letter involution sigma followed by reversal. Fixed letters and an infinite alphabet are allowed.

Set d=gcd(p,q). The threshold implies L>=max(p,q)>0, making both roots valid. Extend an alternating p-template to all integer positions. Its central boundary reflection is s[-1-i]=sigma(s[i]). Restricted to [-L,L-1], it is exactly the SAME finite word theta(w)w, for either the p-template or q-template. Therefore that concrete finite extension has ordinary periods 2p and 2q. Agreement of two infinite extensions outside this interval is never assumed.

Since 2L>=2p+2q-2d, classical Fine–Wilf gives ordinary period 2d on the extension. Its central 2d block is theta(v)v, where v is the initial d block of w. Chaining period equalities within the finite interval transfers this center pattern to every position of w and recovers the alternating d phase. Obtaining a doubled ordinary period alone would not suffice; the reflection and center recover the required stronger conclusion. No completed final block, primitive root, minimal supplied period, finite alphabet or fixed-point-free involution is assumed. Equal periods, divisibility, d=1, exact endpoint and fixed letters cause no gap.

The reversal witness w=abb, p=2,q=3 has length3=p+q-d-1, both alternating periods, and no alternating1. The source prefix definition permits q=L. This establishes failure of a uniform one-step decrease. The candidate appropriately makes no claim of optimality for every fixed pair or every fixed involution.

My independently authored controls use literal repeated-block comparisons and import no package code. They check 14062 words,89984 extension equivalences,22232 qualifying unordered period-pair instances and14496 exact-threshold instances. Two binary models through length 9 each give 1022 words/8194 equivalences/2270 instances/1100 endpoints. Two ternary models through length 7 each give 3279/21324/5106/3354. A four-letter model through length 6 gives 5460/30948/7480/5588. Models cover reversal, reverse-exchange, an exchanged pair with a fixed letter, and two exchanged pairs.

Concrete negative controls reject the general theta-period definition mutant (reversal abba,p=2/q=3), wrong extension orientation w theta(w) (abb), ordinary gcd-period conclusion (reverse-exchange abab), and replacing antimorphicity by morphicity at the shorter threshold (letter-swap 0011,p=2/q=3,d1,L4). Uniform sharpness is checked directly. These bounded controls provide falsification evidence; the universal proof carries the theorem.

## Complete file/code review and genuine native runs

The released stable files are:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| alternating-antimorphic-fine-wilf.tex |10658|ccf85ea52eb1d2003b69344e23e5c4641f851b22155bc95cbe01775ca41b2cab|
| alternating-antimorphic-fine-wilf.pdf |68077|3ee2635930d4d107ff80cde1dfb7f8c57752fa833d0d212ba15c4ef7d4cdd81d|
| alternating-antimorphic-verification.zip |116605|2e9137b22696a454bea1b48df1ebc732eb1c20b6950da55a983b3b593c7ab1c2|
| zenodo-deposit.json |2168|fa6d6889ec68a782650231ed86308b06957ac93993c437064af8612274eb73e1|

Safe extraction produced exactly 69 members:68 payloads plus MANIFEST.json. Every member was completely inspected:18 text files,37 JSON bodies,12 Python programs and2 JSONL logs. All executable code was manually read before execution. Standard-library programs, manifests, full-stream comparisons and mathematical controls match the documented scope. No hidden installation/network requirement was found; raw primary PDFs are not in the public ZIP.

The historical 16-file submitted namespace is byte-preserved. Its original independent checker contains an old absolute workspace binding; the portable adapter executes the frozen mathematical tail against 7 public author files. Current public count 68408 differs from historical 68413 by 5 private-source checks. That older private mode is not reproduced or newly certified. The package limitations correctly explain the distinction.

Before each independent run I pinned all 69 package files, all 4 candidate files, runner, interpreter and full expected stdout. Assertions were enabled; bytecode writes disabled. Whole stdout/stderr, status, duration and before/after records are retained. Both package modes exited 0, produced empty stderr, matched the independently assembled COMPLETE expected output byte for byte and left all package bytes unchanged.

| Run | Finished UTC | Seconds | Stdout bytes | SHA256 |
| --- | --- | ---: | ---: | --- |
| default |2026-10-04T01:54:53.269564+00:00|0.272077|1586|cef38ef1a41ebcd26f090f73ef2991e2dbf8d6022c68c0f202d0f959e675fd9e|
| --full |2026-10-04T01:55:33.786437+00:00|40.509584|2960|9555386bf072f272e069bfec19c3cc665c9ace49486d6772069fc3a1171f73d4|
| own literal controls |2026-10-04T01:55:33.941001+00:00|0.146085|1443|3f5defdd0d8ba115fadf6449a101345265cf97d416015f391f69c53c93083a78|

Default executes all 4 public audit verifiers. Full additionally executes 6 programs: author, portable, signed-graph, word-overlap, definition-constraint and priority-comparison controls. Their complete native output hashes/statuses appear in the retained whole wrapper outputs. Preexecution-record SHAs: default `609fe490d1fc926dfd4f13def8a389500482d230f184ec2a4efc4b23b080247f`; full `9db5e7fbf8ad98a9f765de473ae2fd348fd7c7157d522c84b18003dcd37426a4`; own `4b70a613bd1bd10881579624c60066b9379cf3f3cf038cbdef76fbbc22329d5d`.

These are genuine independent executions, not root's earlier runs or substituted expected output. Checksums prove integrity relative to recorded bytes, not independent historical authenticity or human review. Whole streams and private captures retain the practical limits of that statement.

## Actual primary references, credit and priority omissions

I inspected the operative mathematical statements in official Fine–Wilf, Bischoff, Czeizler–Kari–Seki, Kari–Seki and Simpson PDFs. Where new official fetches failed, I read an existing separately hashed cached official PDF. I do not claim a new download or an independently rediscovered provenance chain.

Fine–Wilf's original theorem supplies the ordinary gcd-period step. The plural title, pages and official link are correct. [AMS original paper](https://www.ams.org/journals/proc/1965-016-01/S0002-9939-1965-0174934-9/S0002-9939-1965-0174934-9.pdf).

Bischoff's 2010 thesis Lemma 3.9 already contains the doubled ordinary-period/reflection connection, and Satz 3.11 proves the p+q alternating result. I inspected relevant statements/proofs and title/completion dates. Candidate credit to this mechanism and originating conjecture is appropriate; the shorter gcd endpoint follows through the common extension and classical theorem. [Official thesis](https://www2.informatik.uni-stuttgart.de/bibliothek/ftp/medoc_restrict.ustuttgart_fi/DIP-3095/DIP-3095.pdf).

Czeizler–Kari–Seki's actual TCS411(2010),617–630 paper concerns general theta-powers. Section 6 Theorems 25/26 require a theta-palindromic base for their shorter common-root conclusion; Theorem 28 also uses doubling, while Corollary 32 has the longer arbitrary mixed-power bound. Those antecedents require credit but do not state this exact unrestricted alternating-prefix result at the shorter bound. Candidate distinctions are accurate. [Journal paper](https://cs.uwaterloo.ca/~lila/pdfs/On%20a%20special%20class%20of%20primitive%20words.pdf).

Kari–Seki's inspected author PDF improves a longer general theta-power bound. Because text extraction is garbled, I visually inspected Theorem 8, including actual p>q>=2g and bound2p+q-g-floor(g/2). The candidate discloses the author-PDF/version limitation. [Author PDF](https://cs.uwaterloo.ca/~lila/pdfs/improvedfineandwilf.pdf).

Simpson's published AJC92(3)(2025),450–462 Theorem 3.4 uses threshold2h1+2h2-D for an ordinary period. Under common central phase its direct application on w gives2p+2q-2d, twice the present bound, and its palindromic-periodicity definition has a minimum-length condition. Candidate wording that it does not directly give the shorter bound on w is supported. Using a new extension requires an added deduction. [Published AJC paper](https://ajc.maths.uq.edu.au/pdf/92/ajc_v92_p450.pdf).

The OWR record distinguishes the 2010 report from publication on 2 March 2011; candidate bibliography does too. [EMS record](https://ems.press/journals/owr/articles/4425).

I read every row of the included 53-query and retrieval logs and their report/comparison program, and performed 11 fresh targeted searches. I did not independently rerun all 53 historical queries, inspect every earlier priority reference, or retain new raw web-response payloads in this namespace. The package's access/version gaps and retrospective query-window declarations remain relevant. No exact earlier theorem was found within my inspected primary-source scope. This is not an absence proof, first-discovery claim or global novelty certificate.

## Whole PDF, metadata, storage failures and closure scope

All3 PDF pages were visually read. Complete extracted text agrees with TEX in theorem, proof, witness, qualifications and 6 bibliographic links; ORCID is correct. Glyph rightmost edges 541.9297,541.9335,541.6648 points lie inside 612-point-wide pages; no horizontal clipping was found. The long proposition and proof page transition are readable. No active JavaScript, encryption or forms were found. I did not edit/recompile the manuscript.

The local Zenodo preparation metadata accurately describes theorem, uniform witness, attribution, bounded novelty, extensive AI use, unrefereed status, author/ORCID, CC BY 4.0 and both actual attachment paths. It is a prepared local deposit specification, not evidence of remote acceptance or upload. [Zenodo API documentation](https://developers.zenodo.org/).

An initial wrong ZIP filename was corrected before ZIP content exposure. Genuine later ENOSPC errors prevented harness/report writes and directory creation; no nonexistent artifact or successful run was claimed. The parent original source was never altered. An identical private source path was restored as a hardlink after scratch recovery and every initial gate payload rechecked. Three already-inspected candidate scratch PNGs were removed; the original 4 source-page renders remain retained.

I subsequently verified all 69 own extracted members byte for byte against both unchanged ZIP and native full-run prepins (280609 payload bytes), then removed only that losslessly reproducible scratch extraction. Executed code remains exactly preserved inside ZIP; all whole streams, pins, inventories, candidate/source bytes and gate evidence remain. Private verification reads ZIP members in memory. The original capture helper retains its historical extraction path and should not be rerun over old captures. Root separately disclosed an export-stability failed phase; our successful native runs do not use that history.

The full substantive review was supplied to root in chat while writes were blocked. After root's verified older-capture storage recovery, this concrete report and verifier could be materialized. All failures/restorations are logged rather than silently replaced.

All review writes remain in this folder. No parent-file modification, Git operation, install, outside-person communication, upload or publication occurred. Public curation omits raw sources and complete private provenance but binds them separately. Read-only verification performs no implicit mathematical reruns. Root must read the concrete final report/evidence/verifier/proposal and explicitly approve the exact one-time closure writes. No seal is claimed by this report.

