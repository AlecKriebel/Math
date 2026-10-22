#!/usr/bin/env python3
"""Bounded custody/admin preparation; no Git, network, compiler or service calls."""
import sys
sys.dont_write_bytecode = True
import datetime
import difflib
import hashlib
import io
import json
from pathlib import Path
import zipfile

F = Path(__file__).resolve().parent
A = F.parent.parent
P = A / 'preprint_v1_0'
K = P / 'kit'

def need(q, m):
    if not q:
        raise ValueError(m)

def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def load(p):
    return json.loads(p.read_text())

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2) + '\n')

def main():
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    baseline = load(F / 'INPUT_PINS.json')['entries']
    before = load(F / 'BEFORE_BYTES.json')['entries']
    before_by_path = {r['path']: r for r in before}
    for r in baseline:
        target = A / r['path']
        if r['path'] == 'preprint_v1_0/kit/scripts/common.py':
            target = F / 'before/kit/scripts/common.py'
        need(pin(target) == {'bytes':r['bytes'], 'sha256':r['sha256']}, 'pre-edit baseline changed ' + r['path'])
    # Existing preparation reports/status/seals remain immutable dated history.
    text = (F/'before/README.md').read_text()
    text = text.replace('custody copies, and individual include/exclude decisions for all 165 preexisting',
                        'original custody copies, supplemental captured-stage records, and individual include/exclude decisions for all 165 preexisting')
    text += '''\n## Bounded repair checkpoint, 16 October 2026\n\nThe first complete whole-package review found one P3 filesystem case-alias\noutput-guard bypass. This repair retains lexical exclusions and additionally\ncompares every existing output ancestor's device/inode identity with every\nexisting protected root, covering case and normalization aliases without a\nplatform-specific lowercase rule. Missing original roots remain optional.\nFresh-leaf, real-ancestor, traversal, symlink and exclusive-create protections\nremain. No protection against hostile concurrent filesystem mutation is claimed.\n\n`kit/CURRENT_REPAIR.json` is the current repair-stage accounting: one complete\nwhole review, minimum two, the sole P3 addressed pending root adoption and a\nNEW complete whole review02. Publication-ready/published remain false; ordered\nservices remain held at PR #1032. The original zero-review preparation records\nabove and in STATUS retain their dated meaning. The proof, PDF, TeX, mathematical\nchecker and native bibliographic metadata are unchanged. Supplemental custody\nrecords preserve complete safe authored whole01/root-adoption evidence and exact\nbefore-bytes of changed interfaces. Old ZIPs, third-party bodies/text/pixels and\nraw compiler streams are not redistributed. Current controls do not replay omitted\nhistorical programs; copied review programs are historical evidence only.\n'''
    (P/'README.md').write_text(text)
    text = (F/'before/kit/README.md').read_text()
    text = text.replace('paths, traversal components and existing PDF-output directories are rejected',
                        'paths, actual case/normalization aliases of protected directories, traversal\ncomponents and existing PDF-output directories are rejected')
    text = text.replace('and is not a dependency for verification or calculation. The scripts create',
                        'and is not a dependency for verification or calculation. Existing protected\nroot identities are compared against every existing output ancestor, in addition\nto lexical containment. This does not promise safety against hostile concurrent\nfilesystem mutation. The scripts create')
    text += '''\n## Repair-stage checkpoint, 16 October 2026\n\n`CURRENT_REPAIR.json` records one complete whole review and the sole P3 repair.\nA NEW complete whole review02 is required after root adoption; minimum two\ncomplete reviews, publication-ready/published false, services held at #1032.\nThe 15 October zero-review preparation STATUS and copied historical pending\nrecords are preserved. No paper, mathematics, mathematical checker, priority\nqualification or native bibliographic metadata changed in this repair.\n\n`provenance/repair01/` gives the new hash-only capture, exact authored whole01\nand root-adoption copies, exact changed-interface before-bytes, one distribution\ndecision per captured file and individual resolution of prior pin records.\nThe original 83 copy decisions and 82 exclusions remain byte-exact. Before-byte\ninterfaces are historical, not active commands. Copied reviewer programs are\nauthored historical evidence, not supported kit controls or claims that omitted\nprograms were replayed. Source bodies/text/pixels, raw compiler streams and old\nZIPs remain omitted with hashes and individual reasons.\n'''
    (K/'README.md').write_text(text)
    text = (F/'before/kit/provenance/README.md').read_text()
    text += '''\nThe supplementary `repair01/` layer was captured on 16 October 2026 before\nrepairing the sole P3 outputguard case-alias issue. It does not rewrite the\noriginal INPUT_PINS/CUSTODY or any preparation/whole01 stage. Its CUSTODY lists\na separate decision for every repair-baseline file; STAGE_RESOLUTION resolves\neach prior inventory pin to exact distributed bytes or an explicit metadata-only\nomission. A captured locator is retained even when a path's active bytes changed.\nBefore-bytes and exact whole01/root-adoption records retain historical meanings.\nThe old delivery ZIP is preserved only in the original audit repair records,\nnot redistributed in this kit. None of these inventories is a digital signature.\n'''
    (K/'provenance/README.md').write_text(text)
    repair_status = {
        'recorded_at_utc':utc, 'record_type':'DATED_BOUNDED_REPAIR_STAGE_ONLY',
        'pr':1097, 'head':'ad7b0eeef847da65afe1b691705cfa6e832e8201',
        'complete_whole_package_reviews_completed':1,
        'minimum_complete_whole_package_reviews_required':2,
        'prior_whole01_finding_counts':{'P0':0,'P1':0,'P2':0,'P3':1},
        'addressed_finding':'P3_CASE_ALIAS_PROTECTED_OUTPUT_BYPASS',
        'repair_root_adoption':'PENDING', 'new_complete_whole02':'REQUIRED',
        'mathematics_and_paper':'UNCHANGED', 'priority':'UNKNOWN',
        'native_bibliographic_metadata':'UNCHANGED',
        'publication_ready':False, 'published':False, 'ordered_service_hold_pr':1032,
        'hostile_concurrent_filesystem_mutation_guarantee':False,
        'historical_omitted_program_replayed':False,
    }
    write(K/'CURRENT_REPAIR.json',repair_status)
    write(P/'CURRENT_REPAIR.json',repair_status)
    source_copies = []
    def copy(src, dst, captured):
        need(not dst.exists(), 'copy destination exists '+str(dst))
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(src.read_bytes())
        need(src.read_bytes()==dst.read_bytes(),'source copy mismatch')
        source_copies.append({'captured_locator':captured,
                             'source_path':str(src.relative_to(A)),
                             'copy_path':str(dst.relative_to(K)), **pin(src)})
    selected = [r['path'] for r in baseline if r['path'].startswith('reviews/package_01/')]
    selected += ['ROOT_PREPRINT_REVIEW_01.json','ROOT_WHOLE_PACKAGE_REVIEW_01.json']
    selected += ['preprint_v1_0/'+n for n in ['INPUT_PINS.json','OUTPUT_PINS.json','PREPARATION_REPORT.md','PREPARATION_SEAL.json']]
    selected += [r['path'] for r in baseline if r['path'].startswith('preprint_v1_0/evidence/') and r['path'].endswith('.json')]
    for rel in sorted(set(selected)):
        copy(A/rel,K/'provenance/repair01/selected'/rel,rel)
    for r in before:
        if r['path'].endswith('.zip'):
            continue
        rel = r['path'].removeprefix('preprint_v1_0/')
        copy(A/r['before_path'],K/'provenance/repair01/before'/rel,r['path'])
    for name in ['INPUT_PINS.json','BEFORE_BYTES.json','INITIAL_ENOSPC_ATTEMPTS.json']:
        copy(F/name,K/'provenance/repair01'/name,'repairs/package01/'+name)
    write(K/'provenance/repair01/COPIES.json',{'utc':utc,'entries':source_copies})

    distributed = {}
    for p in sorted(K.rglob('*')):
        if p.is_file() and p != K/'MANIFEST.json':
            r=pin(p);distributed.setdefault((r['bytes'],r['sha256']),[]).append(str(p.relative_to(K)))
    custody=[]
    for r in baseline:
        value={'captured_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256']}
        matches=distributed.get((r['bytes'],r['sha256']),[])
        if matches:
            value.update(decision='EXACT_DISTRIBUTED_BYTES',copy_path=matches[0])
        else:
            if r['path'].endswith('.zip'):
                reason='Old ZIP omitted; exact prior bytes retained only in original repair before/ custody, not distributed.'
            elif '/sources/' in r['path'] or r['path'].startswith('root_reproduction/') or '/tmp/' in r['path']:
                reason='Primary source body/text/pixels or local derivative/program/compiler stream omitted; metadata-only captured hash, no replay claim.'
            else:
                reason='Local historical artifact omitted from this portable layer; captured locator/hash retained; no distributed-file or replay claim.'
            value.update(decision='EXCLUDED',reason=reason)
        custody.append(value)
    write(K/'provenance/repair01/CUSTODY.json',{'utc':utc,'capture':'INPUT_PINS.json','entries':custody})

    # Resolve every row in every preexisting inventory, including historical source
    # renders and already selected duplicates, without assuming a stale root label.
    actual={}
    for r in baseline:
        path=A/r['path']
        if r['path'] in before_by_path:
            path=A/before_by_path[r['path']]['before_path']
        need(pin(path)=={'bytes':r['bytes'],'sha256':r['sha256']},'before-stage resolution '+r['path'])
        actual.setdefault((r['bytes'],r['sha256']),[]).append(str(path.relative_to(A)))
    stage_rows=[]
    for b in baseline:
        if not b['path'].endswith('PINS.json'):
            continue
        source=A/b['path']
        value=load(source)
        rows=next((value[k] for k in ['entries','files','records','renders'] if isinstance(value.get(k),list)),[])
        for index,r in enumerate(rows):
            size=r.get('bytes',r.get('size'))
            digest=r.get('sha256')
            need(isinstance(size,int) and isinstance(digest,str),'unsupported pin row '+b['path'])
            locator=r.get('snapshot_path',r.get('path',r.get('file',r.get('repository_path'))))
            key=(size,digest)
            out={'inventory':b['path'],'row_zero_based':index,'captured_locator':locator,
                 'bytes':size,'sha256':digest}
            if actual.get(key):
                out['original_audit_resolution']={'state':'EXACT_CURRENT_OR_CAPTURED_BEFORE_BYTES','path':actual[key][0]}
            else:
                out['original_audit_resolution']={'state':'INDIVIDUAL_OMISSION','reason':'No retained current/before byte object with this old-stage identity; historical metadata only.'}
            if distributed.get(key):
                out['portable_resolution']={'state':'EXACT_DISTRIBUTED_BYTES','path':distributed[key][0]}
            else:
                out['portable_resolution']={'state':'INDIVIDUAL_OMISSION','reason':'Historical body/program/derivative/oldZIP or unselected artifact is not distributed; this captured locator and exact hash do not claim local availability or replay.'}
            stage_rows.append(out)
    write(K/'provenance/repair01/STAGE_RESOLUTION.json',{
        'utc':utc,'scope':'Every row of every preexisting *PINS.json inventory, including immutable selected duplicates; explicit captured locators and byte identities',
        'entries':stage_rows})
    (K/'provenance/repair01/README.md').write_text('''# Repair01 captured-stage custody\n\nINPUT_PINS hashes all332 regular audit files before this repair. COPIES records\neach supplementary exact authored source-copy pair. CUSTODY gives an individual\ndistributed-byte or omission decision for every captured file. STAGE_RESOLUTION\nresolves every row of every preexisting pin inventory, including unchanged\noriginal/selected duplicate manifests, to exact current/captured-before audit\nbytes and, separately, portable bytes or individual omission. Hash-equivalent\ncopy locators are explicit and do not relabel an old path as an active interface.\n\nThe original165-entry capture and83/82 custody decisions remain byte-exact.\nThe complete safe authored whole01 records, root adoption and preparation\nmetadata are exact copies. Before/ holds the old active code/docs/manifest and\nexternal hash binding, not an old ZIP. Third-party bodies/text/pixels, raw compiler\nstreams and old ZIPs are omitted. Copied reviewer programs are historical\nevidence only; supported commands remain the scripts/ interfaces in the top\nREADME. No omitted program replay or universal proof-by-enumeration is claimed.\n\nThe current repair addresses the one physical case-alias guard finding; root\nadoption and a NEW complete whole02 review are required. Minimum two reviews,\npublication-ready/published false, services held atPR#1032. This layer does not\nchange mathematical proof, PDF/TeX, checker or bibliographic metadata.\n''')

    files=sorted(q for q in K.rglob('*') if q.is_file() and q.name!='MANIFEST.json')
    # Only the top-level manifest self-excludes; historical before/manifest remains a payload.
    files=sorted(q for q in K.rglob('*') if q.is_file() and q != K/'MANIFEST.json')
    write(K/'MANIFEST.json',{'schema':1,'scope':'All distributed kit files except this manifest. External delivery descriptors excluded to avoid hash cycles.',
                            'entries':[{'path':str(q.relative_to(K)),**pin(q)} for q in files]})
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_STORED) as z:
        for q in sorted(q for q in K.rglob('*') if q.is_file()):
            name=q.relative_to(K).as_posix()
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0))
            info.create_system=3; info.external_attr=0o100644<<16
            z.writestr(info,q.read_bytes())
    (P/'pr1097_support_v1_0.zip').write_bytes(stream.getvalue())
    binding=load(F/'before/DEPOSIT_BINDING.json')
    binding['kit_manifest_sha256']=pin(K/'MANIFEST.json')['sha256']
    binding['files']=[{'name':n,**pin(P/n)} for n in ['paper.pdf','pr1097_support_v1_0.zip']]
    write(P/'DEPOSIT_BINDING.json',binding)
    changes=[];diff=[]
    for r in baseline:
        current=pin(A/r['path'])
        if current != {'bytes':r['bytes'],'sha256':r['sha256']}:
            need(r['path'] in before_by_path,'unpermitted existing edit '+r['path'])
            old=A/before_by_path[r['path']]['before_path']
            changes.append({'path':r['path'],'before':{'bytes':r['bytes'],'sha256':r['sha256']},'after':current,'before_path':str(old.relative_to(A))})
            if not r['path'].endswith('.zip'):
                diff.extend(difflib.unified_diff(old.read_text().splitlines(True),(A/r['path']).read_text().splitlines(True),fromfile='before/'+r['path'],tofile='after/'+r['path']))
            else:
                diff.append('\nBINARY ZIP CHANGE '+r['path']+'\n'+json.dumps(changes[-1],indent=2)+'\n')
    write(F/'CURRENT_CHANGES.json',{'utc':utc,'baseline_count':len(baseline),'changes':changes,'unchanged':len(baseline)-len(changes)})
    (F/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(diff))
    write(F/'CONSTRUCTION.json',{'utc':utc,'status':'BOUNDED_REPAIR_CONSTRUCTED_PENDING_ACTUAL_VALIDATION',
        'baseline':len(baseline),'changed_existing':len(changes),'supplementary_source_copies':len(source_copies),
        'prior_inventory_rows':len(stage_rows),'old_custody_copies':83,'old_custody_exclusions':82,
        'paper':pin(P/'paper.pdf'),'archive':pin(P/'pr1097_support_v1_0.zip'),
        'publication_ready':False,'published':False,'new_complete_whole02_required':True})
    print(json.dumps(load(F/'CONSTRUCTION.json'),indent=2))

if __name__=='__main__':
    main()
