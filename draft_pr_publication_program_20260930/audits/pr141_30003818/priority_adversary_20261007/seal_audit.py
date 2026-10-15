from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess

D=Path(__file__).resolve().parent
A=D.parent
UTC=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(path):
    body=path.read_bytes()
    return {'path':str(path),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'mode':oct(stat.S_IMODE(path.stat().st_mode))}
def write_new(name,data):
    path=D/name
    with path.open('x') as f:json.dump(data,f,indent=2);f.write('\n')

if (D/'FINAL_MANIFEST.json').exists():raise RuntimeError('already sealed; refusing overwrite')
for receipt_name in ('PRIMARY_RETRIEVAL.json','FOLLOWUP_RETRIEVAL.json'):
    receipt=json.loads((D/receipt_name).read_text())
    for row in receipt['sources']:
        if 'sha256' not in row:continue
        path=Path(row['private_path']);actual=digest(path)
        if actual['bytes']!=row['bytes'] or actual['sha256']!=row['sha256']:raise RuntimeError('source hash mismatch: '+str(path))

querylog=json.loads((D/'SEARCH_LOG.json').read_text())
gate=json.loads((A/'ROOT_MATHEMATICAL_GATE.json').read_text())
metadata=json.loads((A/'ORIGINAL_PR_METADATA.json').read_text())
if gate['verdict']!='PASS_COMPLETE_EXPLICIT_TRANSFORM_LAW':raise RuntimeError('wrong mathematical gate')
if metadata['head']['sha']!='523247e3246a5f44c7b0089074bb304c1f642bd0':raise RuntimeError('wrong original PR head')
if metadata['created_at']!='2026-09-30T11:34:25Z':raise RuntimeError('wrong PR chronology')
mathinput=A/'original_submitted_attempt/JOINT_LAW.md'
if digest(mathinput)['sha256']!=gate['mathematical_artifact_sha256']:raise RuntimeError('math source hash mismatch')

