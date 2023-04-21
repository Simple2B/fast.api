from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


import app.model as m
import app.schema as s
from tests.fixture import TestData

TEST_USERNAME = "tester1"
TEST_EMAIL = "t@t.bu"
TEST_PASS = "password"
TEST_TITLE = "TEST_TITLE"
TEST_CONTENT = "TEST_CONTENT"


def test_posts(
    client: TestClient,
    db: Session,
    test_data: TestData,
    authorized_users_tokens: list[s.Token],
):
    # create new post
    request_data = s.BasePost(
        title=TEST_TITLE,
        content=TEST_CONTENT,
    )
    response = client.post(
        "api/post/",
        json=request_data.dict(),
        headers={"Authorization": f"Bearer {authorized_users_tokens[0].access_token}"},
    )
    assert response and response.status_code == 201
    post = s.Post.parse_obj(response.json())
    assert post.title == TEST_TITLE
    assert post.content == TEST_CONTENT

    # read all posts
    response = client.get(
        "api/post/posts",
    )
    assert response and response.status_code == 200
    posts = s.PostList.parse_obj(response.json())
    assert len(posts.posts) > 0

    # read certain post by uuid
    response = client.get(
        f"api/post/{posts.posts[0].uuid}",
        headers={"Authorization": f"Bearer {authorized_users_tokens[0].access_token}"},
    )
    assert response and response.status_code == 200
    post = s.Post.parse_obj(response.json())
    assert post.title == TEST_TITLE

    # updating post
    request_data = s.BasePost(
        title=TEST_TITLE + "test",
        content=TEST_CONTENT + "test",
    )
    response = client.put(
        f"api/post/{posts.posts[0].uuid}",
        json=request_data.dict(),
        headers={"Authorization": f"Bearer {authorized_users_tokens[0].access_token}"},
    )
    assert response and response.status_code == 200
    post = s.Post.parse_obj(response.json())
    assert post.title != TEST_TITLE

    # deleting post
    response = client.delete(
        f"api/post/{posts.posts[0].uuid}",
        headers={"Authorization": f"Bearer {authorized_users_tokens[0].access_token}"},
    )
    assert response and response.status_code == 200
    assert not db.query(m.Post).filter_by(uuid=posts.posts[0].uuid).first()
