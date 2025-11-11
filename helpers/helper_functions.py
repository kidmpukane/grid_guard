import random


def gen_id_segment(count):
    """Generates a random string of digits for a unique ID segment."""
    return ''.join(str(random.randint(0, 9)) for _ in range(count))


def generate_event_id():
    """Generates a unique, structured Event ID."""
    return f"PV-{gen_id_segment(3)}-{gen_id_segment(3)}-{gen_id_segment(2)}"
