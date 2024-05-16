As it's my first time using a neural network, I asked Cs50's debugger Duck for some starting tips and how it's usually done. The recommended was to start slowly and increase the number of neurons/filters from there until it stops improving.

### 1° attempt:
For my first attempt I used as base the examples given in Cs50Ai video and it's ideas, while going a bit heavy handed on the number of filters and layers. That is a convolution, pooling to get the basic idea of the image while reducing it's dimmensions,  followed by another convolution/pooling with more filters and less reductions to get a better grasp of it's details, then flattening and inside the neural network. 

    Convolutional lyaer of 32 filters using a 3x3 Kernel with activation = 'relu' and input_shape =(IMG_WIDTH, IMG_HEIGHT, 3)

    Max-pooling layer, using 3x3 pool size

    Convolutional lyaer of 96 filters using a 3x3 Kernel with activation = 'relu' and strides = (2,2)

    max pooling layers, using a pool of 3x3 and a stride of 2x2 (so it's a overlaping pooling)

    Flatten

    a dense hidden layer with 128 neurons with activation = 'relu' and a dropout of 0.5

    with a output layer with a number of neurons = NUM_CATEGORIES and activations ="softmax"

    a Compilie with optimizer="adam", loss="categorical_crossentropy" and metrics=["accuracy"]

    This model's last epoch returned a accuracy of 0.893, loss of 0.3623. while it's test returned a accuracy of 0.9184 and a loss of 0.3052

    Given this attempt's high score, it was used as base for comparission.

### 2º attempt:
    Decided to try adding more hidden layers to see how this would affect the model. added a a dense hidden layer with 64 neurons with activation = 'relu' and a dropout of 0.5 before the layer with 128 neurons. did 3 attempts and they all returned with a accuracy lower then 6%. 
    
    2° attempt discarderd and returned to 1° attempt's model.

    Conclusion: Using smaller layers before large ones seem to lead to a loss of information. Will attempt more configurations, but apparently it's better to start with larger layers and then reduce them over time, instead of starting with smaller and increasing.

### 3° attempt:
    Followed the idea of the 2° attempt, but added the layer with 64 neurons after the one with 128. last epoch returned with a accuracy of 0.5295 and a loss of 1.3401. Test returned accuracy: 0.6165 - loss: 1.0679

    Better then the 2° attempt, but still worse then the original. Should i try to recude the number of neurons per layer more slowly? another attempt using 96 instead of 64, ambiguous results. reaching accuracy of 0.5592 on last epoch and accuracy of 0.6793 on test, meaning it could be a good idea to increase the number of Neurons. But at times reached accuracy of 0,1, This inconsistency wasn't present in the initial attempt. Perhaps this is due to both layers using the same activation.

    Conclusion: increase the number of layers and check results. look for other options for activation.

### 4° attempt:
    Continuing with the idea of increasing the number of neurons in the layers following the one with 128. Using another layer with 128 neurons led to last epoch returning accuracy: 0.7241 - loss: 0.8767, while test returned accuracy: 0.8367 - loss: 0.5366, but there were times it returned accuracy of 0.15. 
    increasing the number of neurons to 258 led to the last epoch returning accuracy: 0.7484 - loss: 0.8208 while test returns accuracy: 0.8405 - loss: 0.5471. But as before, there were a case where it returned a accuracy of 0.05. 
    Considering how increasing the number of Neurons isn't improving the accuracy, perhaps it's time to a change of tatics.

    Moved the layer with 256 Neurons to before the one with 128. This configuration got result that came close 1º attempt, but were still worse then it, with it's last epoch returning accuracy: 0.8409 - loss: 0.5303 while it's test returned accuracy: 0.8850 - loss: 0.3974

    Made another attempt where both layers had 256 neurons, where the last epoch returned accuracy: 0.8724 - loss: 0.4578 and test returned accuracy: 0.9181 - loss: 0.2973

    and a last one where both layers had 256, last epoch - accuracy: 0.8513 - loss: 0.5085 and test - accuracy: 0.8808 - loss: 0.4362

    Conclusion: Given how increasing the number of neurons didn't improve the accuracy, I believe 128 is the best amount for this model. So I will focus on working with this numbers and trying to spread it through more layers.

### 4° attempt:

    Given how increasing the number of neurons didn't improve the accuracy, I am going to try to spread them through more layers to see how the Model would react to that. initially splitting it into two layers of 64 each.

    results 64/64:
     last epoch - accuracy: 0.0566 - loss: 3.5018
     Test - accuracy: 0.0540 - loss: 3.4985

    result 64/32/32:
     last epoch - accuracy: 0.0554 - loss: 3.5072
     Test - accuracy: 0.0539 - loss: 3.5014

    result 32/32/32/32:
     last epoch - accuracy: 0.0554 - loss: 3.4973
     Test - accuracy: 0.0532 - loss: 3.5061

    result 32/32/32/16/16:
     last epoch - accuracy: 0.0582 - loss: 3.5052
     Test - accuracy: 0.0557 - loss: 3.4922

     Since the results from using few Neurons were nearly the same, I once again tried to increase that number and check how that affects multiple layers:

    result 128/32/32/16/16:
     last epoch - accuracy: 0.1148 - loss: 3.1432
     Test - accuracy: 0.1336 - loss: 3.0495

    result 128/128/64/64/32:
     last epoch - accuracy: 0.0600 - loss: 3.5036
     Test - accuracy: 0.0556 - loss: 3.5039

    result 128/128/128/64/64:
     last epoch - accuracy: 0.1225 - loss: 2.9018
     Test - accuracy: 0.0914 - loss: 3.0953

    Conclusion: Since adding more layers and changing the number of neurons didn't improve the accuracy, I dediced to remain with just 1 hidden layer with 128 neurons.

### 5º attempt:

    decided to stick to 1 hidden layer and to try different amounts of Neurons:
    result of 64:
        last epoch - accuracy: 0.0559 - loss: 3.4909
        Test - accuracy: 0.0546 - loss: 3.5038

    result of 96:
        last epoch - accuracy: 0.8193 - loss: 0.5930
        Test - accuracy: 0.9000 - loss: 0.3551
    
    result of 128:
        last epoch - accuracy: 0.9150 - loss: 0.2927
        Test - accuracy: 0.9318 - loss: 0.2700

    result of 256:
        last epoch - accuracy: 0.8945 - loss: 0.3585
        Test - accuracy: 0.9127 - loss: 0.3039

    result of 532:
        last epoch - accuracy: 0.8835 - loss: 0.4030
        Test - accuracy: 0.8920 - loss: 0.3939

    Given these reseult, a single hidden layer with 128 neurons appear to be the optimal configuration.

### 6º attempt:

    Given how the results didn't improve whem adding more Layers or changing the number of neurons, I decided to try different activation functions. This is the same model as attempt one, only difference being that the Layer with 128 neuron are using different activation functions.

    result of 128 neurons and activation function ReLU:
        last epoch - accuracy: 0.9150 - loss: 0.2927
        Test - accuracy: 0.9318 - loss: 0.2700

    result of 128 neurons and activation function leaky ReLU:
        last epoch - accuracy: 0.9219 - loss: 0.3029
        Test - accuracy: 0.9347 - loss: 0.2522

    result of 128 neurons and activation function parametric ReLU:
        last epoch - accuracy: 0.9083 - loss: 0.3196
        Test - accuracy: 0.9274 - loss: 0.2918

    result of 128 neurons and activation function GeLU:
        last epoch - accuracy: 0.8961 - loss: 0.3562
        Test - accuracy: 0.9250 - loss: 0.2763
    
    result of 128 neurons and activation function Sigmoid:
        last epoch - accuracy: 0.9581 - loss: 0.1685
        Test - accuracy: 0.9599 - loss: 0.1481

    result of 128 neurons and activation function Tanh:
        last epoch - accuracy: 0.0572 - loss: 3.5566
        Test - accuracy: 0.0535 - loss: 3.5239

    result of 128 neurons and activation function Softmax:
        last epoch - accuracy: 0.0547 - loss: 3.4970
        Test - accuracy: 0.0549 - loss: 3.5071

    result of 128 neurons and activation function Linear:
        last epoch - accuracy: 0.8037 - loss: 0.6489
        Test - accuracy: 0.8537 - loss: 0.5135

    Given how well Sigmoid performed, I've decided to make it the standard from here on, while still using ReLU for comparission during the experiements with different configuration.

    Also tried to use sigmoid with multiple hidden layers raging from 128/96 to 128/96/64/32, but all of them resulted on accuracy below 0.06.

    Considering Sigmoid accuracy of near 96%, I believe this Project already reached a good result. But considering how this is meant to simulate the creation of an Ai for a self driving car, it also means that lives could be at stake. as Such I will try to raise this value as high as I can before considering this project finished.

    Conclusion: Sigmoid showed the best accuracy compared to others activation functions, thus becoming my standard for tests from here on. ReLU is still going to be used in experiments for comparission. Despite Sigmoid reaching a accuracy for nearly 0.96, given how this project is supposed to simulate an Ai for a self driving car, I will aim to get the highest accuracy possible instead of stopping here.

### 7º attempt:

    will attempt testing different configurations for convolutional and pooling layers. for this testing, will use a single deep hidden layer of 128 neurons and while varying the activation fuctions betweem ReLU and Sigmoid. the standard configuration of the convolutional and pooling layers are:

    1º - Convolutional layer with 32 filters, 3x3 kernel, activation Relu
    2º - Max-pooling layer with a 3x3 pool size
    3º - convolutional layer with 96 filters, 3x3 kernel, strides of 2x2, activation Relu
    4º - Max-overlapping-pooling layer, 3x3 kernel and strides of 2x2 

    Test with modification to the 1º layer. 2x2 Kernel:

        Using Sigmoit on Hidden lyaer:
            Last Epoch: accuracy: 0.9433 - loss: 0.2030
            Test: accuracy: 0.9457 - loss: 0.1829

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8166 - loss: 0.5957
            Test: accuracy: 0.8826 - loss: 0.3940

    Test with modification to the 1º layer. 5x5 Kernel:

        Using Sigmoit on Hidden lyaer:
            Last Epoch: accuracy: 0.0525 - loss: 3.5178
            Test: accuracy: 0.0572 - loss: 3.5163

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8909 - loss: 0.3799
            Test: accuracy: 0.9135 - loss: 0.3264

    Test with modification to the 1º layer. 7x7 Kernel:

        Using Sigmoit on Hidden lyaer:
            Last Epoch: accuracy: 0.0505 - loss: 3.5331
            Test: accuracy: 0.0540 - loss: 3.5149

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.6100 - loss: 1.2418
            Test: accuracy: 0.6957 - loss: 0.9626