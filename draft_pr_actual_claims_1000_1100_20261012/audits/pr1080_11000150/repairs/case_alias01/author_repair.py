#!/usr/bin/env python3
"""Bounded atomic authoring; no services and no mathematical payload edits."""
import hashlib,json,os,shutil,datetime
from pathlib import Path
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.case_alias01-new');t.write_bytes(b);os.replace(t,p)
def text(p,s):put(p,s.encode())
def dump(p,d):text(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def replace(p,a,b):
 s=p.read_text()
 if s.count(a)!=1:raise RuntimeError('replacement anchor '+str(p))
 text(p,s.replace(a,b))
if (W/'AUTHORING_COMPLETE.json').exists():raise RuntimeError('one-shot authoring already completed')
replace(K/'verify.py','    require(not output.exists(), "archive destination must be fresh; existing files and aliases rejected")', '''    # Lexical containment alone misses case aliases on case-insensitive volumes.
    # Inspect every existing ancestor, including above absent intermediates.
    protected = ROOT.stat()
    for part in [output, *output.parents]:
        try:
            identity = part.stat()
        except (FileNotFoundError, NotADirectoryError):
            continue
        require((identity.st_dev, identity.st_ino) != (protected.st_dev, protected.st_ino),
                "archive must be outside the physical kit")
    require(not output.exists(), "archive destination must be fresh; existing files and aliases rejected")''')
replace(K/'verify.py','    for index, relocation in relocations.items():','''    case_relocations = json.loads(regular_input(ROOT / "CASE_ALIAS_HISTORY_RELOCATIONS.json").read_text())["rows"]
    for relocation in case_relocations:
        index = relocation["reference_index"]
        require(type(index) is int and 0 <= index < 4628 and index not in relocations
                and history["references"][index] == relocation["historical_reference"],
                "case repair historical relocation changed original row")
        relocations[index] = relocation
    for index, relocation in {r["reference_index"]: r for r in relocation_rows}.items():''')
anchor='    native = native_metadata()'
replace(K/'verify.py',anchor,'''    current = json.loads(regular_input(ROOT / "CURRENT_CASE_ALIAS_REPAIR01.json").read_text())
    require(current["status"] == "BOUNDED_CASE_ALIAS_REPAIR_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03"
            and current["supersedes_dated_terminal_review_requirement"] is True,
            "case repair current stage authority")
    require(type(current["whole_reviews_completed"]) is int and current["whole_reviews_completed"] == 2
            and type(current["minimum_whole_reviews"]) is int and current["minimum_whole_reviews"] == 2
            and current["new_complete_review_required"] is True and current["required_next_review"] == "NEW complete whole03",
            "case repair new complete review required")
    require(current["root_repair_adoption_required"] is True and current["root_integrity_adoption_required"] is True
            and all(current[key] is False for key in ["root_repair_adopted", "root_integrity_adopted", "publication_ready", "issues_resolved", "published"])
            and current["services_held_at"] == 1032, "case repair publication/service boundary")
    require(current["full_original_maximum_classification_bundle"] == "PARTIAL"
            and current["exact_application_priority"] == "UNKNOWN", "case repair scope boundary")
    native = native_metadata()''')
replace(K/'verify.py','        require(regular_input(p.parent / "TERMINAL_ADMIN_STAGE.json").read_bytes()', '        require(regular_input(p.parent / "CURRENT_CASE_ALIAS_REPAIR01.json").read_bytes() == (ROOT / "CURRENT_CASE_ALIAS_REPAIR01.json").read_bytes(), "external case repair status differs")\n        require(regular_input(p.parent / "TERMINAL_ADMIN_STAGE.json").read_bytes()')
replace(K/'verify.py','["CURRENT_STATUS_REPAIR01.json", "README.md", "TERMINAL_ADMIN_STAGE.json", "deposit_metadata.json", "metadata.json", "preprint.tex", "research_metadata.json"], "external delivery file inventory differs")','["CURRENT_CASE_ALIAS_REPAIR01.json", "CURRENT_STATUS_REPAIR01.json", "README.md", "TERMINAL_ADMIN_STAGE.json", "deposit_metadata.json", "metadata.json", "preprint.tex", "research_metadata.json"], "external delivery file inventory differs")')
replace(K/'output_guard_checks.py','            def command(dest):\n                return subprocess.run(prefix + [str(kit / "build_archive.py"), "--output", str(dest)],','            def command(dest, script_root=kit):\n                return subprocess.run(prefix + [str(script_root / "build_archive.py"), "--output", str(dest)],')
replace(K/'output_guard_checks.py','            def reject(kind, dest, cleanup=None):\n                result = command(dest)','            def reject(kind, dest, cleanup=None, script_root=kit):\n                result = command(dest, script_root)')
replace(K/'output_guard_checks.py','            dest = outside / ("fresh-optimized.zip" if optimized else "fresh-normal.zip")','''            case_kit = kit.with_name(kit.name.swapcase())
            case_available = case_kit.exists() and case_kit.samefile(kit)
            if case_available:
                for kind, dest, script_root in [
                    ("physical-case-root", case_kit / "fresh-case.zip", kit),
                    ("physical-case-nested", case_kit / "originals" / "fresh-case.zip", kit),
                    ("physical-case-absent-parent", case_kit / "absent-parent" / "fresh-case.zip", kit),
                    ("physical-case-traversal", case_kit / "originals" / ".." / "fresh-case.zip", kit),
                    ("physical-case-reverse-root", kit / "fresh-case.zip", case_kit),
                    ("physical-case-reverse-absent-parent", kit / "absent-parent" / "fresh-case.zip", case_kit),
                ]:
                    reject(kind, dest, script_root=script_root)
                    require(not dest.exists(), "rejected physical case output was created")
                require(not (kit / "absent-parent").exists(), "rejected absent parent was created")
            observations.append({"control": "physical-case-alias-availability", "optimized": optimized,
                                 "same_physical_directory": case_available})
            dest = outside / ("fresh-optimized.zip" if optimized else "fresh-normal.zip")''')
replace(K/'output_guard_checks.py','            dest.unlink()\n        require(len(set(positive_hashes)) == 1','''            dest.unlink()
            case_outside = outside.with_name(outside.name.swapcase())
            if case_outside.exists() and case_outside.samefile(outside):
                dest = case_outside / "fresh-case-outside.zip"
                result = command(dest)
                require(result.returncode == 0, "fresh physical outside case rebuild failed: " + result.stderr)
                positive_hashes.append(sha(dest))
                require(pins(protected) == expected, "case outside rebuild changed protected inputs")
                dest.unlink()
        require(len(set(positive_hashes)) == 1''')
replace(K/'output_guard_checks.py','"rejection_count": len(observations),','"rejection_count": sum("fault" in r for r in observations),')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
status={'utc':now,'status':'BOUNDED_CASE_ALIAS_REPAIR_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03','supersedes_dated_terminal_review_requirement':True,'dated_terminal_record':'TERMINAL_ADMIN_STAGE.json remains exact historical pre-finding evidence. Its no-new-review field is superseded by this repair record.','whole_reviews_completed':2,'minimum_whole_reviews':2,'new_complete_review_required':True,'required_next_review':'NEW complete whole03','root_repair_adoption_required':True,'root_repair_adopted':False,'root_integrity_adoption_required':True,'root_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'full_original_maximum_classification_bundle':'PARTIAL','exact_application_priority':'UNKNOWN','math_research_completion_best_guess_percent':60,'scope':'Bounded physical output containment repair; no mathematical, PDF, TeX, source-credit or native metadata changes; no new compile/render/view or PDF marker.'}
for base in [D,K]:dump(base/'CURRENT_CASE_ALIAS_REPAIR01.json',status)
for p in [D/'README.md',K/'README.md']:
 s=p.read_text().replace('`TERMINAL_ADMIN_STAGE.json` is the current dated successor, pending separate ROOT integrity adoption;', '`CURRENT_CASE_ALIAS_REPAIR01.json` is the current repair checkpoint, requiring ROOT repair adoption and NEW complete whole03;').replace('`TERMINAL_ADMIN_STAGE.json` records the current dated successor:', '`CURRENT_CASE_ALIAS_REPAIR01.json` supersedes the dated terminal checkpoint and requires ROOT repair adoption plus NEW complete whole03:').replace('Current terminal state is recorded separately in `TERMINAL_ADMIN_STAGE.json`.','The later `CURRENT_CASE_ALIAS_REPAIR01.json` requires NEW complete whole03 after the physical case-alias repair; `TERMINAL_ADMIN_STAGE.json` remains unchanged historical evidence.')
 s+='''
## Physical case-alias repair checkpoint

`CURRENT_CASE_ALIAS_REPAIR01.json` supersedes the dated terminal record's earlier no-new-review requirement. The terminal P3 case-alias finding is repaired in this candidate, pending ROOT adoption and a **NEW complete whole03**. The two prior complete reviews remain completed; minimum two remains unchanged. Readiness, issues-resolved and publication remain false; services remain held at PR1032. This bounded repair is not whole03 or final readiness clearance.

The archive output guard compares the device/inode identity of every existing output ancestor with the actual kit root, including ancestors above absent intermediate components. This rejects physical case aliases in either script-root/output spelling direction. Unresolved symlink, lexical containment, existing destination, hardlink, traversal and exclusive-creation checks remain. Ordinary fresh external outputs, including case-varied spellings of an external directory, still work. These are bounded CLI prewrite guarantees, not adversarial concurrency-lock claims.

`output_guard_checks.py` adds actual normal/optimized archive-writer cases for physical root and nested aliases, absent parents, traversal, reverse script-root spelling, and positive case-varied external output when supported by the filesystem. Availability is reported explicitly on case-sensitive filesystems. The exact earlier 145 source-copy rows, 4,628 history rows and two terminal relocations remain unchanged prefixes/records. `CASE_ALIAS_HISTORY_RELOCATIONS.json` supplies seven further exact-before resolutions for old rows naming the live output-guard program. Selected case-finding/adoption evidence and every changed nonarchive before snapshot are retained under `case_alias01_history`; the old ZIP remains local only. Complete custody and actual current receipts are in `../repairs/case_alias01` relative to the delivery folder. No paper, mathematical adapter, source credit, metadata, prior seal or prior dated status changed; no new compilation, rendering or page view occurred.
'''
 text(p,s)
# Exact before copies and compact selected authored case evidence, never old ZIP.
newrows=[]
for r in obj(W/'BEFORE_COPIES.json')['files']:
 if r['original_path'].endswith('.zip'):continue
 dest='case_alias01_history/before/'+r['original_path'];put(K/dest,(A/r['source_snapshot']).read_bytes())
 newrows.append({**r,'destination':dest,'stage':'case-alias01 exact immediately-before stage'})
selected=['finalization/terminal_admin_20261016/CASE_ALIAS_OUTPUT_FINDING.json','finalization/terminal_admin_20261016/REPORT.md','ROOT_TERMINAL_ADMIN_REVIEW_20261016.json']
selectedpins=[]
for name in selected:
 p=A/name;dest='case_alias01_history/evidence/'+name;put(K/dest,p.read_bytes())
 r={'path':name,'bytes':p.stat().st_size,'sha256':sha(p)};selectedpins.append(r)
 newrows.append({'original_path':name,'source_snapshot':name,'destination':dest,'bytes':r['bytes'],'sha256':r['sha256'],'stage':'case-alias01 exact case finding and ROOT adoption'})
dump(W/'SELECTED_CASE_INPUTS.json',{'files':selectedpins})
# Preserve every prefix row; new history describes only 10 changed inputs and three authored case records.
oldcopies=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json');oldcopies['files']+=newrows;dump(K/'REPAIR01_STAGE_COPIES.json',oldcopies);dump(W/'NEW_COPY_ROWS.json',{'files':newrows})
history=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json');reloc=[]
for index,r in enumerate(history['references']):
 if r.get('destination')=='output_guard_checks.py':reloc.append({'reference_index':index,'historical_reference':r,'current_exact_destination':'case_alias01_history/before/preprint_v1_0/verification_kit/output_guard_checks.py','reason':'Exact old live-program bytes retained; unchanged old row now resolves to its before snapshot.'})
dump(K/'CASE_ALIAS_HISTORY_RELOCATIONS.json',{'scope':'Additional exact resolutions; existing two terminal relocation rows remain unchanged.','rows':reloc})
append=[]
for r in obj(W/'BEFORE_COPIES.json')['files']:
 h={'stage':'case-alias01-changed-before','inventory':'repairs/case_alias01/BEFORE_COPIES.json','original_path':r['original_path'],'bytes':r['bytes'],'sha256':r['sha256']}
 if r['original_path'].endswith('.zip'):h.update(disposition='omitted',reason='Exact old ZIP retained locally at '+r['source_snapshot']+'; no current or duplicate old archive is newly packed.')
 else:h.update(disposition='exact_captured_stage_or_canonical_copy',destination='case_alias01_history/before/'+r['original_path'])
 append.append(h)
for r in selectedpins:append.append({'stage':'case-alias01-selected-evidence','inventory':'repairs/case_alias01/SELECTED_CASE_INPUTS.json','original_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'disposition':'exact_captured_stage_or_canonical_copy','destination':'case_alias01_history/evidence/'+r['path']})
history['references']+=append;history['inventory_counts'].update({'case-alias01-changed-before':10,'case-alias01-selected-evidence':3});dump(K/'REPAIR01_HISTORY_RESOLUTION.json',history);dump(W/'APPENDED_HISTORY_ROWS.json',{'references':append})
dump(W/'AUTHORING_COMPLETE.json',{'utc':now,'new_exact_copies':len(newrows),'new_history_rows':len(append),'new_relocations':len(reloc),'status':'Authored support payload; validation and ROOT adoption/new whole03 pending.'})
with (W/'RESEARCH_LOG.md').open('a') as f:f.write('- '+now+': Added physical ancestor identity guard and current mandatory whole03 checkpoint, preserving old dated states. Appended 12 exact copies, 13 compact historical references and seven relocation records. Bounded support repair estimate 45%; mathematical research estimate 60%.\n')
print(json.dumps(obj(W/'AUTHORING_COMPLETE.json')))
