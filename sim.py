import tongits
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

sims_per_testcase = 1000 # Each Testcase will run this number * 3
random_seed = 8092001

# Returns a dictionary with the number of wins player1 had at each level
def run_testcase_sims(p2risk, p3risk):
    wins_per_level = {0: 0, 0.5: 0, 1: 0}  # Dictionary to count wins per risk level
    
    for p1risk in [0, 0.5, 1]:
        for i in range(sims_per_testcase):
            winner = tongits.RunTongitsSim(p1risk, p2risk, p3risk, random_seed)
            if winner == 1:
                wins_per_level[p1risk] += 1
    
    return wins_per_level

def spline_interpolation(risk_levels, win_probs):
    # Perform spline interpolation
    cs = CubicSpline(risk_levels, win_probs, bc_type='natural')
    return cs

# Plot the spline curve
def plot_spline_curve(p2risk, p3risk, x_axis, y_axis, risk_levels):
    plt.plot(x_axis, y_axis, label='Spline Interpolation', color='red')
    plt.xlabel(f'Player 1 Risk Level')
    plt.ylabel(f'Frequency of Player 1 Wins')
    plt.title(f'Wins vs Risk when P2={p2risk} and P3={p3risk}')
    plt.xticks(risk_levels, ['0', '0.5', '1'])  # Set custom x-axis tick labels
    plt.legend()

    plt.show()

def do_testcase(p2risk, p3risk):
    wins_per_level = run_testcase_sims(p2risk, p3risk);

    risk_levels = np.array(list(wins_per_level.keys()))
    win_counts = np.array(list(wins_per_level.values()))

    plt.figure(figsize=(8, 6))
    plt.bar(risk_levels, win_counts, align='center', alpha=0.8, width=0.3, label='Actual Wins')

    # Perform spline interpolation
    cs = spline_interpolation(risk_levels, win_counts)

    # Evaluate the spline on a finer grid
    x_axis = np.linspace(min(risk_levels), max(risk_levels), 300)
    y_axis = cs(x_axis)
    
    # Plot the spline curve
    # plot_spline_curve(p2risk, p3risk, x_axis, y_axis, risk_levels)
    return (x_axis.tolist(), y_axis.tolist())
                
def main():
    # p1riskLevel = 0 with 9 testcases (1000 simulations each testcase)
    # p2riskLevel = 0.5 with 9 testcases (1000 simulations each testcase)
    # p3riskLevel = 1 with 9 testcases (1000 simulations each testcase)
    risk_values = [0, 0.5, 1]

    # 2D array full of the optimum values from each testcase
    # for optima[i][j] where i=p2risk and j=p3risk
    optima = [[0 for _ in range(3)] for _ in range(3)]
    
    for p2risk in risk_values:
        for p3risk in risk_values:
            (x_axis, y_axis) = do_testcase(p2risk, p3risk)
            optimum = x_axis[y_axis.index(max(y_axis))]
            print("For p2risk =", p2risk, "p3risk =", p3risk, ", optimal p1risk =", optimum)
            optima[risk_values.index(p2risk)][risk_values.index(p3risk)] = optimum

    print(optima)

if __name__ == "__main__":
    main()
