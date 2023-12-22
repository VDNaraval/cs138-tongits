import tongits
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

def spline_interpolation(risk_levels, win_probs):
    # Perform spline interpolation
    cs = CubicSpline(risk_levels, win_probs, bc_type='natural')
    return cs

def plot_player_wins(p2risk, p3risk):
    wins_per_level = {0: 0, 0.5: 0, 1: 0}  # Dictionary to count wins per risk level
    
    for p1riskLevel in [0, 0.5, 1]:
        for p2riskLevel in [0, 0.5, 1]:
            for p3riskLevel in [0, 0.5, 1]:
                for i in range(100):
                    winner = tongits.RunTongitsSim(p1riskLevel, p2riskLevel, p3riskLevel)
                    if winner == 1 and p2riskLevel == p2risk and p3riskLevel == p3risk:
                        wins_per_level[p1riskLevel] += 1

    risk_levels = np.array(list(wins_per_level.keys()))
    win_counts = np.array(list(wins_per_level.values()))

    plt.figure(figsize=(8, 6))
    plt.bar(risk_levels, win_counts, align='center', alpha=0.8, width=0.3, label='Actual Wins')

    # Perform spline interpolation
    cs = spline_interpolation(risk_levels, win_counts)

    # Evaluate the spline on a finer grid
    x_new = np.linspace(min(risk_levels), max(risk_levels), 300)
    y_smooth = cs(x_new)

    # Plot the spline curve
    plt.plot(x_new, y_smooth, label='Spline Interpolation', color='red')
    plt.xlabel(f'Player 1 Risk Level')
    plt.ylabel(f'Frequency of Player 1 Wins')
    plt.title(f'Wins vs Risk when P2={p2risk} and P3={p3risk}')
    plt.xticks(risk_levels, ['0', '0.5', '1'])  # Set custom x-axis tick labels
    plt.legend()

    plt.show()

def main():
    # p1riskLevel = 0 with 9 testcases (100 simulations each testcase)
    # p2riskLevel = 0.5 with 9 testcases (100 simulations each testcase)
    # p3riskLevel = 1 with 9 testcases (100 simulations each testcase)
    
    for p2risk in [0, 0.5, 1]:
        for p3risk in [0, 0.5, 1]:
            plot_player_wins(p2risk, p3risk)

if __name__ == "__main__":
    main()
