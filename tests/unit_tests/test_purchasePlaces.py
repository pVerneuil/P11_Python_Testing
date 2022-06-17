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
    
    def test_places_should_be_deducted_from_the_competition_when_redeemed(self, client, testing_data):
        """
        test issue#4 : club's should not be able to book more than 12 places per competitons
        """
        club = testing_data['clubs'][2] 
        competition = testing_data['competitions'][2]
        number_of_place_club_try_to_redeem = 12
        expected_values ={
            'number_of_place_in_competitions_updated' : int(competition['numberOfPlaces'])- number_of_place_club_try_to_redeem
        }
        response1 = client.post(
            '/purchasePlaces', data={
            'club' : club['name'] , 
            'competition': competition['name'],
            'places':number_of_place_club_try_to_redeem
            })
        
        assert response1.status_code == 200
        assert int(competition['numberOfPlaces']) == expected_values['number_of_place_in_competitions_updated']
        
    def test_club_should_be_able_to_book_12_or_less_place_per_competition(self,client,testing_data):
        """
        test issue#4 : club's should not be able to book more than 12 places per competitons
        """
        club = testing_data['clubs'][2] 
        competition = testing_data['competitions'][2]
        number_of_place_club_try_to_redeem = 12
        
        response1 = client.post(
            '/purchasePlaces', data={
            'club' : club['name'] , 
            'competition': competition['name'],
            'places':number_of_place_club_try_to_redeem
            })
        
        assert response1.status_code == 200

    def test_club_should_not_be_able_to_book_more_than_12_place_per_competition_at_once(self,client,testing_data):
        """
        test issue#4 : club's should not be able to book more than 12 places per competitons
        """
        club = testing_data['clubs'][4] 
        competition = testing_data['competitions'][0]
        number_of_place_club_try_to_redeem = 13
        
        response = client.post(
            '/purchasePlaces', data={
            'club' : club['name'] , 
            'competition': competition['name'],
            'places':number_of_place_club_try_to_redeem
            })
        message ='You can not book more than 12 places per competition' 
        
        assert response.status_code == 400
        assert message in response.data.decode('UTF-8')

    def test_club_should_not_be_able_to_book_more_than_12_place_per_competition_in_multiple_time(self,client,testing_data):
        """
        test issue#4 : club's should not be able to book more than 12 places per competitons
        """
        club = testing_data['clubs'][0] 
        competition = testing_data['competitions'][1]
        number_of_place_club_try_to_redeem = 6
        
        response1 = client.post(
            '/purchasePlaces', data={
            'club' : club['name'] , 
            'competition': competition['name'],
            'places':number_of_place_club_try_to_redeem
            })
        
        assert response1.status_code == 200
        
        club = testing_data['clubs'][0] 
        competition = testing_data['competitions'][1]
        number_of_place_club_try_to_redeem = 7
        
        response2 = client.post(
            '/purchasePlaces', data={
            'club' : club['name'] , 
            'competition': competition['name'],
            'places':number_of_place_club_try_to_redeem
            })
        message ='You can not book more than 12 places per competition' 
        
        assert response2.status_code == 400
        assert message in response2.data.decode('UTF-8')
