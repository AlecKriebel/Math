from pathlib import Path
import sys,subprocess,json
root=Path(__file__).resolve().parent
rows=[]
for name in ['exact_certificates.py','parity_controls.py']:
    for optimized in [False,True]:
        cmd=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(root/'mutation_runner.py'),name]
        p=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
        expected='exact check failed: physical paired focal-distance factorization' if name.startswith('exact') else 'parity check failed at source-audit line 20'
        row={'script':name,'optimized':optimized,'exit':p.returncode,'substantive_false_identity_rejected':p.returncode!=0 and expected in p.stderr,'no_success_certificate_written':not any((root/('mutation_output_'+name.removesuffix('.py'))).glob('*.json'))}
        rows.append(row)
        if not(row['substantive_false_identity_rejected'] and row['no_success_certificate_written']):raise RuntimeError(str(row))
(root/'MUTATION_CHECKS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
