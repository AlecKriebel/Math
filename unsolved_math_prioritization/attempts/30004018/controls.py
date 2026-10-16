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
    cases=['stale_report','repinned_report','repinned_receipt','malicious_verifier','extra_file','extra_empty_directory','missing_file','symlink_file','symlink_directory','hardlink_file','manifest_duplicate_key','manifest_duplicate_path','manifest_bool_bytes','manifest_negative_bytes','manifest_traversal','manifest_absolute_path','manifest_unknown_key','manifest_wrong_type','scope_promoted','scope_bool_approaches','scope_gap_removed','scope_source_falsely_passed','queue_arg_absent','queue_symlink','root_symlink','root_parent_traversal','queue_absent','queue_wrong_path','queue_modified','queue_chat_modified','queue_doi_modified','queue_other_row_modified','queue_proof_forged','writable_file','writable_directory','writable_queue','anchor_internal','unknown_option']
    rows=[]
    for mode,flags in [(0,[]),(1,['-O']),(2,['-OO'])]:
      for case in cases:
        with tempfile.TemporaryDirectory(prefix='duflo-control-') as t:
          w=Path(t);c=w/'candidate';shutil.copytree(root,c);perms(c,False)
          q=w/'repository/unsolved_math_prioritization/QUEUE.md';q.parent.mkdir(parents=True);q.write_bytes(queue_bytes)
          anc=w/'anchor.py';anc.write_bytes(original_anchor);anchor_type='fixed_reviewed_anchor'
          m=json.loads((c/'DELIVERY_MANIFEST.json').read_bytes())
          manifest_changes=False;test_repin=False
          if case=='stale_report':(c/'original/MATHEMATICAL_AUDIT.md').write_bytes((c/'original/MATHEMATICAL_AUDIT.md').read_bytes()+b'\nunauthorized edit\n')
          elif case in ['repinned_report','repinned_receipt','malicious_verifier']:
            n={'repinned_report':'original/MATHEMATICAL_AUDIT.md','repinned_receipt':'verification/REPRODUCTION.json','malicious_verifier':'verify_publication.py'}[case]
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
            shutil.move(str(c/'audit'),str(w/'outside_audit'));(c/'audit').symlink_to(w/'outside_audit',target_is_directory=True)
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
            elif case=='scope_gap_removed':s['remaining_gap']='resolved'
            elif case=='scope_source_falsely_passed':s['default_absent_inputs']['source_pdf_rehash']='PASS'
            write_json(c/'SCOPE.json',s)
            for e in m['files']:
              if e['path']=='SCOPE.json':e.update(pin((c/'SCOPE.json').read_bytes()))
            manifest_changes=True;test_repin=True
          elif case=='queue_symlink':
            q.rename(w/'outside_queue');q.symlink_to(w/'outside_queue')
          elif case=='queue_absent':q.unlink()
          elif case=='queue_wrong_path':q.rename(q.with_name('SHADOW.md'));q=q.with_name('SHADOW.md')
          elif case=='queue_modified':q.write_bytes(queue_bytes+b'\n')
          elif case in ['queue_chat_modified','queue_doi_modified']:
            lines=queue_bytes.splitlines(keepends=True);i=next(i for i,l in enumerate(lines) if b'| 30004018 / OWR-16635-003 |' in l);cells=lines[i].split(b'|');cells[10 if case=='queue_chat_modified' else 12]=b' changed ';lines[i]=b'|'.join(cells);q.write_bytes(b''.join(lines))
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
          elif case=='writable_directory':(c/'audit').chmod(0o755)
          elif case=='writable_queue':q.chmod(0o644)
          command=[sys.executable,'-I','-S','-B',*flags,str(c/'bootstrap.py' if case=='anchor_internal' else anc),str(c),'--queue',str(q)]
          if case=='unknown_option':command+=['--integrity-only']
          elif case=='queue_arg_absent':command=command[:-2]
          elif case=='root_symlink':
            (w/'linked_root').symlink_to(c,target_is_directory=True);command[-3]=str(w/'linked_root')
          elif case=='root_parent_traversal':
            command[-3]=str(c/'audit/../')
          r=run(command,w);need(r['exit_code']!=0,'hostile control unexpectedly accepted '+case);need(not (c/'MALICIOUS_EXECUTED').exists(),'unauthenticated code executed')
          rows.append({'case':case,'optimization':mode,'anchor':anchor_type,'expected':'REJECT','result':r})
          perms(c,False)
      # Direct mathematical failures, without manifest or source-hash guards.
      for mutation in ['exterior-sign','wrong-weight','wrong-parity','class-implies-object','wrong-moment','drop-total-arrow','action-rank-is-algebra-rank','omit-Koszul-sign']:
        r=run([sys.executable,'-I','-S','-B',*flags,str(root/'audit/independent_checks.py'),'--mutation',mutation],root)
        output=[json.loads(x) for x in r['stdout']['text'].splitlines()]
        need(r['exit_code']==1 and r['stderr']['text']=='' and output[-1]['status']=='FAIL','unmasked mathematical rejection '+mutation)
        rows.append({'case':'mathematical_'+mutation,'optimization':mode,'hash_guards_involved':False,'expected':'REJECT','result':r})
      # Pure comparison tests call the comparison function directly. No manifest,
      # byte-pin or scope guard can mask an output-schema/value/type failure here.
      for who in ['original','independent']:
        for case in ['unchanged','unchecked_value','extra_top_key','nested_int_to_bool','nested_int_to_float','stdout_whitespace','stderr_added','duplicate_json_key']:
          code=r'''
import importlib.util,json,pathlib,sys
try:
    root=pathlib.Path(sys.argv[1]);who=sys.argv[2];mode=sys.argv[3];case=sys.argv[4]
    spec=importlib.util.spec_from_file_location('reviewed_comparator',root/'verify_publication.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    receipt=json.loads((root/'verification/REPRODUCTION.json').read_bytes())
    entry=next(e for e in receipt['runs'] if e['kind']==who and e['optimization']==int(mode))
    expected=module.output_reference(entry['stdout']);expected_err=module.output_reference(entry['stderr'])
    data=module.parse_output(expected);actual=expected;actual_err=expected_err
    if case=='unchecked_value':data[-1]['scope']='changed formerly unchecked output'
    elif case=='extra_top_key':data[0]['unchecked_extra']=True
    elif case=='nested_int_to_bool':
        if who=='original':data[0]['python_optimize']=bool(data[0]['python_optimize'])
        else:next(row for row in data if row.get('event')=='tensor_Kunneth')['cases'][0]['factor_ranks'][0]=False
    elif case=='nested_int_to_float':
        if who=='original':data[0]['checks']=float(data[0]['checks'])
        else:next(row for row in data if row.get('event')=='tensor_Kunneth')['cases'][0]['factor_ranks'][0]=0.0
    elif case=='stdout_whitespace':actual=expected+b'\n'
    elif case=='stderr_added':actual_err=b'unexpected stderr\n'
    elif case=='duplicate_json_key':actual=expected.replace(b'{',b'{"event":"duplicate",' if who=='independent' else b'{"status":"duplicate",',1)
    if case not in ['unchanged','stdout_whitespace','stderr_added','duplicate_json_key']:actual=('\n'.join(json.dumps(row,sort_keys=True) for row in data)+'\n').encode()
    module.compare_output(actual,actual_err,expected,expected_err)
    print('{"status":"PASS_UNCHANGED_FULL_OUTPUT"}')
except Exception as e:
    print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
'''
          r=run([sys.executable,'-I','-S','-B',*flags,'-c',code,str(root),who,str(mode),case],root)
          need((r['exit_code']==0)==(case=='unchanged'),'pure output comparison '+who+' '+case)
          if case!='unchanged':
            reason={'unchecked_value':'exact JSON value','extra_top_key':'exact JSON keys','nested_int_to_bool':'exact JSON type','nested_int_to_float':'exact JSON type','stdout_whitespace':'complete fresh stdout bytes','stderr_added':'complete fresh stderr bytes','duplicate_json_key':'duplicate JSON key'}[case]
            need(reason in r['stderr']['text'],'pure comparator rejection was masked')
          rows.append({'case':who+'_pure_comparison_'+case,'optimization':mode,'hash_guards_involved':False,'expected':'PASS' if case=='unchanged' else 'REJECT','result':r})
    return {'schema':'duflo-socle-hostile-controls-v1','uid':os.geteuid(),'input_delivery_manifest_sha256':sha((root/'DELIVERY_MANIFEST.json').read_bytes()),'input_external_bootstrap_sha256':sha(original_anchor),'receipt_scope':'This pre-seal test inventory excludes this receipt itself. Final external bootstrap re-seals the complete delivery including this receipt. Test-only manifest anchors are explicitly labeled.','modes':[0,1,2],'negative_count':sum(x['expected']=='REJECT' for x in rows),'positive_count':sum(x['expected']=='PASS' for x in rows),'semantic_negative_count':24,'pure_comparison_negative_count':42,'pure_comparison_positive_count':6,'tests':rows}

if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
