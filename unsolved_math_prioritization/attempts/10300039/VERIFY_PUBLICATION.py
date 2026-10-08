#!/usr/bin/env python3
"""Fail-closed source-free replay. Authenticate through externally pinned BOOTSTRAP.py."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, os, re, runpy, stat, subprocess, sys, tempfile, zipfile
EXPECTED_MANIFEST='339735f98a4a1a71b016282726360dd8f9ce62280e8716e29e01ae0484267404'
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
def safe(n): return type(n) is str and re.fullmatch('[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*',n) is not None and all(x not in ('.','..') for x in n.split('/'))
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
    need(m['schema']=='hyperbolic-separation-publication-manifest-v1','manifest version')
    for key,value in [('problem_id',10300039),('rank',1007),('disposition','unsolved'),('approaches',5)]:
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
            need(safe(i.filename) and not i.is_dir() and not(i.flag_bits&1),'unsafe archive path/encryption')
            mode=i.external_attr>>16;need(not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG),'archive type')
            need(i.file_size==len(expected[i.filename]) and z.read(i)==expected[i.filename],'archive member bytes')
    return len(expected)

def identity(b): return {'bytes':len(b),'sha256':sha(b)}
def bind_members(m,files):
    need(type(m) is dict and set(m)==set(files),'exact frozen file map')
    for n,x in m.items():
        need(safe(n) and type(x) is dict and set(x)=={'bytes','sha256'},'frozen identity schema')
        need(type(x['bytes']) is int and x['bytes']>=0 and type(x['sha256']) is str and re.fullmatch('[0-9a-f]{64}',x['sha256']) is not None,'frozen identity types')
        need(identity(files[n])==x,'frozen identity: '+n)
def semantics(f):
    pins={
        'archives/author_packet.zip':(45884,'df03afb408c6eb41c56a3a4a94faed0c6a90a08d890d9fd58ce568456de23b7b'),
        'AUTHOR_PACKET_EXTERNAL_MANIFEST.json':(3399,'4ddc7651c1da6facd2692d5b2cfa1291ad64dbf8765bfb69079372aa9c46684f'),
        'author_original/bootstrap.py':(5077,'fa007f533eedc28a8d62b0197777c5d6d8cc7c6323a02bf9c3ec0534cf9e1665'),
        'author_original/bundle/EXTERNAL_MANIFEST.json':(1832,'d179561ee1b36ae1d5fda2d8974a32ed23cd52f014fb98f08bbaf22e6b206c95'),
        'archives/independent_audit.zip':(25972,'20e48ae4879c095cc2fc45dd0cad2fc74cbc17e39876b5fd642788b00a2ba78d'),
        'AUDIT_EXTERNAL_MANIFEST.json':(1774,'b84e65c7d4a7621032248050f17f602d941dd2663aa266bbfe51edcf4604741a')}
    for n,pin in pins.items():need((len(f[n]),sha(f[n]))==pin,'accepted external pin: '+n)
    author={n.removeprefix('author_original/'):b for n,b in f.items() if n.startswith('author_original/')}
    audit={n.removeprefix('audit/'):b for n,b in f.items() if n.startswith('audit/')}
    ac=archive_members(f['archives/author_packet.zip'],author);rc=archive_members(f['archives/independent_audit.zip'],audit)
    need(ac==21 and rc==9,'complete frozen archive member counts')
    am=load(f['AUTHOR_PACKET_EXTERNAL_MANIFEST.json']);rm=load(f['AUDIT_EXTERNAL_MANIFEST.json'])
    bind_members(am['files'],author);bind_members(rm['files'],audit)
    need(type(am['packet_version']) is int and am['packet_version']==2,'accepted v2 required')
    need(type(am['problem_id']) is int and type(rm['problem_id']) is int and am['problem_id']==rm['problem_id']==10300039,'frozen target')
    need(am['packet']==identity(f['archives/author_packet.zip']) and rm['archive']==identity(f['archives/independent_audit.zip']),'external archive bindings')
    inner={n.removeprefix('bundle/author/'):b for n,b in author.items() if n.startswith('bundle/author/')}
    im=load(author['bundle/EXTERNAL_MANIFEST.json']);bind_members(im['files'],inner)
    need(im['archive']==identity(author['bundle/AUTHOR.zip']) and archive_members(author['bundle/AUTHOR.zip'],inner)==12,'inner author archive')
    a=load(audit['ACCEPTANCE.json'])
    for k,v in [('verdict','accept_corrected_v2_scoped_partials'),('status','unsolved'),('turns','5/5'),('problem_id',10300039),('rank',1007),('mathematical_routes_reviewed',5)]:
        need(type(a[k]) is type(v) and a[k]==v,'acceptance identity or scope: '+k)
    for k in ['Anosov_subclass_resolved','formal_proof_claim','full_solution_claim','human_review_claim','mathematical_correction_required','novelty_claim','source_complete_original_proof_audit','worldwide_current_openness_certified']:
        need(a[k] is False,'acceptance limit: '+k)
    need(a['patch'] is None and a['initial_freeze']=='superseded; not accepted or included','accepted corrected-v2 scope')
    need(a['author_packet']==dict(identity(f['archives/author_packet.zip']),files=21),'audit author packet pin')
    need(a['author_packet_manifest']==identity(f['AUTHOR_PACKET_EXTERNAL_MANIFEST.json']) and a['author_bootstrap']==identity(author['bootstrap.py']),'audit author trust pins')
    need(a['inner_author_archive']==identity(author['bundle/AUTHOR.zip']),'audit inner pin')
    need(rm['author_packet_sha256']==sha(f['archives/author_packet.zip']),'audit target archive')
    return {'author_archive_members':ac,'audit_archive_members':rc,'inner_author_members':12,'accepted_version':2,'accepted_author_and_audit_bytes_unchanged':True,'post_acceptance_correction':False,'audit_scope':a['verdict']}
def flags():return ['-I','-S','-B']+(['-'+'O'*sys.flags.optimize] if sys.flags.optimize else [])
def invoke(root,script,*args):
    # The preserved audit deliberately constructs a duplicate ZIP member as a rejection control.
    warning_flags=['-W','ignore:Duplicate name:UserWarning:zipfile'] if script=='audit/audit_replay.py' else []
    c=subprocess.run([sys.executable,*flags(),*warning_flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=600)
    need(c.returncode==0 and not c.stderr,'replay failed '+script+': '+c.stderr.decode('utf8','replace'))
    return load(c.stdout)
def freeze(root):
    for p in root.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
    root.chmod(0o555)
def thaw(root):
    root.chmod(0o755)
    for p in root.rglob('*'):p.chmod(0o755 if p.is_dir() else 0o644)
def denied_write(path,mode):
    try:
        with path.open(mode):pass
    except PermissionError:return True
    return False

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.research_results is None),'both complete corpus inputs required')
    need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10300039,**report}
    need(os.geteuid()!=0,'unprivileged execution required for genuine read-only controls')
    with tempfile.TemporaryDirectory(prefix='hyperbolic-separation-publication-') as tmp:
        work=Path(tmp)
        for n,b in before.items():q=work/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        freeze(work)
        try:
            need(denied_write(work/'WRITE_PROBE','xb') and denied_write(work/'author_original/bootstrap.py','r+b'),'actual read-only writes must be denied')
            args=[]
            if a.source_dir is not None:args+=['--sources',a.source_dir.absolute()]
            if a.problems is not None:args+=['--problems',a.problems.absolute(),'--reports',a.research_results.absolute()]
            replay=invoke(work,'author_original/bootstrap.py',*args)
            expected=load(before['author_original/bundle/author/CONTROL_OUTPUT.json'])
            primary={'sources':'NOT_RUN','corpora':'NOT_RUN'}
            if a.source_dir is not None:expected['source_binding']='all_five_private_pdf_identities_match';primary['sources']='PASS_CURRENT_REHASH'
            if a.problems is not None:expected['corpus_binding']='full_files_and_exact_target_records_match';primary['corpora']='PASS_CURRENT_REHASH'
            need(replay=={'accepted':True,'problem_id':10300039,'archive_sha256':'460994fabf6b31d69852a10a47e72db74590823043df6a0b0649a73c9b20ac44','result':expected},'author replay mismatch')
            controls=invoke(work,'author_original/controls.py')
            need(controls['positive_count']==6 and controls['negative_count']==51 and controls['frozen_source_unchanged'] is True and controls['modes']==['normal','-O','-OO'],'author controls mismatch')
            trusted=runpy.run_path(str(work/'audit/audit_replay.py'),run_name='authenticated_independent_audit')
            inventory_checked=trusted['check_distribution'](work/'author_original',work/'archives/author_packet.zip',work/'AUTHOR_PACKET_EXTERNAL_MANIFEST.json')
            need(len(inventory_checked)==21,'independent full author boundary')
            math=trusted['math_controls']();historical=load(before['audit/INDEPENDENT_REPLAY_normal.json'])
            need(math==historical['exact_math_controls'] and math['total']==2773,'independent finite diagnostics')
            independent_full={'status':'NOT_RUN','reason':'Full original independent external-binding audit requires supplied sources and both complete corpora; historical receipts are not current replay.'}
            if a.source_dir is not None and a.problems is not None:
                independent_full=invoke(work,'audit/audit_replay.py','--delivery',work/'author_original','--packet',work/'archives/author_packet.zip','--manifest',work/'AUTHOR_PACKET_EXTERNAL_MANIFEST.json','--problems',a.problems.absolute(),'--reports',a.research_results.absolute(),'--sources',a.source_dir.absolute())
                need(independent_full['accepted'] is True and independent_full['actual_final_readonly_enforced'] is True and independent_full['original_unchanged'] is True,'independent full replay status')
                need(independent_full['rejected_mutation_count']==60 and independent_full['exact_math_controls']==math,'independent full replay controls')
            report.update(author_replay=replay,author_controls=controls,independent_finite_replay=math,independent_full_external_replay=independent_full,current_primary_rehash=primary,genuine_read_only_write_denied=True)
            need(authenticate(work)==before,'temporary authenticated distribution changed')
        finally:thaw(work)
    need(authenticate(root)==before,'input bytes changed')
    return {'schema':'hyperbolic-separation-publication-replay-v1','status':'PASS_SCOPED_PUBLICATION','problem_id':10300039,'rank':1007,'disposition':'unsolved','approaches':5,'full_solution':False,'formal_geometric_proof':False,'github_ci':False,'source_free_default':True,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError,zipfile.BadZipFile) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
