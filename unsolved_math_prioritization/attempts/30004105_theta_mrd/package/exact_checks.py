"""Additional strict schemas and independent exact rank/profile checks; no assert."""
import contextlib, io, json, runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok: raise ValueError(msg)
def exact_int(x): return type(x) is int

def rank(rows):
    # Independent rank via incremental normalized pivot dictionaries.
    piv={}
    for row in rows:
        v=[x%3 for x in row]
        for j in range(7):
            if not v[j]:continue
            if j in piv:v=[(a-v[j]*b)%3 for a,b in zip(v,piv[j])]
            else:
                inv=1 if v[j]==1 else 2
                piv[j]=[(inv*a)%3 for a in v];break
    return len(piv)
def main():
    f=json.loads((ROOT/'FINITE_TEST.json').read_text())
    require(set(f)=={'field','nonzero_inverse_checks','codes'},'finite schema')
    require(f['field']=='F_3[z]/(z^7+z^2+2)','field')
    require(exact_int(f['nonzero_inverse_checks']) and f['nonzero_inverse_checks']==2186,'inverse count')
    require(type(f['codes']) is list and len(f['codes'])==2,'two codes')
    names=['monomial_013','twisted_eta1']
    for c,name in zip(f['codes'],names):
        require(type(c) is dict and set(c)=={'name','projective_rank_histogram'} and c['name']==name,'code schema')
        h=c['projective_rank_histogram']
        require(type(h) is list and len(h)==8 and all(exact_int(x) and x>=0 for x in h),'strict histogram')
        require(h==[0,0,0,0,0,99463,1993632,2692062],'exact rank histogram')
        require(sum(h)==4785157,'projective count')
    p=json.loads((ROOT/'PROFILES.json').read_text())
    require(type(p) is dict and set(p)==set(names),'profile code schema')
    checks=0
    for name in names:
        require(set(p[name])==set(map(str,range(1,7))),'generator labels')
        for s in range(1,7):
            v=p[name][str(s)]
            require(type(v) is dict and set(v)=={'sums','intersections'},'profile fields')
            for key in v:require(type(v[key]) is list and len(v[key])==8 and all(exact_int(x) and 0<=x<=7 for x in v[key]),'strict dimensions')
            ordinary=name==names[0] or s in (1,6)
            require(v=={'sums':([3,5,6,7,7,7,7,7] if ordinary else [3,6,7,7,7,7,7,7]),'intersections':([3,1,0,0,0,0,0,0] if ordinary else [3,0,0,0,0,0,0,0])},'exact profiles')
            checks+=1
    with contextlib.redirect_stdout(io.StringIO()): prog=runpy.run_path(str(ROOT/'profile_test.py'))
    # Deterministic independent rank oracle, including singular and full matrices.
    state=1
    for t in range(1000):
        rows=[]
        for i in range(t%15):
            row=[]
            for j in range(7):state=(1103515245*state+12345)%2147483648;row.append(state%3)
            rows.append(row)
        require(len(prog['rref'](rows)[0])==rank(rows),'independent rank check')
        orth=prog['perp'](rows)
        require(rank(orth)+rank(rows)==7,'rank nullity')
        require(all(sum(a*b for a,b in zip(r,s))%3==0 for r in rows for s in orth),'orthogonality')
    status=json.loads((ROOT/'STATUS.json').read_text())
    require(exact_int(status['problem_id']) and status['problem_id']==30004105,'status ID')
    require(exact_int(status['audit_count']) and status['audit_count']==1,'one audit')
    require(status['original_question_resolved'] is False and status['all_generator_collision'] is False and status['certified_MRD'] is True,'scope flags')
    print(json.dumps({'status':'PASS','strict_histograms':2,'generator_profiles':checks,'independent_rank_and_orthogonality_cases':1000,'minimum_rank':5,'projective_words_each':4785157,'audit_count':1},indent=2))
if __name__=='__main__':main()
