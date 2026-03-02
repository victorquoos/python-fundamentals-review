def format_time(name: str, day_period: str):
    return f"Good {day_period}, {name}!"


def get_evens(numbers: list[int]):
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n)
    return result


def tip_calculator(bill_amount: float, tip_percentage: float):
    return bill_amount + bill_amount*tip_percentage
