import re
import os
import csv
from remove_event_date import remove_date_from_file

# Get the path of the chess-games directory
chess_games_dir = "chess-games"

# Loop over each file in the directory
for root, dirs, files in os.walk(chess_games_dir):
    for file in files:
        # Skip files that do not have the .pgn extension
        name, extension = os.path.splitext(file)
        if extension != ".pgn":
            continue

        file_path = os.path.join(root, file)
        remove_date_from_file(file_path)
        # Open the file and read its contents
        with open(file_path, "r", errors="ignore") as file:
            data = file.read()

            # Split the file into a list of games
            games = re.split(r"\[Event.*?\]", data)[1:]

            # Get the parent directory of the root directory
            parent_dir = os.path.dirname(root)
            parent_dir = os.path.dirname(root)

            # Create a CSV file for the games in this file
            csv_file_path = os.path.join(parent_dir, file.name + ".csv")

            with open(file.name + ".csv", "w") as csv_file:
                writer = csv.writer(csv_file)

                # Loop over each game
                for game in games:
                    # Extract the player names and Elo ratings
                    player1 = re.search(r"\[White \"(.*?)\"\]", game)
                    if player1:
                        player1 = player1.group(1)
                    else:
                        player1 = "N/A"
                    player2 = re.search(r"\[Black \"(.*?)\"\]", game)
                    if player2:
                        player2 = player2.group(1)
                    else:
                        player2 = "N/A"

                    white_elo_match = re.search(r"\[WhiteElo \"(.*?)\"\]", game)
                    if white_elo_match:
                        white_elo = white_elo_match.group(1)
                    else:
                        white_elo = "N/A"
                    black_elo = re.search(r"\[BlackElo \"(.*?)\"\]", game)
                    if black_elo:
                        black_elo = black_elo.group(1)
                    else:
                        black_elo = "N/A"

                    result = re.search(r"\[Result \"(.*?)\"\]", game)
                    if result:
                        result = result.group(1)
                    else:
                        result = "N/A"

                    # Parse the chess moves
                    moves = []
                    move_lines = re.findall(r"\d+\..*", game)
                    for line in move_lines:
                        line_moves = line.strip().split(".")
                        true_moves = []
                        for m in line_moves:
                            m = re.sub(r"\{.*?\}", "", m)
                            m = re.sub(r'(?<![\w-])\d+(?![\w-])', '', m).strip()
                            if len(m) > 0:
                                true_moves.append(m)

                        moves += true_moves

                    # Add a row to the CSV file with the player names, Elo ratings, and moves
<<<<<<< HEAD:auto_parser.py
                    writer.writerow([player1, white_elo, player2, black_elo, result] + [move for move in moves])
=======
                    writer.writerow([player1, white_elo, player2, black_elo, result] + [move for move in moves])
>>>>>>> 13c8e4ab4afd37d3dd51aea9427a903c1b4082cf:parser.py
