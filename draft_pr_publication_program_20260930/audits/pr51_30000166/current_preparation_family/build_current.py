"""Text-only private science builder. No imported/compiled/executed production helpers."""
import datetime
import hashlib
import json
from pathlib import Path
import stat

F=Path(__file__).resolve().parent
A=F.parent
O=A/'original_preparation_family'
S=O/'source_snapshot'
A45=A.parent/'pr45_9900007'
HEAD='8006dd5f134ad0a2fa930e7278d3cb17945f4201'
checks=0


def require(x):
    global checks
    assert x
    checks+=1


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def pairs(ps):
    d={}
    for k,v in ps:require(k not in d);d[k]=v
    return d


def read(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs)


def row(p,role):
    s=p.lstat();require(stat.S_ISREG(s.st_mode) and s.st_nlink==1)
    return {'path':str(p),'bytes':s.st_size,'sha256':sha(p),
            'full_mode':format(stat.S_IMODE(s.st_mode),'04o'),'role':role}


def write(p,b):
    require(p.is_relative_to(F));p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as t:t.write(b)
    if p.is_relative_to(F/'current_science') or p.is_relative_to(F/'original_head_archive'):p.chmod(0o444)


def jwrite(p,d):write(p,(json.dumps(d,indent=2)+'\n').encode())


def closed_input(name,schema,pin,count,mode_key,count_key):
    root=A/name;m=root/'SELF_MANIFEST.json';require(sha(m)==pin)
    d=read(m);require(d['schema']==schema and d[count_key]==count)
    names=[q['path'] for q in d['files']];require(names==sorted(set(names)))
    require(sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())==sorted(names+['SELF_MANIFEST.json']))
    rows=[row(m,'actual ROOT self-only manifest')]
    for q in d['files']:
        r=q['path'];require(not Path(r).is_absolute() and '..' not in Path(r).parts)
        x=row(root/r,'closed first-party external payload')
        require(x['bytes']==q['bytes'] and x['sha256']==q['sha256'] and x['full_mode']=='0444')
        require(q[mode_key] in ('0444','0o444'));rows.append(x)
    require(rows[0]['full_mode']=='0444')
    actual_dirs=sorted(['.']+[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()])
    declared=d['directories']
    if name=='original_preparation_family':require(actual_dirs==declared)
    else:
        parsed=sorted('.' if q['path']=='' else q['path'] for q in declared);require(parsed==actual_dirs)
        for q in declared:
            key='mode' if name=='eta_algebra_adversary_family' else 'full_mode'
            require(q[key] in ('0555','0o555'))
            require(stat.S_IMODE((root/q['path']).stat().st_mode)==0o555)
    dirs=[{'path':str(root/r),'full_mode':format(stat.S_IMODE((root/r).stat().st_mode),'04o')} for r in actual_dirs]
    return {'name':name,'manifest_sha256':pin,'schema_actual':schema,
            'payload_files_actual':count,'directories':dirs,'rows':rows}


def root_capture(name,pid,pin):
    cap=A45/name;d=read(cap/'CAPTURE.json')
    require(d['schema']=='root-explicit-command-capture/v1' and d['actual_execution'] is True)
    require(d['pid']==pid and d['exit_code']==0 and d['completed'] is True and d['status']=='PASS')
    require(datetime.datetime.fromisoformat(d['started_utc'])<datetime.datetime.fromisoformat(d['finished_utc']))
    require(sha(cap/'prelaunch_operator.py')==d['operator_sha256'] and d['operator_unchanged'] is True)
    for k in ('stdout','stderr'):
        p=cap/d[k]['path'];require(p.stat().st_size==d[k]['bytes'] and sha(p)==d[k]['sha256'])
    require(d['stderr']['bytes']==0)
    require(read(cap/'stdout.bin')['manifest_sha256']==pin)
    require(sorted(p.name for p in cap.iterdir())==['CAPTURE.json','prelaunch_operator.py','stderr.bin','stdout.bin'])
    return {'name':name,'actual_child_pid':pid,'actual_argv':d['argv'],'actual_cwd':d['cwd'],
            'started_utc':d['started_utc'],'finished_utc':d['finished_utc'],
            'rows':[row(p,'actual completed ROOT CAP4, read in place') for p in sorted(cap.iterdir())]}


