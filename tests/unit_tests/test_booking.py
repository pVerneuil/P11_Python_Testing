from flask import url_for, request

class TestBooking:
    """
    test issue #5 :Booking places in past competitions
    """
    def test_should_not_access_booking_page_for_past_competitions(self, client, testing_data):
        club =  testing_data['clubs'][0]
        competition = testing_data['competitions'][4] #this competition is in the past (1900)
        response = client.get(
            f'/book/{competition["name"]}/{club["name"]}'
        )
        expected_message = 'This competition already took place. '
        assert response.status_code == 400
        assert expected_message in response.data.decode('UTF-8')

    def test_should_be_able_to_access_booking_page_for_futur_competitions(self, client, testing_data):
        club =  testing_data['clubs'][0]
        competition = testing_data['competitions'][3] #this competition is in the futur
        response = client.get(
            f'/book/{competition["name"]}/{club["name"]}'
        )
        assert response.status_code == 200