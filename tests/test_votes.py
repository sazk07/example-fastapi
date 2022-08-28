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
    assert response.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    """test to delete a post that does not exist"""
    response = authorized_client.post(
        "/vote/", json={"posts_id": test_posts[3].posts_id, "votes_dir": 0}
    )
    assert response.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):
    """voting on a post that does not exist"""
    response = authorized_client.post(
        "/vote/", json={"posts_id": 8888888888888888888888, "votes_dir": 1}
    )
    assert response.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    """check to see if user who isn't authenticated can't vote"""
    response = client.post(
        "/vote/", json={"posts_id": test_posts[3].posts_id, "votes_dir": 1}
    )
    assert response.status_code == 401