def main():
    require(F.name=='current_preparation_family' and not (F/'SELF_MANIFEST.json').exists())
    inputs=[closed_input('original_preparation_family','pr51-original-preparation-self-only-manifest/v1','d358945982e92b1e3fc121cbdf54664304f6ae6118375f3fb1da8c590d75e57d',188,'mode','files_count'),
            closed_input('eta_algebra_adversary_family','pr51-eta-algebra-adversary-self-only-closure/v1','dc8d2d207850534823110c9eff6055ad30d0b21fc0ec84d82a74f27b4475453b',23,'mode','files_count'),
            closed_input('modular_geometry_adversary_family','pr51-modular-geometry-adversary-self-only-closure/v1','29a9e737671999b864e02364a6a3f47f584f2b4d5c13cb41b230f14632e05ac6',35,'full_mode','payload_file_count')]
    capspec=[('original_preparation',54239,54410,inputs[0]['manifest_sha256']),('eta_algebra_review',60953,63869,inputs[1]['manifest_sha256']),('modular_geometry_review',60971,63874,inputs[2]['manifest_sha256'])]
    caps=[]
    for name,closer,reader,pin in capspec:
        caps.extend([root_capture('root_pr51_'+name+'_closure_actual_capture',closer,pin),root_capture('root_pr51_'+name+'_closed_readback_actual_capture',reader,pin)])
        require(datetime.datetime.fromisoformat(caps[-2]['finished_utc'])<datetime.datetime.fromisoformat(caps[-1]['started_utc']))
    ident=read(O/'SNAPSHOT_IDENTITY.json');require(ident['original_head']==HEAD and ident['science_files_count']==15)
    rows=ident['files'];require(sum(q['bytes'] for q in rows)==53495)
    replacements={'README.md','SOURCE_STATUS.md','PR_DRAFT.md','RESEARCH_LOG.md','provenance.json','independent_review/REVIEW.md'}
    for q in rows:
        r=q['snapshot_relative_path'];b=(S/r).read_bytes()
        require(len(b)==q['bytes'] and hashlib.sha256(b).hexdigest()==q['sha256'] and q['git_mode']=='100644')
        write(F/'original_head_archive'/r,b)
        if r not in replacements:write(F/'current_science'/r,b)
    source=(S/'SOURCE_STATUS.md').read_text()
    old='This is a source correction and proof-scope audit, not a new discovery. Separate review of this package is required before its draft PR.'
    new='This is a publication-free known-result reconciliation, not a new discovery. Two fresh independent mathematical families reviewed the exact original body on 2026-10-03 with no mandatory science correction. This preparer is not an independent third mathematical reviewer. Native changes, acceptance, merge and publication remain unapproved here.'
    require(source.count(old)==1);source=source.replace(old,new)
    old="Both arXiv records currently show one version, with no withdrawal notice. The bounded current-source search found no correction affecting this theorem. Yasuda's"
    new="The original archive's version/search statements are historical. The two 2026-10-03 reviews accessed both versioned primary manuscripts and recorded bounded access/version limits; no exhaustive correction absence is asserted. Their SOURCE observations distinguish readable primary text from unavailable inspectable pixels and an unobtained typeset journal proof. Yasuda's"
    require(source.count(old)==1);source=source.replace(old,new)
    old="The original report's displayed prime-case formula on p. 54 prints $(p^2-1)/12$. Direct inspection of the PDF confirms that denominator; with the report's own $\\eta=q^{1/24}E(q)$ definition, the correct denominator is 24. Berkovich–Garvan's equation (1.6) uses 24. This local normalization discrepancy has no effect on the coefficient-positivity theorem."
    new="The historical archive claims visual inspection of a denominator-12 prime display. Fresh accessible primary text was read by the preparer and new families, but their screenshot requests did not supply inspectable pixels; none of those fresh reads revalidates the historical PDF hashes or visual receipt. Direct substitution in $\\eta=q^{1/24}E(q)$ gives $(p^2-1)/24$, agreeing with Berkovich–Garvan (1.6). Examples are $A_2=1/8$, $A_3=1/3$ and $A_6=5/12$. Fractional shifts are permitted, and this local normalization issue does not change coefficient signs."
    require(source.count(old)==1);source=source.replace(old,new)
    old=source[source.index('Run `python3 verify.py`'):]
    new="The unchanged original `verify.py` and saved `verification.json` are historical finite diagnostics. Original preparation actually replayed them and the old review checker with exact bytes and recursive JSON types/keys/values: 2,837 author assertions and 35,980 historical-review assertions. That replay is not a new independent family. The two fresh families separately report 324,186 algebra assertions and 140,708 geometry assertions; these remain diagnostics, not the infinite proof. Their checkable universal derivations independently expose the core/theta foundation, analytic uniqueness and all-N factorization. All dated original PASS, PDF, model, runtime, pending-review and publication-readiness claims are qualified globally in `GLOBAL_QUALIFICATIONS.json`; literal originals remain under `../original_head_archive`.\n\nOriginal accounting stays one JSON object, zero proof attempts, budget 5, two source-audit events, with no separately supplied source-verification response count. Both source records omit `prior_report`; selected SQL reports contain text `{}` rather than NULL. Duplicate 30000167 shares this result and budget. Its absent native queue row is not invented. No new theorem, paper, DOI or tracker result is recommended.\n"
    source=source[:source.index(old)]+new
    write(F/'current_science/SOURCE_STATUS.md',source.encode())
    write(F/'current_science/README.md',("# PR51: credited known eta-product theorem\n\nThe exact all-positive-integer target and duplicate 30000167 are covered by Berkovich–Garvan (2006/2007 preprints, 2008 publication). Recommended mathematical classification: already_solved, original 0/5. No new theorem or paper is claimed. Read SOURCE_STATUS.md and GLOBAL_QUALIFICATIONS.json together.\n\nAll dated claims in the literal original archive and retained source/ledger/checker/result JSON are historical: old PASS, pending state, PDF hashes/pixels, original model/runtime/search and publication authorization do not become current approval. The operative proof synopsis credits existing mathematics and references two fresh independent reviews, each actually ROOT-closed and separately read back. Those recommendations are not a fresh third verdict by this preparer.\n\nThe 15 original science bodies remain byte exact in ../original_head_archive. The retained plain integer source IDs, omitted prior_report keys and one-object turns ledger are unchanged. Current native rows have not been re-read or written here; original selected observations are historical. Duplicate shares scope and budget and has no supplied queue row. All native/ROOT acceptance/Git/merge/publication authority is false in this packet. No paper, DOI or tracker artifact is supplied.\n").encode())
    write(F/'current_science/PR_DRAFT.md',("# Prepared PR51 description — no new publication\n\nReconcile the exact Möbius–totient eta-product question with Berkovich–Garvan's existing all-positive-integer theorem, preserving attribution, the correct denominator-24 Fourier shift and fractional leading powers. Duplicate 30000167 repeats the same composite-case question and shares original 0/5 accounting.\n\nThe two fresh algebra and analytic geometry families found no mandatory mathematical correction. Their universal proofs and actual finite controls are referenced by exact frozen inputs. Original helper/result/source/ledger bodies and old review receipts remain literal and globally historical; old PDF/model/runtime/PASS/readiness claims supply no current native or merge approval.\n\nThis is a science-only partial candidate. Acceptance operations, native reconciliation and merge are pending the parent workflow. No new paper, DOI, tracker entry or discovery credit is recommended.\n").encode())
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(F/'current_science/RESEARCH_LOG.md',("# Current science preparation history\n\n"+utc+" — 85%: known theorem and original proof mathematics retained, historical source/runtime/PDF/PASS claims qualified globally, and two fresh distinct-family recommendations bound. Original September30 research log is preserved byte exact in ../original_head_archive/RESEARCH_LOG.md. Its pending/publication/model statements are historical. Preparation supplies no new independent mathematical or production verdict.\n").encode())
    wrapper="# Historical independent review reference\n\nThe September30 REVIEW.md is preserved byte exact in ../../original_head_archive/independent_review/REVIEW.md. Its PASS, visual PDF and runtime/model/source-hash claims apply only to that historical review. Its optional author_replay path was not a supplied original branch file and is not fabricated here. The other unchanged old review helper/JSON receipts in this directory are globally historical under ../GLOBAL_QUALIFICATIONS.json.\n\nCurrent mathematical inputs are the separately frozen eta_algebra_adversary_family and modular_geometry_adversary_family proofs/reports/verdicts listed in ../provenance.json and the external binding table. Each concludes the exact known all-N theorem without a mandatory correction. This reference wrapper creates no new review verdict, ROOT acceptance, native authority or publication permission.\n"
    write(F/'current_science/independent_review/REVIEW.md',wrapper.encode())
    historical={'scope':'All original_head_archive bodies and every retained literal source/ledger/helper/result/review JSON in current_science',
                'claim_kinds':['PASS','pending review','publication readiness/authorization','model','runtime','deadline if mentioned','PDF SHA256','visual pixels','source search/status/history'],
                'global_rule':'These are dated historical claims, not freshly revalidated facts or current authority. Source open labels are literal imported triage; old PASS does not authorize current acceptance.',
                'original_prior_report':'ABSENT key and file; no administrative null marker invented',
                'selected_sql_report':'literal text{}; not SQL NULL; original selected observations are dated',
                'ledger':'one object, two source events, zero proof attempts, budget5; no separate source-response count',
                'duplicate':'same exact target, shared budget; absent native queue row not inserted',
                'native_authority':False,'root_acceptance_authority':False,'git_authority':False,
                'merge_authority':False,'publication_authority':False,'new_paper':False,'new_DOI':False}
    jwrite(F/'current_science/GLOBAL_QUALIFICATIONS.json',{'schema':'pr51-current-global-historical-qualifications/v1','observed_utc':utc,**historical})
    jwrite(F/'current_science/provenance.json',{'schema':'pr51-current-science-provenance/v1','prepared_utc':utc,'original_head':HEAD,
            'original_15_science_archive':'../original_head_archive','original_provenance':'../original_head_archive/provenance.json',
            'historical_qualification_index':'GLOBAL_QUALIFICATIONS.json','current_preparer_independent_math_verdict':None,
            'current_model_or_reasoning_setting_not_inferred':None,'current_actual_runtime':'see private builder and readback prelaunch/completed captures',
            'fresh_math_inputs':[{'family':q['name'],'manifest_sha256':q['manifest_sha256'],'closed_and_separately_readback':True} for q in inputs[1:]],
            'external_normalized_rows_reference':'../EXTERNAL_BINDINGS.json',
            'all_native_root_git_merge_publication_authority':False,'project_novelty':False,'new_paper_recommended':False})
    external={'schema':'pr51-current-external-normalized-bindings/v1','observed_utc':utc,'original_head':HEAD,
              'closed_inputs':inputs,'actual_root_capture_references':caps,
              'rows_count':sum(len(q['rows']) for q in inputs+caps),'administrative_capture_bodies_copied':False,
              'foreign_raw_source_bodies_copied':False,'original_first_party_science_bodies_copied':15,
              'qualification':'Body/mode/path rows and actual capture references only. Original science alone is copied as authorized first-party archive; no administrative capture/PDF/cache bodies copied.',
              'future_authority':False}
    jwrite(F/'EXTERNAL_BINDINGS.json',external)
    science=[]
    for folder in ('current_science','original_head_archive'):
        for p in sorted((F/folder).rglob('*')):
            if p.is_file():science.append(row(p,'operative qualification' if folder=='current_science' else 'literal original archive'))
    require(len(science)==31 and len(list((F/'original_head_archive').rglob('*.json')))==8)
    jwrite(F/'CURRENT_SCIENCE_INDEX.json',{'schema':'pr51-current-science-body-index/v1','original_head':HEAD,'science_files_count':31,'rows':science,
            'original_science_files':15,'operative_science_files':16,'original_git_mode':'100644','current_science_storage_mode':'0444',
            'future_authority':False})
    print(json.dumps({'schema':'pr51-current-builder-result/v1','utc':utc,'status':'PASS_SCIENCE_PREPARATION_ONLY',
                     'checks_actual':checks,'science_files':31,'external_rows':external['rows_count'],
                     'closed_external_payloads':[188,23,35],'actual_root_completed_captures':6,
                     'import_compile_execute_production':False,'new_native_root_git_merge_publication_authority':False},indent=2))


if __name__=='__main__':main()
