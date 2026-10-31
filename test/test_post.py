from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    # Extract only the Post dictionaries
    posts = [p["Post"] for p in res.json()]

    assert res.status_code == 200
    assert len(posts) == len(test_posts)

    for i in range(len(test_posts)-1):
        assert posts[i]["title"] == test_posts[i].title
        assert posts[i]["content"] == test_posts[i].content
        assert posts[i]["owner_id"] == test_posts[i].owner_id


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content



@pytest.mark.parametrize("title, content, rating", [
("awesome new title", "awesome new content", 2),
("favorite pizza", "i love pepperoni", 3),
("tallest skyscrapers", "wahoo", 4),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, rating):
    res = authorized_client.post("/posts/", json={"title": title, "content": content,
    "rating": rating})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
    "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401

def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
    "/posts/{test_posts[0].id)")
    assert res.status_code == 401

def test_delete_other_user_post(test_posts, test_user, authorized_client):
    res = authorized_client.delete(
        f"/posts/{test_posts[2].id}"
    )
    assert res.status_code == 403

def test_update_post(test_posts, test_user, authorized_client):
    data = {
        "title": "updataed title",
        "content": "updated content",
        "rating" : 3,
        "id": test_posts[0].id
    }
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json=data
    )
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]

