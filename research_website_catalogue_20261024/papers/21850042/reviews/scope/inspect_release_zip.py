"""Own read-only ZIP-directory preview; no source program execution/extraction."""
from pathlib import Path, PurePosixPath
import collections
import datetime
import hashlib
import json
import stat
import zipfile

O=Path(__file__).resolve().parent
S=O.parents[1]/'sources'
prefix='AlecKriebel-Math-dec8693/universal_simultaneous_amplification/'
target=prefix+'phase4_landmark_closure/paper_lower_threshold/output/pdf/simultaneous_amplification_below_three_halves.pdf'
archive=S/'cache/original-release.zip'
with zipfile.ZipFile(archive) as z:
    seen=set();duplicates=[];unsafe=[];nonregular=[];selected=[];metadata=hashlib.sha256()
    for ordinal,x in enumerate(z.infolist()):
        p=PurePosixPath(x.filename);canonical='/'.join(p.parts)
        if canonical in seen:duplicates.append(x.filename)
        seen.add(canonical)
        if p.is_absolute() or '..' in p.parts or '\\' in x.filename:unsafe.append(x.filename)
        mode=x.external_attr>>16
        if not x.is_dir() and stat.S_IFMT(mode) not in (0,stat.S_IFREG):nonregular.append(x.filename)
        row={'ordinal':ordinal,'filename':x.filename,'compressed_bytes':x.compress_size,
             'uncompressed_bytes':x.file_size,'CRC32':f'{x.CRC:08x}',
             'flag_bits':x.flag_bits,'compression':x.compress_type,
             'external_attributes':x.external_attr,'local_header_offset':x.header_offset,
             'ZIP_date_time':list(x.date_time),'directory':x.is_dir()}
        metadata.update(json.dumps(row,separators=(',',':')).encode()+b'\n')
        if x.filename.startswith(prefix):selected.append(row)
    regular=[x for x in selected if not x['directory']]
    summary={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'whole_original_archive':str(archive),'scope':'Entire directory structurally inventoried; no unrelated body read/extracted/CRC replay. Complete target project selected for safe intake.',
      'global_entries':len(z.infolist()),'global_uncompressed_bytes':sum(x.file_size for x in z.infolist()),
      'global_directory_metadata_SHA256':metadata.hexdigest(),
      'global_duplicate_canonical_names':duplicates,'global_unsafe_names':unsafe,
      'global_nonregular_payload_names':nonregular,
      'selected_target_prefix':prefix,'selected_regular_members':len(regular),
      'selected_uncompressed_bytes':sum(x['uncompressed_bytes'] for x in regular),
      'selected_compressed_bytes':sum(x['compressed_bytes'] for x in regular),
      'selected_main_PDF_member':target,'selected_main_PDF_present':target in z.namelist(),
      'all_selected_central_entries_in_original_order':selected}
    (S/'release-directory-preview.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='all_selected_central_entries_in_original_order'},indent=2))
    print('Target paper source path candidates:')
    print('\n'.join(x['filename'] for x in regular if 'paper_lower_threshold/' in x['filename']))
