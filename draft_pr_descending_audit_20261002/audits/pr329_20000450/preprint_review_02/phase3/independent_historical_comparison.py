#!/usr/bin/env python3
"""Reconstruct bounded semantic, serialization, archive-metadata and snapshot checks."""
from pathlib import Path
import hashlib,json,re,stat
N=Path(__file__).resolve().parent;A=N.parent.parent
E=A/'priority_audit/stage3_current_priority/private_evidence';sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((E/n/'source.bytes').read_bytes())
report=load('upstream_research_results')['AIM-ALGEBRAIC_NUMBER_THEORY-0102']
problem=next(x for x in load('upstream_problems') if x.get('id')==20000450)
current_report=json.loads((A/'root_sources_private/imported_record/prior_report.json').read_bytes())
current_problem=json.loads((A/'root_sources_private/imported_record/source_payload.json').read_bytes())
assert report==current_report and problem==current_problem
legacy=(json.dumps(report,indent=2,ensure_ascii=True)+'\n').encode()
assert len(legacy)==26340 and sha(legacy)=='56ce26a89b743cdf34807407c9e392dd1738b92c1982c661132ab159172eb93a'
snap=json.loads((N/'snapshot_manifest.json').read_bytes());snap_results=[]
for row in snap['files']:
    p=A/'snapshot'/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes'] and sha(b)==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha']
    assert stat.S_IMODE(p.stat().st_mode)==0o644
    snap_results.append({'path':row['path'],'body_and_git_blob_and_mode_match':True})
assert len(snap_results)==22
names={'turn1':'TURN_1.md','final_result':'FINAL_RESULT.md','source_theory':'SOURCE_THEORY.md','verify':'verify_turn1.py'}
for version in ['first','head']:
    for tag,name in names.items():
        assert (E/('gh329_'+version+'_'+tag)/'source.bytes').read_bytes()==(A/'snapshot/unsolved_math_prioritization/attempts/20000450'/name).read_bytes()
releases=load('github_releases');assert len(releases)==28 and load('github_releases_page2')==[]
pattern=re.compile(r'20000450|pentagon|qptsurface2|torsion',re.I)
release_hits=[]
for row in releases:
    text=' '.join([row.get('name',''),row.get('body',''),*[x.get('name','') for x in row.get('assets',[])]])
    if pattern.search(text):release_hits.append(row['id'])
versions=load('zenodo_repo_versions')['hits']['hits'];assert len(versions)==19
titles1=load('zenodo_pentagonal_torsion')['hits']['hits'];titles2=load('zenodo_pentagonal_torsion_page2')['hits']['hits']
assert len(titles1)==25 and len(titles2)==7
exact=load('zenodo_exact_target')['hits']['hits'];assert len(exact)==1 and exact[0]['id']==20000450
commits=load('github_pr329_commits');assert len(commits)==2
out={'status':'PASS','semantic_equalities':{'pinned_selected_report':True,'pinned_selected_problem':True},
     'legacy_report_reconstructed_bytes':len(legacy),'legacy_report_reconstructed_sha256':sha(legacy),
     'reconstruction_boundary':'Computed serialization from pinned current upstream semantics, not a historical native retrieval; the separate 6071-byte old problem-wrapper serialization remains unestablished.',
     'snapshot_file_checks':snap_results,'eight_public_scientific_commit_bodies_match_snapshot':True,
     'github_release_metadata_count':28,'github_release_second_page_empty':True,'release_metadata_pattern_hits':release_hits,
     'known_repository_zenodo_version_count':19,'latest_known_version_created':max(x['created'] for x in versions),
     'broad_zenodo_metadata_titles':[{'id':x['id'],'title':x['metadata']['title']} for x in titles1+titles2],
     'exact_numeric_zenodo_hit':{'id':exact[0]['id'],'title':exact[0]['metadata']['title']},
     'commit_metadata':[{'sha':x['sha'],'author_date':x['commit']['author']['date'],'committer_date':x['commit']['committer']['date']} for x in commits],
     'firstness_or_current_openness_certified':False,'deposited_archive_contents_inspected':False,
     'no_outside_communication':True}
(N/'HISTORICAL_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
