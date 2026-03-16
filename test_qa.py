"""
Unit tests for Q&A database
"""
import pytest
from qa_database import search_qa, get_qa_database, get_random_questions

def test_qa_database_loaded():
    """Test that Q&A database loads correctly."""
    db = get_qa_database()
    assert db is not None
    assert len(db) > 0
    assert 'seguridad_edad' in db

def test_search_qa_by_question():
    """Test searching Q&A by question."""
    results = search_qa('50 años')
    assert len(results) > 0
    assert any('50' in result['question'] for result in results)

def test_search_qa_by_keyword():
    """Test searching Q&A by keyword."""
    results = search_qa('precio')
    assert len(results) > 0

def test_search_qa_no_results():
    """Test search with no results."""
    results = search_qa('xyzabc123nonsense')
    assert len(results) == 0

def test_qa_entry_structure():
    """Test that Q&A entries have required fields."""
    db = get_qa_database()
    for category, items in db.items():
        for item in items:
            assert 'question' in item
            assert 'answer' in item
            assert 'keywords' in item

def test_random_questions():
    """Test getting random questions."""
    questions = get_random_questions(5)
    assert len(questions) == 5
    assert all('question' in q for q in questions)

def test_random_questions_count():
    """Test random questions with custom count."""
    questions = get_random_questions(3)
    assert len(questions) == 3

def test_all_entries_have_answers():
    """Test that all Q&A entries have non-empty answers."""
    db = get_qa_database()
    for category, items in db.items():
        for item in items:
            assert item['answer'].strip() != ""
            assert len(item['answer']) > 10  # Reasonable answer length

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
