#!/usr/bin/env python3
"""Fresh round-2 exact and offline integration checks. No live API or Git calls."""
from pathlib import Path
from fractions import Fraction as F
import argparse, copy, hashlib, importlib.util, json, math, os, shutil, subprocess, sys, types, zipfile

def need(c,m):
    if not c: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p):
    s=importlib.util.spec_from_file_location('r2_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def add(a,b): return [(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(max(len(a),len(b)))]
def sc(a,c): return [x*c for x in a]
def mul(a,b):
    ans=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): ans[i+j]+=x*y
    return ans
def pw(a,k):
    ans=[F(1)]
    for _ in range(k): ans=mul(ans,a)
    return ans
def integral(a,k=0): return sum((v/F(i+k+1) for i,v in enumerate(a)),F(0))
def kernel(m):
    # Imaginary part of (sqrt(1-t)+i sqrt(t))^(2m+1), divided by N sqrt(t).
    a=[F(0)]*(m+1);N=2*m+1
    for k in range(m+1):
        piece=[F(0)]*k+sc(pw([F(1),F(-1)],m-k),F((-1)**k*math.comb(N,2*k+1),N))
        a=add(a,piece)
    return a
def math_checks():
    beta=[]
    for n in range(1,6):
        for m in range(1,5):
            L=n+2;a=kernel(m);need(a[0]==1 and len(a)==m+1 and a[-1]!=0,'kernel degree')
            q=pw(a,2*L);z=n*integral(q,n-1);v=n*integral(q,n);h=F(1,(2*m+1)**2)
            need(z>0 and v>0 and v<=h*h**n*(1+2**(n+2)),'exact scalar numerator')
            need(z>=F(7,11)**(2*L)*h**n,'exact core lower consistency')
            beta.append({'dimension':n,'m':m,'normalizer':str(z),'first_moment_ratio':str(v/z)})
    laplace=0
    for j in range(17):
        rod=pw([F(-1),F(0),F(1)],j)
        for _ in range(j):rod=[(i+1)*rod[i+1] for i in range(len(rod)-1)]
        rod=sc(rod,F(1,2**j*math.factorial(j)));lap=[F(0)]*(j+1)
        for k in range(j//2+1):
            term=[F(0)]*(j-2*k)+sc(pw([F(1),F(0),F(-1)],k),F(math.comb(j,2*k)*(-1)**k*math.comb(2*k,k),4**k))
            lap=add(lap,term)
        need(rod==lap,'finite Laplace identity');laplace+=1
    def moment(a,b,c):return F(0) if a%2 or b%2 else F(4,(a+1)*(b+1)*(a+b+c+3))
    def ldl(M):
        M=copy.deepcopy(M); piv=[]
        for i in range(len(M)):
            p=M[i][i];need(p>0,'exact positive definite moment pencil');piv.append(p)
            for j in range(i+1,len(M)):
                for k in range(j,len(M)):M[k][j]=M[j][k]=M[j][k]-M[j][i]*M[k][i]/p
        return {'dimension':len(M),'minimum_pivot':str(min(piv))}
    matrices=[]
    for r in range(4):
        I=[(a,b,c) for a in range(r+1) for b in range(r+1-a) for c in range(r+1-a-b)]
        H=[[moment(*[x+y for x,y in zip(a,b)]) for b in I] for a in I]
        Z=[[moment(a[0]+b[0],a[1]+b[1],a[2]+b[2]+1) for b in I] for a in I]
        matrices.append({'r':r,'H':ldl(H),'Z':ldl(Z),'H_minus_Z':ldl([[x-y for x,y in zip(a,b)] for a,b in zip(H,Z)])})
    return {'beta_endpoint_measures':beta,'Rodrigues_Laplace_polynomial_identities':laplace,'exact_pyramid_PD_checks':matrices,'scope':'Finite exact checks only; universal geometry, trigonometric inequalities and all-order degree arguments were checked analytically.'}

def archive_checks(a,scratch):
    p=a/'publication';b=json.loads((p/'BUILD_RECEIPT.json').read_text());raw=(p/b['verification_zip']['path']).read_bytes();need(sha(raw)==b['verification_zip']['sha256'],'ZIP outside SHA')
    out=scratch/'extracted';out.mkdir(parents=True);runs=[]
    with zipfile.ZipFile(p/b['verification_zip']['path']) as z:
        names=z.namelist();need(len(names)==152 and len(set(names))==152,'unique archive inventory')
        for name in names:
            need(name and not name.startswith('/') and '..' not in Path(name).parts and '\\' not in name and Path(name).as_posix()==name,'unsafe member')
            d=out/name;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(z.read(name))
    args=[part for k,v in b['verification_anchors'].items() for part in ['--expected-'+k+'-sha256',v]]
    for flag in [[],['-O'],['-OO']]:
        r=subprocess.run([sys.executable,'-B',*flag,str(out/'verify.py'),*args],capture_output=True,text=True,timeout=180);need(r.returncode==0,r.stderr);v=json.loads(r.stdout);need(v['authenticated_members']==151,'portable member count');runs.append({'flags':flag,'result':v})
    cp=scratch/'rebuild/program/audits/pr1261_30003990';cp.mkdir(parents=True)
    for e in json.loads((a/'reviews/package_round2/INPUT_FREEZE.json').read_text())['files']:
        dst=cp/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a/e['path'],dst)
    r=subprocess.run([sys.executable,'-B',str(cp/'publication/build_package.py')],capture_output=True,text=True,timeout=180);need(r.returncode==0,r.stderr)
    need((cp/'publication'/b['verification_zip']['path']).read_bytes()==raw,'frozen152-member byte rebuild');need((cp/'publication'/b['pdf']['path']).read_bytes()==(p/b['pdf']['path']).read_bytes(),'PDF copy drift')
    return cp,{'archive_members':152,'verification_modes':runs,'frozen_release_exact_rebuild':True,'later_review_or_receipt_added_to_archive':False}

