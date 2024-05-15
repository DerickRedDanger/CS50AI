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

    decided to stick to 1 hidden layer and to try different amounts of Neurons