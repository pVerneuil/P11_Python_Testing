from P11_Python_Testing.server import POINTS_PER_PLACE

class TestIntegration:
    
    def test_purchace_place(self,client, testing_data):
        """
        test of the purchase of places by a club
        """
        club = testing_data["clubs"][4]
        competition = testing_data["competitions"][0]
        
        response_login = client.post(
            "/showSummary",
            data ={
                "email": club['email']
            }
        )
        assert response_login.status_code == 200
        
        club_points_before_purchase = int(club['points'])
        competition_place_before_purchase = int(competition['numberOfPlaces'])
        number_of_place_purchase = 3
        response_purchase_place = client.post(
            "/purchasePlaces",
            data ={
                "club": club["name"],
                "competition": competition["name"],
                "places": number_of_place_purchase
            }
            )
        assert response_purchase_place.status_code == 200
        assert club['points'] == club_points_before_purchase - number_of_place_purchase*POINTS_PER_PLACE
        assert competition['numberOfPlaces'] == competition_place_before_purchase - number_of_place_purchase
        
        response_logout =  client.get('/logout')
        assert response_logout.status_code == 302