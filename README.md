# neuralist

A Python interface to access [neural-redis](https://github.com/antirez/neural-redis), a neural networks module for Redis.

🚨 This stuff is an alpha stage (like neural-redis), so use it with caution!


# Installation 🚀

To install simply do following:
```
$ pip install neuralist
```


# Example usage

```python
from neuralist import NeuralNetwork

nn = NeuralNetwork('additions',
                   type='regressor',
                   inputs=('number1', 'number2'),
                   outputs=('result',),
                   hidden_layers=(3, ),
                   dataset_size=50,
                   testset_size=10)

nn.observe_train(input={'number1': 1, 'number2': 1},
                 output={'result': 2})
                
nn.train()

while nn.is_training():
    print 'Training...'
    time.sleep(1)

print nn.run({'number': 1, 'number': 2})
```


# API spec

## NeuralNetwork class

The NeuralNetwork object follows the arguments of the `nn.create` command.

Required arguments:
* `name`: (string) The name of the neural network
* `type`: (string) Type of network, can be `'classifier'` or `'regressor'`
* `inputs`: (tuple) The keys of the input dict
* `outputs`: (tuple) The keys of the output dict
* `hidden_layers`: (tuple) zero or more arguments indicating the number of hidden units, one number for each layer.
* `dataset_size`: (int) Max number of data samples in the training dataset
* `testset_size`: (int) Max number of data samples in the testing dataset

Optional arguments.
* `normalize`: (bool) Default `True`. Specify if you want the network to normalize your inputs. Use this if you don't know
* `redis_client`: (Redis.Client) Specify which Redis client to use
* `prefix`: (string) Default `nn:`. Ability to prefix the neural networks, so they don't collide with other keys
* `auto_create`: (bool) Default `True`. Neural network will be auto created if it isn't found



## NeuralNetwork.run(input)

Run the network on the `input`, returning a `dict` as the result.

Required arguments:
* `input`: (dict) The input vector encoded as `dict`


## NeuralNetwork.classify(input)

Run the network on the `input`, returning a class as the result.

Required arguments:
* `input`: (dict) The input vector encoded as `dict`


## NeuralNetwork.observe_train(input, output)

Add a data sample into the training dataset.

Required arguments:
* `input`: (dict) The input vector encoded as `dict`
* `output`: (dict) The output vector encoded as `output`


## NeuralNetwork.observe_test(input, output)

Add a data sample into the testing dataset.

Required arguments:
* `input`: (dict) The input vector encoded as `dict`
* `output`: (dict) The output vector encoded as `output`


## NeuralNetwork.is_training()
Returns `True` if the network is being trained.


## NeuralNetwork.train()
Train a network in a background thread.

Optional arguments.
* `max_cycles`: (int) Default `None`. Max cycles count
* `max_time`: (int) Default `None`. Max time to train
* `autostop`: (bool) Default `True`. If no `autostop` is `True`, trains the network till the maximum number of cycles or milliseconds are reached. If no maximum number of cycles is specified there are no cycles limits. If no milliseconds are specified, the limit is set to 10 seconds.
* `backtrack`: (bool) Default `True`. If `backtrack` is `True`, and `autostop` is also `True`, while the network is trained, the trainer thread saves a copy of the neural network every time it has a better score compared to the previously saved one and there are hints suggesting that overfitting may happen soon. This network is used later if it is found to have a smaller error.


## NeuralNetwork.is_created()
Returns `True` if the neural network is created.

## NeuralNetwork.create()
Create the neural network.

## NeuralNetwork.recreate()
Recreate the neural network.

## NeuralNetwork.delete()
Delete the neural network.

## NeuralNetwork.info()
Returns a `dict` with info about the neural network. The keys are the same that are found on `nr.info` command.


# More examples

To see how to use this library please see the [tests](https://github.com/amix/neuralist/tree/master/tests) directory -- there's an example of a neural network that can do additions and one that can answer if a Titanic passenger will survive or not.
