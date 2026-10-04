"""Read-only GitHub authentication and selected local raw-source provenance."""
import base64, datetime, hashlib, json, pathlib, sqlite3, subprocess
F = pathlib.Path(__file__).resolve().parent
R = F.parents[3]
HEAD = 'd49a1bd56d8cc268159331e5ce868e258a32bb58'
PREFIX = 'unsolved_math_prioritization/attempts/30000671/'
def sha(b): return hashlib.sha256(b).hexdigest()
def write(rel, b):
    p=F/rel; p.parent.mkdir(parents=True, exist_ok=True)
    assert not p.exists(), str(p)
    p.write_bytes(b)
def jwrite(rel,v): write(rel,(json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def call(name, argv):
    d=F/'api_captures'/name; d.mkdir(parents=True,exist_ok=False)
    operator=pathlib.Path(__file__).read_bytes()
    (d/'prelaunch_operator.py').write_bytes(operator)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate(); end=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (d/'stdout.bin').write_bytes(out); (d/'stderr.bin').write_bytes(err)
    (d/'CAPTURE.json').write_text(json.dumps({'schema':'pr53-authentication-capture/v1','pid':p.pid,'argv':argv,'cwd':str(R),'started_at':start,'completed_at':end,'exit_code':p.returncode,'operator_sha256':sha(operator),'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':sha(out)},'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':sha(err)}},indent=2)+'\n')
    assert p.returncode==0,(name,p.returncode)
    return out
def api(name,endpoint): return json.loads(call(name,['gh','api',endpoint]))
def main():
    pr=json.loads(call('pr53_view',['gh','pr','view','53','--repo','AlecKriebel/Math','--json','number,title,body,state,isDraft,headRefName,headRefOid,baseRefName,baseRefOid,files,commits,url']))
    assert pr['headRefOid']==HEAD and pr['isDraft'] and pr['state']=='OPEN'
    jwrite('PR_METADATA.json',pr)
    write('FULL_PR_DIFF.patch',call('pr53_full_diff',['gh','pr','diff','53','--repo','AlecKriebel/Math']))
    commit=api('head_commit','repos/AlecKriebel/Math/git/commits/'+HEAD)
    assert commit['sha']==HEAD
    tree_sha=commit['tree']['sha']; chain=[]
    for part in ['unsolved_math_prioritization','attempts','30000671']:
        tree=api('tree_'+part,'repos/AlecKriebel/Math/git/trees/'+tree_sha)
        assert not tree['truncated'] and tree['sha']==tree_sha
        entry=next(e for e in tree['tree'] if e['path']==part)
        assert entry['type']=='tree'
        chain.append({'parent_tree':tree_sha,'name':part,'child_tree':entry['sha']})
        tree_sha=entry['sha']
    tree=api('target_tree','repos/AlecKriebel/Math/git/trees/'+tree_sha)
    assert tree['sha']==tree_sha and not tree['truncated']
    entries={e['path']:e for e in tree['tree']}
    review=api('review_tree','repos/AlecKriebel/Math/git/trees/'+entries['review']['sha'])
    assert not review['truncated']
    for e in review['tree']: entries['review/'+e['path']]=e
    rows=[]
    for n,f in enumerate(pr['files']):
        path=f['path']
        if path=='unsolved_math_prioritization/QUEUE.md': continue
        assert path.startswith(PREFIX),path
        rel=path[len(PREFIX):]; ent=entries[rel]
        bodyj=api('blob_'+str(n),'repos/AlecKriebel/Math/git/blobs/'+ent['sha'])
        assert bodyj['encoding']=='base64' and bodyj['sha']==ent['sha']
        b=base64.b64decode(bodyj['content'])
        gitsha=hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
        assert gitsha==ent['sha'] and len(b)==ent['size']
        write('original_archive/'+rel,b)
        rows.append({'repo_path':path,'archive_path':'original_archive/'+rel,'bytes':len(b),'sha256':sha(b),'git_blob_sha1':gitsha,'git_mode':ent['mode']})
    assert len(rows)==11
    jwrite('GITHUB_AUTHENTICATION.json',{'head':HEAD,'head_tree':commit['tree']['sha'],'base_ref_oid':pr['baseRefOid'],'tree_chain':chain,'target_tree':tree_sha,'files':rows,'queue_diff_archived_separately':True,'native_or_git_writes':False})
    cache=R/'unsolved_math_prioritization/cache'
    con=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro',uri=True)
    selected=con.execute('SELECT key,payload,report FROM records WHERE json_extract(payload,\'$.id\')=?',(30000671,)).fetchall()
    assert len(selected)==1
    key,payload,report=selected[0]; con.close()
    rec=json.loads(payload)
    archived=json.loads((F/'original_archive/source_record.json').read_text())
    assert rec==archived['record']
    jwrite('SELECTED_SQL_ROW.json',{'key':key,'payload_json':rec,'report_sql_type':'null' if report is None else 'text','report_literal':report})
    raw_reports=json.loads((cache/'research_results.json').read_bytes())
    report_present=rec['problem_number'] in raw_reports
    report_value=raw_reports.get(rec['problem_number'])
    jwrite('RAW_PRIOR_REPORT_JOIN.json',{'code':rec['problem_number'],'raw_research_results_key_present':report_present,'raw_research_results_value':report_value,'sql_report_literal':report,'archived_research_result_for_code':archived['research_result_for_code'],'archived_null_is_not_proof_of_raw_key_presence':True})
    hashes=[]
    for name in ['problems.json','research_results.json','catalog.sqlite']:
        p=cache/name; h=hashlib.sha256()
        with p.open('rb') as inp:
            for block in iter(lambda:inp.read(1024*1024),b''):h.update(block)
        hashes.append({'absolute_path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest(),'copied':False,'claim':'dated local source bytes only'})
    jwrite('RAW_CACHE_HASHES.json',hashes)
    groups=json.loads((R/'unsolved_math_prioritization/review_v2/related_target_groups.json').read_text())
    # Exact ID absence checked against the entire serialized value, not a partial excerpt.
    jwrite('RELATED_GROUP_CHECK.json',{'source_sha256':sha((R/'unsolved_math_prioritization/review_v2/related_target_groups.json').read_bytes()),'numeric_id_occurrences_in_serialization':json.dumps(groups).count('30000671'),'no_alias_asserted_from_absence':True})
    print(json.dumps({'status':'PASS','authenticated_original_changed_files':len(rows),'total_original_bytes':sum(x['bytes'] for x in rows),'raw_report_key_present':report_present,'sql_report_literal':report,'head':HEAD}))
if __name__=='__main__':main()
