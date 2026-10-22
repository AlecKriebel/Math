"""Reproduce bounded negative tests without editing the accepted packet."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(root):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    result = {'assertion_risk_probe':[], 'semantic_mutations':[], 'integrity_mutations':[]}
    with tempfile.TemporaryDirectory(prefix='ep642-negative-') as directory:
        temp = Path(directory)
        for candidate in ['author_original','corrected']:
            source = (root/candidate/'validation.py').read_text()
            old = 'sum(len(a[v])-4 for v in s)-boundary'
            require(source.count(old) == 1, 'boundary probe target mismatch')
            script = source.replace(old, 'sum(len(a[v])-5 for v in s)-boundary')
            for optimized in [False,True]:
                target = temp/(candidate+str(optimized)); target.mkdir()
                (target/'validation.py').write_text(script)
                cp = subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(target/'validation.py')],capture_output=True,text=True,cwd=temp,env=env,timeout=60)
                rejected = cp.returncode != 0
                require(rejected == (candidate == 'corrected' or not optimized), 'assertion probe unexpected')
                result['assertion_risk_probe'].append({'candidate':candidate,'optimized':optimized,'rejected':rejected,'reports_passed':'"passed": true' in cp.stdout})
        source = (root/'corrected/validation.py').read_text()
        mutations = [('strict_forbidden_inequality','if q >= len(c):','if q > len(c):'),
                     ('duplicate_cycle_orientations','and path[1] < path[-1]',''),
                     ('incorrect_degree_classification','all(len(a[v])==4 for v in s)','all(len(a[v])==3 for v in s)'),
                     ('omit_closing_edge','start in adj[last]','True'),
                     ('incorrect_chord_subtraction','q = induced-len(c)','q = induced-2*len(c)')]
        for name, old, new in mutations:
            require(source.count(old) == 1, 'semantic probe target mismatch')
            target = temp/name;target.mkdir();(target/'validation.py').write_text(source.replace(old,new))
            for optimized in [False,True]:
                cp = subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/'independent_checks.py'),str(target/'validation.py')],capture_output=True,text=True,cwd=temp,env=env,timeout=60)
                require(cp.returncode != 0, 'semantic mutation accepted: '+name)
                result['semantic_mutations'].append({'mutation':name,'optimized':optimized,'rejected':True})
        manifest_hash = hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()
        probes = ['changed_original_proof','missing_original_member','extra_member','changed_status',
                  'changed_acceptance','changed_corrected_results','changed_manifest','wrong_external_pin']
        for probe in probes:
            target = temp/probe;shutil.copytree(root,target)
            pin = manifest_hash
            if probe == 'changed_original_proof':
                with (target/'author_original/proof_note.md').open('a') as stream:stream.write('\nmutation\n')
            elif probe == 'missing_original_member':
                (target/'author_original/proof_note.md').unlink()
            elif probe == 'extra_member':
                (target/'unexpected.txt').write_text('extra')
            elif probe == 'changed_status':
                p=target/'author_original/status.json';d=json.loads(p.read_text());d['full_solution']=True;p.write_text(json.dumps(d))
            elif probe == 'changed_acceptance':
                p=target/'acceptance_report.json';d=json.loads(p.read_text());d['full_solution_accepted']=True;p.write_text(json.dumps(d))
            elif probe == 'changed_corrected_results':
                p=target/'corrected/validation_results.json';d=json.loads(p.read_text());d['eleven_vertex_example']['cycles']=75;p.write_text(json.dumps(d))
            elif probe == 'changed_manifest':
                with (target/'MANIFEST.json').open('a') as stream:stream.write(' ')
            elif probe == 'wrong_external_pin':
                pin='0'*64
            for optimized in [False,True]:
                cp=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/'verify_audit.py'),'--root',str(target),'--expected-manifest-sha256',pin,'--integrity-only'],capture_output=True,text=True,cwd=temp,env=env,timeout=60)
                require(cp.returncode != 0, 'integrity mutation accepted: '+probe)
                result['integrity_mutations'].append({'mutation':probe,'optimized':optimized,'rejected':True})
        # Reconstruct the derivative from the original with the exact public diff.
        target=temp/'patch_reconstruction';target.mkdir();shutil.copy2(root/'author_original/validation.py',target/'validation.py')
        cp=subprocess.run(['patch','-p1','-i',str(root/'validation_hardening.patch')],cwd=target,capture_output=True,text=True,timeout=60)
        require(cp.returncode == 0 and (target/'validation.py').read_bytes() == (root/'corrected/validation.py').read_bytes(), 'patch replay mismatch')
        result['patch_reconstructs_exact_derivative']=True
    result['passed']=True
    return result


if __name__ == '__main__':
    print(json.dumps(run(Path(__file__).resolve().parent),indent=2))
