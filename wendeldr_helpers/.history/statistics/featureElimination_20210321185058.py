import numpy as np
import pandas as pd


from round_robin_tournament import Tournament as rrT
from lifelines.fitters.coxph_fitter import CoxPHFitter
from lifelines.exceptions import ConvergenceWarning, ConvergenceError
from statsmodels.stats.outliers_influence import variance_inflation_factor 
from patsy import dmatrices

from wendeldr_helpers.statistics.general import recombitulate_covariates
from wendeldr_helpers.statistics.outliers import tukey_outlier


import warnings


class Match_Results:
    def __init__(self, contenders, pthresh=0.05):
        self.winner = ''
        self.loser = ''
        self.istie = False
        self.a = ''
        self.a_hr = ''
        self.a_se = ''
        self.a_lower_ci = ''
        self.a_upper_ci = ''
        self.a_p = ''
        self.b = ''
        self.b_hr = ''
        self.b_se = ''
        self.b_lower_ci = ''
        self.b_upper_ci = ''
        self.b_p = ''

        if isinstance(contenders, pd.DataFrame):
            if 'Covariates' in contenders.columns.values:
                if len(contenders)==2:
                    self.b = contenders.Covariates.iat[1]
                    self.b_hr = contenders['HR'].iat[1]
                    self.b_se = contenders['HR SE'].iat[1]
                    self.b_lower_ci = contenders['HR -95%CI'].iat[1]
                    self.b_upper_ci = contenders['HR +95%CI'].iat[1]
                    self.b_p = contenders['HR P'].iat[1]

                self.a = contenders.Covariates.iat[0]
                self.a_hr = contenders['HR'].iat[0]
                self.a_se = contenders['HR SE'].iat[0]
                self.a_lower_ci = contenders['HR -95%CI'].iat[0]
                self.a_upper_ci = contenders['HR +95%CI'].iat[0]
                self.a_p = contenders['HR P'].iat[0]

                if self.b != '':
                    self.winner = contenders.Covariates.iat[0] 
                    if self.b_p < pthresh:
                        self.loser = self.b
                        self.istie = True
                else:
                    self.winner = contenders.Covariates.iat[0]
            elif 'coef' in contenders.columns.values:
                if len(contenders) != 2:
                    raise(NotImplementedError)
                else:

                    if ((np.sign(contenders['coef'][0]) == 1) & (np.sign(contenders['coef'][1]) == -1)
                        or (np.sign(contenders['coef'][0]) == -1) & (np.sign(contenders['coef'][1]) == 1)):
                        winner = contenders.index[0]
                    else:
                        if sum(contenders['p'] < pthresh) == 2:
                            self.istie=True
                            winner = 'asdfawgfjo'
                        else:
                            winner = contenders.index[np.argmin(contenders['p'])]

                    self.winner = winner
                    # a
                    self.a = contenders.index[0]
                    self.a_hr = contenders['exp(coef)'].iat[0]
                    self.a_se = contenders['se(coef)'].iat[0]
                    self.a_lower_ci = contenders['exp(coef) lower 95%'].iat[0]
                    self.a_upper_ci = contenders['exp(coef) upper 95%'].iat[0]
                    self.a_p = contenders['p'].iat[0]
                    # b
                    self.b = contenders.index[1]
                    self.b_hr = contenders['exp(coef)'].iat[1]
                    self.b_se = contenders['se(coef)'].iat[1]
                    self.b_lower_ci = contenders['exp(coef) lower 95%'].iat[1]
                    self.b_upper_ci = contenders['exp(coef) upper 95%'].iat[1]
                    self.b_p = contenders['p'].iat[1]

    def printterm():
        from terminaltables import AsciiTable
        table_data = [
            ['Covariates', 'Haz. Ratio', 'Haz. Ratio', 'Haz. Ratio', 'Haz. Ratio', 'Haz. Ratio'],
            ['row1 column1', 'row1 column2'],
            ['row2 column1', 'row2 column2'],
            ['row3 column1', 'row3 column2']
        ]
        table = AsciiTable(table_data)
        print table.table



def getParticipents(lst):
    participents = []
    for x in lst:
        for lvl in x.log:
            pass

class RoundRobin:
    def __init__(self, df, univariate_participents):
        self.log = {}
        self.winner = ''
        univariate_participents = univariate_participents.sort_values(by='HR P',ascending=True).reset_index(drop=True)
        self.participents = univariate_participents.Covariates.to_list()
        self.contestant_n = len(self.participents)
        self.run(df, univariate_participents)

    def run(self, df, univariate_participents):
        if len(univariate_participents) > 0:
            # round robin expects top seed to be first so sort by p
            if len(univariate_participents) == 1:
                return {0: Match_Results(univariate_participents)}
            else:
                tournament = rrT(univariate_participents.Covariates.to_list())
                matches = tournament.get_active_matches()
                idx = 0
                while len(matches) > 0:
                    match = matches[0]
                    participants = match.get_participants()
                    uni = univariate_participents[univariate_participents.Covariates.isin([participants[0].get_competitor(), participants[1].get_competitor()])]
                    r = fight(df, uni, participants[0].get_competitor(), participants[1].get_competitor())

                    self.log[idx] = r
                    idx += 1
                    tournament.add_win(match, r.winner)
                    matches = tournament.get_active_matches()

                if idx > 1:
                    a=1
                w = tournament.get_winners()
                if type(w) == list:
                    self.winner = w[0]
                else:
                    self.winner = w
        # else:
#             r = fight(df, ss, a, current_round, self.univariate_participents[0], self.univariate_participents[0])
#             self.winner = r[-1]
#             self.log.append(r)

#         for r in result.log:
#             for i, (aaaaa, bbbbb) in enumerate(zip(round_track,r)):
#                 if i == 0:
#                     round_track[aaaaa].append(result.winner)
#                 else:
#                     round_track[aaaaa].append(bbbbb)

#         # return tournament.get_winners(), ret







def fight(df, univariate_results, independent1, independent2, vif_thresh=10) -> Match_Results:
    cph_model = CoxPHFitter()

    # calculate outliers for first var
    out = ~tukey_outlier(df[independent1], 10)

    # if multivariate analysis
    if independent1 != independent2:
        out1 = ~tukey_outlier(df[independent2], 10)
        tmp_df = df[[independent1,independent2,'event','time_event']][(out&out1)].dropna()


        # check if VIF >= threshold
        y, X = dmatrices('event ~' + f'{independent1}+{independent2}', tmp_df, return_type='dataframe')
        vif = pd.DataFrame()
        vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        vif["features"] = X.columns

        # if vif gt threshold return univariate of lowest p
        if vif.loc[0]['VIF Factor'] >=vif_thresh or vif.loc[1]['VIF Factor'] >=vif_thresh:
            return Match_Results(univariate_results)

        if tmp_df[independent1].std() == 0 or tmp_df[independent2].std() == 0:
            return Match_Results(univariate_results)

        cph_model.fit(df=tmp_df, duration_col='time_event', event_col='event')

        return Match_Results(cph_model.summary)
            # except ConvergenceError:
            # pass