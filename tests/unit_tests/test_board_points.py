class TestBoardPoint:
    def test_should_access_board_points_page(self, client, testing_data):
        response = client.get(
            "/pointsBoard",
        )
        data = response.data.decode("utf-8")
        assert response.status_code == 200
        for club in testing_data["clubs"]:
            assert club["name"] in data
            assert club["points"] in data
