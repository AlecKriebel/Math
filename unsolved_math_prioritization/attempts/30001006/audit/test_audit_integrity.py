#!/usr/bin/env python3
"""Integrity regression in temporary copies, without modifying source files."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def verify(root,anchor,opt,cwd):
    return subprocess.run([sys.executable]+(['-O'] if opt else [])+['-B',str(root/'verify_audit.py'),'--expected-manifest',anchor],capture_output=True,cwd=cwd)
def main():
    anchor=hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest();good=[];bad=[];math=[]
    with tempfile.TemporaryDirectory(prefix='ricci-bridge-independent-') as temp:
        temp=pathlib.Path(temp);rel=temp/'relocated';shutil.copytree(ROOT,rel)
        for opt in (False,True):
            for root,label in ((ROOT,'original'),(rel,'relocated')):
                p=verify(root,anchor,opt,temp);need(p.returncode==0,p.stderr.decode());good.append(label+('_optimized' if opt else '_normal'))
            for kind in ('report_edit','result_edit','missing_member','extra_member','symlink_member','bad_anchor'):
                dst=temp/(kind+str(opt));shutil.copytree(ROOT,dst);target=dst/'AUDIT_REPORT.md'
                if kind=='report_edit':target.write_text(target.read_text()+'\nMutation\n')
                if kind=='result_edit':(dst/'independent_results.json').write_text('{}\n')
                if kind=='missing_member':target.unlink()
                if kind=='extra_member':(dst/'UNEXPECTED').write_text('Mutation')
                if kind=='symlink_member':target.unlink();target.symlink_to(ROOT/'AUDIT_REPORT.md')
                p=verify(dst,'0'*64 if kind=='bad_anchor' else anchor,opt,temp)
                need(p.returncode!=0,'mutation accepted: '+kind);bad.append(kind+('_optimized' if opt else '_normal'))
        source=(ROOT/'independent_checks.py').read_text()
        for kind,old,new in (('normal_metric_sign','return -(R[i,k,j,l]+R[i,l,j,k])/3','return (R[i,k,j,l]+R[i,l,j,k])/3'),('CK_constant_term','v=ck_poly(q)','v=ck_poly(q+1)'),('barrier_sign','vp=-M*J/w','vp=M*J/w')):
            need(source.count(old)==1,'mutation target mismatch');p=temp/(kind+'.py');p.write_text(source.replace(old,new))
            for opt in (False,True):
                r=subprocess.run([sys.executable]+(['-O'] if opt else [])+['-B',str(p)],capture_output=True,cwd=temp)
                need(r.returncode!=0,'mathematical mutant accepted: '+kind);math.append(kind+('_optimized' if opt else '_normal'))
    print(json.dumps({'status':'PASS','positive_replays':good,'package_mutation_rejections':bad,'mathematical_mutation_rejections':math,'scope':'Selected integrity and code mutations; not a proof of geometric existence.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
