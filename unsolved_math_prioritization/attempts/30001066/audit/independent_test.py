#!/usr/bin/env python3
"""Independent exact geometry, replay, relocation and adversarial inventory tests.

Input is the unchanged reconstructed author ZIP. This script never imports its
verifier. Author code is executed separately, in a disposable relocated copy.
The independent geometric oracle clips actual line/box intersection intervals.
All payloads used in corruption tests are synthetic.
"""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import warnings
import zipfile
import strict_inventory

AUTHOR_SHA = 'be4dabaf22028561681c76c353bd537d0b240cfd67d52aa7ed9531f435905034'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def clip_line(bounds, a, b):
    """Exact closed interval of z values for which (a+b*z,z) is in a box."""
    left, right = bounds[-1]
    for (low, high), intercept, slope in zip(bounds[:-1], a, b):
        if slope == 0:
            if not low <= intercept <= high:
                return None
            continue
        ends = sorted(((low - intercept) / slope, (high - intercept) / slope))
        left, right = max(left, ends[0]), min(right, ends[1])
        if left > right:
            return None
    return left, right


def independently_generate(d):
    k = d - 1
    bodies = []
    motions = []
    for j in range(k):
        for role in range(3):
            ident = 3*j + role
            bounds = [[Q(-1), Q(1)] for _ in range(k)]
            bounds[j] = [Q(-1), Q(0)] if role == 1 else [Q(0), Q(1)]
            bounds.append([Q(2*ident), Q(2*ident+1)])
            bodies.append(bounds)
            intercept, slope = {0: (-6*j-4, 1), 1: (1, 0), 2: (6*j+1, -1)}[role]
            a, b = [Q(0)]*k, [Q(0)]*k
            a[j], b[j] = Q(intercept), Q(slope)
            motions.append((ident, a, b, Q(1, 6*k+2)))
    return bodies, motions


def check_geometry(bodies, motions):
    k = len(bodies[0])-1
    n = len(bodies)
    require(n == 3*k and len(motions) == n, 'wrong family size')
    zeros = [Q(0)]*k
    for i, bounds in enumerate(bodies):
        require(all(low < high for low, high in bounds), 'non-full-dimensional body')
        require(clip_line(bounds, zeros, zeros) is not None, 'axis excluded')
        for other in bodies[:i]:
            require(other[-1][1] < bounds[-1][0] or bounds[-1][1] < other[-1][0],
                    'closed boxes lack strict slab separation')
    for j in range(k):
        three = bodies[3*j:3*j+3]
        require(three[0][-1][1] < three[1][-1][0] and three[1][-1][1] < three[2][-1][0],
                'unordered interpolation nodes')
        require(three[0][j][0] == three[1][j][1] == three[2][j][0] == 0,
                'missing alternating signs')
    continuum_hits = actual_clips = 0
    for missing, a, b, eps in motions:
        require(eps > 0 and (any(a) or any(b)), 'not a nonzero motion interval')
        for h, bounds in enumerate(bodies):
            for e in (eps, eps/2):
                got = clip_line(bounds, [e*x for x in a], [e*x for x in b])
                require((got is None) == (h == missing), 'actual intersection disagrees with deletion')
                actual_clips += 1
            if h == missing:
                j, role = divmod(h, 3)
                values = [a[j] + b[j]*t for t in bounds[-1]]
                require(min(values) > 0 if role == 1 else max(values) < 0,
                        'omitted box is not excluded on its entire slab')
                continue
            # This is a whole real interval certificate: both endpoints of an
            # affine epsilon trajectory lie in each closed convex coordinate interval.
            t = sum(bounds[-1], Q(0))/2
            for hcoord, (low, high) in enumerate(bounds[:-1]):
                end = eps*(a[hcoord] + b[hcoord]*t)
                require(low <= min(Q(0), end) <= max(Q(0), end) <= high,
                        'continuous epsilon segment leaves a retained box')
            continuum_hits += 1
    return {'dimension': k+1, 'boxes': n, 'whole_real_interval_hit_checks': continuum_hits,
            'actual_line_box_clips': actual_clips}


