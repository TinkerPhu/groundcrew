"""
Tests for ollama API.
"""

from unittest.mock import patch

import pytest
import ollama
import json

from groundcrew.llm import ollamaapi


@pytest.fixture
def ollama_chat_response():
    def _chat_output(content, role):
        return ollama._types.ChatResponse(
            created_at = '2025-02-18T17:23:52.475687808Z',
            message=ollama.Message(role=role, content=content)
        )

    return _chat_output


@pytest.fixture
def ollama_tool_response():
    def _chat_output(content, role, function_name, function_args):
        return ollama._types.chat.ChatCompletion(
            choices=[
                ollama._types.chat.chat_completion.Choice(
                    finish_reason='stop',
                    index=0,
                    logprobs=None,
                    message=ollama._types.chat.ChatCompletionMessage(
                        content=content,
                        role=role,
                        tool_calls=[
                            ollama._types.chat.chat_completion_message_tool_call.ChatCompletionMessageToolCall(
                                id='some_string',
                                function=ollama._types.chat.chat_completion_message_tool_call.Function(
                                    arguments=function_args,
                                    name=function_name
                                ),
                                type='function'
                            )
                        ]
                    )
                )
            ],
            created=1689623190,
            id="chatcmpl-xyz",
            model="gpt-3.5-turbo-0613-mock",
            system_fingerprint="fp_44709d6fcb",
            object="chat.completion",
            usage=ollama._types.CompletionUsage(
                completion_tokens=99,
                prompt_tokens=99,
                total_tokens=99
            )
        )

    return _chat_output

@pytest.fixture
def ollama_embedding_response():
    def _embedding_response(num_embeddings, embedding_dim):
        return ollama._types.CreateEmbeddingResponse(
            data=[
                ollama._types.Embedding(
                    embedding=[0.42]*embedding_dim,
                    index=i,
                    object='embedding'
                )
                for i in range(num_embeddings)
            ],
            model='fake_embedding_model',
            object='list',
            usage=ollama._types.create_embedding_response.Usage(
                prompt_tokens=99,
                total_tokens=99
            )
        )

    return _embedding_response


@patch('groundcrew.llm.ollamaapi.ollama.resources.embeddings.Embeddings.create')
def test_embeddings(embeddings_mock, ollama_embedding_response):
    """test embedding functions"""
    n_texts = 3
    embedding_dim = 10

    embeddings_mock.return_value = ollama_embedding_response(n_texts, embedding_dim)
    texts = ['baloney'] * n_texts

    client = ollamaapi.get_ollamaai_client('fake_api_key')
    embedding_func = ollamaapi.get_embedding_model('fake_model', client)
    results = embedding_func(texts)

    assert len(results)==len(texts)
    assert len(results[0])==embedding_dim
    assert isinstance(results[0][0], float)


def test_toolcall_to_dict():
    toolcall = ollamaapi.ToolCall(
        'tcid',
        'function',
        'func_name',
        {
            'arg1': 42,
            'arg2': 'forty two'
        }
    )
    toolcall_dict = ollamaapi.toolcall_to_dict(toolcall)
    assert toolcall_dict=={
        'id': 'tcid',
        'type': 'function',
        'function': {
            'name': 'func_name',
            'arguments': '{"arg1": 42, "arg2": "forty two"}'
        }
    }


def test_message_to_dict():
    message = ollamaapi.UserMessage('This is a test.')
    message_dict = ollamaapi.message_to_dict(message)
    assert message_dict['role']=='user'
    assert message_dict['content']=='This is a test.'

    message = ollamaapi.AssistantMessage('This is a test.', None)
    message_dict = ollamaapi.message_to_dict(message)
    assert message_dict['role']=='assistant'
    assert message_dict['content']=='This is a test.'
    assert 'tool_calls' not in message_dict

    message = ollamaapi.AssistantMessage(
        'This is a test.',
        [ollamaapi.ToolCall('tcid', 'function', 'func_name', {'arg1': 42})]
    )
    message_dict = ollamaapi.message_to_dict(message)
    assert message_dict['role']=='assistant'
    assert message_dict['content']=='This is a test.'
    assert message_dict['tool_calls']==[{
        'id': 'tcid',
        'type': 'function',
        'function': {
            'name': 'func_name',
            'arguments': '{"arg1": 42}'
        }
    }]


def test_dict_to_message():
    dict = {'role': 'user', 'content': 'This is a test.'}
    message = ollamaapi.UserMessage('This is a test.')
    assert ollamaapi.dict_to_message(dict)==message

    dict = {'role': 'assistant', 'content': 'This is a test.'}
    message = ollamaapi.AssistantMessage('This is a test.', None)
    assert ollamaapi.dict_to_message(dict)==message

    dict = {
        'role': 'assistant',
        'content': 'This is a test.',
        'tool_calls': [
            {
                'id': 'tcid',
                'type': 'function',
                'function': {'name': 'func_name', 'arguments': '{"arg1": 42}'}
            },
        ]
    }
    message = ollamaapi.AssistantMessage(
        'This is a test.',
        [ollamaapi.ToolCall('tcid', 'function', 'func_name', {'arg1': 42})]
    )
    assert ollamaapi.dict_to_message(dict)==message


@patch('groundcrew.llm.ollamaapi.ollama.Client.chat')
def test_chat_completion(chat_mock, ollama_chat_response, ollama_tool_response):
    target_output_content = 'Who is there?'
    target_output_role = 'assistant'
    chat_mock.return_value = ollama_chat_response(
        target_output_content,
        target_output_role
    )
    client = ollamaapi.get_ollamaai_client('fake_host')
    model = ollamaapi.start_chat('test_model', client)
    messages = [
        ollamaapi.SystemMessage('You are a helpful assistant.'),
        ollamaapi.UserMessage('Knock knock.')
    ]
    response = model(messages)
    assert response.content==target_output_content
    assert response.role==target_output_role


    target_output_function_name = 'test_func'
    target_output_function_args = '{"arg1": 42}'
    chat_mock.return_value = ollama_tool_response(
        target_output_content,
        target_output_role,
        target_output_function_name,
        target_output_function_args
    )
    model = ollamaapi.start_chat('test_model', client)
    messages = [
        ollamaapi.SystemMessage('You are a helpful assistant.'),
        ollamaapi.UserMessage('Knock knock.')
    ]
    response = model(messages)
    assert response==ollamaapi.AssistantMessage(
        target_output_content,
        [ollamaapi.ToolCall(
            'some_string',
            'function',
            target_output_function_name,
            json.loads(target_output_function_args))
        ]
    )
