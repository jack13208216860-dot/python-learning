def add(number1, number2):
    return number1 + number2

def is_adult(age):
    if age >= 18:
        return True
    else:
        return False

def get_grade(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"