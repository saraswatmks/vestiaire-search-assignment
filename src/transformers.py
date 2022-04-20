from dataclasses import dataclass

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class Transformer(BaseEstimator, TransformerMixin):
    """Abstract base class from which to create a data Transformer."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        raise NotImplementedError(
            "This method must be implemented in derived classes"
        )


@dataclass
class FilterSessions(Transformer):
    """Filters out sessions with just 1 search query."""

    N_SEARCH: int = 1

    def transform(self, df: pd.DataFrame):
        sessions = (
            df.session.value_counts().loc[lambda x: x > self.N_SEARCH].index
        )
        return df.query("session in @sessions").copy()


@dataclass
class TextProcessing(Transformer):
    """Runs basic text processing."""

    _cols = ["query", "title"]

    def transform(self, df: pd.DataFrame):
        for col in self._cols:
            df[col] = df[col].str.lower().str.strip()
        return df


@dataclass
class CreateGroupId(Transformer):
    """Puts a search query & its pageview into separate groups."""

    def transform(self, df: pd.DataFrame):
        ser = (
            df.query("name == 'search'")
            .groupby(["session", "name"])
            .cumcount()
            + 1
        )
        df.loc[ser.index, "id"] = ser
        df["id"] = df["id"].ffill()
        df["id"] = df["id"].astype(int)
        return df


@dataclass
class CreateMainCategory(Transformer):
    """
    Assumes search query to have similar category to category to
    pages clicked immediately. This helps us having more training
    data. This way we can leverage page titles also as a search query
    data.
    """

    def transform(self, df: pd.DataFrame):
        df["search_title"] = df["query"].combine_first(df["title"])
        df["category_main"] = df["category"].copy()
        df["category_main"] = df.groupby(["session", "id"])[
            "category_main"
        ].bfill()
        return df


class MapCategoryToQueries(Transformer):
    """Create a map of category to queries."""

    def transform(self, df: pd.DataFrame):
        grp = (
            df.groupby("category_main")["search_title"]
            .apply(list)
            .reset_index()
        )
        grp = grp.rename(
            columns={"category_main": "category", "search_title": "title"}
        )
        grp["title"] = grp["title"].str.join(" ")
        return grp


def process_pipeline(X: pd.DataFrame):
    pipe = Pipeline(
        [
            ("FilterSessions", FilterSessions()),
            ("TextProcessing", TextProcessing()),
            ("CreateGroupId", CreateGroupId()),
            ("CreateMainCategory", CreateMainCategory()),
            ("MapCategoryToQueries", MapCategoryToQueries()),
        ]
    )
    return pipe.transform(X)
