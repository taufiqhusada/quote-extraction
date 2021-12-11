#!/bin/sh
# GNU All-Permissive License

RDQUO=$(echo -ne '\u201C\u201D')
sed -i -e "s/[$RDQUO]/\"/g" "${1}"
