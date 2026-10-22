#!/usr/bin/env python3
"""Read-only independent rational-jet and custody checks; no author code."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json,zipfile

P=Path(__file__).resolve().parent
HEAD='c4ef79b3975a6e698ace57446d3d67ca8093fa26'
BASE='4b27092a448d53b61408355ce44ec38d103a1ce4'
def need(c,m):
    if not c: raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((P/n).read_text())

# Ordinary derivatives (value, first, second), not Taylor coefficients.
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,s):return tuple(s*x for x in a)
def mul(a,b):return(a[0]*b[0],a[1]*b[0]+a[0]*b[1],a[2]*b[0]+2*a[1]*b[1]+a[0]*b[2])
def inv(a):return(1/a[0],-a[1]/a[0]**2,2*a[1]**2/a[0]**3-a[2]/a[0]**2)
def power(a,n):
    if n<0:return power(inv(a),-n)
    ans=(Q(1),Q(0),Q(0))
    for _ in range(n):ans=mul(ans,a)
    return ans

def math_checks():
    jet_count=0
    for n,ell,t,r in product(range(2,13),range(1,19),(Q(1,2),Q(1),Q(2)),(Q(0),Q(1,4),Q(1),Q(3))):
        k=n-1;x=(t,Q(1),Q(0));f=mul(x,add(power(x,2*ell),(r,Q(0),Q(0))))
        m=power(f,-k);a=-t*m[1]/m[0]
        need(a>=k>=1,'Hardy weight positivity')
        veff=m[2]/(2*m[0])-m[1]**2/(4*m[0]**2)
        u=t**(2*ell)/(t**(2*ell)+r)
        poly=Q(k*(k+2),4)+k*ell*(k+1-2*ell)*u+k*(k+2)*ell**2*u*u
        need(t*t*veff==poly,'independent density-jet potential')
        jet_count+=1
    range_count=0
    for n in range(2,101):
        k=n-1
        for ell in range(1,2*n+3):
            A=Q(k*(k+2),4);B=Q(k*ell*(n-2*ell));C=Q(k*(n+1)*ell**2)
            u=max(Q(0),min(Q(1),-B/(2*C)))
            minimum=A+B*u+C*u*u
            closed=A if 2*ell<=n else A-Q(k*(2*ell-n)**2,4*(n+1))
            need(minimum==closed,'minimum by vertex independent from closed form')
            need((minimum>=Q(3,4))==(ell==1 if n==2 else ell<=n),'integer criterion range')
            for v in [Q(0),Q(1,7),Q(1,2),Q(1)]:
                need(A+B*v+C*v*v-minimum>=0,'global interval minimum')
            range_count+=1
    def minval(n,ell):
        k=n-1;return Q(k*(k+2),4)-Q(k*(2*ell-n)**2,4*(n+1))
    need(minval(3,2)==Q(15,8) and minval(3,3)==Q(7,8),'old n/2 claim rejected')
    need(minval(2,2)<Q(3,4),'dimension two fails from ell2')
    # Pointwise integration-by-parts identity, on positive and negative t.
    hardy_count=0
    for t,m,m1,b,b1,w,w1 in product((Q(-2),Q(-1,2),Q(1,3),Q(3)),(Q(1,2),Q(2)),(Q(-1),Q(2)),(Q(-2),Q(1)),(Q(-1),Q(3)),(Q(-1),Q(2)),(Q(-2),Q(1))):
        a=-t*m1/m;coef=b*(1+a-b)-t*b1
        left=m*w1*w1-m*(w1-b*w/t)**2-coef*m*w*w/t**2
        derivative=(m1*b/t+m*b1/t-m*b/t**2)*w*w+2*m*b*w*w1/t
        need(left==derivative,'Hardy sign/derivative guard')
        hardy_count+=1
    end_count=0
    for ell,x,z in product(range(1,17),(Q(5,4),Q(3,2),Q(7,4)),(Q(2),Q(3),Q(10))):
        f=x*(x**(2*ell)+z*z);fz=2*x*z
        raw=2*f*f/z**3-f*fz/z**2
        expected=2*x**(2*ell+2)*(x**(2*ell)+z*z)/z**3
        need(raw==expected,'literal end Laplacian derivative')
        need(f/z**2==x+x**(2*ell+1)/z**2,'nonzero boundary limit')
        y=1/z
        need(1/(f*f*y**4)==1/(x*x*(1+x**(2*ell)*y*y)**2),'inverted-end metric')
        end_count+=1
    # General block-triangular determinant, independently eliminated.
    det_count=0
    for k,t,f in product(range(1,8),(Q(1,2),Q(2)),(Q(1,3),Q(3))):
        a=[[Q(0) for _ in range(2*k)] for _ in range(2*k)]
        for i in range(k):a[i][i]=f;a[i][k+i]=t;a[k+i][k+i]=Q(1)
        determinant=Q(1)
        for i in range(2*k):
            pivot=a[i][i];determinant*=pivot
            for j in range(i+1,2*k):
                factor=a[j][i]/pivot
                a[j]=[v-factor*w for v,w in zip(a[j],a[i])]
        need(determinant==f**k,'twisted-frame determinant F^k')
        need(determinant!=f**(2*k),'doubled determinant negative control')
        det_count+=1
    need(Q(32768*113664,110125*1500625)>Q(1,45),'ridge D constant')
    need(Q(182,9)<21 and 32*144*Q(21,8)==12096,'ridge A/B constants')
    need(Q(2*(2-3)+2*2,4)*2==1,'PRS n2 ell2 path is positive')
    # Explicit witness to loss of the critical cutoff cancellation below Hardy1.
    need(Q(1,2)**2-Q(3,4)*Q(1,2)**2>0,'weaker Hardy does not cancel G=r')
    return {'density_jet_cases':jet_count,'criterion_range_cases':range_count,
            'Hardy_pointwise_identity_cases':hardy_count,'end_identity_cases':end_count,
            'frame_determinant_cases':det_count,'negative_controls':['old_ell_le_n_over_2','doubled_determinant','Hardy_constant_below_one','wrong_boundary_zero','dimension_two_overextension'],
            'analytic_domains_and_limits':'proved in REPORT.md, not certified by finite tests'}

def entries_check(es,base,excluded=None):
    names=[e['file'] for e in es];need(len(names)==len(set(names)),'duplicate seal entry')
    for e in es:
        r=Path(e['file']);need(not r.is_absolute() and '..' not in r.parts,'unsafe seal path')
        q=base/r;need(q.is_file() and not q.is_symlink(),'missing/symlink member')
        b=q.read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'sealed digest '+e['file'])
    actual=set()
    for q in base.rglob('*'):
        need(not q.is_symlink(),'symlink closure')
        if q.is_file() and q!=excluded:actual.add(q.relative_to(base).as_posix())
    need(actual==set(names),'exact recursive file-set')

def custody():
    b=load('PR_BINDING.json');need(b['head']==HEAD and b['base']==BASE and b['state']=='open' and b['draft'] and not b['queue_changed'],'PR binding')
    pr=load('private/pr.json');final=load('private/pr_final.json')
    for a in [pr,final]:need(a['head']['sha']==HEAD and a['base']['sha']==BASE and a['state']=='open' and a['draft'],'PR live identity')
    need(pr['body']==final['body'] and sha(pr['body'].encode())==b['body_sha256'],'body')
    fs={e['filename']:e for e in load('private/files.json')};need(len(fs)==len(b['eight_blobs'])==8,'eight files')
    for e in b['eight_blobs']:
        f=fs[e['path']];data=(P/'private'/Path(e['path']).name).read_bytes()
        need(e['path'].startswith('unsolved_math_prioritization/attempts/30004272/') and 'QUEUE' not in e['path'],'scope')
        need(f['status']=='added' and f['sha']==e['git_blob_sha']==hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'Git blob')
        need(len(data)==e['bytes'] and sha(data)==e['sha256'],'payload')
    man=load('private/MANIFEST.json');need(len(man['members'])==8 and len(man['entries'])==7,'nested manifest')
    for e in man['entries']:
        data=(P/'private'/e['file']).read_bytes();need(len(data)==e['bytes'] and sha(data)==e['sha256'],'public manifest bytes')
    proof=(P/'private/PROOF.md').read_text();audit=(P/'private/AUDIT.md').read_text()
    need(proof[proof.index('## 2 '):proof.index('## 8 ')] in audit,'integrated proof retained verbatim')
    graw=(P/'private/GWS_FULL43.json').read_bytes();g=json.loads(graw);clear=load('GWS_CLEARANCE.json');vr=g['valueRanges'][0]
    need(sha(graw)==clear['sha256']=='fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1','fresh own tracker')
    need(vr['dataFilters']==[{'gridRange':{'endColumnIndex':43,'sheetId':1254632077,'startColumnIndex':0}}],'43 numeric columns')
    need(len(vr['valueRange']['values'])==191 and not clear['unresolved_duplicate_leads'],'clearance')
    for token in load('SOURCE_ALIASES.json')['no_hit_tokens']:
        need(not any(token.casefold() in '\t'.join(map(str,r)).casefold() for r in vr['valueRange']['values']),'unresolved alias '+token)
    for n in ['ORIGINAL_RECEIPT.json','PRS_RECEIPT.json']:
        e=load(n);fname='original.pdf' if n.startswith('ORIGINAL') else 'prs_journal.pdf';data=(P/'private'/fname).read_bytes()
        need(e['http']==200 and len(data)==e['bytes'] and sha(data)==e['sha256'],'primary original/PRS')
    rec=load('PUBLICATION_RECEIPT.json')
    for e in rec['sources']:
        data=(P/'private'/e['name']).read_bytes();need(e['http']==200 and len(data)==e['bytes'] and sha(data)==e['sha256'],'source receipt')
    html=(P/'private/zenodo_record.html').read_text()
    for fname,md5 in [('ferudun.pdf','d76ca1ecef96362591ca06e7ede0a87f'),('source.zip','c3c9b6696165828003a5d6f9d98301f1'),('ferudun_report.md','c100151e16eca74efd33ffe3f6c0c544')]:
        need(hashlib.md5((P/'private'/fname).read_bytes()).hexdigest()==md5 and 'md5:'+md5 in html,'record file checksum')
    z=zipfile.ZipFile(P/'private/source.zip');need(z.testzip() is None,'all ZIP CRC')
    ze=load('ZIP_CRC.json')['entries'];need(len(ze)==len([x for x in z.infolist() if not x.is_dir()])==22,'ZIP closure')
    for e in ze:need(sha(z.read(e['file']))==e['sha256'],'ZIP payload')
    need(z.read('verification_report.md')==(P/'private/ferudun_report.md').read_bytes(),'report source identity')
    d=load('private/datacite.json')['data']['attributes'];need(d['doi']=='10.5281/zenodo.23041946' and d['creators'][0]['familyName']=='Ferudun' and d['version']=='1.0','publication identity')
    need(d['relatedIdentifiers']==[{'relationType':'IsVersionOf','relatedIdentifier':'10.5281/zenodo.23041945','relatedIdentifierType':'DOI'}],'same-work concept DOI alias')
    prop=load('CELL_PROPOSAL.json');need(len(prop['values'])==1 and len(prop['values'][0])==4 and prop['values'][0][1]=='','four literal cells Bblank')
    need(prop['values'][0][2]=='https://doi.org/10.5281/zenodo.23041946' and prop['service_write_performed'] is False,'existing DOI proposal only')
    entries_check(load('PRIVATE_BODY_SEAL.json')['entries'],P/'private')
    entries_check(load('REVIEW_SEAL.json')['entries'],P,P/'REVIEW_SEAL.json')
    return {'head':HEAD,'eight_blobs':8,'tracker_rows':191,'ZIP_members_crc':22,'private_and_exact_recursive_seals':'PASS','author_programs_executed':False,'service_writes':False}

if __name__=='__main__':
    try:need(False,'deliberate guard probe')
    except RuntimeError:pass
    else:raise RuntimeError('guard disabled')
    print(json.dumps({'status':'PASS','algebra':math_checks(),'custody':custody()},sort_keys=True,indent=2))
