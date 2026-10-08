#!/usr/bin/env python3
"""Adversarial tests of the fixed bootstrap; outputs remain outside tested inputs.
Schema controls deliberately update ONLY a test anchor's manifest SHA. This tests
schema guards independently of fixed-hash rejection and grants no publication trust.
Semantic controls run mutated authored code directly, without byte-integrity guards.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(ok,label):
    if not ok:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def pack(b):return {'type':'inline_utf8','bytes':len(b),'sha256':sha(b),'text':b.decode('utf-8')}
def write_json(p,o):p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def perms(root,ro):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if not p.is_symlink():p.chmod((0o555 if p.is_dir() else 0o444) if ro else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if ro else 0o755)
def run(command,cwd):
    r=subprocess.run(command,cwd=cwd,capture_output=True,timeout=60)
    return {'exit_code':r.returncode,'stdout':pack(r.stdout),'stderr':pack(r.stderr)}
def pin(b):return {'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('anchor',type=Path);p.add_argument('--queue',required=True,type=Path);a=p.parse_args();root=a.root.absolute();original_anchor=a.anchor.read_bytes();queue_bytes=a.queue.read_bytes()
    need(os.getuid()==os.geteuid()==1000,'UID 1000 required')
    cases=['stale_report','repinned_report','repinned_receipt','malicious_verifier','extra_file','extra_empty_directory','missing_file','symlink_file','symlink_directory','hardlink_file','manifest_duplicate_key','manifest_duplicate_path','manifest_bool_bytes','manifest_negative_bytes','manifest_traversal','manifest_absolute_path','manifest_unknown_key','manifest_wrong_type','scope_promoted','scope_bool_approaches','scope_interpolation_removed','scope_original_falsely_passed','scope_self_gluings_removed','scope_isometry_map_promoted','scope_D_conflated','scope_unknown_key','receipt_truncated_output','receipt_bool_mode','receipt_wrong_failure','receipt_wrong_uid','queue_arg_absent','queue_symlink','root_symlink','root_parent_traversal','queue_absent','queue_wrong_path','queue_modified','queue_chat_modified','queue_doi_modified','queue_other_row_modified','queue_proof_forged','writable_file','writable_directory','writable_queue','anchor_internal','unknown_option']
    rows=[]
    for mode,flags in [(0,[]),(1,['-O']),(2,['-OO'])]:
      for case in cases:
        with tempfile.TemporaryDirectory(prefix='variational-control-') as t:
          w=Path(t);c=w/'candidate';shutil.copytree(root,c);perms(c,False)
          q=w/'repository/unsolved_math_prioritization/QUEUE.md';q.parent.mkdir(parents=True);q.write_bytes(queue_bytes)
          anc=w/'anchor.py';anc.write_bytes(original_anchor);anchor_type='fixed_reviewed_anchor'
          m=json.loads((c/'DELIVERY_MANIFEST.json').read_bytes())
          manifest_changes=False;test_repin=False
          if case=='stale_report':(c/'current_derivative/REPORT.md').write_bytes((c/'current_derivative/REPORT.md').read_bytes()+b'\nunauthorized edit\n')
          elif case in ['repinned_report','repinned_receipt','malicious_verifier']:
            n={'repinned_report':'current_derivative/REPORT.md','repinned_receipt':'verification/REPRODUCTION.json','malicious_verifier':'verify_publication.py'}[case]
            if case=='malicious_verifier':(c/n).write_text("from pathlib import Path\nPath('MALICIOUS_EXECUTED').write_text('unsafe')\n")
            else:(c/n).write_bytes((c/n).read_bytes()+b'\n')
            for e in m['files']:
              if e['path']==n:e.update(pin((c/n).read_bytes()))
            manifest_changes=True
          elif case=='extra_file':(c/'extra.txt').write_text('extra')
          elif case=='extra_empty_directory':(c/'empty').mkdir()
          elif case=='missing_file':(c/'ACCEPTANCE.md').unlink()
          elif case=='symlink_file':
            b=(c/'ACCEPTANCE.md').read_bytes();(w/'outside.md').write_bytes(b);(c/'ACCEPTANCE.md').unlink();(c/'ACCEPTANCE.md').symlink_to(w/'outside.md')
          elif case=='symlink_directory':
            shutil.move(str(c/'current_derivative'),str(w/'outside_derivative'));(c/'current_derivative').symlink_to(w/'outside_derivative',target_is_directory=True)
          elif case=='hardlink_file':os.link(c/'ACCEPTANCE.md',w/'hardlink.md')
          elif case.startswith('manifest_'):
            test_repin=True;manifest_changes=True
            if case=='manifest_duplicate_key':pass
            elif case=='manifest_duplicate_path':m['files'].append(dict(m['files'][0]))
            elif case=='manifest_bool_bytes':m['files'][0]['bytes']=True
            elif case=='manifest_negative_bytes':m['files'][0]['bytes']=-1
            elif case=='manifest_traversal':m['files'][0]['path']='../escape'
            elif case=='manifest_absolute_path':m['files'][0]['path']='/escape'
            elif case=='manifest_unknown_key':m['unexpected']=True
            elif case=='manifest_wrong_type':m['files']={}
          elif case.startswith('scope_'):
            s=json.loads((c/'SCOPE.json').read_bytes())
            if case=='scope_promoted':s['full_target_resolved']=True
            elif case=='scope_bool_approaches':s['approaches']=True
            elif case=='scope_interpolation_removed':s['interpolation_admissibility_required']=False
            elif case=='scope_original_falsely_passed':s['default_checks']['original_full_reproduction']='PASS'
            elif case=='scope_self_gluings_removed':s['self_glued_faces_remain_in_full_target']=False
            elif case=='scope_isometry_map_promoted':s['isometry_map_identification_conditional']=False
            elif case=='scope_D_conflated':s['D_and_weak_closure_distinct']=False
            elif case=='scope_unknown_key':s['unexpected']=True
            write_json(c/'SCOPE.json',s)
            for e in m['files']:
              if e['path']=='SCOPE.json':e.update(pin((c/'SCOPE.json').read_bytes()))
            manifest_changes=True;test_repin=True
          elif case.startswith('receipt_'):
            rr=json.loads((c/'verification/REPRODUCTION.json').read_bytes())
            if case=='receipt_truncated_output':rr['runs'][0]['stdout']['text']=''
            elif case=='receipt_bool_mode':rr['runs'][0]['optimization']=False
            elif case=='receipt_wrong_failure':
              out=json.loads(rr['runs'][1]['stdout']['text']);out['error']='wrong';rr['runs'][1]['stdout']=pack((json.dumps(out)+'\n').encode())
            elif case=='receipt_wrong_uid':rr['uid']=0
            write_json(c/'verification/REPRODUCTION.json',rr)
            for e in m['files']:
              if e['path']=='verification/REPRODUCTION.json':e.update(pin((c/'verification/REPRODUCTION.json').read_bytes()))
            manifest_changes=True;test_repin=True
          elif case=='queue_symlink':
            q.rename(w/'outside_queue');q.symlink_to(w/'outside_queue')
          elif case=='queue_absent':q.unlink()
          elif case=='queue_wrong_path':q.rename(q.with_name('SHADOW.md'));q=q.with_name('SHADOW.md')
          elif case=='queue_modified':q.write_bytes(queue_bytes+b'\n')
          elif case in ['queue_chat_modified','queue_doi_modified']:
            lines=queue_bytes.splitlines(keepends=True);i=next(i for i,l in enumerate(lines) if b'| 30003946 / OWR-16415-008 |' in l);cells=lines[i].split(b'|');cells[10 if case=='queue_chat_modified' else 12]=b' changed ';lines[i]=b'|'.join(cells);q.write_bytes(b''.join(lines))
          elif case=='queue_other_row_modified':q.write_bytes(queue_bytes.replace(b'| 1 | 30000990 /',b'| 0 | 30000990 /',1))
          elif case=='queue_proof_forged':
            s=json.loads((c/'QUEUE_PROOF.json').read_bytes());s['before']['bytes']+=1;write_json(c/'QUEUE_PROOF.json',s)
            for e in m['files']:
              if e['path']=='QUEUE_PROOF.json':e.update(pin((c/'QUEUE_PROOF.json').read_bytes()))
            manifest_changes=True;test_repin=True
          if manifest_changes:
            write_json(c/'DELIVERY_MANIFEST.json',m)
            if case=='manifest_duplicate_key':
              b=(c/'DELIVERY_MANIFEST.json').read_bytes();(c/'DELIVERY_MANIFEST.json').write_bytes(b.replace(b'{',b'{"schema":"duplicate",',1))
          if test_repin:
            oldhash=sha((root/'DELIVERY_MANIFEST.json').read_bytes());newhash=sha((c/'DELIVERY_MANIFEST.json').read_bytes());changed=original_anchor.replace(oldhash.encode(),newhash.encode());need(changed!=original_anchor,'test anchor replacement');anc.write_bytes(changed);(c/'bootstrap.py').write_bytes(changed);anchor_type='test_only_manifest_repin'
          perms(c,True)
          if q.exists():q.chmod(0o444)
          if case=='writable_file':(c/'ACCEPTANCE.md').chmod(0o644)
          elif case=='writable_directory':(c/'current_derivative').chmod(0o755)
          elif case=='writable_queue':q.chmod(0o644)
          command=[sys.executable,'-I','-S','-B',*flags,str(c/'bootstrap.py' if case=='anchor_internal' else anc),str(c),'--queue',str(q)]
          if case=='unknown_option':command+=['--integrity-only']
          elif case=='queue_arg_absent':command=command[:-2]
          elif case=='root_symlink':
            (w/'linked_root').symlink_to(c,target_is_directory=True);command[-3]=str(w/'linked_root')
          elif case=='root_parent_traversal':
            command[-3]=str(c/'current_derivative/../')
          r=run(command,w);need(r['exit_code']!=0,'hostile control unexpectedly accepted '+case);need(not (c/'MALICIOUS_EXECUTED').exists(),'unauthenticated code executed')
          rows.append({'case':case,'optimization':mode,'anchor':anchor_type,'expected':'REJECT','result':r})
          perms(c,False)
      mutations={'flat_laplacian':'flat_harmonicity_by_exact_differences','flat_orientation':'flat_jacobian_polynomial_interpolation','area_normalization':'energy_area_exact_interpolation','curvature_sign':'negative_curvature_strict_rank_two_term','cusp_amplitude':'cusp_remote_folds_and_upper_derivative','cusp_harmonicity':'cusp_is_not_harmonic','collapsed_trace_injectivity':'collapsed_trace_tests_have_nontrivial_kernel','weak_lower_semicontinuity_direction':'lower_semicontinuity_is_only_one_sided','quotient_trace_equals_side_incidence':'quotient_trace_is_not_side_incidence'}
      for mutation,failed in mutations.items():
        r=run([sys.executable,'-I','-S','-B',*flags,str(root/'independent_verify.py'),'--mutation',mutation],root)
        need(r['exit_code']==1 and r['stderr']['text']=='' and json.loads(r['stdout']['text'])['failed_check']==failed,'named semantic mutation '+mutation)
        rows.append({'case':'semantic_'+mutation,'optimization':mode,'anchor':'none_direct_mathematical_mutation','expected':'REJECT','result':r})
      comparison_cases=['unchanged_author','unchanged_independent','author_scope','author_extra_key','independent_scope','independent_extra_key','nested_extra_key','nested_bool_int','nested_int_float','stdout_whitespace','stderr_added','nested_value','list_reordered','outer_bool_exit','outer_extra_key','outer_string_mode']
      for case in comparison_cases:
        probe="""import copy,hashlib,importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('replay',sys.argv[1]);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=json.loads(Path(sys.argv[2]).read_bytes())['runs'];case=sys.argv[3];mode=int(sys.argv[4]);label='author_positive' if case in ['unchanged_author','author_scope','author_extra_key','stdout_whitespace','stderr_added','outer_bool_exit','outer_extra_key','outer_string_mode'] else 'independent_positive'
