# Experimentation Process
As it's my first time using a neural network, I consulted CS50's debugger Duck for starting tips. The recommendation was to start slowly and increase the number of neurons/filters until improvement stops.

## 1° Attempt - Initial Model
For the first attempt, I used the examples from CS50 AI video, focusing on convolution, pooling, and neural network layers. The configuration was as follows:

* **Convolutional Layer:** 32 filters, 3x3 kernel, activation = 'relu', input_shape =(IMG_WIDTH, IMG_HEIGHT, 3)
* **Max-pooling Layer:** 3x3 pool size
* **Convolutional Layer:** 96 filters, 3x3 kernel, activation = 'relu', strides = (2,2)
* **Max-pooling Layer:** 3x3 pool size, stride = (2,2)
* **Flatten Layer**
* **Dense Hidden Layer:** 128 neurons, activation = 'relu', dropout = 0.5
* **Output Layer:** NUM_CATEGORIES neurons, activation = 'softmax'
* **Compile:** optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy']

### Results:

* **Last epoch**: accuracy = 0.893, loss = 0.3623
* **Test**: accuracy = 0.9184, loss = 0.3052
This attempt served as a baseline for comparison.

## 2º Attempt - Additional Hidden Layers Before the Original One
I added a dense hidden layer with 64 neurons (activation = 'relu', dropout = 0.5) before the 128-neuron layer. All three attempts returned an accuracy lower than 6%, leading to the following conclusion:

### Conclusion:
Using smaller layers before larger ones leads to loss of information. It's better to start with larger layers and reduce them over time.

## 3° Attempt - Additional Hidden Layers After the Original One
I added the 64-neuron layer after the 128-neuron layer. The results showed some improvement but were still inconsistent and worse than the baseline.

### Conclusion:
Increasing the number of neurons increased accuracy but led to inconsistency. I will explore different activation functions.

## 4° Attempt - Additional Hidden Layers with Higher Amount of Neurons
I tested various configurations with higher numbers of neurons, resulting in mixed outcomes. None performed better than the baseline consistently.

### Conclusion:
128 neurons appear optimal for this model. I will focus on these numbers, spreading them through more layers.

## 5° Attempt - Spreading Neurons Through the Hidden Layers
I tested configurations with neurons spread across multiple layers. Results varied, but none surpassed the baseline.

### Conclusion:
Maintaining a single hidden layer with 128 neurons is optimal.

## 6º Attempt - Varying the Number of Neurons on the Original Hidden Layer
I tested different numbers of neurons in a single hidden layer, finding that 128 neurons yielded the best results.

### Results:

* 64 neurons: accuracy = 0.0559, loss = 3.4909 (test: accuracy = 0.0546, loss = 3.5038)
* 96 neurons: accuracy = 0.8193, loss = 0.5930 (test: accuracy = 0.9000, loss = 0.3551)
* 128 neurons: accuracy = 0.9150, loss = 0.2927 (test: accuracy = 0.9318, loss = 0.2700)
* 256 neurons: accuracy = 0.8945, loss = 0.3585 (test: accuracy = 0.9127, loss = 0.3039)
* 532 neurons: accuracy = 0.8835, loss = 0.4030 (test: accuracy = 0.8920, loss = 0.3939)

### Conclusion:
A single hidden layer with 128 neurons is optimal.

## 7º Attempt - Trying Different Activation Functions in the Hidden Layer
I experimented with various activation functions in the hidden layer. Sigmoid outperformed others.

### Results:

* **ReLU:** accuracy = 0.9150, loss = 0.2927 (test: accuracy = 0.9318, loss = 0.2700)
* **Leaky ReLU:** accuracy = 0.9219, loss = 0.3029 (test: accuracy = 0.9347, loss = 0.2522)
* **Parametric ReLU:** accuracy = 0.9083, loss = 0.3196 (test: accuracy = 0.9274, loss = 0.2918)
* **GeLU;** accuracy = 0.8961, loss = 0.3562 (test: accuracy = 0.9250, loss = 0.2763)
* **Sigmoid:** accuracy = 0.9581, loss = 0.1685 (test: accuracy = 0.9599, loss = 0.1481)
* **Tanh:** accuracy = 0.0572, loss = 3.5566 (test: accuracy = 0.0535, loss = 3.5239)
* **Softmax:** accuracy = 0.0547, loss = 3.4970 (test: accuracy = 0.0549, loss = 3.5071)
* **Linear:** accuracy = 0.8037, loss = 0.6489 (test: accuracy = 0.8537, loss = 0.5135)

### Conclusion:
Sigmoid is the new standard, though ReLU is used for comparison. Despite near 96% accuracy with Sigmoid, further improvements are necessary for higher reliability.

## 8º Attempt - Changing the First Convolutional Layer
I tested different kernel sizes in the first convolutional layer.

### Results:

* **2x2 Kernel (ReLU):**

    * Sigmoid Hidden Layer: accuracy = 0.9433, loss = 0.2030 (test: accuracy = 0.9457, loss = 0.1829)
    * ReLU Hidden Layer: accuracy = 0.8166, loss = 0.5957 (test: accuracy = 0.8826, loss = 0.3940)

* **3x3 Kernel (ReLU) - Standard:**

    * Sigmoid Hidden Layer: accuracy = 0.9607, loss = 0.1480 (test: accuracy = 0.9680, loss = 0.1207)
    * ReLU Hidden Layer: accuracy = 0.8966, loss = 0.3599 (test: accuracy = 0.9249, loss = 0.2803)

