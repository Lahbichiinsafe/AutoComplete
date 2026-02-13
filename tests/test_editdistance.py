"""
Unit tests for Edit Distance autocomplete
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(src_dir, 'src'))

from autocomplete.editdistance_autocomplete import EditDistanceAutocomplete


def test_exact_match():
    """Test exact prefix match"""
    autocomplete = EditDistanceAutocomplete()
    autocomplete.load_glossary(["tomato", "tomatoes"])
    autocomplete.train_on_corpus("tomato tomato tomatoes plant")
    
    results = autocomplete.autocomplete("tom")
    words = [w for w, _ in results]
    
    assert "tomato" in words
    assert "tomatoes" in words
    print("Test exact match: PASSED")


def test_typo_correction():
    """Test typo correction"""
    autocomplete = EditDistanceAutocomplete()
    autocomplete.load_glossary(["tomato", "plant"])
    autocomplete.train_on_corpus("tomato plant water")
    
    # Typo: toamto -> tomato
    results = autocomplete.autocomplete("toamto")
    words = [w for w, _ in results]
    
    assert "tomato" in words
    print("Test typo correction: PASSED")


def test_glossary_priority():
    """Test that glossary terms are prioritized"""
    autocomplete = EditDistanceAutocomplete()
    autocomplete.load_glossary(["tomato"])
    autocomplete.train_on_corpus("total total total tomato")
    
    results = autocomplete.autocomplete("tom")
    words = [w for w, _ in results]
    
    # Glossary term should appear even if less frequent
    assert "tomato" in words
    print("Test glossary priority: PASSED")


def test_distance_limit():
    """Test that words with large edit distance are excluded"""
    autocomplete = EditDistanceAutocomplete()
    autocomplete.load_glossary(["tomato"])
    autocomplete.train_on_corpus("tomato elephant")
    
    results = autocomplete.autocomplete("tom")
    words = [w for w, _ in results]
    
    # "elephant" should not appear (too different)
    assert "elephant" not in words
    assert "tomato" in words
    print("Test distance limit: PASSED")


def test_empty_prefix():
    """Test with empty prefix"""
    autocomplete = EditDistanceAutocomplete()
    autocomplete.load_glossary(["tomato"])
    autocomplete.train_on_corpus("tomato plant")
    
    results = autocomplete.autocomplete("")
    
    assert len(results) == 0
    print("Test empty prefix: PASSED")


if __name__ == "__main__":
    test_exact_match()
    test_typo_correction()
    test_glossary_priority()
    test_distance_limit()
    test_empty_prefix()
    
    print("\nAll tests passed!")
