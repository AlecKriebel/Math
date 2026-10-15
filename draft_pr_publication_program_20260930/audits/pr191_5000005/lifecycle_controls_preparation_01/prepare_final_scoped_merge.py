"""PROPOSED fresh-MAIN/original-head two-parent integration; never moves refs."""
import json,sys
from lifecycle_common import integration_prepare,integration_accept
if __name__=='__main__':
 if sys.argv[1]=='prepare':out=integration_prepare(sys.argv[2])
 elif sys.argv[1]=='accept':out=integration_accept()
 else:raise RuntimeError('Unknown action')
 print(json.dumps(out))
