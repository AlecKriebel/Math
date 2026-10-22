from pathlib import Path
import ast,copy,json,hashlib,datetime as dt
home=Path(__file__).resolve().parent;bp=home/'bound_ops';source=bp/'repository_integration.py';t=ast.parse(source.read_text());names={'signature','unchanged_parent','assert_scoped_preservation','own_queue_row','verify_integrated_tree'}
blobsha=lambda b:hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
env={'Path':Path,'json':json,'hashlib':hashlib,'PROBLEM':'problems/9700002_congestion_transition','QUEUE':'unsolved_math_prioritization/QUEUE.md','blob_sha':blobsha};exec(compile(ast.Module(body=[x for x in t.body if isinstance(x,ast.FunctionDef) and x.name in names],type_ignores=[]),str(source),'exec'),env)
snapshot=json.loads((home/'extracted/congestion-fragmentation-verification/SOURCE_SNAPSHOT.json').read_text());original={v['repository_path'].split('problems/9700002_congestion_transition/',1)[1]:('100644','blob',v['git_blob']) for v in snapshot['files']};selected={'preprint/'+p.name:p.read_bytes() for p in (home/'bound_release').iterdir()};origqueue=b'other row\n| 9700002 / AMR-096-0002 | queued | 0/5 | fixed |\nend\n';desired=origqueue.replace(b'| queued | 0/5 |',b'| claimed_solved | 2/5 |');head='h';base='b';merged='m';controlrows=[]
def entry(sha,kind='blob'):return {'mode':'040000' if kind=='tree' else '100644','type':kind,'sha':sha}
def fixture():
 leaves={'b':{'previous.txt':('100644','blob','previous')},'m':{'previous.txt':('100644','blob','previous'),**original,**{k:('100644','blob',blobsha(v)) for k,v in selected.items()}}}
 blobs={'b':origqueue,'m':desired,'h':desired}
 sub={('b',''):{'problems':entry('old-problems','tree'),'unsolved_math_prioritization':entry('old-queue','tree'),'other.txt':entry('unchanged')},('m',''):{'problems':entry('new-problems','tree'),'unsolved_math_prioritization':entry('new-queue','tree'),'other.txt':entry('unchanged')},('b','problems'):{'9700002_congestion_transition':entry('old','tree'),'other_problem':entry('unchanged-other','tree')},('m','problems'):{'9700002_congestion_transition':entry('new','tree'),'other_problem':entry('unchanged-other','tree')},('b','unsolved_math_prioritization'):{'QUEUE.md':entry('old'),'other.md':entry('unchanged')},('m','unsolved_math_prioritization'):{'QUEUE.md':entry('new'),'other.md':entry('unchanged')}}
 return leaves,blobs,sub
def run(label,mutation,ok=False):
 leaves,blobs,sub=fixture();mutation(leaves,blobs,sub);env['selection']=lambda:selected;env['originals']=lambda:original;env['leaves']=lambda commit,path:leaves[commit];env['blob']=lambda commit,path:blobs[commit];env['subtree']=lambda commit,path,recursive:sub[(commit,path)];env['api']=lambda path:{'tree':{'sha':'synthetic'}}
 try:env['verify_integrated_tree']('b','m','h')
 except Exception as ex:controlrows.append({'case':label,'actual':'reject','expected':'accept' if ok else 'reject','reason':str(ex)});assert not ok,(label,str(ex))
 else:controlrows.append({'case':label,'actual':'accept','expected':'accept' if ok else 'reject'});assert ok,label
run('exact_five_overlay_preserves_all_originals_unrelated_entries',lambda a,b,c:None,True)
run('main_already_has_exact_target_row',lambda a,b,c:b.update(b=desired),True)
name=next(iter(original))
run('base_original_collision',lambda a,b,c:a['b'].update({name:('100644','blob','changed')}))
run('missing_original_in_merge',lambda a,b,c:a['m'].pop(name))
run('changed_original_in_merge',lambda a,b,c:a['m'].update({name:('100644','blob','changed')}))
run('missing_publication_payload',lambda a,b,c:a['m'].pop('preprint/congestion-fragmentation.pdf'))
run('changed_publication_payload',lambda a,b,c:a['m'].update({'preprint/congestion-fragmentation.pdf':('100644','blob','changed')}))
run('unexpected_problem_payload',lambda a,b,c:a['m'].update({'unexpected.txt':('100644','blob','extra')}))
run('lost_existing_problem_payload',lambda a,b,c:a['m'].pop('previous.txt'))
run('own_queue_other_status',lambda a,b,c:b.update(b=origqueue.replace(b'| queued | 0/5 |',b'| active | 1/5 |')))
run('head_queue_claim_changed',lambda a,b,c:b.update(h=desired.replace(b'| claimed_solved | 2/5 |',b'| claimed_solved | 3/5 |')))
run('other_queue_row_changed',lambda a,b,c:b.update(m=desired.replace(b'other row',b'changed row')))
run('duplicate_own_queue_row',lambda a,b,c:b.update(m=desired+env['own_queue_row'](desired)))
run('unrelated_root_file_changed',lambda a,b,c:c[('m','')].update({'other.txt':entry('changed')}))
run('unrelated_problem_changed',lambda a,b,c:c[('m','problems')].update({'other_problem':entry('changed','tree')}))
run('unrelated_queue_directory_file_changed',lambda a,b,c:c[('m','unsolved_math_prioritization')].update({'other.md':entry('changed')}))
out={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'all_assertions_passed':True,'controls':len(controlrows),'accepted':sum(x['actual']=='accept' for x in controlrows),'rejected':sum(x['actual']=='reject' for x in controlrows),'cases':controlrows,'scope':'Actual production integration verification AST with synthetic trees/blobs and exact original/publication selected identities. No API, branch, index, ref or checkout mutation.'};(home/'INTEGRATION_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
