# Independent signed-graph audit: PR 356 / problem 30001552

Audit checkpoint UTC: 2026-10-04T00:47:24.349272+00:00
Verdict: PASS of the submitted universal mathematical argument against the exact original source. No mandatory mathematical correction found. Estimated audit completion: 95%; root review and explicitly authorized closure remain.

Frozen head: 12fc989f8635fd202eb66b553b9599f0546d05d3.
Original base: efd29c05204703acca9a0860812f54b94fae54b1.
Approach family: signed constraints, finite reflection orbits, and equality-graph lifting.

## Exact source target and audit independence

The complete Nowotka/Bischoff section, printed 2219-2222 / PDF 25-28, was read as text and visually checked before any candidate exposure. Its unnumbered conjecture following Theorem 23 on printed 2220 asks:

For every alphabet A, antimorphic involution theta on A*, finite word w, and positive alternating theta-periods p,q, let d=gcd(p,q). If |w|>=p+q-d, then d is an alternating theta-period.

The source definition means a prefix of (u theta(u))^omega with |u| equal to the claimed period. It differs from freely mixed theta-periods and weak letterwise periods. The imported problem record's unqualified theta-period conclusion is weaker; the submission explicitly handles the stronger source target, correctly.

Source: Dirk Nowotka, joint work with Bastian Bischoff, Word periods under involution, Oberwolfach Report 37/2010, DOI 10.4171/OWR/2010/37, [official report](https://ems.press/content/serial-article-files/46296). Source PDF SHA-256: e88f211c5be990a68a967f3a9549f5db042279e8473e2cb126ea1e3caaebf98c. Its Theorem 20 explicitly states the classical finite-word Fine-Wilf theorem used by the candidate.

The immutable source-first baseline was pinned at 2026-10-04T00:36:22.857399+00:00 before root release. Baseline SHA-256: c861095d10225fed3b4aedd960ce765f8b78025c763db5fc42b941f102c4f33c. Gate SHA-256: 849b70d32cd30e6b974c30bae698832d47ff7c81850c84dc75cf1fce7177055b. A source-only graph derivation was saved before release. All 16 frozen problem files, snapshot manifest, and own queue row were then read after explicit root release. The independent mathematical PASS was saved before any sibling-family conclusions; pre-computation assessment SHA-256: 0271136fbc298cf5a1f89cb50051557314c432af9a8ac96e02cf80a6118e8b28.

## Independent signed-graph verification of the universal mechanism

An involutive antimorphism fixes the empty word and is bijective. Nonempty words cannot map to the empty word, and an image of a letter cannot split into two nonempty factors, since applying theta again would split that letter. Therefore theta is reversal followed by an involutive alphabet permutation tau, including arbitrary fixed letters.

Use positions t=0,...,L-1. For h>0 define r=t mod 2h,

    c_h(t)=r if r<h, otherwise 2h-1-r;
    e_h(t)=0 if r<h, otherwise 1.

When L>=h, alternating h-period is exactly the collection of signed equations

    w[t]=tau^(e_h(t))(w[c_h(t)]), h<=t<L.

Necessity follows by reading its infinite template; sufficiency chooses the first h letters as the seed. No final-block alignment is used. At the theorem threshold L>=max(p,q), both full seeds exist.

For d dividing h, c_d(t)=c_d(c_h(t)) and e_d(t) xor e_d(c_h(t))=e_h(t). Thus all p,q signed edges lie inside a target folded d-color with the required sign, and the graph is balanced under the potential e_d. The remaining issue from the source-only stage was finite connectivity of each required color; the following lifting resolves that exact gap with the credited ordinary theorem.

Lift every position t into two formal slots (t,0) and (t,1), interpreted as w[t] and tau(w[t]). A signed edge t~(s)c produces equality edges (t,b)=(c,b xor s), b=0,1. Map (t,0) to coordinate t and (t,1) to coordinate -1-t in [-L,L-1]. For an h-edge these coordinates are congruent modulo 2h: when s=0 their difference is t-c; when s=1 it is t+1+c, in both cases a multiple of 2h. Each coordinate is linked to its representative in [-h,h-1], and these representatives are present because L>=h. Conversely, all coordinates congruent modulo 2h fold to the same representative and hence are connected in the lifted graph. Thus the lifted h-partition is exactly the equality closure of translation by 2h on the doubled interval.

The union for p,q therefore contains all equalities of ordinary periods 2p and 2q for a length-2L word. The Fine-Wilf equality-graph connectivity form follows directly from source Theorem 20: color each connected component of the translation graph with a distinct ordinary letter. The resulting word has the two periods, so the theorem forces equal colors at coordinates congruent modulo 2d, hence those coordinates must be connected. Its threshold holds exactly because

    2L >= 2p+2q-2d = 2p+2q-gcd(2p,2q).

The complete central block [-d,d-1] is available. Every nonnegative coordinate t is linked to r=t mod 2d if r<d, and otherwise to r-2d, the negative slot -1-(2d-1-r). Mapping back gives precisely the required signed d-edge. Consequently w is a prefix of v theta(v) repeated, with v its first d letters.

This is a checkable signed-graph audit of the submission's reflection mechanism. It credits classical Fine-Wilf; it does not claim a distinct new theorem input or infer a universal result from finite scans.

## Submitted mathematical claims checked

| Submitted claim | Assessment | Reason or exact limitation |
|---|---|---|
| Theorem in TURN_1.md and RESULT.md proves the stronger source implication | PASS | Lifted graph proof above establishes all positive p,q and all L>=p+q-d. |
| Antimorphism acts by alphabet involution followed by reversal | PASS | Bijective indecomposability argument; neither finite alphabet nor fixed-point exclusion needed. |
| Two-sided alternating extension obeys s(-1-i)=tau(s(i)) | PASS | Reflection exchanges the two h-halves modulo 2h; applying tau twice verifies the other half. |
| The same word theta(w)w has ordinary periods 2p and 2q | PASS | Both extensions have identical letters on [-L,L-1]; arbitrary partial final blocks are allowed. |
| Fine-Wilf threshold and gcd arithmetic | PASS | gcd(2p,2q)=2d; doubling the precise endpoint gives the exact threshold. |
| Ordinary period 2d recovers an alternating d-period | PASS | Central [-d,d-1] representatives retain the tau signs; it is stronger than arbitrary theta mixing. |
| Equal periods, divisibility, fixed letters, empty word boundary | PASS | Equal/dividing cases already contain d as a premise; fixed letters obey the same equations; L>=max(p,q)>0 excludes the empty word. |
| Reversal witness abb with periods 2,3 but no period 1 | PASS | It is a prefix of abba repeated and abbbba repeated; every reversal period-1 theta-block is constant. |
| Sharpness scope is the universal formula, not every pair | PASS | The example refutes a uniform one-letter decrease; no general pairwise minimality is asserted. |
| Freely mixed and morphic variants excluded | PASS | The deterministic reflected 2h extension is not available by those hypotheses; no generalization is promoted. |
| Finite controls supplement, rather than prove, the theorem | PASS | All integer/enumeration runs reproduced below; written proof provides the universal step. |

The candidate's graph checker proves its fixed finite cases by equality propagation, sound for every alphabet/involution assignment. Its binary word checker restricts to observed full seeds, harmless at the theorem threshold. The independent checker here also explicitly permits h>L as the source definition does, and verifies empty-prefix encoding; these are relevant to below-threshold controls rather than a missing theorem case.

## Reproduction and adversarial controls

All native commands used existing Python 3.11 with assertions enabled and no installs. Whole stdout and stderr streams, exact arguments, timestamps, code hashes, return codes and receipt byte comparisons are retained. Pre-execution pin SHA-256: 6c596da058526bfbcc72fcb46e848d8903a9c41145e0f5fb6cca901379db6a90. Independent checker SHA-256: 9ac902749801209a4d0c8b20fcabaa84bbe2f6cbd02207815ca1d37284780f9f.

- Unmodified submitted author checker: exit 0; stdout matches TURN_1_CHECKS.json byte for byte, including 526,887 assertions, 18,316 qualifying binary period-pair cases and 5,050 universal finite graph pairs.
- Unmodified public portable reviewer entry point: exit 0; stdout matches PORTABLE_CHECKS.json byte for byte with 68,408 assertions. No --source-root was supplied.
- Independent signed graph: 24,310 endpoint pairs with 1<=q<=p<=220, plus 48,620 longer-length runs at L0+1 and L0+p. All target edges hold.
- Independent divisor-sign checks: 22,725,320 exact checks. Lifted signed partitions equal ordinary translation partitions in 494,130 coordinate checks over 1<=h<=L<=90.
- Independent direct-word checks: 187,787 encoding equivalences, 33,568 reflected-word period checks and 35,828 qualifying gcd conclusions. Alphabets include three fixed letters, a fixed letter with a complement pair, and one complement pair; lengths reach 8 for the three-letter cases and 10 for the binary case.
- Below the endpoint: 24,310 symbolic runs; 23,084 have a split required class. A retained witness is p=3,q=2,L=3, word (0,2,3), tau=(1,0,3,2); p,q hold and d=1 fails. This is a finite observation, not a promoted general pairwise sharpness theorem.

All executed programs exited 0 with empty stderr. Entire author, publication and review artifact-manifest bindings were validated; the independently read official OWR PDF also matches its submitted source hash.

## Provenance and remaining qualifications

The original hardcoded review checker targets /workspace/shared/math-30001552. The additive public portable program is the documented reproducible entry point and executes its frozen mathematical loops. The original five-source mode's 68,413 receipt was not rerun here. Four original raw source payloads (CKS PDF/text, OWR full text and historical printed2220 PNG) are unavailable in this audit; the available official OWR PDF hash was checked separately. No substitute or regenerated bytes were used to claim the missing historical bindings. Their absence does not remove a proof premise, because the exact source definitions and Fine-Wilf theorem were independently inspected in the official report.

The audit does not certify publication priority, later literature nonexistence, historical exhaustive PR/commit searches, human peer review, formal proof-assistant verification, or CI success. The submission itself qualifies novelty. The original imported prior_research={} is root-reported and does not establish newness.

The snapshot's complete API/object/disk/mode identity is root-reported; literal local Git binding and ancestry/queue-diff verification remained pending at this family's mathematical checkpoint and are not claimed by this report. I made no Git read/write, candidate modification, branch/checkout, install, outside contact, merge, release or publication.

No mathematical gap remains in the target implication conditional on the explicitly credited classical Fine-Wilf theorem. Remaining operational work for this family: root reads/approves this report and evidence, then explicitly authorizes the single read-only public/private seal. No closure has occurred at this checkpoint.

## Read-only namespace verifier added before closure

UTC 2026-10-04T00:52:34.677322+00:00: verify_namespace.py supports an exact full saved-evidence check and a public-only inventory check, with private omissions declared explicitly. It hashes curated files, matches whole native streams and archived executed-code bytes to pre-execution pins, and checks the immutable source-first gate. It never executes mathematical controls, writes files, installs dependencies or resolves missing optional source bodies. Before the single authorized closure it accepts a pinned proposal; after closure it reads separate curated public/private inventories and the last-written closure seal. Root authorization to seal is still pending. All earlier plan/report versions and captures are retained.

UTC 2026-10-04T00:54:12.597467+00:00: Both verifier modes passed against closure-plan version 2, with complete saved streams, pre-execution pins and measured execution times. Full mode took 0.048871457984205335 seconds; public-only mode took 0.038616292004007846 seconds. The entire 37-file namespace was byte-identical before/after these read-only runs. Their captures are now archived as additional private evidence in version 3; the public-only result explicitly excluded private bodies, native bindings and source-first gate checks. No mathematical control was rerun by either verifier. Estimated audit completion at this checkpoint: 97%; root full-read approval and authorized one-time seal remain.
