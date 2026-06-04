"""
Unit tests for add_serie_a_players module.
Run with: python -m pytest test_add_serie_a_players.py
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dream.add_serie_a_players import (
    validate_player_data,
    load_existing_characters,
    save_characters,
    get_player_stats,
    SERIE_A_PLAYERS
)


class TestAddSerieAPlayers(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test_characters.json"
        
        self.valid_player_data = {
            "answers": {
                "Is this person a football player?": "yes",
                "Is this player currently active?": "yes"
            },
            "image_url": "https://example.com/player.png"
        }
        
        self.invalid_player_data = {
            "answers": {},  # Empty answers
            "image_url": ""  # Empty URL
        }
    
    def test_validate_player_data_valid(self):
        """Test validation with valid player data."""
        result = validate_player_data("Test Player", self.valid_player_data)
        self.assertTrue(result)
    
    def test_validate_player_data_invalid(self):
        """Test validation with invalid player data."""
        with patch('logging.error'):
            result = validate_player_data("Test Player", self.invalid_player_data)
            self.assertFalse(result)
    
    def test_validate_player_data_missing_fields(self):
        """Test validation with missing required fields."""
        incomplete_data = {"answers": {"test": "yes"}}  # Missing image_url
        