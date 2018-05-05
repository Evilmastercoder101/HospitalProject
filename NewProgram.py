import math

# EDIT CONSTANTS ON LAST LINES OF THE CODE (313 lines in code :D)


# calculates the best number of patients to schedule for a given day
def find_no_patients(ttot, scheduling, r, s, wC, wH, p):

    """
    :return: tuple (a,b)
    """

    # initialize the variables
    best_profit = -math.inf
    best_no_patients = 0

    for i in range(1, ttot):

        # calculate optimal profit with i patients
        new_profit = schedule(ttot, i, scheduling, r, s, wC, wH, p)

        # check whether new profit is the best and change
        # variables accordingly
        if new_profit > best_profit:
            best_profit = new_profit
            best_no_patients = i

    return best_profit, best_no_patients


# calculates the optimal scheduling for a certain number of patients
def schedule(ttot, m_init, scheduling, r, s, wC, wH, p):

    """
    :return: float (or int)
    (because Python...)
    """

    # initiate dictionary of optimal expected values
    fun_dict = {}

    # the total number of patients in the clinic will not exceed this number,
    # as only 1 emergency patient can arrive in every time slot
    total_states = m_init+ttot

    # we loop over all time slots backwards (from 35 to 1)
    for i in range(ttot, 0, -1):

        # we loop over all possible values for the amount of patients sitting at home
        for j in range(0, m_init+1):

            # we loop over all possible values for the amount of patients waiting at the clinic4
            for k in range(0, total_states):

                # according to whether we can schedule patients,
                # we call the appropriate optimal value function
                if scheduling:
                    fun_dict[(i, j, k)] = opt_val_fun_scheduling(i, j, k, fun_dict, r, s, wC, wH, p, total_states)
                else:
                    fun_dict[(i, j, k)] = opt_val_fun_walk_in(i, j, k, fun_dict, r, s, wC, wH, p, total_states)

    # return the optimal expected revenue for the given amount of patients
    return fun_dict[1, m_init-1, 1]


# returns the value of the optimal value function
# for the problem where we can schedule patients
def opt_val_fun_scheduling(t, m, n, dicti, r, s, wC, wH, p, total_states):

    """
    :return: float (or int)
    (because Python...)
    """

    # time slots for certain parts of the function are indicated above the if-statement
    # corresponding to the calculation for that time slot. Values are only calculated for
    # m = 0 if t > 31 since that is the only possible value for m in these time slots

    # 17:00
    if t == 35:

        if m == 0:

            # we sum the amount of waiting costs after 17:00
            total_cost_overtime = 0

            for i in range(0, n):
                total_cost_overtime += i*wC

            # we return the profit when there are n patients left at 17:00
            return (r-s)*n - total_cost_overtime

    # 16:45
    if t == 34:

        # whenever n > 0 we calculate the profit made in this time slot and
        # add it to the profit made in the 17:00 time slot
        if n > 0 and m == 0:

            return r - (n-1)*wC + dicti[(t+1, 0, n-1)]

        # if n = 0, we return 0 since there are no patients in our clinic
        if n == 0:

            return 0

    # 16:30
    if t == 33:

        # whenever n > 0 we calculate the profit made in this time slot and
        # add it to the profit made in the 16:45 time slot
        if n > 0 and m == 0:

            return r - (n-1)*wC + dicti[t+1, 0, n-1]

        # if n = 0, we return 0 since there are no patients in our clinic
        if n == 0:

            return 0

    # 16:15
    if t == 32:

        # whenever n > 0 we calculate the profit made in this   and add to it
        # the expected profit made in the 16:30 time slot (depending on whether an
        # emergency patient arrives)
        if n > 0 and m+n < total_states:

            return r - (n-1)*wC + p*dicti[t+1, 0, m+n] + (1-p)*dicti[t+1, 0, m+n-1]

        # if n = 0 we return the expected profit in the 16:30 time slot depending on whether
        # an emergency patient arrives
        if n == 0:

            return p*dicti[t+1, 0, n+1] + (1-p)*dicti[t+1, 0, n]

    #8:30 - 16:00
    if 0 <= t <= 31:

        # we initiate a non-empty (!) vector with all possible expected profits based on
        # whether we call a patient or not
        possible_values = [-math.inf]

        # calculate expected profit if there is at least 1 patient in the clinic and
        # we call a patient who is currently sitting at home
        if m >= 1 and n >= 1 and n+1 < total_states and m+n < total_states:

            fun1 = r - (n - 1)*wC - (m-1)*wH + p*dicti[(t+1, m - 1, n + 1)] + (1 - p)*dicti[(t + 1, m - 1, n)]
            possible_values.append(fun1)

        # calculate expected profit if there is at least 1 patient in the clinic
        # and we do not call a patient who is currently sitting at home
        if m >= 0 and n >= 1 and m+n < total_states:

            fun2 = r - (n - 1)*wC - m*wH + p*dicti[(t+1, m, n)] + (1 - p)*dicti[(t+1, m, n-1)]
            possible_values.append(fun2)

        # calculate expected profit if there are no patients in the clinic and we
        # call a patient who is currently sitting at home
        if m >= 1 and n == 0:

            fun3 = -(m-1)*wH + p*dicti[(t+1, m-1, 2)] + (1-p)*dicti[(t+1, m-1, 1)]
            possible_values.append(fun3)

        # calculate expected profit if there are not patients in the clinic and we
        # do not call a patient who is currently sitting at home
        if m >= 0 and n == 0:

            fun4 = -m*wH + p*dicti[(t+1, m, 1)] + (1-p)*dicti[(t+1, m, 0)]
            possible_values.append(fun4)

        return max(possible_values)


