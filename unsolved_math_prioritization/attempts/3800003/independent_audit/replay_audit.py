#!/usr/bin/env python3
"""Independent pinned-input audit replay. No source/corpus contents are emitted.

Run with Python -I -B, optionally -O, and six explicitly supplied input paths.
This executable is itself subject to the separately held audit-manifest anchor.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

AUTHOR_ZIP = ('DEGENERATE_POLYTOPE_3800003_AUTHOR_SAFE_FREEZE.zip', 12004, '1d82820c9e37d3d8118a8ddc5b2aa55bea0d0744b78b5594b85e23bb80e81f34')
AUTHOR_EXTERNAL = ('DEGENERATE_POLYTOPE_3800003_AUTHOR_EXTERNAL_MANIFEST.json', 3250, '0cdd8ad3ad85c08c3d5905f107d44627f6969a8a0e698feb65b873aa2758b9cb')
MEMBER_MANIFEST_SHA = '59c526e5013aec636862e5455400f056fc58b366222399f209174b4ff8c57481'
PAIR_SHA = '53c09f2d30d1c19a2cb903b1a75400bfcfe593074e64bd305035fb630a1c99c3'

def require(value, message):
    if not value:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def load(data):
    return json.loads(data, object_pairs_hook=unique)

def checked_bytes(path, size, digest, label):
    require(not path.is_symlink() and path.is_file(), label + ': not a regular non-symlink file')
    data = path.read_bytes()
    require(len(data) == size and sha(data) == digest, label + ': byte/hash mismatch')
    return data

def pinned_archive(data, external):
    z = zipfile.ZipFile(io.BytesIO(data))
    infos = z.infolist()
    require(len(infos) == len({x.filename for x in infos}), 'duplicate ZIP member')
    require({x.filename for x in infos} == set(external['members']), 'ZIP inventory mismatch')
    members = {}
    for info in infos:
        path = Path(info.filename)
        require(not path.is_absolute() and '..' not in path.parts and len(path.parts) == 1, 'unsafe ZIP path')
        require(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), 'nonregular ZIP member')
        content = z.read(info)
        pin = external['members'][info.filename]
        require(len(content) == pin['bytes'] and sha(content) == pin['sha256'], 'ZIP member pin mismatch')
        members[info.filename] = content
    require(sha(members['MANIFEST.json']) == MEMBER_MANIFEST_SHA, 'member manifest pin mismatch')
    manifest = load(members['MANIFEST.json'])
    require(set(manifest['files']) | {'MANIFEST.json'} == set(members), 'internal manifest inventory mismatch')
    for name, pin in manifest['files'].items():
        require(pin == external['members'][name], 'internal/external member pin mismatch')
    return members

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--author-zip', type=Path, required=True)
    ap.add_argument('--author-external', type=Path, required=True)
    ap.add_argument('--catalog', type=Path, required=True)
    ap.add_argument('--problems', type=Path, required=True)
    ap.add_argument('--reports', type=Path, required=True)
    ap.add_argument('--sources', type=Path, required=True)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    zb = checked_bytes(args.author_zip, *AUTHOR_ZIP[1:], 'author ZIP')
    eb = checked_bytes(args.author_external, *AUTHOR_EXTERNAL[1:], 'author external manifest')
    external = load(eb)
    require(external['archive'] == dict(zip(('filename','bytes','sha256'), AUTHOR_ZIP)), 'external ZIP pin mismatch')
    members = pinned_archive(zb, external)
    metadata = load(members['VERIFICATION_METADATA.json'])
    corpus_inputs = [args.catalog, args.problems, args.reports]
    corpus_bytes = [checked_bytes(p, pin['bytes'], pin['sha256'], 'complete corpus ' + pin['name'])
                    for p, pin in zip(corpus_inputs, metadata['complete_corpora'])]
    require(len(metadata['complete_corpora']) == 3, 'corpus pin count')
    catalog, problems, reports = map(load, corpus_bytes)
    c = [x for x in catalog if str(x.get('id')) == '3800003']
    p = [x for x in problems if str(x.get('id')) == '3800003']
    require(len(c) == len(p) == 1, 'ID uniqueness')
    record = p[0]
    report = reports.get(record['problem_number'], {})
    require(c[0]['rank'] == 927 and c[0]['problem_number'] == record['problem_number'] == 'AMR-037-0003', 'corpus identity')
    pair = json.dumps([record, report], sort_keys=True).encode()
    require(len(pair) == 3881 and sha(pair) == PAIR_SHA == c[0]['review_hash'], 'complete pair pin')
    require(sha(record['statement'].encode()) == metadata['statement_sha256'] == c[0]['statement_hash'], 'statement pin')
    require(report.get('classification') == 'OPEN-TRIAGE', 'inherited classification')
    sources = {}
    for pin in metadata['public_sources']:
        if 'sha256' in pin:
            sources[pin['filename']] = checked_bytes(args.sources / pin['filename'], pin['bytes'], pin['sha256'], 'public source ' + pin['filename'])
    require(len(sources) == 4, 'source count')
    del catalog, problems, reports, record, report, c, p
    cases = []
    with tempfile.TemporaryDirectory(prefix='facet-independent-relocation-') as td:
        temp = Path(td)
        root = temp / 'renamed packet'
        root.mkdir()
        for name, content in members.items():
            (root / name).write_bytes(content)
        inp = temp / 'renamed private inputs'
        inp.mkdir()
        for content, name in zip(corpus_bytes, ('a.json','b.json','c.json')):
            (inp / name).write_bytes(content)
        del corpus_bytes
        src = inp / 'public sources held privately'
        src.mkdir()
        for name, content in sources.items():
            (src / name).write_bytes(content)
        foreign = temp / 'unrelated cwd'
        foreign.mkdir()
        # This must never be imported by isolated subprocesses.
        (foreign / 'fractions.py').write_text("raise RuntimeError('cwd import poisoned')\n")
        (foreign / 'json.py').write_text("raise RuntimeError('cwd import poisoned')\n")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(foreign))
        def run(script, tail=(), optimized=False):
            return subprocess.run([sys.executable, '-I', '-B', *(['-O'] if optimized else []), str(script), *map(str, tail)], cwd=foreign, env=env, capture_output=True, text=True, timeout=120)
        def accept(label, script, tail, expected):
            out = []
            for optimized in (False, True):
                result = run(script, tail, optimized)
                require(result.returncode == 0 and result.stderr == '', label + ': unexpected success-process state')
                payload = load(result.stdout)
                require(payload == expected, label + ': unexpected result')
                out.append(result.stdout)
            require(out[0] == out[1], label + ': normal/optimized difference')
            cases.append({'case':label,'normal_and_optimized':'PASS','outputs_identical':True,'result':expected})
        def reject(label, script, tail, reason):
            for optimized in (False, True):
                result = run(script, tail, optimized)
                require(result.returncode == 1 and result.stdout == '', label + ': wrong rejection state')
                require(result.stderr.rstrip().splitlines()[-1] == 'ValueError: ' + reason, label + ': wrong rejection reason')
                require('Traceback (most recent call last):' in result.stderr, label + ': missing expected Python exception')
            cases.append({'case':label,'normal_and_optimized':'REJECTED','exception':'ValueError','reason':reason})
        math_expected = load(members['CHECK_RESULTS.json'])['math_normal_and_optimized']
        source_expected = load(members['CHECK_RESULTS.json'])['source_normal_and_optimized']
        packet_expected = {'result':'PASS','files_verified':11,'external_manifest_anchor_verified':True,'scope':'Integrity only; this checker does not establish mathematical correctness.'}
        source_tail = ['--catalog',inp/'a.json','--problems',inp/'b.json','--reports',inp/'c.json','--sources',src]
        accept('relocated_authentic_math', root/'check_math.py', [], math_expected)
        accept('relocated_authentic_sources', root/'verify_sources.py', source_tail, source_expected)
        accept('relocated_authentic_integrity', root/'verify_packet.py', ['--root',root,'--manifest-sha256',MEMBER_MANIFEST_SHA], packet_expected)
        for label in ('changed_proof','extra_file','missing_file','symlink_file','manifest_rebound','scope_rebound','forged_pass_script','metadata_rebound','duplicate_manifest_key'):
            mutant = temp / label
            shutil.copytree(root, mutant)
            reason = None
            if label == 'changed_proof':
                (mutant/'PROOF.md').write_bytes(members['PROOF.md'] + b'\nchanged\n'); reason='member mismatch: PROOF.md'
            elif label == 'extra_file':
                (mutant/'EXTRA.txt').write_text('extra'); reason='unexpected or missing package file'
            elif label == 'missing_file':
                (mutant/'STATUS.json').unlink(); reason='unexpected or missing package file'
            elif label == 'symlink_file':
                (mutant/'PROOF.md').unlink(); (mutant/'PROOF.md').symlink_to(root/'PROOF.md'); reason='symlink forbidden'
            elif label == 'forged_pass_script':
                (mutant/'check_math.py').write_text("print('PASS')\n"); reason='member mismatch: check_math.py'
            elif label == 'duplicate_manifest_key':
                old=members['MANIFEST.json'].decode();(mutant/'MANIFEST.json').write_text(old.replace('{','{"problem_id": 0,',1));reason='manifest differs from external anchor'
            else:
                mf = load(members['MANIFEST.json'])
                if label == 'scope_rebound':
                    st=load(members['STATUS.json']);st['full_extremal_problem_solved']=True
                    data=(json.dumps(st,sort_keys=True,indent=2)+'\n').encode();(mutant/'STATUS.json').write_bytes(data)
                    mf['files']['STATUS.json']={'bytes':len(data),'sha256':sha(data)}
                elif label == 'metadata_rebound':
                    m=load(members['VERIFICATION_METADATA.json']);m['complete_corpora'][0]['sha256']='0'*64
                    data=(json.dumps(m,sort_keys=True,indent=2)+'\n').encode();(mutant/'VERIFICATION_METADATA.json').write_bytes(data)
                    mf['files']['VERIFICATION_METADATA.json']={'bytes':len(data),'sha256':sha(data)}
                else:
                    mf['files']['PROOF.md']['sha256']='0'*64
                (mutant/'MANIFEST.json').write_text(json.dumps(mf,sort_keys=True,indent=2)+'\n');reason='manifest differs from external anchor'
            reject(label,root/'verify_packet.py',['--root',mutant,'--manifest-sha256',MEMBER_MANIFEST_SHA],reason)
        # Exercise scope gate separately with a deliberately changed anchor. This
        # is a diagnostic only; the changed artifact is not accepted/published.
        mutant=temp/'scope_rebound'
        reject('scope_gate_with_test_reanchor',root/'verify_packet.py',['--root',mutant,'--manifest-sha256',sha((mutant/'MANIFEST.json').read_bytes())],'scope escalation')
        for index,name in enumerate(('catalog.json','problems.json','research_results.json')):
            wrong=inp/('wrong_'+str(index)+'.json');wrong.write_text('[]\n')
            tail=source_tail[:];tail[2*index+1]=wrong
            reject('wrong_complete_'+name,root/'verify_sources.py',tail,'complete corpus mismatch: '+name)
        for name in sources:
            bad=temp/('bad_'+name.replace('.','_'));shutil.copytree(src,bad)
            (bad/name).write_bytes(sources[name]+b'\n')
            tail=source_tail[:];tail[-1]=bad
            reject('changed_source_'+name,root/'verify_sources.py',tail,'source mismatch: '+name)
        mutations=[
            ('wrong_cubical_count','c=(m-2)*2**(m-2)','c=(m-1)*2**(m-2)','Euler mismatch'),
            ('wrong_ridge_incidence','return [n,e,3*c,c]','return [n,e,4*c,c]','ridge-facet incidence mismatch'),
            ('wrong_threshold_witness','==[1024,5120,6144,2048]','==[1024,5120,6144,2047]','witness mismatch'),
            ('wrong_upper_coefficient','d<=n*(n-3)//4','d<=n*(n-3)//8','coarse upper bound'),
            ('wrong_regular_cells','b=(2*k-2)*l*l','b=(2*k-3)*l*l','regular-subdivision count mismatch')]
        for label,old,new,reason in mutations:
            text=members['check_math.py'].decode();require(text.count(old)==1,'mutation target not unique: '+label)
            script=temp/(label+'.py');script.write_text(text.replace(old,new))
            reject(label,script,[],reason)
        # Independent arithmetic in a fresh subprocess, without copying any of
        # the author's face-vector formula into the expected-value side.
        independent=temp/'independent_math.py'
        independent.write_text('''import importlib.util,json,sys\nspec=importlib.util.spec_from_file_location("audited_math",sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\ndef need(v,s):\n if not v: raise ValueError(s)\nfor dimension in range(4,101):\n vertices=1<<dimension\n edges=sum(vertices//2 for i in range(dimension))\n facets=(edges-vertices)//2\n expected=[vertices,edges,facets*6//2,facets]\n need(m.face_vector(dimension)==expected,"independent face vector")\n need(m.validate(dimension,expected)==facets,"independent validator")\n need((facets>=2*vertices)==(dimension>=10),"independent threshold")\nfor vertices in range(5,1001):\n edges=vertices*(vertices-1)//2\n tetrahedra=edges-vertices\n need(tetrahedra//2==vertices*(vertices-3)//4,"independent floor bound")\nprint(json.dumps({"result":"PASS","cubical_dimensions":97,"upper_bound_vertex_counts":996},sort_keys=True))\n''')
        accept('independent_extended_arithmetic',independent,[root/'check_math.py'],{'result':'PASS','cubical_dimensions':97,'upper_bound_vertex_counts':996})
        require(not list(root.rglob('__pycache__')), 'unexpected generated package file')
    result={'schema':'independent-facet-audit-replay-v1','problem_id':3800003,'problem_number':'AMR-037-0003','queue_rank':927,
            'author_archive':dict(zip(('filename','bytes','sha256'),AUTHOR_ZIP)),
            'author_external_manifest':dict(zip(('filename','bytes','sha256'),AUTHOR_EXTERNAL)),
            'whole_corpora_verified':metadata['complete_corpora'],
            'complete_pair':{'bytes':3881,'sha256':PAIR_SHA},
            'public_source_files_verified':[{k:pin[k] for k in ('filename','bytes','sha256','title','url')} for pin in metadata['public_sources'] if 'sha256' in pin],
            'author_files_verified':len(members),'source_contents_emitted':False,'isolated_python':True,
            'relocated_packet_and_all_inputs':True,'unrelated_poisoned_cwd':True,'normal_optimized_outputs_identical':True,
            'acceptance_cases':sum(x['normal_and_optimized']=='PASS' for x in cases),
            'rejection_cases':sum(x['normal_and_optimized']=='REJECTED' for x in cases),'cases':cases,
            'result':'PASS','scope':'Integrity, exact identity, arithmetic diagnostics and exact-reason corruption controls; mathematical correctness and source interpretation are reviewed separately.'}
    encoded=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded,end='')

if __name__ == '__main__':
    main()
