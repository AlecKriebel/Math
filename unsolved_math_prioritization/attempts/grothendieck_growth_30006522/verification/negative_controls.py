"""Mathematical strategy controls and fail-closed filesystem controls; no asserts."""
import itertools,json,os,pathlib,stat,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research'))
from explore import poly,code,expand,left,length,dd,add
from audit_skew_sums import skew,skew_product
from verify_inventory import inventory,classify
from replay import equivalent

def require(x,m):
    if not x:raise RuntimeError(m)
def rejected(f):
    try:f()
    except (ValueError,OSError):return True
    return False

def main():
    baseline={'seconds':1.0,'nested':{'seconds':7},'count':3}
    require(equivalent({**baseline,'seconds':2.0},baseline,'exact_n8.json'),'valid timing variation rejected')
    require(not equivalent({**baseline,'nested':{'seconds':8}},baseline,'exact_n8.json'),'nested seconds mutation accepted')
    for bad in ('nonnumeric',None,True,-1,float('nan'),float('inf')):
        try: equivalent({**baseline,'seconds':bad},baseline,'exact_n8.json')
        except (RuntimeError,ValueError,OverflowError): pass
        else: raise RuntimeError('invalid runtime accepted: '+repr(bad))
    try: equivalent({'count':3},baseline,'exact_n8.json')
    except RuntimeError: pass
    else: raise RuntimeError('missing runtime accepted')
    require(not equivalent({'seconds':2},{'seconds':1},'independent_pipe_audit_n6.json'),'untimed seconds mutation accepted')
    require(not equivalent({'count':True},{'count':1},'independent_pipe_audit_n6.json'),'boolean/integer mutation accepted')
    W=list(itertools.permutations(range(1,6)));a=expand(poly((1,2,5,4,3),True),{code(w):w for w in W})
    u=(2,3,5,4,1);v=(2,4,5,3,1);z=(3,4,5,2,1)
    succ=lambda t:[left(t,k) for k in range(1,len(t)) if t.index(k)<t.index(k+1) and left(t,k) in a]
    require(a[u]==3 and a[v]==-2 and a[z]==1 and succ(u)==[v] and succ(v)==[z],'coefficient injection control failed')
    b={(2,1,3):1,(2,3,1):-1};t=(2,1,3)
    require(not any(left(t,k) in b for k in (1,2) if t.index(k)<t.index(k+1)),'monomial transfer false strategy not rejected')
    require(poly((2,1,3))=={(1,0,0):1} and poly((2,3,1))=={(1,1,0):1},'monomial example changed')
    inv=lambda w:{(i,j) for i in range(len(w)) for j in range(i+1,len(w)) if w[i]>w[j]}
    require(a[(1,4,5,2,3)]==-1 and not inv((1,2,5,4,3))<=inv((1,4,5,2,3)),'rootedness false strategy not rejected')
    f=poly((2,1));h=dict(f)
    for m,c in f.items():q=list(m);q[1]+=1;add(h,tuple(q),-c)
    require(dd(h,0)=={(0,0):1},'isobaric cancellation control failed')
    # Deliberately omit the rectangular factor: the strengthened false identity must fail.
    p=(1,);q=(1,)
    require(poly(skew(p,q))!={(0,0):1} and skew_product(poly(p),poly(q),1,1)==poly(skew(p,q)),'skew factor mutation was not detected')
    synthetic=[]
    for mode in (stat.S_IFLNK,stat.S_IFIFO,stat.S_IFSOCK,stat.S_IFCHR,stat.S_IFBLK):
        require(rejected(lambda:classify(mode|0o600)),'special mode accepted');synthetic.append(oct(mode))
    with tempfile.TemporaryDirectory() as tmp:
        r=pathlib.Path(tmp);(r/'ok.txt').write_text('ok');baseline=inventory(r)
        (r/'nested').mkdir();os.mkfifo(r/'nested'/'fifo')
        real_open=os.open;reads=[]
        def tracked_open(*args,**kwargs):reads.append(args[0]);return real_open(*args,**kwargs)
        os.open=tracked_open
        try:
            require(rejected(lambda:inventory(r)),'nested FIFO accepted')
            require(not reads,'payload opened before full-tree FIFO rejection')
        finally:os.open=real_open
        (r/'nested'/'fifo').unlink();(r/'nested').rmdir()
        (r/'link').symlink_to(r/'ok.txt');require(rejected(lambda:inventory(r)),'symlink accepted');(r/'link').unlink()
        (r/'extra').write_text('unexpected');require(inventory(r)!=baseline,'extra regular file not detected');(r/'extra').unlink()
        (r/'ok.txt').write_text('changed');require(inventory(r)!=baseline,'payload mutation not detected')
    print(json.dumps({'mathematical_controls':['coefficient injection 3>2>1','generic monomial transfer','left-weak rootedness','isobaric cancellation','missing skew rectangle mutation'],'filesystem_controls':['nested real FIFO before any payload open','real symlink','extra regular file','payload mutation'],'synthetic_rejected_modes':synthetic,'runtime_controls':['valid top-level timing variation','nested seconds mutation rejected','nonnumeric/null/bool/negative/nonfinite runtime rejected','missing runtime rejected','untimed seconds mutation rejected','boolean/integer mutation rejected'],'socket_creation':'not attempted','status':'PASS'},indent=2))
if __name__=='__main__':main()
