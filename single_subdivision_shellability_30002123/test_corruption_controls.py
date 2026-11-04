"""Actual certificate/input and manifest mutations, tested normally and with -O."""
import json,pathlib,shutil,subprocess,sys,tempfile

def require(ok,why):
    if not ok:raise RuntimeError(why)
def run(work,target,opt):
    return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[target],cwd=work,capture_output=True,text=True,timeout=300)
def main():
    root=pathlib.Path(__file__).resolve().parent;checks=[]
    cases=['same_size_report','missing_file','extra_file','nested_manifest','manifest_hash','manifest_duplicate','manifest_traversal','corrupt_saved_result','missing_certificate_facet','duplicate_certificate_facet','wrong_complete_order','unknown_face_label','repeated_face_label','wrong_realization','wrong_square_coordinates','wrong_square_facets','wrong_sweep_slope']
    for opt in (False,True):
        require(run(root,'verify_manifest.py',opt).returncode==0,'Baseline manifest failed')
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='shellability-corruption-') as tmp:
                work=pathlib.Path(tmp)/'package';shutil.copytree(root,work)
                target='verify_manifest.py';diagnostic=''
                if case=='same_size_report':
                    p=work/'RESEARCH.md';b=p.read_bytes();p.write_bytes(bytes([b[0]^1])+b[1:]);diagnostic='SHA-256 mismatch'
                elif case=='missing_file':(work/'SOURCE_GATE.md').unlink();diagnostic='Inventory mismatch'
                elif case=='extra_file':(work/'EXTRA.txt').write_text('extra');diagnostic='Inventory mismatch'
                elif case=='nested_manifest':
                    (work/'nested').mkdir();(work/'nested'/'MANIFEST.json').write_text('{}');diagnostic='Inventory mismatch'
                elif case.startswith('manifest_'):
                    p=work/'MANIFEST.json';obj=json.loads(p.read_text())
                    if case=='manifest_hash':obj['files'][0]['sha256']='0'*64;diagnostic='SHA-256 mismatch'
                    elif case=='manifest_duplicate':obj['files'].append(obj['files'][0]);diagnostic='Invalid manifest path'
                    else:obj['files'][0]['path']='../escape';diagnostic='Invalid manifest path'
                    p.write_text(json.dumps(obj))
                elif case=='corrupt_saved_result':
                    p=work/'computation_results.json';obj=json.loads(p.read_text());obj['two_4simplices']['facets']=239;p.write_text(json.dumps(obj));target='run_checks.py';diagnostic='Complete saved output differs'
                else:
                    target='independent_check.py';diagnostic='Independent exact verification failed'
                    if case in ('missing_certificate_facet','duplicate_certificate_facet','wrong_complete_order','unknown_face_label','repeated_face_label'):
                        p=work/'two_4simplices_certificate.json';obj=json.loads(p.read_text())
                        if case=='missing_certificate_facet':obj.pop()
                        elif case=='duplicate_certificate_facet':obj.append(obj[0])
                        elif case=='wrong_complete_order':obj[1],obj[-1]=obj[-1],obj[1]
                        elif case=='unknown_face_label':obj[0][0]=99999
                        else:obj[0][0]=obj[0][1]
                    elif case=='wrong_realization':
                        p=work/'realization.json';obj=json.loads(p.read_text());obj['vertices'][4][0]='1/3'
                    else:
                        p=work/'failed_convex_sweep.json';obj=json.loads(p.read_text())
                        if case=='wrong_square_coordinates':obj['coordinates'][0][0]='2'
                        elif case=='wrong_square_facets':obj['facets'][0]=[0,1,2]
                        else:obj['slope']='-13/11'
                    p.write_text(json.dumps(obj))
                done=run(work,target,opt)
                require(done.returncode!=0 and diagnostic in done.stderr,'Mutation not rejected as intended: '+case+' '+done.stderr)
                checks.append({'mutation':case,'optimized':opt,'rejected':True,'diagnostic':diagnostic})
    print(json.dumps({'status':'PASS','controls':checks,'scope':'Selected input, reference and integrity controls. Not authentication or exhaustive parser/security testing.'},indent=2))
if __name__=='__main__':main()
