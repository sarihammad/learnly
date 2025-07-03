from unittest.mock import patch
from app.schemas import CurriculumRequest
from app.services.generator import generate_learning_path

MOCK_SUCCESS_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": """
                {
                    "Learning Path": {
                        "Introduction": {
                            "Courses": [
                                { "Course Name": "AI Basics", "Link": "http://example.com/ai" }
                            ]
                        },
                        "Core Topics": {
                            "Courses": [
                                { "Course Name": "ML in Finance", "Link": "http://example.com/ml-fin" }
                            ]
                        }
                    }
                }
                """
            }
        }
    ]
}

MOCK_INVALID_JSON_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": "This is not JSON. just plain text."
            }
        }
    ]
}


@patch("app.services.generator.openai.ChatCompletion.create")
def test_generate_learning_path_success(mock_openai):
    mock_openai.return_value = MOCK_SUCCESS_RESPONSE
    req = CurriculumRequest(goal="Learn AI for finance")
    result = generate_learning_path(req)
    assert "Learning Path" in result
    assert "Introduction" in result["Learning Path"]
    assert isinstance(result["Learning Path"]["Introduction"]["Courses"], list)


@patch("app.services.generator.openai.ChatCompletion.create")
def test_generate_learning_path_invalid_json(mock_openai):
    mock_openai.return_value = MOCK_INVALID_JSON_RESPONSE
    req = CurriculumRequest(goal="Learn AI for finance")
    result = generate_learning_path(req)
    assert "error" in result
    assert "Failed to parse" in result["error"]


@patch("app.services.generator.openai.ChatCompletion.create")
def test_generate_learning_path_with_known_skills(mock_openai):
    mock_openai.return_value = MOCK_SUCCESS_RESPONSE
    req = CurriculumRequest(goal="Learn AI for finance", known_skills="Python, statistics")
    result = generate_learning_path(req)
    assert "Learning Path" in result