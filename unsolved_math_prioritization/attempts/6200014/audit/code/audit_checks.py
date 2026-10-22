#!/usr/bin/env python3
"""Independent finite controls and optional frozen-author replay, not formal topology."""
import argparse, hashlib, importlib.util, itertools, json, pathlib, shutil, stat, subprocess, sys, tempfile, zipfile
sys.dont_write_bytecode = True
AUTHOR_SHA = 'a7085468b08f93b8422c2764799a0712b806e2772292cbafe5514b38851fb5b9'
AUTHOR_SIZE = 14171
AUTHOR_MANIFEST_SHA = 'a06410f384f30791a067a97d639b0ec73eaf7df75334fcc4dd0cb896987b9b61'
AUTHOR_FILES = {'APPROACHES.md','IDENTITY.json','MANIFEST.json','PROOF.md','README.md','SOURCES.json','code/checks.py','results/checks.json','verify.py'}

def require(ok, text):
    if not ok: raise ValueError(text)

def digest(data): return hashlib.sha256(data).hexdigest()

def edge(a,b): return frozenset((a,b))

def square_oracle(vs, es):
    """Enumerate cyclic orders and explicitly require four sides and two nonedges."""
    found=set()
    for q in itertools.combinations(vs,4):
        a=q[0]
        for b,c,d in itertools.permutations(q[1:]):
            if all(edge(x,y) in es for x,y in [(a,b),(b,c),(c,d),(d,a)]) and edge(a,c) not in es and edge(b,d) not in es:
                found.add(tuple(q));break
    return found

def finite_controls(author=None):
    # Independent graph enumeration, not randomized sampling.
    count=0; square_free=0; triangle_free=0
    for n in range(6):
        vs=list(range(n));pairs=list(itertools.combinations(vs,2))
        for mask in range(1<<len(pairs)):
            es={edge(*p) for j,p in enumerate(pairs) if (mask>>j)&1}
            oracle=square_oracle(vs,es)
            tf=not any(all(edge(a,b) in es for a,b in itertools.combinations(q,2)) for q in itertools.combinations(vs,3))
            if author:
                require({tuple(q) for q in author.squares(vs,es)}==oracle,'square detector differs from cyclic-order oracle')
                require(author.flag_dimension_one(vs,es)==tf,'dimension-one flag test mismatch')
            count+=1;square_free+=not oracle;triangle_free+=tf
    # Icosahedral graph with two poles and two five-vertex rings.
    vs=list(range(12));es=set()
    for i in range(5):
        for a,b in [(0,1+i),(11,6+i),(1+i,1+(i+1)%5),(6+i,6+(i+1)%5),(1+i,6+i),(1+i,6+(i-1)%5)]:es.add(edge(a,b))
    faces=[q for q in itertools.combinations(vs,3) if all(edge(a,b) in es for a,b in itertools.combinations(q,2))]
    require(len(es)==30 and len(faces)==20,'icosahedron counts')
    require(not square_oracle(vs,es),'icosahedron has induced square')
    require(not any(all(edge(a,b) in es for a,b in itertools.combinations(q,2)) for q in itertools.combinations(vs,4)),'icosahedron has four-clique')
    for v in vs:
        ns={u for u in vs if edge(u,v) in es};require(len(ns)==5,'vertex link size')
        require(all(sum(edge(u,w) in es for w in ns if w!=u)==2 for u in ns),'vertex link is not pentagon')
    if author: require(not author.squares(vs,es),'author rejects admissible icosahedron')
    # C4 tests the forbidden no-square omission, C3 tests flag omission.
    e4={edge(i,(i+1)%4) for i in range(4)}
    require(square_oracle(range(4),e4)=={(0,1,2,3)},'C4 rejection failed')
    require(not square_oracle(range(4),e4|{edge(0,2)}),'diagonal rejection failed')
    return {'all_pass':True,'exhaustive_labeled_graphs_vertices_0_through_5':count,'square_free_graphs':square_free,'triangle_free_graphs':triangle_free,'icosahedron':{'vertices':12,'edges':30,'triangles':20,'euler_characteristic':2,'induced_squares':0,'vertex_links':'12 pentagons'},'square_with_diagonal_not_induced':True,'finite_only_not_topological_certification':True}

def rehash(root, name):
    p=root/'MANIFEST.json';m=json.loads(p.read_text());b=(root/name).read_bytes();m['files'][name]={'sha256':digest(b),'bytes':len(b)};p.write_text(json.dumps(m))

