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
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('anchor',type=Path);a=p.parse_args();root=a.root.absolute();original_anchor=a.anchor.read_bytes()
    need(os.getuid()==os.geteuid()==1000,'UID 1000 required')
    cases=['stale_report', 'repinned_report', 'repinned_receipt', 'malicious_verifier', 'extra_file', 'extra_empty_directory', 'missing_file', 'symlink_file', 'symlink_directory', 'hardlink_file', 'manifest_duplicate_key', 'manifest_duplicate_path', 'manifest_bool_bytes', 'manifest_negative_bytes', 'manifest_traversal', 'manifest_absolute_path', 'manifest_unknown_key', 'manifest_wrong_type', 'scope_novelty', 'scope_bool_approaches', 'scope_import_removed', 'scope_cover_degree', 'scope_forests_solved', 'scope_revised_solved', 'scope_machine_topology', 'scope_unknown_key', 'receipt_truncated_output', 'receipt_bool_mode', 'receipt_wrong_failure', 'receipt_wrong_uid', 'root_symlink', 'root_parent_traversal', 'writable_file', 'writable_directory', 'anchor_internal', 'unknown_option']
    rows=[]
    for mode,flags in [(0,[]),(1,['-O']),(2,['-OO'])]:
      for case in cases:
        with tempfile.TemporaryDirectory(prefix='hopf-tree-control-') as t:
          w=Path(t);c=w/'candidate';shutil.copytree(root,c);perms(c,False)
          anc=w/'anchor.py';anc.write_bytes(original_anchor);anchor_type='fixed_reviewed_anchor'
          m=json.loads((c/'DELIVERY_MANIFEST.json').read_bytes())
          manifest_changes=False;test_repin=False
          if case=='stale_report':(c/'original/PROOF_APPLICATION.md').write_bytes((c/'original/PROOF_APPLICATION.md').read_bytes()+b'\nunauthorized edit\n')
          elif case in ['repinned_report','repinned_receipt','malicious_verifier']:
            n={'repinned_report':'original/PROOF_APPLICATION.md','repinned_receipt':'verification/REPRODUCTION.json','malicious_verifier':'verify_publication.py'}[case]
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
            shutil.move(str(c/'original'),str(w/'outside_original'));(c/'original').symlink_to(w/'outside_original',target_is_directory=True)
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
            if case=='scope_novelty':s['novelty_claim']=True
            elif case=='scope_bool_approaches':s['approaches']=False
            elif case=='scope_import_removed':s['smooth_Q8_theorem_explicitly_imported']=False
            elif case=='scope_cover_degree':s['oriented_labelled_connected_cover_degree']=2
            elif case=='scope_forests_solved':s['general_forest_formula_solved']=True
            elif case=='scope_revised_solved':s['revised_conjecture_solved']=True
            elif case=='scope_machine_topology':s['smooth_topology_machine_verified']=True
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
              rr['runs'][2]['stderr']=pack(b'RuntimeError: wrong failure\n')
            elif case=='receipt_wrong_uid':rr['uid']=0
            write_json(c/'verification/REPRODUCTION.json',rr)
            for e in m['files']:
              if e['path']=='verification/REPRODUCTION.json':e.update(pin((c/'verification/REPRODUCTION.json').read_bytes()))
            manifest_changes=True;test_repin=True
          if manifest_changes:
            write_json(c/'DELIVERY_MANIFEST.json',m)
            if case=='manifest_duplicate_key':
              b=(c/'DELIVERY_MANIFEST.json').read_bytes();(c/'DELIVERY_MANIFEST.json').write_bytes(b.replace(b'{',b'{"schema":"duplicate",',1))
          if test_repin:
            oldhash=sha((root/'DELIVERY_MANIFEST.json').read_bytes());newhash=sha((c/'DELIVERY_MANIFEST.json').read_bytes());changed=original_anchor.replace(oldhash.encode(),newhash.encode());need(changed!=original_anchor,'test anchor replacement');anc.write_bytes(changed);(c/'bootstrap.py').write_bytes(changed);anchor_type='test_only_manifest_repin'
          perms(c,True)
          if case=='writable_file':(c/'ACCEPTANCE.md').chmod(0o644)
          elif case=='writable_directory':(c/'original').chmod(0o755)
          command=[sys.executable,'-I','-S','-B',*flags,str(c/'bootstrap.py' if case=='anchor_internal' else anc),str(c)]
          if case=='unknown_option':command+=['--integrity-only']
          elif case=='root_symlink':
            (w/'linked_root').symlink_to(c,target_is_directory=True);command[-1]=str(w/'linked_root')
          elif case=='root_parent_traversal':
            command[-1]=str(c/'original/../')
          r=run(command,w);need(r['exit_code']!=0,'hostile control unexpectedly accepted '+case);need(not (c/'MALICIOUS_EXECUTED').exists(),'unauthenticated code executed')
          rows.append({'case':case,'optimization':mode,'anchor':anchor_type,'expected':'REJECT','result':r})
          perms(c,False)
      comparison_cases=['unchanged_author','unchanged_independent','unchanged_negative','author_scope','author_extra_key','independent_scope','independent_extra_key','nested_extra_key','nested_bool_int','nested_int_float','stdout_whitespace','stderr_added','nested_value','outer_bool_exit','outer_extra_key','outer_string_mode','negative_stderr_changed','negative_stdout_added','synthetic_list_reordered']
      for case in comparison_cases:
        probe="""import copy,importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('replay',sys.argv[1]);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=json.loads(Path(sys.argv[2]).read_bytes())['runs'];case=sys.argv[3];mode=int(sys.argv[4]);label='independent_positive' if case in ['unchanged_independent','independent_scope','independent_extra_key'] else 'author_positive'
if case in ['unchanged_negative','negative_stderr_changed','negative_stdout_added']:label='independent_split_extension'
reference=next(e for e in rows if e['label']==label and e['optimization']==mode);fresh=copy.deepcopy(reference)
if reference['exit_code']==0:
 o=json.loads(fresh['stdout']['text'])
 if case in ['author_scope','independent_scope']:o['scope']='unchecked alteration'
 elif case in ['author_extra_key','independent_extra_key']:o['extra']='unexpected'
 elif case=='nested_extra_key':o['q8_order_distribution']['extra']=0
 elif case=='nested_bool_int':o['q8_order_distribution']['1']=True
 elif case=='nested_int_float':o['q8_order_distribution']['4']=6.0
 elif case=='nested_value':o['q8_order_distribution']['4']=7
 if case in ['author_scope','independent_scope','author_extra_key','independent_extra_key','nested_extra_key','nested_bool_int','nested_int_float','nested_value']:fresh['stdout']=v.stream((json.dumps(o,sort_keys=True)+'\\n').encode())
if case=='stdout_whitespace':fresh['stdout']=v.stream((fresh['stdout']['text']+' ').encode())
elif case=='stderr_added':fresh['stderr']=v.stream(b'unexpected stderr\\n')
elif case=='outer_bool_exit':fresh['exit_code']=False
elif case=='outer_extra_key':fresh['extra']='unexpected'
elif case=='outer_string_mode':fresh['optimization']=str(mode)
elif case=='negative_stderr_changed':fresh['stderr']=v.stream((fresh['stderr']['text']+' ').encode())
elif case=='negative_stdout_added':fresh['stdout']=v.stream(b'unexpected')
try:
 if case=='synthetic_list_reordered':v.exact_json_equal({'nested':[2,1]},{'nested':[1,2]})
 else:result=v.compare_fresh_reference(fresh,reference)
except Exception as e:print(json.dumps({'status':'REJECT','reason':str(e)}));sys.exit(1)
print(json.dumps({'status':'PASS','comparison':result}))
"""
        r=run([sys.executable,'-I','-S','-B',*flags,'-c',probe,str(root/'verify_publication.py'),str(root/'verification/REPRODUCTION.json'),case,str(mode)],root)
        expected=0 if case.startswith('unchanged_') else 1
        need(r['exit_code']==expected and r['stderr']['text']=='','direct exact-byte/type comparison '+case)
        rows.append({'case':'pure_output_'+case,'optimization':mode,'anchor':'pure_comparison_no_hash_or_integrity_shortcut','expected':'PASS' if expected==0 else 'REJECT','result':r})
    return {'schema':'hopf-tree-authored-hostile-controls-v1' ,'uid':os.geteuid(),'input_delivery_manifest_sha256':sha((root/'DELIVERY_MANIFEST.json').read_bytes()),'input_external_bootstrap_sha256':sha(original_anchor),'receipt_scope':'This pre-seal test inventory excludes this receipt itself. Final external bootstrap re-seals the complete delivery including this receipt. Test-only manifest anchors are explicitly labeled.','modes':[0,1,2],'negative_count':sum(x['expected']=='REJECT' for x in rows),'positive_count':sum(x['expected']=='PASS' for x in rows),'semantic_negative_count_in_fresh_reproduction':30,'pure_output_comparison_negatives':48,'pure_output_comparison_positives':9,'tests':rows}

if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
