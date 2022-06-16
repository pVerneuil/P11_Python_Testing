class TestPurshase:
    
    def test_should_return_error_message_when_club_try_to_redeem_more_points_than_available(self, client, testing_data ):
        """
        test issue#2 : club shouldn't be able to purchase more place than they have points 
        """
        club = testing_data['clubs'][3] #This club as no point
        competition = testing_data['competitions'][0]
        number_of_place_club_try_to_redeem = 1
        response = client.post(
            '/purchasePlaces', data={
            'club' : club['name'] , 
            'competition': competition['name'],
            'places':number_of_place_club_try_to_redeem
            })
        message = f"You do not have enough points to perfom this action ( you have {club['points']} point(s))"
        # print(response.data.decode())
        
        assert response.status_code == 400
        assert message in response.data.decode('UTF-8')
    

    def test_club_points_should_be_deducted_after_redeemed(self, client,testing_data):
        """
        test issue#2 : club's points should be updated after a purchase
        """
        club = testing_data['clubs'][4] 
        competition = testing_data['competitions'][0]
        number_of_place_club_try_to_redeem = 10
        
        expected_values ={
            'number_of_club_points_updated' : int(club['points'])- number_of_place_club_try_to_redeem
        }
        response = client.post(
            '/purchasePlaces', data={
            'club' : club['name'] , 
            'competition': competition['name'],
            'places':number_of_place_club_try_to_redeem
            })

        assert response.status_code == 200
        assert int(club['points']) == expected_values['number_of_club_points_updated']