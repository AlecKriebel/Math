"""PROPOSED merged-scope and combined-current-map factual acceptance."""
import json,sys
from lifecycle_common import factual_prepare,factual_accept
if __name__=='__main__':
 if sys.argv[1]=='prepare':out=factual_prepare(sys.argv[2])
 elif sys.argv[1]=='accept':out=factual_accept()
 else:raise RuntimeError('Unknown action')
 print(json.dumps(out))
