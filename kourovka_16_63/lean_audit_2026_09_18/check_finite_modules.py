"""Compile production finite modules sequentially; requires Integral.olean first."""
from pathlib import Path
import subprocess, json, time
ROOT = Path(__file__).resolve().parent.parent / 'lean'
OUT = Path(__file__).resolve().parent
modules = [
    'Kourovka/Finite/AdditiveLinear',
    'Kourovka/Finite/BracketTrees',
    'Kourovka/Finite/Coordinates',
    'Kourovka/Finite/LieAutomorphisms',
    'Kourovka/Finite/PadicQuotient',
    'Kourovka/Finite/Nilpotency',
    'Kourovka/Lattice/NearIdentity',
]
results = []
for module in modules:
    obj = ROOT / '.lake/build/lib/lean' / (module + '.olean')
    obj.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['lake','env','lean','-j1',module+'.lean','-o',str(obj)]
    start = time.time()
    run = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = OUT / ('finite_' + Path(module).name + '.log')
    log.write_text(run.stdout)
    row = {'module':module, 'exit_code':run.returncode, 'elapsed_seconds':time.time()-start, 'log':log.name}
    results.append(row)
    (OUT/'finite_compile_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(row),flush=True)
    if run.returncode:
        print(run.stdout,flush=True)
        raise SystemExit(run.returncode)
