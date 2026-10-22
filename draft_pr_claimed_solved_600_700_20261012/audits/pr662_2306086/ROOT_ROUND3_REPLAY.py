from pathlib import Path
import types
A=Path(__file__).absolute().parent
source=A/'reviews/package_round3/independent_checks.py'
m=types.ModuleType('_root_round3_replay');m.__file__=str(source)
exec(compile(source.read_bytes(),str(source),'exec'),m.__dict__)
m.HERE=A/'tmp/root-round3-replay';m.HERE.mkdir(parents=True,exist_ok=True)
m.TMP=m.HERE/'tmp';m.TMP.mkdir(exist_ok=True)
old=A/'reviews/package_round3/tmp/prepare_integration.before_timestamp_repair.py'
(m.TMP/old.name).write_bytes(old.read_bytes())
m.main()
