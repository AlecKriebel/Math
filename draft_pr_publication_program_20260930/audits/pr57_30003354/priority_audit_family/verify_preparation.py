"""Bounded read-only administrative readiness; imports no proposed closure/helper."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent
assert not (F/'SELF_MANIFEST.json').exists()
assert all(not p.is_symlink() for p in [F,*F.parents])
v=json.loads((F/'VERDICT.json').read_text());assert v['status']=='READY_FOR_PRIORITY_ADJUDICATION'
assert v['target_match'] is True and v['checked_exact_prior_resolution_found'] is False
assert v['ROOT_approval_claimed'] is False and v['paper_prepared'] is False
assert v['author_or_proposed_helpers_executed'] is False and v['math_reviewer_credit_transferred'] is False
q=v['report_reference'];b=(F/q['path']).read_bytes();assert (len(b),hashlib.sha256(b).hexdigest())==(q['bytes'],q['sha256'])
assert type(v['subjective_new_geometric_contribution_likelihood_percent']) is int
assert v['source_accounting']['original_budget']=='1/5' and v['source_accounting']['new_substantive_turns']==0
assert len(json.loads((F/'BINDINGS.json').read_text())['rows'])==7
count=0
for z in json.loads((F/'BINDINGS.json').read_text())['rows']:
    p=Path(z['path']);s=p.lstat();b=p.read_bytes();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
    assert (len(b),hashlib.sha256(b).hexdigest(),format(stat.S_IMODE(s.st_mode),'04o'))==(z['bytes'],z['sha256'],z['full_mode']);count+=1
r=json.loads((F/'PRIMARY_READING.json').read_text());assert len(r['read_receipts'])==7
for z in r['read_receipts']:
    assert z['whole_bodies_publicly_retained'] is False
    for k in ('pdf_reference','extracted_text_reference'):
        q=z[k];p=Path(q['path']);s=p.lstat();b=p.read_bytes();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
        assert (len(b),hashlib.sha256(b).hexdigest(),format(stat.S_IMODE(s.st_mode),'04o'))==(q['bytes'],q['sha256'],q['full_mode']);count+=1
for name in ['PRIMARY_FETCH_RECEIPTS.json','ADDITIONAL_PRIMARY_FETCH_RECEIPTS.json','LATEST_PRIMARY_FETCH_RECEIPTS.json']:
    d=json.loads((F/name).read_text());assert type(d['actual_reader_pid']) is int
    for z in d['rows']:assert z['status'] in ['ACCESS_FAILED','DOWNLOADED_COMPLETE_PRIMARY_PDF']
    assert any(z['status']=='DOWNLOADED_COMPLETE_PRIMARY_PDF' for z in d['rows'])
c=json.loads((F/'LATEST_PRIMARY_TEXT_CONVERSION.json').read_text());assert len(c['rows'])==4
assert all(type(z['child_pid']) is int and z['exit_code']==0 and z['complete_stdout_utf8']=='' and z['complete_stderr_utf8']=='' for z in c['rows'])
assert all(p.is_file() and not p.is_symlink() for p in F.iterdir())
print(json.dumps(dict(status='PREPARATION_READBACK_PASS',actual_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),fixed_complete_bodies=count,primary_PDFs=7,proposed_closure_or_math_helpers_imported_compiled_executed=False,ROOT_approval_claimed=False)))
