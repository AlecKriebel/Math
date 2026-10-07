#!/usr/bin/env python3
"""Relocation and fail-closed integrity/scope controls, in both Python modes."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def rehash(root):
    path=root/'PUBLICATION_MANIFEST.json';m=json.loads(path.read_bytes())
    for row in m['files']:
        b=(root/row['path']).read_bytes();row['bytes']=len(b);row['sha256']=hashlib.sha256(b).hexdigest()
    path.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
def change_json(root,name,key,value):
    p=root/name;m=json.loads(p.read_bytes());m[key]=value;p.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n');rehash(root)
def run(root,flags,extra,work):
    return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'verify_publication.py'),*extra],cwd=work,capture_output=True,timeout=240)
def main():
    need(len(sys.argv)==1,'Unexpected argument')
    checks=[]
    with tempfile.TemporaryDirectory(prefix='polygon publication controls ') as temp:
        work=Path(temp);clean=work/'relocated publication with spaces';shutil.copytree(ROOT,clean)
        positives=[]
        for flags in ([],['-O']):
            r=run(clean,flags,[],work);need(r.returncode==0 and not r.stderr,'Relocated full replay failed')
            need(json.loads(r.stdout)['finite_replay']['status']=='PASS','Relocated finite replay missing')
            positives.append(r.stdout)
        need(positives[0]==positives[1],'Relocated wrapper modes disagree')
        mutations=[
          'author_archive_byte','audit_archive_byte','author_manifest_byte','audit_manifest_byte',
          'author_member_byte','audit_acceptance_byte','receipt_byte','missing_member',
          'extra_file','symlink','manifest_duplicate','manifest_missing_row',
          'metadata_claim_solution','metadata_claim_novelty','metadata_component_computation',
          'metadata_turn_count','metadata_findings_changed','unexpected_argument',
          'partial_corpus_options','partial_queue_options','integrity_with_source_inputs']
        for label in mutations:
            altered=work/label;shutil.copytree(ROOT,altered);extra=['--integrity-only']
            names={
              'author_archive_byte':'archives/equilateral_polygon_2731_author.zip',
              'audit_archive_byte':'archives/EQUILATERAL_POLYGON_2731_INDEPENDENT_AUDIT_SAFE.zip',
              'author_manifest_byte':'archives/AUTHOR_FREEZE_MANIFEST.json',
              'audit_manifest_byte':'archives/EQUILATERAL_POLYGON_2731_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json',
              'author_member_byte':'author_original/PROOF_AND_GAPS.md',
              'audit_acceptance_byte':'independent_audit/EXACT_ACCEPTANCE.json',
              'receipt_byte':'INDEPENDENT_AUDIT_RECEIPT.json'}
            if label in names:
                p=altered/names[label];p.write_bytes(p.read_bytes()+b' ');rehash(altered)
            elif label=='missing_member':(altered/'author_original/STATUS.json').unlink()
            elif label=='extra_file':(altered/'unlisted_payload.txt').write_text('negative-control sentinel\n')
            elif label=='symlink':
                p=altered/'author_original/STATUS.json';p.unlink();p.symlink_to(clean/'author_original/STATUS.json')
            elif label.startswith('manifest_'):
                p=altered/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_bytes())
                if label=='manifest_duplicate':m['files'].append(m['files'][0])
                else:m['files'].pop()
                p.write_text(json.dumps(m))
            elif label.startswith('metadata_'):
                key,value={'metadata_claim_solution':('full_solution_claimed',True),'metadata_claim_novelty':('novelty_claimed',True),'metadata_component_computation':('component_computation_executed',True),'metadata_turn_count':('turns_used',5),'metadata_findings_changed':('queue',{'allowed_cells':['Status','Turns','Findings'],'changed_cells':['Status','Turns','Findings']})}[label]
                change_json(altered,'PUBLICATION_METADATA.json',key,value)
            elif label=='unexpected_argument':extra+=['--not-a-valid-option']
            elif label=='partial_corpus_options':extra=['--catalog','unused']
            elif label=='partial_queue_options':extra+=['--queue-base','unused']
            elif label=='integrity_with_source_inputs':extra+=['--source-dir','unused']
            for flags in ([],['-O']):
                r=run(altered,flags,extra,work)
                need(r.returncode!=0 and not r.stdout and bool(r.stderr),'Negative control survived: '+label)
                checks.append({'control':label,'mode':'optimized' if flags else 'normal','returncode':r.returncode})
            shutil.rmtree(altered)
    print(json.dumps({'status':'PASS','relocated_full_wrapper_replays':2,'relocated_normal_optimized_identical':True,'negative_control_cases':len(mutations),'negative_control_runs_rejected':len(checks),'controls':checks,'scope':'Publication integrity/scope regression controls; underlying finite checks do not settle the global problem.'},sort_keys=True,indent=2))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'status':'FAIL','error':str(e)},sort_keys=True),file=sys.stderr);sys.exit(1)
