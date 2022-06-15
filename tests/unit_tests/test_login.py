class TestLogin:

    def test_should_return_status_200(self, client, testing_data):
        user = testing_data["clubs"][0]["email"]
        response = client.post('/showSummary', data={"email": user})
        assert response.status_code == 200
    
    def test_should_return_no_mathching_email_message(self, client, testing_data):
        response = client.post('/showSummary', data={"email": "unknow@mail.com"})
        message = "Email does not match any accounts"
        print(response.data.decode())
        assert response.status_code == 200
        assert message in response.data.decode()
        
