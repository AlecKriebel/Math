#!/usr/bin/env python3
"""Independent finite checks and authenticated replay; no analytic certification.

The author ZIP is an input. Source PDFs and public corpora are optional private
inputs and are never copied into this audit. Uses only Python's standard library.
"""
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE_BYTES = 19789
ARCHIVE_SHA = '6f7d74f0cd6157fb207d846f7404d22de2b16d09b7e16fdf6f1c2a1a4faed0f6'
MANIFEST_SHA = 'cc3bcf24fd192eeaa676963370f8e360c0039d86a2ded951fbb80ab6240cd60f'
REVIEW_SHA = 'e97a8eb02f3fdd31ea65947bad980189b3b9f8923a4af6e46cc55c1c37817330'
AUTHOR_FILES = {'APPROACHES.md', 'PROOF.md', 'README.md', 'RESULTS.json',
                'SCOPE.json', 'SOURCE_VERIFICATION.json', 'verify_integrity.py',
                'verify_math.py', 'MANIFEST.json'}
PDF_NAMES = ['milnor.pdf','lyubich_peters.pdf','hedgehogs.pdf',
             'partially_hyperbolic.pdf','escaping2024.pdf','wandering.pdf','fatou_survey.pdf']


def demand(condition, label):
    if not condition:
        raise ValueError(label)


def no_duplicates(pairs):
    result = {}
    for k, v in pairs:
        demand(k not in result, 'duplicate JSON key')
        result[k] = v
    return result


def parse(text):
    return json.loads(text, object_pairs_hook=no_duplicates)


