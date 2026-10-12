"""One authorized tracker append after exact published-payload verification."""
import datetime, hashlib, importlib.util, json, os
from pathlib import Path
from capture import capture
A=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr80_30000177')
R=A.parents[2]
F=Path(__file__).parent
pub=json.loads((A/'ROOT_PUBLICATION_VERIFICATION_20261004.json').read_text())
assert pub['status']=='PUBLISHED_EXACT_METADATA_AND_PUBLIC_PAYLOAD_BYTES_VERIFIED'
assert pub['all8_public_bytes_identical'] and pub['intended_metadata_exact']
spec=importlib.util.spec_from_file_location('tracker',R/'draft_pr_publication_program_20260930/infrastructure/append_publication.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
commands=[]
def captured(gws,parts,params,attempt,name,body=None,dry_run=False):
    argv=[gws,'sheets',*parts,'--params',json.dumps(params)]
    if body is not None: argv+=['--json',json.dumps(body)]
    if dry_run: argv+=['--dry-run']
    result,out,err=capture('tracker_'+name,argv,sources=[str(Path(__file__).resolve()),str(R/'draft_pr_publication_program_20260930/infrastructure/append_publication.py')])
    commands.append(result)
    t.save(attempt/(name+'-command.json'),{'argv':argv,'started_utc':result['start_UTC'],'actual_PID':result['actual_PID']})
    t.save(attempt/(name+'-raw.json'),{'returncode':result['exit_code'],'stdout':out.decode(),'stderr':err.decode()})
    if result['exit_code']: raise t.TrackerError(name+' failed; inspect before retry')
    value=json.loads(out)
    if not isinstance(value,dict): raise t.TrackerError(name+' returned nonobject')
    t.save(attempt/(name+'.json'),value)
    return value
t.run_gws=captured
notes=(
    'Asymptotic LOCC dense coding with the symmetric four-qubit W state; Alec Kriebel (ORCID 0009-0001-9320-500X), v1.0, 2026-10-04. '
    'Original-model symmetric W4: two independent unitary senders each route one qubit to a separate receiver; receiver LOCC with local block decoding achieves sum-rate supremum at least 3/2+h2(1/4)=2.311278124459... bits/copy, including rates (9/8,9/8) with vanishing uniform average error. Original LOCC-DC classification resolved; no optimal-capacity or one-copy claim. '
    'Cao-Song decomposition, Pradhan Bell forwarding, Winter cqMAC theorem and Huang-Zhang-Hou framework credited. Bounded primary-literature priority audit with documented access/version limitations; no categorical worldwide firstness certification. '
    'AI tools used extensively; unrefereed, without conventional human peer review. Two sequential whole-package AI reviews; round1 minor corrections fixed, final corrected package clean. Eight files: PDF, LaTeX, rational verifier, results, priority supplement, README, license and digests. '
    +pub['record_url']+'; PR https://github.com/AlecKriebel/Math/pull/80. Original proof budget1/5; new central proof-search0.'
)
notes_path=F/'TRACKER_NOTES.txt'
notes_path.write_text(notes+'\n')
argv=['--problem-url','https://www.unsolvedmath.com/problems/OWR-785-003','--problem-alias','30000177','--doi',pub['DOI'],'--notes-file',str(notes_path),'--receipt-dir',str(F/'tracker'),'--execute']
assert t.main(argv)==0
attempts=list((F/'tracker').glob('tracker-attempt-*'))
assert len(attempts)==1
attempt=attempts[0]
result=json.loads((attempt/'result.json').read_text())
assert result['state'] in ('appended_verified','verified_existing')
requested=['https://www.unsolvedmath.com/problems/OWR-785-003','','https://doi.org/'+pub['DOI'],notes]
title=json.loads((attempt/'request.json').read_text())['resolved_title']
assert title=='Math Puzzles'
fresh_rows=t.read_table('/Users/alec/.nvm/versions/node/v22.16.0/bin/gws',attempt,title,'table-final')
number=t.range_row(result['range'],title)
assert t.duplicate_row(fresh_rows,{'unsolvedmath:OWR-785-003','unsolvedmath:30000177'},t.normalize_doi(pub['DOI']))==(number,requested)
assert fresh_rows[number-1]==requested
receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'status':'TRACKER_EXACT_FOUR_CELLS_READ_BACK_UNIQUE','spreadsheet_id':t.SPREADSHEET_ID,'sheet_gid':t.SHEET_ID,'range':result['range'],'DOI':pub['DOI'],'four_cells':requested,'append_performed':result['append_performed'],'fresh_full_table_exactly_one_pair':True,'actual_command_count':len(commands),'workflow_percent':90,'program_completed':'9/99','original_budget':'1/5','new_central_proof_search_turns':0}
with (A/'ROOT_TRACKER_VERIFICATION_20261004.json').open('x') as f: f.write(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
