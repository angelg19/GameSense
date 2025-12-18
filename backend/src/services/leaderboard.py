import csv

def read_top_players():
    """
    Reads a csv file to gather the names of all the players in the top 1000 leaderboard and return them in a list.

    Returns:
        List (str): A string list with the player tags of top 1000 players.
    """

    top_players = []
    with open('../data/S5_leaderboard_wr.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            top_players.append(row['Name'])

    return top_players