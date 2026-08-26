import logging
import os
from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

logger = logging.getLogger(__name__)

class PostgresStore:
    """
    PostgresSQL connection layer for MyEDR
    uses a psycopg3 connection pool and returns rows as normal python dictionaries
    """
    def __init__(self, db_url: str | None=None, min_size:int=1,max_size:int=5):
        self.db_url=db_url or os.getenv("DATABASE_URL")

        if not self.db_url:
            raise ValueError("DATABASE_URL is not set")

        self.pool=ConnectionPool(
            conninfo=self.db_url,
            min_size=min_size,
            max_size=max_size,
            timeout=30,
            kwargs={
                "row_factory": dict_row,
                "prepare_threshold": None
            },
        )

        #fail immediately if the database isn't reachable
        self.pool.wait()

        logger.info("Postgres connection pool ready")


    def execute(self, query:str, params: tuple[Any, ...]=(),)-> dict[str, Any]:
        """
        Execute INSERT / UPDATE / DELETE / DDL
        queries using RETURNING can return the inserted/updated row
        """

        with self.pool.connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(query, params)

                    row=None

                    if cur.description:
                        row=cur.fetchone()

                    conn.commit()

                    return {
                        "lastrowid": (row.get("id") if row else None),
                        "row_count": cur.rowcount,
                        "row": row
                        }

            except Exception:
                conn.rollback()
                logger.exception("Database execute failed: %s", query)
                raise


    def fetch_all(self, query: str, params: tuple[Any, ...] = (),) -> list[dict[str, Any]]:
        """
        Execute SELECT and return all rows.
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()


    def fetch_one(self, query:str, params:tuple[Any, ...]=())-> dict[str, Any] | None:
        """
        Execute SELECT and return one row
        """

        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                return cur.execute(query, params,).fetchone()


    def ping(self)->None:
        """
        Raise an exception if PostgresSQL isn't reachable
        """

        self.fetch_one("SELECT 1")


    def close(self)->None:
        """
        Close the connection pool
        """
        self.pool.close()

        logger.info("Postgres connection pool closed")