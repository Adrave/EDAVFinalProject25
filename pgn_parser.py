import re
import os
import csv
# from remove_event_date import remove_date_from_file

# Get the path of the chess-games directory
chess_games_dir = "chess-games"
player_games_dir = "player-moves"

def extract_line(target, game):
    line = re.search(f'\\[{target} \\"(.*?)\\"\\]', game)
    if line:
        return line.group(1)
    else:
        return "N/A"

# Loop over each file in the directory
with open("player-moves/all_games.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    for dir in os.listdir(chess_games_dir):
        if not os.path.isdir(f"{chess_games_dir}/{dir}"):
            continue
        player_name = dir.replace('-', ' ').title()

        for page in os.listdir(f"{chess_games_dir}/{dir}"):
            # Skip files that do not have the .pgn extension
            name, extension = os.path.splitext(page)
            if extension != ".pgn":
                continue

            # remove_date_from_file(file_path)
            # Open the file and read its contents
            with open(f"{chess_games_dir}/{dir}/{page}") as file:
                data = file.read()

                # Split the file into a list of games
                games = re.split("\n\n\n\[", data)[1:]


                # Loop over each game
                for game in games:
                    # Extract the player names and Elo ratings
                    player1 = extract_line("White", game)
                    player2 = extract_line("Black", game)
                    white_elo = extract_line("WhiteElo", game)
                    black_elo = extract_line("BlackElo", game)
                    result = extract_line("Result", game)
                    if result == "*":
                        result = "1/2-1/2"
                        game = game.replace("*", "1/2-1/2")

                    # Parse the chess moves
                    # print(csv_file_path)
                    # print(player2)
                    # print(game)

                    whitespace_clockttime = re.compile(r"(\{\[%clk [0-9:]*\]\}|\s+)")
                    game_string = whitespace_clockttime.sub(' ', game).strip().split(']')[-1]

                    # print(game_string)
                    # print(result)
                    # print(re.search(f"1.*{result}", game_string))
                    move_string = re.search(f"1.*{result}", game_string)[0]
                    move_inds = re.findall("[0-9][0-9]?\.", move_string)
                    move_inds.append(result)
                    moves = []
                    for i in range(len(move_inds) - 1):
                        start_dex = move_string.index(move_inds[i]) + len(move_inds[i])
                        if move_string[start_dex] == ' ':
                            start_dex += 1
                        end_dex = move_string.index(move_inds[i + 1])
                        if move_string[end_dex - 1] == ' ':
                            end_dex -= 1
                        moves.append((move_inds[i][:-1], move_string[start_dex:end_dex]))


                    # Add a row to the CSV file with the player names, Elo ratings, and moves
                    for move in moves:
                        writer.writerow([player_name, white_elo, player2, black_elo, result, move[0], move[1]])
