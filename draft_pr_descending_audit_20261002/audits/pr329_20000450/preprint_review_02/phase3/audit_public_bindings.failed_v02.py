#!/usr/bin/env python3
"""Bind formal bytes, disclosed public exports, and historical source receipts."""
from pathlib import Path
import hashlib,json,difflib,subprocess,stat
N=Path(__file__).resolve().parent;A=N.parent.parent;P=N/'archive_replay'
PUBLIC=Path('/Users/alec/Documents/Math/problems/20000450_pentagonal_torsion/preprint')
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
bindings=[]
for name in ['manuscript.tex','manuscript.pdf','zenodo-deposit.json','verification.zip','snapshot_manifest.json','ROOT_CURRENT_MATHEMATICAL_GATE.json','ROOT_PRIORITY_CLOSURE.json','source_pdf_binding.json']:
    own=(N.parent/'phase2'/name) if name in ['manuscript.tex','manuscript.pdf','zenodo-deposit.json'] else N/name
    active=A/'preprint/qualification_v03/inputs'/name
    assert own.read_bytes()==active.read_bytes(),name
    assert stat.S_IMODE(own.stat().st_mode)==stat.S_IMODE(active.stat().st_mode)
    bindings.append({'input':name,'own':pin(own),'active':pin(active)})
for archive_name,public_name in [('manuscript.tex','pentagonal-torsion-note.tex'),('manuscript.pdf','pentagonal-torsion-note.pdf'),('zenodo-deposit.json','zenodo-deposit.json')]:
    assert (P/archive_name).read_bytes()==(PUBLIC/public_name).read_bytes()==(N.parent/'phase2'/archive_name).read_bytes()
    bindings.append({'archive':pin(P/archive_name),'public':pin(PUBLIC/public_name)})
assert (N/'verification.zip').read_bytes()==(PUBLIC/'pentagonal-torsion-verification.zip').read_bytes()
bindings.append({'public_zip':pin(PUBLIC/'pentagonal-torsion-verification.zip')})
source_binding=json.loads((N/'source_pdf_binding.json').read_bytes())
assert source_binding['source_before']==source_binding['source_after']=={k:pin(P/'manuscript.tex')[k] for k in ['bytes','sha256']}
assert source_binding['pdf']=={k:pin(P/'manuscript.pdf')[k] for k in ['bytes','sha256']}
meta=json.loads((P/'zenodo-deposit.json').read_bytes())
assert [x['path'] for x in meta['files']]==['pentagonal-torsion-note.pdf','pentagonal-torsion-verification.zip']
assert all((PUBLIC/x['path']).is_file() for x in meta['files'])
guard='#!/usr/bin/env python3\n# Public export: optimization must not disable scientific assertions.\nimport sys\nif sys.flags.optimize:\n    raise SystemExit("Verification refuses Python optimization (-O/-OO).")\n'
portable=json.loads((P/'PORTABILITY.json').read_bytes());exports=[]
for name,r in portable['programs'].items():
    original=A/r['original_path'];export=P/'programs'/(name+'.py')
    ob=original.read_bytes();eb=export.read_bytes()
    assert len(ob)==r['original_bytes'] and sha(ob)==r['original_sha256']
    assert sha(eb)==r['exported_sha256']
    transformed=ob.decode()
    if transformed.startswith('#!/usr/bin/env python3\n'):
        transformed=transformed[len('#!/usr/bin/env python3\n'):]
    if name=='division_quintic':
        old="(Path(__file__).parent/'native/independent_generic_chord_final.stdout')"
        new="(Path(__file__).parent.parent/'expected/division_chord.json')"
        assert transformed.count(old)==1;transformed=transformed.replace(old,new)
    if name=='geometry_primitivity':
        old='print("python",sys.version.split()[0],"sympy",S.__version__,flush=True)'
        new='print("sympy",S.__version__,flush=True)'
        assert transformed.count(old)==1;transformed=transformed.replace(old,new)
    assert eb.decode()==guard+transformed,name
    exports.append({'name':name,'original':pin(original),'export':pin(export),
                    'exact_declared_transformation_equal':True,
                    'diff':''.join(difflib.unified_diff(ob.decode().splitlines(True),eb.decode().splitlines(True)))})
S=P/'priority_evidence';hist=A/'priority_audit/stage3_current_priority';evidence=hist/'private_evidence'
src=json.loads((S/'SOURCE_INVENTORY.json').read_bytes());reading=json.loads((S/'READING_LEDGER.json').read_bytes())
assert src['source_count']==len(src['sources'])==50
assert len(reading['entries'])==50
byid={x['id']:x for x in reading['entries']};source_checks=[]
for x in src['sources']:
    for key in ['source_sha256','actual_pdf_page_count','read_scope','operative_role_or_limit']:
        assert x[key]==byid[x['id']][key]
    if x['id']=='original_aim_pdf_source_stage':
        base=A/'priority_audit/private_source_evidence'
        rp=base/'official_current.retrieval_receipt.json';op=base/'official_current.http_stdout';ep=base/'official_current.http_stderr';body=base/'official_current.pdf'
    else:
        base=evidence/x['id'];rp=base/'retrieval.receipt.json';op=base/'retrieval.stdout';ep=base/'retrieval.stderr';body=base/'source.bytes'
    rec=json.loads(rp.read_bytes());out=op.read_bytes();err=ep.read_bytes()
    assert x['canonical_url']==rec['argv'][-1]
    assert x['retrieval_started_utc']==rec['started_utc'] and x['retrieval_finished_utc']==rec['finished_utc']
    assert x['actual_native_exit_code']==rec.get('actual_exit_code',rec.get('exit_code'))
    assert sha(out)==rec['stdout_sha256'] and sha(err)==rec['stderr_sha256']
    curl=json.loads(out);assert x['actual_http_status_from_curl']==curl['http_code']
    if x['source_sha256'] is not None:
        assert len(body.read_bytes())==x['retrieved_source_bytes'] and sha(body.read_bytes())==x['source_sha256']
    if x['actual_pdf_page_count'] is not None:
        info=(base/'pdfinfo.stdout').read_text();assert 'Pages:' in info
        pages=int(next(z.split(':')[1] for z in info.splitlines() if z.startswith('Pages:')))
        assert pages==x['actual_pdf_page_count']
    source_checks.append({'id':x['id'],'receipt':pin(rp),'stdout':pin(op),'stderr':pin(ep),
                          'source':pin(body) if x['source_sha256'] is not None else None,
                          'body_argv_clocks_exit_http_pages_match':True,
                          'reading_not_independently_witnessed':True})
search=json.loads((S/'SEARCH_INVENTORY.json').read_bytes())
queries=[q for row in search['web_searches'] for q in row['query_text_from_retrospective_working_record']]
assert len(queries)==search['query_count']==35
assert len(search['web_searches'])==9
summary={'status':'PASS','formal_input_bindings':bindings,'public_export_bindings':exports,
         'historical_source_receipt_bindings':source_checks,'public_source_count':50,'retrospective_query_count':35,
         'historical_reading_boundary':'Native retrieval/render evidence and agent declared reading scopes are distinct. This mechanical comparison does not independently witness past reading, certify first publication, or prove current openness.',
         'publication_approval':False,'candidate_changed':False}
(N/'PUBLIC_BINDING_AUDIT.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['formal_input_bindings','public_export_bindings','historical_source_receipt_bindings']},indent=2))
