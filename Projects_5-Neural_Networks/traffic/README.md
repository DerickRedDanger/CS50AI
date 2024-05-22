As it's my first time using a neural network, I asked Cs50's debugger Duck for some starting tips and how it's usually done. The recommended was to start slowly and increase the number of neurons/filters from there until it stops improving.

### 1° attempt:
For my first attempt, I used as base the examples given in Cs50Ai video and its ideas, while going a bit heavy-handed on the number of filters and layers. That is a convolution, pooling to get the basic idea of the image while reducing it' dimensions,  followed by another convolution/pooling with more filters and fewer reductions to get a better grasp of its details, then flattening and passed to the neural network. 

    Convolutional layer of 32 filters using a 3x3 Kernel with activation = 'relu' and input_shape =(IMG_WIDTH, IMG_HEIGHT, 3)

    Max-pooling layer, using 3x3 pool size

    Convolutional layer of 96 filters using a 3x3 Kernel with activation = 'relu' and strides = (2,2)

    max pooling layers, using a pool of 3x3 and a stride of 2x2 (so it's a overlapping pooling)

    Flatten

    a dense hidden layer with 128 neurons with activation = 'relu' and a dropout of 0.5

    with an output layer with a number of neurons = NUM_CATEGORIES and activations ="softmax"

    a Compile with optimizer="adam", loss="categorical_crossentropy" and metrics=["accuracy"]

    This model's last epoch returned an accuracy of 0.893, loss of 0.3623. While its test returned an accuracy of 0.9184 and a loss of 0.3052

    Given this attempt's high score, it was used as base for comparision.

### 2º attempt:
    Decided to try adding more hidden layers to see how this would affect the model. Added  a dense hidden layer with 64 neurons with activation = 'relu' and a dropout of 0.5 before the layer with 128 neurons. Did 3 attempts, and they all returned with an accuracy lower than 6%. 
    
    2° attempt discarded and returned to 1° attempt's model.

    Conclusion: Using smaller layers before large ones seem to lead to a loss of information. Will attempt more configurations, but apparently it's better to start with larger layers and then reduce them over time, instead of starting with smaller and increasing.

### 3° attempt:
    Followed the idea of the 2° attempt, but added the layer with 64 neurons after the one with 128. Last epoch returned with an accuracy of 0.5295 and a loss of 1.3401. Test returned accuracy: 0.6165 - loss: 1.0679

    Better than the 2° attempt, but still worse than the original. Another attempt using 96 instead of 64, ambiguous results. Reaching accuracy of 0.5592 on last epoch and accuracy of 0.6793 on test, meaning it could be a good idea to increase the number of Neurons. But at times reached accuracy of 0,1, This inconsistency wasn't present in the initial attempt. Perhaps this is due to both layers using the same activation.

    Conclusion: increase the number of layers and check results. Look for other options for activation.

### 4° attempt:
    Continuing with the idea of increasing the number of neurons in the layers following the one with 128. Using another layer with 128 neurons led to last epoch returning accuracy: 0.7241 - loss: 0.8767, while test returned accuracy: 0.8367 - loss: 0.5366, but there were times it returned accuracy of 0.15. 
    Increasing the number of neurons to 258 led to the last epoch returning accuracy: 0.7484 - loss: 0.8208 while test returns accuracy: 0.8405 - loss: 0.5471. But as before, there were a case where it returned an accuracy of 0.05. 
    Considering how increasing the number of Neurons isn't improving the accuracy, perhaps it's time to change tactics.

    Moved the layer with 256 Neurons to before the one with 128. This configuration got a result that came close to 1º attempt, but were still worse than it, with its last epoch returning accuracy: 0.8409 - loss: 0.5303 while its test returned accuracy: 0.8850 - loss: 0.3974

    Made another attempt where both layers had 256 neurons, where the last epoch returned accuracy: 0.8724 - loss: 0.4578 and test returned accuracy: 0.9181 - loss: 0.2973

    and a last one where both layers had 256, last epoch - accuracy: 0.8513 - loss: 0.5085 and test - accuracy: 0.8808 - loss: 0.4362

    Conclusion: Given how increasing the number of neurons didn't improve the accuracy, I believe 128 is the best amount for this model. So I will focus on working with these numbers and trying to spread it through more layers.

### 4° attempt:

    Given how increasing the number of neurons didn't improve the accuracy, I am going to try to spread them through more layers to see how the model would react to that. Initially splitting it into two layers of 64 each.

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

    Conclusion: Since adding more layers and changing the number of neurons didn't improve the accuracy, I decided to remain with just 1 hidden layer with 128 neurons.

### 5º attempt:

    Decided to stick to 1 hidden layer and to try different amounts of Neurons:
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

    Given these result, a single hidden layer with 128 neurons appear to be the optimal configuration.

### 6º attempt:

    Given how the results didn't improve when adding more layers or changing the number of neurons, I decided to try different activation functions. This is the same model as attempt one, only difference being that the Layer with 128 neuron are using different activation functions.

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

    Given how well Sigmoid performed, I've decided to make it the standard from here on, while still using ReLU for comparison during the experiments with different configuration.

    Also tried to use sigmoid with multiple hidden layers raging from 128/96 to 128/96/64/32, but all of them resulted on accuracy below 0.06.

    Considering Sigmoid accuracy of near 96%, I believe this Project already reached a good result. But considering how this is meant to simulate the creation of an Ai for a self-driving car, it also means that lives could be at stake. As such, I will try to raise this value as high as I can before considering this project finished.

#### Conclusion:
    Sigmoid showed the best accuracy compared to others activation functions, thus becoming my standard for tests from here on. ReLU is still going to be used in experiments for comparision. Despite Sigmoid reaching an accuracy of nearly 0.96, given how this project is supposed to simulate an Ai for a self-driving car, I will aim to get the highest accuracy possible instead of stopping here.

### 7º attempt - changing the first convolutional layer - 1º layer:

    From here on, will attempt testing different configurations for convolutional and pooling layers. For this testing, will use a single deep hidden layer of 128 neurons and while varying the activation functions between ReLU and Sigmoid. The standard configuration of the convolutional and pooling layers are:

    1º layer - Convolutional layer with 32 filters, 3x3 kernel, activation Relu
    2º layer - Max-pooling layer with a 3x3 pool size
    3º layer - convolutional layer with 96 filters, 3x3 kernel, strides of 2x2, activation Relu
    4º layer - Max-overlapping-pooling layer, 3x3 kernel and strides of 2x2 

* Test with modification to the 1º layer. 2x2 Kernel - ReLU:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.9433 - loss: 0.2030
            Test: accuracy: 0.9457 - loss: 0.1829

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8166 - loss: 0.5957
            Test: accuracy: 0.8826 - loss: 0.3940

* Test with standard values to the 1º layer. 3x3 Kernel - ReLU:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.9607 - loss: 0.1480
            Test: accuracy: 0.9680 - loss: 0.1207

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8966 - loss: 0.3599
            Test: accuracy: 0.9249 - loss: 0.2803

* Test with modification to the 1º layer. 5x5 Kernel - ReLU:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.0525 - loss: 3.5178
            Test: accuracy: 0.0572 - loss: 3.5163

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8909 - loss: 0.3799
            Test: accuracy: 0.9135 - loss: 0.3264

* Test with modification to the 1º layer. 7x7 Kernel - ReLU:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.0505 - loss: 3.5331
            Test: accuracy: 0.0540 - loss: 3.5149

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.6100 - loss: 1.2418
            Test: accuracy: 0.6957 - loss: 0.9626

#### Tests changing the 1º layer from ReLU to Sigmoid:

* Test with modification to the 1º layer. 2x2 Kernel - Sigmoid:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.8790 - loss: 0.3970
            Test: accuracy: 0.8995 - loss: 0.3292

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8848 - loss: 0.3660
            Test: accuracy: 0.9017 - loss: 0.3121

* Test with standard values to the 1º layer. 3x3 Kernel - Sigmoid:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.9057 - loss: 0.3205
            Test: accuracy: 0.9417 - loss: 0.2108

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8712 - loss: 0.4158
            Test: accuracy: 0.9004 - loss: 0.3099

* Test with modification to the 1º layer. 5x5 Kernel - Sigmoid:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.7838 - loss: 0.6965
            Test: accuracy: 0.7994 - loss: 0.6118

        Using ReLU on Hidden lyaer:
            Last Epoch: accuracy: 0.8909 - loss: 0.3799
            Test: accuracy: 0.9135 - loss: 0.3264

* Test with modification to the 1º layer. 7x7 Kernel - Sigmoid:

        Using Sigmoid on Hidden lyaer:
            Last Epoch: accuracy: 0.5740 - loss: 1.30431
            Test: accuracy: 0.6712 - loss: 1.0556

        Using ReLU on Hidden lyaer:
            Last Epoch: 0.2984 - loss: 2.1921 
            Test: accuracy: 0.3558 - loss: 1.9896

#### Conclusion:

    Using the ReLU activation on the first layer yielded better results than Sigmoid on the standard case, meanwhile sigmoid yielded better results on all the other cases. This might be because ReLU have the dying neuron problem, where a neuron outputs 0 during training, thus being unable to be updated and effectively 'dying' during training.

    On the other hand, despite the initial expectations that using a filter with a larger kernel on the 1º layer would yield better results (since it would allow the program to capture larger or more complex patterns in the input image), it ended up reducing my program's accuracy. I believe this is happening because the images used are only 30x30, so using a larger Kernel might be capturing too much, losing important details. 

    Despite sigmoid yielding better results in general, none of them came close to the result ReLU yielded with the standard values, so I will continue to focus on the standard case, but may switch to Sigmoid to try alternatives sometimes.

### 8º attempt - changing the first pooling - 2º layer:

    Using the standard case as base, I will try changing the dize of the pooling and it's kind to check how that will affect the accuracy.

* Test with modification - Max pooling using 2x2
        Last Epoch: accuracy: 0.0549 - loss: 3.5379
        Test: accuracy: 0.0583 - loss: 3.4997

* Test with standard case - Max pooling using 3x3
        Last Epoch: accuracy: 0.9635 - loss: 0.1318
        Test: accuracy: 0.9660 - loss: 0.1273

* Test with modification - Max pooling using 4x4
        Last Epoch: accuracy: 0.0558 - loss: 3.5153
        Test: accuracy: 0.0563 - loss: 3.5071

* Test with modification - averange pooling using 2x2
        Last Epoch: accuracy: 0.0507 - loss: 3.5351
        Test: accuracy: 0.0522 - loss: 3.5077

* Test with modification - averange pooling using 3x3
        Last Epoch: accuracy: 0.9622 - loss: 0.1507
        Test: accuracy: 0.9680 - loss: 0.1131

* Test with modification - averange pooling using 4x4
        Last Epoch: accuracy: 0.9577 - loss: 0.1641
        Test: accuracy: 0.9644 - loss: 0.1279

    There were also the option of using Global max/average Pooling, but as these reduce the feature of the whole map to a single value, it would lead to a too much loss of spatial information as the first pooling layers. So I will only test it on the second layer.

#### Conclusion:

    Average pooling gave a similar result for using a kernel with 3x3, but still allowed good values in 4x4, So I will use it instead of maxpooling for the following tests.

### 9º attempt - Changing the second convolution - 3° layer

    In order to be able to make the most from the information gathered from the first convolution, I decided to use 128 filters to gather as much information as possible, while using strides (reducing the steps from the pool size to the size of the stride) to ensure my Ai isn't missing any information.

    Here I will try to change the number of filters, the activation function and whether I should keep or remove the strides.

* Test with standard case - 128 filters, 3x3 Kernel, 2x2 strides, activation ReLU:
    Last Epoch: accuracy: 0.9537 - loss: 0.1682
    Test: accuracy: 0.9608 - loss: 0.1386

* Test with modified case - 128 filters, 3x3 Kernel, 2x2 strides, activation Sigmoid:
    Last Epoch: accuracy: 0.8925 - loss: 0.3892
    Test: accuracy: 0.9293 - loss: 0.2828

* Test with modified case - 128 filters, 3x3 Kernel, No stride, activation ReLU:
    Last Epoch: accuracy: 0.0542 - loss: 3.5247
    Test: accuracy: 0.0512 - loss: 3.5121

* Test with modified case - 128 filters, 3x3 Kernel, No stride, activation Sigmoid:
    Last Epoch: accuracy: 0.9821 - loss: 0.0852
    Test: accuracy: 0.9831 - loss: 0.0637

    After this result, I looked up and realized that convolutional layers actually work with a stride of 1x1, and not a stride equal to its kernel (like the pooling). So by using a stride, I was actually losing information instead of preserving it. So from this point on I stopped using strides in my convolution.

    On the same note, all my tries with no stride using ReLu led to accuracy lower than 0.06, So I stopped using ReLU and focused on Sigmoid.

* Test with modified case - 258 filters, 3x3 Kernel, No stride, activation Sigmoid:
    Last Epoch: accuracy: 0.9906 - loss: 0.0479
    Test: accuracy: 0.9920 - loss: 0.0277

    Upon reaching an accuracy of 0.99 on both test and last epoch, I decided to do more tests on this configuration. Checking other metrics and the time it takes to run a prediction. To achieve this I've made the following changes to my Model.compile:

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )

    While I did the following to get a random x_test and make its prediction to check how long it takes for my program to run a single prediction, since for a self-driving car, I believe the program need to have the highest accuracy possible while still being relatively quick.

    test = random.choice(x_test)
    test = np.expand_dims(test, axis=0)
    predictions = model.predict(test)

    Below are the result, as is, from the terminal (the words 'Test' and 'Prediction' were added for clarification):

    Epoch 10/10:
    500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - accuracy: 0.9877 - loss: 0.0575 - precision: 0.9911 - recall: 0.9831  

    Test:
    333/333 - 1s - 4ms/step - accuracy: 0.9916 - loss: 0.0334 - precision: 0.9929 - recall: 0.9899

    Prediction:
    1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 57ms/step

