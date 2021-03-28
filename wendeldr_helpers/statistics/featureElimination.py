import numpy as np
import pandas as pd


from round_robin_tournament import Tournament as rrT
from lifelines.fitters.coxph_fitter import CoxPHFitter
from lifelines.exceptions import ConvergenceWarning, ConvergenceError
from statsmodels.stats.outliers_influence import variance_inflation_factor 
from patsy import dmatrices

from wendeldr_helpers.statistics.general import recombitulate_covariates
from wendeldr_helpers.statistics.outliers import tukey_outlier
from terminaltables import AsciiTable

import warnings

class Match_Results:
    def __init__(self, contenders, pthresh=0.05):
        self.grand_winner = ''
        self.winners = []
        self.n_event = []
        self.n = []

        self.istie = False

        self.participants = []
        self.haz_ratio = []
        self.standard_error = []
        self.lower_ci = []
        self.upper_ci = []
        self.p = []

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

                for index, row in contenders.iterrows():
                    self.participants.append(row['Covariates'])
                    self.haz_ratio.append(row['HR'])
                    self.standard_error.append(row['HR SE'])
                    self.lower_ci.append(row['HR -95%CI'])
                    self.upper_ci.append(row['HR +95%CI'])
                    self.p.append(row['HR P'])
                    self.n.append(row['N Total'])
                    self.n.append(row['N Event'])

                self.a = contenders.Covariates.iat[0]
                self.a_hr = contenders['HR'].iat[0]
                self.a_se = contenders['HR SE'].iat[0]
                self.a_lower_ci = contenders['HR -95%CI'].iat[0]
                self.a_upper_ci = contenders['HR +95%CI'].iat[0]
                self.a_p = contenders['HR P'].iat[0]
                self.n = contenders['N Total'].iat[0]
                self.n_event = contenders['N Event'].iat[0]

                if self.b != '':
                    if self.a_p < pthresh and self.b_p < pthresh:
                        if self.a_p <= self.b_p:
                            self.grand_winner = self.a
                        else:
                            self.grand_winner = self.b
                        self.winners.append(self.a)
                        self.winners.append(self.b)
                        self.istie = True
                    else:
                        if self.a_p <= self.b_p:
                            self.grand_winner = self.a
                        else:
                            self.grand_winner = self.b
                        self.winners.append(self.grand_winner)
                else:
                    self.grand_winner = self.a
                    self.winners.append(self.a)
        else:
            self.n = len(contenders.event_observed)
            self.n_event = sum(contenders.event_observed)
            contenders = contenders.summary
            if len(contenders) != 2:
                raise NotImplementedError
            else:

                if ((np.sign(contenders['coef'][0]) == 1) & (np.sign(contenders['coef'][1]) == -1)
                    or (np.sign(contenders['coef'][0]) == -1) & (np.sign(contenders['coef'][1]) == 1)):
                    self.grand_winner = contenders.index[np.argmin(contenders['p'])]
                    self.winners = [contenders.index[np.argmin(contenders['p'])]]
                else:
                    if sum(contenders['p'] < pthresh) == 2:
                        self.istie=True
                        self.grand_winner = contenders.index[np.argmin(contenders['p'])]
                        self.winners = contenders.index[contenders['p'] < pthresh].to_list()
                    else:
                        self.grand_winner = contenders.index[np.argmin(contenders['p'])]
                        self.winners = [contenders.index[np.argmin(contenders['p'])]]

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

    def table(self, header):
        header = ['Covariates', 'Haz. Ratio', 'Std. Err.', 'P>|z|', 'Lower 95% CI', 'Upper 95% CI']
        table_data=[]
        table_data.append(header)
        table_data.append([self.a, self.a_hr, self.a_se, self.a_p, self.a_upper_ci, self.a_lower_ci])
        if self.b != '':
            table_data.append([self.b, self.b_hr, self.b_se, self.b_p, self.b_upper_ci, self.b_lower_ci])
        t = AsciiTable(table_data)
        return t.table

    def printTable(self):
        print(table())

def getParticipents(lst):
    participents = []
    for x in lst:
        for lvl in x.log:
            pass

