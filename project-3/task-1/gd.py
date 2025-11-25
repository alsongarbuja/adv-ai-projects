import numpy as np
import matplotlib.pyplot as plt
import ast
import argparse

def load_coordinates(filepath: str):
  """
  Load the coordinates from the given file

  Args:
    filepath: (string) path to the file

  Returns:
    x: (ArrayLike) x coordinates
    y: (ArrayLike) y coordinates
  """
  x_coords = []
  y_coords = []

  with open(filepath, "r") as f:
    next(f) # Skip the first row / header

    for line in f:
      line = line.strip().rstrip(",") # Remove the comma from end
      if not line:
        continue

      x, y = ast.literal_eval(line) # Safely evaluate the tuple

      x_coords.append(float(x))
      y_coords.append(float(y))

  return np.array(x_coords), np.array(y_coords)

def normalize_features(X, Y):
    """
    Normalize features to scale data between 0 and 1

    Args:
      X: (ArrayLike) x coordinates
      Y: (ArrayLike) y coordinates

    Returns:
      X_norm: (ArrayLike) normalized x coordinates
      Y_norm: (ArrayLike) normalized y coordinates
    """
    X_norm = (X - X.min()) / (X.max() - X.min())
    Y_norm = (Y - Y.min()) / (Y.max() - Y.min())
    return X_norm, Y_norm

def plot_data(x, y, data):
  """
  plotting the data in the matplot graph

  Args:
    x: (ArrayLike) x coordinates
    y: (ArrayLike) y coordinates
    data: (object) object containing params in each epoch
  """
  plt.figure(figsize=(6, 6))
  plt.scatter(x, y, color='green', label='Data Points', alpha=0.5)
  x_line = np.linspace(min(x), max(x), 100)

  for epoch, params in sorted(data.items()):
    y_line = np.zeros_like(x_line)
    for i, coeff in enumerate(params):
      y_line += coeff * x_line** i
    plt.plot(x_line, y_line, label=f'Epoch {epoch + 1}')

  plt.xlabel('Normalized X')
  plt.ylabel('Normalized Y')
  plt.title(f'Gradient descent using {len(params)} features')
  plt.legend()
  plt.show()

def build_feature(X, n):
  """
  Return the feature of the X with n number of features

  Args:
    X: (ArrayLike) x coordinates
    n: (int) number of features to use

  Return
    F: Feature of x with n number of features
  """
  return np.column_stack([X**i for i in range(n)])

def gradient_descent(y, f, lr, epochs):
  """
  The actual gradient descent function to minimize the loss

  Args:
    y: (ArrayLike) y coordinates
    f: features
    lr: (float) the learning rate
    epochs: (int) number of epoch to run

  Returns
    params: Final parameter values
    epoch_data: object of each epoch params
  """
  m, n =  f.shape
  params = np.zeros(n) # parameters initialized to 0
  epoch_data = {}

  for epoch in range(epochs):
    prediction = f.dot(params)
    errors = prediction - y
    gradient = 2 / m * f.T.dot(errors)
    params -= lr * gradient

    # Save the epoch parameters for every fixed rounds (e.g. every 10 rounds for 100 epochs, every 50 rounds for 500 epochs)
    if epoch >= 9 and (epoch + 1) % (epochs/10) == 0:
      epoch_data[epoch] = params.copy()
      print(f"Epoch: {epoch+1}, params: {params}")

  return params, epoch_data

X, Y = load_coordinates('assets/Part1_x_y_Values.txt')
x_norm, y_norm = normalize_features(X, Y)

# Parse the arguments from terminal for custom epochs and learning rate
parser = argparse.ArgumentParser(description="Find optimized curve with gradient descent")
# add --epochs argument for custom epoch with default 100
parser.add_argument('--epochs', type=int, default=100, help="Number of epoch rounds")
# add --lr argument for custom learning rate with default 0.01
parser.add_argument('--lr', type=float, default=0.01, help="Learning rate")
# add --features argument for number of features with default 3
parser.add_argument('--features', type=int, default=3, help="Number of features")
args = parser.parse_args()

feature = build_feature(x_norm, args.features)
params, epoch_data = gradient_descent(y_norm, feature, args.lr, args.epochs)
print(f"Final Parameters: ", params)

plot_data(x_norm, y_norm, epoch_data)