* **5x5 Kernel (ReLU):**

    * Sigmoid Hidden Layer: accuracy = 0.0525, loss = 3.5178 (test: accuracy = 0.0572, loss = 3.5163)
    * ReLU Hidden Layer: accuracy = 0.8909, loss = 0.3799 (test: accuracy = 0.9135, loss = 0.3264)

* **7x7 Kernel (ReLU):**

    * Sigmoid Hidden Layer: accuracy = 0.0505, loss = 3.5331 (test: accuracy = 0.0540, loss = 3.5149)
    * ReLU Hidden Layer: accuracy = 0.6100, loss = 1.2418 (test: accuracy = 0.6957, loss = 0.9626)

### Conclusion:
ReLU activation in the first layer yielded better results in the standard case, while Sigmoid performed better in other cases. Larger kernels did not improve accuracy, likely due to the small image size (30x30). I will continue with the standard configuration but may explore alternatives using Sigmoid.

## 9º Attempt - Changing the First Pooling Layer
I tested different pooling configurations.

### Results:

* **Max Pooling 2x2:**
    * accuracy = 0.0549, loss = 3.5379 (test: accuracy = 0.0583, loss = 3.4997)
* **Max Pooling 3x3 - Standard:**
    * accuracy = 0.9635, loss = 0.1318 (test: accuracy = 0.9660, loss = 0.1273)
* **Max Pooling 4x4:**
    * accuracy = 0.0558, loss = 3.5153 (test: accuracy = 0.0563, loss = 3.5071)
* **Average Pooling 2x2:**
    * accuracy = 0.0507, loss = 3.5351 (test: accuracy = 0.0522, loss = 3.5077)
* **Average Pooling 3x3:**
    * accuracy = 0.9622, loss = 0.1507 (test: accuracy = 0.9680, loss = 0.1131)
* **Average Pooling 4x4:**
    * accuracy = 0.9577, loss = 0.1641 (test: accuracy = 0.9644, loss = 0.1240)

### Conclusion:
Standard pooling configurations yielded the best results. I will focus on fine-tuning other layers while keeping the pooling layers standard.

## 10º Attempt - Changing the second convolutional layer - 3º layer:
Using the standard case as a base, I will try changing the size of the kernel, number of filters, and activation functions for the second convolutional layer to see how that affects the accuracy.

* Test with modification - Convolutional layer with 64 filters, 3x3 kernel, activation ReLU:

    * Last Epoch: accuracy: 0.9350 - loss: 0.2332
    * Test: accuracy: 0.9421 - loss: 0.1985

* Test with standard case - Convolutional layer with 96 filters, 3x3 kernel, activation ReLU:

    * Last Epoch: accuracy: 0.9607 - loss: 0.1480
    * Test: accuracy: 0.9680 - loss: 0.1207

* Test with modification - Convolutional layer with 128 filters, 3x3 kernel, activation ReLU:

    * Last Epoch: accuracy: 0.9570 - loss: 0.1562
    * Test: accuracy: 0.9645 - loss: 0.1323

* Test with modification - Convolutional layer with 96 filters, 3x3 kernel, activation Sigmoid:

    * Last Epoch: accuracy: 0.9408 - loss: 0.2120
    * Test: accuracy: 0.9505 - loss: 0.1920

* Test with modification - Convolutional layer with 96 filters, 5x5 kernel, activation ReLU:

    * Last Epoch: accuracy: 0.9430 - loss: 0.2215
    * Test: accuracy: 0.9470 - loss: 0.2015

* Test with modification - Convolutional layer with 96 filters, 7x7 kernel, activation ReLU:

    * Last Epoch: accuracy: 0.9205 - loss: 0.3085
    * Test: accuracy: 0.9260 - loss: 0.2763

* Test with modification - Convolutional layer with 258 filters, 3x3 kernel, activation Sigmoid:

    * Last Epoch: accuracy: 0.9900 - loss: 0.0500
    * Test: accuracy: 0.9900 - loss: 0.0400

### Conclusion:
The test with 258 filters, 3x3 kernel, and sigmoid activation showed exceptional results, reaching an accuracy of 0.99 on both the last epoch and the test. This configuration, despite having a high number of filters, significantly improved the model's performance, with some tests reaching an accuracy of 0.997 and a runtime of 57ms per image. Therefore, this became the new standard configuration.

## 11º Attempt - Automating Training to Stop Upon Reaching High Accuracy:
In this attempt, I automated the original file's training to stop once it reached a high accuracy, improving efficiency and saving time.

* Implementation:
    * Early stopping criteria were introduced, monitoring the accuracy during training and stopping once a predefined threshold was reached.
    * This helped in preventing overfitting and reducing unnecessary computations.

### Conclusion:
The automation allowed the model to stop training upon reaching a high accuracy, optimizing the training process and ensuring the model did not overfit.

## 12º Attempt - Creating a Fully Automated Training Script:
Building on the automation from the 11º attempt, a fully automated training script was created on a separate file. This script included data preprocessing, model training, evaluation, and saving the trained model.

* Implementation:
    * The script was designed to handle the entire training pipeline, from data loading and preprocessing to model training, evaluation, and saving.
    * It included options for hyperparameter tuning and early stopping based on validation accuracy.

## Conclusion:
The fully automated training script streamlined the entire process, making it easy to train the model with different configurations and ensuring optimal performance without manual intervention.