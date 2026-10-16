"""Run fresh exact finite diagnostics; stdout only; no historical imports."""
import sys
sys.dont_write_bytecode = True
import json
from checks import run

if __name__ == '__main__':
    if sys.argv[1:] == ['--invalid']:
        raise ValueError('deliberate unconditional diagnostic guard')
    if sys.argv[1:]:
        raise ValueError('no output or other arguments accepted; stdout only')
    print(json.dumps(run(), sort_keys=True, indent=2))
