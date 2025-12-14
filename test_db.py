import database

# Test database
def test_database():
    database.init_db()
    games = database.get_games()
    print("Games in database:")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game[1]} - URL: {game[12]}")
    
    print(f"\nTotal games: {len(games)}")

if __name__ == "__main__":
    test_database()