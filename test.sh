#!/bin/bash

repo=$(dirname $0)
myremove=${repo}/myremove.py
test_dir=/tmp/test

generate_testfiles() {
    prefix=$1
    postfix=$2
    # Generate test files
    mkdir -p ${test_dir}/inner/
    for num in $(seq 1 20); do
        touch ${test_dir}/${prefix}${num}${postfix} ${test_dir}/inner/a${num}.file
    done
}

die() {
    echo test $1 failed!
    exit 1
}

assertNotExist() {
    [ -n "$(find $test_dir -name '$1')" ] && die prefix
}

mkdir -p $test_dir
rm -rf ${test_dir}/*

generate_testfiles a .file

# Now run the test for prefix
echo -e "${test_dir}\na" | $myremove || die prefix
assertNotExist 'a*'

# Now run the test for postfix
echo -e "${test_dir}\n.file" | $myremove || die postfix
assertNotExist '*.file'

generate_testfiles a
# Now rerun the test, it should fail
echo -e "${test_dir}\na" | $myremove && die no-overwrite

echo -e "\nAll test passed!"
