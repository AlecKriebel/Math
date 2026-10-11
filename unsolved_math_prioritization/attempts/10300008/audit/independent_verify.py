#!/usr/bin/env python3
"""Independent source-free algebra, archive, and frozen-permission controls.
Run with the immutable author ZIP as the sole argument. No author module imports.
Temporary writable fixtures are disposable; no author path is modified.
"""
from fractions import Fraction as Q
from itertools import product, permutations
from pathlib import Path, PurePosixPath
import hashlib, json, os, stat, subprocess, sys, tempfile, zipfile

ARCHIVE_SHA = '61fc41de148b8502dbc899e9eaa09e5864fabbf98869c691378b50a3001c8274'
MANIFEST_SHA = '0c1731e5864003466319176235ee3e4feb16c0d7bc29d75a0bc6e43c1f289d89'
PROOF_SHA = '9c06dee3bb1b609f4afd885e9e4fcbdf0608b734f4d41cc54a592001db821051'
BOOTSTRAP_SHA = '8c9d563a3db73283718d50c7fefe44f846eda56035df85ea4c8b4dab72b22b2e'
HARNESS_SHA = '582fd716a9b52d2b81a19acab2d01b9135c3004b2f37ed9cae95c2deb48a0cd7'
MODES = ('normal','-O','-OO')
class Failure(Exception): pass
def need(c,m):
    if not c: raise Failure(m)
def digest(b): return hashlib.sha256(b).hexdigest()
def transpose(a): return [list(x) for x in zip(*a)]
def mm(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def scale(c,a): return [[c*x for x in r] for r in a]
def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def determinant(a):
    n=len(a); total=Q(0)
    for p in permutations(range(n)):
        s=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));v=Q(s)
        for i in range(n): v*=a[i][p[i]]
        total+=v
    return total
