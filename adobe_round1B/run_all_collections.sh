#!/bin/bash

for i in 1 2 3
do
    echo "Running Collection $i"
    docker run --rm \
        -v "$(pwd)/Collection $i/PDFs:/app/input" \
        -v "$(pwd)/Collection $i:/app/output" \
        -v "$(pwd)/Collection $i/challenge1b_input.json:/app/challenge1b_input.json" \
        adobe1b
done

echo "All collections processed successfully!"
echo "You can find the output files in their respective Collection directories."
