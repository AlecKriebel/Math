"""Acceptance-bearing final checks; only creates records in this review namespace."""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat, sys, zipfile

R = Path(__file__).resolve().parent
F = R.parent / 'preprint_package_v01'
def now(): return datetime.now(timezone.utc).isoformat()
def pin(p):
    p = Path(p); b = p.read_bytes()
    return {'path':str(p.absolute()), 'resolved_path':str(p.resolve()),
            'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest(),
            'mode':stat.S_IMODE(p.stat().st_mode)}
def check_bytes(p, declared):
    actual = pin(p)
    assert all(actual[k] == declared[k] for k in ('bytes','sha256')), str(p)
    return actual
def write(p, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')

auth = json.loads((R/'AUTHENTICATION.json').read_bytes())
assert auth['status']=='PASS_WHOLE_BYTES_LITERAL23_REAL_ZIP20_METADATA'
check_bytes(F/'FIRST_CANDIDATE_MANIFEST.json', auth['frozen_manifest'])
candidate=[]
for row in auth['literal_public_files']:
    p=Path(row['path']); q=check_bytes(p,row)
    assert p.parent == F or p.parent == F/'controls'
    assert q['mode']==0o444 and not p.is_symlink()
    candidate.append(q)
assert len(candidate)==23
with zipfile.ZipFile(F/'spectral_tensor_verification.zip') as z:
    assert len(z.infolist())==20
    assert {i.filename for i in z.infolist()}=={x['name'] for x in auth['ZIP_members']}
    for row in auth['ZIP_members']:
        b=z.read(row['name'])
        assert len(b)==row['uncompressed_bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
        check_bytes(row['extracted']['path'], row['extracted'])
metadata=json.loads((F/'record_metadata.json').read_bytes())
wrapper=json.loads((F/'zenodo-deposit.json').read_bytes())
assert metadata==wrapper['metadata']
assert wrapper['files']==[{'path':'spectral_tensor_consistency.pdf'}, {'path':'spectral_tensor_verification.zip'}]

evidence=json.loads((R/'EVIDENCE_CROSSCHECK.json').read_bytes())
assert evidence['case_count']==8 and evidence['leaf_counts']=={'float':19,'exact_nonfloat':4077}
assert not evidence['floating_differences']
build_path=F/'BUILD_RECEIPT_02.json'
check_bytes(build_path,evidence['build_receipt_pin'])
build=json.loads(build_path.read_bytes())
check_bytes(F/'spectral_tensor_consistency.tex',build['manuscript'])
check_bytes(F/'spectral_tensor_consistency.pdf',build['exported_pdf'])
assert len(build['page_images'])==8
for expected, visual in zip(build['page_images'],evidence['page_pins']):
    assert expected['path']==visual['path']
    check_bytes(expected['path'],expected)
    check_bytes(visual['path'],visual)
check_bytes(R/'FINAL_PDF_TEXT.txt', evidence['PDF_text_pin'])
assert (R/'FINAL_PDF_TEXT.txt').read_text().count('\f')==8
for row in evidence['source_pins']:
    check_bytes(row['original_extract']['path'],row['original_extract'])
    check_bytes(row['retained_complete_extract']['path'],row['retained_complete_extract'])
    assert row['original_extract']['sha256']==row['retained_complete_extract']['sha256']
    if row['raw_body'] is not None:
        check_bytes(row['raw_body']['path'],row['raw_body'])

process_rows=[]
receipt_paths=sorted((R/'processes').glob('*/execution.json'))+sorted((R/'portable_replay').glob('*/execution.json'))
assert len(receipt_paths)==13
for path in receipt_paths:
    e=json.loads(path.read_bytes())
    pid=e.get('actual_Popen_PID',e.get('actual_child_PID'))
    assert isinstance(pid,int) and pid>0
    argv=e['argv']; assert Path(argv[0]).is_absolute()
    assert Path(e['cwd']).is_dir()
    start=e.get('UTC_started',e.get('started_UTC'))
    end=e.get('UTC_completed',e.get('completed_UTC'))
    assert datetime.fromisoformat(start)<=datetime.fromisoformat(end)
    failed=path.parent.name=='authenticate' and path.parent.parent.name=='processes'
    assert e['exit_code']==(1 if failed else 0)
    for kind in ('stdout','stderr'):
        item=e[kind]; p=Path(item['stored']['path'])
        check_bytes(p,item['stored'])
        body=gzip.decompress(p.read_bytes())
        assert len(body)==item['logical_bytes']
        assert hashlib.sha256(body).hexdigest()==item['logical_sha256']
    for item in e.get('sources',[]):
        q=check_bytes(item['immutable_full_copy']['path'],item['immutable_full_copy'])
        assert q['mode']==0o444
        assert all(q[k]==item['input'][k] for k in ('bytes','sha256'))
    if path.parent.parent.name=='portable_replay':
        check_bytes(e['source']['path'],e['source'])
        check_bytes(e['original_source']['path'],e['original_source'])
        assert e['source']['sha256']==e['original_source']['sha256']
        assert e['runtime']['optimization']==0 and e['runtime']['sympy']=='1.14.0'
    executable=e.get('executable',e.get('runtime',{}).get('executable'))
    assert executable is not None
    check_bytes(executable['path'],executable)
    process_rows.append({'receipt':pin(path),'actual_PID':pid,'argv':argv,'cwd':e['cwd'],
                         'UTC_started':start,'UTC_completed':end,'exit_code':e['exit_code'],
                         'stdout':e['stdout'],'stderr':e['stderr']})
assert sum(row['exit_code']!=0 for row in process_rows)==1

required=['REPORT.md','DERIVATION.md','READ_LEDGER.md','VERDICT.json','RESEARCH_LOG.md']
assert all((R/name).is_file() and (R/name).stat().st_size>1000 for name in required)
verdict=json.loads((R/'VERDICT.json').read_bytes())
assert not verdict['mandatory_unresolved_issues']
assert len(verdict['nonmandatory_suggestions'])==4
assert verdict['publication_clearance'] is False
assert verdict['verification']['actual_control_suites_passed']==8
assert all(not p.is_symlink() for p in R.rglob('*'))
physical_before=R.stat().st_blocks*512+sum(p.stat().st_blocks*512 for p in R.rglob('*'))
assert physical_before<20_000_000

stamp=now()
with (R/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+stamp+' — Captured final closure checker PID'+str(os.getpid())+
              ' reauthenticated all frozen candidate bytes/actual ZIP/extracted files, exact metadata, all eight build02 page pins,17 retained source extracts/raw locators,13 earlier real process receipts and their complete streams, including the genuine failed checker. No new mathematical defect or candidate mutation detected. Completion estimate:100% bounded analytic/package review; final noncircular sealing and permission readback are performed next by the parent launcher. Publication remains ROOT-owned.\n')
report_pins=[pin(R/name) for name in required]
write(R/'EXECUTION_LEDGER.json',{'UTC':stamp,'earlier_real_processes':process_rows,
                                'closing_child_PID':os.getpid(),
                                'closing_receipt_written_after_exit':'processes/closure/execution.json',
                                'limits':'Child PIDs are actual launcher Popen observations. Launcher PIDs are genuine self-reports, not an independent upstream Popen certificate. Historical launch modes are not final frozen modes.'})
write(R/'COVERAGE_PINS.json',{'UTC':stamp,'candidate_files':candidate,
                            'visual_pages':evidence['page_pins'],
                            'primary_source_bodies_and_full_extracts':evidence['source_pins'],
                            'interpretation':'Manual read extent is in READ_LEDGER.md; full-file pins alone do not assert whole-source reading.'})
write(R/'PRESEAL_CHECK.json',{'UTC':stamp,'actual_PID':os.getpid(),'status':'PASS_FINAL_INPUT_STREAM_SOURCE_BUILD_BINDING_AND_REPORT_CHECKS',
                             'argv':sys.argv,'cwd':str(Path.cwd()),'runtime':sys.version,
                             'resolved_interpreter':pin(sys.executable),'reports':report_pins,
                             'candidate_file_count':len(candidate),'earlier_process_receipts':len(process_rows),
                             'failed_receipts_retained':1,'page_count':8,'source_extracts':17,
                             'physical_added_bytes_before_seal':physical_before,
                             'mandatory_unresolved_issues':[],
                             'nonmandatory_suggestion_ids':['C1','C2','C3','C4']})
print(json.dumps({'status':'PASS_FINAL_INPUT_STREAM_SOURCE_BUILD_BINDING_AND_REPORT_CHECKS',
                  'PID':os.getpid(),'candidate_files':len(candidate),'earlier_process_receipts':len(process_rows),
                  'physical_bytes_before_seal':physical_before},indent=2))
