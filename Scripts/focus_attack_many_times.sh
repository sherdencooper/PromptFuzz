#! /bin/bash
save_dir='./Results/focus/extraction/'
log_dir='/home/hwmiao/PromptFuzz/PromptFuzz/Logs/focus/extraction/coefficient/'
save_dir1='./Results/focus/extraction/coefficient'
log_dir1='/home/hwmiao/PromptFuzz/PromptFuzz/Logs/focus/extraction/coefficient'
mkdir -p $save_dir1
mkdir -p $log_dir1

iters=(0.3 0.5 0.7 0.9)
for i in "${iters[@]}"; do
    echo $i
    bash ./Scripts/focus_attack.sh $i
    mv ${log_dir}all_defenses.log $log_dir1/all_defense_${i}.log
    mv ${save_dir}all_results.csv ${save_dir1}/all_results_${i}.csv
done
