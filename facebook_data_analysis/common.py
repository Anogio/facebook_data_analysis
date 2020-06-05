from typing import cast
from typing import TYPE_CHECKING

import pandas as pd


# This file holds shared objects
# It should not import anything from the project to avoid circular dependencies
# NB: this will not work for a server used by more than one user:
#     it is fine for local usage but we would need to use Store otherwise

# This is used to ensure that mypy knows this should be a DataFrame even if it is None initially
if TYPE_CHECKING:
    conversations_df = cast(
        pd.DataFrame, None
    )  # pylint: disable=used-before-assignment
else:
    conversations_df = None


class FacebookName:
    def __init__(self, name: str):
        self.name = name


# Holds common informations such as your facebook name
if TYPE_CHECKING:
    my_name = cast(FacebookName, None)  # pylint: disable=used-before-assignment
else:
    my_name = None
