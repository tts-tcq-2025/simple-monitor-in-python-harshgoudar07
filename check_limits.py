
class Parameter:
    def __init__(self, name, min_limit, max_limit):
        self.name = name
        self.min = min_limit
        self.max = max_limit

    def is_within_range(self, value):
        if value < self.min:
            return False, "LOW"
        if value > self.max:
            return False, "HIGH"
        return True, None


class Reporter:
    def report(self, parameter_name, status, breach=None):
        if status:
            return
        message = f"{parameter_name} is out of range!"
        if breach:
            message += f" Breach: {breach}"
        print(message)


def battery_is_ok(parameters, readings, reporter=Reporter()):
    all_ok = True
    for param in parameters:
        value = readings.get(param.name)
        if value is None:
            raise ValueError(f"Missing reading for {param.name}")
        is_ok, breach = param.is_within_range(value)
        reporter.report(param.name, is_ok, breach)
        all_ok = all_ok and is_ok
    return all_ok


if __name__ == '__main__':
    PARAMETERS = [
        Parameter("temperature", 0, 45),
        Parameter("soc", 20, 80),
        Parameter("charge_rate", 0, 0.8)
    ]

    # Test cases
    assert battery_is_ok(PARAMETERS, {"temperature": 25, "soc": 70, "charge_rate": 0.7}) is True
    assert battery_is_ok(PARAMETERS, {"temperature": -5, "soc": 70, "charge_rate": 0.7}) is False
    assert battery_is_ok(PARAMETERS, {"temperature": 25, "soc": 85, "charge_rate": 0.7}) is False
    assert battery_is_ok(PARAMETERS, {"temperature": 25, "soc": 70, "charge_rate": 0.9}) is False

