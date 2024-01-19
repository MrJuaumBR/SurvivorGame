"""
Database Creation, Setup and Connection
"""

from ..config import DATABASE_PATH,AUINS

try:
    from JPyDB import (pyDatabase, Columns, Tables)
except ModuleNotFoundError:
    AUINS.InstallJPyDB()
    from JPyDB import (pyDatabase, Columns, Tables)

DB = pyDatabase(DATABASE_PATH, 'pydata')