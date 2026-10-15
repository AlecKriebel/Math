#!/usr/bin/env python3
"""Replay byte-exact original finite checker; use explicit guards under -O."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
sys.dont_write_bytecode=True
from pathlib import Path
from package_paths import fresh_output,safe_path
root=Path(__file__).resolve().parents[1]
def require(condition,message):
    if not condition:raise RuntimeError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(d):return {k:v for k,v in d.items() if k!='utc'}
def source_guard(tex,qualification,addendum):
    markers=[r'H\in(1/4,1)',r'n\ge1',r'F\in L^2(\G_{T,n})',r'j=1,\ldots,n',r'\overline{\widehat h(\xi)}',r'\frac1{2(5-\alpha)}',r'\frac{D_H\overline P_r}{2\pi}',r'\operatorname{tr}(AC)',r'na\Delta^{2H}',r'c_H=\frac{2\pi a}{D_H\sqrt{\overline P_f\overline P_g}}',r'P_m=L_m+Q_m',r'\tfrac12\sum',r'c_0+2\sum_{r\ge1}c_r','UNKNOWN','2009 primary announcement','not a journal-error claim']
    for marker in markers:require(marker in tex,'Missing authored source/proof guard: '+marker)
    require('eq27' in qualification and 'little-o' in qualification,'Convergence-only qualification missing.')
    require('Eq29' in addendum and 'Eq30' in addendum and '3f7467eea58ebf6998981bf0337a579f45ad1db1c544273eb955507fe2e55c68' in addendum,'Current journal-version boundary missing.')
def result_guard(result,expected):
    require(canonical(result)==canonical(expected),'Original checker mathematics differs from frozen original result.')
    require(result['exact_area_pairing']=='4/45045','Area pairing changed.')
    require(result['L1_f']=='1/128' and result['L1_g']=='1/630','Polynomial L1 norms changed.')
    require(result['L1_gthird']=='113/196','Third-derivative norm changed.')
    require(all(x==['0','0'] for x in result['endpoint_traces_phi_derivatives_0_to_3'].values()),'Endpoint traces changed.')
    require(all(x['c_H']>0 for x in result['constant_float_checks']),'Finite positivity check failed.')
def expect_rejection(fn,label):
    try:fn()
    except RuntimeError:return {'control':label,'rejected':True}
    raise RuntimeError('Negative control escaped: '+label)
def run(out):
    out=fresh_output(out,root)
    out.mkdir()
    copies=json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']
    row=next(r for r in copies if r['package_copy']=='checks/original_finite_checks.py')
    src=safe_path(root,row['package_copy']);require(digest(src)==row['sha256'],'Original checker bytes changed.')
    expected=json.loads(safe_path(root,'checks/original_expected.json').read_text())
    tex=safe_path(root,'paper.tex').read_text();q=safe_path(root,'custody/ROOT_CURRENT_SOURCE_QUALIFICATION.md').read_text();add=safe_path(root,'custody/ROOT_SOURCE_VERSION_ADDENDUM_20261014.md').read_text()
    source_guard(tex,q,add)
    modes=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        dest=out/mode;dest.mkdir(exist_ok=True);checker=dest/'original_finite_checks.py';shutil.copyfile(src,checker)
        require(digest(checker)==row['sha256'],'Isolated replay copy is not byte-exact.')
        proc=subprocess.run([sys.executable,*flags,str(checker)],capture_output=True,text=True,cwd=dest)
        (dest/'stdout.txt').write_text(proc.stdout);(dest/'stderr.txt').write_text(proc.stderr)
        require(proc.returncode==0 and proc.stderr=='','Original finite checker failed.')
        result=json.loads((dest/'FINITE_CHECKS.json').read_text());result_guard(result,expected)
        bad=json.loads(json.dumps(result));bad['exact_area_pairing']='0'
        controls=[expect_rejection(lambda:source_guard(tex.replace(r'\overline{\widehat h(\xi)}',r'\widehat h(\xi)'),q,add),'Fourier conjugation removed'),expect_rejection(lambda:source_guard(tex,q,add.replace('Eq30','removed')),'Journal tail-cutoff qualification removed'),expect_rejection(lambda:result_guard(bad,expected),'Area pairing changed to zero')]
        modes.append({'mode':mode,'returncode':proc.returncode,'stderr_bytes':0,'copy_sha256':digest(checker),'result_sha256':digest(dest/'FINITE_CHECKS.json'),'full_mathematics_equal_utc_only_difference':True,'negative_controls':controls})
    report={'python':sys.version,'wrapper_optimized':not __debug__,'original_checker_sha256':row['sha256'],'modes':modes,'guard_implementation':'Explicit RuntimeError guards remain active under python -O. Original checker assertions are active only in normal mode; optimized execution is accepted only after full result comparison by explicit guards.','meaning':'Exact rational finite identities and sampled floating computations only. Not a universal proof, formal certification or interval quadrature validation.'}
    (out/'CHECK_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path);args=parser.parse_args()
    if args.out:
        run(args.out)
    else:
        with tempfile.TemporaryDirectory(prefix='pr1071-finite-',dir=Path(tempfile.gettempdir()).resolve()) as d:run(Path(d)/'result')
