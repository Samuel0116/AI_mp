import numpy as np
from planar_arm import Arm
import math

epsilon = 1e-15
# -------------- setup linear regression --------------

# return x,y
# x is a numpy array of shape (num_samples, 1)
#   x values should be uniformly distributed between x_range[0] and x_range[1]
# y is a numpy array of shape (num_samples, 1)
# y = slope * x + intercept + uniform_noise
#   where uniform_noise is uniformly distributed between -noise and noise
def create_linear_data(num_samples, slope, intercept, x_range=[-1.0, 1.0], noise=0.1):
    x_val = np.random.uniform(x_range[0], x_range[1], (num_samples, 1))
    uniform_noise = np.random.uniform(-noise, noise, (num_samples, 1))
    y_val = slope * x_val + intercept + uniform_noise
    return [x_val, y_val]


# return the modified features for simple linear regression
# x is a numpy array of shape (num_samples, num_features)
# return a numpy array of shape (num_samples, num_features+1)
#   where the last column is all ones
def get_simple_linear_features(x):
    ones = np.ones((x.shape[0], 1))
    res = np.hstack((x, ones))
    return res


# return the prediction for linear regression given x and A
# x is a numpy array of shape (num_samples, num_features)
# A is a numpy array of shape (num_modified_features, 1)
# get_modified_features is a function that takes in x and returns the modified features
#   which have shape (num_samples, num_modified_features)
#   for example get_simple_linear_features
def linear_prediction(x, A, get_modified_features):
    m = get_modified_features(x)
    res = m @ A
    return res


# return the mean squared error loss
# y_pred is a numpy array of shape (num_samples, 1)
# y_true is a numpy array of shape (num_samples, 1)
def mse_loss(y_pred, y_true):
    tot = y_pred.shape[0]
    mse = sum((y_pred - y_true) ** 2) / tot
    return mse


# return the model error for linear regression
# NOTE: the model error here is just the loss function, 
# in logistic regression later the model error and loss will be different...
def compute_model_error(x, y, A, get_modified_features):
    return mse_loss(linear_prediction(x, A, get_modified_features), y)


# return matrix A of parameters for linear regression, A has shape (num_modified_features, 1)
#   in particular you should compute the analytical solution A for y = A * X
#   i.e., A = (X^T * X)^-1 * X^T * y
# X is a numpy array of shape (num_samples, num_modified_features)
# y is a numpy array of shape (num_samples, 1)
def analytical_linear_regression(X, y):
    A = np.linalg.inv(X.T @ X) @ X.T @ y
    return A


# -------------- gradient descent for linear regression --------------

# return the gradient of the MSE loss function for linear regression
#   MSE loss is: 1/N * ||Y - XA||_2^2, i.e., 1/N * (Y - XA)^T * (Y - XA)
#   and the gradient is: 2 * X^T * (X * A - Y) / N
#   where N is the number of samples
# A is a numpy array of shape (num_modified_features, 1)
# X is a numpy array of shape (num_samples, num_modified_features)
# y is a numpy array of shape (num_samples, 1)
def get_linear_regression_gradient(A, X, y):
    N = X.shape[0]
    pred = X @ A
    error = pred - y
    res = (2 / N) * (X.T @ error)
    return res


# return matrix A of parameters, A has shape (num_modified_features, 1)
#   in particular run gradient descent with learning rate learning_rate for num_iterations
# A_init is a numpy array of shape (num_modified_features, 1)
# get_gradient is a function that returns the gradient of the loss function with respect to A
#   i.e., get_gradient = lambda A: get_linear_regression_gradient(A, X, y) 
def gradient_descent(get_gradient, A_init, learning_rate, num_iterations):
    A = A_init.copy()

    for i in range(num_iterations):
        gradient = get_gradient(A)
        A = A - learning_rate * gradient
    return A


# -------------- stochastic gradient descent for linear regression --------------

