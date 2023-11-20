#!/bin/bash
mkdir -p tests

for seed in $(seq 255)
do
	python3 ./trivia.py $seed > tests/$seed.start.txt
done


