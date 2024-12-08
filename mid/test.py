import numpy as np
from scipy.optimize import minimize

data = np.genfromtxt('circle.csv', delimiter=',', skip_header=1)

def sum_of_squared_distances(params):
    a, b, r = params
    total_distance = 0
    for x, y in data:
        distance_to_center = np.sqrt((x - a) ** 2 + (y - b) ** 2)
        
        if distance_to_center < r:
            d = abs(distance_to_center - r)
        elif x < a:
            d = abs(a - r - x)  # 수평 거리
        else:
            d = 100
        
        total_distance += d ** 2
    return total_distance

initial_guess = (0, 0, 1)
result = minimize(sum_of_squared_distances, initial_guess)
circle_params = result.x

print(circle_params)
# Output: [-0.0588, 0.0, 1.0587]