def mutate(root, case):
    p=root/'MANIFEST.json'
    if case=='missing_proof':(root/'PROOF.md').unlink()
    elif case=='changed_proof':
        p2=root/'PROOF.md';b=p2.read_bytes();p2.write_bytes(b'!'+b[1:])
    elif case=='extra_file':(root/'extra.txt').write_text('extra')
    elif case=='symlink':(root/'linked').symlink_to(root/'PROOF.md')
    elif case=='duplicate_manifest_key':p.write_text(p.read_text().replace('"schema_version": 1','"schema_version": 1, "schema_version": 1'))
    elif case=='wrong_size':
        m=json.loads(p.read_text());m['files']['PROOF.md']['bytes']+=1;p.write_text(json.dumps(m))
    elif case=='traversal_entry':
        m=json.loads(p.read_text());m['files']['../outside']={'bytes':0,'sha256':digest(b'')};p.write_text(json.dumps(m))
    elif case in {'no_square_removed','flag_removed','pl_strengthened','wrong_identity'}:
        q=root/'IDENTITY.json';j=json.loads(q.read_text())
        if case=='no_square_removed':j['scope']['no_induced_square']=False
        elif case=='flag_removed':j['scope']['flag']=False
        elif case=='pl_strengthened':j['scope']['PL_assumed_separately']=True
        else:j['id']=6200015
        q.write_text(json.dumps(j));rehash(root,'IDENTITY.json')
    elif case=='false_recorded_result':
        q=root/'results/checks.json';j=json.loads(q.read_text());j['cycle_cases'][0]['flag']=True;q.write_text(json.dumps(j));rehash(root,'results/checks.json')
    elif case=='broken_mathematical_control':
        q=root/'code/checks.py';s=q.read_text();require('flag == (m >= 4)' in s,'missing control mutation site');q.write_text(s.replace('flag == (m >= 4)','flag == (m >= 3)'));rehash(root,'code/checks.py')
    elif case=='forged_all_pass':
        # Rehash coherent altered results to show that rerunning actual controls is required.
        q=root/'results/checks.json';j=json.loads(q.read_text());j['all_controls_pass']=False;q.write_text(json.dumps(j));rehash(root,'results/checks.json')
    else:raise ValueError('unknown mutation')

def frozen_replay(path):
    data=path.read_bytes();require(len(data)==AUTHOR_SIZE and digest(data)==AUTHOR_SHA,'frozen author archive identity mismatch')
    with tempfile.TemporaryDirectory(prefix='boundary-audit-') as tmp:
        tmp=pathlib.Path(tmp);clean=tmp/'frozen';clean.mkdir()
        with zipfile.ZipFile(path) as z:
            names=z.namelist();require(len(names)==len(set(names)) and set(names)==AUTHOR_FILES,'unsafe author archive file set')
            for info in z.infolist():require(not stat.S_ISLNK(info.external_attr>>16),'archive symlink forbidden')
            require(digest(z.read('MANIFEST.json'))==AUTHOR_MANIFEST_SHA,'author manifest mismatch');z.extractall(clean)
        spec=importlib.util.spec_from_file_location('frozen_controls',clean/'code/checks.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        controls=finite_controls(module)
        cases=['clean','missing_proof','changed_proof','extra_file','symlink','duplicate_manifest_key','wrong_size','traversal_entry','no_square_removed','flag_removed','pl_strengthened','wrong_identity','false_recorded_result','broken_mathematical_control','forged_all_pass']
        results=[]
        for optimized in [False,True]:
            for case in cases:
                root=tmp/('case_'+str(optimized)+'_'+case);shutil.copytree(clean,root)
                if case!='clean':mutate(root,case)
                proc=subprocess.run([sys.executable,*(['-O'] if optimized else []),'-B',str(root/'verify.py')],cwd=tmp,capture_output=True,text=True)
                require((proc.returncode==0)==(case=='clean'),'unexpected replay outcome: '+case)
                results.append({'case':case,'optimized':optimized,'exit_code':proc.returncode,'expected_outcome_observed':True})
                shutil.rmtree(root)
        relocated=tmp/'unrelated folder'/'relocated';shutil.copytree(clean,relocated)
        for opt in [[],['-O']]:
            p=subprocess.run([sys.executable,*opt,'-B',str(relocated/'verify.py')],cwd='/',capture_output=True,text=True);require(p.returncode==0,'relocation failed: '+p.stderr)
        return {'author_archive_sha256':AUTHOR_SHA,'author_archive_bytes':AUTHOR_SIZE,'author_manifest_sha256':AUTHOR_MANIFEST_SHA,'all_pass':True,'independent_finite_controls':controls,'normal_and_optimized_cases':results,'relocated_normal_and_optimized_pass':True,'topological_theorems_formally_verified':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--author-archive',type=pathlib.Path);args=p.parse_args()
    print(json.dumps(frozen_replay(args.author_archive) if args.author_archive else finite_controls(),sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
