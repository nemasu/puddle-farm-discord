import aiohttp
import logging

logger = logging.getLogger('discord_bot')

async def handle_rating_command(user, channel, server, name):
    """Handle the rating command logic"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://puddle.farm/api/player/search?exact=true&search_string={name}') as response:
                if response.status != 200:
                    logger.error(f"/rating {name} | User: {user} | Server: {server} | Channel: {channel} | Status: Error - Site down")
                    return "Error: Site appears to be down"

                body = await response.json()
                
                if 'results' in body and body['results']:
                    results = body['results']
                    unique_players = {result['id'] for result in results}
                    
                    if len(unique_players) == 1:
                        return await handle_single_player(results, name, user, server, channel)
                    else:
                        return await handle_multiple_players(results, name, user, server, channel)
                else:
                    logger.warning(f"/rating {name} | User: {user} | Server: {server} | Channel: {channel} | Status: Error - Name not found")
                    return f"{name}: Error: Name not found."

    except Exception as e:
        logger.error(f"/rating {name} | User: {user} | Server: {server} | Channel: {channel} | Status: Error - {str(e)}")
        return f"{name}: Error: Try again."

async def handle_single_player(results, name, user, server, channel):
    """Handle single player results"""
    player_id = next(iter({result['id'] for result in results}))
    urls = []

    for result in results:
          url = f"https://puddle.farm/player/{player_id}/{result['char_short']}"
          urls.append(url)

    logger.info(f"/rating {name} | User: {user} | Server: {server} | Channel: {channel} | Status: Success - Single player")
    highest_rating = max(results, key=lambda x: x['rating'])
    url = f"https://puddle.farm/player/{player_id}/{highest_rating['char_short']}"
    return url

async def handle_multiple_players(results, name, user, server, channel):
    """Handle multiple player results"""
    player_best = {}
    for result in results:
        player_id = result['id']
        effective_rating = result['rating']
        
        if (player_id not in player_best or 
            effective_rating > player_best[player_id]['rating']):
            player_best[player_id] = result
    
    sorted_results = sorted(
        player_best.values(), 
        key=lambda x: x['rating'],
        reverse=True
    )[:5]

    urls = []
    for result in sorted_results:
        player_id = result['id']
        rating_str = f"{round(result['rating'])}"
        url = f"{result['name']}: {result['char_short']} {rating_str}"
        urls.append(url)
        # player_id = result['id']
        # url = f"https://puddle.farm/player/{player_id}/{result['char_short']}"
        # urls.append(url)
    
    logger.info(f"/rating {name} | User: {user} | Server: {server} | Channel: {channel} | Status: Success - Top 5 unique players")
    return 'Top 5 Results for ' + name + ':\n' + '\n'.join(urls)