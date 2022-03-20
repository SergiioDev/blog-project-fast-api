def test_get_all_posts(authorized_client):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200


def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 200


def test_unauthorized_user_get_one_post(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/posts/22")
    assert res.status_code == 404