def digest(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as handle:
        for b in iter(lambda: handle.read(1048576), b''):
            size += len(b)
            h.update(b)
    return {'bytes': size, 'sha256': h.hexdigest()}


def check_audit_manifest():
    root=Path(__file__).resolve().parent
    allowed={'AUDIT.md','CORRECTIONS.md','PROVENANCE.json','README.md',
             'RESULTS.json','verify_audit.py'}
    m=parse((root/'AUDIT_MANIFEST.json').read_text())
    demand(set(m)=={'schema','algorithm','files'} and type(m['schema']) is int
           and m['schema']==1 and m['algorithm']=='sha256','audit manifest schema')
    demand(len(m['files'])==len(allowed),'audit payload count')
    demand({e.get('path') for e in m['files']}==allowed,'audit payload allowlist')
    demand({p.name for p in root.iterdir()}==allowed|{'AUDIT_MANIFEST.json'},'unexpected audit member')
    for e in m['files']:
        demand(set(e)=={'path','bytes','sha256'},'audit entry schema')
        p=root/e['path']
        demand(p.is_file() and not p.is_symlink(),'audit file type')
        demand(digest(p)=={'bytes':e['bytes'],'sha256':e['sha256']},'audit payload identity')


@dataclass(frozen=True)
class QI:
    """Independent Gaussian-rational arithmetic representation."""
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', Fraction(self.a))
        object.__setattr__(self, 'b', Fraction(self.b))

    def __add__(self, other):
        other = other if isinstance(other, QI) else QI(other)
        return QI(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return QI(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, QI) else QI(-other))

    def __mul__(self, other):
        other = other if isinstance(other, QI) else QI(other)
        return QI(self.a*other.a-self.b*other.b, self.a*other.b+self.b*other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, QI) else QI(other)
        den = other.a*other.a+other.b*other.b
        return self * QI(other.a/den, -other.b/den)

    def norm_squared(self):
        return self.a*self.a+self.b*self.b


def independent_math():
    counts = Counter()
    def check(label, condition):
        demand(condition, label)
        counts[label] += 1
    zero, one = QI(), QI(1)
    F = Fraction
    ls = [QI(1),QI(-1),QI(0,1),QI(0,-1),QI(F(3,5),F(4,5)),
          QI(F(5,13),F(12,13)),QI(2),QI(F(1,2)),QI(-2)]
    ms = [QI(F(1,2)),QI(F(1,8)),QI(F(1,32)),QI(F(-1,3)),QI(0,F(1,4))]
    points = [(QI(F(k,7), F(k-3,11)),QI(F(2-k,5),F(k,13))) for k in range(-3,4)]
    for l in ls:
        for m in ms:
            trace, delta = l+m, l*m
            def H(point):
                x,y = point
                return (x*x+trace*x-delta*y,x)
            def I(point):
                x,y = point
                return (y,(y*y+trace*y-x)/delta)
            check('fixed_point', H((zero,zero)) == (zero,zero))
            for root in [l,m]:
                check('characteristic_polynomial', root*root-trace*root+delta == zero)
            for point in points:
                check('inverse_left', I(H(point)) == point)
                check('inverse_right', H(I(point)) == point)
                x,y = point
                # Exact central differences of this quadratic give its Jacobian.
                t = QI(F(1,17), F(2,19))
                hp, hm = H((x+t,y)), H((x-t,y))
                a,c = ((hp[i]-hm[i])/(2*t) for i in [0,1])
                hp, hm = H((x,y+t)), H((x,y-t))
                b,d = ((hp[i]-hm[i])/(2*t) for i in [0,1])
                check('jacobian_via_central_difference', (a,b,c,d)==(2*x+trace,-delta,one,zero))
                check('determinant_via_central_difference', a*d-b*c == delta)
                # Explicit product recurrence, independent of author matrix routine.
                A,B,C,D = one,zero,zero,one
                power = one
                for n in range(1,7):
                    factor=2*x+trace
                    A,B,C,D = factor*A-delta*C, factor*B-delta*D, A,B
                    power=power*delta
                    check('iterate_determinant', A*D-B*C == power)
                    x,y=H((x,y))
    l=QI(F(3,5),F(4,5))
    check('neutral_unit_modulus', l.norm_squared()==1)
    check('neutral_not_one', l!=one)
    check('neutral_rational_trace', l+one/l==QI(F(6,5)))
    check('neutral_trace_not_integer', F(6,5).denominator!=1)
    check('saddle_determinant_control', (QI(2)*QI(F(1,8))).norm_squared()<1)
    check('saddle_expanding_control', QI(2).norm_squared()>1)
    # Pythagorean samples at a different radius from the author checker.
    samples=0
    for x in range(-50,51):
        for y in range(-50,51):
            radius=isqrt(x*x+y*y)
            if radius*radius!=x*x+y*y:
                continue
            samples+=1
            value_squared=F(radius+x,2)
            check('threshold_nonnegative',value_squared>=0)
            check('threshold_zero_ray',(value_squared==0)==(y==0 and x<=0))
            for degree in range(2,21):
                scaled=F(degree*degree*(radius+x),2)
                check('threshold_scaling',scaled==degree*degree*value_squared)
    for degree in range(2,21):
        for denominator in range(1,8):
            for numerator in range(1,13):
                exponent=F(numerator,denominator)
                # lambda=d^(-exponent); log(d)/log(1/lambda)=1/exponent.
                check('strict_order_equivalence',(exponent>2)==(1/exponent<F(1,2)))
    # Exhaust all gap words of length four with values from 1..M.
    from itertools import product
    from bisect import bisect_right
    for M in range(1,7):
        for gaps in product(range(1,M+1),repeat=4):
            ns=[0]
            for g in gaps:
                ns.append(ns[-1]+g)
            for n in range(ns[-1]):
                j=bisect_right(ns,n)-1
                check('bounded_gap_exhaustive',0<=n-ns[j]<M)
    return {'status':'PASS','counts':dict(sorted(counts.items())),
            'assertions':sum(counts.values()),'parameter_pairs':len(ls)*len(ms),
            'pythagorean_samples':samples,'analytic_theorems_certified':False,
            'henon_counterexample_constructed':False}


def replay(root, optimized=False):
    cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/'verify_integrity.py')]
    result=subprocess.run(cmd,capture_output=True,text=True)
    return result


def rehash(root):
    manifest={'algorithm':'sha256','schema':1,'files':[]}
    for p in sorted(root.iterdir()):
        if p.name!='MANIFEST.json' and p.is_file():
            manifest['files'].append({'path':p.name,**digest(p)})
    (root/'MANIFEST.json').write_text(json.dumps(manifest))


