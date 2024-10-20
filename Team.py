from threading import Thread

class Team:
    def __init__ (self, name):
        self.name = name
        self.offensive_score = 0.0
        self.defensive_score = 0.0
        self.talent_score = 0.0
        self.sos_score = 0.0
        self.sor = 0.0
        self.total_score = 0.0
        self.adj_wins = 0.0
        self.adj_losses = 0.0

        #talent score
        self.talent = 0.0

        #w-l data
        self.wins = 0
        self.losses = 0
        self.home_wins = 0
        self.road_wins = 0
        self.home_losses = 0
        self.road_losses = 0
        self.teams_beaten_home = []
        self.teams_lost_home = []
        self.teams_beaten_road = []
        self.teams_lost_road = []
        self.teams_beaten_home_obj = []
        self.teams_lost_home_obj = []
        self.teams_beaten_road_obj = []
        self.teams_lost_road_obj = []

        #offensive data
        self.total_yards = 0
        self.passing_yards = 0
        self.rushing_yards = 0
        self.possession_time = 0
        self.turnovers = 0
        self.rushing_tds = 0
        self.passing_tds = 0
        
        #defensive data
        self.interceptions = 0
        self.fumbles_recovered = 0
        self.tackles_for_loss = 0
        self.overall_ppa = 0.0
        self.passing_ppa = 0.0
        self.rushing_ppa = 0.0
        self.success_rate = 0.0



    
    def calc_offensive_score(self, average):
        score = self.total_yards/average.total_yards + self.possession_time/average.possession_time - self.turnovers/average.turnovers + self.rushing_tds/average.rushing_tds + self.passing_tds/average.passing_tds
        # score -= abs(abs(self.passing_yards/average.passing_yards) - abs(self.rushing_yards/average.rushing_yards))
        self.offensive_score = score*10

    def calc_defensive_score(self, average):
        score = (self.interceptions/average.interceptions + self.fumbles_recovered/average.fumbles_recovered) + self.tackles_for_loss/average.tackles_for_loss - self.overall_ppa/average.overall_ppa - self.success_rate/average.success_rate
        score -= abs(abs(self.passing_ppa/average.passing_ppa) - abs(self.rushing_ppa/average.rushing_ppa))
        self.defensive_score = score*10

    def calc_talent_score(self, average):
        score = self.talent/average.talent
        self.talent_score = score*10
    

        
        