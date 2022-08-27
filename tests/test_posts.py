import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    def validate_posts_and_votes(post):
        """function will receive a post that will be a dict and return an unpacked post"""
        return schemas.PostOut(**post)

    posts_mapping = map(validate_posts_and_votes, response.json())
    posts_lists = list(posts_mapping)
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    """make sure an unauthenticated user is not able to retrieve all posts"""
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    """test get individual post by non auth user"""
    response = client.get(f"/posts/{test_posts[0].posts_id}")
    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    """test to retrieve one post that does not exist, by auth user"""
    response = authorized_client.get(f"/posts/888888")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    """test to retrieve valid post"""
    response = authorized_client.get(f"/posts/{test_posts[0].posts_id}")
    post_out = schemas.PostOut(**response.json())
    assert post_out.post.posts_id == test_posts[0].posts_id
    assert post_out.post.posts_content == test_posts[0].posts_content
    assert post_out.post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, posts_content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("second awesome new title", "second awesome new content", False),
        ("third awesome new title", "third awesome new content", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, posts_content, published
):
    """test to create a post
    additional parameter test_posts sees DB if any post you are making was already created
    """
    response = authorized_client.post(
        "/posts/",
        json={"title": title, "posts_content": posts_content, "published": published},
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.posts_content == posts_content
    assert created_post.published == published
    assert created_post.owner_id == test_user["users_id"]


def test_creat_post_default_published_true(authorized_client, test_user, test_posts):
    """test to see default value for create post is published:True"""
    response = authorized_client.post(
        "/posts/",
        json={"title": "arbitrary title", "posts_content": "random content"},
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.posts_content == "random content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["users_id"]


def test_unauthorized_user_create_posts(client, test_user, test_posts):
    """test to make sure an unauthenticated user is not able to create posts"""
    response = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "random content"}
    )
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    """testing to make sure an unauthorized user cannot delete post"""
    response = client.delete(f"/posts/{test_posts[0].posts_id}")
    assert response.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    """test a valid deletion"""
    response = authorized_client.delete(f"/posts/{test_posts[0].posts_id}")
    assert response.status_code == 204


def test_delete_non_existent_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/9999999")
    assert response.status_code == 404


def test_delete_other_user_post(test_user, authorized_client, test_posts):
    """test where a user tries to delete a post that isn't theirs
    we need to have more than 1 user in the DB
    and we need to have posts owned by multiple users
    therefore we create another test_user2 function to create another user"""
    response = authorized_client.delete(f"/posts/{test_posts[3].posts_id}")
    assert response.status_code == 403


def test_update_post(test_user, authorized_client, test_posts):
    """test to update post"""
    data = {
        "title": "updated title",
        "posts_content": "updated content",
        "posts_id": test_posts[0].posts_id,
    }
    response = authorized_client.put(f"/posts/{test_posts[0].posts_id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.posts_content == data["posts_content"]


def test_update_other_user_post(test_user, authorized_client, test_posts):
    """test to update another user's post"""
    data = {
        "title": "updated title",
        "posts_content": "updated content",
        "posts_id": test_posts[3].posts_id,
    }
    response = authorized_client.put(f"/posts/{test_posts[3].posts_id}", json=data)
    assert response.status_code == 403

def test_unauthorized_user_update_post(client,test_user,test_posts):
    """test to check if unauthorized user is forbidden from updating posts"""
    response = client.put(f"/posts/{test_posts[0].posts_id}")
    assert response.status_code == 401