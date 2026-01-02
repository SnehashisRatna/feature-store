import pandas as pd

def compute_feature(raw_table, logic: str):
    """
    raw_table: RawTable ORM object
    logic: feature logic (string)
    """

    # Step 1: Load raw data
    if raw_table.source_type != "csv":
        raise ValueError("Only CSV source supported for now")

    df = pd.read_csv(raw_table.location)

    # Step 2: Ensure entity column exists
    if raw_table.entity_column not in df.columns:
        raise ValueError("Entity column missing in raw data")

    # Step 3: Execute feature logic
    # Example logic: "df.groupby('user_id')['amount'].mean()"
    try:
        result = eval(logic)
    except Exception as e:
        raise ValueError(f"Feature logic failed: {e}")

    # Step 4: Convert result to dictionary
    return result.to_dict()