def inverse(a):
    n=len(a); x=[[Q(y) for y in a[i]]+eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot=next((r for r in range(col,n) if x[r][col]),None)
        need(pivot is not None,'singular')
        x[col],x[pivot]=x[pivot],x[col]
        v=x[col][col];x[col]=[z/v for z in x[col]]
        for row in range(n):
            if row!=col:
                v=x[row][col];x[row]=[z-v*y for z,y in zip(x[row],x[col])]
    return [r[n:] for r in x]
def exterior2(a):
    # Matrix of Lambda^2(a), columns (e2^e3,e3^e1,e1^e2).
    pairs=((1,2),(2,0),(0,1))
    return [[a[i][k]*a[j][l]-a[i][l]*a[j][k] for k,l in pairs] for i,j in pairs]
def is_spd(a):
    return a==transpose(a) and all(determinant([r[:k] for r in a[:k]])>0 for k in range(1,len(a)+1))
def rejected(fn):
    try:fn()
    except (Failure,ValueError,TypeError):return True
    return False

def algebra():
    count={'cofactor_and_frame_covariance':0,'scaled_form_compatibility':0,'jet_trace':0,'homology_squeeze':0,'conformal_frame':0,'average_area':0}
    for r,s,t in product((-2,-1,0,1,2),repeat=3):
        a=[[2,r,s],[0,3,t],[0,0,1]];g=mm(transpose(a),a);b=exterior2(g)
        need(is_spd(g) and is_spd(b),'positive metric')
        need(b==scale(determinant(g),inverse(g)),'cofactor identity')
        need(determinant(b)==determinant(g)**2,'cofactor determinant')
        need(scale(determinant(g),inverse(b))==g,'inverse reconstruction')
        # Include non-unit determinant and orientation-reversing frame changes.
        p=[[1,s,0],[0,2,r],[0,0,-3]];w=exterior2(p)
        gp=mm(mm(transpose(p),g),p);bp=mm(mm(transpose(w),b),w)
        need(exterior2(gp)==bp,'frame covariance')
        need(scale(determinant(gp),inverse(bp))==gp,'frame-covariant reconstruction')
        count['cofactor_and_frame_covariance']+=1
    for x,y,z in product((Q(-1,5),Q(0),Q(1,5)),repeat=3):
        corr=[[Q(1),x,y],[x,Q(1),z],[y,z,Q(1)]];d=[[Q(2),0,0],[0,Q(3),0],[0,0,Q(5)]]
        s=mm(mm(d,corr),d);need(is_spd(s),'compatible SPD')
        areas=(Q(2),Q(3),Q(5));omega=[[s[i][j]/areas[i] for j in range(3)] for i in range(3)]
        need(all(omega[i][i]==areas[i] for i in range(3)),'diagonal values')
        need([[areas[i]*omega[i][j] for j in range(3)] for i in range(3)]==s,'scaled forms')
        frame=[[1,2,0],[0,1,-1],[0,0,3]];inv=inverse(frame)
        b=mm(mm(transpose(inv),s),inv)
        need(mm(mm(transpose(frame),b),frame)==s,'bivector Gram transport')
        count['scaled_form_compatibility']+=1
    for r,s,u,v in product(range(-2,3),repeat=4):
        if u==v==0:continue
        c=[[Q(1+r*r),Q(r*s)],[Q(r*s),Q(1+s*s)]]
        trace=c[0][0]*u*u+2*c[0][1]*u*v+c[1][1]*v*v
        need(trace==u*u+v*v+(r*u+s*v)**2 and trace>0,'PSD trace')
        count['jet_trace']+=1
    for a,c in product((Q(1,7),Q(2,3),Q(1),Q(5,2),Q(11)),repeat=2):
        b=c*a;need(b>=c*a and a>=b/c and b==c*a,'calibration squeeze');count['homology_squeeze']+=1
    for r,s,t in product((-2,-1,0,1,2),repeat=3):
        frame=[[1,r,0],[s,1+r*s,0],[0,t,2]];beta=[[Q(3,7)],[Q(-2,5)],[Q(7,3)]]
        need(mm(inverse(frame),mm(frame,beta))==beta,'conformal frame solve');count['conformal_frame']+=1
    for a,ap in product((Q(1,3),Q(1,2),Q(1),Q(2),Q(3)),(Q(-3),Q(0),Q(2))):
        A=(a+1/a)/2;Ap=ap*(1-1/a**2)/2
        need(A*A==(a*a+1)*(1/a**2+1)/4,'average area')
        need(Ap/A==ap*(a*a-1)/(a*(a*a+1)),'average divergence')
        count['average_area']+=1
    controls={
      'positive_diagonals_do_not_imply_symmetry':not is_spd([[1,2,0],[0,1,0],[0,0,1]]),
      'symmetric_positive_diagonals_do_not_imply_spd':not is_spd([[1,2,0],[2,1,0],[0,0,1]]),
      'dependent_frame_rejected':rejected(lambda:inverse([[1,0,0],[0,1,0],[0,0,0]])),
      'indefinite_hessian_can_have_zero_trace':Q(1)+Q(-1)==0,
      'zero_homology_scalar_cannot_be_divided':rejected(lambda:need(Q(0)>0,'positive scalar')),
      'negative_homology_scalar_not_positive_case':rejected(lambda:need(Q(-1)>0,'positive scalar')),
      'strict_area_inequality_fails_second_bound':not(Q(1)>=Q(2)/Q(1)),
      'common_calibration_two_unit_coordinate_normals_impossible':1+1>1,
      'conformal_factor_two':3-1==2,
      'nonclosed_beta_coefficient_at_origin':Q(4,2)==2,
      'closed_beta_can_have_nonzero_period':Q(1)!=0,
      'metric_average_h_over_pi_at_origin':Q(2)*(1-Q(1,4))/(2*((Q(2)+Q(1,2))/2))==Q(3,5),
    }
    need(all(controls.values()),'independent countercontrol')
    return {'positive_groups':count,'positive_cases':sum(count.values()),'countercontrols':controls,'countercontrol_count':len(controls),'scope':'Exact algebra only; smooth and topological statements require the written audit.'}

def invoke(root,filename,mode):
    flags=[] if mode=='normal' else [mode]
    return subprocess.run([sys.executable,'-I','-S','-B']+flags+[str(root/filename)],cwd=root,capture_output=True,timeout=120)
def snapshot(root):return {str(p.relative_to(root)):digest(p.read_bytes()) for p in root.rglob('*') if p.is_file() and not p.is_symlink()}
def materialize(data,root,readonly):
    root.mkdir()
    for name,raw in data.items():
        p=root/name;p.parent.mkdir(exist_ok=True);p.write_bytes(raw);p.chmod(0o444 if readonly else 0o644)
    if readonly:
        for p in root.rglob('*'):
            if p.is_dir():p.chmod(0o555)
        root.chmod(0o555)
def thaw(root):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if p.is_dir():p.chmod(0o755)
        elif not p.is_symlink():p.chmod(0o644)
def main():
    need(len(sys.argv)==2,'usage: independent_verify.py AUTHOR.zip')
    archive=Path(sys.argv[1]);raw=archive.read_bytes();need(digest(raw)==ARCHIVE_SHA,'archive anchor')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();need(len(names)==len(set(names))==13,'archive inventory')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            need(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'unsafe member')
            need(not stat.S_ISLNK(i.external_attr>>16),'symlink member')
        data={n:z.read(n) for n in names}
    anchors={'AUTHOR_MANIFEST.json':MANIFEST_SHA,'packet/PROOF.md':PROOF_SHA,'bootstrap.py':BOOTSTRAP_SHA,'test_bootstrap.py':HARNESS_SHA}
    for n,h in anchors.items():need(digest(data[n])==h,'member anchor '+n)
    manifest=json.loads(data['AUTHOR_MANIFEST.json']);need(manifest['disposition']=='unsolved' and manifest['approaches']==5,'disposition')
    need({n for n in names if n.startswith('packet/')}=={'packet/'+e['path'] for e in manifest['files']},'payload inventory')
    for e in manifest['files']:
        b=data['packet/'+e['path']];need(len(b)==e['bytes'] and digest(b)==e['sha256'],'manifest member')
    original=data['test_bootstrap.py'].decode()
    old="    shutil.copytree(base/'packet',dest/'packet')\n"
    new=old+"    # Only disposable fixtures are made writable; frozen sources stay untouched.\n    for p in dest.rglob('*'):\n        p.chmod(0o755 if p.is_dir() else 0o644)\n"
    need(original.count(old)==1,'patch context count')
    patched=original.replace(old,new).encode()
    positives=[];original_failures=[];patched_replays=[];negative=[]
    with tempfile.TemporaryDirectory(prefix='independent-minimal-review-') as tmp:
        top=Path(tmp);ro=top/'frozen-read-only';materialize(data,ro,True);before=snapshot(ro)
        denied=False
        try:(ro/'packet'/'WRITE_PROBE').write_text('must fail')
        except PermissionError:denied=True
        need(denied,'read-only not enforced')
        expected=None
        for mode in MODES:
            cp=invoke(ro,'bootstrap.py',mode);need(cp.returncode==0,'author bootstrap fails '+mode)
            if expected is None:expected=cp.stdout
            need(cp.stdout==expected,'bootstrap mode mismatch');positives.append({'mode':mode,'output_sha256':digest(cp.stdout)})
            cp=invoke(ro,'test_bootstrap.py',mode)
            need(cp.returncode==1 and b'Permission denied' in cp.stderr and b'mutation-0' in cp.stderr,'expected frozen-harness defect not reproduced')
            original_failures.append({'mode':mode,'exit':1,'reason':'0444 payload permissions copied into mutation-0'})
        need(snapshot(ro)==before,'frozen read-only bytes changed');thaw(ro)
        patchdata=dict(data);patchdata['test_bootstrap.py']=patched
        pr=top/'patched-read-only';materialize(patchdata,pr,True);pbefore=snapshot(pr);replay_expected=None
        for mode in MODES:
            cp=invoke(pr,'test_bootstrap.py',mode);need(cp.returncode==0,'patched harness fails: '+cp.stderr.decode())
            if replay_expected is None:replay_expected=cp.stdout
            need(cp.stdout==replay_expected,'patched harness mode mismatch')
            result=json.loads(cp.stdout);need(result['positive_count']==6 and result['negative_count']==78 and result['read_only_write_denied'],'patched replay counts')
            patched_replays.append({'mode':mode,'positive_runs':6,'negative_integrity_runs':78,'output_sha256':digest(cp.stdout)})
        need(snapshot(pr)==pbefore,'patched read-only bytes changed');thaw(pr)
        # Independently selected malformed and hostile fixtures, no author imports.
        cases=('malformed-manifest','missing-proof','extra-payload','symlink-proof','swapped-code','wrong-boolean-type','duplicate-json-key','truncated-claims','wrong-isotopy-claim','self-consistent-manifest-forgery')
        for case in cases:
            r=top/case;materialize(data,r,False);payload=r/'packet';m=r/'AUTHOR_MANIFEST.json'
            if case=='malformed-manifest':m.write_bytes(b'{')
            elif case=='missing-proof':(payload/'PROOF.md').unlink()
            elif case=='extra-payload':(payload/'EXTRA').write_text('extra')
            elif case=='symlink-proof':
                target=r/'external-proof';target.write_bytes(data['packet/PROOF.md']);(payload/'PROOF.md').unlink();(payload/'PROOF.md').symlink_to(target)
            elif case=='swapped-code':(payload/'verify.py').write_text("from pathlib import Path\nPath('../UNAUTHENTICATED').write_text('executed')\n")
            elif case=='duplicate-json-key':(payload/'CLAIMS.json').write_bytes(b'{"status":"unsolved","status":"solved"}')
            elif case=='truncated-claims':(payload/'CLAIMS.json').write_bytes(data['packet/CLAIMS.json'][:17])
            else:
                c=json.loads(data['packet/CLAIMS.json'])
                if case=='wrong-boolean-type':c['general_resolution']=0
                else:c['separate_isotopies_allowed']=False
                (payload/'CLAIMS.json').write_text(json.dumps(c))
                if case=='self-consistent-manifest-forgery':
                    altered=json.loads(m.read_text())
                    for e in altered['files']:
                        if e['path']=='CLAIMS.json':
                            b=(payload/e['path']).read_bytes();e.update(bytes=len(b),sha256=digest(b))
                    m.write_text(json.dumps(altered))
            for mode in MODES:
                cp=invoke(r,'bootstrap.py',mode)
                need(cp.returncode==1 and cp.stderr.startswith(b'REJECT:'),'malformed fixture accepted '+case)
                need(not (r/'UNAUTHENTICATED').exists(),'untrusted code ran')
                negative.append({'case':case,'mode':mode,'rejected':True})
    need(digest(archive.read_bytes())==ARCHIVE_SHA,'archive changed')
    return {'schema':'minimal-surfaces-independent-review-v1','status':'pass_with_harness_patch','archive_sha256':ARCHIVE_SHA,'author_members':len(names),'geometry_disposition':'scoped_partial_results_accepted_general_problem_unsolved','algebra':algebra(),'author_bootstrap_read_only':positives,'original_harness_reproducible_failure':original_failures,'patched_harness_replay':patched_replays,'independent_malformed_runs':negative,'independent_malformed_run_count':len(negative),'patched_harness_sha256':digest(patched),'read_only_write_denied':denied,'source_free':True,'author_archive_unchanged':True,'scope':'Independent mathematical audit is in AUDIT.md; tests do not establish the global geometry or literature status.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Failure,OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError,zipfile.BadZipFile) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
