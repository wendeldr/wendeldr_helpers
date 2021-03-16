from round_robin_tournament import Tournament as rrT
from lifelines import CoxPHFitter

class Feature():
    def __init__(self, name, univariate_ttest, univariate_hr, univariate_hrp):
        self.name = name
        self.univariate_ttest = univariate_ttest
        self.univariate_hr = univariate_hr
        self.univariate_hrp = univariate_hrp



class RoundRobin:
    def __init__(self, ss, a, round, participents):
        self.log = []
        if len(participents) > 0:
            if type(participents[0]) == Feature:
                tmp = []
                for x in participents:
                    tmp.append((x.name, x.univariate_hrp, x.univariate_ttest))

                tmp = sorted(tmp, key=lambda x: (x[1],x[2]))
                self.participents = []
                for x in tmp:
                    self.participents.append(x[0])
            else:
                self.participents = participents

        # print(self.participents)

        if len(self.participents) > 1:
            tournament  = rrT(self.participents)
            matches = tournament.get_active_matches()
            # for idx, i in enumerate(list(self.comb)): 
            while len(matches) > 0:
                match = matches[0]
                participants = match.get_participants()
                r = fight(ss, a, round, participants[0].get_competitor(), participants[1].get_competitor())
                self.log.append(r)
                tournament.add_win(match, r[-1])
                matches = tournament.get_active_matches()

            self.winner = tournament.get_winners()
        else:
            r = fight(ss, a, round, self.participents[0], self.participents[0])
            self.winner = r[-1]
            self.log.append(r)
        # return tournament.get_winners(), ret

def fight(ss,analysis,round,independent1,independent2):
    cph_model = CoxPHFitter()
    try:
        out = ~findOutilers(df[independent1], 5)
        out1 = ~findOutilers(df[independent2], 5)
        cph_model.fit(df=df[[independent1,independent2,'time_event','event']][(out&out1)].dropna(), duration_col='time_event', event_col='event')

        if ((np.sign(cph_model.summary['coef'][0]) == 1) & (np.sign(cph_model.summary['coef'][1]) == -1)) or (np.sign(cph_model.summary['coef'][0]) == -1) & (np.sign(cph_model.summary['coef'][1]) == 1):
            winner = cph_model.summary.index[0]
        else:
            winner = cph_model.summary.index[np.argmin(cph_model.summary['p'])]
        return ['', ss, analysis, round, cph_model.summary.index[0], cph_model.summary.index[1], cph_model.summary['exp(coef)'][0], cph_model.summary['exp(coef)'][1], cph_model.summary['p'][0], cph_model.summary['p'][1], winner]

    except:
        return ['', ss, analysis, round, '', '', '', '', '', '', independent1]