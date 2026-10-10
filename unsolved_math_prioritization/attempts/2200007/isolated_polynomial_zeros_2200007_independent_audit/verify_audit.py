#!/usr/bin/env python3
"""Pinned, isolated replay and adversarial checks for one credited prior example.

Usage: python3 -I -S -B verify_audit.py ORIGINAL_ZIP HARDENED_ZIP
Both archives must have the exact accepted bytes. No network is used.
"""
import ast
import hashlib
import itertools
import json
import os
from pathlib import Path
import py_compile
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    'original': (12522, '07d389bc5a1ad1af4debd4c854b0a81227d930bec6f1ae38065d6fdc4f87ce53', 'isolated_polynomial_zeros_2200007'),
    'hardened': (13302, '2ddf71b86de99d5eb79724fad089a47479ecf58a8536fc2af080dab6416b0dbd', 'isolated_polynomial_zeros_2200007_hardened'),
}
NAMES = {'MANIFEST.json', 'README.md', 'RESEARCH_LOG.json', 'SCOPE_BRIDGE.md',
         'SOURCE_METADATA.json', 'STATUS.json', 'certificate_results.json',
         'verify_certificate.py', 'verify_package.py'}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin_extract(path, destination, kind):
    data = path.read_bytes()
    size, sha, root = PINS[kind]
    need(len(data) == size and digest(data) == sha, kind + ' external archive pin')
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        need(len(members) == 9, 'archive count')
        need({i.filename for i in members} == {root + '/' + n for n in NAMES}, 'archive inventory')
        for info in members:
            need(stat.S_ISREG(info.external_attr >> 16), 'nonregular archive member')
            target = destination / Path(info.filename).name
            target.write_bytes(archive.read(info))
    manifest = json.loads((destination / 'MANIFEST.json').read_text())
    need(set(manifest['files']) == NAMES - {'MANIFEST.json'}, 'manifest inventory')
    for name, meta in manifest['files'].items():
        data = (destination / name).read_bytes()
        need(len(data) == meta['bytes'] and digest(data) == meta['sha256'], 'manifest pin: ' + name)


def rehash(directory, name):
    p = directory / 'MANIFEST.json'
    manifest = json.loads(p.read_text())
    data = (directory / name).read_bytes()
    manifest['files'][name] = {'bytes': len(data), 'sha256': digest(data)}
    p.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')


def independent_math():
    # Separate integer-polynomial representation: q_i = x_i^2 + a_i*t^2+b_i*t+c_i.
    abc = [(1, -8, 0), (-1, 1, 0), (-1, 3, -2), (-1, 5, -6),
           (-1, 7, -12), (-1, 9, -20), (-1, 11, -30),
           (-1, 13, -42), (-1, 15, -56)]
    all_points, slices, residual_checks = set(), [], 0
    for t in range(9):
        squares = [-(a*t*t+b*t+c) for a,b,c in abc]
        need(all(r >= 0 for r in squares), 'integer slice feasible')
        positive = [i for i,r in enumerate(squares) if r > 0]
        zero = [i for i,r in enumerate(squares) if r == 0]
        need(len(positive) == 7 and len(zero) == 2, 'exact slice degeneracy')
        count = 0
        for signs in itertools.product((-1,1), repeat=len(positive)):
            s = dict(zip(positive, signs))
            point = (t,) + tuple((s.get(i,0), squares[i]) for i in range(9))
            need(point not in all_points, 'point collision')
            all_points.add(point)
            for i,(a,b,c) in enumerate(abc):
                # The encoded real coordinate is sign*sqrt(r), so its square is r.
                sign, r = point[i+1]
                x_squared = sign*sign*r
                need(x_squared+a*t*t+b*t+c == 0, 'quadratic residual')
                residual_checks += 1
            count += 1
        need(count == 128, 'slice cardinality')
        slices.append({'t':t,'zeros':zero,'positive':len(positive),'points':count})
    need(len(all_points) == 1152 and len(all_points)>2**10,'strict disproof')
    # Exact identity check on the factors that exclude every open real cell.
    need(abc[0] == (1,-8,0), 'outer exclusion polynomial')
    for i in range(1,9):
        need(abc[i] == (-1,2*i-1,-i*(i-1)), 'unit interval factorization')
    # Every q_i has its own x_i^2 term, so P's x_0^4 coefficient is exactly 1.
    return {'variables':10,'quadratic_summands':9,'degree_exactly':4,
            'x0_fourth_power_coefficient':1,'slices':slices,'distinct_points':len(all_points),
            'all_nine_equation_residual_checks':residual_checks,'proposed_bound':2**10,
            'strict_excess':128,'all_real_t_exclusion':'factored sign proof; see AUDIT.md',
            'isolation':'finite exact zero set; see AUDIT.md'}


