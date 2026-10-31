
def test_votes_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[0].id})
    assert res.status_code == 201

def test_delete_votes_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[2].id})
    assert res.status_code == 201

def test_votes_unorthorized_user(client, test_posts):
    res = client.post(
        "/vote/", json={"post_id": test_posts[2].id}
    )
    assert res.status_code == 401
    