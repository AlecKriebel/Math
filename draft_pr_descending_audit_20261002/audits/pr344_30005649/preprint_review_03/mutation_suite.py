import pathlib,shutil,subprocess,json,os,datetime,hashlib
R=pathlib.Path(__file__).resolve().parent;P=R/'packet/qss-self-duality-verification';M=R/'mutants';M.mkdir(exist_ok=True)
def pin(p):return {'size':p.stat().st_size,'mode':oct(p.stat().st_mode&0o777),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
    mutations=[
      ('old_generic_formula','verify_intrinsic.py','rank(join(transpose(twist(twist(v2,k.sigma),k.sigma)),transpose(twist(twist(f2,k.tau),k.tau))),k)','rank(join(transpose(f2),transpose(v2)),k)'),
      ('inverse_integral_F_twist','check_integral_flag.py','sigma(c,1)*monomial(0,weights[j])','sigma(c,-1)*monomial(0,weights[j])'),
      ('unsaturated_integral_first_generator','check_integral_flag.py','basis = [m1,m0,x,y,sA,sB]','basis = [scale(p,m1),m0,x,y,sA,sB]'),
      ('bad_Honda_input','verify_intrinsic.py',None,None)]
    rows=[]
    for label,filename,old,new in mutations:
        d=M/label;d.mkdir(exist_ok=True);src=P/'controls'/filename;txt=src.read_text()
        if old is not None:
            assert txt.count(old)==1;txt=txt.replace(old,new)
        script=d/filename;script.write_text(txt);script.chmod(0o644)
        spec=json.loads((P/'controls/construction.json').read_text())
        if label=='bad_Honda_input':spec['honda_basis_indices']=[0,1,3]
        (d/'construction.json').write_text(json.dumps(spec,indent=2)+'\n')
        for runtime,python in [('py314','/opt/homebrew/bin/python3'),('py312','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')]:
            command=[python,'-B',str(script)];t=datetime.datetime.now(datetime.timezone.utc).isoformat();cp=subprocess.run(command,cwd=d,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat();stem=runtime+'-negative-'+label
            out=R/'receipts'/(stem+'.stdout');err=R/'receipts'/(stem+'.stderr');out.write_bytes(cp.stdout);err.write_bytes(cp.stderr)
            rec={'started_utc':t,'ended_utc':end,'command':command,'cwd':str(d),'exit_code':cp.returncode,'original_control':pin(src),'mutant_control':pin(script),'literal_old':old,'literal_new':new,'changed_input':label=='bad_Honda_input','stdout':pin(out),'stderr':pin(err),'manifest_verifier_invoked':False,'mathematical_rejection':cp.returncode!=0 and (b'AssertionError' in cp.stderr or b'ValueError' in cp.stderr)}
            (R/'receipts'/(stem+'.json')).write_text(json.dumps(rec,indent=2)+'\n');assert rec['mathematical_rejection'],stem;rows.append({'receipt':stem,'exit_code':cp.returncode,'stderr':cp.stderr.decode()});print(stem,'mathematically rejected',cp.returncode)
    (R/'mutation_summary.json').write_text(json.dumps({'written_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mutations':rows},indent=2)+'\n')
if __name__=='__main__':main()
