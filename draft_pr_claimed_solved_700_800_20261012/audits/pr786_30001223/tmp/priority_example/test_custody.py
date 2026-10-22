#!/usr/bin/env python3
"""Test only copied packet/input/body files under the supplied owned body scratch."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def sha(raw): return hashlib.sha256(raw).hexdigest()
def need(x,m):
    if not x: raise ValueError(m)
def dump(path,obj): path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(a):
    packet, inputs, bodies = (Path(getattr(a,k)).resolve() for k in ('packet','inputs_root','bodies_root'))
    baseline = (packet/'MANIFEST.json').read_bytes()
    manifest_pin, checker_pin = sha(baseline),sha((packet/'custody_check.py').read_bytes())
    original_files = json.loads((packet/'INPUTS.json').read_text())['files']
    body_files = json.loads((packet/'BODIES.json').read_text())['files']
    results = []
    controls = [
      'wrong_manifest_pin','wrong_checker_pin','report_bytes','missing_report','extra_file',
      'nested_directory','listed_symlink','author_source_bytes','archive_bytes','historical_source_bytes',
      'unlisted_original','public_record_bytes','math_gate_bytes','pdf_bytes','extracted_text_bytes',
      'render_bytes','exception_widen_rebound','duplicate_json_rebound','unsafe_path_rebound',
      'novelty_flag_rebound','peer_input_rebound','frozen_plan_rebound','query_ledger_rebound',
      'input_symlink','comparison_result_rebound','comparison_execution_rebound','nonfinite_json_rebound',
      'boolean_byte_count_rebound','required_removed_rebound','unsafe_input_path_rebound'
    ]
    with tempfile.TemporaryDirectory(prefix='custody-test-',dir=bodies) as work:
      work=Path(work)
      for mode in (0,1):
        opts=['-B']+(['-O'] if mode else [])
        def invoke(pk,ir,br,mp=manifest_pin,cp=checker_pin):
            return subprocess.run([sys.executable]+opts+[str(pk/'custody_check.py'),
                   '--packet',str(pk),'--inputs-root',str(ir),'--bodies-root',str(br),
                   '--expected-manifest-sha',mp,'--expected-checker-sha',cp],
                   capture_output=True,text=True)
        good=invoke(packet,inputs,bodies)
        need(good.returncode==0,'Baseline failed: '+good.stderr)
        results.append({'mode':mode,'control':'unaltered_positive','accepted':True,
                        'stdout_sha256':sha(good.stdout.encode())})
        for control in controls:
            case=work/'case'
            if case.exists(): shutil.rmtree(case)
            pk=case/'packet';pk.mkdir(parents=True)
            for f in packet.iterdir():
                need(f.is_file() and not f.is_symlink(),'Test baseline must be flat regular files')
                shutil.copyfile(f,pk/f.name)
            ir,br=inputs,bodies
            if control in ('author_source_bytes','archive_bytes','historical_source_bytes',
                           'unlisted_original','public_record_bytes','math_gate_bytes','input_symlink'):
                ir=case/'inputs'
                for rel in original_files:
                    dst=ir/rel;dst.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copyfile(inputs/rel,dst)
            if control in ('pdf_bytes','extracted_text_bytes','render_bytes'):
                br=case/'bodies';br.mkdir()
                for name in body_files: shutil.copyfile(bodies/name,br/name)
            mp,cp=manifest_pin,checker_pin
            def mutate(path):
                path.write_bytes(path.read_bytes()+b'\nTAMPERED_COPY\n')
            def rebind():
                nonlocal mp
                m=json.loads((pk/'MANIFEST.json').read_text())
                for name in list(m['files']):
                    f=pk/name
                    if f.exists() and f.is_file():
                        raw=f.read_bytes();m['files'][name]={'bytes':len(raw),'sha256':sha(raw)}
                dump(pk/'MANIFEST.json',m);mp=sha((pk/'MANIFEST.json').read_bytes())
            if control=='wrong_manifest_pin': mp='0'*64
            elif control=='wrong_checker_pin': cp='0'*64
            elif control=='report_bytes': mutate(pk/'REPORT_PRE_PEER.md')
            elif control=='missing_report': (pk/'REPORT_PRE_PEER.md').unlink()
            elif control=='extra_file': (pk/'EXTRA').write_text('unlisted')
            elif control=='nested_directory': (pk/'NESTED').mkdir()
            elif control=='listed_symlink':
                target=case/'linked-report';shutil.copyfile(pk/'REPORT_PRE_PEER.md',target)
                (pk/'REPORT_PRE_PEER.md').unlink();(pk/'REPORT_PRE_PEER.md').symlink_to(target)
            elif control=='author_source_bytes': mutate(ir/'intake/original/unsolved_math_prioritization/attempts/30001223/author/proof.md')
            elif control=='archive_bytes': mutate(ir/'intake/original/unsolved_math_prioritization/attempts/30001223/archives/YOUNG_TOPS_30001223_SECOND_ADVERSARIAL_REVIEW_SAFE.zip')
            elif control=='historical_source_bytes': mutate(ir/'intake/original/unsolved_math_prioritization/attempts/30001223/first_audit/mathematical_audit.md')
            elif control=='unlisted_original': (ir/'intake/original/EXTRA').write_text('unbound original')
            elif control=='public_record_bytes': mutate(ir/'intake/SELECTED_PUBLIC_RECORD.json')
            elif control=='math_gate_bytes': mutate(ir/'root-receipts/MATH_GATE.json')
            elif control=='pdf_bytes': mutate(br/'dd.pdf')
            elif control=='extracted_text_bytes': mutate(br/'owr.txt')
            elif control=='render_bytes': mutate(br/'owr-p30.png')
            elif control=='exception_widen_rebound':
                m=json.loads((pk/'MANIFEST.json').read_text());m['excluded']['VERDICT.json']='exempt'
                dump(pk/'MANIFEST.json',m);mp=sha((pk/'MANIFEST.json').read_bytes())
            elif control=='duplicate_json_rebound':
                raw=(pk/'MANIFEST.json').read_text();(pk/'MANIFEST.json').write_text(raw[:-2]+',"pr":786}\n')
                mp=sha((pk/'MANIFEST.json').read_bytes())
            elif control=='unsafe_path_rebound':
                m=json.loads((pk/'MANIFEST.json').read_text());m['files']['../outside']={'bytes':0,'sha256':sha(b'')}
                dump(pk/'MANIFEST.json',m);mp=sha((pk/'MANIFEST.json').read_bytes())
            elif control=='novelty_flag_rebound':
                v=json.loads((pk/'VERDICT.json').read_text());v['novelty_certified']=True;dump(pk/'VERDICT.json',v);rebind()
            elif control=='peer_input_rebound':
                v=json.loads((pk/'PEER_PROVISIONAL_INPUT.json').read_text());v['target']['head']='0'*40
                dump(pk/'PEER_PROVISIONAL_INPUT.json',v);rebind()
            elif control=='frozen_plan_rebound': mutate(pk/'INDEPENDENT_PLAN.json');rebind()
            elif control=='query_ledger_rebound':
                v=json.loads((pk/'QUERY_LEDGER.json').read_text());v['queries'].pop();dump(pk/'QUERY_LEDGER.json',v);rebind()
            elif control=='input_symlink':
                victim=ir/'intake/SELECTED_PUBLIC_RECORD.json';target=case/'linked-input'
                shutil.copyfile(victim,target);victim.unlink();victim.symlink_to(target)
            elif control=='comparison_result_rebound':
                v=json.loads((pk/'COMPARISON_RESULTS.json').read_text());v['p3_I_4_1_dimension']=6
                dump(pk/'COMPARISON_RESULTS.json',v);rebind()
            elif control=='comparison_execution_rebound':
                (pk/'comparison_check.py').write_text("raise ValueError('deliberate test failure')\n");rebind()
            elif control=='nonfinite_json_rebound':
                raw=(pk/'MANIFEST.json').read_text();(pk/'MANIFEST.json').write_text(raw[:-2]+',"invalid":NaN}\n')
                mp=sha((pk/'MANIFEST.json').read_bytes())
            elif control=='boolean_byte_count_rebound':
                m=json.loads((pk/'MANIFEST.json').read_text());m['files']['VERDICT.json']['bytes']=True
                dump(pk/'MANIFEST.json',m);mp=sha((pk/'MANIFEST.json').read_bytes())
            elif control=='required_removed_rebound':
                (pk/'REPORT_PRE_PEER.md').unlink();m=json.loads((pk/'MANIFEST.json').read_text())
                del m['files']['REPORT_PRE_PEER.md'];dump(pk/'MANIFEST.json',m);mp=sha((pk/'MANIFEST.json').read_bytes())
            elif control=='unsafe_input_path_rebound':
                v=json.loads((pk/'INPUTS.json').read_text());row=v['files'].pop('intake/SELECTED_PUBLIC_RECORD.json')
                v['files']['../outside']=row;dump(pk/'INPUTS.json',v);rebind()
            else: raise ValueError('Unhandled control')
            bad=invoke(pk,ir,br,mp,cp)
            need(bad.returncode!=0,'Accepted negative control '+control+' mode'+str(mode))
            need('CUSTODY_FAIL:' in bad.stderr,'Negative control did not reach explicit custody failure: '+control)
            results.append({'mode':mode,'control':control,'rejected':True,'returncode':bad.returncode,
                            'failure':bad.stderr.strip()[:400]})
            shutil.rmtree(case)
    return {'status':'PASS','testing_manifest_sha256':manifest_pin,'testing_checker_sha256':checker_pin,
            'positive_cases':2,'negative_cases':len(controls)*2,'distinct_negative_controls':len(controls),
            'all_test_mutations_on_copies':True,'results':results,
            'scope':'Rebound cases deliberately supply a new external test pin to exercise internal semantics. Normal external pin remains mandatory. Receipt is added only after these tests; final manifest is a separate pin.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('packet','inputs-root','bodies-root'): ap.add_argument('--'+k,required=True)
    print(json.dumps(run(ap.parse_args()),indent=2,sort_keys=True))
