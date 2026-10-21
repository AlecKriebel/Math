from pathlib import Path
import hashlib,json,datetime
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");p=T/"publication_driver.py";old=p.read_text()
before='''        need({p.relative_to(T/packet).as_posix()for p in(T/packet).rglob("*")if p.is_file()}==actual|{"MANIFEST.json"},
             "Review closed inventory differs")
'''
after='''        actual_files=set();actual_dirs=set()
        for item in(T/packet).rglob("*"):
            need(not item.is_symlink(),"Review packet symlink")
            relative=item.relative_to(T/packet).as_posix()
            if item.is_dir():actual_dirs.add(relative)
            else:
                need(item.is_file()and item.stat().st_nlink==1,"Nonregular/multiply linked review packet entry")
                actual_files.add(relative)
        expected_dirs={str(parent)for name in actual for parent in Path(name).parents if str(parent)!="."}
        need(actual_files==actual|{"MANIFEST.json"}and actual_dirs==expected_dirs,
             "Review closed inventory differs")
'''
assert before in old
new=old.replace(before,after).replace('and isinstance(row.get("reviewer"),str)and row["reviewer"]','and isinstance(row.get("reviewer"),str)and row["reviewer"].startswith("/root/pr789_whole_preprint_round")').replace('and receipt.get("reviewer")==row["reviewer"]','and receipt.get("problem")=="30001478"and receipt.get("pr")==789\n             and receipt.get("original_scientific_head")=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"\n             and receipt.get("reviewer")==row["reviewer"]').replace('and type(receipt.get("review_actionable_issues"))is int','and type(row.get("actionable_issues"))is int\n             and type(receipt.get("review_actionable_issues"))is int')
p.write_text(new)
r=json.loads((T/"root-receipts/PUBLICATION_REVIEW_GUARD_REPAIR.json").read_text());r.update(updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),new_driver_sha256=hashlib.sha256(new.encode()).hexdigest(),closed_packet_directories_specialfiles_and_target_bound=True)
(T/"root-receipts/PUBLICATION_REVIEW_GUARD_REPAIR.json").write_text(json.dumps(r,indent=2)+"\n")
print(json.dumps({"result":"PASS_ADMIN_REPAIR_PREPARED","driver_sha256":r["new_driver_sha256"]}))
