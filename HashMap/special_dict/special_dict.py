import re
from typing import Any, Dict, Tuple

class ConditionError(Exception):
    pass

class SpecialDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sorted_keys = sorted(self.keys())

    def _update_sorted_keys(self):
        self._sorted_keys = sorted(self.keys())

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._update_sorted_keys()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._update_sorted_keys()

    @property
    def iloc(self):
        class ILocAccessor:
            def __init__(self, outer):
                self.outer = outer

            def __getitem__(self, index):
                if not (0 <= index < len(self.outer._sorted_keys)):
                    raise IndexError("ILoc index out of range")
                key = self.outer._sorted_keys[index]
                return self.outer[key]

        return ILocAccessor(self)

    @property
    def ploc(self):
        class PLocAccessor:
            def __init__(self, outer):
                self.outer = outer

            def __getitem__(self, condition):
                try:
                    conditions = self._parse_condition(condition)
                    result = {}

                    for key, value in self.outer.items():
                        parsed_key = self._parse_key(key)

                        if not parsed_key or len(parsed_key) != len(conditions):
                            continue

                        if self._evaluate_conditions(parsed_key, conditions):
                            result[key] = value

                    return result
                except Exception as e:
                    raise ConditionError(f"Invalid condition: {condition}") from e

            def _parse_condition(self, condition: str) -> Tuple[str, ...]:
                condition = re.sub(r'[\s()]+', '', condition)
                parts = re.split(r'[,;]', condition)
                return tuple(parts)

            def _parse_key(self, key: Any) -> Tuple[float, ...]:
                try:
                    if isinstance(key, str):
                        key = re.sub(r'[\\s()]+', '', key)
                        return tuple(map(float, re.split(r'[,;]', key)))
                    elif isinstance(key, (tuple, list)):
                        return tuple(map(float, key))
                    else:
                        return (float(key),)
                except ValueError:
                    return ()

            def _evaluate_conditions(self, key_parts: Tuple[float, ...], conditions: Tuple[str, ...]) -> bool:
                for key_part, condition in zip(key_parts, conditions):
                    if not self._evaluate_single_condition(key_part, condition):
                        return False
                return True

            def _evaluate_single_condition(self, key_part: float, condition: str) -> bool:
                match = re.match(r'(<=|>=|<>|<|>|=)\s*(-?\d+(\.\d+)?)', condition.strip())
                if not match:
                    raise ConditionError(f"Invalid condition syntax: {condition}")

                operator, value = match.groups()[:2]
                value = float(value)

                if operator == "<":
                    return key_part < value
                elif operator == ">":
                    return key_part > value
                elif operator == "<=":
                    return key_part <= value
                elif operator == ">=":
                    return key_part >= value
                elif operator == "=":
                    return key_part == value
                elif operator == "<>":
                    return key_part != value
                else:
                    raise ConditionError(f"Unknown operator: {operator}")

        return PLocAccessor(self)
