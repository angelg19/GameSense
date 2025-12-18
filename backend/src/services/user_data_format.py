from models.user import UserData

# Cleans user data to easily readible format to send to frontend
def cleanup_user_data(data: UserData):
    heroes = []
    if data.heroes_ranked:
      for hero in data.heroes_ranked:
        if (hero.main_attack.total <= 0 or hero.matches <= 0):
            continue
        heroObj = {}
        heroObj["name"] = hero.hero_name
        accuracy = round(hero.main_attack.hits / hero.main_attack.total, 3)
        heroObj["matchesPlayed"] = hero.matches
        heroObj["totalKills"] = hero.kills
        heroObj["totalDeaths"] = hero.deaths
        heroObj["totalAssists"] = hero.assists
        heroObj["accuracy"] = accuracy
        heroObj["mvp"] = hero.mvp
        heroObj["svp"] = hero.svp
        heroObj["wins"] = hero.wins
        heroObj["totalDamage"] = hero.damage
        heroObj["totalHealing"] = hero.heal
        heroObj["damageTaken"] = hero.damage_taken
        heroes.append(heroObj)
    
    maps = []
    if data.maps:
      for map in data.maps:
        maps.append(map.dict())

    url = data.player.icon if data.player.icon else ""

    sorted_heros = sorted(heroes, key=lambda x: x["matchesPlayed"], reverse=True)[:8]
    sorted_maps = sorted(maps, key=lambda x: x["matches"], reverse=True)
    cleaned_data = {
        "name": data.name,
        "rank": data.player.rank if data.player.rank else "Unranked",
        "icon": url,
        "level": data.player.level if data.player.rank else "0",
        "topHeroes": sorted_heros,
        "topMaps": sorted_maps,
        
    }
    return cleaned_data