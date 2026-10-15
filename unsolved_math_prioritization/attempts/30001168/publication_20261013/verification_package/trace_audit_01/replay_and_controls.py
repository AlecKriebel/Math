#!/usr/bin/env python3
"""Read-only frozen-source replay; mutations confined to private_sources.

Exact semantic checks are additional to comparisons with stored JSON bytes.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from fractions import Fraction
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source'
PRIVATE=HERE/'private_sources'
EXPECTED=Fraction(1106714561,1700054750)


def demand(condition,message):
    if not condition:
        raise ValueError(message)


def run(args,optimized,cwd=PRIVATE,env=None):
    base=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
    return subprocess.run(base+args,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)


def author_semantics(d):
    demand(d['problem_id']==30001168 and d['dimension']==3 and d['cylinder_length']==10000,
           'author identity and finite dimensional witness')
    demand(d['round_uniform_upper_threshold']=='129/200' and
           d['cylinder_strict_lower_threshold']=='13/20' and d['strict_threshold_gap']=='1/200',
           'author exact threshold semantics')
    demand(Fraction(d['cylinder_rational_lower'])==EXPECTED and d['grid_cells']==100 and
           d['checks']==613 and d['round_grid_worst_interval']==['189/100','190/100'],
           'author result semantics')
    demand(d['round_grid_certified_upper_decimal']=='0.643380136594',
           'author displayed outward upper')


def audit_semantics(d):
    demand(d['problem_id']==30001168 and d['accepted'] is True and d['grid_cells']==200,
           'audit identity and grid')
    demand(d['round_all_time_threshold']=='129/200' and d['cylinder_strict_threshold']=='13/20' and
           Fraction(d['cylinder_rational_lower'])==EXPECTED, 'audit threshold semantics')


def review_semantics(d):
    demand(d['problem_id']==30001168 and d['accepted'] is True and d['cylinder_length']==10000,
           'review identity and witness')
    demand(d['round_threshold']=='129/200' and d['cylinder_threshold']=='13/20' and
           len(d['round_regions'])==4 and Fraction(d['cylinder_rational_lower'])==EXPECTED,
           'review exact threshold semantics')


def main():
    PRIVATE.mkdir(exist_ok=True)
    records=[]
    specs=[('author/certificate.py','author/RESULTS.json',author_semantics),
           ('audit/independent_certificate.py','audit/INDEPENDENT_RESULTS.json',audit_semantics),
           ('second_review/four_region_certificate.py','second_review/RESULTS.json',review_semantics)]
    for script,expected,semantics in specs:
        for optimized in (False,True):
            p=run([str(SOURCE/script)],optimized)
            demand(p.returncode==0 and not p.stderr,'certificate replay '+script+p.stderr)
            demand(p.stdout==(SOURCE/expected).read_text(),'exact expected output '+script)
            semantics(json.loads(p.stdout))
            records.append({'case':script,'optimized':optimized,'accepted':True,
                            'exact_expected_bytes':True,'semantic_checks':True,
                            'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()})
    for script in ['author/verify_bundle.py','audit/verify_audit.py','second_review/verify_review.py']:
        for optimized in (False,True):
            p=run([str(SOURCE/script)],optimized)
            demand(p.returncode==0 and not p.stderr,'wrapper replay '+script+p.stderr)
            d=json.loads(p.stdout)
            demand(d['verified'] is True and d['optimized']==optimized,'wrapper status semantics')
            records.append({'case':script,'optimized':optimized,'accepted':True,'semantic_checks':True})
    for optimized in (False,True):
        p=run([str(HERE/'check_trace_bounds.py')],optimized)
        demand(p.returncode==0 and not p.stderr,'independent certificate '+p.stderr)
        d=json.loads(p.stdout)
        demand(d['accepted'] is True and d['problem_id']==30001168 and d['dimension']==3 and
               d['round_stronger_uniform_threshold']=='321/500' and len(d['middle_intervals'])==6 and
               Fraction(d['cylinder_lower_exact'])==EXPECTED,'independent exact semantics')
        if not optimized:
            (HERE/'EXACT_RESULTS.json').write_text(p.stdout)
        else:
            demand(p.stdout==(HERE/'EXACT_RESULTS.json').read_text(),'independent -O exact output')
        records.append({'case':'check_trace_bounds.py','optimized':optimized,
                        'accepted':True,'exact_normal_optimized_bytes':True,'semantic_checks':True})
    # Run the supplied copied-payload control runner entirely within this folder.
    tmp=PRIVATE/'tmp'
    tmp.mkdir(exist_ok=True)
    env=dict(os.environ,TMPDIR=str(tmp))
    for optimized in (False,True):
        p=run([str(SOURCE/'audit/run_audit_controls.py')],optimized,env=env)
        demand(p.returncode==0 and not p.stderr,'original controls '+p.stderr)
        d=json.loads(p.stdout)
        demand(d['total']==34 and d['passes']==34 and d['accepted_baselines']==4 and
               d['expected_rejections']==30 and d['all_optimization_modes_checked'] is True,
               'original controls exact counts')
        demand(p.stdout==(SOURCE/'audit/CONTROL_RESULTS.json').read_text(),
               'original controls exact archived bytes')
        records.append({'case':'original 34 copied-payload controls','optimized':optimized,
                        'accepted':True,'exact_expected_bytes':True,'accepted_baselines':4,
                        'expected_rejections':30})
    # New independent semantic attacks on all four certificates, without stale hashes.
    attacks=[('author short cylinder',SOURCE/'author/certificate.py',
              "d['L']=100; d['calculate'].__globals__['L']=100; d['calculate']()",'finite-cylinder strict separation'),
             ('author too tight round',SOURCE/'author/certificate.py',
              "d['calculate'].__globals__['ROUND_BOUND']=Q(3,5); d['calculate']()",'round interval'),
             ('audit short cylinder',SOURCE/'audit/independent_certificate.py',
              "d['calculate'].__globals__['LENGTH']=100; d['calculate']()",'strict cylinder separation'),
             ('audit too tight round',SOURCE/'audit/independent_certificate.py',
              "d['calculate'].__globals__['ROUND_LIMIT']=Q(3,5); d['calculate']()",'round interval bound'),
             ('review short cylinder',SOURCE/'second_review/four_region_certificate.py',
              "d['calculate'](length=100)",'cylinder separation'),
             ('review too tight round',SOURCE/'second_review/four_region_certificate.py',
              "d['calculate'](limit=Q(16,25))",'round bound failed'),
             ('own short cylinder',HERE/'check_trace_bounds.py',
              "d['calculate'](length=100)",'cylinder strict threshold'),
             ('own too tight round',HERE/'check_trace_bounds.py',
              "d['calculate'](round_limit=Q(3,5))",'small-time bound')]
    for label,script,attack,error in attacks:
        for optimized in (False,True):
            code="import runpy; from fractions import Fraction as Q; d=runpy.run_path("+repr(str(script))+"); "+attack
            p=run(['-c',code],optimized)
            demand(p.returncode!=0 and error in p.stderr,'semantic attack did not reject '+label+p.stderr)
            records.append({'case':label,'optimized':optimized,'accepted':False,
                            'expected_rejection':error,'semantic_checks':True})
    # Boundary demonstration: inventory/hash/arithmetic alone cannot certify prose.
    with TemporaryDirectory(dir=PRIVATE,prefix='analytical scope control ') as td:
        root=Path(td)/'author'
        shutil.copytree(SOURCE/'author',root)
        proof=root/'PROOF.md'
        s=proof.read_text()
        anchor='Y₀ = Δ_g₀ + n(n−2)/4.'
        demand(s.count(anchor)==1,'unique analytic corruption anchor')
        proof.write_text(s.replace(anchor,'Y₀ = Δ_g₀ + n(n−2)/8.'))
        mp=root/'MANIFEST.json'; manifest=json.loads(mp.read_text())
        for row in manifest['files']:
            b=(root/row['path']).read_bytes()
            row['bytes']=len(b); row['sha256']=hashlib.sha256(b).hexdigest()
        mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
        for optimized in (False,True):
            p=run([str(SOURCE/'author/verify_bundle.py'),'--root',str(root)],optimized)
            demand(p.returncode==0 and not p.stderr,'expected arithmetic-only scope control')
            records.append({'case':'corrupted analytic prose with valid fresh manifest',
                            'optimized':optimized,'accepted':True,
                            'meaning':'Expected: package checks do not prove analytic prose; independently reviewed obligations are essential.'})
    report={'accepted':True,'cases':records,'case_count':len(records),
            'frozen_source_edited':False,'bytecode_writing_disabled':True,
            'mutation_directory':'private_sources only',
            'scope_boundary':'Arithmetic replay and hash integrity do not prove analytic lemmas.'}
    (HERE/'REPLAY_CONTROLS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'accepted':True,'case_count':len(records),
                      'independent_negative_cases':len(attacks)*2,
                      'original_control_runs':2,'scope_demonstrations':2},indent=2,sort_keys=True))


if __name__=='__main__':
    demand(len(sys.argv)==1,'No arguments accepted')
    main()