# return matrix A of parameters, A has shape (num_modified_features, 1)
#   in particular run stochastic gradient descent with learning rate learning_rate 
#   for num_epochs epochs (one epoch is one pass through the entire dataset) with batch size batch_size
#   HINT: make sure to shuffle the indices of the dataset before EACH epoch
#       - you may find np.random.permutation useful
# A_init is a numpy array of shape (num_modified_features, 1)
# get_batch_gradient is a function that returns the gradient of the loss function with respect to A
#   for a specific batch of indices, 
#   i.e., get_batch_gradient = lambda A, indices: get_linear_regression_gradient(A, X[indices], y[indices])
# data_size is the number of samples in the dataset
# batch_size is an integer representing the number of samples to use in each iteration
#   1 <= batch_size <= data_size
def stochastic_gradient_descent(get_batch_gradient, A_init, learning_rate, num_epochs, data_size, batch_size):
    A = A_init.copy()
    for _ in range(num_epochs):
        indices = np.random.permutation(data_size)
        for i in range(0, data_size - batch_size, batch_size):
            gradient = get_batch_gradient(A, indices[i:i + batch_size])
            A = A - learning_rate * gradient
    return A


# -------------- polynomial regression for sine function --------------

# return x, y for the sine function with noise
# x is a numpy array of shape (num_samples, 1)
#   x values should be uniformly distributed between x_range[0] and x_range[1]
# y is a numpy array of shape (num_samples, 1)
# y = sin(x) + uniform_noise
# uniform_noise is uniformly distributed between -noise and noise
def create_sine_data(num_samples, x_range=[0.0, 2 * np.pi], noise=0.1):
    x_val = np.random.uniform(x_range[0], x_range[1], (num_samples, 1))
    uniform_noise = np.random.uniform(-noise, noise, (num_samples, 1))
    y_val = np.sin(x_val) + uniform_noise
    return [x_val, y_val]


# return the modified polynomial features for doing linear regression
#   i.e., polynomial regression: y = a_n * x^n + ... + a_1 * x + a_0
# x is a numpy array of shape (num_samples, num_features)
#   - NOTE: num_features is 1 for this problem but later we will use more features
# return a numpy array of shape (num_samples, num_features * (degree + 1))
#   i.e., return X = [x^n, x^(n-1), ..., x, 1]
def get_polynomial_features(x, degree):
    features = [x ** i for i in range(degree, -1, -1)]
    X = np.hstack(features)
    return X


# -------------- inverse kinematics via gradient descent --------------

# return the loss for the inverse kinematics problem, 
#   i.e., the (2 dimensional) euclidean distance between the end effector and the goal
#   you can get the end effector position by calling arm.forward_kinematics(config)[-1]
# arm is an Arm object
# config is a numpy array of shape (num_joints,)
# goal is a numpy array of shape (2,)
def ik_loss(arm: Arm, config, goal):
    arm_pos = arm.forward_kinematics(config)[-1]
    res = math.sqrt(abs(arm_pos[0] - goal[0])**2 + abs(arm_pos[1] - goal[1])**2)
    return res


# we provide a more complex loss function that includes obstacles
# this loss is high when the arm is close to an obstacle
# obstacles is a list of obstacles, each obstacle is a numpy array of shape (num_obstacles, 3) 
# where each obstacle is a circle with (x,y,radius)
def ik_loss_with_obstacles(arm: Arm, config, goal, obstacles):
    # first compute the ik loss without obstacles
    ee_loss = ik_loss(arm, config, goal)
    # now compute the obstacle loss as a sum of harmonic losses (1/distance)
    workspace_config = arm.forward_kinematics(config)
    total_obstacle_loss = 0
    for obstacle in obstacles:
        # find the closest joint to the obstacle 
        # (technically we should do line-segment to circle distance)
        obstacle_dist = np.min(np.linalg.norm(workspace_config - obstacle[:2], axis=1))
        # if the joint is inside the obstacle, return infinity
        if obstacle_dist < obstacle[2]:
            return np.inf
        # otherwise, compute the harmonic loss
        total_obstacle_loss += 1 / (obstacle_dist - obstacle[2])
        # we could instead use a quadratic penalty...
        # total_obstacle_loss += -(obstacle_dist - obstacle[2])**2
    return ee_loss + total_obstacle_loss


