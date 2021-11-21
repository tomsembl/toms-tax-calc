def comma_number(number): return ("{:,}".format(number))

def austax(gross, is_hecs):
    #Error Handling
    if type(gross) not in (int, float): raise TypeError(f"type {type(gross)} is not int or float")
    if gross < 0 or gross > 10**20: raise ValueError("outside of bounds 0 - 10²⁰")

    #Tax
    if gross >= 180001: tax = 51667 + 0.45 * (gross - 180000)
    elif gross >= 120001: tax = 29467 + 0.37 * (gross - 120000)
    elif gross >= 45001: tax = 5092 + 0.325 * (gross - 45000)
    elif gross >= 18201: tax = 0.19 * (gross - 18200)
    else: tax = 0
    tax_percent = round(100*tax/(gross+0.01), 2)

    #HECS
    if is_hecs:
        hecs_brackets = [0, 47014, 54283, 57539, 60992, 64652, 68530, 72642, 77002, 81621, 86519, 91710, 97213, 103046, 109228, 115782, 122729, 130093, 137898, 10**20]
        hecs_percents = [0, 0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.1]
        for i, hecs_bracket in enumerate(hecs_brackets):
            if i == len(hecs_brackets)-1: break #error handling
            if hecs_bracket <= gross < hecs_brackets[i+1]: hecs_percent = hecs_percents[i]
        hecs = gross * hecs_percent
        hecs_percent = round(100*hecs_percent, 2)
    
    net = gross - tax - hecs if is_hecs else gross - tax
    net_percent = round(100-hecs_percent-tax_percent if is_hecs else 100-tax_percent, 2)
    
    #formatting
    gross = comma_number(gross); net = comma_number(int(net)); tax = comma_number(int(tax))
    if is_hecs: hecs = comma_number(int(hecs))

    #Output
    return f"Gross:${gross}: , Net:${net}:({net_percent}%), Tax:${tax}:({tax_percent}%)" + (f", HECS:${hecs}:({hecs_percent}%)" if is_hecs else "")

