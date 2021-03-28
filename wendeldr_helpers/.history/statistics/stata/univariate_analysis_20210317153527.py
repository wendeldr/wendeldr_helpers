import pandas as pd

def save_univariate_list(path):



def save_univariate_list_dan(path):
    global univariate_list

    df = pd.DataFrame(univariate_list)

    df = df.replace('.',np.nan)
    df = df.replace('inf',np.nan)
    df = df.astype({'covariate':str,
                    'stats_missing_0':float,
                    'stats_missing_0_precent':float,
                    'stats_missing_1':float,
                    'stats_missing_1_precent':float,
                    'stats_mean_0':float,
                    'stats_mean_1':float,
                    'stats_mean_tot':float,
                    'stats_se_0':float,
                    'stats_se_1':float,
                    'stats_se_tot':float,
                    'stats_n_0':float,
                    'stats_n_1':float,
                    'stats_n_tot':float,
                    'stats_sd_0':float,
                    'stats_sd_1':float,
                    'stats_sd_tot':float,
                    'stats_skew_0':float,
                    'stats_skew_1':float,
                    'stats_skew_tot':float,
                    'stats_kurt_0':float,
                    'stats_kurt_1':float,
                    'stats_kurt_tot':float,
                    'stats_min_0':float,
                    'stats_min_1':float,
                    'stats_min_tot':float,
                    'stats_p25_0':float,
                    'stats_p25_1':float,
                    'stats_p25_tot':float,
                    'stats_p50_0':float,
                    'stats_p50_1':float,
                    'stats_p50_tot':float,
                    'stats_p75_0':float,
                    'stats_p75_1':float,
                    'stats_p75_tot':float,
                    'stats_max_0':float,
                    'stats_max_1':float,
                    'stats_max_tot':float,
                    'ttest_pvalue':float,
                    'power_val':float,
                    'logit_odds':float,
                    'logit_stderr':float,
                    'logit_z':float,
                    'logit_pvalue':float,
                    'logit_lowerCI':float,
                    'logit_higherCI':float,
                    'roc_rocnum':float,
                    'roc_area':float,
                    'stcox_haz':float,
                    'stcox_stderr':float,
                    'stcox_z':float,
                    'stcox_pvalue':float,
                    'stcox_lowerCI':float,
                    'stcox_higherCI':float})

    df.save()