# returns the value of the optimal value function
# for the problem where we cannot schedule patients (walk-in clinic)
def opt_val_fun_walk_in(t, m, n, dicti, r, s, wC, wH, p, total_states):

    """
    :return: float (or int)
    (because Python)
    """

    # time slots for certain parts of the function are indicated above the if-statement
    # corresponding to the calculation for that time slot. Values are only calculated for
    # m = 0 if t > 31 since that is the only possible value for m in these time slots

    # 17:00
    if t == 35:

        if m == 0:

            # we sum the amount of waiting costs after 17:00
            total_cost_overtime = 0

            for i in range(0, n):
                total_cost_overtime += i * wC

            # we return the profit when there are n patients left at 17:00
            return (r - s) * n - total_cost_overtime

    # 16:45
    if t == 34:

        # whenever n > 0 we calculate the profit made in this time slot and
        # add it to the profit made in the 17:00 time slot
        if n > 0 and m == 0:
            return r - (n - 1) * wC + dicti[(t + 1, 0, n - 1)]

        # if n = 0, we return 0 since there are no patients in our clinic
        if n == 0:
            return 0

    # 16:30
    if t == 33:

        # whenever n > 0 we calculate the profit made in this time slot and
        # add it to the profit made in the 16:45 time slot
        if n > 0 and m == 0:
            return r - (n - 1) * wC + dicti[t + 1, 0, n - 1]

        # if n = 0, we return 0 since there are no patients in our clinic
        if n == 0:
            return 0

    # 16:15
    if t == 32:

        # whenever n > 0 we calculate the profit made in this time slot and add to it
        # the expected profit made in the 16:30 time slot (depending on whether an
        # emergency patient arrives)
        if n > 0 and m + n < total_states:
            return r - (n - 1) * wC + p * dicti[t + 1, 0, m + n] + (1 - p) * dicti[t + 1, 0, m + n - 1]

        # if n = 0 we return the expected profit in the 16:30 time slot depending on whether
        # an emergency patient arrives
        if n == 0:
            return p * dicti[t + 1, 0, n + 1] + (1 - p) * dicti[t + 1, 0, n]

    # 8:30 - 16:00
    if 0 <= t <= 31:

        # the probability of a patient choosing to arrive in the current time slot
        p_arrival = 1/(33-t)

        # initiating sums to 0
        sum_no_emergency = 0
        sum_emergency = 0

        # this clause ensures we do not go out of the state space we defined (when calling
        # for entries in are dictionary and thus we don't encounter any errors
        if m+n < total_states:

            # calculate the expected profits for any number of scheduled patients and
            # emergency patients that can arrive in this time slot
            for k in range(0, m+1):

                # probability calculated by means of a Binomial distribution
                m_choose_k = math.factorial(m) / (math.factorial(k) * math.factorial(m - k))
                p_k_arrivals = m_choose_k * (p_arrival ** k) * ((1 - p_arrival) ** (m - k))

                # adding the weighted profit to our total expected profit
                sum_emergency += p_k_arrivals * dicti[(t+1, m-k, n+k)]

                # several clauses to make sure we do not call for a negative number of
                # people in our clinic when asking for the expected value in this scenario
                if n > 0:

                    # adding the weighted profit to our total expected profit
                    sum_no_emergency += p_k_arrivals * dicti[(t+1, m-k, n+k-1)]

                else:
                    if k > 0:

                        # adding the weighted profit to our total expected profit
                        sum_no_emergency += p_k_arrivals * dicti[(t+1, m-k, k-1)]

                    else:

                        # adding the weighted profit to our total expected profit
                        sum_no_emergency += p_k_arrivals * dicti[(t + 1, m, 0)]

            # when n = 0, we do not have any waiting costs but we also do not get any profit
            # since we don't treat a patient. We treat this case separately. In all cases,
            # the expected profit for the following time slot (given the values in this time
            # slot is added to the returned value
            if n == 0:

                return p * sum_emergency + (1 - p) * sum_no_emergency

            # when n >  0 we might have waiting costs and we do treat a patient
            else:

                return r - (n - 1) * wC + p * sum_emergency + (1 - p) * sum_no_emergency

# constants and function calls are here

# edit constants here
r = 1000
s = 1200
wC = 500
wH = 10
p = 0.3
# edit constants here

# structure of input: (no. time slots, scheduling(True/False), constants)
# we now call the function twice, once to find the optimal profit when we schedule our
# patients by time slot, and once to find the optimal profit for a walk-in clinic.
# We print the results and the optimal number of patients we should have that day (i.e. how
# many patients we tell beforehand that they can come on that particular day)
print(find_no_patients(35, True, r, s, wC, wH, p))
print(find_no_patients(35, False, r, s, wC, wH, p))
