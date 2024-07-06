import csv
import os
import json
import ast
import statistics
    
    

if __name__ == '__main__':
    csv_dir = '../Analyze_results/'
    file_list = ['finetuned1_focus_attack_result_defense100_1.csv','finetuned1_focus_attack_result_defense100_2.csv','finetuned1_focus_attack_result_defense100_3.csv']
    results = list()
    success_count_list = []
    mean_query_list = list()
    mean_token_list = list()
    for (i,csv_file) in enumerate(file_list):
        success_count = 0
        all_count = 0
        query_list = list()
        token_list = list()
        csv_path = os.path.join(csv_dir,csv_file)
        with open(csv_path) as f:
            reader = csv.reader(f)
            rows = list(reader)
            all_count = len(rows) - 1
            for row in rows:
                if row[0]=='defense_index':
                    continue
                if row[1]=="":
                    row[-3] = "1000"
                else:
                    success_count += 1 
                query_list.append(int(row[-3]))
                token_list.append(int(row[-1])) 
        #success_rate = round(success_count / all_count, 2)
        mean_queries = round(sum(query_list) / len(query_list), 2)
        mean_tokens = round(sum(token_list) / len(token_list), 2)    
        success_count_list.append(success_count)
        mean_query_list.append(mean_queries)
        mean_token_list.append(mean_tokens)
        results.append([i,all_count,success_count,mean_queries,mean_tokens])
    print(mean_query_list)
    print(mean_token_list)
    mean0 = statistics.mean(success_count_list)
    std0 = statistics.stdev(success_count_list)
    mean1 = statistics.mean(mean_query_list)
    std1 = statistics.stdev(mean_query_list)
    mean2 = statistics.mean(mean_token_list)
    std2 = statistics.stdev(mean_token_list)
    print(mean0)
    print(std0)
    print(mean1)
    print(std1)
    print(mean2)
    print(std2)
    with open('../Analyze_results/finetuned1_focus_attack_static_defense100.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['attempt','all_count','success_count','mean_queries','mean_tokens'])
        for result in results:
            writer.writerow(result)
    
    
