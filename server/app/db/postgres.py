import logging
import os
from typing import Any

from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool


logger = logging.getLogger(__name__)


class PostgresStore:
    """
    PostgreSQL database wrapper for MyEDR.

    Responsibilities:
    - Manage a bounded PostgreSQL connection pool.
    - Execute parameterized SQL.
    - Return rows as dictionaries.
    - Adapt Python dict/list values to PostgreSQL JSONB.
    - Provide basic database health checking.
    """

    def __init__(self, db_url: str | None = None, min_size: int = 1, max_size: int = 5):
        self.db_url = db_url or os.getenv("DATABASE_URL")

        if not self.db_url:
            raise ValueError("DATABASE_URL is not set")

        self.pool = ConnectionPool(
            conninfo=self.db_url,
            min_size=min_size,
            max_size=max_size,
            timeout=30,
            kwargs={
                "row_factory": dict_row,
                "prepare_threshold": None,
            },
        )

        # Fail fast during application startup.
        self.pool.wait()

        logger.info("Postgres connection pool ready")

    @staticmethod
    def _adapt_params(params: tuple[Any, ...]) -> tuple[Any, ...]:
        """
        Convert Python dict/list values to JSONB.

        Psycopg otherwise treats them as regular Python
        objects rather than PostgreSQL JSONB values.
        """

        return tuple(Jsonb(value) if isinstance(value, (dict, list)) else value for value in params)

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any]:
        """
        Execute a write query.

        For queries using RETURNING, the returned row is
        available through result["row"].

        Returns:
            {
                "row": dict | None,
                "row_count": int,
            }
        """

        with self.pool.connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, self._adapt_params(params))

                    row = (cursor.fetchone() if cursor.description else None)

                    row_count = cursor.rowcount

                    conn.commit()

                    return {
                        "row": row,
                        "row_count": row_count,
                    }

            except Exception:
                conn.rollback()

                logger.exception("Postgres execute failed: %s", query)

                raise

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        """
        Execute a SELECT and return one row.
        """

        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, self._adapt_params(params))

                return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        """
        Execute a SELECT and return all rows.
        """

        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, self._adapt_params(params))

                return cursor.fetchall()

    def ping(self) -> None:
        """
        Verify that PostgreSQL is reachable.

        Raises an exception if the database is unavailable.
        """

        self.fetch_one("SELECT 1")

    def close(self) -> None:
        """
        Close the PostgreSQL connection pool.
        """

        self.pool.close()

        logger.info("Postgres connection pool closed")