from typing import cast
from typing import TYPE_CHECKING

import pandas as pd


# This file holds shared objects
# It should not import anything from the project to avoid circular dependencies

# This is used to ensure that mypy knows this should be a DataFrame even if it is None initially
if TYPE_CHECKING:
    conversations_df = cast(
        pd.DataFrame, None
    )  # pylint: disable=used-before-assignment
else:
    conversations_df = None

if TYPE_CHECKING:
    conversations_agg_df = cast(
        pd.DataFrame, None  # pylint: disable=used-before-assignment
    )
else:
    conversations_agg_df = None
