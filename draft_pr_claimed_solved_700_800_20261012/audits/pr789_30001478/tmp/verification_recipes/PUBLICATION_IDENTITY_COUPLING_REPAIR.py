from pathlib import Path
import datetime,hashlib,json
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");p=T/"publication_driver.py";old=p.read_text()
before='''    need(r.returncode==0 and not r.stderr and json.loads(r.stdout)["result"]=="PASS","Closed source changed")
    return g,inv
'''
after='''    need(r.returncode==0 and not r.stderr and json.loads(r.stdout)["result"]=="PASS","Closed source changed")
    source=json.loads((P/"source/audit/intake/ROOT_SOURCE_IDENTITY.json").read_text())
    need(source["reviewed_head"]=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
         and g.get("original_scientific_head",g["reviewed_head"])==source["reviewed_head"]
         and g["statement_hash"]==source["statement_sha256"]=="628ed4ce70b7b62857ead560403291f24b890137a8073ce34a17c50d857aa3a6"
         and g["review_hash"]==source["review_hash"]=="cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f",
         "Readiness scientific identity differs from the exact audited original source")
    return g,inv
'''
assert before in old
new=old.replace(before,after).replace('    g,inv=gate()\n    if args.command=="stage":','    g,inv=gate()\n    if args.command in("stage","publish"):\n        need(g["reviewed_head"]=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a",\n             "Production publication requires the literal audited scientific head; postpublication merge integration is separate")\n    if args.command=="stage":')
p.write_text(new)
(T/"root-receipts/PUBLICATION_IDENTITY_COUPLING_REPAIR.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"reason":"Independent administrative adversary found simultaneous gate/remote head or source identity drift could satisfy the earlier relational eligibility guard.","old_driver_sha256":hashlib.sha256(old.encode()).hexdigest(),"new_driver_sha256":hashlib.sha256(new.encode()).hexdigest(),"source_identity_hard_pinned_and_coupled_to_verified_original_intake":True,"stage_and_publish_require_literal_original_scientific_head":True,"postpublication_readonly_verification_can_retain_distinct_administrative_merge_head_with_original_scientific_binding":True,"source_or_six_changed":False,"production_mutation":False,"independent_rejection_control_rerun_pending":True},indent=2)+"\n")
print(json.dumps({"result":"REPAIRED_ADMIN_ONLY","driver_sha256":hashlib.sha256(new.encode()).hexdigest()}))
