import random
import string

NUMBER_WORDS = [
    "zero", "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten"
]

SYMBOLS = "!@#$%^&*()_+=-[]{}|;:',.<>?/"

def _normal_int():
    return str(random.randint(-10**6, 10**6))

def _big_int():
    digits = random.randint(50, 1000)
    sign = random.choice(["", "-", "+"])
    return sign + "".join(random.choices(string.digits, k=digits))

def _scientific():
    """Generate scientific notation numbers."""
    base = random.uniform(-1000, 1000)
    exp = random.randint(-10, 10)
    return f"{base}e{exp}"

def _infinity():
    """Generate infinity representations."""
    return random.choice(["inf", "-inf", "Infinity", "-Infinity", "+inf"])

def _mixed_numeric():
    return f"{random.randint(1,999)}{random.choice(SYMBOLS)}{random.randint(1,999)}"

def _garbage():
    charset = string.ascii_letters + string.digits + SYMBOLS
    return "".join(random.choices(charset, k=random.randint(5, 50)))

def _spelled():
    return " ".join(random.choices(NUMBER_WORDS, k=random.randint(1, 5)))

def _empty():
    return " " * random.randint(0, 5)

def generate(path: str, count: int) -> None:
    """
    Generate a file with mixed numeric and invalid data.
    
    Enhanced with edge cases:
    - Scientific notation
    - Infinity representations
    """
    
    generators = [
        (_normal_int, 40),
        (_big_int, 18),
        (_scientific, 7),   
        (_infinity, 3),    
        (_mixed_numeric, 10),
        (_garbage, 10),
        (_spelled, 10),
        (_empty, 2),
    ]
    weighted = [g for g, w in generators for _ in range(w)]

    with open(path, "w", encoding="utf-8") as f:
        for _ in range(count):
            f.write(random.choice(weighted)() + "\n")
