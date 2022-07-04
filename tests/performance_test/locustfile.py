from locust import HttpUser, task, between 
from server import loadClubs, loadCompetitions


clubs = loadClubs()
competitions = loadCompetitions()


class TestUser(HttpUser):
    wait_time = between(2,5)
    club = clubs[0]
    competition = competitions[1] 

    def on_start(self):
        self.client.post("/showSummary",{ 
            "email": self.club['email']
        } )
    @task
    def index(self):
        self.client.get('/')
    
    @task
    def booking(self):
        self.client.get(f'/book/{self.competition["name"]}/{self.club["name"]}')

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces",
        {
            "club" : self.club["name"],
            "competition" : self.competition['name'],
            'places' : 0
        })
    

    def on_stop(self):
        self.client.get('/logout')