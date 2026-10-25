#!/usr/bin/env python3
"""Build a provenance-bound paper queue, not a proof-validation result."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json

ROOT=Path('/Users/alec/Documents/Math')
HERE=Path(__file__).resolve().parent
OLD=ROOT/'paper_inventory_20261024'
def read(p): return json.loads(p.read_text())
def write(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
sheet_path=HERE.parent/'sources/spreadsheet-initial.json'
grid=read(sheet_path)['values']
rows=[dict(sheet_row=i,values=r) for i,r in enumerate(grid[1:],7)]
current=read(HERE/'zenodo-current-public.json')
fresh={r['id']:r for r in current['records']}
old={r['id']:r for r in read(OLD/'sources/corpus_records.json')['records']}
candidates=read(OLD/'sources/supplemental_candidates.json')['candidates']
adjudication=read(OLD/'sources/work_group_adjudication.json')
mapping={r['candidate_id']:r for r in adjudication['mapping']}
aliases={21699069:21699161,21971507:22013710}
archive_papers={'reversible-mass-action-continuum':21753997,'simultaneous-amplification-below-three-halves':21850042}
primary={rid:r for rid,r in fresh.items() if r['metadata'].get('upload_type')=='publication' and any(f['filename'].lower().endswith('.pdf') for f in r['files'])}
assert len(primary)==203
known_sheet={r['values'][22]:r for r in rows if isinstance(r['values'][22],int)}
errors=[];integrity=[];queue=[];dispositions=[]

def verify_source(s,f=None):
    p=Path(s['pdf_path']); entry={'pdf_path':str(p),'filename':s['filename']}
    if not p.is_file():
        entry['status']='missing_local_file';errors.append(entry);integrity.append(entry);return
    data=p.read_bytes(); md5=hashlib.md5(data).hexdigest(); h=hashlib.sha256(data).hexdigest()
    expected_md5=(f or {}).get('checksum',s.get('md5','')).removeprefix('md5:')
    expected_size=(f or {}).get('filesize',s.get('bytes'))
    ok=md5==expected_md5 and len(data)==expected_size and h==s.get('sha256',h)
    entry.update(status='verified' if ok else 'mismatch',bytes=len(data),md5=md5,sha256=h,expected_md5=expected_md5)
    integrity.append(entry)
    if not ok:errors.append(entry)

for rid,r in sorted(primary.items()):
    if rid in aliases:continue
    m=r['metadata']; oldrow=old.get(rid,{})
    sources=[dict(s) for s in oldrow.get('sources',[])]
    if rid==23624706:
        p=ROOT/'kourovka_descending_20261017/problems/21_131/publication/paper.pdf'
        sources=[{'filename':'paper.pdf','pdf_path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'md5':hashlib.md5(p.read_bytes()).hexdigest(),'status':'checksum_bound_local_release'}]
    assert sources,(rid,'missing sources')
    files={f['filename']:f for f in r['files']}
    for s in sources:
        assert s['filename'] in files
        verify_source(s,files[s['filename']])
        s['zenodo_file_url']=f'https://zenodo.org/records/{rid}/files/{s["filename"]}'
    row=known_sheet.get(rid)
    work_id='Bell-setting-minimum' if rid==21699161 else 'Z-'+r['conceptrecid']
    q={'work_id':work_id,'record_id':rid,'title':m['title'],'sheet_row':row['sheet_row'] if row else None,'inventory_index':row['values'][0] if row else 245,'eligibility':'published_paper_record_with_manuscript','doi':r['doi'],'record_url':f'https://zenodo.org/records/{rid}','publication_date':m['publication_date'],'version':m.get('version') or 'Not supplied in Zenodo metadata','sources':sources,'supporting_files':[f for f in r['files'] if not f['filename'].lower().endswith('.pdf')],'related_record_ids':[a for a,c in aliases.items() if c==rid],'related_sheet_rows':[],'status':'awaiting_deep_review','prior_inventory_assessment_is_not_deep_review':True}
    if rid==23575190:
        q['status']='pilot_live_requires_current_state_reconciliation'
        q['existing_page']='https://aleckriebel.com/research/free-spanning-forest-degree/'
    queue.append(q)

supp_by_sha={c['sha256']:c for c in candidates}
q_by_rid={q['record_id']:q for q in queue}
for row in rows:
    v=row['values'];rid=v[22]
    d={'sheet_row':row['sheet_row'],'inventory_index':v[0],'title':v[1],'existing_record_field':rid,'existing_work_group':v[23]}
    if isinstance(rid,int):
        canonical=aliases.get(rid,rid)
        assert canonical in q_by_rid
        d.update(disposition='superseded_or_presentation_copy' if rid in aliases else 'eligible_canonical',canonical_record_id=canonical,work_id=q_by_rid[canonical]['work_id'])
        if rid in aliases:
            d['reason']=next(x['reason'] for x in adjudication['primary_aliases'] if x['record_id']==rid)
            q_by_rid[canonical]['related_sheet_rows'].append(row['sheet_row'])
        else:d['reason']='Published paper record with checksum-bound manuscript; deep review still required.'
    else:
        assert v[25] in supp_by_sha,(row['sheet_row'],v[1])
        c=supp_by_sha[v[25]]; key=c['candidate_id']; rel=mapping[key]; d['candidate_id']=key
        canonical=rel['canonical_entry_id']
        if isinstance(canonical,str) and canonical.isdigit():canonical=int(canonical)
        if key in archive_papers:
            arid=archive_papers[key];r=fresh[arid];m=r['metadata']
            matches=[x for x in c['archive_matches'] if x['deposit_id']==arid]
            assert matches and c['archive_payload_check']['matches_candidate_sha256']
            match=next((x for x in matches if '/releases/' in x['member']),matches[0])
            p=Path(c['archive_payload_check']['exact_archived_pdf_path'])
            s={'filename':Path(match['member']).name,'pdf_path':str(p),'text_path':c['text_path'],'sha256':c['sha256'],'bytes':c['bytes'],'md5':c['md5'],'archive':match,'integrity_scope':'Public archive member CRC32, size and SHA-256 verified in prior acquisition; local bytes and current advertised archive MD5 rechecked. Whole large archive MD5 not recomputed.'}
            verify_source(s)
            archived_file=next(f for f in r['files'] if f['filename']==match['archive_filename'])
            assert archived_file['checksum']==match['archive_advertised_md5']
            q={'work_id':'named-release:'+key,'record_id':arid,'title':c['title'],'sheet_row':row['sheet_row'],'inventory_index':v[0],'eligibility':'explicit_named_paper_release_with_manuscript_inside_zip','doi':r['doi'],'record_url':f'https://zenodo.org/records/{arid}','publication_date':m['publication_date'],'version':m.get('version') or 'Not supplied','sources':[s],'supporting_files':r['files'],'related_record_ids':[21753527] if arid==21753997 else [],'related_sheet_rows':[],'status':'awaiting_deep_review','prior_inventory_assessment_is_not_deep_review':True,'repository_concept_is_not_work_group':True}
            queue.append(q);q_by_rid[arid]=q
            d.update(disposition='eligible_canonical',canonical_record_id=arid,work_id=q['work_id'],reason='Zenodo record expressly publishes this named paper; archived manuscript identity is verified. Correct incidental archive reference in existing sheet.')
        elif isinstance(canonical,int) and rel['relation']!='rejected_attempted_extension':
            assert canonical in q_by_rid
            d.update(disposition='superseded_or_presentation_copy',canonical_record_id=canonical,work_id=q_by_rid[canonical]['work_id'],reason=rel['reason'])
            q_by_rid[canonical]['related_sheet_rows'].append(row['sheet_row'])
        else:
            reason='No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work.' if c.get('archive_matches') else 'No published Zenodo record or archived manuscript match; repository-only work.'
            if rel['relation']=='rejected_attempted_extension':reason='Rejected attempted extension; no eligible published paper-specific Zenodo manuscript. Preserve earlier defect record; do not treat as the published canonical paper.'
            d.update(disposition='excluded_from_zenodo_paper_goal',reason=reason,archive_record_ids=sorted({x['deposit_id'] for x in c.get('archive_matches',[])}),sha256=c['sha256'])
            d['evidence_file']='paper_inventory_20261024/sources/supplemental_candidates.json'
        d['previous_semantic_relation']=rel['relation']
    dispositions.append(d)

queue.sort(key=lambda q:(q['sheet_row'] is None,q['sheet_row'] or 10**6))
named_release_links={
    21699181:21699161,21699205:21699161,21699224:21699161,
    21753405:22089748,21753527:21753997,21753997:21753997,
    21850042:21850042,21852072:22089807,
    21940945:22089373,21944479:22089373,21974911:22089373,21985363:22089373,21989619:22089373,22064121:22089373,
    22032277:22729355,22039095:22729355,22050742:22729355,22058969:22729355,22062080:22729355,22074358:22729355,22478273:22729355,22559244:22729355,22625980:22729355,
}
record_dispositions=[]
for rid,r in sorted(fresh.items()):
    canonical=aliases.get(rid,rid) if rid in primary else named_release_links.get(rid)
    assert canonical in q_by_rid,(rid,'unaccounted published record')
    role='canonical_direct_paper' if rid in primary and rid==canonical else 'paper_edition_or_presentation' if rid in primary else 'canonical_named_paper_zip' if rid==canonical else 'related_named_release_or_support_record'
    record_dispositions.append({'record_id':rid,'title':r['metadata']['title'],'role':role,'canonical_record_id':canonical,'work_id':q_by_rid[canonical]['work_id']})
    if rid!=canonical and rid not in q_by_rid[canonical]['related_record_ids']:q_by_rid[canonical]['related_record_ids'].append(rid)
for q in queue:
    q['related_record_ids'].sort()
    dates=[{'record_id':rid,'date':fresh[rid]['metadata']['publication_date']} for rid in [q['record_id']]+q['related_record_ids']]
    q['earliest_related_named_zenodo_release']=min(dates,key=lambda x:(x['date'],x['record_id']))
    q['publication_date_scope']='The publication_date field is the selected reviewed edition date. Earlier named release history is recorded separately; do not invent or backdate publication.'
summary={'eligible_distinct_works':len(queue),'existing_sheet_rows':len(rows),'existing_eligible_canonical_rows':sum(d['disposition']=='eligible_canonical' for d in dispositions),'existing_superseded_or_presentation_rows':sum(d['disposition']=='superseded_or_presentation_copy' for d in dispositions),'existing_excluded_rows':sum(d['disposition']=='excluded_from_zenodo_paper_goal' for d in dispositions),'new_eligible_records_absent_from_sheet':[q['record_id'] for q in queue if q['sheet_row'] is None],'published_owned_records':len(fresh),'unpublished_drafts_omitted':current['unpublished_entries_omitted'],'local_source_integrity_checks':len(integrity),'local_source_integrity_errors':len(errors)}
assert len(queue)==203 and len({q['work_id'] for q in queue})==203
assert not errors,errors
assert len(dispositions)==244
result={'generated_utc':datetime.now(timezone.utc).isoformat(),'scope':'Distinct expressly published Zenodo papers, including named paper releases whose manuscript is inside the archived ZIP; excluding incidental manuscripts in unrelated repository release archives.','summary':summary,'spreadsheet_snapshot_sha256':sha(sheet_path),'zenodo_snapshot_sha256':sha(HERE/'zenodo-current-public.json'),'queue':queue,'sheet_dispositions':dispositions,'published_record_dispositions':record_dispositions,'source_integrity':integrity,'important_limits':['Eligibility is not correctness, novelty, peer review, or readiness for website publication.','Fresh author identity queries exactly cover the owned published account. They do not establish historical priority.','Repository-wide concept 21753404 groups unrelated releases and must never be used to merge scientific works.']}
write('queue.json',result)

updates=[]
for rid in archive_papers.values():
    q=q_by_rid[rid];row=next(r for r in rows if r['sheet_row']==q['sheet_row']);s=q['sources'][0];m=s['archive']
    updates.extend([{'range':f"'Full List'!L{q['sheet_row']}:Q{q['sheet_row']}",'values':[['https://doi.org/'+q['doi'],q['record_url'],q['publication_date'],q['version'],'Named paper release on Zenodo; manuscript inside source archive','Paper-specific version record; repository concept DOI 21753404 also groups unrelated releases. Original inventory used incidental archive 22625980.']]},{'range':f"'Full List'!V{q['sheet_row']}:X{q['sheet_row']}",'values':[[m['archive_filename']+' :: '+m['member'],rid,q['work_id']]]}])
q=q_by_rid[23624706];m=fresh[q['record_id']]['metadata']
new=['']*26
for col,value in {0:245,1:q['title'],11:'https://doi.org/'+q['doi'],12:q['record_url'],13:q['publication_date'],14:q['version'],15:'Latest standalone Zenodo manuscript',17:'Kriebel, Alec',18:'Not yet assessed under the website review protocol; local published manuscript size, MD5 and SHA-256 match the fresh Zenodo file inventory.',20:'Deep review required.',21:'paper.pdf',22:q['record_id'],23:q['work_id'],25:'paper.pdf: '+q['sources'][0]['sha256']}.items():new[col]=value
assert len(new)==26
write('spreadsheet-proposals.json',{'note':'Proposed exact edits only; this agent did not mutate the spreadsheet. Existing scores and assessment prose are preserved. New-row reviewed-version field remains empty until review.','corrections':updates,'append':{'range':"'Full List'!A251:AD251",'values':[new+['','Queued — eligible Zenodo paper','','New published record found during account reconciliation; deep review pending.']]},'source_metadata':{'23624706':m},'disposition_column_suggestions':[{'sheet_row':d['sheet_row'],'status':'Excluded — no eligible Zenodo paper' if d['disposition']=='excluded_from_zenodo_paper_goal' else 'Superseded — use canonical work','note':d['reason']+(' Canonical Zenodo record: '+str(d['canonical_record_id'])+'.' if 'canonical_record_id' in d else '')} for d in dispositions if d['disposition']!='eligible_canonical']})
print(json.dumps(summary,indent=2))
