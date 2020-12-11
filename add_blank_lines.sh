#!/usr/bin/bash

# This script is used to add a blank line before every closing } bracket
# It is used for source files formatted by clang-format which deletes
# blank lines before closing } brackets

# clang-format also deletes blank lines after public/protected/private:
# so this script also undoes this action of clang-format

if [[ $# -ne 1 ]]; then
    echo "Please provide file name!"
    exit 0
fi

file=$1
if [[ ! -f $file ]]; then
    echo "ERROR: File $file not found!"
    exit 1
fi

# The awk command that does the work
awk -v closing_pat='^[ \t]*}[ \t;]*$' \
-v blank_line='^[ \t]*$' \
-v opening_pat='^[ \t]*{[ \t]*$' \
-v access_kw='^[ \t]*(public|protected|private)[ \t]*:[ \t]*$' \
'{
  if ($0 ~ closing_pat) {
    if (b !~ blank_line && b !~ opening_pat && b !~ access_kw) print "\n" $0; else print $0
  } else if ($0 ~ access_kw) {
    print $0 "\n"
  } else print $0
}
{b=$0}' $file > cf.tmp && mv cf.tmp $file
