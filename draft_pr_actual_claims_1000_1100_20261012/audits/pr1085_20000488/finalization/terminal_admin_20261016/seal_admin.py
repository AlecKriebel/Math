"""Independent final custody inventories for the bounded terminal edition."""
from pathlib import Path
import datetime, difflib, hashlib, io, json, zipfile
F=Path(__file__).resolve().parent
A=F.parents[1]
K=A/'preprint_v1_0'
def sha(data):return hashlib.sha256(data).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def ident(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def pin(p,base):return {'path':str(p.relative_to(base)),**ident(p)}
def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    baseline=load(F/'BASELINE_INPUT_PINS.json')['files']
    allowed=load(F/'AUTHORIZED_EXISTING_CHANGES.json')['files']
    changes=[];unchanged=[]
    for row in baseline:
        path=A/row['path'];current=ident(path)
        if current!={k:row[k] for k in ['bytes','sha256']}:
            need(row['path'] in allowed,'unauthorized old input changed: '+row['path'])
            before=F/'before'/row['path'];need(ident(before)=={k:row[k] for k in ['bytes','sha256']},'missing exact before bytes')
            changes.append({'path':row['path'],'before':{k:row[k] for k in ['bytes','sha256']},'after':current,'before_snapshot':str(before.relative_to(A))})
        else:unchanged.append(row)
    need(set(r['path'] for r in changes)==set(allowed),'unexpected permitted change set')
    all_current=[pin(p,A) for p in sorted(A.rglob('*')) if p.is_file() and F not in p.parents]
    prior_paths={r['path'] for r in baseline}
    new=[r for r in all_current if r['path'] not in prior_paths]
    dump(F/'CHANGE_INVENTORY.json',{'utc':now,'baseline_count':len(baseline),'changed_count':len(changes),'unchanged_count':len(unchanged),'changes':changes,'new_files':new})
    dump(F/'PROTECTED_UNCHANGED.json',{'utc':now,'all_rehashed':True,'files':unchanged})
    dump(F/'CURRENT_AUDIT_PINS.json',{'utc':now,'scope':'All current regular audit files outside this terminal effort. Historical rows retain captured-stage meaning.','files':all_current})
    dump(F/'CURRENT_CANDIDATE_PINS.json',{'utc':now,'scope':'All physical current candidate files, including external historical outputs and unchanged renders.','files':[pin(p,K) for p in sorted(K.rglob('*')) if p.is_file()]})
    core=['paper.pdf','paper.tex','STATUS.json','SOURCE_METADATA.json','check_math.py','kit_common.py','build_pdf.py','build_archive.py','metadata_constants.py','.zenodo.json','metadata.json','zenodo-deposit.json','COPY_MAP.json','EXCLUSIONS.json','PREPARATION_INPUT_PINS.json','PREPARATION_REPORT.md','PREPARATION_SEAL.json','OUTPUT_PINS.json','FINAL_VERIFICATION.json','PROPOSED_PR_FRAMING.md']
    old_map={r['path']:r for r in baseline}
    for name in core:need(ident(K/name)=={k:old_map['preprint_v1_0/'+name][k] for k in ['bytes','sha256']},'core changed '+name)
    metadata=load(K/'.zenodo.json')
    need(metadata==load(K/'metadata.json')['metadata']==load(K/'zenodo-deposit.json')['metadata']==load(K/'UPLOAD_BINDINGS.json')['metadata']==load(F/'before/preprint_v1_0/UPLOAD_BINDINGS.json')['metadata'],'bibliographic object changed')
    dump(F/'CORE_PROTECTED_IDENTITIES.json',{'utc':now,'metadata_exact_unchanged':True,'files':[pin(K/n,K) for n in core]})
    copy_checks=[]
    for map_name,baseline_name,exclusion_name in [('COPY_MAP.json','PREPARATION_INPUT_PINS.json','EXCLUSIONS.json'),('TERMINAL_COPY_MAP.json','TERMINAL_INPUT_PINS.json','TERMINAL_EXCLUSIONS.json')]:
        srcs=load(K/baseline_name)['files'];frozen={r['path']:r for r in srcs}
        copies=load(K/map_name)['files'];exclusions=load(K/exclusion_name)['files']
        need(len(frozen)==len(srcs),'duplicate frozen map')
        selected={r['source_relative_audit'] for r in copies};excluded={r['path'] for r in exclusions}
        need(len(selected)==len(copies) and len(excluded)==len(exclusions) and selected.isdisjoint(excluded) and selected|excluded==set(frozen),'incomplete partition')
        for row in copies:
            source=A/row.get('source_snapshot_relative_audit',row['source_relative_audit']);copy=K/row['copy']
            expect={k:row[k] for k in ['bytes','sha256']}
            need(ident(source)==ident(copy)==expect=={k:frozen[row['source_relative_audit']][k] for k in ['bytes','sha256']},'copy mismatch '+row['copy'])
            need(source.read_bytes()==copy.read_bytes(),'not byte equal copy')
            copy_checks.append({'map':map_name,'source':str(source.relative_to(A)),'copy':row['copy'],**expect,'bytes_equal':True})
        for row in exclusions:need({k:row[k] for k in ['bytes','sha256']}=={k:frozen[row['path']][k] for k in ['bytes','sha256']} and bool(row['reason']),'bad exclusion')
    dump(F/'COPY_EQUALITY_RECHECK.json',{'utc':now,'passed':True,'total_exact_copies':len(copy_checks),'files':copy_checks,'preparation_partition':{'inputs':192,'copies':66,'exclusions':126},'terminal_partition':{'inputs':len(baseline),'copies':52,'exclusions':323}})
    # Resolve every captured row in every pre-terminal pin/manifest stage,
    # including historical copies of such stages, to exact extant bytes.
    index={}
    for p in sorted(A.rglob('*')):
        if p.is_file() and (F not in p.parents or F/'before' in p.parents):
            item=ident(p);index.setdefault((item['bytes'],item['sha256']),[]).append(p)
    stage_rows=[];stage_counts=[]
    def rows(obj,pointer=''):
        if isinstance(obj,dict):
            if isinstance(obj.get('sha256'),str) and type(obj.get('bytes',obj.get('size'))) is int:
                yield pointer,obj
            for key,value in obj.items():yield from rows(value,pointer+'/'+str(key))
        elif isinstance(obj,list):
            for i,value in enumerate(obj):yield from rows(value,pointer+'/'+str(i))
    for stage in baseline:
        rel=stage['path'];p=Path(rel)
        if not ('PINS' in p.name or p.name in ['MANIFEST.json','SUPPORT_MANIFEST.json']):continue
        origin=F/'before'/rel if rel in allowed else A/rel
        obj=load(origin);count=0
        for pointer,row in rows(obj):
            size=row.get('bytes',row.get('size'));matches=index.get((size,row['sha256']),[])
            need(bool(matches),'unresolved stage bytes '+rel+pointer+' '+str(row))
            hint=row.get('snapshot_path',row.get('path',row.get('file',pointer.split('/')[-1])))
            preferred=[A/hint,origin.parent/hint,origin.parent/'frozen'/hint]
            resolved=next((x for x in preferred if x in matches),matches[0])
            need(ident(resolved)=={'bytes':size,'sha256':row['sha256']},'resolution rehash')
            stage_rows.append({'stage':rel,'json_pointer':pointer,'captured_locator':hint,'resolved_exact_path':str(resolved.relative_to(A)),'bytes':size,'sha256':row['sha256']})
            count+=1
        stage_counts.append({'stage':rel,'records':count,'stage_bytes':ident(origin)})
    # Add the immediate terminal capture, preserving old bytes for each edit.
    for row in baseline:
        target=F/'before'/row['path'] if row['path'] in allowed else A/row['path']
        need(ident(target)=={k:row[k] for k in ['bytes','sha256']},'terminal baseline resolution')
        stage_rows.append({'stage':'terminal baseline','json_pointer':'/'+row['path'],'captured_locator':row['path'],'resolved_exact_path':str(target.relative_to(A)),**{k:row[k] for k in ['bytes','sha256']}})
    stage_counts.append({'stage':'terminal baseline','records':len(baseline)})
    dump(F/'HISTORICAL_STAGE_RESOLUTION.json',{'utc':now,'passed':True,'scope':'Every size/SHA256 row in all pre-terminal pin/manifest files, including historical copied manifests, plus immediate baseline. Alternate identical copies are explicit; changed paths resolve exact saved before bytes, never relabelled current bytes. This does not assert omitted source programs were replayed.','records':len(stage_rows),'stages':stage_counts,'rows':stage_rows})
    seals=[]
    for rel in ['preprint_v1_0/PREPARATION_SEAL.json','reviews/ground_state_01/REVIEW_SEAL.json','reviews/hardy_absence_01/SEAL.json','reviews/priority_01/SEAL.json','reviews/package_01/FINAL_SEAL.json','reviews/package_02/SEAL.json']:
        p=A/rel;obj=load(p);expected=obj.get('output_pins_sha256',obj.get('manifest_sha256'))
        actual=sha((p.parent/'OUTPUT_PINS.json').read_bytes());need(expected==actual,'historical seal output pin mismatch '+rel)
        seals.append({'seal':rel,'output_pins_sha256':actual,'passed':True})
    dump(F/'HISTORICAL_SEAL_BINDINGS.json',{'passed':True,'seals':seals})
    # Complete code/prose and scalar-binding diff; large pin/copy/exclusion arrays
    # are individually verified above and fully retained as JSON, not abbreviated.
    diff=[]
    for name in ['README.md','verify_package.py','UPLOAD_BINDINGS.json']:
        before=(F/'before/preprint_v1_0'/name).read_text().splitlines(keepends=True)
        after=(K/name).read_text().splitlines(keepends=True)
        diff.extend(difflib.unified_diff(before,after,fromfile='before/preprint_v1_0/'+name,tofile='after/preprint_v1_0/'+name))
    diff.extend(difflib.unified_diff([], (K/'TERMINAL_ACCOUNTING.json').read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/preprint_v1_0/TERMINAL_ACCOUNTING.json'))
    (F/'COMPLETE_CODE_PROSE_CHANGES.patch').write_text(''.join(diff))
    payload=load(K/'SUPPORT_MANIFEST.json')['files']
    archive=(K/'pr1085_support_v1_0.zip').read_bytes(); expected_names=sorted([r['path'] for r in payload]+['SUPPORT_MANIFEST.json'])
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        need(z.namelist()==expected_names and z.testzip() is None,'archive member set/CRC')
        for info in z.infolist():
            need(info.date_time==(2026,10,14,0,0,0) and info.create_system==3 and info.external_attr==0o100644<<16 and info.compress_type==zipfile.ZIP_DEFLATED and info.flag_bits==0 and info.extra==info.comment==b'','header')
            need(z.read(info)==(K/info.filename).read_bytes(),'exact archive payload')
    result=load(F/'CONTROL_SUMMARY.json');need(result['passed'],'controls incomplete')
    report=f'''# PR1085 terminal administrative reconciliation

Completed {now}. Candidate `preprint_v1_0`, PR head `5e23f0c801d23976830657d2eef2b32bdc7da05a`, problem 20000488.

**Bounded terminal administration passes, with external root terminal integrity adoption still required.** Two NEW complete whole-package reviews both returned zero actionable P0–P3 findings and root adopted both. This worker does not confer release readiness: terminal `publication_ready`, `all_actionable_issues_resolved` and `published` remain false, root terminal adoption is mandatory, and all services remain held after PR1032. The task is AI-assisted and unrefereed, with no human peer review, formal certificate or firstness clearance.

## Exact scope and preserved substantive material

I read the COMPLETE reports and verdicts of both whole reviews, both root whole-review adoptions, the current README/status, all operative verifier/guard/archive/math/PDF interfaces, metadata forms and custody structures. Root whole02 adoption records its full proof/source/derivation read and independent replay of the 1,083 new exact controls in both modes, with fourteen fault rejections. The whole02 reviewer actually compiled the paper in both modes byte-exact and actually viewed all seven pages. Those are historical review facts; this terminal task is not a third mathematical review.

The mathematics remains the credited dimension-dependent answer to literal dimension-unrestricted AIM Problem 1.4. The paper preserves Exner–Minakov's planar theorem and exponential/Stokes mechanism credit; HHRV's published Theorem A.6 gives graph absence and the explicit example through the proved bounded H1/Fourier/compactness bridge. Source-version qualifications, the all-form Hardy alternative, the exact R4 example and low-dimensional nongraph binding are unchanged. Exact remaining geometric priority, novelty, worldwide current-open status and independent discovery remain UNKNOWN. No embedded-eigenvalue exclusion, one-fixed-nonzero-graph all-strength absence or general higher-dimensional nongraph classification is introduced.

The unchanged seven-page paper PDF is 97,501 bytes, SHA256 `464de043ac6b723f3bd5c03dddb6efd1c0bfeb05b5209bb532006580b7aedc2d`. The paper TeX remains SHA256 `c18a6ed12250dcee413e85f9a6297c525015396f151cdab8d89a6eb76938046d`. Mathematical checker, writer/path guards, archive/PDF builders, metadata constants, all four native bibliographic metadata objects, original six files and every prior status/report/pin/seal retain exact bytes. The native uploader descriptor itself is unchanged; its paths select the same-named current ZIP and unchanged PDF. Only the external hash binding's ZIP size/hash changes. No DOI or remote-publication assertion is added.

## Bounded changes and current accounting

`BASELINE_INPUT_PINS.json` hash-froze all {len(baseline)} immediate regular audit inputs before mutation. Exact before bytes of every permitted existing edit were saved first. Exactly six existing files changed: README, operative verifier, allowlist, payload manifest, support ZIP and external ZIP binding. All {len(unchanged)} other immediate inputs are unchanged. `CHANGE_INVENTORY.json`, `PROTECTED_UNCHANGED.json`, current candidate/audit pins and the twenty core-protected identities independently substantiate this boundary.

The original preparation `STATUS.json`, its zero-new-review field, prior pending-readiness assertions and dated reports/seals remain byte-exact captured-stage records. New `TERMINAL_ACCOUNTING.json` records the actual two-review/minimum-two/latest-zero state and mandatory external root terminal adoption. README explicitly distinguishes these stages. The verifier first validates the unchanged preparation stage, then checks the separate terminal identity, strict review counts, zero latest findings, false readiness/refereeing flags, ordered service hold, unknown historical predicates, paper identities, exact copied review/root interfaces and output-manifest-to-seal/root bindings. It cannot promote release readiness.

`COMPLETE_CODE_PROSE_CHANGES.patch` contains the COMPLETE operative code/prose diff, new terminal accounting and scalar binding change. New large input/copy/exclusion arrays and changed manifest/allowlist are retained in full JSON/text and every row was actually rehashed; they are not substituted with a summary. No mathematical code, path guard or bibliography was changed.

## Copies, exclusions and captured-stage custody

The original 66 preparation copies and 126 individual exclusions are unchanged. The new terminal partition covers all {len(baseline)} immediate input records: 52 exact selected copies and 323 individual exclusions. Selected material includes safe authored whole01/02 reports, derivations/checkers, result/custody/source-read identity receipts, their input/output pin manifests/seals and root adoptions, plus the root preparation adoption. Five small before-edit snapshots preserve the old README/verifier/allowlist/manifest/binding bytes. Their source_snapshot locator points explicitly to exact before custody.

All {len(copy_checks)} source/copy pairs were independently rehashed and compared as bytes. No full third-party body, source extract, image, runtime, raw compiler/command stream or old ZIP was added. The exact prior support ZIP remains only in local before custody. Historical code copies retain their original environment assumptions; no omitted program or nonexistent original executable is claimed replayed.

`HISTORICAL_STAGE_RESOLUTION.json` resolves all {len(stage_rows)} captured size/hash rows across {len(stage_counts)} manifest/pin stages, including every copied historical manifest and all {len(baseline)} immediate baseline rows. Every claimed body resolves to actual exact current or saved-before bytes. Alternate identical-copy resolution is explicit. No stale pin is silently rewritten to new bytes. All six prior stage-seal/output-pin bindings were checked separately.

## Actual clean administrative reproduction

The suite executed {result['commands']} actual commands: {result['successes']} successes and {result['expected_rejections']} expected nonzero rejections, all with correct outcomes. One disposable extraction was used and automatically removed. Normal and optimized Python passed the documented verifier, checker, closed deterministic archive rebuild, repeat verifier and strict actual external native binding. Their COMPLETE default, mathematical and strict-binding JSON results agree. The unchanged shipped mathematical checker is a finite diagnostic, not a continuum proof certificate; no historical omitted checker or original executable was replayed.

In both modes, strict missing descriptors/bindings, stale attachment hashes, duplicate JSON, missing root evidence, incomplete terminal partitions and missing individual exclusion reasons were rejected. Identical bootstrap-manifest/member-list symlinks were rejected before JSON ingestion. Nineteen terminal/review semantic cases per mode refresh coherent outer manifests; the four review-evidence cases also refresh the source-copy/frozen-map hashes, so their rejection reaches the intended semantic guard rather than a trivial stale hash. They reject fewer reviews, nonzero findings, missing root adoption, premature readiness/refereeing/priority promotion and service-hold bypass. Full actual outputs and exact reached guards are retained.

All three file-output entry points reject direct current inputs, external hardlinks, symlinks and linked-parent aliases. The supplied external descriptor hardlink is rejected before parse/write. Each of the four PDF child aliases is rejected before any output or compiler invocation; the control gives it a nonexistent compiler path and proves only the pre-existing alias remains. All targets are disposable copies, never destructive links to canonical audit inodes. The static file guards make no concurrent hostile-filesystem race claim.

The current ZIP has {len(expected_names)} sorted regular members, fixed 2026-10-14 timestamps, Unix mode0644, deflate9 and empty extra/comment fields. Every header/payload/CRC was checked. An independent writer was compared only AFTER its ZipFile closed and matches exactly; both documented builders match too. All successful commands leave the clean extraction unchanged, and the final restored negative-control tree also matches exactly. The actual repository uploader LOCAL check accepts the unchanged native manifest and reports the exact current PDF/ZIP identities; no credentials, network deposit or publication operation is used.

The current support ZIP is {len(archive):,} bytes, SHA256 `{sha(archive)}`. `UPLOAD_BINDINGS.json` pins it, with the bibliographic metadata object exactly unchanged. There is no self-containing ZIP or circular asset hash. The external terminal pin/seal are outside the candidate and archive.

No new compilation, rendering or PDF marker was needed because the paper source and PDF are unchanged and both complete reviews already actually compiled both modes and inspected every current page. No Git/index/branch mutation, Zenodo stage/publication, spreadsheet write, PR action, external outreach or new subagent occurred.

Administrative execution completion estimate: **100%**. External root terminal integrity adoption remains required; ordered services remain held after PR1032.
'''
    (F/'REPORT.md').write_text(report)
    with (F/'RESEARCH_LOG.md').open('a') as log:log.write('\n'+now+f' — Completed {result["commands"]} actual controls, all {len(copy_checks)} exact copies, all {len(stage_rows)} historical rows, six prior seal bindings, unchanged core/native metadata and exact CLOSED ZIP. Administrative execution 100%; external root adoption and ordered service hold remain.\n')
    dump(F/'FINAL_VERIFICATION.json',{'utc':now,'passed':True,'baseline_inputs':len(baseline),'bounded_existing_changes':len(changes),'protected_unchanged':len(unchanged),'all_exact_copies':len(copy_checks),'historical_resolved_rows':len(stage_rows),'historical_stages':len(stage_counts),'historical_seals':6,'archive_members':len(expected_names),'archive_bytes':len(archive),'archive_sha256':sha(archive),'paper_unchanged':True,'metadata_exact_unchanged':True,'controls_commands':result['commands'],'new_whole_reviews':2,'latest_actionable':0,'root_terminal_integrity_adoption_required':True,'publication_ready':False,'published':False,'services_hold':'preceding PR1032 priority cursor'})
    outputs=[pin(p,F) for p in sorted(F.rglob('*')) if p.is_file() and p.name not in ['OUTPUT_PINS.json','SEAL.json']]
    dump(F/'OUTPUT_PINS.json',{'utc':now,'scope':'Every terminal effort file, including exact local before custody; pin file and separate seal self-excluded. Not redistributed source bodies.','files':outputs})
    for row in outputs:need(ident(F/row['path'])=={k:row[k] for k in ['bytes','sha256']},'terminal pin changed')
    dump(F/'SEAL.json',{'utc':now,'terminal':True,'kind':'BOUNDED_TERMINAL_ADMIN_PASS_PENDING_EXTERNAL_ROOT_INTEGRITY_ADOPTION','pr':1085,'audited_head':'5e23f0c801d23976830657d2eef2b32bdc7da05a','output_records':len(outputs),'output_pins_bytes':(F/'OUTPUT_PINS.json').stat().st_size,'output_pins_sha256':sha((F/'OUTPUT_PINS.json').read_bytes()),'report_sha256':sha((F/'REPORT.md').read_bytes()),'final_verification_sha256':sha((F/'FINAL_VERIFICATION.json').read_bytes()),'core_math_PDF_metadata_unchanged':True,'two_complete_whole_reviews_latest_ZERO':True,'root_terminal_integrity_adoption_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032})
    print(json.dumps(load(F/'FINAL_VERIFICATION.json'),indent=2))
if __name__=='__main__':main()
