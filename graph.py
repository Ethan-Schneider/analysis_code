import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


directory = os.fsencode('user_data/')
json_files = [json_file for json_file in os.listdir(directory)]

data = pd.DataFrame(columns=['id', 'study_condition','scenario', 'difficulty', 'error_type', 'exit_condition', 'num_foils', 'elapsed_time', 'Ds', 'D_user_belief', 
                             'user_response', 'num_changes', 'start_edit_distance', 'final_edit_distance', 'final_system_makespan'])
threshold_values = []

index = 0
ids = []
for js in json_files:
    with open(os.path.join(directory, js)) as f:
        if 'gitignore' in f.name.decode():
            continue
        json_text = json.load(f)
        id = js.decode().replace('.json', '')
        ids.append(id)
        for scenario in json_text[id]:
            study_condition = json_text[id][scenario]['study_condition']
            difficulty = json_text[id][scenario]['difficulty']
            error_type = json_text[id][scenario]['error_type']
            exit_condition = json_text[id][scenario]['exit_condition']
            number_of_foils = json_text[id][scenario]['number_of_foils']
            elapsed_time = json_text[id][scenario]['elapsed_time']
            Ds = json_text[id][scenario]['Ds']
            D_user_belief = json_text[id][scenario]['D_user_belief']
            user_response = json_text[id][scenario]['user_response']
            num_changes = json_text[id][scenario]['num_changes']
            start_edit_distance = json_text[id][scenario]['start_edit_distance']
            final_edit_distance = json_text[id][scenario]['final_edit_distance']
            final_system_makespan = json_text[id][scenario]['final_system_makespan']
            data.loc[index] = [id, study_condition, scenario, difficulty, error_type, exit_condition, number_of_foils, elapsed_time, Ds, D_user_belief, user_response, num_changes, start_edit_distance, final_edit_distance, final_system_makespan]
            # threshold_values.append(json_text[id][scenario]['threshold_data'])
            index += 1
        

p1 = data[data['scenario'] != 'warmup_1']
p2 = p1[p1['scenario'] != 'warmup_2']

data = p2

data = data[data['num_changes'] != 'N/A']
data = data[data['final_edit_distance'] != 'N/A']
data = data[data['start_edit_distance'] == 5]
# data = data[data['scenario'] != 'low_1']
# data
# data[data['scenario']=='low_1']
# data[data['num_changes'] == 0]

condition_1_data = data[data['study_condition'] == 1]
condition_2_data = data[data['study_condition'] == 2]

# Bubble plot: count occurrences of each (final_edit_distance, num_changes) pair for each study condition
for condition_data, label, color in [
    (condition_1_data, 'Condition 1', 'blue'),
    (condition_2_data, 'Condition 2', 'red')
]:
    # Convert columns to numeric (in case they are not)
    x = pd.to_numeric(condition_data['final_edit_distance'])
    y = pd.to_numeric(condition_data['num_changes'])
    # Count occurrences
    grouped = condition_data.groupby(['final_edit_distance', 'num_changes']).size().reset_index(name='count')
    plt.scatter(
        grouped['final_edit_distance'],
        grouped['num_changes'],
        s=grouped['count'] * 60,  # scale bubble size for visibility
        alpha=0.5,
        label=label,
        color=color,
        edgecolors='none'
    )

plt.plot([0, 6], [5, 0], linestyle='--', color='gray')
plt.xlabel('Final Remaining Errors', fontsize=15)
plt.ylabel('Number of Repair Attempts', fontsize=15)
plt.title('Efficiency of User Error Corrections', fontsize=15)
plt.ylim(-2, 38)
plt.xlim(-0.25, 6.25)
# plt.legend()
plt.savefig('bubble_plot.png')