def author_checks(archive, temp):
    demand(digest(archive)=={'bytes':ARCHIVE_BYTES,'sha256':ARCHIVE_SHA},'frozen author archive identity')
    root=temp/'original'
    root.mkdir()
    with zipfile.ZipFile(archive) as z:
        expected={'henon_boundary_5300080/'+n for n in AUTHOR_FILES}
        names=z.namelist()
        demand(len(names)==len(expected) and set(names)==expected,'archive exact members')
        for item in z.infolist():
            demand(not item.is_dir() and not stat.S_ISLNK(item.external_attr>>16),'archive file type')
            # Validated single-level names, written without extractall.
            (root/Path(item.filename).name).write_bytes(z.read(item))
    demand(digest(root/'MANIFEST.json')['sha256']==MANIFEST_SHA,'frozen manifest identity')
    manifest=parse((root/'MANIFEST.json').read_text())
    demand(len(manifest['files'])==8,'payload count')
    for entry in manifest['files']:
        demand({'bytes':entry['bytes'],'sha256':entry['sha256']}==digest(root/entry['path']),'independent payload hash')
    runs={}
    for label,opt in [('normal',False),('optimized',True)]:
        r=replay(root,opt)
        demand(r.returncode==0,'author '+label+' replay')
        runs[label]=parse(r.stdout)
        demand(runs[label]['math_assertions']==14006,'author arithmetic count')
    relocated=temp/'path with spaces'/'frozen release'
    shutil.copytree(root,relocated)
    r=replay(relocated,True)
    demand(r.returncode==0,'relocated replay')
    runs['relocated_optimized']=parse(r.stdout)
    mutations=['changed_byte','missing_file','extra_file','extra_directory','symlink',
               'duplicate_manifest_path','unsafe_manifest_path','duplicate_json_key',
               'unexpected_pdf_allowlisted','rehashed_scope_upgrade','rehashed_credit_upgrade',
               'rehashed_budget_change','rehashed_rank_change','rehashed_false_result']
    controls=[]
    for name in mutations:
        altered=temp/name
        shutil.copytree(root,altered)
        if name=='changed_byte':
            with (altered/'PROOF.md').open('a') as f:f.write('x')
        elif name=='missing_file':(altered/'PROOF.md').unlink()
        elif name=='extra_file':(altered/'unexpected.txt').write_text('x')
        elif name=='extra_directory':(altered/'unexpected').mkdir()
        elif name=='symlink':
            (altered/'PROOF.md').unlink()
            (altered/'PROOF.md').symlink_to(root/'PROOF.md')
        elif name in ['duplicate_manifest_path','unsafe_manifest_path']:
            m=parse((altered/'MANIFEST.json').read_text())
            if name=='duplicate_manifest_path':m['files'].append(m['files'][0])
            else:m['files'][0]['path']='../PROOF.md'
            (altered/'MANIFEST.json').write_text(json.dumps(m))
        elif name=='duplicate_json_key':
            p=altered/'MANIFEST.json'
            p.write_text(p.read_text().replace('"schema": 1','"schema": 1, "schema": 1'))
        elif name=='unexpected_pdf_allowlisted':
            (altered/'source.pdf').write_bytes(b'%PDF-INVALID')
            rehash(altered)
        elif name=='rehashed_false_result':
            p=altered/'RESULTS.json';o=parse(p.read_text());o['assertions']+=1
            p.write_text(json.dumps(o));rehash(altered)
        else:
            p=altered/'SCOPE.json';o=parse(p.read_text())
            k,v={'rehashed_scope_upgrade':('full_target_resolved',True),
                 'rehashed_credit_upgrade':('original_solution_credit',1),
                 'rehashed_budget_change':('substantive_approaches_used',4),
                 'rehashed_rank_change':('rank',792)}[name]
            o[k]=v;p.write_text(json.dumps(o));rehash(altered)
        r=replay(altered,True)
        demand(r.returncode!=0,'negative control was accepted: '+name)
        controls.append({'name':name,'rejected':True})
    return root,{'archive':{'bytes':ARCHIVE_BYTES,'sha256':ARCHIVE_SHA},
                 'manifest_sha256':MANIFEST_SHA,'archive_members':len(AUTHOR_FILES),
                 'replays':runs,'negative_controls':controls,
                 'frozen_author_modified':False}


