from pathlib import Path
import hashlib,subprocess
A=Path(__file__).resolve().parent;S=A/'current_preparation_family';R=A.parents[2]
def main():
    assert __debug__; (A/'ROOT_CURRENT_LAUNCHER_PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    builder=S/'prepare_current_packet.py';operator=S/'capture_root_builder_operation.py'
    assert hashlib.sha256(builder.read_bytes()).hexdigest()=='7bde800ce050ddf1a9ac071ff54551813e87309eae9834805b3ef632b4342aff'
    assert hashlib.sha256(operator.read_bytes()).hexdigest()=='7f9c717bd3b8ef32160d4388f38ddaf3617c04c1e5c8c3884dd04725684acd3f'
    argv=['/usr/bin/python3','-B',str(operator),'--execute','--expected-builder-sha256',hashlib.sha256(builder.read_bytes()).hexdigest()]
    for flag,name in [('root-scope-certificate','ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md'),('root-read-ledger','ROOT_PRIMARY_READ_LEDGER.json'),('root-science-card','ROOT_SCIENCE_CARD.json'),('root-current-input-manifest','ROOT_CURRENT_INPUT_PREIMAGES.json'),('root-evidence-bindings','ROOT_EVIDENCE_BINDINGS.json')]:argv.extend(['--'+flag+'-sha256',hashlib.sha256((A/name).read_bytes()).hexdigest()])
    subprocess.run(argv,cwd=R,stdin=subprocess.DEVNULL,check=True)
if __name__=='__main__':main()
