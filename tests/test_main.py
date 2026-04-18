import pytest
from chat_server import ChatServer

@pytest.fixture
def chat_server():
    return ChatServer()

def test_add_user(chat_server):
    user_id = 1
    username = "John"
    chat_server.add_user(user_id, username)
    assert chat_server.get_user(user_id) == username

def test_remove_user(chat_server):
    user_id = 1
    username = "John"
    chat_server.add_user(user_id, username)
    chat_server.remove_user(user_id)
    assert chat_server.get_user(user_id) is None

def test_send_message(chat_server):
    user_id = 1
    username = "John"
    message = "Hello"
    chat_server.add_user(user_id, username)
    chat_server.send_message(user_id, message)
    assert chat_server.get_messages() == [(user_id, message)]

def test_get_messages(chat_server):
    user_id1 = 1
    username1 = "John"
    message1 = "Hello"
    user_id2 = 2
    username2 = "Jane"
    message2 = "Hi"
    chat_server.add_user(user_id1, username1)
    chat_server.add_user(user_id2, username2)
    chat_server.send_message(user_id1, message1)
    chat_server.send_message(user_id2, message2)
    assert chat_server.get_messages() == [(user_id1, message1), (user_id2, message2)]

def test_get_user_messages(chat_server):
    user_id1 = 1
    username1 = "John"
    message1 = "Hello"
    user_id2 = 2
    username2 = "Jane"
    message2 = "Hi"
    chat_server.add_user(user_id1, username1)
    chat_server.add_user(user_id2, username2)
    chat_server.send_message(user_id1, message1)
    chat_server.send_message(user_id2, message2)
    assert chat_server.get_user_messages(user_id1) == [(user_id1, message1)]
