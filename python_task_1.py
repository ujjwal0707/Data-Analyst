import pandas as pd

def generate_car_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(len(car_matrix))]*2] = 0  # Set diagonal values to 0
    return car_matrix

def get_type_count(df: pd.DataFrame) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    type_counts = df['car'].value_counts().to_dict()
    return type_counts

def get_bus_indexes(df: pd.DataFrame) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    bus_indexes = df[df['car'] == 'bus'][df['car'].gt(2 * df['car'].mean())].index.tolist()
    return bus_indexes

def filter_routes(df: pd.DataFrame) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    avg_truck_per_route = df.groupby('route')['car'].mean()
    routes_above_7 = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()
    return routes_above_7

def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 2 if x > 5 else x)
    return modified_matrix

def time_check(df: pd.DataFrame, dataset_2: pd.DataFrame) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)
        dataset_2 (pandas.DataFrame): Assuming this DataFrame has columns 'id', 'id_2', 'timestamp'

    Returns:
        pd.Series: return a boolean series
    """
    merged_df = pd.merge(df, dataset_2, on=['id', 'id_2'])
    time_diff = (merged_df['timestamp_y'] - merged_df['timestamp_x']).dt.total_seconds()
    completeness_check = (time_diff >= 0) & (time_diff <= 24 * 3600 * 7)
    return completeness_check
