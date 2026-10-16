import argparse
import io
import sys
import zipfile
sys.dont_write_bytecode=True
from safety import ROOT, verify_payload, fresh_output, member, write_new

def archive_bytes():
    data=verify_payload();names=sorted(['MANIFEST.json']+[r['path'] for r in data['records']])
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as archive:
        for name in names:
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.create_system=3
            info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED
            archive.writestr(info,member(name).read_bytes())
    return buffer.getvalue()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args()
    out=fresh_output(args.out);payload=archive_bytes();write_new(out,payload)
    print('PASS: wrote closed deterministic stored ZIP ('+str(len(payload))+' bytes)')
if __name__=='__main__': main()
