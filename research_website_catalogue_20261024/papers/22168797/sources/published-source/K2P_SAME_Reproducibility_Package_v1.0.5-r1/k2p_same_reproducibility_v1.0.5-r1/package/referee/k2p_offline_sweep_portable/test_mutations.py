#!/usr/bin/env python3
"""Fail-closed mutation tests for the portable schema-v3 sweep driver."""
from __future__ import annotations

if not __debug__:
    raise SystemExit("K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN")

import argparse, importlib.util, json, pathlib, subprocess, sys, tempfile


def load_driver(path):
    spec=importlib.util.spec_from_file_location('portable_driver',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def run(cmd):return subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
def must_fail(result,needle):
    if result.returncode==0 or needle not in result.stdout:raise AssertionError((needle,result.returncode,result.stdout))
def rehash(mod,data):
    data['semantic_record_sha256']=mod.semantic_payload_hash(data)
    data['record_payload_sha256']=mod.payload_hash(data)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--package-root');args=parser.parse_args()
    root=pathlib.Path(args.package_root or pathlib.Path(__file__).resolve().parent).resolve();driver=root/'resumable_four_port_driver.py'
    mod=load_driver(driver)
    with tempfile.TemporaryDirectory(prefix='k2p_driver_mut_') as tmp:
        base=[sys.executable,str(driver),'--package-root',str(root),'--source-index','0','--start','206','--end','210','--output-root',tmp]
        subprocess.run(base,check=True,stdout=subprocess.PIPE,text=True)
        record=pathlib.Path(tmp)/'source_0'/'records'/'class_000206.json';original=record.read_text()

        # 1. Mathematical status edited without updating the self-hash.
        data=json.loads(original);data['status']='isomorphic';record.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
        must_fail(run(base),'record_payload_sha256');record.write_text(original)

        # 2. Canonicalizer binding edited and self-hash recomputed.
        data=json.loads(original);data['canonicalizer_sha256']='f'*64;rehash(mod,data);record.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
        must_fail(run(base),'canonicalizer_sha256');record.write_text(original)

        # 3. Source graph binding edited and self-hash recomputed.
        data=json.loads(original);data['source_graph_sha256']='e'*64;rehash(mod,data);record.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
        must_fail(run(base),'source_graph_sha256');record.write_text(original)

        # 4. Hard-case certificate removed and self-hash recomputed.
        data=json.loads(original);data['certificate']=None;data['certificate_payload_sha256']=None;rehash(mod,data);record.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
        # Record validation accepts shape only if status remains separated? It must reject certificate hash or required field semantics.
        result=run(base)
        if result.returncode==0:raise AssertionError('missing hard certificate accepted')
        record.write_text(original)

        # 5. Truncated JSON must fail, never be silently regenerated/reused.
        record.write_text('{"schema":');result=run(base)
        if result.returncode==0:raise AssertionError('truncated record accepted')
        record.write_text(original)

        # 6. Wrong command-line lock pins.
        must_fail(run(base+['--expected-compiler-sha256','0'*64]),'compiler hash mismatch')
        must_fail(run(base+['--expected-canonicalizer-sha256','0'*64]),'canonicalizer hash mismatch')

        # 7. A cubic coefficient cannot be changed and rehashed into a
        # reusable exact certificate.  The fixed four-port universe has cubic
        # cases only at source 5, classes 9 and 10.
        cubic_base=[sys.executable,str(driver),'--package-root',str(root),'--source-index','5','--start','9','--end','11','--output-root',tmp]
        subprocess.run(cubic_base,check=True,stdout=subprocess.PIPE,text=True)
        cubic_record=pathlib.Path(tmp)/'source_5'/'records'/'class_000009.json'
        cubic_original=cubic_record.read_text();data=json.loads(cubic_original)
        data['certificate']['coefficients'][0]+=1
        data['certificate_payload_sha256']=mod.sha_object(data['certificate'])
        rehash(mod,data);cubic_record.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
        must_fail(run(cubic_base),'cubic case binding');cubic_record.write_text(cubic_original)
    print('PORTABLE_DRIVER_MUTATIONS_PASS')

if __name__=='__main__':main()
