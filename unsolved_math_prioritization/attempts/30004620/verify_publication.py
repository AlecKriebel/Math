#!/usr/bin/env python3
"""Read-only portable integrity and exact replay; no network or source redistribution."""
import argparse, hashlib, json, os, stat, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FROZEN={'ABELIAN_SURFACE_CONE_30004620_AUTHOR_SAFE_FREEZE.zip': {'bytes': 17582, 'sha256': '43caecab347e51a96dfbed59f9f61cfc354aa89121c3f6be8aea0916e205274b'}, 'ABELIAN_SURFACE_CONE_30004620_INDEPENDENT_AUDIT.zip': {'bytes': 21456, 'sha256': 'dd3b58d72de9dace73bbe01f83174cf299b0474dba3549c70c6099d85f91f497'}, 'audit/AUDIT.md': {'bytes': 11179, 'sha256': 'b2f15513b68812fc4d6ef356ce267518224bf12613d0e89bb400212254038041'}, 'audit/AUDIT_MANIFEST.json': {'bytes': 1845, 'sha256': '711db4800576bce3bb8d685012e6b5f7a29e97ffeaddb32aad317e01fc955613'}, 'audit/AUDIT_STATUS.json': {'bytes': 1192, 'sha256': 'fc17383d9be1d712d69ece09385e9c0083cfebd893919ba52cfb62d715594994'}, 'audit/CORRECTIONS.md': {'bytes': 2755, 'sha256': '5b4245991def6a14fd3aaafc0cbce66b26a6114d69456df87fb0ad94d6fa56f7'}, 'audit/README.md': {'bytes': 1078, 'sha256': '85e9a37c24a57e519154f651c27c70f7cc681c62b4ec568fc309060bbe3dde76'}, 'audit/SOURCE_AUDIT.json': {'bytes': 8139, 'sha256': 'd3c7ffdf2841c170e0f423a41ccdf786297b3db5b673140b31ee945c4ebd1276'}, 'audit/evidence_results.json': {'bytes': 3109, 'sha256': '9fc28a7cb743a20db9a6f12a18edc01bf9510ee8604a46ac4feae85f61406019'}, 'audit/independent_results.json': {'bytes': 3859, 'sha256': '5650033d3c64963a74dcadceb507be42f4a3c3ba7465f70e21331d6b91c25249'}, 'audit/verify_evidence.py': {'bytes': 6152, 'sha256': 'a51ff1dad28d9501ff9613e9981e06d7623c4e37229bcca0c15cc369dee514aa'}, 'audit/verify_independently.py': {'bytes': 8686, 'sha256': 'bae092ac14814f9784428b9f004a17995605a3011d805f468a32be902ea88f36'}, 'author/APPROACHES.json': {'bytes': 1874, 'sha256': '87b9645a02ebe4af02129af9990335224b99d04894977d07902af57cb23cbc23'}, 'author/AUTHOR_MANIFEST.json': {'bytes': 1432, 'sha256': '6dbce0c54fee5c33b7cca0e2209959287afe38b3780f6dcb28eb43c48d934073'}, 'author/README.md': {'bytes': 1303, 'sha256': '68fec7d6707f5a6a18cc99dde863b2c033ffed6c9f5a0e9cc5b8ef5f8932efed'}, 'author/RESULT.md': {'bytes': 14046, 'sha256': 'f537ee870c88c5519c36472fc1205503b064c725cf72147ab3b980770792f8cc'}, 'author/SOURCES.md': {'bytes': 5428, 'sha256': '2f01539d85b127475a30d83c94d6a7ed7462820d54ca54a794e636c62289b6a5'}, 'author/provenance.json': {'bytes': 3727, 'sha256': 'b9fd129a8e18db3e5b45d58d3f2f86e84ce0ae0eca66714a2bac83645a6e1613'}, 'author/results.json': {'bytes': 3873, 'sha256': 'dcd09e217faca7f4535bb594b67179310d246d30b1bfd9f135256857f0579ae3'}, 'author/verify.py': {'bytes': 7861, 'sha256': '001d47d135270422cc53fdcbb329d6b6f3763ee10f37c43d5f71572815d588ef'}}
SCOPE={'actual_geometric_counterexample': False, 'closure_scope': 'Effective extremality and the effective contracted face are distinct from claims about the ambient pseudoeffective closure. Convex models are not realized surfaces.', 'editorial_acceptance': False, 'freeze_labels': 'Author audit-pending and audit no-remote-write labels are historical checkpoints, preserved unchanged. The wrapper records the later accepted scoped audit.', 'general_problem_solved': False, 'historical_novelty_certified': False, 'human_peer_review': False, 'independent_audit': 'PASS_SCOPED_RESULTS_WITH_PROVENANCE_ADDENDUM', 'localization_scope': 'The repaired F1/F2 criterion uses credited primary geometric localization; neither F1 nor F2 is proved nef.', 'mandatory_mathematical_edits': False, 'nef_product_scope': 'Four numerically nonzero nef divisor factors give an interior class. A numerically zero factor gives zero.', 'polar_discrepancy_scope': 'Inspected arXiv:2007.02995v2 only; publisher final full text uninspected. The numerical witness is not a geometric counterexample.', 'problem_id': 30004620, 'problem_number': 'OWR-4990375-013', 'rank': 782, 'review_sha256': 'b3f0019b864f0700a2943a882d9f11eef9e98dcee2299462ab55eabab2486fe9', 'source_typo': 'The audit records arXiv v2 Remark 9.2: 28L-3D = 3M-8L, not 3M-8D. The author uses the correct expression.', 'statement_sha256': '66d79ee91479b1e8c8ca329adeaca6e27a8a54ea1cafd98a6a35f905b578cff9', 'status': 'unsolved', 'turns': '5/5'}
ARCHIVES=[('ABELIAN_SURFACE_CONE_30004620_AUTHOR_SAFE_FREEZE.zip','author','AUTHOR_MANIFEST.json'),('ABELIAN_SURFACE_CONE_30004620_INDEPENDENT_AUDIT.zip','audit','AUDIT_MANIFEST.json')]
def require(ok,label):
    if not ok:raise RuntimeError('FAIL: '+label)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def integrity(root=ROOT):
    require(not root.is_symlink(),'root symlink')
    manifest=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
    entries=manifest['files'];require(isinstance(entries,dict),'manifest mapping')
    expected=set(entries)|{'PUBLICATION_MANIFEST.json'}
    require(all(not Path(n).is_absolute() and '..' not in Path(n).parts and Path(n).as_posix()==n for n in expected),'safe manifest paths')
    expected_dirs={str(p) for n in expected for p in Path(n).parents if str(p)!='.'}
    files,dirs=set(),set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink')
        n=p.relative_to(root).as_posix()
        if p.is_file():files.add(n)
        elif p.is_dir():dirs.add(n)
        else:require(False,'nonregular file')
    require(files==expected,'recursive file allowlist')
    require(dirs==expected_dirs,'recursive directory allowlist')
    for n,h in entries.items():require(pin((root/n).read_bytes())==h,'manifest payload '+n)
    for n,h in FROZEN.items():require(pin((root/n).read_bytes())==h,'frozen pin '+n)
    require(json.loads((root/'PUBLICATION.json').read_bytes())==SCOPE,'scoped status')
    for name,folder,mname in ARCHIVES:
        d=root/folder;frozen=json.loads((d/mname).read_bytes());rows=frozen['payload_files']
        members={r['path'] for r in rows}|{mname}
        require(len(rows)+1==len(members),'frozen duplicate paths')
        require({p.name for p in d.iterdir()}==members,'frozen exact directory inventory')
        for row in rows:
            require(Path(row['path']).name==row['path'],'flat frozen path')
            require(pin((d/row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')},'frozen manifest member')
        with zipfile.ZipFile(root/name) as z:
            infos=z.infolist();require(len(infos)==len(members) and {i.filename for i in infos}==members,'ZIP exact member allowlist')
            require(z.testzip() is None,'ZIP CRC')
            for i in infos:
                require(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16) and not i.flag_bits&1,'unsafe ZIP entry')
                require(z.read(i)==(d/i.filename).read_bytes(),'ZIP member byte equality')
    return len(files)
def run(path,*args,optimized=False):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    cmd=[sys.executable]+(['-O'] if optimized else [])+['-B',str(path),*map(str,args)]
    with tempfile.TemporaryDirectory(prefix='abelian-cone-replay-') as tmp:
        return subprocess.run(cmd,cwd=tmp,env=env,capture_output=True,timeout=300)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['catalog','problems','research','gh-pdf','vdg-pdf','owr-pdf','queue-code']:
        parser.add_argument('--'+key,type=Path,help='Optional external evidence input; PDFs and corpora are not part of this packet.')
    args=parser.parse_args();count=integrity()
    for script,expected,control,n in [('author/verify.py','author/results.json','assertions',8800),('audit/verify_independently.py','audit/independent_results.json','independent_assertions',20879)]:
        r=run(ROOT/script);require(r.returncode==0 and not r.stderr,'normal replay '+script)
        require(r.stdout==(ROOT/expected).read_bytes(),'replay byte equality '+script)
        require(json.loads(r.stdout)[control]==n,'exact control count')
        r=run(ROOT/script,optimized=True);require(r.returncode!=0 and b'without -O' in r.stderr,'direct optimized invocation rejected')
    required=['catalog','problems','research','gh_pdf','vdg_pdf','owr_pdf'];given=[getattr(args,k) for k in required]
    evidence='NOT_RUN_EXTERNAL_INPUTS_REQUIRED'
    if any(given) or args.queue_code:
        require(all(p and p.is_file() for p in given),'provide all six existing external evidence inputs')
        opts=['--archive',ROOT/ARCHIVES[0][0]]
        for k in required:opts+=['--'+k.replace('_','-'),getattr(args,k).resolve()]
        if args.queue_code:
            require(args.queue_code.is_file(),'queue code exists');opts+=['--queue-code',args.queue_code.resolve()]
        r=run(ROOT/'audit/verify_evidence.py',*opts);require(r.returncode==0 and not r.stderr,'external evidence replay')
        result=json.loads(r.stdout);require(result['status']=='PASS' and result['descriptor']['review_sha256']==SCOPE['review_sha256'],'external review hash')
        evidence='PASS_SUPPLIED_EXTERNAL_INPUTS'
    out={'status':'PASS','problem_id':30004620,'disposition':'UNSOLVED 5/5','packet_files':count,'frozen_files_and_archives':len(FROZEN),'author_assertions':8800,'independent_assertions':20879,'author_replay':'byte-identical','independent_replay':'byte-identical','original_optimized_invocations_rejected':2,'replay_children':'normal Python; PYTHONOPTIMIZE removed; assertions enabled','external_evidence_replay':evidence,'general_problem_solved':False,'actual_geometric_counterexample':False}
    b=(json.dumps(out,indent=2,sort_keys=True)+'\n').encode()
    if evidence=='NOT_RUN_EXTERNAL_INPUTS_REQUIRED':require(b==(ROOT/'VERIFICATION_RESULTS.json').read_bytes(),'publication expected output')
    sys.stdout.buffer.write(b)
if __name__=='__main__':main()
