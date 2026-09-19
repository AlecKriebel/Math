#!/usr/bin/env python3
"""Bounded actual module compilation; logs bind source/import object bytes."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,sys,time
AUDIT=Path(__file__).resolve().parent
ROOT=AUDIT.parent/'lean'
sys.path.insert(0,str(ROOT/'scripts'))
from audit_support import inventory,closure
from build_serial import run_process
OUT=AUDIT/'embedding_rows'
OUT.mkdir(exist_ok=True)
INV=inventory(ROOT)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs(module):
    result={}
    for m in sorted(closure(INV,module)):
        stem=Path(*m.split('.'))
        p=ROOT/stem.with_suffix('.lean')
        result[str(p.relative_to(ROOT))]=sha(p)
        if m!=module:
            p=ROOT/'.lake/build/lib/lean'/stem.with_suffix('.olean')
            result[str(p.relative_to(ROOT))]=sha(p)
    return result

def run(i):
    name=f'Chunk{i:02}'
    module=f'Kourovka.Lattice.Checks.{name}'
    src=f'Kourovka/Lattice/Checks/{name}.lean'
    obj=ROOT/'.lake/build/lib/lean'/Path(src).with_suffix('.olean')
    obj.parent.mkdir(parents=True,exist_ok=True)
    obj.unlink(missing_ok=True)
    before=inputs(module)
    args=['lake','env','lean','-j1','-s65536','-o',str(obj),src]
    start=time.monotonic()
    code,output,timed=run_process(args,cwd=ROOT,timeout=1800)
    (OUT/f'{name}.log').write_text(output)
    after=inputs(module)
    okay=code==0 and not timed and obj.exists() and obj.stat().st_size>0 and before==after
    record={'module':module,'command':args,'returncode':code,'timeout':timed,
            'seconds':time.monotonic()-start,'accepted':okay,'input_hashes':before,
            'inputs_unchanged':before==after,'object_sha256':sha(obj) if obj.exists() else None}
    (OUT/f'{name}.json').write_text(json.dumps(record,indent=2)+'\n')
    print(f'{name}: accepted={okay} exit={code} seconds={record["seconds"]:.1f}',flush=True)
    return record

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(run,range(2,31)))
    summary={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'workers':2,'results':results,'all_passed':all(x['accepted'] for x in results)}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    sys.exit(0 if summary['all_passed'] else 2)
