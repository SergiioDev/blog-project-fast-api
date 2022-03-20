from app.schemas import PostResponse


def test_get_all_posts(authorized_client):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200


def test_get_one_post(authorized_client, test_post):
    response = authorized_client.get(f"/posts/{test_post[0].id}")
    post = PostResponse(**response.json())
    assert post.Post.id == test_post[0].id
    assert post.Post.title == test_post[0].title
    assert post.Post.content == test_post[0].content
    assert post.Post.published == test_post[0].published


def test_unauthorized_user_get_one_post(client, test_post):
    response = client.get(f"/posts/{test_post[0].id}")
    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_post):
    response = authorized_client.get(f"/posts/22")
    assert response.status_code == 404


