from dataclasses import dataclass

import jax.numpy as jnp

from mpgno.utils import Array, ScalarArray


@dataclass
class EvalMetrics:
  error_direct_ms: float = None
  error_direct_l1: float = None
  error_direct_l2: float = None
  error_rollout_ms: float = None
  error_rollout_l1: float = None
  error_rollout_l2: float = None
  error_final_ms: float = None
  error_final_l1: float = None
  error_final_l2: float = None

def mse_error(predictions: Array, labels: Array) -> Array:
    """
    Returns the mean squared error per variable.
    All input shapes are [batch_size, num_times_output,
        num_grid_points_0, num_grid_points_1, num_outputs]
    Output shape is [batch_size, num_outputs].
    """

    mean_err_per_var_squared = jnp.mean(jnp.power(predictions - labels, 2), axis=(1, 2, 3))

    return mean_err_per_var_squared

def rel_l1_error(predictions: Array, labels: Array) -> Array:
    """
    Returns the relative L1-norm of the error per variable.
    All input shapes are [batch_size, num_times_output,
        num_grid_points_0, num_grid_points_1, num_outputs]
    Output shape is [batch_size, num_outputs].
    """

    sum_err_per_var_abs = jnp.sum(jnp.abs(predictions - labels), axis=(1, 2, 3))
    sum_lab_per_var_abs = jnp.sum(jnp.abs(labels), axis=(1, 2, 3))
    rel_l2_err_per_var = (sum_err_per_var_abs / sum_lab_per_var_abs)

    return rel_l2_err_per_var

def rel_l2_error(predictions: Array, labels: Array) -> Array:
    """
    Returns the relative L2-norm of the error per variable.
    All input shapes are [batch_size, num_times_output,
        num_grid_points_0, num_grid_points_1, num_outputs]
    Output shape is [batch_size, num_outputs].
    """

    sum_err_per_var_squared = jnp.sum(jnp.power(predictions - labels, 2), axis=(1, 2, 3))
    sum_lab_per_var_squared = jnp.sum(jnp.power(labels, 2), axis=(1, 2, 3))
    rel_l2_err_per_var = jnp.sqrt(sum_err_per_var_squared / sum_lab_per_var_squared)

    return rel_l2_err_per_var

def mse_loss(predictions: Array, labels: Array) -> ScalarArray:
    """
    Returns the mean squared error.
    Input shapes are [batch_size, num_times_output, num_grid_points, num_outputs].
    Output shape is [1].
    """

    return jnp.mean(jnp.power(predictions - labels, 2))

def msre_loss(predictions: Array, labels: Array) -> ScalarArray:
    """
    Returns the mean squared relative error.
    Input shapes are [batch_size, num_times_output, num_grid_points, num_outputs].
    Output shape is [1].
    """

    eps = 1e-08
    return jnp.mean(jnp.power((predictions - labels) / (labels + eps), 2))

def rel_l1_loss(predictions: Array, labels: Array) -> ScalarArray:
    """
    Returns the mean relative L1-norm loss.
    Input shapes are [batch_size, num_times_output, num_grid_points, num_outputs].
    Output shape is [1].
    """

    rel_err_per_var = rel_l1_error(predictions, labels)
    rel_err_agg = jnp.linalg.norm(rel_err_per_var, axis=-1)

    return jnp.mean(rel_err_agg)

def rel_l2_loss(predictions: Array, labels: Array) -> ScalarArray:
    """
    Returns the mean relative L2-norm loss.
    Input shapes are [batch_size, num_times_output, num_grid_points, num_outputs].
    Output shape is [1].
    """

    rel_err_per_var = rel_l2_error(predictions, labels)
    rel_err_agg = jnp.linalg.norm(rel_err_per_var, axis=-1)

    return jnp.mean(rel_err_agg)