sourcepdf=A/'private_sources/owr.pdf'
extractpath=D/'private/owr_printed1452.txt'
if extractpath.exists():raise RuntimeError('refusing source extract overwrite')
proc=subprocess.Popen(['/opt/homebrew/bin/pdftotext','-f','72','-l','72','-layout',str(sourcepdf),str(extractpath)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:out,err=proc.communicate(timeout=20)
except subprocess.TimeoutExpired:
    proc.kill();out,err=proc.communicate();raise RuntimeError('source extraction timed out; killed/reaped')
if proc.returncode:raise RuntimeError('source extraction failed')
source_text=extractpath.read_text()
for marker in ('Voronoi-like decomposition','Agelos Georgakopoulos','probability distribution of the vector'):
    if marker not in source_text:raise RuntimeError('wrong source-page extract')

parent_inputs=[mathinput,A/'original_submitted_attempt/README.md',A/'original_submitted_attempt/RESEARCH_LOG.md',A/'ROOT_MATHEMATICAL_GATE.json',A/'ROOT_EXACT_CLAIM_SOURCE_CHECK.json',A/'ORIGINAL_PR_METADATA.json',sourcepdf]
private_inputs=sorted((D/'private').iterdir())
if any(not p.is_file() for p in private_inputs):raise RuntimeError('unexpected private subdirectory')
write_new('INPUT_MANIFEST.json',{
 'schema':'pr141-independent-priority-input-manifest/v1','actual_reader_PID':os.getpid(),'UTC':UTC(),
 'parent_inputs':[digest(p) for p in parent_inputs],
 'private_source_members':[digest(p) for p in private_inputs],
 'source_page_extract_child':{'PID':proc.pid,'returncode':proc.returncode,'reaped':proc.poll() is not None,'stderr':err.decode('utf-8','replace'),'printed_page':1452,'PDF_page_one_based':72},
 'read_scope':'Public parent inputs hashed in full; original mathematical claim read; problem source printed1452 extracted/read. Literature bodies retrieved in full with relevant statements/sections and references inspected as specified in REPORT. No claim to have inspected every line of every fulltext. Third-party bodies remain private and ignored.',
 'no_parent_input_mutation':True
})
write_new('RESULT.json',{
 'schema':'pr141-independent-bounded-priority-result/v1','actual_finalizer_PID':os.getpid(),'UTC':UTC(),
 'verdict':'NO_PRIOR_COMPLETE_TARGET_RESOLUTION_IDENTIFIED_REQUIRED_ATTRIBUTION_REPAIRS',
 'problem_id':30003818,'PR':141,'original_head':gate['original_head'],'original_created_at':metadata['created_at'],
 'original_math_sha256':digest(mathinput)['sha256'],'literal_status':'claimed_solved','submitted_effort':'1/5','new_central_proof_turns':0,
 'query_inventory_count':len(querylog['queries']),
 'mathematical_gate_input':gate['verdict'],
 'strongest_priority_conclusion':'In the documented bounded primary-source search, no earlier complete finite-k Brownian-circle first-visit volume-vector transform or directly supplying explicit generic theorem was identified.',
 'unread_identified_full_resolution_candidate':None,
 'close_unread_related_sources':['Gomes et al.1996 fulltext: direct PDF HTTP403; publisher indexed abstract identifies two-walker one-point scaling calculation and simulated interfaces.','Lee Dicker2006 fulltext: direct PDF HTTP403; primary index title identifies two-walker d>=3 lattice setting.'],
 'fulltext_limit_assessment':'Neither accessible scope currently identifies a prior full general finite-k target resolution. This does not assert that all fulltext remarks/theorems have been excluded. Reopen priority if a general explicit characterization is located.',
 'registry_gap':'Zenodo API queries HTTP403; indexed no-match is not exhaustive registry clearance.',
 'required_repairs':[
  'Credit first-arrival painting literature including Gomes1996, Miller2013, the2026 cycle interface, real-line competitive-range and strategic-painting results.',
  'Distinguish one-point/correlation/interface/span/payoff/scaling results from the complete finite-k circle volume law.',
  'Credit established interval/strong-Markov/moment/transform methods and avoid claims of their novelty.',
  'Present priority as a dated bounded search conclusion and disclose inaccessible close fulltexts and Zenodo registry limitations.',
  'Avoid first-ever, new-model, absolute priority, independent-discovery or copying assertions.',
  'Use the2018 source-volume date and2019-04-12 publisher date accurately in any chronology.'
 ],
 'recommendation':'Prepare the package after attribution/presentation repairs; fresh whole-package adversarial reviews and root priority gate remain required.',
 'recommend_close_as_already_solved':False,'publication_ready':False,'overall_goal_complete':False,'bounded_audit_percent_complete':100,
 'no_PR_or_remote_or_provider_or_tracker_action':True,
 'no_external_outreach':True,
 'background_root_checks_not_counted_as_this_agent_fulltext_reads':True
})

allowed={'REPORT.md','RESEARCH_LOG.md','SEARCH_LOG.json','INPUT_MANIFEST.json','RESULT.json','PRIMARY_RETRIEVAL.json','FOLLOWUP_RETRIEVAL.json','ZENODO_API_SEARCH_RECEIPT.json','retrieve_primary_sources.py','retrieve_followup_sources.py','seal_audit.py'}
actual={p.name for p in D.iterdir() if p.is_file()}
if actual!=allowed:raise RuntimeError('public member set differs: '+repr(actual^allowed))
for p in private_inputs:p.chmod(0o444)
members=[]
for name in sorted(allowed):
    p=D/name;p.chmod(0o444);members.append(digest(p))
write_new('FINAL_MANIFEST.json',{
 'schema':'pr141-independent-priority-closed-public-manifest/v1','actual_sealer_PID':os.getpid(),'sealed_UTC':UTC(),
 'closed_members':members,'closed_member_count':len(members),'all_closed_members_read_in_full_and_frozen':True,
 'private_third_party_bodies_excluded_from_public_set':True,'private_member_hashes_custodied_in':'INPUT_MANIFEST.json',
 'self_excluded_from_hash_set':True,'all_children_completed_or_reaped':proc.poll() is not None,
 'verdict':'NO_PRIOR_COMPLETE_TARGET_RESOLUTION_IDENTIFIED_REQUIRED_ATTRIBUTION_REPAIRS'
})
(D/'FINAL_MANIFEST.json').chmod(0o444)
print(json.dumps({'PID':os.getpid(),'UTC':UTC(),'manifest':digest(D/'FINAL_MANIFEST.json'),'RESULT':digest(D/'RESULT.json'),'REPORT':digest(D/'REPORT.md'),'members':len(members),'queries':len(querylog['queries']),'all_children_reaped':True},indent=2))
