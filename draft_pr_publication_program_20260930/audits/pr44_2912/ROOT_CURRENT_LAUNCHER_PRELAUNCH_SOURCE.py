from pathlib import Path
import hashlib,subprocess
A=Path(__file__).resolve().parent;S=A/'current_preparation_family';R=A.parents[2]
def main():
    assert __debug__; (A/'ROOT_CURRENT_LAUNCHER_PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    builder=S/'prepare_current_packet.py';operator=S/'capture_root_builder_operation.py'
    assert hashlib.sha256(builder.read_bytes()).hexdigest()=='09948a4ca10ef5014cdd35ec75ea82bf10887a5fd6ec9400fee0239fcc04983d'
    assert hashlib.sha256(operator.read_bytes()).hexdigest()=='fe0f02ceea16a15895073bda8851a9b67baaf6f02c5da55bfe13a06dc01733ec'
    argv=['/usr/bin/python3','-B',str(operator),'--execute','--expected-builder-sha256',hashlib.sha256(builder.read_bytes()).hexdigest()]
    for flag,name in [('root-scope-certificate','ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md'),('root-read-ledger','ROOT_PRIMARY_READ_LEDGER.json'),('root-science-card','ROOT_SCIENCE_CARD.json'),('root-current-input-manifest','ROOT_CURRENT_INPUT_PREIMAGES.json'),('root-evidence-bindings','ROOT_EVIDENCE_BINDINGS.json')]:argv.extend(['--'+flag+'-sha256',hashlib.sha256((A/name).read_bytes()).hexdigest()])
    subprocess.run(argv,cwd=R,stdin=subprocess.DEVNULL,check=True)
if __name__=='__main__':main()
