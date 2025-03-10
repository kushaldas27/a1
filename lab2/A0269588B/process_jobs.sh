#!/bin/bash

# Check if we have enough arguments
if [[ $# -ne 1 ]]; then 
    echo "Usage ./process_jobs.sh <filename>"
    exit 1
fi

# Iterate over every job directory
    # Compile C code
    # Print compile error message to output file
    # Generate output from C code using *.in files
    # Measure the execution time
    # Record any runtime errors
    
function compile {
    command=""
    for file in $(ls *.c); do
        command="$command $file"
    done
    command="$command -o $1"
    gcc $command 2>> logs.txt
}

function run {
    for file in $(ls *.in); do
        start=`gdate +%s.%3N`
        $1 < $file > $file.out 2>> logs.txt
        end=`gdate +%s.%3N`
        runtime=$(echo "$end-$start" | bc)
        total_runtime=$(echo "$total_runtime+$runtime" | bc) 
        echo "Execution time for $path/$file: $runtime seconds" >> logs.txt
    done 
} 

cd jobs
total_jobs=0
successful_compilations=0
total_runtime=0
for folder in $(ls -d */); do
    let total_jobs=$total_jobs+1
    cd $folder
    path="jobs/$folder"
    echo "Processing student job in $path" > logs.txt
    compile $1
    if [[ $? -eq 0 ]]; then
        echo "Compilation successful for $path" >> logs.txt
        let successful_compilations=$successful_compilations+1
        program="./$1"
        run $program
        if [[ $? -eq 0 ]]; then
            echo "Execution completed without errors in $path" >> logs.txt
        else 
            echo "E"
        fi
    else
        echo "Compilation failed for $path" >> logs.txt
    fi
    cd ..
done

# Generate a summary report
echo "Summary Report" > summary_report.txt
echo "Total jobs processed: $total_jobs" >> summary_report.txt
echo "Successful compilations: $successful_compilations" >> summary_report.txt
echo "Failed compilations: $(($total_jobs-$successful_compilations))" >> summary_report.txt
echo "Total runtime of all jobs: $total_runtime seconds" >> summary_report.txt