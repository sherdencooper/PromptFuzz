#! /bin/bash


#defense100_index=(1 31 32 37 14 13 3 15 8  21 12 10 23 17 7 34 26 11 9 5 35 6 18 19 29 30 27 16 20 0 33 36 22 28 24 25 2 4)
#defense100_index=(14 13 3 15 8  21 12 10 23 17 7 34 26 11 9 5 35 6 18 19 29 30 27 16 20 0 33 36 22 28 24 25 2 4)
result_dir='/home/hwmiao/PromptFuzz/PromptFuzz/Results/focus/extraction/'
save_dir='/home/hwmiao/PromptFuzz/PromptFuzz/Results/focus/extraction/single/'
mkdir -p $save_dir
index_file=$1
    
while IFS= read -r line; do
    echo "$line"
    bash ./Scripts/focus_attack_single.sh $line
    mv ${result_dir}${line}.csv $save_dir
done < $index_file
     
    