def execute(script, args=(), optimized=False, cwd=None, expect=True):
    cmd = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(script), *map(str, args)]
    result = subprocess.run(cmd, cwd=cwd, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                            text=True, capture_output=True)
    require((result.returncode == 0) == expect,
            'unexpected subprocess status: '+str(cmd)+' '+result.stdout+' '+result.stderr)
    return {'optimized': optimized, 'returncode': result.returncode,
            'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-archive', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    archive = args.author_archive.resolve()
    strict_inventory.validate_zip(archive, AUTHOR_SHA)
    raw_archive = archive.read_bytes()
    with zipfile.ZipFile(archive) as z:
        payload = {name: z.read(name) for name in z.namelist()}
    base = json.loads(payload['certificate.json'])
    frozen_bodies = [[tuple(map(Q, pair)) for pair in body['bounds']] for body in base['boxes']]
    frozen_motions = [(w['omitted'], list(map(Q,w['intercepts'])), list(map(Q,w['slopes'])),Q(w['epsilon_max']))
                      for w in base['deletion_witnesses']]
    geometry = [check_geometry(frozen_bodies, frozen_motions)]
    for d in [2,4,5,8,12,16,24,32]:
        geometry.append(check_geometry(*independently_generate(d)))
    # Closed endpoint contact and actual varying-z intersection guard against
    # replacing intersection by a fixed slab-center linear condition.
    unit = [(Q(0),Q(1)),(Q(0),Q(1))]
    require(clip_line(unit, [Q(-1)], [Q(1)]) == (Q(1),Q(1)), 'endpoint clipping failed')
    require(Q(-1) + Q(1)*Q(1,2) < 0, 'center counterexample failed')
    grid_passes = 0
    for coeffs in itertools.product(range(-2,3), repeat=4):
        a,b = [Q(x,100) for x in coeffs[:2]], [Q(x,100) for x in coeffs[2:]]
        hit_all = all(clip_line(bounds,a,b) is not None for bounds in frozen_bodies)
        require(hit_all == (not any(coeffs)), 'grid contradicts unique transversal')
        grid_passes += 1
    semantic = []
    def add(label, fn):
        obj = copy.deepcopy(base)
        fn(obj)
        semantic.append((label,json.dumps(obj)))
    add('wrong_classification',lambda o:o.update(classification='full_solution'))
    add('wrong_problem',lambda o:o.update(problem_id=30001067))
    add('wrong_size',lambda o:o.update(claimed_minimal_size=5))
    add('boolean_dimension',lambda o:o.update(dimension=True))
    add('zero_width_box',lambda o:o['boxes'][0]['bounds'].__setitem__(1,['0','0']))
    add('reversed_interval',lambda o:o['boxes'][0]['bounds'].__setitem__(1,['1','-1']))
    add('touching_closed_slabs',lambda o:o['boxes'][1]['bounds'][-1].__setitem__(0,'1'))
    add('overlapping_slabs',lambda o:o['boxes'][1]['bounds'][-1].__setitem__(0,'0'))
    add('lost_negative_middle',lambda o:o['boxes'][1]['bounds'].__setitem__(0,['0','1']))
    add('axis_excluded',lambda o:o['boxes'][0]['bounds'].__setitem__(1,['1','2']))
    add('incorrect_role',lambda o:o['boxes'][1].update(role=2))
    add('duplicate_id',lambda o:o['boxes'][1].update(id=0))
    add('wrong_coordinate',lambda o:o['boxes'][1].update(coordinate=1))
    add('missing_body',lambda o:o['boxes'].pop())
    add('missing_deletion',lambda o:o['deletion_witnesses'].pop())
    add('duplicate_deletion',lambda o:o['deletion_witnesses'][1].update(omitted=0))
    add('stationary_motion',lambda o:o['deletion_witnesses'][0].update(intercepts=['0','0'],slopes=['0','0']))
    add('reversed_motion',lambda o:o['deletion_witnesses'][0].update(slopes=['-1','0']))
    add('oversized_epsilon',lambda o:o['deletion_witnesses'][0].update(epsilon_max='99'))
    add('zero_epsilon',lambda o:o['deletion_witnesses'][0].update(epsilon_max='0'))
    add('negative_epsilon',lambda o:o['deletion_witnesses'][0].update(epsilon_max='-1'))
    add('omitted_hit',lambda o:o['deletion_witnesses'][0]['hits'][0].update(box=0))
    add('missing_hit',lambda o:o['deletion_witnesses'][0]['hits'].pop())
    add('outside_slab_hit',lambda o:o['deletion_witnesses'][0]['hits'][0].update(t='99'))
    add('float_geometry',lambda o:o['boxes'][0]['bounds'][0].__setitem__(0,0.0))
    add('noncanonical_rational',lambda o:o['deletion_witnesses'][0].update(epsilon_max='2/28'))
    add('unknown_field',lambda o:o.update(unverified=True))
    semantic += [('duplicate_json_key',json.dumps(base)[:-1]+',"dimension":3}'),
                 ('nonfinite_geometry',json.dumps(base).replace('"1/14"','NaN',1)),
                 ('malformed_json','{')]
    variants=[]
    obj=copy.deepcopy(base)
    obj['boxes'].reverse();obj['deletion_witnesses'].reverse()
    for w in obj['deletion_witnesses']:w['hits'].reverse()
    variants.append(('permuted_rows',obj))
    obj=copy.deepcopy(base)
    for w in obj['deletion_witnesses']:w['epsilon_max']='1/140'
    variants.append(('smaller_motion_interval',obj))
    obj=copy.deepcopy(base)
    for b in obj['boxes']:
        b['bounds'][-1]=[str(Q(t)+100) for t in b['bounds'][-1]]
    for w in obj['deletion_witnesses']:
        w['intercepts']=[str(Q(a)-100*Q(b)) for a,b in zip(w['intercepts'],w['slopes'])]
        for hit in w['hits']:hit['t']=str(Q(hit['t'])+100)
    variants.append(('translated_slabs',obj))
    obj=copy.deepcopy(base)
    for b in obj['boxes']:b['bounds'][-1]=[str(3*Q(t)) for t in b['bounds'][-1]]
    for w in obj['deletion_witnesses']:
        w['slopes']=[str(Q(b)/3) for b in w['slopes']]
        for hit in w['hits']:hit['t']=str(3*Q(hit['t']))
    variants.append(('rescaled_slabs',obj))
    replays=[];cache_hole=[];inventory_cases=[]
    with tempfile.TemporaryDirectory(prefix='isolated-independent-relocated-') as td:
        td=Path(td); packet=td/'a new relocated directory'; packet.mkdir()
        for name,content in payload.items():(packet/name).write_bytes(content)
        for optimized in (False,True):
            for name in ['verify_package.py','verify.py','test_verifier.py']:
                r=execute(packet/name,optimized=optimized,cwd=td)
                replays.append({'script':name,**r})
            for name,content in semantic:
                path=td/'mutation.json';path.write_text(content)
                execute(packet/'verify.py',[path],optimized,cwd=td,expect=False)
            for name,obj in variants:
                path=td/'valid_variant.json';path.write_text(json.dumps(obj))
                execute(packet/'verify.py',[path],optimized,cwd=td,expect=True)
            r=execute(packet/'verify.py',['--generated-dimension','64'],optimized,cwd=td)
            replays.append({'script':'verify.py --generated-dimension 64',**r})
        for name in ['unexpected-source.pdf','arbitrary.bin']:
            bad=packet/'__pycache__'/name;bad.parent.mkdir(exist_ok=True);bad.write_bytes(b'SYNTHETIC UNLISTED PAYLOAD')
            for optimized in (False,True):
                r=execute(packet/'verify_package.py',optimized=optimized,cwd=td)
                cache_hole.append({'synthetic_member':'__pycache__/'+name,**r})
                try:strict_inventory.validate_directory(packet)
                except ValueError:pass
                else:raise RuntimeError('strict inventory missed cache payload')
            bad.unlink()
        (packet/'__pycache__').rmdir()
        strict_inventory.validate_directory(packet)
        # Each archive mutation is independently rejected, without relying on
        # the frozen outer digest. That digest is checked separately above.
        def zip_case(label, modify):
            candidate=td/'bad.zip'
            entries=[(n,c) for n,c in payload.items()]
            comment=modify(entries)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',UserWarning)
                with zipfile.ZipFile(candidate,'w',zipfile.ZIP_DEFLATED) as z:
                    for n,c in entries:z.writestr(n,c)
                    if isinstance(comment,bytes):z.comment=comment
            try:strict_inventory.validate_zip(candidate)
            except (ValueError,KeyError,TypeError):inventory_cases.append(label)
            else:raise RuntimeError('strict inventory accepted '+label)
        zip_case('unlisted_root_pdf',lambda e:e.append(('unexpected.pdf',b'SYNTHETIC')))
        zip_case('unlisted_cache_pdf',lambda e:e.append(('__pycache__/unexpected.pdf',b'SYNTHETIC')))
        zip_case('unlisted_cache_pyc',lambda e:e.append(('__pycache__/verify.cpython-312.pyc',b'SYNTHETIC')))
        zip_case('nested_directory_member',lambda e:e.append(('nested/',b'')))
        zip_case('duplicate_member',lambda e:e.append(e[0]))
        zip_case('path_traversal',lambda e:e.append(('../escape',b'SYNTHETIC')))
        zip_case('absolute_member',lambda e:e.append(('/escape',b'SYNTHETIC')))
        zip_case('missing_member',lambda e:e.pop())
        zip_case('changed_payload',lambda e:e.__setitem__(1,(e[1][0],e[1][1]+b'corrupt')))
        zip_case('archive_comment',lambda e:b'SYNTHETIC UNLISTED COMMENT')
        def manifest_change(fn):
            def change(entries):
                i=next(i for i,(name,_) in enumerate(entries) if name=='MANIFEST.json')
                obj=json.loads(entries[i][1]);fn(obj)
                entries[i]=('MANIFEST.json',json.dumps(obj).encode())
            return change
        zip_case('unknown_manifest_key',manifest_change(lambda o:o.update(extra=True)))
        zip_case('wrong_manifest_identity',manifest_change(lambda o:o.update(version='not-this-freeze')))
        zip_case('boolean_manifest_size',manifest_change(lambda o:o['files'][0].update(bytes=True)))
        zip_case('incorrect_manifest_digest',manifest_change(lambda o:o['files'][0].update(sha256='0'*64)))
        zip_case('duplicate_manifest_row',manifest_change(lambda o:o['files'].__setitem__(1,o['files'][0])))
        zip_case('missing_manifest_row',manifest_change(lambda o:o['files'].pop()))
        (packet/'unexpected.txt').write_text('synthetic')
        try:strict_inventory.validate_directory(packet)
        except ValueError:inventory_cases.append('directory_unlisted_root')
        else:raise RuntimeError('unlisted root file accepted')
        (packet/'unexpected.txt').unlink()
        (packet/'README.md').unlink();(packet/'README.md').symlink_to(td/'mutation.json')
        try:strict_inventory.validate_directory(packet)
        except ValueError:inventory_cases.append('directory_symlink')
        else:raise RuntimeError('symlink accepted')
    output={'status':'PASS_WITH_CONFIRMED_ORIGINAL_INVENTORY_DEFECT',
            'author_archive':{'bytes':len(raw_archive),'sha256':hashlib.sha256(raw_archive).hexdigest()},
            'geometry':geometry,'varying_z_closed_endpoint_test':'PASS','rational_line_grid_cases':grid_passes,
            'semantic_mutations_rejected_per_mode':len(semantic),'semantic_mutation_names':[x[0] for x in semantic],
            'valid_generalized_variants_per_mode':[x[0] for x in variants],
            'author_replays':replays,'original_cache_bypass_reproductions':cache_hole,
            'strict_inventory_mutations_rejected':inventory_cases,
            'continuous_claim_basis':'Exact affine epsilon interval endpoints plus convexity; sampled clipping is supplemental.',
            'all_dimension_claim_basis':'Independent written affine interpolation and deletion proofs; finite tests are not a universal proof.',
            'scope':'Geometry/inventory suite only; full-corpus replay is a separate tool. No unrestricted finite h(d) result.'}
    if args.output:args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'independent_dimensions':[r['dimension'] for r in geometry],
                      'semantic_mutations_per_mode':len(semantic),'strict_inventory_mutations':len(inventory_cases),
                      'original_inventory_bypass_reproductions':len(cache_hole)},sort_keys=True))


if __name__=='__main__':main()
