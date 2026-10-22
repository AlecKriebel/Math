#!/usr/bin/env python3
"""Exact old false-uniqueness, all4columns, both root digest states, no providers."""
from contextlib import ExitStack
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch
import controls_support as S


def main():
    B,P,G,V,D=S.implementation(True)
    cases=[]
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',S.forbidden));guards.enter_context(patch.object(socket,'socket',S.forbidden))
        guards.enter_context(patch.object(V,'urlopen',S.forbidden))
        for method in ['request','create','upload','update','publish','get']:
            guards.enter_context(patch.object(B.zenodo.ZenodoClient,method,S.forbidden))
        with tempfile.TemporaryDirectory(dir=S.HERE,prefix='old_synthetic_') as temp:
            root=Path(temp)
            for alias in ['https://zenodo.org/record/999/','https://zenodo.org:443/records/999',
                          'https://zenodo.org/records/./999','https://zenodo.org/records/999/export/json']:
                for column in range(4):
                    for exempt in [False,True]:
                        row=['','','',''];row[column]=alias
                        result=S.run_pipeline(root/str(len(cases)),(B,P,G,V,D),[row],False,exempt)
                        S.check(result['collector_matching_rows']==0 and result['gate_accepted'] and result['append_calls']==1 and result['append_returned_verified'],'old duplicate and false uniqueness must reproduce')
                        cases.append({'alias':alias,'column':column+1,'root_digest_exemption':exempt,**result})
    S.check(not S.ATTEMPTS,'zero real provider attempts')
    result={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'old122_manifest_sha256':'5a40e164c22bf6000720f3fa6ccfda6af1fa9de2fb35d1358243e021ad948200',
            'old_false_uniqueness_reproductions':len(cases),'actual_provider_access_attempts':len(S.ATTEMPTS),'cases':cases}
    S.write(S.HERE/('OLD_COUNTEREXAMPLES_OPTIMIZED.json' if sys.flags.optimize else 'OLD_COUNTEREXAMPLES.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
