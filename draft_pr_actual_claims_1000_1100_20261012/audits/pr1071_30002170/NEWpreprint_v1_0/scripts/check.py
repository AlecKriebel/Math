#!/usr/bin/env python3
"""Replay original bytes with exact identities and finite floating diagnostics."""
import argparse,hashlib,json,math,shutil,subprocess,sys,tempfile
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
# Explicit binary64 diagnostic tolerances; these are acceptance envelopes,
# not interval error bounds or a proof of cross-runtime numerical accuracy.
COVARIANCE_ABS_TOL = 2.0**-49  # eight binary64 epsilons; max observed drift is one
DERIVED_REL_TOL = 2.0**-47     # 32 binary64 epsilons for libm-derived positive values
def float_policy(path):
    if path == ('L1_fthird_numeric',):return (DERIVED_REL_TOL,0.0,'derived_relative')
    if len(path)==3 and type(path[1]) is int:
        if path[0]=='finite_covariance_identity_float_cross_checks' and path[2] in ('direct','grouped','difference'):
            return (0.0,COVARIANCE_ABS_TOL,'covariance_absolute')
        if path[0]=='constant_float_checks' and path[2] in ('D_H','Pbar_f','Pbar_g','c_H'):
            return (DERIVED_REL_TOL,0.0,'derived_relative')
    return (0.0,0.0,'exact_float')  # H sample inputs and any other float stay exact
def result_guard(result,expected):
    require(sys.float_info.radix==2 and sys.float_info.mant_dig==53 and sys.float_info.max_exp==1024,'Diagnostic requires IEEE754 binary64 floats.')
    require(type(result) is dict and type(expected) is dict,'Result roots must be objects.')
    coverage={'exact_nonfloat_leaves':0,'exact_float':0,'derived_relative':0,'covariance_absolute':0}
    def compare(value,baseline,path):
        label='/'.join(map(str,path)) or '<root>'
        require(type(value) is type(baseline),'Result type differs: '+label)
        if type(baseline) is dict:
            require(value.keys()==baseline.keys(),'Result field set differs: '+label)
            for key in baseline:compare(value[key],baseline[key],path+(key,))
        elif type(baseline) is list:
            require(len(value)==len(baseline),'Result list length differs: '+label)
            for i,(v,b) in enumerate(zip(value,baseline)):compare(v,b,path+(i,))
        elif type(baseline) is float:
            require(math.isfinite(value) and math.isfinite(baseline),'Nonfinite float: '+label)
            rel,absolute,policy=float_policy(path)
            require(abs(value-baseline)<=max(absolute,rel*max(abs(value),abs(baseline))),'Floating diagnostic differs: '+label)
            coverage[policy]+=1
        else:
            require(value==baseline,'Exact result differs: '+label)
            coverage['exact_nonfloat_leaves']+=1
    # Only the top-level UTC is excluded; every other container, key and leaf
    # is visited. Rational identities, normalization, text and integers are exact.
    compare(canonical(result),canonical(expected),())
    require(result['exact_area_pairing']=='4/45045','Area pairing changed.')
    require(result['L1_f']=='1/128' and result['L1_g']=='1/630','Polynomial L1 norms changed.')
    require(result['L1_gthird']=='113/196','Third-derivative norm changed.')
    require(all(x==['0','0'] for x in result['endpoint_traces_phi_derivatives_0_to_3'].values()),'Endpoint traces changed.')
    require(result['L1_fthird_numeric']>0,'Finite norm positivity check failed.')
    for row in result['constant_float_checks']:
        require(0<row['H']<1 and all(row[k]>0 for k in ('D_H','Pbar_f','Pbar_g','c_H')),'Finite constant positivity check failed.')
    for row in result['finite_covariance_identity_float_cross_checks']:
        require(row['direct']>0 and row['grouped']>0,'Finite covariance positivity check failed.')
        require(row['difference']==row['direct']-row['grouped'],'Stored covariance residual is inconsistent.')
        require(abs(row['difference'])<=COVARIANCE_ABS_TOL,'Direct/grouped covariance identity diagnostic failed.')
    return coverage
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
    modes=[];normal_result=None
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        dest=out/mode;dest.mkdir(exist_ok=True);checker=dest/'original_finite_checks.py';shutil.copyfile(src,checker)
        require(digest(checker)==row['sha256'],'Isolated replay copy is not byte-exact.')
        proc=subprocess.run([sys.executable,*flags,str(checker)],capture_output=True,text=True,cwd=dest)
        (dest/'stdout.txt').write_text(proc.stdout);(dest/'stderr.txt').write_text(proc.stderr)
        require(proc.returncode==0 and proc.stderr=='','Original finite checker failed.')
        result=json.loads((dest/'FINITE_CHECKS.json').read_text());coverage=result_guard(result,expected)
        if normal_result is None:normal_result=canonical(result)
        else:require(canonical(result)==normal_result,'Same-runtime normal/optimized results differ.')
        bad=json.loads(json.dumps(result));bad['exact_area_pairing']='0'
        controls=[expect_rejection(lambda:source_guard(tex.replace(r'\overline{\widehat h(\xi)}',r'\widehat h(\xi)'),q,add),'Fourier conjugation removed'),expect_rejection(lambda:source_guard(tex,q,add.replace('Eq30','removed')),'Journal tail-cutoff qualification removed'),expect_rejection(lambda:result_guard(bad,expected),'Area pairing changed to zero')]
        modes.append({'mode':mode,'returncode':proc.returncode,'stderr_bytes':0,'copy_sha256':digest(checker),'result_sha256':digest(dest/'FINITE_CHECKS.json'),'complete_non_utc_field_contract_pass':True,'comparison_coverage':coverage,'negative_controls':controls})
    report={'python':sys.version,'wrapper_optimized':not __debug__,'original_checker_sha256':row['sha256'],'modes':modes,'same_runtime_normal_optimized_non_utc_exact_equal':True,'float_contract':{'covariance_absolute_tolerance':COVARIANCE_ABS_TOL,'derived_relative_tolerance':DERIVED_REL_TOL,'all_other_values':'exact, with finite guards for all floats','ignored_field':'top-level utc only'},'guard_implementation':'Explicit RuntimeError guards remain active under python -O. Original checker assertions are active only in normal mode; optimized execution is accepted only after complete explicit schema/exact/toleranced result validation and same-runtime normal/optimized equality.','meaning':'Exact rational finite identities and sampled floating computations only. Not a universal proof, formal certification or interval quadrature validation.'}
    (out/'CHECK_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path);args=parser.parse_args()
    if args.out:
        run(args.out)
    else:
        with tempfile.TemporaryDirectory(prefix='pr1071-finite-',dir=Path(tempfile.gettempdir()).resolve()) as d:run(Path(d)/'result')
