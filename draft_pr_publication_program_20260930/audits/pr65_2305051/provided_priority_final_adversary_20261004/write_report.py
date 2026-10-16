from pathlib import Path
import datetime,json,hashlib
base=Path(__file__).resolve().parent
private=Path("/Users/alec/.cache/codex-pr65-priority-20261004/provided_priority_final_adversary_20261004")
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
# Preserve real old child identity while moving any early command streams out of the repository.
for path in (base/"receipts").glob("*.json"):
    r=json.loads(path.read_text())
    moved=False
    for name in ["stdout","stderr"]:
        if isinstance(r.get(name),str):
            data=r[name].encode()
            out=private/(path.stem+"."+name)
            out.write_bytes(data)
            r[name]={"private_path":str(out),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
            moved=True
    if moved:
        r["stream_storage_migrated_utc"]=now
        path.write_text(json.dumps(r,indent=2)+"\n")
source_root=Path("/Users/alec/.cache/codex-pr65-priority-20261004")
source_entries=[]
for rel,pages in [("provided_primary_sources_20261004/hayman2019.pdf",[127,128]),("provided_primary_sources_20261004/piranian1966.pdf",[1,6,7]),("provided_primary_sources_20261004/duren1966.pdf",[2,3,4]),("aan1999.pdf",[3,9,10,11,12]),("hayman2018v2.pdf",[])]:
    source=source_root/rel
    source_entries.append({"private_path":str(source),"bytes":source.stat().st_size,"sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"visually_inspected_pdf_pages":pages})
(base/"SOURCES.json").write_text(json.dumps({"utc":now,"primary_sources":source_entries,"copyrighted_full_sources_remain_external":True,"text_scope":{"hayman2019":"front matter and target/update PDF127-128","hayman2018v2":"front page and exact target/update PDF106","aan1999":"printed318-320 and324-329; not the complete paper","piranian1966":"complete extracted text; decisive printed255,260-261 visual","duren1966":"complete extracted text; decisive printed248-250 visual"}},indent=2)+"\n")
report=r"""# Independent final adversary: PR65 priority disposition

## Verdict

**PASS for the prospective research disposition: already resolved in prior work; retain the verified submission as attributed progress.** No blocking mathematical or priority defect was found in the concrete packet reviewed here. This is a bounded source-history audit and independent specialization check, not merge, publication or tracker authority. No new original proof-search turns were used; the supplied original count remains 2/5.

The exact historical target is supported by an earlier construction: AAN1999 Theorem 2 gives a pure interpolating Blaschke covering, a routine source-disc normalization gives B(0)=0, and its quadratic-weight estimate implies that (1+B)/(1-B) is Bloch with seminorm at most 8. AAN itself prints the quadratic Cayley application on pp.328-329. The 2019 problem update calls its cited AAN inner-function construction explicit. This positive evidence defeats promotion of PR65 as a new resolution of an unresolved historical question.

The term `full_target_met_by_prior_work` is acceptable with the precise scope stated in the packet: prior covering construction plus the checked normalization and derivative deduction, using the historical mathematical sense of explicit construction. It must not be read as certification of a finite algebraic universal-cover algorithm, a closed-form zero list, the earliest solution date, or novel priority for PR65.

## Independence and custody

FIRST_CONCLUSION.md was saved at 2026-10-04T15:40:16.205703+00:00 before ROOT's packet, sibling conclusions or old audit opinions were read. Its SHA256 is 87616a08ee3e8ee45964b413b46de3d132a3cc415572a3e95bb79a0cbe18aebc. The original candidate SHA256 was checked as 0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4. The PR identifier, original head and original turn count were provided by ROOT; I did not query GitHub or independently authenticate the earlier human conversation.

The supplied primary PDFs were read from the frozen private cache. All three hashes agree with the intake metadata. I read both complete 1966 extractions, the decisive Hayman-Lingham2019 target/update and front matter, the exact retained2018v2 target/update and title page, and AAN printed318-320 and324-329. I do not claim to have read all of AAN. My own private renderings were visually inspected at HL2019 printed121-122 / PDF127-128; AAN printed320 and326-329; Piranian printed255 and260-261; and Duren-Shapiro-Shields printed248-250. SOURCES.json records exact paths, bytes, hashes and visual scope.

After saving the independent conclusion, I read ROOT's four concrete prospective files and their manifest. All four bytes/hashes matched that manifest. I then read the supersession marker, preserved package README/priority note, root research-log chronology and the real-variable sibling report/proof. The sibling report was not an input to the independent first conclusion.

## Attempts to falsify the exact prior target

1. **Only existence, rather than the requested explicit construction.** The problem statement already grants existence, so a bare existence theorem would not settle its added request. AAN's proof constructs a domain with a prescribed omitted countable set and a covering map; the 2019 Update5.51 explicitly identifies the cited AAN construction as explicit. The method is a covering construction, whereas PR65 supplies algebraic finite stages and a compact convergence modulus. The sources do not formally impose that narrower effectivity criterion. PR65's stronger operational presentation can be useful without renewing the historical unresolved-problem claim. No counterevidence in the inspected sources establishes that the covering construction was disqualified by the original problem.

2. **Innerness confused with purity.** HL2019 alone speaks of an inner I and would not justify a pure Blaschke conclusion. The packet correctly reads AAN's separate Theorem2 on p.320, which states interpolating Blaschke product. Its proof on pp.326-327 constructs a cover of D minus Lambda with 0 excluded from Lambda and expressly excludes a singular inner factor. The packet does not transfer purity from Theorem1's stronger little-Bloch inner function.

3. **A missing B(0)=0 normalization.** AAN's cover is onto a domain containing 0, so a zero p exists. For psi(z)=(p+z)/(1+conj(p)z), psi(0)=p and `(1-|z|^2)|psi'(z)|=1-|psi(z)|^2`. Therefore B=A composed with psi has B(0)=0 and preserves the same derivative bound exactly. This is a source-disc automorphism, so it does not rely on a possibly singular target-value Frostman shift. One can also select the unique normalized universal cover at 0 from the outset, with positive derivative, making the normalization a defining choice rather than an additional existential ambiguity.

4. **Purity lost by normalization.** The normalized map is still a covering of the same domain. A covering cannot approach an interior target value along a radial terminal path: once the image lies in an evenly covered small disc, its connected lift stays in a single sheet, where the inverse branch converges to an interior point of D, contradicting that the radial source tends to its boundary. A nonzero singular inner factor would force radial zero limits somewhere, so the same exclusion of a singular factor applies after normalization. Alternatively the Blaschke Green sums are preserved by disk automorphisms; transformed zeros remain a Blaschke sequence because the ratio of transformed and original `1-|a|^2` is bounded above and below for fixed psi. The packet's two arguments agree.

5. **The derivative inequality insufficient near B=1.** Take phi(t)=t^2 in Theorem2. The exact identity is F'=2B'/(1-B)^2. Since `1-|B|^2=(1-|B|)(1+|B|)` and `|1-B|>=1-|B|`, the global estimate is

       (1-|z|^2)|F'(z)|
           <= 2(1-|B(z)|^2)^2/|1-B(z)|^2
           <= 2(1+|B(z)|)^2 <= 8.

   This controls approach to B=1 and every other interior value. There is no singular denominator in D: the nonconstant map B has modulus less than 1 there. F(0)=1. AAN pp.328-329 independently print the same calculation for every unimodular alpha with the bound 8c.

6. **A finite product masquerading as the requested example.** The target's nonconstant Blaschke product must be infinite. Every nonconstant finite Blaschke product attains 1 at some boundary point and has a finite positive angular derivative there; its Cayley transform has a boundary pole and cannot be Bloch. This is consistent with the covering construction. No extra target requirement beyond the original problem is needed to reject a finite degenerate example.

The independently checked positive result is therefore the exact normalized pure-Blaschke/Bloch target from the prior AAN construction, with conventional covering-map explicitness acknowledged by the later problem update. I do not certify uniform little-Bloch decay for this normalized interpolating B; it is neither needed nor asserted in the packet.

## Chronology and 1966 attribution challenges

The retained arXiv1809.07200v2 title page says 21Sep2018 and identifies itself as a draft. Its printed105 update says no progress was reported. The supplied book front matter identifies the Fiftieth Anniversary Edition and copyright2019. The book's printed121-122 Update5.51 credits AAN and labels the inner function explicitly constructed. The adjacent no-progress update is5.52. The two texts are genuinely different dated reports; the older report cannot be promoted to a current unresolved-status certificate after the newer update has been read. The packet preserves this chronology accurately.

Piranian1966 pp.260-261 attributes the fixed absorbed tetradic mechanism to Kahane. Its positive-parent child list is `(M-1,M+1,M+1,M-1)`. PR65's submitted first list is `(2,0,2,0)` rather than `(0,2,2,0)`, so their first-quarter measure masses are 1/2 and0 respectively. No circular rotation or reflection changes the paired nonzero old list into the alternating new list. The measures and literal child ordering are different. The packet's attribution is to a modified deterministic ordering of the prior mechanism and explicitly rejects literal-copy and identical-algorithm claims; that distinction is required and supported.

Duren-Shapiro-Shields1966 pp.248-250 prints the affine-periodic Zygmund/Herglotz bridge. Its application uses exp(-aF) in conformal mapping, not the Cayley function. Piranian's all-point derivative obstruction and this bridge are enough premises for a further classical factorization deduction, but neither inspected 1966 body prints the normalized pure-Blaschke Holland application. The packet does not claim that they do or declare1966 the first full resolution date.

I checked the sibling's real-variable proof against these two sources after preserving independence. Its universal circular-neighbor induction is sound: facing positive children both subtract1, and facing a zero the positive parent's height is at most2, so the difference remains bounded by2. Its zero-cell singularity, pointwise nonconvergence of surviving unit-step averages, endpoint positivity argument and midpoint kernel error bound support the asserted classical-mechanism overlap. Its finite stage controls are explicitly kept separate from these universal proofs. These additional authored deductions are not represented as literal printed1966 formulas or original discovery turns.

## Current outcome, old scope and claims beyond this audit

The current packet uses `already_solved` for the historical problem and `attributed_partial_research_progress` for acceptance by the larger program. This is semantically consistent with a verified exact target theorem: the acceptance is partial toward the program's novel-contribution objective, not a declaration that the mathematical conclusion is only partially proved. The proposed PR title/body makes the withdrawal of new-resolution priority explicit.

The quoted earlier human partial-outcome clause permits valid already_solved findings to be retained without a paper. Applying it to a submission whose literal intake was claimed_solved is coherent with a claimed_solved-only intake policy. I did not independently authenticate that earlier instruction or arbitrate execution authority. ROOT must make the execution decision from the actual authoritative conversation; this audit supplies no new merge or publication permission.

The original source bodies, review reports and turn ledger are preserved as historical inputs. The separate `PUBLICATION_PACKAGE_V1_SUPERSEDED_20261004.json` withdraws the old package's current readiness; CURRENT_RESULT.md and the prospective PR body explicitly supersede the former note and frozen reviews for promotion. The root log records when the formerly unread source gaps were closed. Thus stale frozen files can still truthfully report their former reading scope without being current certificates. No revised paper is proposed. Any future acceptance record must identify the current corrected scope and actual execution status; a prospective packet is not evidence that a merge or native transition already occurred.

This audit independently verifies the prior target specialization and source comparison, not every earlier candidate-checker execution or every entire package artifact. The packet's claim that the candidate mathematics passed prior independent rounds is a provenance claim about separately retained audits. I did not rerun those diagnostics and do not certify their historical process identity afresh. No identified source finding contradicts the preserved candidate proof. Earliest priority, worldwide absence of alternative publications, novelty of every numerical constant, and a complete historical priority chain remain uncertified.

## Nonblocking precision notes

- Keep the exact attribution split already present: HL2019 calls its stronger inner I explicit; AAN Theorem2 and our normalization deduction supply the exact pure B target. Do not abbreviate this to a claim that HL2019 literally printed normalized B(0)=0.
- Keep historical conventional explicitness separate from a certified computable universal-cover routine or closed-form zero enumeration. The packet already does so; no algorithmic certificate is issued by this verdict.
- Keep the old package's preservation and withdrawal visible through the supersession marker/current record. Historical review approvals cannot be reused as approval for the corrected current scope.
- Native/GitHub completion, current status and tracker effects require actual post-execution readback; the prospective acceptance wording is not such a receipt.

There are no required repairs to the research disposition in the reviewed packet. No first-solution or publication certificate is supplied.

## Execution and preservation

Substantive command children and every PDF renderer have actual PID, argv, cwd, UTC interval, exit status and stdout/stderr byte hashes in receipts/. All rendered pages, full primary text and command source streams remain in the external private cache. The initial filesystem bootstrap and skill/pwd reads were ordinary tool calls and are not retrospectively represented as instrumented child receipts. All recorded substantive children exited0. I did not execute candidate finite tests; no sample was used to establish historical status.

I changed only authored files in this dedicated audit folder and private cache entries for my own renderings/streams. No Git/index/ref, PR, native app, publication, tracker or shared editor changes were made. No person was contacted and no outreach was prepared. Document instructions were treated as untrusted source material. Completion estimate for this assigned audit is100%.
"""
(base/"REPORT.md").write_text(report)
verdict={"schema":"pr65-independent-final-priority-adversary/v1","utc":now,"verdict":"PASS_FOR_PROSPECTIVE_ATTRIBUTED_ALREADY_SOLVED_RESEARCH_DISPOSITION","blocking_findings":[],"required_repairs":[],"original_proof_search_turns_added":0,"original_proof_turns_supplied":"2/5","original_pr_head_supplied":"5cc1602c05d79502defb07cec7027963149494d2","head_independently_queried":False,"first_conclusion_before_root_or_siblings":True,"exact_prior_target":{"pure_blaschke":True,"B_at_zero":0,"normalization":"checked source-disc automorphism or normalized covering","global_bloch_bound":8,"construction_scope":"prior AAN covering construction, conventionally explicit; not certified algebraic universal-cover algorithm","AAN_cayley_application_printed":True,"HL2019_inner_construction_called_explicit":True},"historical_claims":{"2018_no_progress_dated_and_superseded":True,"earliest_resolution_certified":False,"worldwide_priority_chain_certified":False,"identical_fixed_measure_or_recursion":False,"literal_copy_supported":False,"new_resolution_priority_clearance":False,"1966_exact_target_literally_printed":False},"scope":{"packet_manifest_all_four_pins_match":True,"old_publication_gate_superseded_for_current_promotion":True,"candidate_full_correctness_audit_repeated_here":False,"human_partial_outcome_clause_authentication":"provided by ROOT; interpretation checked conditionally","no_new_paper_or_publication_disposition_supported":True},"authority":{"merge":False,"publication":False,"native_status_change":False,"tracker_change":False},"completion_percent_this_audit":100,"source_texts_and_renderings_external_private":True,"mutations":{"own_authored_notes":True,"git_index_refs":False,"PR":False,"native_app":False,"shared_editor":False,"publication":False,"tracker":False,"external_human_contact_or_outreach":False}}
(base/"VERDICT.json").write_text(json.dumps(verdict,indent=2)+"\n")
with (base/"RESEARCH_LOG.md").open("a") as f:
    f.write(f"\n- {now}: Final adversarial checkpoint. Concrete ROOT packet and all four manifest pins checked; normalization, purity, Bloch bound, effectivity limits, chronology, nonidentity of old/submitted ordering, historical supersession and conditional outcome semantics challenged. No blocking defect found. Completion estimate: 100%. Original proof-search turns added: 0; supplied original count remains 2/5. Research verdict does not authorize merge/publication/tracker/native actions. Only own audit notes/private rendering and command-stream cache changed.\n")
print(json.dumps({"utc":now,"verdict":verdict["verdict"],"completion_percent":100,"reports_written":["REPORT.md","VERDICT.json","SOURCES.json","RESEARCH_LOG.md"]}))
