#!/usr/bin/env python3
"""Fail-closed source-free replay. Authenticate through externally pinned BOOTSTRAP.py."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, os, re, stat, subprocess, sys, tempfile, zipfile
EXPECTED_MANIFEST='3474d1c09eba3021ee49ec3b3416ce35c66b84726c1fdb3c1be85264770d5261'
class Reject(Exception): pass
def need(c,m):
    if not c: raise Reject(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def nonfinite(x): raise Reject('nonfinite JSON constant')
def load(b): return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite)
def safe(n): return type(n) is str and n!='' and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def inventory(root):
    need(not root.is_symlink() and root.is_dir(),'root symlink or not directory')
    out={};dirs=set()
    def visit(d,prefix):
        for e in os.scandir(d):
            name=prefix+e.name;mode=e.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode),'symlink: '+name)
            if stat.S_ISDIR(mode): dirs.add(name);visit(Path(e.path),name+'/')
            else:
                need(stat.S_ISREG(mode),'nonregular member: '+name);out[name]=Path(e.path).read_bytes()
    visit(root,'');return out,dirs

def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest')
    raw=f['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'manifest external pin')
    m=load(raw);need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','approaches','files'},'manifest schema')
    need(m['schema']=='short-geodesics-publication-manifest-v1','manifest version')
    for key,value in [('problem_id',10300043),('rank',1008),('disposition','unsolved'),('approaches',5)]:
        need(type(m[key]) is type(value) and m[key]==value,'manifest identity or scope: '+key)
    need(type(m['files']) is list and m['files'],'manifest files')
    expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path']
        need(safe(n) and n not in expected,'unsafe or duplicate entry');expected.add(n)
        need(n in f,'missing: '+n)
        need(type(e['bytes']) is int and e['bytes']>=0 and len(f[n])==e['bytes'],'byte count: '+n)
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(f[n])==e['sha256'],'digest: '+n)
    need(set(f)==expected,'file inventory mismatch')
    need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
    need(f['VERIFY_PUBLICATION.py']==Path(__file__).read_bytes(),'different verifier copy')
    return f

def archive_members(b,expected):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist();need(len(names)==len(set(names)) and set(names)==set(expected),'archive inventory')
        for i in z.infolist():
            need(safe(i.filename) and not i.is_dir(),'unsafe archive path')
            mode=i.external_attr>>16;need(not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG),'archive type')
            need(z.read(i)==expected[i.filename],'archive member bytes')
    return len(expected)

def semantics(f):
    pins={'author_original/MANIFEST.json':(1648,'24e4e0b001028a38091b1293b490e36227fda8d2ee73f726ef316f2eb0fe4c96'),'author_original/bootstrap.py':(3752,'10efdf3b3290b84365e6cad3e84822f322aa5e7f6778e2551addb2ab9329076c'),'author_original/packet/PROOF.md':(21275,'e095f3cbfb4876a19d01be1558307267031c1eee4af08fcda8ace38e39077f5e'),'audit_original/MANIFEST.json':(1308,'63da4944baf6b34043972ea0b9cda30692890fba65be2973c22c5c0ed2638476'),'audit_original/bootstrap.py':(4809,'d93f2ef75ed287b9cd4b6818e57f59e58784cdae7da43c00b690f29d460e030d'),'archives/author_v1.zip':(24197,'b2d5c49b421e530bdf3863d12ddb753ff9884f4f217ed1c244120b9c38c70fe1'),'archives/audit_v1.zip':(24981,'aa8921a0e711366046db9c51737edece6217a610a936dfea615954cd0e59bbe6')}
    for n,pin in pins.items():need((len(f[n]),sha(f[n]))==pin,'original external pin: '+n)
    for prefix,archive,ziproot,count,extra in [('author_original/','archives/author_v1.zip','author_v1/',13,{'MANIFEST.json','bootstrap.py'}),('audit_original/','archives/audit_v1.zip','audit_v1/',10,{'MANIFEST.json','bootstrap.py'})]:
        members={n.removeprefix(prefix):b for n,b in f.items() if n.startswith(prefix)}
        need(archive_members(f[archive],{ziproot+n:b for n,b in members.items()})==count,'archive member count')
        m=load(members['MANIFEST.json']);need(type(m['problem_id']) is int and m['problem_id']==10300043,'original problem id')
        need(set(members)==set(m['files'])|extra,'original manifest inventory')
        for n,pin in m['files'].items():need(safe(n) and pin=={'bytes':len(members[n]),'sha256':sha(members[n])},'original member binding')
    a=load(f['audit_original/payload/ACCEPTANCE.json']);c=load(f['author_original/packet/CLAIMS.json'])
    need(a['disposition']=='ACCEPT_UNCHANGED_SCOPED_PARTIALS' and a['status']=='unsolved','acceptance disposition')
    for key in ['problem_id','rank','turns_budget','turns_used']:
        want={'problem_id':10300043,'rank':1008,'turns_budget':5,'turns_used':5}[key]
        need(type(a[key]) is int and a[key]==want and type(c[key]) is int and c[key]==want,'scope integer '+key)
    for key in ['correction_required','universal_isotopy_solution','universal_homotopy_solution','geodesic_counterexample','formal_verification','novelty_certified','all_external_source_proofs_certified','original_otal_proof_certified']:
        need(a[key] is False,'audit limit '+key)
    need(a['original_freeze_unchanged'] is True and a['complete_author_proof_read'] is True and a['mathematical_blockers_to_scoped_acceptance']==[],'acceptance unchanged')
    need(a['accepted_propositions']==['1.1','1.2','2.1','2.2','3.1','4.1','5.1'],'accepted propositions')
    need(c['independent_review']=='pending' and c['status']=='unsolved','historical author label')
    for key in ['universal_isotopy_solution','universal_homotopy_solution','geodesic_counterexample','formal_verification','novelty_claim']:need(c[key] is False,'author limit '+key)
    for key,name in [('author_archive','archives/author_v1.zip'),('author_manifest','author_original/MANIFEST.json'),('author_bootstrap','author_original/bootstrap.py'),('author_proof','author_original/packet/PROOF.md')]:need(a[key]=={'bytes':len(f[name]),'sha256':sha(f[name])},'acceptance pin '+key)
    return {'original_mathematics_unchanged':True,'post_freeze_correction':False,'author_archive_members':13,'audit_archive_members':10,'historical_author_review_label':'pending','audit_disposition':a['disposition']}

def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    c=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=600)
    need(c.returncode==0 and not c.stderr,'replay failed '+script+': '+c.stderr.decode('utf8','replace'))
    return load(c.stdout)

def regular(p):
    need(not p.is_symlink() and p.is_file() and stat.S_ISREG(p.stat().st_mode),'missing or nonregular optional input')
    return p.read_bytes()
def rehash(f,sources,corpora):
    report={'sources':'NOT_RUN','corpora':'NOT_RUN','contents_emitted':False,'mathematical_source_proofs_certified':False}
    if sources is not None:
        need(not sources.is_symlink() and sources.is_dir(),'invalid sources directory')
        pins=load(f['author_original/packet/SOURCE_PINS.json'])['sources'];matched=[]
        for p in pins:
            need(safe(p['filename']) and '/' not in p['filename'],'source filename')
            b=regular(sources/p['filename']);need((len(b),sha(b))==(p['bytes'],p['sha256']),'source pin '+p['filename']);matched.append(p['filename'])
        report['sources']='PASS_CURRENT_REHASH';report['source_files_matched']=matched
    if corpora is not None:
        need(not corpora.is_symlink() and corpora.is_dir(),'invalid corpora directory')
        binding=load(f['author_original/packet/CORPUS_BINDINGS.json']);loaded={}
        for p in binding['corpora']:
            need(safe(p['filename']) and '/' not in p['filename'],'corpus filename')
            b=regular(corpora/p['filename']);need((len(b),sha(b))==(p['bytes'],p['sha256']),'corpus pin '+p['filename']);v=load(b);need(len(v)==p['record_count'],'corpus count');loaded[p['filename']]=v
        found=[r for r in loaded['problems.json'] if type(r.get('id')) is int and r['id']==10300043];need(len(found)==1,'target multiplicity');p=found[0];r=loaded['research_results.json']['AMR-102-0043'];need(p['problem_number']=='AMR-102-0043','target code')
        for value,key in [(p,'selected_problem_sha256'),(r,'selected_research_sha256'),({'problem':p,'research':r},'selected_pair_sha256')]:
            need(sha(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==binding[key],'canonical selected binding')
        report['corpora']='PASS_CURRENT_REHASH';report['corpus_files_matched']=2;report['unique_selected_pair']=True
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--sources',type=Path);p.add_argument('--corpora',type=Path);a=p.parse_args()
    need(not a.integrity_only or (a.sources is None and a.corpora is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10300043,**report}
    primary=rehash(before,a.sources,a.corpora)
    with tempfile.TemporaryDirectory(prefix='short-geodesics-publication-') as tmp:
        work=Path(tmp)
        for n,b in before.items():q=work/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        author=invoke(work,'author_original/bootstrap.py')
        need(author['status']=='PASS_AUTHENTICATED_SOURCE_FREE_PACKET','author gate')
        controls=invoke(work,'author_original/controls.py')
        need(controls['status']=='PASS_FREEZE_CONTROLS' and controls['case_count']==84 and controls['source_unchanged'] is True and all(x['pass'] is True for x in controls['cases']),'current author controls')
        audit=invoke(work,'audit_original/bootstrap.py','--author-freeze',work/'author_original')
        need(audit['status']=='PASS_AUTHENTICATED_SCOPED_AUDIT' and audit['original_author_freeze_match'] is True and audit['full_tests_rerun_by_this_gate'] is False,'audit gate')
        # Load only authenticated source-free code; run its independent finite diagnostics.
        # The full historical 111-case suite requires source/corpus inputs and is not claimed here.
        runner=work/'run_independent_finite.py'
        runner.write_text('import json,runpy,sys\nn=runpy.run_path(sys.argv[1],run_name="authenticated_controls")\nprint(json.dumps(n["mathematically_scoped_controls"](),sort_keys=True))\n')
        finite=invoke(work,'run_independent_finite.py',work/'audit_original/payload/independent_controls.py')
        historic=load(before['audit_original/payload/INDEPENDENT_NORMAL.json'])
        need(finite==historic['finite_controls'],'independent finite diagnostics differ')
        report.update(author_gate=author,author_controls_current={'status':controls['status'],'case_count':84,'all_three_inner_modes':True},audit_gate=audit,independent_finite_current=finite,historical_independent_scenarios=111,historical_full_suite_rerun=False)
    need(authenticate(root)==before,'publication bytes changed')
    return {'schema':'short-geodesics-publication-replay-v1','status':'PASS_SCOPED_PUBLICATION','problem_id':10300043,'rank':1008,'disposition':'unsolved','approaches':5,'universal_threshold':False,'geodesic_counterexample':False,'formal_topological_proof':False,'github_ci':False,'source_free_default':True,'primary_rehash':primary,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError,zipfile.BadZipFile) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
