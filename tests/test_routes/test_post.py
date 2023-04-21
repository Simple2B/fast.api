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


def test_create(
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
    )
    assert response and response.status_code == 200
    post = s.Post.parse_obj(response.json())
    assert post.title == TEST_TITLE
    assert post.content == TEST_CONTENT


def test_read(client: TestClient, db: Session, test_posts_ids: list[int]):
    for post_id in test_posts_ids:
        response = client.get(f"/posts/{post_id}")
        assert response and response.ok
        post = s.Post.parse_obj(response.json())
        assert post.id == post_id, "got wrong port"


def test_delete(
    client: TestClient,
    db: Session,
    test_posts_ids: list[int],
):
    # try delete non authorized
    response = client.delete(
        "/posts/1",
    )
    assert response and response.ok
    assert response.status_code == 204
    post_num_after = db.query(m.Post).count()
    assert post_num_after == (len(test_posts_ids) - 1)
