from pathlib import Path
import copy,datetime,hashlib,importlib.util,json
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reusable_probes',H/'independent_workflow_probes.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root,p,u,g=m.updater_fixture('whole_main_gate_mutations');original={x:x.read_bytes() for x in p.rglob('*') if x.is_file()};results=[]
def restore():
 for x,b in original.items():x.write_bytes(b)
def mutatejson(name,fn):
 q=p/name;v=json.loads(q.read_text());fn(v);m.save(q,v)
def run(name,change,expected=None):
 restore();change();before=(g.created,g.pushes,g.edits);reason=m.reject(lambda:m.silent(u.main),expected);assert (g.created,g.pushes,g.edits)==before;results.append({'name':name,'refused_before_Git_object_or_external_mutation':True,'reason':reason})
for n in sorted(u.REQUIRED_WORKFLOW):run('actual_script_digest_'+n,lambda n=n:(p/n).write_bytes((p/n).read_bytes()+b'\n# changed after review\n'),'workflow drift')
for key,value in [('id',322),('doi','10.5281/zenodo.322'),('metadata_manifest_sha256','0'*64),('metadata_fields_verified',['title']),('files',[])]:run('public_receipt_'+key,lambda key=key,value=value:mutatejson('PUBLIC_DOWNLOAD_VERIFICATION.json',lambda x:x.__setitem__(key,value)))
for cell in range(4):run('tracker_cell_'+str(cell),lambda cell=cell:mutatejson('tracker/TRACKER_RECEIPT.json',lambda x:x['row'].__setitem__(cell,'altered')),'Full four-cell')
for key,value in [('gid',1),('spreadsheetId','wrong'),('updatedRange',"'Math Puzzles'!A2:D3"),('readback_verified',False)]:run('tracker_'+key,lambda key=key,value=value:mutatejson('tracker/TRACKER_RECEIPT.json',lambda x:x.__setitem__(key,value)))
run('current_edition_changed_after_review',lambda:(root/'current_edition/PROOF.md').write_bytes((root/'current_edition/PROOF.md').read_bytes()+b'\nchanged'),'differs from reviewed archive')
# This one path is outside the copied publication baseline, so restore it explicitly.
(root/'current_edition/PROOF.md').write_bytes((m.SOURCE/'current_edition/PROOF.md').read_bytes())
run('original_snapshot_drift',lambda:(root/'SUBMITTED_SNAPSHOT.json').write_text('{}'),'Submitted snapshot differs');(root/'SUBMITTED_SNAPSHOT.json').write_bytes((m.SOURCE/'SUBMITTED_SNAPSHOT.json').read_bytes())
run('review_gate_omits_workflow',lambda:mutatejson('FINAL_REVIEW_GATE.json',lambda x:x['workflow'].pop('workflow_regression.py')),'exactly every required')
run('review_gate_nonclean',lambda:mutatejson('FINAL_REVIEW_GATE.json',lambda x:x['latest_review'].__setitem__('status','CHANGES_REQUIRED')),'clean review')
restore();v=root/'reviews/final/VERDICT.json';old=v.read_bytes();m.save(v,{'status':'CHANGES_REQUIRED'});mutatejson('FINAL_REVIEW_GATE.json',lambda x:x['latest_review'].__setitem__('verdict_sha256',hashlib.sha256(v.read_bytes()).hexdigest()));reason=m.reject(lambda:m.silent(u.main),'not CLEAN');v.write_bytes(old);results.append({'name':'nonclean_actual_verdict_with_rebound_digest','reason':reason,'refused_before_Git_object_or_external_mutation':g.created==g.pushes==g.edits==0})
restore();m.silent(u.main);receipt=p/'PR_BRANCH_RECEIPT.json';intent=p/'PR_BRANCH_INTENT.json';good_receipt=receipt.read_bytes();good_intent=intent.read_bytes();summary=json.loads(good_receipt);saved_tests=[]
for key in ['pr','base','branch','paths','files','review_gate_sha256','metadata_sha256','doi','doi_url','record_url','deposit_id','tracker_range','tracker_receipt_sha256','public_verification_receipt_sha256','body_sha256','shared_index_modified']:
 x=json.loads(good_receipt)
 if key=='paths':x[key].append('outside/path')
 elif key=='files':x[key][sorted(x[key])[0]]['sha256']='0'*64
 elif isinstance(x[key],bool):x[key]=not x[key]
 elif isinstance(x[key],int):x[key]+=1
 else:x[key]='altered'
 m.save(receipt,x);before=(g.created,g.pushes,g.edits);reason=m.reject(lambda:m.silent(u.main),'differs from current reviewed package');assert (g.created,g.pushes,g.edits)==before;saved_tests.append({'key':key,'refused':reason});receipt.write_bytes(good_receipt)
c=summary['commit'];oldparent=g.commits[c]['parent'];g.commits[c]['parent']='b'*40;parent=m.reject(lambda:m.silent(u.main),'unexpected parent');g.commits[c]['parent']=oldparent
oldtree=g.commits[c]['tree'];files=g.flatten(oldtree);files['outside/path']=b'not reviewed';g.commits[c]['tree']=g.buildtree(files);paths=m.reject(lambda:m.silent(u.main),'paths differ');g.commits[c]['tree']=oldtree
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','pre_mutation_guards':results,'saved_identity_reuse_mutations':saved_tests,'actual_saved_parent_mutation':parent,'actual_saved_extra_path_mutation':paths,'model_totals_after_all_tests':{'commits':g.created,'pushes':g.pushes,'body_edits':g.edits},'limit':'Production updater main with exact frozen package bytes, real production tree assembly, and Python in-memory Git/API adapters; no Git/network/application action ran.'};m.save(H/'WHOLE_MAIN_GATE_RESULTS.json',out);print(json.dumps({'status':out['status'],'prewrite_controls':len(results),'saved_identity_fields':len(saved_tests),'actual_parent_and_paths_refused':True,'model_totals':out['model_totals_after_all_tests']},indent=2))
