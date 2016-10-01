import time
import csv
import os

from neuralist import NeuralNetwork

DATA_PATH = os.path.join('tests', 'datasets', 'titanic.csv')

INPUTS = ('class1', 'class2', 'class3',
          'female', 'male', 'age',
          'sibsp', 'parch', 'fare')
OUTPUTS = ('dead', 'alive')

nn = NeuralNetwork('titanic',
                   type='classifier',
                   inputs=INPUTS,
                   outputs=OUTPUTS,
                   hidden_layers=(15,),
                   dataset_size=1000,
                   testset_size=500)

# --- CSV data
csv_data = []
with open(DATA_PATH) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not row['age']:
            continue

        pclass = int(row['pclass'])
        input = {'class1': pclass == 1 and 1 or 0,
                 'class2': pclass == 2 and 1 or 0,
                 'class3': pclass == 3 and 1 or 0,
                 'female': row['sex'] == 'female' and 1 or 0,
                 'male': row['sex'] == 'male' and 1 or 0,
                 'age': float(row['age']),
                 'sibsp': float(row['sibsp']),
                 'parch': float(row['parch']),
                 'fare': float(row['fare'])}

        survival = int(row['survival'])
        output = {'dead': survival == 0 and 1 or 0,
                  'alive': survival == 1 and 1 or 0}

        csv_data.append((input, output))

# --- Training dataset
train_dataset = csv_data[0:600]
for input, output in train_dataset:
    nn.observe_train(input, output)

# --- Testing dataset
test_dataset = csv_data[600:]
for input, output in test_dataset:
    nn.observe_test(input, output)

# --- Train
nn.train()

while nn.is_training():
    print('Training...')
    time.sleep(1)

# --- Test
errors = 0
for input, output in test_dataset:
    nn_output = nn.classify(input)
    if not output[nn_output]:
        errors += 1

print('%s prediction errors on %s test items' % (errors, len(test_dataset)))
