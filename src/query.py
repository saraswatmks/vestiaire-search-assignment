import logging
import os
import sqlite3

import pandas as pd

from .transformers import process_pipeline

logger = logging.getLogger()


class Vars:
    training_data: str = "data/predict_category/events.log"


class QueryToCategory(Vars):

    # variables used internally
    _data = None
    _processed_data = None
    _cur = None

    def __init__(self):
        self._load_data()
        self._process_data()
        self._build_db(df=self._processed_data)

    def _load_data(self):
        self._data = pd.read_json(self.training_data, lines=True)

    def _process_data(self):
        self._processed_data = process_pipeline(self._data)

    def _build_db(self, df: pd.DataFrame):
        db = sqlite3.connect(":memory:")
        self._cur = db.cursor()
        self._cur.execute(
            'create virtual table logs using fts5(title, category, tokenize="porter unicode61 ");'
        )
        self._cur.executemany(
            "insert into logs (title, category) values (?,?);",
            df[["title", "category"]].to_records(index=False),
        )
        db.commit()

    def search(self, query):

        query = query.lower().strip()
        cat = None
        # do exact match
        if not cat:
            cat = self._cur.execute(
                f"""select category
                    from logs
                    where title MATCH "{query}"
                    limit 1"""
            ).fetchall()
        # do partial match for spell errors
        if not cat:
            queryp = " ".join(f"{w}*" for w in query.split())
            cat = self._cur.execute(
                f"""select category
                    from logs
                    where title MATCH "{queryp}"
                    limit 1"""
            ).fetchall()
        logger.info(f"Predicted category: {cat}")
        return cat