# given a configuration, sample nearby points and return them
#   return a numpy array of shape (num_samples, num_joints)
# num_samples is the number of samples to return
# config is a numpy array of shape (num_joints,)
# epsilon is the max distance to sample nearby points
#   points should be sampled uniformly a distance epsilon from config (in each dimension)
# HINT: array broadcasting is your friend, and if you don't know what this means look it up
def sample_near(num_samples, config, epsilon=0.1):
    x_val = np.random.uniform(0, epsilon, (num_samples, 1))
    res = config + x_val
    return res


# estimate the gradient of the loss function at config by:
#   1. sampling nearby points 
#   2. picking the direction of MAXIMUM loss
#   3. normalize this vector to return a UNIT vector of shape (num_features,)
# loss is a function that takes in a configuration and returns a scalar loss
# config is a numpy array of shape (num_features,)
# num_samples is the number of samples to use to estimate the gradient (use sample_near)
def estimate_ik_gradient(loss, config, num_samples):
    near_by = sample_near(num_samples, config)
    losses = np.array([loss(point) for point in near_by])

    max_loss_index = np.argmax(losses)
    max_loss_direction = near_by[max_loss_index] - config

    unit_gradient = max_loss_direction / np.linalg.norm(max_loss_direction)
    return unit_gradient


# -------------- logistic regression for provided data --------------

# compute the average error rate given the predictions and true labels
#   a prediction is 1 if y_pred > 0.5 and 0 otherwise
# y_pred is a numpy array of probabilities of shape (num_samples, 1)
# y_true is a numpy array of 0's and 1's of shape (num_samples, 1)
def logistic_error(y_pred, y_true):
    tot = y_pred.shape[0]
    final = np.round(y_pred)
    res = sum(abs(final - y_true))
    return res/tot


# logistic regression prediction is the sigmoid of the linear prediction
#   i.e., y_pred = 1 / (1 + exp(-X * A))
#   you could (should) use linear_prediction to get the linear prediction, i.e., X * A
# x is a numpy array of shape (num_samples, num_features)
# A is a numpy array of shape (num_modified_features, 1)
# get_modified_features is a function that takes in x and returns the modified features
def logistic_prediction(x, A, get_modified_features):
    linear = linear_prediction(x, A, get_modified_features)
    linear = np.array(linear, dtype=np.float64)
    y_pred = 1/(1 + np.exp(-linear))
    return y_pred


# the logistic loss function for binary classification with y_true in {0,1}
#   loss = - sum_i (y_true[i] * log(y_pred[i]) + (1 - y_true[i]) * log(1 - y_pred[i]))
# y_pred is a numpy array of probabilities of shape (num_samples, 1)
# y_true is a numpy array of 0's and 1's of shape (num_samples, 1)
# NOTES:
#   - don't use a for loop!
#   - log(0) is undefined, so you should clip y_pred to be between epsilon and 1-epsilon for small epsilon
def logistic_loss(y_pred, y_true):
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    loss = -np.sum(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return loss


# return the gradient of the logistic loss function for logistic regression
#   the gradient is: X^T * (y_pred - y_true)
#   you should use logistic_prediction to get y_pred with modified_features as the identity, 
#   i.e., y_pred = logistic_prediction(X, A, modified_features = lambda x: x)
# A is a numpy array of shape (num_modified_features, 1)
# X is a numpy array of shape (num_samples, num_modified_features)
# y is a numpy array of 0's and 1's of shape (num_samples, 1)
def get_logistic_regression_gradient(A, X, y):
    y_pred = logistic_prediction(X, A, get_modified_features = lambda x: x)
    gradient = X.T @ (y_pred - y)
    return gradient


# return the modified features for logistic regression
# x is a numpy array of shape (num_samples, num_features)
# return a numpy array of shape (num_samples, num_modified_features)
def get_logistic_regression_features(x):
    features = get_polynomial_features(x, 4)
    ones = np.ones((x.shape[0], 4))
    res = np.hstack((features, ones))
    return res

