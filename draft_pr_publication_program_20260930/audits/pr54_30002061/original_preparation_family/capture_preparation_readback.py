#!/usr/bin/env python3
"""Actual prep check capture with full prelaunch own code and input snapshots."""
from capture_command import HERE,run
import json,sys
sources=[HERE/n for n in ['verify_preparation.py','packet_common.py','ORIGINAL_AUTHENTICATION.json','SOURCE_ACCOUNTING.json','REPRODUCTION.json']]
cap,out,err=run('preparation_readback',['/usr/bin/python3','-B',str(HERE/'verify_preparation.py')],sources=sources)
print(json.dumps(cap,indent=2,sort_keys=True));sys.exit(cap['exit_code'])
