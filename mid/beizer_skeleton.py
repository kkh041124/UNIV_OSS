import numpy as np
import matplotlib.pyplot as plt

def select_ctrl_pts(x, y, theta, x_goal, y_goal, theta_goal, s1=3, s2=3):
    P0 = np.array([x, y])
    P1 = np.array([x + s1 * np.cos(theta), y + s1 * np.sin(theta)])
    P2 = np.array([x_goal - s2 * np.cos(theta_goal), y_goal - s2 * np.sin(theta_goal)])
    P3 = np.array([x_goal, y_goal])
    
    return P0, P1, P2, P3

def generate_cubic_bezier_curve(P0, P1, P2, P3, steps=100):
    t = np.linspace(0, 1, steps).reshape(-1, 1)
    return (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

def visualize_cubic_bezier_curve(P0, P1, P2, P3, steps=100):
    curve = generate_cubic_bezier_curve(P0, P1, P2, P3, steps)
    
    # Plot the Bezier curve
    plt.plot(curve[:, 0], curve[:, 1], 'b-', label='Cubic Bezier Curve')
    
    # Plot control points and lines
    plt.plot([P0[0], P1[0]], [P0[1], P1[1]], 'g--o', label='P0-P1', linewidth=2, markersize=8)
    plt.plot([P2[0], P3[0]], [P2[1], P3[1]], 'r--o', label='P2-P3', linewidth=2, markersize=8)
    
    # Set labels, legend, and grid
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(['Cubic Bezier Curve', 'P0-P1', 'P2-P3'])
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Parameters to create a longer, smoother curve
x, y, theta = 1, 2, np.pi / 4                 # Start position and angle
x_goal, y_goal, theta_goal = 8, 6, -np.pi / 6  # Goal position and angle
s1, s2 = 3,3                                # Control point distances

# Generate control points and visualize
P0, P1, P2, P3 = select_ctrl_pts(x, y, theta, x_goal, y_goal, theta_goal, s1, s2)
visualize_cubic_bezier_curve(P0, P1, P2, P3)
