import os
import pandas as pd
import numpy as np

def parse_univariate_log(file, header=0, footer=0):
    longitudinal_header = ['cohort','covariate','stats_missing_0', 'stats_missing_0_precent', 'stats_missing_1', 'stats_missing_1_precent','stats_mean_0','stats_mean_1','stats_mean_tot','stats_se_0','stats_se_1','stats_se_tot','stats_n_0','stats_n_1','stats_n_tot','stats_sd_0','stats_sd_1','stats_sd_tot','stats_skew_0','stats_skew_1','stats_skew_tot','stats_kurt_0','stats_kurt_1','stats_kurt_tot','stats_min_0','stats_min_1','stats_min_tot','stats_p25_0','stats_p25_1','stats_p25_tot','stats_p50_0','stats_p50_1','stats_p50_tot','stats_p75_0','stats_p75_1','stats_p75_tot','stats_max_0','stats_max_1','stats_max_tot','ttest_pvalue','power_val','stats_effect_size_basic','stats_es_cohend','stats_es_hedgesg','stats_es_glassdelta1','stats_es_glassdelta2','stats_es_pointbiserial','logit_odds','logit_stderr','logit_z','logit_pvalue','logit_lowerCI','logit_higherCI','roc_rocnum','roc_area','stcox_haz','stcox_stderr','stcox_z','stcox_pvalue','stcox_lowerCI','stcox_higherCI']
    # longitudinal_header = ['cohort','covariate','stats_missing_0', 'stats_missing_0_precent', 'stats_missing_1', 'stats_missing_1_precent','stats_mean_0','stats_mean_1','stats_mean_tot','stats_se_0','stats_se_1','stats_se_tot','stats_n_0','stats_n_1','stats_n_tot','stats_sd_0','stats_sd_1','stats_sd_tot','stats_skew_0','stats_skew_1','stats_skew_tot','stats_kurt_0','stats_kurt_1','stats_kurt_tot','stats_min_0','stats_min_1','stats_min_tot','stats_p25_0','stats_p25_1','stats_p25_tot','stats_p50_0','stats_p50_1','stats_p50_tot','stats_p75_0','stats_p75_1','stats_p75_tot','stats_max_0','stats_max_1','stats_max_tot','ttest_pvalue','power_val','logit_odds','logit_stderr','logit_z','logit_pvalue','logit_lowerCI','logit_higherCI','roc_rocnum','roc_area','stcox_haz','stcox_stderr','stcox_z','stcox_pvalue','stcox_lowerCI','stcox_higherCI']
    output_name = os.path.splitext(os.path.basename(file))[0]

    # with open(file,'r') as f:
    #     line = f.readline()
    #     h = 0
    #     while line:
    #         if "{txt} 70{com}. {c )-}\n" == line:
    #             header = h
    #             break
    #         line = f.readline()
    #         h += 1
        
    longitudinal_df = pd.read_csv(file,header=None,names=longitudinal_header,skiprows=header,skipfooter=footer,engine='python')
    longitudinal_df = longitudinal_df.replace('.',np.nan)
    longitudinal_df = longitudinal_df.replace('inf',np.nan)
    longitudinal_df = longitudinal_df.replace('-inf',np.nan)
    longitudinal_df = longitudinal_df.astype({'cohort':str,
                                                'covariate':str,
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
    return longitudinal_df

def parse_features_and_parameters(df):
    df[['sleepstate', 'feature', 'analysis', 'parameters']] = df.Covariates.str.split("_",expand=True)
    df['m'] = df["parameters"].str.split("w",expand=True)[0]
    try:
        df['w'] = df["parameters"].str.split("w",expand=True)[1].str.split("r",expand=True)[0]
        df['r'] = df["parameters"].str.split("r",expand=True)[1]
    except:
        pass
    return df