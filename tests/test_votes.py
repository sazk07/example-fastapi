def test_vote_on_post(authorized_client, test_posts):
    """test if vote on post works"""
    response = authorized_client.post(
        "/vote/", json={"posts_id": test_posts[3].posts_id, "votes_dir": 1}
    )
    assert response.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"posts_id": test_posts[3].posts_id, "votes_dir": 1}
    )
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"posts_id": test_posts[3].posts_id, "votes_dir": 0}
    )
    print(response.json())
    assert response.status_code == 201