class Battle:
    def __init__(self, df, univariate_participents, lbl=''):
        self.label = lbl
        self.log = {}
        self.grand_winner = ''
        self.winners = []
        self.istie = False
        self.win_counts = {}
        univariate_participents = univariate_participents.sort_values(by='HR P',ascending=True).reset_index(drop=True)
        self.participents = univariate_participents.Covariates.to_list()
        self.contestant_n = len(self.participents)
        self.run(df, univariate_participents)
        self.table=self.generate_table()

        m = -1
        for k,v in self.win_counts.items():
            m = max(v, m)

        cnt = 0
        for k,v in self.win_counts.items():
            if m == v:
                cnt+=1
                self.winners.append(k)

        # if len(self.participents) >= 2:
        #     a=1
        if cnt > 1:
            self.istie = True

    def generate_table(self):
        # for x in self.log:
        header = ['Covariates', 'Haz. Ratio', 'Std. Err.', 'P>|z|', 'Lower 95% CI', 'Upper 95% CI']
        table_data=[]
        table_data.append(header)
        # for rnd in
        table_data.append([x.a, x.a_hr, x.a_se, self.a_p, self.a_upper_ci, self.a_lower_ci])
        if self.b != '':
            table_data.append([self.b, self.b_hr, self.b_se, self.b_p, self.b_upper_ci, self.b_lower_ci])
        table = AsciiTable(table_data)
        print(table.table)

    def run(self, df, univariate_participents):
        if len(univariate_participents) > 0:
            # round robin expects top seed to be first so sort by p
            if len(univariate_participents) == 1:
                self.log[0] = Match_Results(univariate_participents)
                self.grand_winner = self.log[0].grand_winner
                self.win_counts = {self.grand_winner: 1}
            else:
                tournament = rrT(univariate_participents.Covariates.to_list())
                matches = tournament.get_active_matches()
                idx = 0
                finished = {}
                while len(matches) > 0 and len(finished) < len(matches):
                    match = matches[0]
                    participants = match.get_participants()
                    if (participants[0].get_competitor(),participants[1].get_competitor()) not in finished:
                        finished[(participants[0].get_competitor(),participants[1].get_competitor())] = 0
                    else:
                        matches.pop(0)
                        continue
                    uni = univariate_participents[univariate_participents.Covariates.isin([participants[0].get_competitor(), participants[1].get_competitor()])]
                    r = fight(df, uni, participants[0].get_competitor(), participants[1].get_competitor())

                    self.log[idx] = r
                    idx += 1
                    if r.istie:
                        tournament.add_win(match, r.a)
                        tournament.add_win(match, r.b)
                    else:
                        tournament.add_win(match, r.grand_winner)
                    matches = tournament.get_active_matches()

                w = tournament.get_winners()
                if type(w) == list:
                    self.grand_winner = w[0]
                    self.win_counts = tournament._Tournament__wins
                else:
                    self.grand_winner = w
                    self.win_counts = tournament._Tournament__wins



def fight(df, univariate_results, independent1, independent2, vif_thresh=10, turkey_thresh=5) -> Match_Results:
    warnings.simplefilter('ignore', RuntimeWarning)
    cph_model = CoxPHFitter()

    # calculate outliers for first var
    out = ~tukey_outlier(df[independent1], turkey_thresh)

    # if multivariate analysis
    if independent1 != independent2:
        out1 = ~tukey_outlier(df[independent2], turkey_thresh)
        tmp_df = df[[independent1,independent2,'event','time_event']][(out&out1)].dropna()

        if len(tmp_df) <= 1:
            return Match_Results(univariate_results)
        
        # check if VIF >= threshold
        y, X = dmatrices('event ~' + f'{independent1}+{independent2}', tmp_df, return_type='dataframe')
        vif = pd.DataFrame()
        vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        vif["features"] = X.columns

        # if vif gt threshold return univariate of lowest p
        if vif.loc[1]['VIF Factor'] >= vif_thresh or vif.loc[2]['VIF Factor'] >=vif_thresh:
            return Match_Results(univariate_results)

        if tmp_df[independent1].std() == 0 or tmp_df[independent2].std() == 0:
            return Match_Results(univariate_results)

        try:
            cph_model.fit(df=tmp_df, duration_col='time_event', event_col='event')
        except ConvergenceError:
            return Match_Results(univariate_results)

        return Match_Results(cph_model)
