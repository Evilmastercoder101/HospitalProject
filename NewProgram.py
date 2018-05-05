import math


def schedule(ttot, m_init):

    # edit constants here
    r = 100
    s = 0
    wC = 100
    wH = 10
    p = 0.3

    fun_dict = {}

    total_states = m_init+ttot

    for i in range(ttot, 0, -1):

        for j in range(0, m_init+1):

            for k in range(0, total_states):
                fun_dict[(i, j, k)] = opt_val_fun_walk_in(i, j, k, fun_dict, r, s, wC, wH, p, total_states)

    return fun_dict[1, m_init-1, 1]

def opt_val_fun_walk_in(t, m, n, dict, r, s, wC, wH, p, total_states):

    # 17:00
    if t == 35:

        if m == 0:

            total_cost_overtime = 0

            for i in range(0, n):
                total_cost_overtime += i*wC

            return (r-s)*n - total_cost_overtime

    # 16:45
    if t == 34:

        if n > 0 and m == 0:

            return r - (n-1)*wC + dict[(t+1, 0, n-1)]

        if n == 0:

            return 0

    # 16:30
    if t == 33:

        if n > 0 and m == 0:

            return r - (n-1)*wC + dict[t+1, 0, n-1]

        if n == 0:

            return 0

    # 16:15
    if t == 32:

        if n > 0 and m+n < total_states:

            return r - (n-1)*wC + p*dict[t+1, 0, m+n] + (1-p)*dict[t+1, 0, m+n-1]

        if n == 0:

            return p*dict[t+1, 0, m+1] + (1-p)*dict[t+1, 0, m]

    if 1 <= t <= 31:

        p_arrival = 1/(33-t)

        sum_no_emergency = 0
        sum_emergency = 0

        if m+n < total_states:

            for k in range(0, m+1):

                m_choose_k = math.factorial(m) / (math.factorial(k) * math.factorial(m - k))
                p_k_arrivals = m_choose_k * (p_arrival ** k) * ((1 - p_arrival) ** m - k)

                sum_emergency += p_k_arrivals * dict[(t+1, m-k, n+k)]

                if n+k-1 > 0:

                    sum_no_emergency += p_k_arrivals * dict[(t+1, m-k, n+k-1)]

                else:

                    sum_no_emergency += p_k_arrivals * dict[(t+1, m, 0)]

            if n == 0:

                return r + p * sum_emergency + (1 - p) * sum_no_emergency

            else:

                return r - (n - 1) * wC + p * sum_emergency + (1 - p) * sum_no_emergency

print(schedule(35, 10))