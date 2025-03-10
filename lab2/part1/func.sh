#!/bin/bash

function func {
    echo "Called with $# parameters."
    i=1
    for param in $@; do
        echo "Parameter $i is $param"
        let i=i+1
    done
    return 139
}

func hello world 83.6
echo "$?"