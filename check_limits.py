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


def validate_parameter(param, value, reporter):
    is_ok, breach = param.is_within_range(value)
    reporter.report(param.name, is_ok, breach)
    return is_ok


def battery_is_ok(parameters, readings, reporter=None):
    reporter = reporter or Reporter()
    return all(
        validate_parameter(param, readings.get(param.name), reporter)
        for param in parameters
    )


if __name__ == '__main__':
    PARAMETERS = [
        Parameter("temperature", 0, 45),
        Parameter("soc", 20, 80),
        Parameter("charge_rate", 0, 0.8)
    ]

    assert battery_is_ok(PARAMETERS, {"temperature": 25, "soc": 70, "charge_rate": 0.7}) is True
    assert battery_is_ok(PARAMETERS, {"temperature": -1, "soc": 70, "charge_rate": 0.7}) is False
    assert battery_is_ok(PARAMETERS, {"temperature": 25, "soc": 85, "charge_rate": 0.7}) is False
    assert battery_is_ok(PARAMETERS, {"temperature": 25, "soc": 70, "charge_rate": 0.9}) is False
    assert battery_is_ok(PARAMETERS, {"temperature": -1, "soc": 85, "charge_rate": 0.9}) is False
