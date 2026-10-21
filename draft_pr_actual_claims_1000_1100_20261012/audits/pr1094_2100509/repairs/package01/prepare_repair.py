"""Bounded package repair; no service, Git, compiler, or source-body copying."""
from pathlib import Path
import datetime
import difflib
import hashlib
import io
import json
import os
import shutil
import stat
import zipfile

R = Path(__file__).resolve().parent
A = R.parent.parent
P = A / 'preprint_v1_0'
K = P / 'kit'
ALLOWED = [
    'preprint_v1_0/kit/scripts/safety.py',
    'preprint_v1_0/kit/README.md',
    'preprint_v1_0/kit/CURRENT_STATUS.json',
    'preprint_v1_0/kit/CUSTODY_MAP.json',
    'preprint_v1_0/kit/MANIFEST.json',
    'preprint_v1_0/README.md',
    'preprint_v1_0/DEPOSIT_BINDING.json',
    'preprint_v1_0/pr1094_supportkit_v1.0.zip',
]

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok, text):
    if not ok: raise ValueError(text)
def writej(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
def rec(path, name):
    b = path.read_bytes()
    return {'path': name, 'bytes': len(b), 'sha256': sha(b)}
def frozen_path(name):
    return R/'before'/name if name in ALLOWED else A/name
def same(row, path):
    return rec(path, row['path']) == {k: row[k] for k in ('path','bytes','sha256')}

def freeze():
    target=R/'FROZEN_INPUT_PINS.json'
    if not target.exists():
        rows=[]
        for path in sorted(A.rglob('*')):
            if R in path.parents or path == R: continue
            if path.is_file() and not path.is_symlink():
                rows.append(rec(path,path.relative_to(A).as_posix()))
        writej(target, {'utc':now(),'scope':'Every preexisting regular audit file, hash-only, before this bounded repair. Repair folder alone excluded.','records':rows})
        for name in ALLOWED:
            src=A/name; dst=R/'before'/name
            dst.parent.mkdir(parents=True,exist_ok=True)
            dst.write_bytes(src.read_bytes())
        writej(R/'ALLOWED_CHANGES.json', {'utc':now(),'records':[rec(R/'before'/n,n) for n in ALLOWED], 'reason':'Only shared guard, current interface/status/custody and their manifest/archive/binding dependencies; no paper or metadata edits.'})
    data=json.loads(target.read_text())
    for row in data['records']:
        need(same(row,frozen_path(row['path'])),'frozen bytes unavailable: '+row['path'])
    return data

def mutate():
    baseline=freeze()
    old=(R/'before/preprint_v1_0/kit/scripts/safety.py').read_text()
    first=old.index('def no_links(path):')
    last=old.index('\ndef regular(path):',first)
    new='''def no_links(path):
    # Inspect the original lexical prefixes before abspath can erase a
    # symlink followed by "..". Ordinary safe sibling "../" paths remain
    # valid. No component is dereferenced through a symlink in this check.
    raw = Path(path)
    if not raw.is_absolute():
        raw = Path.cwd() / raw
    parts = raw.parts
    node = Path(raw.anchor)
    for index, part in enumerate(parts[1:], start=1):
        node = node / part
        if node.is_symlink():
            raise ValueError('symlink component: ' + str(node))
        if index < len(parts) - 1 and node.exists():
            require(node.is_dir(), 'ancestor is not a directory: ' + str(node))
    return Path(os.path.abspath(raw))
'''
    old=old[:first]+new+old[last:]
    first=old.index('    # Preflight all parent components before any mkdir or subprocess write.')
    last=old.index('    return p',first)
    new='''    # A case-insensitive filesystem can give the same protected directory
    # a differently cased lexical name. Compare physical identity for EVERY
    # existing output ancestor, including ancestors above absent components.
    # This is a static preflight, not a concurrent-filesystem security claim.
    root_stat = r.stat()
    root_identity = (root_stat.st_dev, root_stat.st_ino)
    for parent in p.parents:
        if parent.exists():
            require(parent.is_dir(), 'output ancestor is not a directory')
            parent_stat = parent.stat()
            require((parent_stat.st_dev, parent_stat.st_ino) != root_identity,
                    'output physically overlaps protected kit: ' + str(p))
'''
    old=old[:first]+new+old[last:]
    (K/'scripts/safety.py').write_text(old)

    text=(R/'before/preprint_v1_0/kit/README.md').read_text()
    text=text.replace('reject input-tree overlap, and create subprocess outputs only inside one fresh directory.',
        'reject input-tree overlap, check every existing output ancestor against the protected kit\'s device/inode identity (including case aliases on a case-insensitive filesystem), and create subprocess outputs only inside one fresh directory. Safe ordinary `../` sibling destinations remain supported; a symlink component followed by `..` is rejected before normalization.')
    text=text.replace('`CUSTODY_MAP.json` partitions every preexisting audit input individually into an exact selected authored copy or an exclusion.',
        '`CUSTODY_MAP.json` partitions every audit input captured before the 16 October 2026 repair individually into an exact selected authored copy or an exclusion. Its original 171-input stage remains intact as dated history. Selected whole-review/root evidence and the original bytes of every changed interface are appended under `historical/repair01/`; changed original paths resolve to those explicit before-repair copies.')
    text += '''
## Current repair checkpoint (16 October 2026 UTC)

One new complete whole-package review has finished. It accepted the complete
mathematics and conservative priority framing, with one P3 mismatch between
the advertised lexical symlink rejection and the shared path checker. This
bounded repair checks lexical prefixes before normalization and also rejects
physical input-tree aliases through differently cased existing ancestors.
The manuscript, PDF and every native bibliographic metadata field are
unchanged. The first review and original preparation receipts are exact
captured-stage history. A NEW complete independent whole-package review is
still required, with a minimum of two total new complete reviews and all
actionable findings resolved. Readiness and publication remain false, and
all external services remain held after the preceding PR #1032 disposition.
'''
    (K/'README.md').write_text(text)
    status=json.loads((R/'before/preprint_v1_0/kit/CURRENT_STATUS.json').read_text())
    status.update({'stage':'Bounded package repair checkpoint, 2026-10-16 UTC; before deposit or publication',
        'mathematics':'Complete exact classification accepted by two mathematical families, root and complete whole review 01; proof and paper unchanged by repair',
        'completed_new_whole_package_reviews':1,
        'whole_review_01_findings':{'P0':0,'P1':0,'P2':0,'P3':1},
        'bounded_repair':'Lexical-prefix symlink rejection before dot-dot normalization, plus physical protected-root identity for every existing output ancestor including case aliases',
        'new_complete_whole_review_required':True,
        'root_preprint_adoption_required':False,
        'root_repair_adoption_required':True})
    writej(K/'CURRENT_STATUS.json',status)

    outer=(R/'before/preprint_v1_0/README.md').read_text()
    outer=outer.replace('The support kit includes 57 exact selected authored historical copies and\n114 individually justified exclusions from a 171-file hash-only baseline.',
        'The initial preparation included 57 exact selected authored historical\ncopies and 114 individually justified exclusions from a 171-file hash-only\nbaseline. That dated stage is preserved; the current repair custody map\nappends exact whole-review/root evidence and before-repair interfaces.')
    outer=outer.replace('`kit/CURRENT_STATUS.json` records zero such\nnew reviews, false readiness/publication flags, and the ordered service hold',
        'The initial preparation recorded zero such new reviews. After the\n16 October 2026 bounded path-check repair, `kit/CURRENT_STATUS.json` records\none completed full review and requires a NEW complete full review, retaining\nfalse readiness/publication flags and the ordered service hold')
    outer += '\nThe bounded repair report and full before/after code/prose diff are in\n`../repairs/package01/`. The paper, PDF and shared native metadata object\nare byte-identical to the reviewed preparation. No new compilation or layout\nchange was needed for this shared-guard repair.\n'
    (P/'README.md').write_text(outer)

    # Original partition rows are preserved. New rows identify every remaining
    # before-repair input individually. Current edited paths use exact before
    # bytes rather than pretending the dated earlier hashes describe live files.
    custody=json.loads((R/'before/preprint_v1_0/kit/CUSTODY_MAP.json').read_text())
    old_origins={r['original_path'] for r in custody['copies']}|{r['path'] for r in custody['exclusions']}
    appended_copies=[]; appended_exclusions=[]
    for row in baseline['records']:
        name=row['path']
        if name in old_origins: continue
        select=(name in ALLOWED or name.startswith('reviews/package_01/')
                or name in ('ROOT_PREPRINT_REVIEW_01.json','ROOT_WHOLE_PACKAGE_REVIEW_01.json')
                or name.startswith('root_reproduction/') and name.endswith(('.py','.json'))
                or name in ('preprint_v1_0/FROZEN_INPUT_PINS.json','preprint_v1_0/OUTPUT_PINS.json',
                            'preprint_v1_0/PREPARATION_SEAL.json','preprint_v1_0/PREPARATION_REPORT.md'))
        excluded=(name.endswith(('.png','.pdf')) and name != 'preprint_v1_0/paper.pdf'
                  or '/.private_sources/' in name or '/.venv/' in name
                  or name.endswith(('.stdout.txt','.stderr.txt','.log')))
        if select and not excluded:
            copy='historical/repair01/before/'+name if name in ALLOWED else 'historical/repair01/'+name
            dst=K/copy;dst.parent.mkdir(parents=True,exist_ok=True)
            dst.write_bytes(frozen_path(name).read_bytes())
            need(same(row,dst),'selected copy changed: '+name)
            mapped={'original_path':name,'copy_path':copy,'bytes':row['bytes'],'sha256':row['sha256']}
            if name in ALLOWED: mapped['resolution']='Exact before-repair bytes of this explicitly edited path; not its current successor.'
            custody['copies'].append(mapped);appended_copies.append(mapped)
        else:
            reason=('Third-party body/extraction/image, compiler stream or runtime is intentionally not redistributed.' if excluded
                    else 'Duplicate/current preparation interface, derivative or already selected historical payload; individually hashed and retained outside this selected publication kit.')
            item={'path':name,'bytes':row['bytes'],'sha256':row['sha256'],'reason':reason}
            custody['exclusions'].append(item);appended_exclusions.append(item)
    custody['stage']='Captured before bounded package repair, 2026-10-16 UTC; original 2026-10-15 partition rows preserved'
    custody['exact_partition_count']=len(baseline['records'])
    custody['scope']='Every input in the repair hash-only baseline is individually selected or excluded; no third-party body/image/raw compiler stream/runtime is redistributed. Changed input paths resolve to explicitly retained exact before bytes. Earlier labels remain dated history.'
    writej(K/'CUSTODY_MAP.json',custody)
    writej(R/'SOURCE_COPY_SELECTION.json',{'utc':now(),'baseline_count':len(baseline['records']),
        'original_partition_copies_preserved':len(custody['copies'])-len(appended_copies),
        'original_partition_exclusions_preserved':len(custody['exclusions'])-len(appended_exclusions),
        'appended_copies':appended_copies,'appended_exclusions':appended_exclusions,
        'current_copies':len(custody['copies']),'current_exclusions':len(custody['exclusions'])})
    # The repair's own baseline is a new authored receipt, not a preexisting
    # input or an invented additional partition row.
    dst=K/'historical/repair01/FROZEN_REPAIR_INPUT_PINS.json'
    dst.write_bytes((R/'FROZEN_INPUT_PINS.json').read_bytes())
    writej(R/'NEW_RECEIPT_COPY.json',{'source':'repairs/package01/FROZEN_INPUT_PINS.json',
        'copy':'preprint_v1_0/kit/historical/repair01/FROZEN_REPAIR_INPUT_PINS.json',
        'bytes':dst.stat().st_size,'sha256':sha(dst.read_bytes()),
        'scope':'New receipt copied exactly; not counted as a preexisting input.'})

    manifest={'schema':1,'hash_scope':'Every regular kit file except this root manifest; historical manifests retain captured-stage meaning.',
        'records':[rec(p,p.relative_to(K).as_posix()) for p in sorted(K.rglob('*')) if p.is_file() and p!=K/'MANIFEST.json']}
    writej(K/'MANIFEST.json',manifest)
    buffer=io.BytesIO()
    names=sorted(['MANIFEST.json']+[r['path'] for r in manifest['records']])
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as archive:
        for name in names:
            q=zipfile.ZipInfo(name,(1980,1,1,0,0,0));q.create_system=3
            q.external_attr=0o100644<<16;q.compress_type=zipfile.ZIP_STORED
            archive.writestr(q,(K/name).read_bytes())
    (P/'pr1094_supportkit_v1.0.zip').write_bytes(buffer.getvalue())
    binding=json.loads((R/'before/preprint_v1_0/DEPOSIT_BINDING.json').read_text())
    binding['files']=[rec(P/name,name) for name in ('paper.pdf','pr1094_supportkit_v1.0.zip')]
    writej(P/'DEPOSIT_BINDING.json',binding)
    native=json.loads((P/'zenodo-deposit.json').read_text())
    need(binding['metadata']==native['metadata']==json.loads((K/'.zenodo.json').read_text())
         ==json.loads((K/'metadata.json').read_text())==json.loads((K/'metadata_api.json').read_text())['metadata'], 'metadata object changed')

    changes=[]
    for row in baseline['records']:
        name=row['path']; current=rec(A/name,name)
        if current != {k:row[k] for k in ('path','bytes','sha256')}:
            need(name in ALLOWED,'unapproved changed input: '+name)
            changes.append({'path':name,'before':{k:row[k] for k in ('bytes','sha256')},
                            'after':{k:current[k] for k in ('bytes','sha256')},
                            'exact_before_path':'before/'+name})
    need(len(changes)==len(ALLOWED),'expected bounded changes not exact')
    writej(R/'INPUT_PRESERVATION.json',{'utc':now(),'total_before':len(baseline['records']),
        'allowed_changes':changes,'unchanged_count':len(baseline['records'])-len(changes),
        'every_unchanged_input_rehashed':True,'every_changed_before_file_exact':True,
        'proof_PDF_native_metadata_unchanged':True})

    stage_specs=[('preprint_v1_0/FROZEN_INPUT_PINS.json',A),
                 ('preprint_v1_0/OUTPUT_PINS.json',P),
                 ('reviews/package_01/INPUT_PINS.json',A),
                 ('reviews/package_01/OUTPUT_PINS.json',A/'reviews/package_01')]
    stages=[]
    for spec,base in stage_specs:
        data=json.loads((A/spec).read_text());rows=data.get('records',data.get('entries'))
        resolution=[]
        for row in rows:
            name=(base/row['path']).relative_to(A).as_posix()
            source=frozen_path(name)
            need(same(row,source),'dated stage row unresolved: '+spec+' '+row['path'])
            resolution.append({'path':row['path'],'audit_path':name,'bytes':row['bytes'],'sha256':row['sha256'],
                'resolution':('repairs/package01/before/'+name if name in ALLOWED else name)})
        stages.append({'inventory':spec,'inventory_sha256':sha((A/spec).read_bytes()),'count':len(rows),'records':resolution})
    writej(R/'PRIOR_STAGE_RESOLUTION.json',{'utc':now(),'scope':'Every row of each original preparation/review stage resolved to unchanged live bytes or exact explicit before-repair bytes. No dated inventory was rewritten.','stages':stages})
    parts=[]
    for name in ALLOWED:
        if not name.endswith(('.py','.md')): continue
        before=(R/'before'/name).read_text().splitlines(keepends=True)
        after=(A/name).read_text().splitlines(keepends=True)
        parts.extend(difflib.unified_diff(before,after,fromfile='before/'+name,tofile='current/'+name))
    (R/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(parts))
    writej(R/'CURRENT_ARTIFACT_PINS.json',{'utc':now(),'records':[rec(p,p.relative_to(A).as_posix())
        for p in sorted(P.rglob('*')) if p.is_file() and not p.is_symlink()]})
    print(json.dumps({'status':'REPAIR_BUILT_PENDING_VALIDATION','baseline':len(baseline['records']),
        'changes':len(changes),'copy_count':len(custody['copies']),'exclusion_count':len(custody['exclusions']),
        'archive_bytes':len(buffer.getvalue()),'archive_sha256':sha(buffer.getvalue()),'archive_members':len(names)},indent=2))

if __name__=='__main__': mutate()
