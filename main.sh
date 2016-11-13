#!/bin/bash

echo -n "Enter subject ID: "
read subject_ID
echo -n "Choose condition: diffuse (d), clustered (c), or random (r): "
read condition

./EBR_1.py $subject_ID $condition

./scrabble_practice.py  $subject_ID $condition
./scrabble_pretest.py $subject_ID $condition

./visual_foraging_practice.py $subject_ID $condition
./intro_foraging.py $subject_ID $condition
./visual_foraging.py $subject_ID $condition

./EBR_2.py $subject_ID $condition

./scrabble_posttest.py $subject_ID $condition

./EBR_3.py $subject_ID $condition

./bisbas.py $subject_ID
