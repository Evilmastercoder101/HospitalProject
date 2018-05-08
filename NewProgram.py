import math
import copy
import pickle

# EDIT CONSTANTS AND FUNCTION CALLS ON LAST LINES OF THE CODE (FROM 523 ONWARDS)


# method for making a (locally) optimal schedule
def makeschedule(n, x, r, s, wC, wH, p):

    """
    :return: tuple (a,b)
    """

    # making the initial schedule
    schedulemade = [0]*n

    # we initiate the schedule with the first time slot being 1
    schedulemade[0] = 1
    opt_schedule_current = []

    # we first add a 1 x-1 number of times, where x is the amount of 1's
    # that we want to obtain
    for k in range(1, x):

        # we initialize the profit to be equal to minus infinity
        bestprofit = -math.inf

        # we now check which 0 would be most profitable to change to a 1
        # ie. we check in which time slot we would like to schedule a patient
        # the most
        for i in range(1, len(schedulemade)):

            # we change a 0 to a 1, if this is not possible we simply continue
            if schedulemade[i] == 0:

                schedulemade[i] = 1

            else:

                continue

            # we find the profit corresponding to this change
            newprofit = find_no_patients(35, False, r, s, wC, wH, p, True, schedulemade)

            # if the obtained profit is higher than the highest profit we have seen before
            if newprofit[1] > bestprofit:

                # this is now the highest profit we have seen before
                bestprofit = newprofit[1]
                # we deepcopy the current schedule (to make sure this copy is kept intact)
                opt_schedule_current = copy.deepcopy(schedulemade)

            # we revert the original schedule to its previous state
            schedulemade[i] = 0

        # we now make the new schedule with which we continue the schedule with which we
        schedulemade = opt_schedule_current

    # iterating over found optimum to found best policy
    continuing = True

    # as long as our result does not change we iterate
    while continuing:

        # we create a deepcopy to avoid issues with changing the schedule
        current = copy.deepcopy(schedulemade)

        # for every element of the schedule we check whether it's a 1
        for i in range(1, len(schedulemade)):

            if schedulemade[i] == 1:

                # then for all other elements we check whether it's a 0
                for j in range(0, len(schedulemade)):

                    # we interchange the found 0 and 1
                    if schedulemade[j] == 0:

                        schedulemade[i] = 0
                        schedulemade[j] = 1

                        # we find the profit for the obtained new schedule
                        newprofit = find_no_patients(35, False, r, s, wC, wH, p, True, schedulemade)

                        # we check whether the new schedule is the best we have found so far
                        if newprofit[1] > bestprofit:

                            bestprofit = newprofit[1]
                            opt_schedule_current = copy.deepcopy(schedulemade)

                        # we revert the schedule to how it was originally
                        schedulemade[i] = 1
                        schedulemade[j] = 0

                # we make the schedule the optimal found schedule from this iteration
                schedulemade = opt_schedule_current

        # if in a whole iteration (checking every combination) we have not found a single
        # change that improves our profits, we stop the calculations
        if current == schedulemade:

            continuing = False

    # we return the found schedule and profit
    return schedulemade, find_no_patients(35, False, r, s, wC, wH, p, True, schedulemade)[1]


# calculates the best number of patients to schedule for a given day
def find_no_patients(ttot, scheduling, r, s, wC, wH, p, offline, calllist):

    """
    :return: tuple (a,b)
    """

    # initialize the variables
    best_profit = -math.inf
    best_no_patients = 0

    # if we have an offline scheduling we count the number of patients we have and return the exact profit
    if offline:

        totalpatients = 0

        # summing amount of patients in schedule
        for i in calllist:
            if i == 1:
                totalpatients += 1

        # we only return the result for this specific schedule, as checking for multiple number of patients doesn't
        # make sense logically (the number of patients in the schedule we have as input is fixed)
        return totalpatients, schedule(ttot, totalpatients, scheduling, r, s, wC, wH, p, offline, calllist)

    # if we have either online scheduling or a walk-in clinic, we find the optimal number of patients to schedule and
    # the corresponding profit
    for i in range(1, ttot):

        # calculate optimal profit with i patients
        new_profit = schedule(ttot, i, scheduling, r, s, wC, wH, p, offline, calllist)

        # check whether new profit is the best and change
        # variables accordingly
        if new_profit > best_profit:
            best_profit = new_profit
            best_no_patients = i

    return best_profit, best_no_patients


# calculates the optimal scheduling for a certain number of patients
def schedule(ttot, m_init, scheduling, r, s, wC, wH, p, offline, calllist):

    """
    :return: float (or int)
    (because Python...)
    """

    # initiate dictionary of optimal expected values
    fun_dict = {}

    # the total number of patients in the clinic will not exceed this number,
    # as only 1 emergency patient can arrive in every time slot

    total_states = m_init+ttot
    if offline:
        neededm = 0

    # we loop over all time slots backwards (from 35 to 1)
    for i in range(ttot, 0, -1):

        # if we calculate for offline scheduling, we need a certain number of people waiting at home
        # at any given time. For example, if we want to have one patient in the clinic in some time slot,
        # we want at least 1 patient at home in the previous time interval. We can calculate backwards to find the
        # needed amount of patients at home for any time slot

        if offline and i <= 31 and calllist[i] == 1:

            # if call_list[t+1]
            neededm += 1

        # we loop over all possible values for the amount of patients sitting at home
        for j in range(0, m_init+1):

            # we loop over all possible values for the amount of patients waiting at the clinic4
            for k in range(0, total_states):

                # according to whether we can schedule patients,
                # we call the appropriate optimal value function
                if scheduling:
                    fun_dict[(i, j, k)] = opt_val_fun_scheduling(i, j, k, fun_dict, r, s, wC, wH, p, total_states)
                elif offline:
                    fun_dict[(i, j, k)] = opt_val_fun_offline(i, j, k, fun_dict, r, s, wC, wH, p, total_states, calllist, neededm)
                else:
                    fun_dict[(i, j, k)] = opt_val_fun_walk_in(i, j, k, fun_dict, r, s, wC, wH, p, total_states)

    # return the optimal expected revenue for the given amount of patients
    return fun_dict[1, m_init-1, 1]


