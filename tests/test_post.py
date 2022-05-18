import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import model, schema


TEST_USERNAME = "tester1"
TEST_EMAIL = "t@t.bu"
TEST_PASS = "password"
TEST_POST_NUM = 3


@pytest.fixture
def test_token(db: Session, client: TestClient):
    # add test user
    test_user = model.User(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASS)
    db.add(test_user)
    db.commit()
    # login and get token
    response = client.post(
        "/login", data=dict(username=TEST_USERNAME, password=TEST_PASS)
    )
    assert response and response.ok, "unexpected response"
    yield schema.Token.parse_obj(response.json())


def test_create(client: TestClient, db: Session, test_token: schema.Token):
    for i in range(TEST_POST_NUM):
        TEST_TITLE = f"Post {i}"
        TEST_CONTENT = """
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Ipsum dignissimos
        id sint deleniti sequi tempore doloribus sapiente molestias perspiciatis exercitationem?
        """

        post = schema.PostCreate(
            title=TEST_TITLE,
            content=TEST_CONTENT,
        )

        headers = {"Authorization": f"Bearer {test_token.access_token}"}

        # create new post
        response = client.post("/posts/", headers=headers, json=post.dict())
        assert response and response.ok
        response.status_code == 201
        post = schema.Post.parse_obj(response.json())
        assert post.title == TEST_TITLE
        assert post.content == TEST_CONTENT


@pytest.fixture
def test_posts_ids(db: Session):
    # returner value - list of post id
    ids = []
    for i in range(TEST_POST_NUM):
        TEST_TITLE = f"Post {i}"
        TEST_CONTENT = """
        Lorem ipsum dolor sit, amet consectetur adipisicing elit.
        Ipsum dignissimos id sint deleniti sequi tempore doloribus
        sapiente molestias perspiciatis exercitationem?
        """
        post = model.Post(title=TEST_TITLE, content=TEST_CONTENT, user_id=1)
        db.add(post)
        db.commit()
        db.refresh(post)
        ids += [post.id]
    yield ids


def test_read(client: TestClient, db: Session, test_posts_ids: list[int], test_token):
    for post_id in test_posts_ids:
        response = client.get(f"/posts/{post_id}")
        assert response and response.ok
        post = schema.Post.parse_obj(response.json())
        assert post.id == post_id, "got wrong port"


def test_delete_wo_auth(client: TestClient, db: Session, test_posts_ids: list[int]):
    # delete first post
    POST_ID = test_posts_ids[0]
    # try delete non authorized
    response = client.delete(f"/posts/{POST_ID}")
    assert not response.ok
    assert response.status_code == 401


def test_delete(
    client: TestClient,
    db: Session,
    test_posts_ids: list[int],
    test_token: schema.Token,
):
    # delete first post
    POST_ID = test_posts_ids[0]
    # try delete non authorized
    response = client.delete(
        f"/posts/{POST_ID}",
        headers={"Authorization": f"Bearer {test_token.access_token}"},
    )
    assert response and response.ok
    assert response.status_code == 204
    post_num_after = db.query(model.Post).count()
    assert post_num_after == (len(test_posts_ids) - 1)
