from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");S=T/"preprint/source";M=T/"root-receipts";W=T/"root_round02_findings";W.mkdir(exist_ok=False)
packet=S/"audit/math_quotient_algebra";mf="7cd556c6a87d2117f803112268e4b8eb86316c76dac40c9fee82ffe0ccf6eea0";cp="31246b25e6040d2d676f0fd5d1b6c4c65cedc0a67440da313a3ff0a584689333"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(packet/"MANIFEST.json")==mf and sha(packet/"verify_packet.py")==cp
before={p.name:sha(p)for p in packet.iterdir()if p.is_file()};copy=W/"algebra-packet";shutil.copytree(packet,copy)
args=["--packet",str(copy),"--intake-root",str(S/"audit/intake"),"--primary-root",str(T/"math_quotient_algebra_scratch"),"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp]
cmd=[sys.executable,"-I","-B",str(copy/"test_packet.py")]
bad=subprocess.run(cmd+args+["--replay"],cwd=W,capture_output=True,text=True,timeout=60);assert bad.returncode==2 and"unrecognized arguments: --replay"in bad.stderr
good=subprocess.run(cmd+args,cwd=W,capture_output=True,text=True,timeout=120);assert good.returncode==0 and not good.stderr,(good.stdout,good.stderr);controls=json.loads(good.stdout);assert controls["status"]=="PASS"and controls["positive_controls"]==2 and controls["negative_controls"]==16
assert before=={p.name:sha(p)for p in packet.iterdir()if p.is_file()}
page=(T/"scratch_primary/OWR2010_22.txt").read_text().split("\f")[44]
assert"1363"in page[:160]and"[Sie10]"in page and"[Van96]"in page and"[YZ06]"in page
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"TWO_LOW_FINDINGS_INDEPENDENTLY_REPRODUCED","bibliographic_range":{"current_incorrect_contribution_range":"1360–1362","correct_contribution_range":"1360–1363","body_claim_locators_1361_1362_remain_correct":True,"official_PDF_sha256":"c860a92325ab314dc5a784cfac5ad7812a7715735247465b7bf4c27d9bd4cd60","PDF_page":45,"printed_page":1363,"reference_continuation_before_next_talk_confirmed":True},"ancillary_command":{"sealed_family_manifest_sha256":mf,"sealed_checker_sha256":cp,"bad_replay_flag_exit":bad.returncode,"bad_stderr":bad.stderr,"correct_without_replay_status":controls["status"],"correct_positive_controls":2,"correct_negative_controls":16,"ran_only_on_owned_complete_packet_copy_outside_closed_source":True,"primary_root_absolute":True},"sealed_family_and_source_58_unchanged":True,"core_math_or_claim_changes_required":False,"next":"Await complete exactV2 childseal; preserveV2 then correctTeX/endpage and topREADME superseding optional command; new fresh reviewer03"}
(M/"ROUND02_FINDINGS_ROOT_REPRODUCTION.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n");(M/"ROUND02_CORRECTED_ALGEBRA_CONTROLS.json").write_text(good.stdout)
print(json.dumps({"result":out["result"],"correct_end_page":1363,"bad_flag_exit":2,"correct_controls":18,"source_mutated":False}))
