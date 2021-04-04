"""Module to setup fastapi API to expose API to the outside world."""
import logging
import random
from typing import Any, Dict

from fastapi import FastAPI
import uvicorn

ERROR_CODES = [error_code for error_code in range(50)]
LOGGER = logging.getLogger("API")
app = FastAPI()


def _generate_lists() -> Dict[str, Any]:
    """Generate resolved, unresolved and backlog lists."""
    return {
        'resolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error ABC occured, that is `resolved`'
        } for error_idx in range(50)],
        'unresolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error DEF occured, that is `unresolved`'
        } for error_idx in range(50, 100)],
        'backlog': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error XYZ occured, that is in the `backlog`'
        } for error_idx in range(100, 150)]
    }


@app.get("/get_lists")
def get_lists() -> Dict[str, Any]:
    """Return resolved, unresolved and backlog lists."""
    LOGGER.info('Generating resolved, unresolved and backlog lists.')
    return _generate_lists()


@app.get("/get_list_intersection_counts")
def get_list_intersection_counts() -> Dict[str, int]:
    """Return the error intersection counts between a set of resolved, unresolved and backlog lists.

    Returns
    -------
    intersection_counts: Dict[str, int]
        The intersection counts between resolved, unresolved and backlog lists, e.g.:
        ```json
        {
            "resolved_unresolved": 12,
            "resolved_backlog": 6,
            "unresolved_backlog": 35
        }
        ```
        `"resolved_unresolved": 12` describes that there are `12` errors with the *same error code*  shared
        between a `resolved` and `unresolved` list, `"resolved_backlog": 6` describes that there are `6`
        errors with the *same error code*  shared between a `resolved` and `backlog` list.

        The three lists required for this calculation are generated by calling `_generate_lists`.

        Code that checks whether errors from the resolved and unresolved list `intersect`, could look like:
        ```python
        error_lists = _generate_lists()
        resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

        error_from_resolved = resolved[0]
        error_from_unresolved  = unresolved[0]
        if error_from_resolved.code == error_from_unresolved.code:
            print('Errors intersect')
        else:
            print('Errors do not intersect')
        ```

    """
    LOGGER.info('Generating the intersection counts between a set of resolved, unresolved and backlog lists.')

    error_lists = _generate_lists()
    resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

    # TODO: Implement the code that calculates how many errors with *the same error code* are shared between
    # the possible pairs of lists here. Then return a Dict like the one shown in the documentation string above,
    # e.g.:

    ''' I love python but so far i have not used it a lot so the following solution is a mix of trial and error, learning and stack overflow.
     I tried to do all of this in a much simpler way but i was getting "TypeError: unhashable type: 'dict' " so i decided to get the
     error codes and append in a list because then it would be easier to work with set. The i have 3 simple for loops that for each item (x) 
     in resolved, unresolved and backlog, it would append its error code to the list.
     The i tried only for resolved_unresolved exactly what i tried earlier when i was getting TypeError and it worked this time
     thanks to having the error codes in separate lists.
     Then i did exactly the same for the next two. Next i went into the return and for each i returned not the list with duplicates 
     numbers but its lenght.
     '''


    resolvedset = []
    unresolvedset = []
    backlogset = []
    for x in resolved:
        resolvedset.append(x['code'])
    for x in unresolved:
        unresolvedset.append(x['code'])
    for x in backlog:
        backlogset.append(x['code'])
    
    intersection_resolved_unresolved = set.intersection(set(resolvedset), set(unresolvedset))
    intersection_list_resolved_unresolved = list(intersection_resolved_unresolved)

    intersection_unresolved_backlog = set.intersection(set(unresolvedset), set(backlogset))
    intersection_list_unresolved_backlog = list(intersection_unresolved_backlog)

    intersection_resolved_backlog = set.intersection(set(resolvedset), set(backlogset))
    intersection_list_resolved_backlog = list(intersection_resolved_backlog)

    return  {
        'resolved_unresolved': len(intersection_list_resolved_unresolved),
        'resolved_backlog': len(intersection_list_unresolved_backlog),
        'unresolved_backlog': len(intersection_list_resolved_backlog),
    }
    # NOTE: THIS IS JUST AN EXAMPLE, REPLACE WITH YOUR OWN CODE AND `return`!


def run(host: str, port: int) -> None:
    """Run the code challenge API."""
    uvicorn.run(app, host=host, port=port)