#### Conclusion:
    Meanwhile, 258 filters might indeed be excessive, that number allowed the Ai to increase the accuracy from 0.98 to 0.99, with some tests reaching accuracy of 0.997. Given the importance of accuracy to an Ai that is guiding a car (and consequently may have lives at stakes) I believe that his is a worth trade-off. And while initially worried about how computationally costly or slow this prediction would and up running, I believe that utilizing 0.057 seconds to run a prediction is fast enough. As such, meanwhile I will run additional tests for learning's sake, This is going to be the configuration I am going to commit.

### 10º attempt - automate training:

    After some discussions with Cs50 Duck debugger Ai, I got the idea to change my fit function to stop when a epoch's accuracy reaches 0.995. In order to do that i did the following modifications:

    created a new class:

    class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch=EPOCHS, logs=None):
        if logs.get('accuracy') > 0.995:
            self.model.stop_training = True

    and modified the fit function to :
    model.fit(x_train, y_train, epochs=EPOCHS,callbacks=[MyCallback()])

    Changing my Epochs from 10 to 100 let me to the following result:
    Epoch 29/100:
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.9968 - loss: 0.0131 - precision: 0.9971 - recall: 0.9963 

    Test:
    333/333 - 1s - 3ms/step - accuracy: 0.9951 - loss: 0.0165 - precision: 0.9970 - recall: 0.9946

    Prediction:
    1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 57ms/step

    Wanting to go one step further, I decided to use a loop to automatize my training, in such that it would train an Ai multiple times, immediately dropping and reset when it gets stuck in an accuracy below 0.06, or reset after reaching the last epoch but not reaching an accuracy of 0.995. But stopping and saving that Ai upon reaching said accuracy.

    Since these modifications go against Cs50 guidance of not changing anything in the code beside the functions I am supposed to implement, additional functions I could create to assist me or the initial variables (EPOCHS,IMG_WIDTH,IMG_HEIGHT, NUM_CATEGORIES, TEST_SIZE). I will, instead, creating this program in another file.

