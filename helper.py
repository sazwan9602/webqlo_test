import pandas as pd

def data_df():
    """
    Read raw excel file
    :return:
    """
    df = pd.read_excel('OppoMalaysia_Raw_File.xlsx')
    return df


def filter_by_date(start, end):
    """
    Filter dataframe based on date range
    :param start: start date
    :param end: end date
    :return:
    """
    df = data_df()
    date_df = pd.to_datetime(df['created_timestamp'].dt.date)

    filtered_date = df[(date_df >= start) & (date_df <= end)]
    return filtered_date


def cleaned_df(df, col):
    """
    Filter out null column of dataframe
    :param df: Dataframe
    :param col: column name
    :return:
    """
    df = df[df[col].notnull()]

    return df


def get_interaction_summary(df):
    """
    Calculate summary for interaction by type:
        - photo
        - video
        - others
    :param df: dataframe
    :return:
    """
    in_df = cleaned_df(df, 'interactions')
    total_interaction = in_df['interactions'].sum()

    # use if else in one line
    df_id = df['type'].iloc[0] if df['type'].iloc[0] == 'photo' or df['type'].iloc[0] == 'video' else 'others'
    interaction_dict = {
        'id': df_id,
        'name': df_id.capitalize(),
        'count': len(df),
        'interactions': int(total_interaction)
    }
    return interaction_dict

