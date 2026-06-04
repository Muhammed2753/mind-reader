# Football Characters - Serie A Players

A robust Python script for managing football player data with comprehensive error handling, logging, and validation.

## Features

- ✅ **Robust Error Handling**: Comprehensive exception handling for file operations and JSON processing
- ✅ **Data Validation**: Validates player data structure before adding to database
- ✅ **Logging**: Detailed logging with both file and console output
- ✅ **Backup System**: Automatic backup creation before modifying existing files
- ✅ **Type Hints**: Full type annotations for better code documentation
- ✅ **Statistics**: Built-in dataset statistics and analysis
- ✅ **Command Line Support**: Accepts custom file paths as arguments
- ✅ **Unit Tests**: Comprehensive test coverage

## Usage

### Basic Usage
```bash
python add_serie_a_players.py
```

### Custom File Path
```bash
python add_serie_a_players.py custom_characters.json
```

### Show Dataset Statistics
```python
from add_serie_a_players import print_dataset_info
print_dataset_info()
```

## File Structure

```
dream/
├── add_serie_a_players.py    # Main script
├── football_characters.json  # Player database (created automatically)
├── add_players.log          # Log file (created automatically)
├── requirements.txt         # Dependencies
├── test_add_serie_a_players.py  # Unit tests
└── README.md               # This file
```

## Configuration

The script includes a configuration section that can be modified:

```python
CONFIG = {
    \"default_characters_file\": \"football_characters.json\",
    \"backup_enabled\": True,
    \"log_file\": \"add_players.log\",
    \"log_level\": logging.INFO
}
```

## Player Data Structure

Each player entry follows this structure:

```json
{
  \"Player Name\": {
    \"answers\": {
      \"Is this person a football player?\": \"yes\",
      \"Is this player currently active?\": \"yes\",
      // ... more questions and answers
    },
    \"image_url\": \"https://example.com/player.png\"
  }
}
```

## Current Players

The script includes data for these Serie A players:
- **Rafael Leão** (AC Milan, Portugal)
- **Lautaro Martínez** (Inter Milan, Argentina)
- **Paulo Dybala** (Roma, Argentina)

## Error Handling

The script handles various error scenarios:
- Missing or corrupted JSON files
- Permission errors
- Disk space issues
- Invalid player data
- Network connectivity issues (for future API integration)

## Logging

Logs are written to both console and file (`add_players.log`) with timestamps and severity levels:
- INFO: Normal operations
- WARNING: Non-critical issues
- ERROR: Critical errors that prevent operation

## Testing

Run the unit tests:

```bash
python -m pytest test_add_serie_a_players.py -v
```

Or using unittest:

```bash
python test_add_serie_a_players.py
```

## Development

### Adding New Players

1. Add player data to the `SERIE_A_PLAYERS` dictionary
2. Ensure all required fields are present
3. Run the script to validate and add the data
4. Run tests to ensure data integrity

### Code Quality

The code follows these best practices:
- Type hints for all functions
- Comprehensive error handling
- Detailed logging
- Input validation
- Modular design
- Unit test coverage

## Future Enhancements

Potential improvements:
- Database integration (SQLite/PostgreSQL)
- API integration for real-time player data
- Web interface
- Player search and filtering
- Data export functionality
- Performance optimization for large datasets

## License

This project is for educational and personal use.