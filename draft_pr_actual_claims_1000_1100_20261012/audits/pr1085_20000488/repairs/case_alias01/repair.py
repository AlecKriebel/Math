"""Bounded physical-case output-location repair; no mathematical or service change."""
from pathlib import Path
import datetime,difflib,hashlib,io,json,os,shutil,sys,zipfile
F=Path(__file__).resolve().parent;A=F.parents[1];K=A/'preprint_v1_0';P=A.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def dump(p,o):
 p.parent.mkdir(parents=True,exist_ok=True);atomic(p,(json.dumps(o,indent=2)+'\n').encode())
def atomic(p,b):
 t=p.with_name(p.name+'.case_alias01_new');need(not t.exists(),'temporary exists');t.write_bytes(b);os.replace(t,p)
def main():
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 old=(F/'before/preprint_v1_0/kit_common.py').read_text()
 anchor='    for source in protected(extra):\n'
 block='''    # resolve() preserves spelling on case/normalization-insensitive hosts.
    # Compare every existing ancestor physically, even above absent directories.
    # This also works when __file__ names the kit through a different alias.
    root_stat = ROOT.stat()
    root_identity = (root_stat.st_dev, root_stat.st_ino)
    for ancestor in [target, *target.parents]:
        try:
            ancestor_stat = ancestor.stat()
        except FileNotFoundError:
            continue
        require((ancestor_stat.st_dev, ancestor_stat.st_ino) != root_identity,
                "output must be outside physical kit directory")
'''
 need(old.count(anchor)==1,'guard anchor');atomic(K/'kit_common.py',old.replace(anchor,block+anchor).encode())
 finding='''# PR1085 static physical-case output-location repair

The new P3 finding CASE-1085 reproduced fresh archive insertion below a physically identical uppercase kit-directory alias in ordinary and optimized Python. Canonical-spelling controls rejected the same location. Existing protected-input overwrite and mathematical error were not observed. The root scope adoption and subsequent terminal hold are exact authored evidence copies here.

The repaired shared guard preserves its lexical, symlink, resolved-input and existing-hardlink checks. It additionally compares device/inode identity for each existing output ancestor against the kit root, including the existing ancestor above absent intermediate directories. This uses actual filesystem identity without assuming a lowercase normalization rule, and covers either script-root spelling direction. All four current writers call the guard before directory creation, output writes or compiler invocation. The scope remains static local files, without hostile concurrent-race promises.

The paper, mathematics, credits, exact native metadata and historical accounting/seals remain unchanged. Two completed whole reviews are historical evidence. This new repair requires external root adoption and a NEW complete whole03 review before any clearance. All current readiness/publication flags remain false; services remain held after PR1032. No new paper compilation, render or authoring marker is asserted.
'''
 atomic(F/'FINDING_AND_REPAIR.md',finding.encode())
 selected=[(F/'FINDING_AND_REPAIR.md','FINDING_AND_REPAIR.md'),(P/'ROOT_CASE_ALIAS_SCOPE_REVIEW.json','ROOT_CASE_ALIAS_SCOPE_REVIEW.json'),(A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json','ROOT_TERMINAL_ADMIN_REVIEW_20261016.json')]
 for n in ['kit_common.py','README.md','verify_package.py']:
  selected.append((F/'before/preprint_v1_0'/n,'before/'+n))
 copies=[]
 for src,dest in selected:
  b=src.read_bytes();name='evidence/case_alias01/'+dest;atomic_path=K/name;atomic_path.parent.mkdir(parents=True,exist_ok=True);atomic(atomic_path,b)
  copies.append({'source_relative_program':str(src.relative_to(P)),'copy':name,'bytes':len(b),'sha256':sha(b)})
 dump(K/'CASE_ALIAS_REPAIR_COPY_MAP.json',{'schema':1,'scope':'Minimal authored finding/root hold and exact old interface copies only; locators refer to local program custody. Old ZIP is retained locally, never distributed. Original preparation and terminal partitions are unchanged.','files':copies})
 account={'schema':1,'utc':now,'pr':1085,'problem_id':20000488,'audited_head':'5e23f0c801d23976830657d2eef2b32bdc7da05a','status':'CASE_ALIAS_REPAIRED_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03','finding':'CASE-1085','finding_severity':'P3','finding_scope':'Fresh physical internal output insertion; no existing overwrite or mathematical finding.','historical_whole_reviews_completed':2,'minimum_whole_reviews':2,'new_complete_whole03_required':True,'new_complete_whole03_completed':False,'root_repair_adoption_required':True,'publication_ready':False,'all_actionable_issues_resolved':False,'published':False,'human_peer_review':False,'formal_proof_certificate':False,'services_hold':'preceding PR1032 priority cursor','historical_STATUS_and_TERMINAL_ACCOUNTING_preserved':True,'priority':'UNKNOWN_EXACT_REMAINING_GEOMETRIC_FORMULATIONS','novelty':'UNKNOWN','worldwide_open_status':'UNKNOWN','independent_discovery':'UNKNOWN','paper_pdf_sha256':'464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d','paper_tex_sha256':'c18a6ed12250dcee413e85f9a6297c525015396f151cdab8d89a6eb76938046d','physical_ancestor_policy':'Existing ancestor device/inode identity against kit root, including above absent intermediate directories; no case-folding assumption.','guard_scope':'Static local filesystem; no hostile concurrent-race security claim.','meaning':'Historical zero findings predate the new case-alias P3. This bounded repair is not a whole-package review or readiness grant. New complete whole03 and external root adoption remain required.'}
 dump(K/'CASE_ALIAS_REPAIR_ACCOUNTING.json',account)
 v=(F/'before/preprint_v1_0/verify_package.py').read_text()
 anchor='    require(regular(ROOT / "paper.pdf").read_bytes().startswith(b"%PDF-"), "paper PDF signature")\n'
 gate='''    # The terminal stage above remains an exact dated snapshot. The later
    # case-alias repair cannot inherit its old zero-finding clearance.
    repair = read_json(ROOT / "CASE_ALIAS_REPAIR_ACCOUNTING.json")
    require(type(repair.get("schema")) is int and repair["schema"] == 1,
            "case repair schema")
    require(type(repair.get("pr")) is int and repair["pr"] == 1085 and
            type(repair.get("problem_id")) is int and repair["problem_id"] == 20000488 and
            repair.get("audited_head") == status["audited_head"], "case repair identity")
    require(repair.get("status") == "CASE_ALIAS_REPAIRED_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03" and
            repair.get("finding") == "CASE-1085" and repair.get("finding_severity") == "P3",
            "case repair pending stage")
    for key in ["historical_whole_reviews_completed", "minimum_whole_reviews"]:
        require(type(repair.get(key)) is int and repair[key] == 2, "case repair two historical reviews")
    for key in ["new_complete_whole03_required", "root_repair_adoption_required",
                "historical_STATUS_and_TERMINAL_ACCOUNTING_preserved"]:
        require(repair.get(key) is True, "case repair required review/adoption/history")
    for key in ["new_complete_whole03_completed", "publication_ready", "all_actionable_issues_resolved",
                "published", "human_peer_review", "formal_proof_certificate"]:
        require(repair.get(key) is False, "case repair forbidden promotion: " + key)
    require(repair.get("services_hold") == status["services_hold"], "case repair ordered hold")
    for key in ["priority", "novelty", "worldwide_open_status", "independent_discovery"]:
        require(repair.get(key) == status[key], "case repair historical scope: " + key)
    for key in ["paper_pdf_sha256", "paper_tex_sha256"]:
        require(repair.get(key) == terminal[key], "case repair unchanged paper")
    repair_map = read_json(ROOT / "CASE_ALIAS_REPAIR_COPY_MAP.json")
    require(type(repair_map.get("schema")) is int and repair_map["schema"] == 1,
            "case repair copy schema")
    repair_copies = repair_map["files"]
    expected_copies = ["evidence/case_alias01/" + n for n in ["FINDING_AND_REPAIR.md",
        "ROOT_CASE_ALIAS_SCOPE_REVIEW.json", "ROOT_TERMINAL_ADMIN_REVIEW_20261016.json",
        "before/kit_common.py", "before/README.md", "before/verify_package.py"]]
    require([r["copy"] for r in repair_copies] == expected_copies and
            len({r["source_relative_program"] for r in repair_copies}) == len(repair_copies),
            "case repair exact evidence membership")
    for row in repair_copies:
        require(set(row) == {"source_relative_program", "copy", "bytes", "sha256"} and
                type(row["bytes"]) is int and row["copy"] in names, "case repair copy fields")
        data = regular(ROOT / row["copy"]).read_bytes()
        require(len(data) == row["bytes"] and sha(data) == row["sha256"], "case repair copied bytes")
    hold = read_json(ROOT / expected_copies[2])
    require(hold.get("new_complete_whole03_required") is True and
            hold.get("publication_ready") is False and hold.get("published") is False and
            hold.get("services_held_after_pr") == 1032, "case repair root hold evidence")
'''
 need(v.count(anchor)==1,'verifier anchor');v=v.replace(anchor,gate+anchor)
 v=v.replace('"publication_ready": False, "new_whole_reviews": 2,','"publication_ready": False, "new_whole_reviews": 2,\n            "new_complete_whole03_required": True, "new_complete_whole03_completed": False,')
 v=v.replace('two complete whole reviews are recorded, external root terminal integrity adoption remains required, and services are held after PR1032.','two historical complete whole reviews are recorded; the later case-alias repair requires external root adoption and NEW complete whole03, and services are held after PR1032.')
 atomic(K/'verify_package.py',v.encode())
 r=(F/'before/preprint_v1_0/README.md').read_text()
 r=r.replace('Current readiness and all-issues-clearance remain false pending the external root terminal integrity adoption.','Those captured zero-finding verdicts predate the later case-alias finding. CASE_ALIAS_REPAIR_ACCOUNTING.json now requires external root repair adoption and a NEW complete whole03 review; current readiness and all-issues-clearance remain false.')
 r=r.replace('The builder requires an output outside the canonical kit.','The builder requires an output outside the physical kit directory, including case or normalization aliases on filesystems that identify those spellings. Existing output ancestors are compared by device/inode identity, including above absent intermediate directories, in either script-root spelling direction.')
 r=r.replace('All output-writing CLI paths reject direct, resolved, symlink and existing-hardlink aliases','All output-writing CLI paths reject physical kit ancestry, direct, resolved, symlink and existing-hardlink aliases')
 r+='''\n## Later case-alias repair and current review hold\n\nCASE_ALIAS_REPAIR_ACCOUNTING.json supplements the unchanged dated TERMINAL_ACCOUNTING.json. It records CASE-1085 (P3), the static physical-ancestor guard repair, two completed historical whole reviews, the minimum of two reviews, mandatory external root repair adoption and a NEW complete whole03 review. The new review is pending; readiness, all-issues-clearance and publication remain false, and services remain held after PR1032. Historical zero-finding verdicts and their seals keep their captured-stage meaning. This focused repair is not a new whole-package review.\n\nCASE_ALIAS_REPAIR_COPY_MAP.json pins six necessary authored finding/root-hold and exact old-interface copies in evidence/case_alias01/. The original 66/126 preparation and 52/323 terminal copy/exclusion partitions remain exact. No raw streams, third-party bodies, pixels, runtimes or old ZIPs are added. The paper PDF/TeX, mathematical checker, credits, metadata constants and every native metadata field remain byte-exact. No new PDF compilation, render or authoring marker is needed for the unchanged paper.\n'''
 atomic(K/'README.md',r.encode())
 names=(F/'before/preprint_v1_0/PAYLOAD_MEMBERS.txt').read_text().splitlines()+['CASE_ALIAS_REPAIR_ACCOUNTING.json','CASE_ALIAS_REPAIR_COPY_MAP.json']+[r['copy'] for r in copies]
 need(len(names)==len(set(names)),'duplicate payload');names=sorted(names);atomic(K/'PAYLOAD_MEMBERS.txt',('\n'.join(names)+'\n').encode())
 m=json.loads((F/'before/preprint_v1_0/SUPPORT_MANIFEST.json').read_text());m['files']=[{'path':n,'bytes':len((K/n).read_bytes()),'sha256':sha((K/n).read_bytes())} for n in names];dump(K/'SUPPORT_MANIFEST.json',m)
 # Independent closed deflate-9 construction; actual CLI is replayed later.
 s=io.BytesIO()
 with zipfile.ZipFile(s,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in sorted(names+['SUPPORT_MANIFEST.json']):
   i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,(K/n).read_bytes(),compresslevel=9)
 body=s.getvalue();atomic(K/'pr1085_support_v1_0.zip',body)
 b=json.loads((F/'before/preprint_v1_0/UPLOAD_BINDINGS.json').read_text());b['files'][1]['bytes']=len(body);b['files'][1]['sha256']=sha(body);dump(K/'UPLOAD_BINDINGS.json',b)
 with (F/'RESEARCH_LOG.md').open('a') as log:log.write('\n'+now+' — Implemented ancestor identity guard and separate pending-whole03 semantic gate; added six compact authored/old-interface copies. Rebuilt closed deflate9 ZIP with '+str(len(names)+1)+' members. Bounded execution 45%; actual controls and final custody checks pending.\n')
 print(json.dumps({'members':len(names)+1,'archive_bytes':len(body),'sha256':sha(body)}))
if __name__=='__main__':main()
