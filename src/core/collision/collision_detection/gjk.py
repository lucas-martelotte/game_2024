import numpy as np


def gjk_algorithm_2d(poly1: np.ndarray, poly2: np.ndarray) -> bool:
    """Assumes poly1 and poly2 are N x 2 arrays of points"""
    initial_point = poly1[0] - poly2[0]
    simplex = [initial_point]
    direction = -initial_point
    while True:
        new_point = full_support(direction, poly1, poly2)
        if list(new_point) == [0, 0]:
            return True
        if np.dot(new_point, direction) < 0:
            return False
        simplex, direction, collided = do_simplex(simplex, new_point)
        if collided:
            return True


def do_simplex(
    simplex: list[np.ndarray], a: np.ndarray
) -> tuple[list[np.ndarray], np.ndarray, bool]:
    if len(simplex) == 1:
        b, ab, d = simplex[0], simplex[0] - a, -a
        if np.dot(ab, d) > 0:
            new_direction = np.array([-ab[1], ab[0]])
            if np.dot(new_direction, d) < 0:
                new_direction = -new_direction
            return [a, b], new_direction, False
        return [a], d, False
    elif len(simplex) == 2:
        b, c, d = simplex[0], simplex[1], -a
        ab, ac = b - a, c - a
        alpha = np.array([-ac[1], ac[0]])
        if np.dot(alpha, ab) > 0:
            alpha = -alpha
        beta = np.array([ab[1], -ab[0]])
        if np.dot(beta, ac) > 0:
            beta = -beta
        if np.dot(alpha, d) > 0:
            if np.dot(ac, d) > 0:
                return [a, c], alpha, False
            else:
                return [a], d, False
        if np.dot(beta, d) > 0:
            if np.dot(ab, d) > 0:
                return [a, b], beta, False
            else:
                return [a], d, False
        return [], np.zeros(2), True
    else:
        raise Exception("Unexpected error!")


def full_support(
    direction: np.ndarray, poly1: np.ndarray, poly2: np.ndarray
) -> np.ndarray:
    return support(direction, poly1) - support(-direction, poly2)


def support(direction: np.ndarray, poly: np.ndarray) -> np.ndarray:
    max_index = np.argmax(poly @ direction)
    return poly[max_index]