def strict_kit_checks(a,scratch):
    kit=load(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py'));co=load(a.parents[1]/'publication_coordinators/pr1261.py');co.install_exact_verifier(kit);kit.doi_status=lambda d:{'status':'offline'}
    manifest=(a/'publication/zenodo-deposit.json').resolve();meta,files=kit.load_manifest(manifest);results=[]
    for change in [None,*meta,'file_size','file_checksum','extra_file','wrong_id']:
        kit.STATE_DIR=scratch/('kit-'+str(change));place=kit.state_path(manifest,'production');kit.save_state(place,{'manifest':str(manifest),'environment':'production','id':9301261})
        dep={'id':9301261,'submitted':False,'metadata':copy.deepcopy(meta),'files':[{'filename':e['name'],'filesize':e['size'],'checksum':'md5:'+e['md5']} for e in files]};calls=[]
        if change in meta:dep['metadata'][change]=[] if isinstance(meta[change],list) else 'CORRUPTED'
        elif change=='file_size':dep['files'][0]['filesize']+=1
        elif change=='file_checksum':dep['files'][0]['checksum']='md5:'+'0'*32
        elif change=='extra_file':dep['files'].append({'filename':'extra','filesize':0,'checksum':'0'*32})
        elif change=='wrong_id':dep['id']+=1
        class Client:
            def get(self,i):need(i==9301261,'requested ID');calls.append('GET');return copy.deepcopy(dep)
            def publish(self,i):calls.append('POST publish');dep.update(submitted=True,doi='10.5281/zenodo.9301261')
        try:
            result=kit.run(types.SimpleNamespace(command='publish',manifest=manifest,sandbox=False,confirm_id=9301261),client=Client());need(change is None and result['state']=='published' and calls.count('POST publish')==1,'invalid POST')
        except kit.DepositError:need(change is not None and 'POST publish' not in calls,'failure after forbidden POST')
        results.append({'corruption':change,'calls':calls})
    # Exact normalization accepted by the generic verifier is refused by strict wrapper.
    plain=copy.deepcopy(meta);plain['description']='Offline A & B';dep['metadata']=copy.deepcopy(plain);dep['metadata']['description']='Offline A &amp; B';dep['files']=[{'filename':f['name'],'filesize':f['size'],'checksum':f['md5']} for f in files]
    try:kit.verify(dep,plain,files)
    except kit.DepositError:pass
    else:raise RuntimeError('F01 normalization accepted')
    return {'actual_11_field_metadata_and_two_artifacts':True,'actual_shared_run_with_mock_client':True,'cases':results,'F01_entity_normalization_rejected':True}

def postmerge_checks(a,cp,scratch):
    pub=cp/'publication';u=load(pub/'update_pr_publication.py');t=load(pub/'append_tracker.py');b=json.loads((pub/'BUILD_RECEIPT.json').read_text());title=json.loads((pub/'zenodo-deposit.json').read_text())['metadata']['title']
    publication={'environment':'production','id':9301261,'state':'published','metadata_normalizations':[],'doi':'10.5281/zenodo.9301261','doi_url':'https://doi.org/10.5281/zenodo.9301261','record_url':'https://zenodo.org/records/9301261','title':title,'doi_resolution':{'status':'resolved','http_status':200}}
    save(pub/'PUBLICATION_RECEIPT.json',publication);save(pub/'FINAL_REVIEW_GATE.json',{'reviews':[{'status':'CLEAN','reviewer_id':'SYNTHETIC ONLY'}],'latest_review':{'status':'CLEAN'}})
    tracker={'spreadsheetId':t.SID,'gid':t.GID,'readback_verified':True,'updatedRange':"'Math Puzzles'!A2:D2",'row':t.expected_row(publication,title)};save(pub/'tracker/TRACKER_RECEIPT.json',tracker)
    save(pub/'PUBLIC_DOWNLOAD_VERIFICATION.json',{'all_supplied_metadata_exact':True,'public_record_identity_verified':True,'doi':publication['doi'],'id':publication['id']})
    files,_,note=u.desired_files(b,publication,tracker,json.loads((cp/'SUBMITTED_SNAPSHOT.json').read_text()));body=note+'\nThe seven-file PUBLIC_MANIFEST.json binds the six other current mathematical edition records. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata, publication receipt and README. Original historical files are preserved in the portable archive.\n';(pub/'PR_BODY_FINAL.md').write_text(body)
    head='a'*40;merge='b'*40;wanted=u.expected_identity(publication,tracker,files,body);save(pub/'PR_BRANCH_RECEIPT.json',{**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True})
    m=load(a.parents[1]/'publication_coordinators/verify_pr1261_merge.py');m.PROGRAM=cp.parents[1];m.A=cp;m.P=pub
    public_live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-17T22:00:00Z','body':body,'url':'https://github.com/AlecKriebel/Math/pull/1261'}
    fault={'name':None};events=[]
    def git(*args,data=None):
        events.append(args)
        if args[0]=='branch':return b'main\n'
        if args[0] in {'fetch','update-ref'}:return b''
        if args[0]=='diff-tree':return ('\n'.join(files)+'\n').encode()
        if args[0]=='rev-list':
            return ((head+' '+u.ORIGINAL if args[-1]==head else merge+' '+'c'*40+' '+('d'*40 if fault['name']=='merge_parent' else head))+'\n').encode()
        if args[0]=='show':return b'CORRUPTED' if fault['name']=='merged_blob' and args[1].startswith(merge) else files[args[1].split(':',1)[1]]
        raise RuntimeError('Unmocked Git operation '+repr(args))
    u.git=git;u.validate_workflow_gate=lambda gate:None # Real gate separately exercised by deployed regression; this fixture has no actual reviewer clearance.
    def row_call(parts,params,body=None):
        rows=[['Original Problem','Solution Chat URL','DOI','Notes'],copy.deepcopy(tracker['row'])]
        if fault['name']=='duplicate_row':rows.append(copy.deepcopy(rows[1]))
        if fault['name']=='column_B':rows[1][1]='unexpected'
        if fault['name']=='headers':rows[0][0]='wrong'
        return {'values':rows}
    t.call=row_call
    def path_run(path):
        name=Path(path).name
        if name=='update_pr_publication.py':return u.__dict__
        if name=='append_tracker.py':return t.__dict__
        raise RuntimeError('Unmocked script '+str(path))
    m.runpy=types.SimpleNamespace(run_path=path_run)
    def gh(*args,**kwargs):
        live=copy.deepcopy(public_live)
        if fault['name']=='head':live['headRefOid']='d'*40
        if fault['name']=='body':live['body']='outside body'
        return json.dumps(live)
    m.subprocess=types.SimpleNamespace(check_output=gh)
    baseline={'current_pr':1261,'completed_prs':[1205,1211,1216,1225,1241],'publications':[],'eligible_count':12}
    results=[]
    for name in [None,'head','body','merge_parent','merged_blob','duplicate_row','column_B','headers','unresolved_doi']:
        fault['name']=name;save(m.PROGRAM/'PROGRAM_STATE.json',baseline);d=copy.deepcopy(publication)
        if name=='unresolved_doi':d['doi_resolution']={'status':'unavailable'};save(pub/'DOI_INSPECT.json',d)
        save(pub/'PUBLICATION_RECEIPT.json',d)
        # Receipt hashes are regenerated for this synthetic fixture so each check reaches its intended boundary.
        ff,_,_=u.desired_files(b,d,tracker,json.loads((cp/'SUBMITTED_SNAPSHOT.json').read_text()));files=ff
        save(pub/'PR_BRANCH_RECEIPT.json',{**u.expected_identity(d,tracker,files,body),'commit':head,'body_readback_verified':True,'remote_readback_verified':True})
        try:m.main();need(name is None,'fault accepted')
        except RuntimeError:
            need(name is not None,'valid postmerge fixture failed');need(json.loads((m.PROGRAM/'PROGRAM_STATE.json').read_text())==baseline,'program advanced despite failed postmerge boundary')
        else:need(json.loads((m.PROGRAM/'PROGRAM_STATE.json').read_text())['current_pr']==1262,'successful state did not advance')
        results.append({'case':name,'accepted':name is None,'advance_only_after_all_checks':True})
    return {'actual_postmerge_main_with_mocked_external_reads_and_Git':True,'real_gate_validation_separately_regressed':True,'cases':results,'no_real_services_or_refs':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audit',required=True,type=Path);ap.add_argument('--scratch',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);q=ap.parse_args();a=q.audit.resolve();s=q.scratch.resolve();s.mkdir(parents=True)
    cp,archive=archive_checks(a,s)
    result={'status':'PASS','mathematics':math_checks(),'archive':archive,'strict_publication':strict_kit_checks(a,s),'postmerge':postmerge_checks(a,cp,s)}
    save(q.output,result);print(json.dumps({'status':'PASS','output_sha256':sha(q.output.read_bytes())}))
if __name__=='__main__':main()
