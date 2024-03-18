import json
import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

def process_prompts(data_path):
    with open(data_path,'r') as f:
        data = [json.loads(line) for line in f.readlines()]
    duplicates,map_dict = check_duplicates(data)
    prompt_cluster = cluster_prompts(duplicates)
    with open('attack_prompt_cluster.csv','w') as f:
        writer = csv.writer(f) 
        writer.writerow(['AttackPrompt','cluster'])
        for key,val in prompt_cluster.items():
            writer.writerow([key,val])
            
    

            
def check_duplicates(data):
    duplicates = dict()
    for (i,json_dict) in enumerate(data):
        attack = json_dict['attack']
        idx = duplicates.get(attack,[])
        all_idx.append(idx)
        duplicates[attack] = all_idx
    return duplicates
    


def _check_duplicates(data):
    duplicates = dict()
    map_dict = dict()
    for (i,json_dict) in enumerate(data):
        attack = json_dict['attack']
        sample_id = json_dict['sample_id']
        sample_ids = duplicates.get(attack,[])
        sample_ids.append(sample_id)
        duplicates[attack] = sample_ids
        if attack not in map_dict.keys():
            map_dict[attack] = i
    return duplicates,map_dict

def cluster_prompts(duplicates):
    prompts = list(duplicates.keys())
    labels = list(cluster(prompts))

    prompt_cluster = dict()
    for i in range(len(prompts)):
        label = labels[i]
        prompt = prompts[i]
        prompt_list = prompt_cluster.get(label,list())
        prompt_cluster[prompt] = label
    return prompt_cluster

def save(duplicates):
    with open('attack_duplicates.csv','w') as f:
        writer = csv.writer(f) 
        writer.writerow(['AttackID','DuplicateNum','SampleID'])
        for key,val in duplicates.items():
            num = len(val)
            attack_id = map_dict[key]
            writer.writerow([attack_id,num,val])

stemmer = PorterStemmer()
 
def preprocess(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    return ' '.join(stemmed_tokens)


def cluster(prompts):
    sentences = [preprocess(text) for text in prompts]
    tfidf = TfidfVectorizer()
    features = tfidf.fit_transform(sentences) 
    db = DBSCAN(eps=0.3, min_samples=5).fit(features)
    labels = db.labels_
    #print(labels)
    return labels

if __name__ == '__main__':
    data_path = './Datasets/extraction_robustness_dataset.jsonl'
    process_prompts(data_path)
    
  
