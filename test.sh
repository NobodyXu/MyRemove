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

call_myremove() {
    calling_convention=$1
    word=$2

    if [ $calling_convention = argv ]; then
        $myremove $test_dir $word
    elif [ $calling_convention = stdin ]; then
        echo -e "${test_dir}\n${word}" | $myremove
    fi
}

for calling_convention in argv stdin; do
    mkdir -p $test_dir
    rm -rf ${test_dir}/*
    
    generate_testfiles a .file
    
    # Now run the test for prefix
    call_myremove $calling_convention a prefix
    [ $? -ne 0 ] && die prefix
    assertNotExist 'a*'
    
    # Now run the test for postfix
    call_myremove $calling_convention .file
    [ $? -ne 0 ] && die postfix
    assertNotExist '*.file'
    
    generate_testfiles a
    # Now rerun the test, it should fail
    call_myremove $calling_convention a
    [ $? -eq 0 ] && die no-overwrite
    
    echo -e "\nAll test passed!"
done
