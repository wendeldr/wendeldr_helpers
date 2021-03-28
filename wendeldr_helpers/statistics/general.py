from round_robin_tournament import Tournament as rrT
from lifelines import CoxPHFitter


def recombitulate_covariates(df):
    return list(df[['sleepstate', 'feature', 'analysis', 'parameters']].agg('_'.join, axis=1).values)
    

class Feature():
    def __init__(self, 
                name, 
                univariate_cohort_total,
                univariate_n_total,
                univariate_n_event,
                univariate_n_noevent,
                univariate_miss_n_event,
                univariate_miss_precent_n_event,
                univariate_miss_precent_n_noevent,
                univariate_events_precent_total,
                univariate_mean_event,
                univariate_mean_noevent,
                univariate_mean_abs_diff,
                univariate_ttest,
                univariate_or,
                univariate_or_positive_ci,
                univariate_or_negative_ci,
                univariate_or_standard_error,
                univariate_or_p,
                univariate_hr,
                univariate_hr_positive_ci,
                univariate_hr_negative_ci,
                univariate_hr_standard_error,
                univariate_hr_p,):
        self.name = name

        # uv == Univariate, or == odds ratio, hr == hazard ratio
        self.univariate_cohort_total = univariate_cohort_total
        self.univariate_n_total = univariate_n_total
        self.univariate_n_event = univariate_n_event
        self.univariate_n_noevent = univariate_n_noevent
        self.univariate_miss_n_event = univariate_miss_n_event
        self.univariate_miss_precent_n_event = univariate_miss_precent_n_event
        self.univariate_miss_precent_n_noevent = univariate_miss_precent_n_noevent
        self.univariate_events_precent_total = univariate_events_precent_total
        self.univariate_mean_event = univariate_mean_event
        self.univariate_mean_noevent = univariate_mean_noevent
        self.univariate_mean_abs_diff = univariate_mean_abs_diff
        self.univariate_ttest = univariate_ttest
        self.univariate_or = univariate_or
        self.univariate_or_positive_ci = univariate_or_positive_ci
        self.univariate_or_negative_ci = univariate_or_negative_ci
        self.univariate_or_standard_error = univariate_or_standard_error
        self.univariate_or_p = univariate_or_p
        self.univariate_hr = univariate_hr
        self.univariate_hr_positive_ci = univariate_hr_positive_ci
        self.univariate_hr_negative_ci = univariate_hr_negative_ci
        self.univariate_hr_standard_error = univariate_hr_standard_error
        self.univariate_hr_p = univariate_hr_p

