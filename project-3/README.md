# Project 3 (GD, SGD, NN)

In this project we had to create a `Gradient Descent (GD) optimizer` and `Stochastic Gradient Descent (SGD)` to fit given 100 (x, y) data pairs using a curve.

And we also have to create a neural network for predicting hand written devanagarik letters.

### Pre-requisit

In order to run the task program files you need to have the following installed in your system.

- Python (v)
- numpy (v)
- matplotlib (v)

### Task 1

The first task was to build the `GD` and `SGD` optimizers for fitting given 100 data pairs with a curve having atleast 3 features.

#### To run the GD script

```bash
python gd.py
```

> [!Tip]
>
> To change the learning rate provide a `--lr` option in the script followed by the desired learning rate. _(e.g. python gd.py --lr 0.001)_.
>
> To change the number of features provide `--features` option followed by the number of features to use. _(e.g. python gd.py --features 4)_.
>
> To change the number of epochs provide `--epochs` option followed by the number of epochs to iterate. _(e.g. python gd.py --epochs 500)_.
>
> To see curve of all epochs provide `--all` option _(e.g. python gd.py --all True)_

#### To run the SGD script

```bash
python sgd.py
```

> [!TIP]
>
> Similar to `GD` script you can also provide the same options to `SGD` program too.

### Task 2

In the task we had to develop an AI model to solve any kind of problem or application.

We decided to tackle the problem of predicting handwritten devanagarik letters as our problem statement and created a Convulational Neural Network (CNN) using datasets from kaggle.

> The program file is located inside **task-2** folder named as _deva-prediction-cnn.ipynb_