def run_suite(original_path, hardened_path):
    rows = []
    environment = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    with tempfile.TemporaryDirectory(prefix='sos-independent-') as temporary:
        work=Path(temporary)
        original=work/'original'; original.mkdir()
        hardened=work/'hardened'; hardened.mkdir()
        pin_extract(original_path, original, 'original')
        pin_extract(hardened_path, hardened, 'hardened')
        # Ensure the derivative has no unexplained file changes.
        changed=sorted(n for n in NAMES if (original/n).read_bytes() != (hardened/n).read_bytes())
        need(changed == ['MANIFEST.json','README.md','verify_package.py'],'derivative delta')
        counter=0
        def clone(base):
            nonlocal counter
            counter+=1
            p=work/('case'+str(counter)); shutil.copytree(base,p);return p
        def invoke(directory, mode=0, isolated=True, certificate=False, env=None):
            command=[sys.executable]
            if isolated:command+=['-I','-S']
            if mode:command+=['-'+'O'*mode]
            command+=['-B',str(directory/('verify_certificate.py' if certificate else 'verify_package.py'))]
            return subprocess.run(command,cwd='/',env=env or environment,capture_output=True,text=True,timeout=30)
        def record(kind,test,mode,result,expected):
            need(bool(result)==bool(expected),kind+': '+test+' mode '+str(mode))
            rows.append({'artifact':kind,'test':test,'optimization':mode,'result':'PASS' if expected else 'REJECTED_AS_EXPECTED'})
        for kind,base in [('original',original),('hardened',hardened)]:
            for script in ['verify_certificate.py','verify_package.py']:
                tree=ast.parse((base/script).read_text());need(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'assert-dependent script')
            for mode in (0,1,2):
                r=invoke(base,mode);record(kind,'relocated_isolated_package',mode,r.returncode==0,True)
                r=invoke(base,mode,certificate=True);record(kind,'direct_isolated_certificate',mode,r.returncode==0,True)
                need(json.loads(r.stdout)==json.loads((base/'certificate_results.json').read_text()),'direct exact output')
                for mutation in ['proof_bytes','forged_count','extra_file','missing_file','symlink',
                                 'wrong_target','source_insertion','verifier_bytes','bytecode_cache']:
                    d=clone(base)
                    if mutation=='proof_bytes':(d/'SCOPE_BRIDGE.md').write_text((d/'SCOPE_BRIDGE.md').read_text()+'\nchanged\n')
                    elif mutation=='forged_count':
                        p=d/'certificate_results.json';j=json.loads(p.read_text());j['distinct_real_zeros']=1024;p.write_text(json.dumps(j));rehash(d,p.name)
                    elif mutation=='extra_file':(d/'extra').write_text('synthetic')
                    elif mutation=='missing_file':(d/'README.md').unlink()
                    elif mutation=='symlink':p=d/'README.md';p.unlink();p.symlink_to(base/'README.md')
                    elif mutation=='wrong_target':
                        p=d/'STATUS.json';j=json.loads(p.read_text());j['problem_id']=2200006;p.write_text(json.dumps(j));rehash(d,p.name)
                    elif mutation=='source_insertion':(d/'third_party_source.tex').write_text('synthetic marker only')
                    elif mutation=='verifier_bytes':
                        p=d/'verify_package.py';p.write_text(p.read_text()+'\n')
                    elif mutation=='bytecode_cache':
                        (d/'__pycache__').mkdir();(d/'__pycache__'/'unused.pyc').write_bytes(b'synthetic cache marker')
                    r=invoke(d,mode);record(kind,mutation,mode,r.returncode==0,False)
                # Correctly rehashed child instrumentation observes its actual flags.
                d=clone(base);p=d/'verify_certificate.py'
                p.write_text('import sys\nif sys.flags.optimize != '+str(mode)+': raise RuntimeError("child optimization mismatch")\n'+p.read_text());rehash(d,p.name)
                r=invoke(d,mode)
                expected=kind=='hardened' or mode==0
                record(kind,'child_optimization_propagation',mode,r.returncode==0,expected)
            # Internal manifests alone do not authenticate additional members.
            d=clone(base);(d/'synthetic_extra.txt').write_text('synthetic marker only');rehash(d,'synthetic_extra.txt')
            r=invoke(d);record(kind,'rehashed_added_member',0,r.returncode==0,kind=='original')
            # PYTHONPATH startup executes before original verifier; -I -S excludes it.
            injection=work/(kind+'_injection');injection.mkdir();marker=work/(kind+'_site_marker')
            (injection/'sitecustomize.py').write_text('open('+repr(str(marker))+',"w").write("startup")\n')
            polluted=dict(environment,PYTHONPATH=str(injection))
            r=invoke(base,isolated=kind=='hardened',env=polluted)
            record(kind,'ambient_site_replay',0,r.returncode==0,True)
            need(marker.exists()==(kind=='original'),'site hook boundary')
            rows.append({'artifact':kind,'test':'ambient_site_hook_execution','optimization':0,
                         'result':'EXECUTED_BEFORE_CHECK' if marker.exists() else 'EXCLUDED'})
            # Sibling source and legacy bytecode import before original inventory.
            for cache in (False,True):
                d=clone(base);marker=work/(kind+('_pyc_marker' if cache else '_source_marker'))
                p=d/'json.py';p.write_text('open('+repr(str(marker))+',"w").write("shadow")\nraise RuntimeError("synthetic shadow")\n')
                if cache:
                    py_compile.compile(str(p),cfile=str(d/'json.pyc'),doraise=True);p.unlink()
                r=invoke(d,isolated=kind=='hardened')
                need(r.returncode!=0,'shadow should not pass')
                need(marker.exists()==(kind=='original'),'shadow import boundary')
                rows.append({'artifact':kind,'test':'sibling_legacy_bytecode' if cache else 'sibling_source_shadow',
                             'optimization':0,'result':'EXECUTED_BEFORE_CHECK' if marker.exists() else 'REJECTED_WITHOUT_EXECUTION'})
        # Original documented command remains reproducible in a clean environment.
        for mode in (0,1,2):
            r=invoke(original,mode,isolated=False)
            record('original','documented_clean_startup',mode,r.returncode==0,True)
        r=invoke(hardened,isolated=False)
        record('hardened','nonisolated_invocation',0,r.returncode==0,False)
        # -B creates no artifact __pycache__ entries during all valid replays.
        need({p.name for p in original.iterdir()}==NAMES,'original cache pollution')
        need({p.name for p in hardened.iterdir()}==NAMES,'hardened cache pollution')
    return rows


def main():
    need(sys.flags.isolated and sys.flags.no_site,'run audit with -I -S')
    need(len(sys.argv)==3,'supply original and hardened ZIP paths')
    math=independent_math()
    rows=run_suite(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
    result={'schema':1,'problem_id':2200007,'mathematical_status':'FALSE_BY_PRIOR_COUNTEREXAMPLE',
            'prior_creator':'DannyExperiments','new_research_approaches':0,'independent_math':math,
            'checks':rows,'check_count':len(rows),'network_used':False,
            'trust_boundary':'externally pinned bytes and trusted Python installation',
            'original_defects':['optimization not propagated','manifest inventory self-declared',
                                'unisolated startup admits ambient and sibling imports'],
            'hardened_disposition':'ACCEPTED_FOR_ISOLATED_REPLAY'}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
