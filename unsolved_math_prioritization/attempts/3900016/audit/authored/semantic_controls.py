#!/usr/bin/env python3
"""Audit sensitivity controls for the unmodified author checker's math functions.

Each mutation exists in memory only; no source or report file is edited.
Integrity checks are run before mutation, so a hash failure cannot mask a math failure.
"""
import importlib.util
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode=True


def require(ok,message):
    if not ok:raise RuntimeError(message)


def load(path):
    spec=importlib.util.spec_from_file_location('audit_subject',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    require(os.getuid()==os.geteuid()==1000,'actual uid 1000 required')
    path=Path(sys.argv[1]).resolve()
    module=load(path)
    pins=module.verify_pins()
    p5=((0,0),(1,0),(2,1),(1,2),(0,1))
    p6=((0,0),(1,0),(2,1),(2,2),(1,2),(0,1))
    results=[]
    mutations=[
        ('constant triangle area','area2',lambda original:lambda a,b,c:1,
         lambda m:m.mathematics(),'area partition mismatch'),
        ('overstated logarithmic lower bound','bound_G',lambda original:lambda n:original(n)+1,
         lambda m:m.mathematics(),'claimed lower bound exceeds exact optimum'),
        ('overstated packing lower bound','bound_B',lambda original:lambda n:original(n)+1,
         lambda m:m.mathematics(),'packing bound failed'),
        ('missing Catalan triangulation','triangulations',lambda original:lambda i,j:original(i,j)[:-1] if j-i>=2 else original(i,j),
         lambda m:m.spectra(p6),'Catalan count mismatch'),
        ('independent ear generation omitted','ears',lambda original:lambda indices:frozenset(),
         lambda m:m.mathematics(),'independent ear enumeration disagrees'),
        ('normal cross product component corrupted','cross',lambda original:lambda a,b:(original(a,b)[0]+1,)+original(a,b)[1:],
         lambda m:m.lattice_checks(p5),'integer normal multiple failed'),
        ('nonpositive orientation accepted','validate',lambda original:lambda p:None,
         lambda m:m.mathematics(),'expected rejection absent')]
    for label,name,make,run,expected in mutations:
        module=load(path);original=getattr(module,name);setattr(module,name,make(original))
        try:
            run(module)
        except RuntimeError as e:
            require(expected in str(e),'wrong control rejection: '+label+': '+str(e))
            results.append({'label':label,'rejected':True,'diagnostic':str(e)})
        else:
            raise RuntimeError('semantic mutation survived: '+label)
    print(json.dumps({'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),
                     'optimization':sys.flags.optimize,'native_integrity_before_mutations':pins,
                     'controls':results},indent=2,sort_keys=True))


if __name__=='__main__':main()