reference=next(e for e in rows if e['label']==label and e['optimization']==mode);fresh=copy.deepcopy(reference);o=json.loads(fresh['stdout']['text'])
if case in ['author_scope','independent_scope']:o['scope']='unchecked alteration'
elif case in ['author_extra_key','independent_extra_key']:o['extra']='unexpected'
elif case=='nested_extra_key':o['checks'][0]['evidence']['extra']=0
elif case=='nested_bool_int':o['checks'][4]['evidence']['energy_prefactor']=True
elif case=='nested_int_float':o['checks'][5]['evidence']['nondegenerate_rational_cases']=384.0
elif case=='nested_value':o['checks'][0]['evidence']['degree_bound']=4
elif case=='list_reordered':o['checks'][0],o['checks'][1]=o['checks'][1],o['checks'][0]
if case not in ['unchanged_author','unchanged_independent','stdout_whitespace','stderr_added','outer_bool_exit','outer_extra_key','outer_string_mode']:fresh['stdout']=v.stream((json.dumps(o,sort_keys=True)+'\\n').encode())
if case=='stdout_whitespace':fresh['stdout']=v.stream((fresh['stdout']['text']+' ').encode())
elif case=='stderr_added':fresh['stderr']=v.stream(b'unexpected stderr\\n')
elif case=='outer_bool_exit':fresh['exit_code']=False
elif case=='outer_extra_key':fresh['extra']='unexpected'
elif case=='outer_string_mode':fresh['optimization']=str(mode)
try:result=v.compare_fresh_reference(fresh,reference)
except Exception as e:print(json.dumps({'status':'REJECT','reason':str(e)}));sys.exit(1)
print(json.dumps({'status':'PASS','comparison':result}))
"""
        r=run([sys.executable,'-I','-S','-B',*flags,'-c',probe,str(root/'verify_publication.py'),str(root/'verification/REPRODUCTION.json'),case,str(mode)],root)
        expected=0 if case.startswith('unchanged_') else 1
        need(r['exit_code']==expected and r['stderr']['text']=='','direct exact-byte/type comparison '+case)
        rows.append({'case':'pure_output_'+case,'optimization':mode,'anchor':'pure_comparison_no_hash_or_integrity_shortcut','expected':'PASS' if expected==0 else 'REJECT','result':r})
      queue_cases=['valid','missing_target','duplicate_target','chat_changed','doi_changed','other_row_changed','leading_literal_changed','trailing_newline_changed','wrong_turns','missing_findings_change','wrong_status','nonbyte_input']
      for case in queue_cases:
        probe="""import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('anchor',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a=Path(sys.argv[2]).read_bytes();p=json.loads(Path(sys.argv[3]).read_bytes());before=a.replace(p['after_row_utf8'].encode(),p['before_row_utf8'].encode());after=a;case=sys.argv[4]
lines=after.splitlines(keepends=True);i=next(i for i,l in enumerate(lines) if b'| 30003946 / OWR-16415-008 |' in l)
if case=='missing_target':del lines[i]
elif case=='duplicate_target':lines.append(lines[i])
elif case in ['chat_changed','doi_changed','wrong_turns','missing_findings_change','wrong_status']:
 c=lines[i].split(b'|');idx={'chat_changed':10,'doi_changed':12,'wrong_turns':9,'missing_findings_change':11,'wrong_status':8}[case];c[idx]=p['before_row_utf8'].encode().split(b'|')[idx] if case=='missing_findings_change' else b' changed ';lines[i]=b'|'.join(c)
elif case=='other_row_changed':lines[i-1]+=b'changed\\n'
elif case=='leading_literal_changed':lines[0]+=b'changed\\n'
elif case=='trailing_newline_changed':lines.append(b'\\n')
elif case=='nonbyte_input':before=bytearray(before)
after=b''.join(lines)
try:result=m.compare_queue_bytes(before,after)
except Exception as e:print(json.dumps({'status':'REJECT','reason':str(e)}));sys.exit(1)
print(json.dumps({'status':'PASS','comparison':result}))
"""
        r=run([sys.executable,'-I','-S','-B',*flags,'-c',probe,str(a.anchor.absolute()),str(a.queue.absolute()),str(root/'QUEUE_PROOF.json'),case],root)
        expected=0 if case=='valid' else 1
        need(r['exit_code']==expected and r['stderr']['text']=='','pure queue comparison '+case)
        rows.append({'case':'pure_queue_'+case,'optimization':mode,'anchor':'pure_comparison_no_integrity_shortcut','expected':'PASS' if expected==0 else 'REJECT','result':r})
    return {'schema':'variational-maps-hostile-controls-v1' ,'uid':os.geteuid(),'input_delivery_manifest_sha256':sha((root/'DELIVERY_MANIFEST.json').read_bytes()),'input_external_bootstrap_sha256':sha(original_anchor),'receipt_scope':'This pre-seal test inventory excludes this receipt itself. Final external bootstrap re-seals the complete delivery including this receipt. Test-only manifest anchors are explicitly labeled.','modes':[0,1,2],'negative_count':sum(x['expected']=='REJECT' for x in rows),'positive_count':sum(x['expected']=='PASS' for x in rows),'semantic_negative_count':27,'pure_output_comparison_negatives':42,'pure_output_comparison_positives':6,'tests':rows}

if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
