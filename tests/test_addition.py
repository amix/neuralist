import time
import csv
import os

from neuralist import NeuralNetwork

DATA_PATH = os.path.join('tests', 'datasets', 'addition.csv')

nn = NeuralNetwork('additions',
                   type='regressor',
                   inputs=('number1', 'number2'),
                   outputs=('result',),
                   hidden_layers=(3,),
                   dataset_size=50,
                   testset_size=10)

# --- CSV data
csv_data = []
with open(DATA_PATH) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        input = {'number1': int(row['number1']), 'number2': int(row['number2'])}
        output = {'result': int(row['result'])}
        csv_data.append((input, output))

# --- Training dataset
train_dataset = csv_data[0:90]
for input, output in train_dataset:
    nn.observe_train(input, output)

# --- Testing dataset
test_dataset = csv_data[90:]
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
    nn_output = nn.run(input)
    print('NN calculation %s+%s = %s' % (input['number1'],
                                         input['number2'],
                                         nn_output['result']))
    if int(float(nn_output['result'])) != output['result']:
        errors += 1

print('%s prediction errors on %s test items' % (errors, len(test_dataset)))
