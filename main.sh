#!/bin/bash

echo -n "Enter subject ID: "
read subject_ID
echo -n "Choose condition: diffuse (d), clustered (c), or random (r): "
read condition
echo -n "Debug (f = false, t = true): "
read debug

./EBR_1.py $subject_ID $condition $debug

./scrabble_practice.py  $subject_ID $condition $debug
./scrabble_pretest.py $subject_ID $condition $debug

./visual_foraging_practice.py $subject_ID $condition $debug
./intro_foraging.py $subject_ID $condition $debug
./visual_foraging.py $subject_ID $condition $debug

./EBR_2.py $subject_ID $condition $debug

./scrabble_posttest.py $subject_ID $condition $debug

./EBR_3.py $subject_ID $condition $debug

./bisbas.py $subject_ID
