#!/usr/bin/env python3
"""Fresh executions and targeted fault controls; all raw outputs are retained."""
import datetime,hashlib,json,pathlib,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent
CASE=HERE.parent.parent
PRIVATE=CASE/'private_sources/spin_certificate_adversary'
SAVED=PRIVATE/'sealed_validator/certify_integral.py'
EXPECTED='027dc38ea76f1a4e69d8976a4845caefc4429e48b551afa7c327dc243b3dac20'

def need(x,s):
    if not x:raise RuntimeError(s)

def main():
    source=SAVED.read_text()
    need(hashlib.sha256(SAVED.read_bytes()).hexdigest()==EXPECTED,'sealed code hash mismatch')
    mutants=PRIVATE/'targeted_mutants';mutants.mkdir(exist_ok=True)
    changes=[
      ('wrong_modular_root','GENERATOR = 3','GENERATOR = 1',1,'NTT generator checks failed'),
      ('wrong_fft_root','roots.append((r, i))','roots.append((r, i + self.R // 10 if k == 1 else i))',1,'FFT imaginary enclosure failure'),
      ('suppressed_fft_error','outputs = fft_centers(inputs, roots, R)','error = 0\n    outputs = fft_centers(inputs, roots, R)',1,'FFT imaginary enclosure failure'),
      ('sampling_replaces_cell_means','sl, su = fixed.sinc(k, cells, pi)','sl, su = R, R',0,None),
    ]
    mutant_receipts=[]
    for label,old,new,expected,message in changes:
        need(source.count(old)==1,'mutation anchor not unique')
        target=mutants/(label+'.py');target.write_text(source.replace(old,new))
        mutant_receipts.append({'label':label,'private_path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'exact_single_replacement':{'old':old,'new':new},'expected_exit':expected,'expected_guard_message':message})
    (HERE/'MUTATION_RECEIPTS.json').write_text(json.dumps(mutant_receipts,indent=2)+'\n')
    commands=[
      ('fresh_N13_normal',[sys.executable,str(SAVED),'--N','13','--cells','65536','--bits','100','--output',str(HERE/'fresh_N13_normal.json')],0,None),
      ('fresh_N13_optimized',[sys.executable,'-O',str(SAVED),'--N','13','--cells','65536','--bits','100','--output',str(HERE/'fresh_N13_optimized.json')],0,None),
      ('independent_Gram_optimized',[sys.executable,'-O',str(HERE/'gram_crosscheck.py')],0,None),
    ]+[(label,[sys.executable,'-O',str(mutants/(label+'.py')),'--N','13','--cells','65536','--bits','100'],expected,message) for label,_,_,expected,message in changes]
    records=[]
    for label,argv,expected,message in commands:
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        p=subprocess.run(argv,cwd=HERE,text=True,capture_output=True)
        record={'label':label,'actual_argv':argv,'cwd':str(HERE),'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode,'expected_returncode':expected,'stdout':p.stdout,'stderr':p.stderr,'controlling_file_sha256':hashlib.sha256(pathlib.Path(argv[2] if argv[1]=='-O' else argv[1]).read_bytes()).hexdigest()}
        records.append(record);(HERE/'RAW_ADVERSARIAL_RECORDS.json').write_text(json.dumps(records,indent=2)+'\n')
        print(label,'exit',p.returncode,flush=True)
        need(p.returncode==expected,'unexpected child status; raw record preserved')
        if message:need(message in p.stderr,'expected guard message absent; raw record preserved')
    stable=lambda x:{k:v for k,v in x.items() if k not in ('utc_completed','elapsed_seconds','python')}
    normal=json.loads(records[0]['stdout']);optimized=json.loads(records[1]['stdout'])
    published=json.loads((PRIVATE/'sealed_validator/certificate_N13_M65536.json').read_text())
    need(stable(normal)==stable(optimized)==stable(published),'fresh normal/optimized/producer certificate arithmetic mismatch')
    sampling=json.loads(records[-1]['stdout'])
    need(sampling['status']=='CERTIFIED','sampling mutant unexpectedly noncertifying')
    # Independent exact rejection: at N=2 and a positive finite cell width,
    # the center sample is 4 but its mean is 8-4*sinc(2π/M)>4.
    # The strict inequality follows from sin(t)<t for 0<t<π, without floats.
    summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_hash':EXPECTED,'normal_optimized_and_producer_stable_fields_match':True,'fresh_N13_strict_integer_margin':normal['strict_integer_margin'],'fresh_N13_upper_display':normal['normalized_integral_upper_display'],'fault_controls':[{'label':label,'actual_exit':records[3+j]['returncode'],'guard_message':message,'arithmetic_rejected':expected==1} for j,(label,_,_,expected,message) in enumerate(changes)],'sampling_mutant':{'actual_status':sampling['status'],'display':sampling['normalized_integral_upper_display'],'independent_analytic_rejection':True,'counterexample':'N=2, S(x)=8−4cos(4πx). On the cell centered at 0, exact mean=8−4sinc(2π/M)>4=S(0); a sample is not an upper cell mean.','interpretation':'Runtime guards alone do not establish Jensen premises; immutable code plus analytic derivation is essential. This is a deliberately invalid altered program, not a failure of the sealed program.'},'unexpected_child_failures':0,'intentional_guard_rejections':3,'deliberately_invalid_analytic_route_that_passed_internal_guards':1}
    (HERE/'EXECUTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('All fresh arithmetic reproductions and targeted control expectations matched.')
if __name__=='__main__':main()
