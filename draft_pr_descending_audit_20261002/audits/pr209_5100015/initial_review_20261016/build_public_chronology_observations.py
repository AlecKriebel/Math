"""Extract bounded chronology evidence from actual preserved read-only responses."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json

D=Path(__file__).resolve().parent
F=D/'priority_public_chronology_01'
T=F/'private_transport'
OUT=F/'PUBLIC_CHRONOLOGY_OBSERVATIONS.json'
assert not OUT.exists()
rows={}
captures=[]
for p in sorted(T.glob('*.json')):
    data=p.read_bytes()
    o=json.loads(data)
    rows[o['store_key']]=o.get('object') or (json.loads(o['raw']) if o.get('exit_code',0)==0 else None)
    captures.append(dict(path=p.relative_to(F).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),private_raw_capture=True))
pr=rows['pr209_native_chronology_0']
assert pr['number']==209 and pr['created_at']==pr['updated_at']=='2026-10-01T05:48:56Z'
assert pr['head']['sha']=='fd09a95b479f376234835a4494693bb1316c85ec' and pr['draft'] and pr['state']=='open'
commits=rows['pr209_native_chronology_1']
assert len(commits)==pr['commits']==3
proof=rows['pr209_priority_provider_2']
raw=base64.b64decode(proof['content'])
assert proof['sha']=='8978f21f924d1445d1173ba75cd275ce1da4091c'
assert raw==(D/'submitted/unsolved_math_prioritization/attempts/5100015/PROOF.md').read_bytes()
assert rows['pr209_native_chronology_extra_2'] is None

def suites(obj):
    assert obj['total_count']==len(obj['check_suites'])==2
    return [dict(id=x['id'],created_at=x['created_at'],updated_at=x['updated_at'],head_sha=x['head_sha'],head_tree=x['head_commit']['tree_id'],URL=x['url'],current_repository_public=not x['repository']['private']) for x in obj['check_suites']]

versions=[]
for key in ['pr209_priority_provider_1','pr209_priority_provider_0']:
    o=rows[key]
    versions.append(dict(record_id=o['id'],DOI=o['doi'],conceptDOI=o['conceptdoi'],provider_created=o['created'],provider_modified=o['modified'],author_publication_date=o['metadata']['publication_date'],version=o['metadata']['version'],title=o['metadata']['title'],files=[dict(key=x['key'],bytes=x['size'],provider_checksum=x['checksum'],url=x['links']['self']) for x in o['files']],source_api=o['links']['self']))
result=dict(utc=datetime.now(timezone.utc).isoformat(),PR=209,PR_URL=pr['html_url'],server_PR_created_at=pr['created_at'],server_PR_updated_at=pr['updated_at'],current_PR_head=pr['head']['sha'],current_PR_body_explicitly_links_exact_proof_sha256='4f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2' in pr['body'],current_commit_membership=[dict(sha=x['sha'],url=x['html_url'],author_date=x['commit']['author']['date'],committer_date=x['commit']['committer']['date'],message=x['commit']['message'],dates_are_author_controlled=True) for x in commits],actual_full_PROOF_at_candidate_commit=dict(commit='ffe123ee3b525fd4f6c11c2f9eac89b8f3cea6fe',bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),native_blob=proof['sha'],actual_body_identical_to_frozen_proof=True),candidate_commit_server_check_suites=suites(rows['pr209_priority_provider_3']),final_head_server_check_suites=suites(rows['pr209_native_chronology_extra_1']),earlier_WIP_ed599_PROOF_path_HTTP404=True,earlier_WIP_is_not_claimed_as_a_full_PROOF_file_witness=True,comparison_Zenodo_provider_records=versions,raw_capture_pins=captures,limits=['Git author and committer dates are author controlled.','Check-suite creation times authenticate server receipt of an exact Git tree, not by themselves historical public repository visibility.','Current PR created_at=updated_at and exact proof link support the original PR evidence but do not independently exhaust all visibility/history questions.','Zenodo server creation times are stronger than author-set day-only publication dates, but do not exclude an earlier website version.','Current exact-covering source text must be checked in full and all earlier relevant versions investigated before a priority classification.','No absolute-first or already-solved verdict is issued by this chronology-only receipt.'],no_outreach=True,no_remote_mutations=True)
OUT.write_text(json.dumps(result,indent=2)+'\n')
(F/'RESEARCH_LOG.md').write_text('# Public chronology research log\n\n'+result['utc']+' — 60% of assigned chronology inquiry: actual9capture hashes retained, exact frozen full proof body read at candidate commit, server check times05:35:19Z and original PR existence05:48:56Z onOct1 authenticated. Comparison Zenodo versions1.0/1.1 created16:56:14Z/18:12:36Z same day. Historical public visibility/earlier website timing and exact source coverage not certified; no priority verdict.\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['raw_capture_pins','current_commit_membership','comparison_Zenodo_provider_records']},indent=2))