# returns the value of the optimal value function
# for the problem where we can schedule patients (online)
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
                if n > 0:
                    sum_emergency += p_k_arrivals * dicti[(t+1, m-k, n+k)]
                else:
                    sum_emergency += p_k_arrivals * dicti[(t+1, m-k, k+1)]

                # several clauses to make sure we do not call for a negative number of
                # people in our clinic when asking for the expected value in this scenario
                if n > 0:

                    # adding the weighted profit to our total expected profit
                    sum_no_emergency += p_k_arrivals * dicti[(t+1, m-k, n+k-1)]

                else:
                    if k > 0:

                        # adding the weighted profit to our total expected profit
                        sum_no_emergency += p_k_arrivals * dicti[(t+1, m-k, k)]

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


# returns the value of the optimal value function
# for the problem where we have a clinic that uses offline scheduling
def opt_val_fun_offline(t, m, n, dicti, r, s, wC, wH, p, total_states, calllist, neededm):

    """
    :return: float (or int)
    (Because Python)
    """

    # time slots for calculations are mentioned above the corresponding if-statement
    # for that calculation. Values are only calculated for m = 0 when t >= 31 since
    # that is the only possible value for m in this scenario

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

        if m == 0:

            # if n > 0 we return the expected profit in any following
            # time interval plus the profit in this time interval. If n = 0
            # we return 0 as no patients are present
            if n > 0:
                return r - (n-1)*wC + dicti[(t+1, 0, n-1)]
            else:
                return 0

    if t == 33:

        if m == 0:

            # if n > 0 we return the expected profit in any following
            # time interval plus the profit in this time interval. If n = 0
            # we return 0 as no patients are present
            if n > 0:

                return r - (n-1)*wC + dicti[(t+1, 0, n-1)]

            else:

                return 0

    if t == 32:

        if m == 0:

            # if n > 0 we return the expected profit in any following
            # time interval plus the profit in this time interval. If n = 0 we
            # only consider the possibility of a last emergency patient arriving.

            if n > 0:

                return r - (n-1)*wC + p*(dicti[(t+1, 0, n)]) + (1-p)*(dicti[(t+1, 0, n-1)])

            else:

                return p*(dicti[(t+1, 0, 1)]) + (1-p)*(dicti[(t+1, 0, 0)])

    if t <= 31:

        # we only do calculations if the state is reachable. That is, if m+n > total_states, we cannot ever go to this
        # state. Moreover, m needs to be equal to neededm since we have a predetermined schedule, and m != neededm would
        # mean we are not keeping to this schedule.
        if m == neededm and m+n < total_states:

            if n > 0:

                # return expected profit for next time interval plus current profit
                return r - (n-1)*wC + p*(dicti[(t+1, m - calllist[t], n + calllist[t])]) + (1-p)*(dicti[t+1, m - calllist[t], n -1 + calllist[t]])

            else:

                # return expected profit for next time interval
                return p*(dicti[(t+1, m - calllist[t], 1 + calllist[t])]) + (1-p)*(dicti[t+1, m - calllist[t], calllist[t]])


# constants and function calls are here

# EDIT CONSTANTS HERE
r = 10
s = 12
wC = 0
wH = 0
p = 0.3
# EDIT CONSTANTS HERE

# BELOW, ONE CAN UNCOMMENT A FUNCTION CALL TO OBTAIN A CERTAIN RESULT


# # UNCOMMENT THESE LINES (536-545): A vector is created which calculates schedules
# # which are correspond to a locally optimal profit. They are then added to a vector and returned
# # in the form of an .obj file, which can again be read in Python
# tempresult = []
# for i in range(1, 33):
#     tempresult.append((i, makeschedule(32, i, r, s, wC, wH, p)))
#
# open('resultsbonus.obj', 'w+').close()
# filehand = open('resultsbonus.obj', 'wb')
# pickle.dump(tempresult, filehand)


# # UNCOMMENT THESE LINES (548 - 550): A clinic with online scheduling is simulated. The output
# # is a tuple with the optimal number of patients and the expected proceeds
# print(find_no_patients(35, True, r, s, wC, wH, p, False, []))


# # UNCOMMENT THESE LINES (553 - 555): A walk-in clinic is simulated. The output is a tuple with the
# # optimal number of patients and the expected proceeds
# print(find_no_patients(35, False, r, s, wC, wH, p, False, []))

# # UNCOMMENT THESE LINES (557 - 562): A locally optimal schedule is created for the situation where
# # 20 patients need to be treated. We first generate the schedule and then compute the proceeds. The
# # output is a tuple with the first element being the number of patients and the second being the
# # expected proceeds
# newschedule = makeschedule(32, 20, r, s, wC, wH, p)[0]
# print(find_no_patients(35, False, r, s, wC, wH, p, True, newschedule))

