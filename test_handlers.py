import pytest
from handlers import handle_rating_command

@pytest.mark.asyncio
async def test_handle_rating_command_real_player():
    """Test handling of real player results"""
    result = await handle_rating_command('tester', '#test', 'testserver', 'nemu')
    print(f"\nAPI Response for 'nemu':\n {result}")
    
    # Assert response contains expected sections
    assert "Top 5 Results for nemu" in result
    
    # Split the response into lines and check structure
    lines = result.split('\n')
    for line in lines[1:]:  # Skip the header line
        if line:  # Skip empty lines
            # Each line should contain name, character, and rating
            assert ':' in line, f"Line missing player name separator: {line}"
            assert '±' in line, f"Line missing rating deviation separator: {line}"

@pytest.mark.asyncio
async def test_handle_rating_command_not_found():
    """Test handling of non-existent player"""
    result = await handle_rating_command('tester', '#test', 'testserver', 'thisisnotarealplayername12345')
    print(f"\nAPI Response for non-existent player:\n {result}")
    assert "Error: Name not found" in result

@pytest.mark.asyncio
async def test_handle_rating_command_single_char():
    """Test handling of single character player"""
    result = await handle_rating_command('tester', '#test', 'testserver', 'nemasu')
    print(f"\nAPI Response for 'nemasu:\n' {result}")
    
    # Verify URL structure
    assert "https://puddle.farm/player/" in result
