from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import sympy as sp
import mpmath as mp
import ast,types
out=Path(__file__).resolve().parent;b=out.parent
# Load only my own pure geometry definitions, avoiding the standalone receipt-writing main body.
mp.mp.dps=70
node=ast.parse((out/'independent_controls.py').read_text())
ns={'mp':mp,'jac':mp.ellipfun}
for item in node.body:
    if isinstance(item,ast.FunctionDef) and item.name in ('cross','area','calc'):
        exec(compile(ast.Module(body=[item],type_ignores=[]),str(out/'independent_controls.py'),'exec'),ns)
ic=types.SimpleNamespace(**ns)
alpha,beta,lam,W,U=sp.symbols('alpha beta lam W U',nonzero=True);D=alpha*beta;s=alpha+beta;L=D-s*lam;J=(alpha-lam)*(beta-lam)
Wprime=(lam*W+L)/(W-lam)
identities=[sp.factor(Wprime-lam-J/(W-lam)),sp.factor(L+lam*Wprime-J*W/(W-lam))]
C2=1-lam*U/D;z2=alpha-U
pair=((2*beta-U)*(alpha+z2*C2-2*z2)+U*(U-beta)*(1-C2))/(beta*(alpha*C2-z2))
identities.append(sp.factor(pair-(2-L*U/(D*(beta-lam)))))
R=(D*(3*beta-alpha)+lam*(alpha-beta)**2)/(2*D*(beta-lam))
identities.append(sp.factor(R-(2-s*L/(2*D*(beta-lam)))))
identities.append(sp.factor(R.subs(lam,D/s)-2))
assert identities==[0]*5
# Independent raw official-response reading and byte hashing, not prior comparison outputs.
native=json.loads((b/'root_priority_readonly/ZENODO_NATIVE_RECORD.json').read_text());dc=json.loads((b/'root_priority_readonly/DATACITE_RECORD.json').read_text())['data']['attributes']
assert native['status']=='published' and native['is_published'] and not native['is_draft']
assert native['access']['files']==native['access']['record']=='public' and not native['access']['embargo']['active']
assert native['pids']['doi']['identifier']==dc['doi']=='10.5281/zenodo.23079799'
entries=native['files']['entries'];files=[]
for key,local in [('main.pdf','external.pdf'),('arxiv_source.zip','external_source.zip'),('verification_report.md','external_verification.md')]:
    path=b/'competing_preprint_priority_adversary'/local;raw=path.read_bytes();e=entries[key];m=json.loads((b/'root_priority_readonly/zenodo_archive_actual'/f'{key}.metadata.json').read_text())
    md5=hashlib.md5(raw).hexdigest();sha=hashlib.sha256(raw).hexdigest()
    assert e['checksum']==m['checksum']=='md5:'+md5 and e['size']==m['size']==len(raw)
    assert e['id']==m['file_id'] and e['key']==m['key']==key and m['status']=='completed'
    assert not e['access']['hidden'] and not m['access']['hidden']
    files.append({'archive_key':key,'current_local_path':str(path),'bytes':len(raw),'current_md5':md5,'current_sha256':sha,'official_md5':m['checksum'],'created':m['created'],'updated':m['updated'],'file_id':m['file_id'],'version_id':m['version_id'],'status':m['status'],'direct_archived_body_sha256_verified':False})
parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
commits=[]
for name in ('our_github_first_commit.json','our_github_first_proof_commit.json','our_github_full_checkpoint_commit.json'):
    d=json.loads((b/'competing_preprint_priority_adversary'/name).read_text());commits.append({'sha':d['sha'],'author_utc':d['commit']['author']['date'],'committer_utc':d['commit']['committer']['date'],'time_type':'authored_commit','full_proof_added':any(e['filename'].endswith('/PROOF.md') and e['status']=='added' for e in d['files'])})
