#!/bin/bash

repo=$(dirname $0)
myremove=${repo}/myremove.py
test_dir=/tmp/test

generate_testfiles() {
    # Generate test files
    for num in $(seq 1 20); do
        touch ${test_dir}/a${num}.file
    done
}

die() {
    echo test $1 failed!
    exit 1
}

mkdir -p $test_dir
rm -rf ${test_dir}/*

generate_testfiles

# Now run the test, it should success
echo -e "${test_dir}\na" | $myremove || die

generate_testfiles
# Now run the test, it should fail
echo -e "${test_dir}\na" | $myremove && die

echo -e "\nAll test passed!"
