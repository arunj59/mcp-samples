# tools/file_reader_tools.py

# from server import mcp
from mcp.server.fastmcp import FastMCP
import pandas as pd
from pathlib import Path
# Base directory where our data lives

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
def read_csv_summary(filename: str) -> str:
    """
    Read a CSV file and return a simple summary.
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    return f"CSV file '{filename}' has {len(df)} rows and {len(df.columns)} columns."
def read_parquet_summary(filename: str) -> str:
    """
    Read a Parquet file and return a simple summary.
    Args:
        filename: Name of the Parquet file (e.g. 'sample.parquet')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_parquet(file_path)
    return f"Parquet file '{filename}' has {len(df)} rows and {len(df.columns)} columns."

mcp = FastMCP("file_reader_tools")

@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Summarize a CSV file by reporting its number of rows and columns.
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
    Returns:
        A string describing the file's dimensions.
    """
    return read_csv_summary(filename)

@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarize a Parquet file by reporting its number of rows and columns.
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
    Returns:
        A string describing the file's dimensions.
    """
    return read_parquet_summary(filename)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')