#!/usr/bin/env bash

# Et program til at rydde op i data fra mobilepay.dk

# Et CSV fra mobilepay.dk kommer i UTF-16 litte-endian format uden et
# byte-order mark (BOM). Desuden bruger den \r\n som linjeseparator,
# og angiver på første linje at semikolon (;) bruges som
# kolonneseparator. Det lader til at de er glade for Windows hos
# mobilepay.dk..

# Dette program konverterer sådan et CSV til UTF-8 indkodning, fjerner
# \r-tegn, og den første linje. Dernæst fjernes kolonner som
# indeholder personfølsomt og redundant data.

set -euo pipefail

path="$1"

tmp=$(mktemp kantine-data-XXXXXX)
cleanup() {
  rm -f "${tmp}"
}
trap "cleanup" INT TERM EXIT

cat "${path}" \
  | iconv -f UTF-16LE -t UTF-8 \
  | tr -d '\r' \
  | tail -n +2 \
  | cut -d ';' -f1,4,7,8,10,11,12 \
  > "${tmp}"
mv "${tmp}" "${path}"

first=$(head -1 "${path}")
if [ "$first" != \
  "\"Type\";\"Beløb\";\"Dato\";\"Tid\";\"Besked\";\"Gebyr\";" ]
then
  printf "Endte med uforventede kolonne-navne:\n  %s\n" "${first}" 1>&2
  printf "Tjek at der evt. ikke lækkes personfølsomt data.\n" 1>&2
  exit 1
fi
