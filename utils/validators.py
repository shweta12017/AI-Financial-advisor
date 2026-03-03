from typing import Optional, Tuple, Union


NumberLike = Union[float, int, str]


def to_positive_float(value: Optional[NumberLike]) -> float:
    """
    Coerce input to a non-negative float.

    Invalid inputs and negatives both become 0.0.
    This keeps Streamlit inputs robust against edge cases and string values.
    """
    if value is None:
        return 0.0
    try:
        f = float(value)
        return max(f, 0.0)
    except (TypeError, ValueError):
        return 0.0


def validate_goal(target_amount: float, years: float) -> Tuple[bool, str]:
    """
    Validate that a goal has a sensible target amount and time horizon.

    Returns (is_valid, message). On success, message is empty.
    """
    if target_amount <= 0:
        return False, "Goal target amount must be greater than 0."
    if years <= 0:
        return False, "Goal time horizon (years) must be greater than 0."
    if years > 100:
        return False, "Time horizon is unrealistically long; please reduce it."
    return True, ""

