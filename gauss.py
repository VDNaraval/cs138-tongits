import numpy as np

# Gaussian Seidel Method Function taken from Probset 1
def gauss_seidel(M, b, n, epsilon):
    # x_i^{(k+1)}= \frac1{a_{ii}}(b_i-\sum_{j=1}^{i-1}a_{ij}x_j^{(k+1)}-\sum_{j=i+1}^na_{ij}x_j^{(k)})
    x = [0] * n # Solution Vector

    # Residual
    r = [5] * n
    oldr = [1] * n

    iterations = 1

    while np.linalg.norm(np.subtract(r, oldr)) >= epsilon:
        oldr = r.copy()
        for i in range(n):
            sum = 0
            mx = 0
            for j in range(n):
                if j == i:
                    continue
                sum = sum + M[i][j]*x[j]
                mx = mx + M[i][j]*x[i]
      
            #   if M[i][i] != 0:
            x[i] = (b[i] - sum)/M[i][i]
            #   else:
            #     x[i] = 0

            # residual = b - Mx
            r[i] = b[i] - mx - M[i][i]*x[i]
        iterations = iterations + 1

        # Fail safe in case code takes too long
        if iterations > 5000:
            break
    return x