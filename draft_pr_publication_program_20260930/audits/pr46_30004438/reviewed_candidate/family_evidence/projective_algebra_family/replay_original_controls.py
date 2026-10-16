from pathlib import Path
import hashlib
import json
import sys

root=Path(__file__).resolve().parent
snapshot=root.parent/'source_snapshot'
selection=sys.argv[1]
choices={'author':('verify.py','verification.json'),
         'prior_review':('independent_review/independent_checks.py','independent_review/independent_results.json')}
source_name,result_name=choices[selection]
source=snapshot/source_name
body=source.read_bytes()
source_sha=hashlib.sha256(body).hexdigest()
expected={'author':'f774bc1e4b3ba1412d0973e12baeef087ed580f1b0a14d353dcd968dceeb9908',
          'prior_review':'a8c18a6f181a703e593d91d7af27348bcfcc79822b3f2b16e9025e3ea3e7be8d'}
assert source_sha==expected[selection]
# Execute exactly the frozen source bytes. Redirect only its __file__ output base,
# because both original programs write their receipt beside __file__. The source
# is not copied or patched; compile uses its actual immutable path for tracebacks.
destination=root/('replay_'+selection)
destination.mkdir(exist_ok=True)
namespace={'__name__':'__main__','__file__':str(destination/source.name)}
exec(compile(body,str(source),'exec'),namespace)
output=destination/Path(result_name).name
original=snapshot/result_name
assert output.read_bytes()==original.read_bytes()
print(json.dumps({'replay_selection':selection,'unmodified_source_sha256':source_sha,
                  'redirected___file__':namespace['__file__'],
                  'receipt_byte_identical':True,
                  'receipt_sha256':hashlib.sha256(output.read_bytes()).hexdigest()},indent=2))
