import redis


class NeuralNetwork:

    def __init__(self, name, type,
                       inputs, outputs,
                       hidden_layers,
                       dataset_size, testset_size,
                       normalize=True, redis_client=None,
                       prefix='nn:',
                       auto_create=True):
        self.name = '%s%s' % (prefix, name)
        self.type = type
        self.inputs = inputs
        self.outputs = outputs
        self.hidden_layers = hidden_layers
        self.normalize = normalize
        self.dataset_size = dataset_size
        self.testset_size = testset_size

        if redis_client:
            self.client = redis_client
        else:
            self.client = default_redis_cli()

        if not self.is_created():
            self.create()


    def info(self):
        """
        Returns Redis internal info about the neural network
        """
        result = self.client.execute_command('nr.info', self.name)
        return dict(zip(result[0::2], result[1::2]))

    #--- Run and classify
    def run(self, input):
        """
        Run the network returning a dict result
        """
        self._validate_input(input)
        args = [self.name]
        args.extend( input[i] for i in self.inputs )
        result = self.client.execute_command('nr.run', *args)
        return dict(zip(self.outputs, result))

    def classify(self, input):
        """
        Run the network returning the classified class
        """
        self._validate_input(input)
        args = [self.name]
        args.extend( input[i] for i in self.inputs )
        result = self.client.execute_command('nr.class', *args)
        return self.outputs[int(result)]


    #--- Observe
    def observe_train(self, input, output):
        """
        Add a data sample into the training dataset
        """
        return self._observe(input, output, 'train')

    def observe_test(self, input, output):
        """
        Add a data sample into the testing dataset
        """
        return self._observe(input, output, 'test')

    def _observe(self, input, output, mode):
        """
        Add a data sample into the training or testing dataset

        Mode can be `train` or `test`
        """
        self._validate_input(input)
        self._validate_output(output)

        args = [self.name]
        args.extend( input[i] for i in self.inputs )
        args.append('->')
        if self.type == 'regressor':
            args.extend( output[o] for o in self.outputs )
        else:
            cls_type = 0
            for (i, name) in enumerate(self.outputs):
                if output[name]:
                    cls_type = i
                    break
            args.append( cls_type )
        args.append(mode)

        return self.client.execute_command('nr.observe', *args)


    # --- Creation and deletion
    def is_created(self):
        """
        Returns true if the neural network is created
        """
        return self.client.exists(self.name)

    def create(self):
        """
        Create the neural network
        """
        args = [
            self.name, self.type,
            len(self.inputs)
        ]
        args.extend(self.hidden_layers)
        args.append('->')

        args.append(len(self.outputs))
        if self.normalize:
            args.append('NORMALIZE')
        args.append('DATASET')
        args.append(self.dataset_size)
        args.append('TEST')
        args.append(self.testset_size)

        return self.client.execute_command('nr.create', *args)

    def recreate(self):
        """
        Recreate the neural network
        """
        self.delete()
        self.create()

    def delete(self):
        """
        Delete the neural network
        """
        self.client.delete(self.name)


    # --- Training
    def is_training(self):
        return self.info().get('training', 1) == 1

    def train(self, max_cycles=None, max_time=None,
              autostop=True, backtrack=True):
        args = [ self.name ]

        if max_cycles:
            args.append('MAXCYCLES')
            args.append(max_cycles)

        if max_time:
            args.append('MAXTIME')
            args.append(max_time)

        if autostop:
            args.append('AUTOSTOP')

        if backtrack:
            args.append('BACKTRACK')

        return self.client.execute_command('nr.train', *args)


    #--- Validators
    def _validate_input(self, input):
        if set(input.keys()) != set(self.inputs):
            raise TypeError('Input does not have the required keys')

    def _validate_output(self, output):
        if set(output.keys()) != set(self.outputs):
            raise TypeError('Output does not have the required keys')

#--- Helpers
def default_redis_cli():
    return redis.StrictRedis(host='localhost')
