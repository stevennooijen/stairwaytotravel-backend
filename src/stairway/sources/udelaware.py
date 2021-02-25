import netCDF4
import pandas as pd


def netcdf_to_pandas(file_path: str, last_x_years: int = 30) -> pd.DataFrame:
    """
    Parses either the air or precip weather dataset from the University of
    Delaware and outputs the not null data in a long format pandas dataframe.
    Data per month is averaged over the `last_x_years`.

    Parameters
    ----------
    file_path: str
        Path to the input dataset.
    last_x_years: int
        Last X years to average the data over.

    Returns
    -------
    out: DataFrame
        Long format data frame containing weather averages per month.
    """
    variable_name = file_path.split("/")[-1].split(".")[0]
    column_name = "temp" if variable_name == "air" else "precip"

    data = netCDF4.Dataset(file_path)

    last_x_months = last_x_years * 12
    subset = data.variables[variable_name][-last_x_months:, :, :]

    temp_monthly = []
    for month_id in range(12):
        monthly_means = subset[range(month_id, 30 * 12, 12), :, :].mean(axis=0)
        monthly_means = (
            pd.DataFrame(
                data=monthly_means,
                index=data.variables["lat"],
                columns=data.variables["lon"],
            )
            .unstack()
            .reset_index()
            .rename(columns={0: column_name})
            .loc[lambda df: df[column_name].notnull()]
            .assign(month=month_id)
        )
        temp_monthly.append(monthly_means)

    return pd.concat(temp_monthly)
