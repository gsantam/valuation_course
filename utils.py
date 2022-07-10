def mergeFuzzyDate(df_main, df_aux, date_main, date_aux, join_by = None, aux_features = None, debug = False):
    """
    Merge two dataframes by fuzzy date.
    - df_main: main dataframe
    - df_aux: auxiliar dataframe
    - date_main: date column in df_main
    - date_aux: date column in df_aux
    - join_by: list of column to join by in df_main and df_aux
    - aux_features: list of features to merge in df_main and df_aux. All except date_aux if None.
    """
    import pandas as pd
    from datetime import datetime, timedelta

    if aux_features is None:
        aux_features = [feature for feature in df_aux.columns if feature != date_aux]
        if join_by is not None:
            aux_features = [feature for feature in aux_features if feature not in join_by]

    else:
        keep_features = aux_features + [date_aux] 
        if join_by is not None:
            keep_features = keep_features + join_by
        df_aux = df_aux[keep_features]

    df_main = df_main.sort_values(date_main)
    df_aux = df_aux.sort_values(date_aux)

    df_main = pd.merge_asof(df_main, df_aux.rename(columns = {date_aux: 'Date_nearest'}), by = join_by, \
        left_on = date_main, right_on = 'Date_nearest', direction = 'nearest')
    df_main = pd.merge_asof(df_main, df_aux.rename(columns = {date_aux: 'Date_back'}), by = join_by, \
        left_on = date_main, right_on = 'Date_back', direction = 'backward')
    df_main = pd.merge_asof(df_main, df_aux.rename(columns = {date_aux: 'Date_14D'}), by = join_by, \
        left_on = date_main, right_on = 'Date_14D', direction = 'nearest',  tolerance = timedelta(days = 14))

    for feature in aux_features:
        df_main[feature] = df_main[feature].fillna(df_main[f"{feature}_y"]).fillna(df_main[f"{feature}_x"])

    if not debug:
        df_main.drop(columns = ['Date_14D', 'Date_back', 'Date_nearest'], inplace = True)
        for feature in aux_features:
            df_main.drop(columns = [f"{feature}_x", f"{feature}_y"], inplace = True)
        
    return df_main

# betas_industry = getBetasIndustry(global_ind = global_ind)
# betas_industry['test'] = np.random.rand(len(betas_industry2))
# betas_industry
# mergeFuzzyDate(data, betas_industry, date_main = 'date', date_aux = 'Date', join_by = ['Industry'], aux_features = ['test'], debug = True)