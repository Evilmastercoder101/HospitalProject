import math

def schedule(ttot, m):
    # m number of patients waiting at home at start of day
    # ttot total number of time intervals

    # we use a dictionary for our results since we want results for tuples
    state_dict = {}

    # calculating values for each element of the matrix
    # j current time
    for j in range(ttot, -1, -1):
        print(j)
        # m current patients at home
        for w in range(0, m):
            print(j, w)
            # n current patients in clinic
            for n in range(0, m+ttot):
                print(j, w, n)
                state_dict[(j, w, n)] = optvalfun(j, w, n, state_dict)
    return state_dict


def optvalfun(j, m, n, state_dict):
    # fun is the function value of the optimal value function
    # this method can be changed for the optimal value function we choose in the end

    # defining constants
    R = 3
    S = 4
    WC = 10
    WH = 5
    p = 0.3

    # function value for j = 35 (time at 5:00)
    if j == 34:
        if m > 0:
            fun = -math.inf
        elif n >= 0:
            sums = 0
            for i in range(1, n):
                sums = sums + i*WC
            fun = (R-S)*n - sums
        else:
            fun = 0

    # function value for j = 34 (time at 4:45)
    elif j == 33:
        if n != 0:
            fun = R - (n-1)*WC + state_dict[(j+1, 0, n-1)]
        else:
            fun = 0

    # function value for j = 33 (time at 4:30)
    elif j == 32:
        if n != 0:
            fun = R - (n-1)*WC + state_dict[(j+1, 0, n-1)]
        else:
            fun = 0

    # function value for j = 32 (time at 4:15)
    elif j == 31:
        if n != 0:
            fun = R - (n-1)*WC + p*state_dict[(j+1, 0, m+n)] + (1-p)*state_dict[(j+1, 0, m+n-1)]
        else:
            fun = p*state_dict[(j+1, 0, m+1)] + (1-p)*state_dict[(j+1, 0, m)]

    elif 0 <= j < 31:

        total_funvals = []

        # since there are multiple possibilities, a maximum is calculated
        if m >= 1 and n >= 1:  # calling
            fun1 = R - (n-1)*WC - (m-1)*WH + p*state_dict[(j+1, m-1, n+1)] + (1-p)*state_dict[(j+1, m-1, n)]
            total_funvals.append(fun1)
        if m >= 0 and n >= 1:  # not calling
            fun2 = R - (n-1)*WC - m*WH + p*state_dict[(j+1, m, n)] + (1-p)*state_dict[(j+1, m, n-1)]
            total_funvals.append(fun2)
        if m >= 1 and n == 0:  # calling
            fun3 = -(m-1)*WH + p*state_dict[(j+1, m-1, 2)] + (1-p)*state_dict[(j+1, m-1, 1)]
            total_funvals.append(fun3)
        if m >= 0 and n == 0:  # not calling
            fun4 = -m*WH + p*state_dict[(j+1, m, 1)] + (1-p)*state_dict[(j+1, m, 0)]
            total_funvals.append(fun4)

        fun = max(total_funvals)
    else:
        fun = -math.inf

    return fun

print(schedule(35,3)[(0,1,1)])