pr=json.loads((b/'competing_preprint_priority_adversary/our_github_pr261.json').read_text())
assert commits[1]['full_proof_added'] and not commits[0]['full_proof_added']
firstproof=json.loads((b/'competing_preprint_priority_adversary/our_github_first_proof_commit.json').read_text())
proofentry=next(e for e in firstproof['files'] if e['filename'].endswith('/PROOF.md'))
proofbody=('\n'.join(line[1:] for line in proofentry['patch'].splitlines() if line.startswith('+'))+'\n').encode()
assert proofbody==(b/'submitted/unsolved_math_prioritization/attempts/5100021/PROOF.md').read_bytes()
firstproofbinding={'added_lines':proofentry['additions'],'reconstructed_bytes':len(proofbody),'reconstructed_sha256':hashlib.sha256(proofbody).hexdigest(),'exact_original_submitted_body_match':True}
events={'native_created':native['created'],'native_updated':native['updated'],'datacite_registered':dc['registered'], **{k['archive_key']+'_created':k['created'] for k in files}}
ours={c['sha']:c['author_utc'] for c in commits};ours['PR261_service_created']=pr['created_at']
deltas={e:{o:str(parse(t)-parse(eventtime)) for o,t in ours.items()} for e,eventtime in events.items()}
assert all(parse(t)>parse(eventtime) for eventtime in events.values() for t in ours.values())
# External K/R factors independently checked against direct geometry, using my own functions.
checks=[]
for N,tau,kk in [(4,1,mp.mpf('.4')),(8,1,mp.mpf('.8')),(8,3,mp.mpf('.8')),(12,5,mp.mpf('.6'))]:
    K=mp.ellipk(kk*kk);v=2*K*tau/N;dn=lambda u:mp.ellipfun('dn',u,kk*kk);sn=lambda u:mp.ellipfun('sn',u,kk*kk);cn=lambda u:mp.ellipfun('cn',u,kk*kk)
    a=dn(v)/cn(v);bb=mp.sqrt(1-kk*kk)/cn(v);aa=a*a;be=bb*bb;la=aa-1;DD=aa*be;JJ=(aa-la)*(be-la)
    kfactor=mp.sqrt(JJ)*(be-la)/(be*be);rfactor=(DD*(3*be-aa)+la*(aa-be)**2)/(2*DD*(be-la))
    for phase in ('.13','.83'):
        w=mp.mpf(phase)*K;ps=[(-a*sn(w+j*2*v),bb*cn(w+j*2*v)) for j in range(N)];outer=[]
        for j,P in enumerate(ps):
            Q=ps[(j+1)%N];n1=(P[0]/aa,P[1]/be);n2=(Q[0]/aa,Q[1]/be);dd=ic.cross(n1,n2)
            outer.append(((n2[1]-n1[1])/dd,(n1[0]-n2[0])/dd))
        A=ic.area(ps);T=ic.area(outer);p,q,*_=ic.calc(kk,N,tau,w);ep=abs(p-kfactor*T)/(1+abs(p));eq=abs(q-rfactor*A)/(1+abs(q))
        assert max(ep,eq)<mp.mpf('1e-55')
        checks.append({'N':N,'tau':tau,'k':str(kk),'phase':phase,'pedal_KT_error':str(ep),'antipedal_RA_error':str(eq),'R':str(rfactor)})
result={'generated_utc':datetime.now(timezone.utc).isoformat(),'exact_external_bridge_rational_remainders':[str(x) for x in identities],'direct_external_factor_controls':checks,'native_record':{k:native[k] for k in ('id','created','updated','status','is_published','is_draft','access','versions')},'datacite':{k:dc[k] for k in ('doi','created','registered','updated','state','isActive','version','titles')},'files':files,'our_commits':commits,'first_full_proof_patch_binding':firstproofbinding,'PR261_service_created':pr['created_at'],'event_deltas':deltas,'limits':['MD5+size archive association, not direct archived-body SHA256','Authored commits are not first public push times','No exact first HTTP visibility measured','No absolute global priority or causal-independence inference']}
(out/'INDEPENDENT_BRIDGE_ARCHIVE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'rational_remainders':result['exact_external_bridge_rational_remainders'],'factor_cases':len(checks),'official_file_matches':len(files),'first_proof_sha':commits[1]['sha'],'registration_to_first_proof':deltas['datacite_registered'][commits[1]['sha']]},indent=2))
