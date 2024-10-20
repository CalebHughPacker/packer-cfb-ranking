from Team import *

class Analysis:
    def __init__(self):
        pass
    
    def combine_rankings(self, off, defe, tal):
        off_names = {team.name for team in off}
        for team in defe:
            if team.name in off_names and any(team.name == t.name for t in tal):
                score = team.offensive_score + team.defensive_score + team.talent_score
                team.total_score = score
    def combine_rankings_with_sor(self, off, defe, tal, sor):
        off_names = {team.name for team in off}
        for team in defe:
            if team.name in off_names and any(team.name == t.name for t in tal) and any(team.name == s.name for s in sor):
                score = (team.offensive_score +
                        team.defensive_score +
                        team.talent_score +
                        team.sor)
                team.total_score = score
    def find_teams(self, target, teams):       
        for team in teams:
            if team.name == target:
                return team
        else:
            return None
        
    

    def calc_rankings_with_sor(self, teams):
        DIMIN_MULT = .9
        AUG_MULT = 1.1
        average = 0.0
        analysis = Analysis()
        for team in teams:
            average += team.total_score
        average/=len(teams)
        print("AVG", average)
        for team in teams:
            games_played = team.wins + team.losses
            sos = 0.0
            for opponent in team.teams_beaten_home:
                team.teams_beaten_home_obj.append(self.find_teams(opponent, teams))
            
            for opponent in team.teams_beaten_road:
                team.teams_beaten_road_obj.append(self.find_teams(opponent, teams))
            
            for opponent in team.teams_lost_home:
                team.teams_lost_home_obj.append(self.find_teams(opponent, teams))
            
            for opponent in team.teams_lost_road:
                team.teams_lost_road_obj.append(self.find_teams(opponent, teams))
            
            for item in team.teams_beaten_home_obj:
                if item != None:
                    sos += item.total_score*DIMIN_MULT/abs(average)
            for item in team.teams_beaten_road_obj:
                if item != None:
                    sos += item.total_score*AUG_MULT/abs(average)
            for item in team.teams_lost_home_obj:
                if item != None:
                    sos += item.total_score*AUG_MULT/abs(average)
            for item in team.teams_lost_road_obj:
                if item != None:
                    sos += item.total_score*DIMIN_MULT/abs(average)
                    
            sos /= games_played
            record = 0.0
            try:
                record = team.wins / (games_played)
            except ZeroDivisionError:
                pass
            if sos >= 0 or sos < 0  and record == 1:
                sor = sos*record
            else:
                val = 1-record
                sor = sos*val
            team.sor = sor


    def rank_teams(self, teams, average):
        for team in teams:
            for key, value in vars(team).items():
                if key != 'name' and key != 'offensive_score' and key != 'defensive_score' and key != 'talent_score' and key != 'wins' and key != 'losses':
                    self.get_score(average, team, key)
    # print(f"{team.name}: {team.talent}\nRecord: {team.wins} - {team.losses}\nTotal Yards: {team.total_yards}")
            team.calc_offensive_score(average)
            team.calc_defensive_score(average)
            team.calc_talent_score(average)
        ranked_offenses = sorted(teams, key=lambda team: team.offensive_score, reverse=True)
        ranked_defenses = sorted(teams, key=lambda team: team.defensive_score, reverse=True)
        ranked_talent = sorted(teams, key=lambda team: team.talent_score, reverse=True)
        self.combine_rankings(ranked_offenses, ranked_defenses, ranked_talent)
        ranked_totals = sorted(teams, key=lambda team: team.total_score, reverse=True)
        print("OVR")
        for i, team in enumerate(ranked_totals):
            print(f"{i+1}. {team.name}: {team.total_score:.2f}")
        self.calc_rankings_with_sor(teams)
        ranked_sor = sorted(teams, key=lambda team: team.sor, reverse=True)
        self.combine_rankings_with_sor(ranked_offenses, ranked_defenses, ranked_talent, ranked_sor)
        
        ranked_totals = sorted(teams, key=lambda team: team.total_score, reverse=True)
        
        print("Teams who are above average in each following statistic:")
        print("OFF")
        for i, team in enumerate(ranked_offenses):
            if team.offensive_score > 0:
                print(f"{i+1}. {team.name}: {team.offensive_score:.2f}")
        print("DEF")
        for i, team in enumerate(ranked_defenses):
            if team.defensive_score > 0:
                print(f"{i+1}. {team.name}: {team.defensive_score:.2f}")
        print("TAL")
        for i, team in enumerate(ranked_talent):
            if team.talent_score > 0:
                print(f"{i+1}. {team.name}: {team.talent_score:.2f}")
        print("SOR")
        for i, team in enumerate(ranked_sor):
            if team.sor > 0:
                print(f"{i+1}. {team.name}: {team.sor:.2f}")
        print("Overall Passing and Rushing Ratings of each FBS team")
        print("PASS")
        ranked_pass = sorted(teams, key=lambda team: team.passing_yards, reverse=True)
        for i, team in enumerate(ranked_pass):
            print(f"{i+1}. {team.name}: {team.passing_yards:.2f}")
        print("RUSH")
        ranked_rush = sorted(teams, key=lambda team: team.rushing_yards, reverse=True)
        for i, team in enumerate(ranked_rush):
            print(f"{i+1}. {team.name}: {team.rushing_yards:.2f}")
        print("OVR")
        print("Full overall ranking of each FBS team")
        for i, team in enumerate(ranked_totals):
            print(f"{i+1}. {team.name}: {team.total_score:.2f}")
    def find_average(self, teams):
        average = Team("Average")
        for team in teams:
            for key, value in vars(team).items():
                if key != 'name':  
                    setattr(average, key, getattr(average, key) + value)

        for key, value in vars(average).items():
            if key != 'name' and not isinstance(value, list):
                setattr(average, key, value / len(teams))
        return average
    
    def get_score(self, average, team, stat):
        
        team_stat = getattr(team, stat)
        average_stat = getattr(average, stat)
        if isinstance(team_stat, list) or isinstance(average_stat, list):
            return None
        else:
            score = team_stat - average_stat
            setattr(team, stat, score)
            return score