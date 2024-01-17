import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
import tongits
import gauss

sims_per_testcase = 1000 # Each Testcase will run this number * 3
random_seed = 8092001

# Returns a dictionary with the number of wins player1 had at each level
def run_testcase_sims(p2risk, p3risk):
    wins_per_level = {0: 0, 1: 0}  # Dictionary to count wins per risk level
    
    for p1risk in [0, 1]:
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
    risk_values = [0, 1]

    # 2D array full of the optimum values from each testcase
    # for optima[i][j] where i=p2risk and j=p3risk
    optima = [[0 for _ in range(2)] for _ in range(2)]
    
    #* 1. RUN SIMULATIONS
    #* 2. OBTAIN OPTIMA

    i = 0
    print("\n[Running Simulations and obtaining Maximum p1risk values]")
    for p2risk in risk_values:
        for p3risk in risk_values:
            i = i + 1
            (x_axis, y_axis) = do_testcase(p2risk, p3risk) #* <--- Simulations
            optimum = x_axis[y_axis.index(max(y_axis))] #* <--- Optima
            print("Simulation Batch " + str(i) + ") For p2risk=" + str(p2risk), "\tp3risk=" + str(p3risk), "\t| optimal p1risk=" + str(optimum))
            optima[risk_values.index(p2risk)][risk_values.index(p3risk)] = optimum

    print("\n[Performing Bilinear Interpolation in order to obtain coefficients to the following eq.]")
    print("f(x,y) = a0 + a1x + a2y + a3xy")
    print("\tNote: x=p2risk, y=p3risk, f(x,y)=optimal p1risk for a given p2risk & p3risk")
    
    #* 3. SET UP MATRICES FOR SLE
    # f(x,y) = a[0] + a[1]*x + a[2]*y + a[3]*x*y

    # p2risk: x_1 = 0, x_2 = 1
    x1 = risk_values[0]
    x2 = risk_values[1]

    # p3risk: y_1 = 0, y_2 = 1
    y1 = risk_values[0]
    y2 = risk_values[1]
    
    #! NOTE: Row 2 Swapped with Row 3 to keep the matrix Dominantly Diagonal
    M = [[1, x1, y1, x1 * y1],
         [1, x2, y1, x2 * y2], # Row 2 Swapped with Row 3 to keep the matrix Dominantly Diagonal
         [1, x1, y2, x1 * y2],
         [1, x2, y2, x2 * y2]]
    
    b = [optima[risk_values.index(x1)][risk_values.index(y1)], 
         optima[risk_values.index(x2)][risk_values.index(y1)], # Row 2 Swapped with Row 3 to keep the matrix Dominantly Diagonal
         optima[risk_values.index(x1)][risk_values.index(y2)], 
         optima[risk_values.index(x2)][risk_values.index(y2)]]
    
    print("matrix M=", M)
    print("matrix A= [a0, a2, a1, a3]")
    print("matrix b=", b)

    #* 4. PERFORM BILINEAR INTERPOLATION USING GAUSSIAN ELIMINATION METHOD
    print("\n[Performing Gaussian Elimination to solve MA = b]")
    constants = gauss.gauss_seidel(M, b, len(M[0]), 0.0001)

    print("matrix A=", constants)

    [a0, a2, a1, a3] = constants
    print("\n[Final Multilinear Equation]")
    print("f(x,y) = "+ str(a0) +" + " + str(a1) +"*x + " + str(a2) +"*y + " + str(a3) +"*x*y")
    

if __name__ == "__main__":
    main()
