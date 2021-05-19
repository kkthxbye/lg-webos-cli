from typing import Callable, Dict, Iterable, Tuple, Union

from pywebostv.controls import WebOSControlBase


def unpack_payload(payload: Union[Dict, Callable]) -> Iterable:
    return payload if isinstance(payload, dict) else []


def format_controls_help(controls: Dict[str, Tuple[WebOSControlBase, Dict]]):
    return '\n'.join(' '.join(x for x in [
        control,
        ' '.join(f'[{x}]' for x in unpack_payload(config.get('payload', {}))),
        ' '.join(f'({x})' for x in [*[x.__name__ for x in config.get('args', [])], *config.get('kwargs', {}).keys()]),
    ] if x) for control, (_, config) in controls.items())
