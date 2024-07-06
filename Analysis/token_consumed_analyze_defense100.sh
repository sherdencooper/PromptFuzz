#! /bin/bash

log_dir='/home/hwmiao/PromptFuzz/PromptFuzz/Logs/focus/extraction/'
iter=(1 2 3)
for i in "${iter[@]}";do
    log_subdir=${log_dir}finetuned1_single_${i}
    save_subdir=${log_dir}finetuned1_token_${i}
    mkdir -p $save_subdir
    for line in `ls $log_subdir`;do
        cat $log_subdir/$line |grep 'token usage' > ${save_subdir}/$line
    done
done
    
