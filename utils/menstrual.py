from datetime import datetime

def estimate_cycle_phase(last_period_start, cycle_length=28):
    try:
        start = datetime.strptime(last_period_start, "%Y-%m-%d")
        today = datetime.today()
        days = (today - start).days % cycle_length

        if days <= 5:
            return "Menstrual"
        elif 6 <= days <= 13:
            return "Follicular"
        elif days == 14:
            return "Ovulation"
        else:
            return "Luteal"
    except:
        return None