### 11º attempt - Automation completed:

    As said in attempt 10º, I create a new file, on which I copied traffic to and modified. A short explanation of the code I made is the following:
    The model is the exact same I used on the original traffic, the differences are the loop made to automate the training and the callback function.:

#### Training loop:

    My training uses two whiles up, each using a variable that is either true or false. These variables are meant to keep my code running till an exit condition appears: The Ai reached the desired accuracy on both last Epoch and test this breaking out of both loops. It got stuck at low accuracy and needs to be reset. If trained for too long and should be reset. Or if it was reset the set maximum amount of times, thus breaking out of the loop.

    As for how the loop works:

    It defines my Model's, then trains it. When it finishes training (reached the max number of epochs or the callback function ended it), its last epoch's accuracy is tested, if it's the same or higher as the value required, it will be evaluated. If the test's accuracy is the same or higher than the accuracy required, the model is saved.

    If after the training, the model didn't reach the required accuracy, it's breaks out of the training loop and is reset. If it passes the training's accuracy but not the test's, it will be trained again, then tested. This will repeat until it passes the test's accuracy or either reaches the max amount of training epochs in a row or maximal number of training, at which point it will break out of the training loop and is reset.

#### Callback Function:

    This is the function I added to the fit function to add conditions on which my model stops training.

    There are three conditions on which my model should stop training:
    
* When it reaches a low accuracy (set to 0.07 in this case) 6 times, it means my model is stuck, so it will stop training and be reset back in the loop.

* When My model trained for a total number of MAX_EPOCHES(int) of epochs set by the user. This was made to give the user more control on how many times a model should be allowed to train before resetting (together with variable MAX_TRAINING_ROW, which control how many times a model can be trained before resetting).

* When my model's latest epoch reach an accuracy equal or higher than TEST_ACCURACY. Note, however, that the last epoch accuracy is different from the one presented in the terminal by the Keras. 
    
    When Keras reports the accuracy during training, it's giving this running average at the current point in the epoch. This means that early batches have a larger influence on this reported accuracy than later batches.

    On the other hand, the print made in the terminal gives you the final accuracy for the latest epoch, calculated after all batches have been processed, meaning that their values might be slightly different from the one given by the Keras, often different enough to get opposite results when compared to the training accuracy if.