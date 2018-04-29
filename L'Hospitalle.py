import math

def schedule(ttot, m):
    # m number of patients waiting at home at start of day
    # ttot total number of time intervals

    # we use a dictionary for our results since we want results for tuples
    state_dict = {}
    decision_dict = {}

    total_states = m+ttot
    # calculating values for each element of the matrix
    # j current time
    for j in range(ttot, -1, -1):
        # m current patients at home
        for w in range(0, m):
            # n current patients in clinic
            for n in range(0, total_states):
                state_dict[(j, w, n)] = optvalfun(j, w, n, state_dict, total_states)

    # return the maximum profit given that at time slot 0 some patient has been called and is being treated
    return state_dict[(0, m-1, 0)]


def optvalfun(j, m, n, state_dict, total_states):
    # fun is the function value of the optimal value function
    # this method can be changed for the optimal value function we choose in the end

    # defining constants

    # EDIT CONSTANTS HERE
    R = 1000
    S = 2000
    WC = 100
    WH = 10
    p = 0.3
    # EDIT CONSTANTS HERE

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
            if m+n < total_states:
                fun = R - (n-1)*WC + p*state_dict[(j+1, 0, m+n)] + (1-p)*state_dict[(j+1, 0, m+n-1)]
            else:
                fun = -math.inf
        else:
            fun = p*state_dict[(j+1, 0, m+1)] + (1-p)*state_dict[(j+1, 0, m)]

    # function value for j below 32 (any time between 8:30 and 4:00 including 4:00)
    elif 0 <= j < 31:

        total_funvals = []

        # since there are multiple possibilities, a maximum is calculated
        if m >= 1 and n >= 1:  # calling
            if n+1 < total_states:
                fun1 = R - (n-1)*WC - (m-1)*WH + p*state_dict[(j+1, m-1, n+1)] + (1-p)*state_dict[(j+1, m-1, n)]
            else:
                fun1 = -math.inf
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

    # if none of these options apply, we are somehow in an "illegal" time interval and make the function value
    # -infinity. This else statement is not used during regular calculations (with 35 time intervals)
    else:
        fun = -math.inf

    return fun


# finding the best number of patients ahead of time
def findbestschedule(time_intervals):

    # initializing best profit and best number of patients corresponding to this profit
    bestprofit = -math.inf
    best_number_of_patients = -math.inf

    # we choose any number of patients between 1 and the number of time intervals we have
    for i in range(1, time_intervals):

        # we calculate the max. expected profit with this number of patients...
        new_value = schedule(time_intervals, i)

        # ...and check if it's the best overall profit
        if new_value > bestprofit:
            bestprofit = new_value
            best_number_of_patients = i

    # return tuple: profit and number of patients corresponding to this profit
    return bestprofit, best_number_of_patients


print(findbestschedule(35))