def provenance_checks(args, root):
    source=parse((root/'SOURCE_VERIFICATION.json').read_text())
    out={}
    if args.source_dir:
        results=[]
        for name,record in zip(PDF_NAMES,source['sources']):
            path=args.source_dir/name
            actual=digest(path)
            demand(actual==record['pdf'],'PDF identity '+name)
            demand(path.open('rb').read(5)==b'%PDF-','PDF signature '+name)
            results.append({'title':record['title'],'url':record['url'],**actual})
        out['pdfs']=results
    paths=[args.problems,args.research,args.catalog]
    demand(not any(paths) or all(paths),'provide all three corpus/catalog inputs together')
    if all(paths):
        datasets={}
        for name,path in [('problems.json',args.problems),('research_results.json',args.research)]:
            m=digest(path)
            expected=source['dataset']['files'][name]
            demand(m=={k:expected[k] for k in ['bytes','sha256']},'corpus hash '+name)
            datasets[name]=m
        problems=parse(args.problems.read_text())
        reports=parse(args.research.read_text())
        catalog_bytes=args.catalog.read_bytes()
        catalog=parse(catalog_bytes.decode())
        selected=[p for p in problems if p['id']==5300080]
        demand(len(selected)==1,'problem ID uniqueness')
        problem=selected[0]
        code=problem['problem_number']
        demand(code=='AMR-052-0080','code identity')
        demand(sum(p['problem_number']==code for p in problems)==1,'problem code uniqueness')
        record=[p for p in catalog if p['id']=='5300080']
        demand(len(record)==1,'catalog ID uniqueness')
        record=record[0]
        statement_sha=hashlib.sha256(problem['statement'].encode()).hexdigest()
        review_sha=hashlib.sha256(json.dumps([problem,reports[code]],sort_keys=True).encode()).hexdigest()
        demand(statement_sha==record['statement_hash']==source['dataset']['selected_statement_sha256'],'statement identity')
        demand(review_sha==record['review_hash']==REVIEW_SHA,'recomputed review hash')
        demand(record['rank']==793,'catalog rank')
        gitblob=hashlib.sha1(b'blob '+str(len(catalog_bytes)).encode()+b'\0'+catalog_bytes).hexdigest()
        demand(gitblob==source['catalog']['git_blob_sha'],'catalog git object')
        demand(digest(args.catalog)=={k:source['catalog'][k] for k in ['bytes','sha256']},'catalog SHA256')
        demand(len(problems)==15458,'problem record count')
        demand(reports[code]['classification']=='OPEN-TRIAGE','prior report classification')
        out.update({'corpora':datasets,'problem_records':len(problems),'selected_ID_count':1,
                    'selected_code_count':1,'statement_sha256':statement_sha,
                    'review_hash_recomputed':review_sha,'review_hash_matches':True,
                    'catalog':{**digest(args.catalog),'git_blob_sha':gitblob,'rank':record['rank']},
                    'prior_report_classification':'OPEN-TRIAGE'})
    return out


def main():
    check_audit_manifest()
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('author_zip',type=Path)
    p.add_argument('--source-dir',type=Path)
    p.add_argument('--problems',type=Path)
    p.add_argument('--research',type=Path)
    p.add_argument('--catalog',type=Path)
    args=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='henon_independent_') as temp:
        root,author=author_checks(args.author_zip,Path(temp))
        result={'status':'PASS_SCOPED_PARTIAL_RESULTS','problem_id':5300080,'rank':793,
                'disposition':'unsolved','substantive_approaches_used':5,'original_solution_credit':0,
                'author_checks':author,'independent_math':independent_math(),
                'provenance_checks':provenance_checks(args,root),
                'analytic_theorems_certified':False,'human_peer_review':False,
                'exhaustive_literature_search':False,'remote_writes_performed':False}
        print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
