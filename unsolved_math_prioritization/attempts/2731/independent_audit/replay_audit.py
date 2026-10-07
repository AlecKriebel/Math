#!/usr/bin/env python3
"""Independent exact-input and finite-regression audit; not a global solver.

Usage: python replay_audit.py AUTHOR.zip AUTHOR_MANIFEST.json
Optional: --catalog FILE --problems FILE --reports FILE --source-dir DIR
Only metadata are printed. No network access is used. The optional source
inspection uses the Poppler pdfinfo and pdftotext commands; other checks use
only the Python standard library.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, ast, hashlib, importlib.util, itertools, json, random
import re, subprocess, sys, tempfile, zipfile

ARCHIVE = (16268, 'f213feeb58b23c4c98aafb865c5965751386aba27fc64981a9aa92bebf04eca2')
EXTERNAL = (1638, '7b71bde678bba64192812f49058f8cc91d46fa3bfd36f725bbcda86a1f7be4d8')
EXPECTED_OUTPUT = 'de669f167f692bb747f72409fa415539fab6226b0b526e98b5bbc79481648a62'
STREAMS = {
    'catalog.json': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems.json': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'research_results.json': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
}
PDFS = {
    'K3_author.pdf': (6578041, 'ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f'),
    'aim_workshop_summary.pdf': (96371, '02aebaf8acf36d227ce25409680d1b4d2a596da71eaa687e1be251f64c9ed2c1'),
    'Calvo_geometric_knot_spaces.pdf': (283124, '86d8840c9674caaa765f8bbca6da6beeb02093988e4ace8155d7e98208275959'),
    'hard_unknots_2607.28772.pdf': (543977, '26ad773510d757a23c559759ec72a6b1b36c0e3a164a6960bcdc746d8363926b'),
}
PAIR = 'eef75cf825610172fc68ed1c073143bb6d65a5ab572b5756affadd88bdd6cc6d'
STATEMENT = '9f0678048e8c8bc1ea0ff193d5821eeb6d3ba72c4851de391190f0fe2a2f337d'


def ensure(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(b, expected, label):
    ensure((len(b), sha(b)) == expected, label + ': byte/hash mismatch')
    return {'bytes': len(b), 'sha256': sha(b), 'match': True}


def bind_archive(archive, manifest):
    pin(archive, ARCHIVE, 'archive')
    pin(manifest, EXTERNAL, 'external manifest')
    m = json.loads(manifest)
    ensure((m['archive']['bytes'],m['archive']['sha256']) == ARCHIVE, 'manifest archive pin')
    import io
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        names = z.namelist()
        ensure(len(names) == len(set(names)) == 9, 'duplicate or missing ZIP member')
        expected = {x['path']:x for x in m['files']}
        prefix = 'equilateral_polygon_2731/'
        ensure(set(names) == {prefix+x for x in expected}, 'ZIP/member manifest mismatch')
        ensure(all(Path(x).name == x and not x.startswith('.') for x in expected), 'unsafe member path')
        members = {n:z.read(prefix+n) for n in expected}
    for name, b in members.items():
        row = expected[name]
        pin(b, (row['bytes'],row['sha256']), 'member '+name)
    inner = json.loads(members['MANIFEST.json'])
    ensure({x['path'] for x in inner['files']} == set(members)-{'MANIFEST.json'}, 'inner member set')
    for row in inner['files']:
        pin(members[row['path']], (row['bytes'],row['sha256']), 'inner '+row['path'])
    return members, m


def oracle(p,q,r,s):
    """Independent exact segment oracle using cross-product geometry."""
    sub=lambda a,b: tuple(x-y for x,y in zip(a,b))
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    cross=lambda a,b:(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    add=lambda a,b:tuple(x+y for x,y in zip(a,b))
    scale=lambda a,t:tuple(x*t for x in a)
    u,v,w=sub(q,p),sub(s,r),sub(r,p)
    n=cross(u,v)
    norm=dot(n,n)
    if norm:
        if dot(w,n): return None
        a=dot(cross(w,v),n)/norm
        b=dot(cross(w,u),n)/norm
        return ('point',add(p,scale(u,a))) if 0<=a<=1 and 0<=b<=1 else None
    if cross(w,u)!=(0,0,0):return None
    # Scalar projection on u avoids the author's coordinate-pivot implementation.
    uu=dot(u,u)
    x,y=dot(w,u)/uu,dot(sub(s,p),u)/uu
    lo,hi=max(Q(0),min(x,y)),min(Q(1),max(x,y))
    if lo>hi:return None
    if lo==hi:return ('point',add(p,scale(u,lo)))
    return ('overlap',)


def finite_replays(members):
    records=[]
    mutations = [
        ('circle_bound', 'c >= F(3, 5)', 'c >= F(4, 5)'),
        ('flattening_identity', 'expected = F(9, 25)', 'expected = F(8, 25)'),
        ('rotation', 'F(-2, 3), F(1, 3), F(2, 3)', 'F(2, 3), F(1, 3), F(2, 3)'),
        ('convex_orientation', "cross(e, sub(proj[j], proj[i]))[2] > 0", "cross(e, sub(proj[j], proj[i]))[2] < 0"),
        ('mixed_height_length', '{F(11, 12), F(2, 3)}', '{F(5, 6), F(2, 3)}'),
        ('unit_length', "all(q == 1 for q in length_squares(vertices))", "all(q == 2 for q in length_squares(vertices))"),
    ]
    with tempfile.TemporaryDirectory(prefix='polygon independent audit ') as tmp:
        root=Path(tmp)
        tree=root/'relocated packet with spaces'
        tree.mkdir()
        for n,b in members.items(): (tree/n).write_bytes(b)
        code=members['verify_examples.py'].decode()
        ensure(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(code))), 'removable assert found')
        for flag in ([],['-O']):
            cmd=[sys.executable,*flag,str(tree/'verify_examples.py')]
            r=subprocess.run(cmd,cwd=root,capture_output=True)
            ensure(r.returncode==0 and not r.stderr and r.stdout==members['EXACT_CHECKS.json'], 'relocated replay mismatch')
            bad=subprocess.run(cmd+['unexpected'],cwd=root,capture_output=True)
            ensure(bad.returncode!=0 and json.loads(bad.stderr)['result']=='FAIL','argument accepted')
            records.append({'mode':'optimized' if flag else 'normal','returncode':r.returncode,
                'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),
                'invalid_argument_returncode':bad.returncode,'invalid_argument_stderr_sha256':sha(bad.stderr)})
        spec=importlib.util.spec_from_file_location('audited_polygon_examples',tree/'verify_examples.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        points=[tuple(map(Q,x)) for x in itertools.product(range(-1,2),repeat=3)]
        segments=list(itertools.combinations(points,2))
        comparisons=0
        for i,(p,q) in enumerate(segments):
            for r,s in segments[i:]:
                want=oracle(p,q,r,s)
                ensure(module.intersection(p,q,r,s)==want,'independent intersection oracle mismatch')
                comparisons+=1
        rng=random.Random(2731)
        symmetry_comparisons=0
        for _ in range(1000):
            p,q=rng.choice(segments);r,s=rng.choice(segments)
            want=oracle(p,q,r,s)
            for args in [(q,p,r,s),(p,q,s,r),(r,s,p,q),(s,r,q,p)]:
                ensure(module.intersection(*args)==want,'intersection symmetry mismatch')
                symmetry_comparisons+=1
        mutation_runs=[]
        for name,old,new in mutations:
            ensure(code.count(old)==1,'mutation target not unique: '+name)
            path=root/(name+'.py');path.write_text(code.replace(old,new))
            for flag in ([],['-O']):
                r=subprocess.run([sys.executable,*flag,str(path)],cwd=root,capture_output=True)
                ensure(r.returncode!=0 and json.loads(r.stderr)['result']=='FAIL','mutation survived: '+name)
                mutation_runs.append({'mutation':name,'mode':'optimized' if flag else 'normal','returncode':r.returncode,
                                      'stderr_sha256':sha(r.stderr)})
        # Boundary tests not covered merely by the author's three invalid fixtures.
        malformed=[[],[(Q(0),)*3]*3,
            [points[0],points[1],points[2],points[0]],
            [(Q(0),Q(0),Q(0)),(Q(1),Q(0),Q(0)),(Q(0),Q(0),Q(0)),(Q(0),Q(1),Q(0))]]
        rejected=0
        for v in malformed:
            try:module.simple(v)
            except module.CheckFailure:rejected+=1
            else:raise ValueError('malformed polygon accepted')
    return {'relocated_replays':records,'segment_oracle_comparisons':comparisons,
            'segment_symmetry_comparisons':symmetry_comparisons,'additional_malformed_polygons_rejected':rejected,
            'checker_mutation_runs':mutation_runs,'assert_nodes':0}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive');p.add_argument('manifest')
    for x in ('catalog','problems','reports','source-dir'):p.add_argument('--'+x)
    args=p.parse_args()
    archive=Path(args.archive).read_bytes();manifest=Path(args.manifest).read_bytes()
    members,m=bind_archive(archive,manifest)
    out={'schema':1,'problem_id':2731,'result':'PASS','scope':'exact pins and finite regression checks; analytical audit is separate',
         'author_archive':pin(archive,ARCHIVE,'archive'),'author_external_manifest':pin(manifest,EXTERNAL,'manifest'),
         'member_count':len(members),'inner_manifest_member_count':8,'python_version':sys.version.split()[0]}
    out.update(finite_replays(members))
    tamper=[]
    for label,a,e in [('archive-byte-flip',bytes([archive[0]^1])+archive[1:],manifest),('manifest-byte-append',archive,manifest+b' ')]:
        try:bind_archive(a,e)
        except ValueError:tamper.append(label)
        else:raise ValueError('tampering accepted')
    out['pinned_input_mutations_rejected']=tamper
    opts=[args.catalog,args.problems,args.reports]
    if any(opts):
        ensure(all(opts),'all three corpus paths must be supplied together')
        data=[];out['full_stream_pins']=[]
        for name,path in zip(STREAMS,opts):
            b=Path(path).read_bytes();out['full_stream_pins'].append({'name':name,**pin(b,STREAMS[name],name)})
            data.append(json.loads(b))
        catalog,problems,reports=data
        records=[x for x in problems if str(x['id'])=='2731']
        cats=[x for x in catalog if str(x['id'])=='2731']
        ensure(len(records)==len(cats)==1,'exact ID not unique')
        record=records[0];cat=cats[0];report=reports.get(record['problem_number'],{})
        pair=sha(json.dumps([record,report],sort_keys=True).encode())
        statement=sha(record['statement'].encode())
        ensure(pair==PAIR==cat['review_hash'],'complete pair pin')
        ensure(statement==STATEMENT==cat['statement_hash'],'statement pin')
        ensure(report=={},'report not empty')
        ensure(cat['rank']==906 and record['problem_number']=='KP-1.72','identity mismatch')
        out['exact_record_verification']={'pair_sha256':pair,'statement_sha256':statement,'report_empty':True,'rank':906,
            'serialization':'json.dumps([complete_record, reports.get(problem_number,{})], sort_keys=True), Python defaults, UTF-8',
            'catalog_id_matches':1,'problem_id_matches':1}
    else:out['full_stream_pins']='not requested'
    if args.source_dir:
        out['source_pdf_pins']=[{'name':name,**pin((Path(args.source_dir)/name).read_bytes(),value,name)} for name,value in PDFS.items()]
        counts={}
        for name,expected in [('K3_author.pdf',436),('aim_workshop_summary.pdf',4),('Calvo_geometric_knot_spaces.pdf',23)]:
            info=subprocess.check_output(['pdfinfo',str(Path(args.source_dir)/name)]).decode()
            count=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
            ensure(count==expected,'source page count: '+name);counts[name]=count
        out['source_pdf_page_counts']=counts
        if args.problems:
            source=subprocess.check_output(['pdftotext','-layout','-f','67','-l','68',str(Path(args.source_dir)/'K3_author.pdf'),'-']).decode()
            statement_text=source.split('Problem 1.72 ',1)[1].split('Remarks.',1)[0].strip()
            normalize=lambda x:' '.join(re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',x).split())
            norm=normalize(statement_text)
            ensure(norm==normalize(record['statement']),'normalized primary statement mismatch')
            ensure('Proposed for K3 by: J. Cantarella' in source and 'Scribed by: D. Ruberman' in source,'proposer or scribe mismatch')
            out['normalized_primary_statement']={'match':True,'sha256':sha(norm.encode()),'printed_pages':[67,68],
                'normalization':'join word-internal line-end hyphenation, then collapse whitespace','proposer_and_scribe_match':True}
    else:out['source_pdf_pins']='not requested'
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'result':'FAIL','error':str(e)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
