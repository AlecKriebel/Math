"""Final metadata/custody seal; no network, corpus search, Git or native run."""
from pathlib import Path
import datetime, hashlib, json, os, stat

R=Path(__file__).resolve().parent
M=R.parents[2]

def pin(p):
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode): raise ValueError('Not regular: '+str(p))
    b=p.read_bytes()
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'mode':oct(stat.S_IMODE(s.st_mode))}

def git(kind,b):
    return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()

def connector(name):
    o=json.loads((R/name).read_text())
    assert o['isError'] is False
    return json.loads(o['structuredContent']['content'])

def write(name,obj):
    with (R/name).open('x') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n')

def main():
    terminals=['OWNED_MANIFEST.json','FINAL.json']
    assert all(not (R/n).exists() for n in terminals+['READING_AND_CUSTODY.json'])
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=json.loads((R/'SEARCH.stdout.json').read_text())
    assert (R/'SEARCH.exit').read_text()=='0\n' and pin(R/'SEARCH.stderr')['bytes']==0
    current=connector('FINAL_REMOTE_REF.connector.json')
    commit=connector('FINAL_REMOTE_COMMIT.connector.json')
    root=connector('FINAL_ROOT_TREE.connector.json')
    assert current['object']['sha']==commit['sha']
    assert commit['tree']['sha']==root['sha'] and root['truncated'] is False
    entries=sorted(root['tree'],key=lambda e:e['path'].encode()+(b'/' if e['type']=='tree' else b'\0'))
    b=b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in entries)
    assert git('tree',b)==root['sha']
    assert next(e for e in entries if e['path']=='docs')['sha']==result['docs_tree']=='e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'
    body_read=[]
    for path in ['docs/papers/wreath-monodromy/index.html','docs/papers/kourovka-16-45/index.html','docs/papers/kourovka-16-63/index.html']:
        row=next(x for x in result['rows'] if x['path']==path)
        p=M/path; actual=pin(p); data=p.read_bytes()
        assert actual['bytes']==row['bytes'] and actual['SHA256']==row['SHA256'] and git('blob',data)==row['Git_blob']
        body_read.append({'path':str(p),**actual,'Git_blob':row['Git_blob'],'extent':'Whole actual body personally read in b0cd5c; identity assessment only, no scientific verdict.'})
    write('READING_AND_CUSTODY.json',{'UTC':now,'opening_main':result['remote_main'],'opening_root_tree':result['root_tree'],
        'pre_checkpoint_closing_ref':connector('CLOSE_REMOTE_REF.connector.json')['object']['sha'],
        'final_main':commit['sha'],'final_root_tree':root['sha'],'docs_tree':result['docs_tree'],'current_root_reconstructed':True,
        'whole_current_docs_authentication':{'HTML_files':47,'HTML_bytes':612221,'metadata_rows':304,'blob_rows':254,'directory_rows':50,'docs_tree_objects':51},
        'search_source':{'path':'search_current.py',**pin(R/'search_current.py'),'whole_actual_read_before_only_run':'d574df'},
        'prior_algorithm_reference_only':{'path':str(R.parents[1]/'verification/low-exponent-su5-legacy-sol-20261116/search_current.py'),
            **pin(R.parents[1]/'verification/low-exponent-su5-legacy-sol-20261116/search_current.py'),'whole_read_tool':'544459','executed':False},
        'personally_whole_read_HTML':body_read,'metadata_title_H1_and_context_inspection_tool':'b0c694',
        'all47_whole_bodies_machine_read_authenticated_searched':True,'all47_bodies_personally_human_read_claim':False,
        'native_identity_pins':[t['native_record_pin'] for t in result['targets']],
        'semantic_same_work_matches':{'23203143':[],'23205181':[],'23331540':[]},
        'weak_or_lexical_hits_retained_in_literal_output':True,'search_execution_history':[0],
        'stdout':pin(R/'SEARCH.stdout.json'),'stderr':pin(R/'SEARCH.stderr'),'native_or_old_helper_or_Git_execution':False,
        'GitHub_connector_transport_status_headers_exposed':False,'new_HTML_PDF_ZIP_bodies_fetched':0,
        'redirect_or_publication_authority':False,'follow_up':None})
    files=[]; dirs=[]
    for base,names,leaves in os.walk(R,followlinks=False):
        for name in names:
            p=Path(base)/name; assert not p.is_symlink()
            dirs.append({'path':p.relative_to(R).as_posix(),'mode':oct(stat.S_IMODE(p.stat().st_mode))})
        for name in leaves:
            p=Path(base)/name; files.append({'path':p.relative_to(R).as_posix(),**pin(p)})
    files.sort(key=lambda x:x['path']); dirs.sort(key=lambda x:x['path'])
    assert not any(x['path'] in terminals for x in files)
    write('OWNED_MANIFEST.json',{'UTC':now,'files':files,'directories':dirs,'root_mode':oct(stat.S_IMODE(R.stat().st_mode)),
        'exact_terminal_controls':terminals,'regular_files_including_terminals':len(files)+2,'child_directories':len(dirs),
        'all_ignored_and_empty_files_included':True,'future_exclusions':[]})
    final={'UTC':now,'status':'BOUNDED_CURRENT_DOCS_CORRESPONDENCE_COMPLETE_NO_GENUINE_MATCH',
        'records':['23203143','23205181','23331540'],'same_work_article_matches':{'23203143':[],'23205181':[],'23331540':[]},
        'opening_main':result['remote_main'],'opening_root_tree':result['root_tree'],'final_main':commit['sha'],'final_root_tree':root['sha'],
        'docs_tree':result['docs_tree'],'HTML_files':47,'HTML_bytes':612221,'metadata_entries':304,
        'search_execution_history':[0],'search_stderr_bytes':0,'full_personally_read_identity_article_and_moved_pages':3,
        'report':{'path':'REPORT.md',**pin(R/'REPORT.md')},'manifest':{'path':'OWNED_MANIFEST.json',**pin(R/'OWNED_MANIFEST.json')},
        'search_result':{'path':'SEARCH.stdout.json',**pin(R/'SEARCH.stdout.json')},
        'extent':{'regular_files':len(files)+2,'child_directories':len(dirs),'exact_terminal_names':terminals},
        'no_history_global_absence_priority_traffic_or_science_verdict':True,'redirect_payload':None,'redirect_authority':False,
        'Git_W_Sheet_source_old_packet_deploy_contact_or_outreach_mutation':False,'native_or_old_helper_execution':False,
        'follow_up':None,'completion_percent':100,'running_handles':[],'quiescent_after_seal':True}
    write('FINAL.json',final)
    print(json.dumps({'extent':final['extent'],'FINAL':pin(R/'FINAL.json'),'manifest':pin(R/'OWNED_MANIFEST.json'),'report':pin(R/'REPORT.md')}))

if __name__=='__main__': main()
