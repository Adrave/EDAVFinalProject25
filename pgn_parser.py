import re
import os
import csv
# from remove_event_date import remove_date_from_file

# Get the path of the chess-games directory
chess_games_dir = "chess-games"
player_games_dir = "player-moves"

CHAMPS = ['magnus-carlsen', 'viswanathan-anand', 'vladimir-kramnik', 'garry-kasparov', 'anatoly-karpov', 'bobby-fischer',
          'boris-spassky', 'tigran-petrosian', 'mikhail-tal', 'vasily-smyslov', 'mikhail-botvinnik', 'max-euwe',
          'alexander-alekhine', 'jose-raul-capablanca', 'emanuel-lasker', 'wilhelm-steinitz']

MASTERS = ['magnus-carlsen', 'ding-liren', 'ian-nepomniachtchi', 'alireza-firouzja', 'hikaru-nakamura', 'fabiano-caruana',
           'anish-giri', 'wesley-so', 'viswanathan-anand', 'sergey-karjakin', 'teimour-radjabov', 'alexander-grischuk',
           'leinier-dominguez-perez', 'shakhriyar-mamedyarov', 'richard-rapport', 'maxime-vachier-lagrave']

def extract_line(target, game):
    line = re.search(f'\\[{target} \\"(.*?)\\"\\]', game)
    if line:
        return line.group(1)
    else:
        return "N/A"

# Loop over each file in the directory
if not os.path.isdir(player_games_dir):
    os.makedirs(player_games_dir)
with open(f"{player_games_dir}/all-games.csv", 'w') as csv_file:
    all_writer = csv.writer(csv_file)
    all_game_num = 1
    for dir in os.listdir(chess_games_dir):
        if not os.path.isdir(f"{chess_games_dir}/{dir}"):
            continue
        with open(f"{player_games_dir}/{dir}.csv", 'w') as csv_file:
            player_game_num = 1
            player_writer = csv.writer(csv_file)
            player_name = dir.replace('-', ' ').title()
            if dir in CHAMPS and dir in MASTERS:
                player_status = "Both"
            elif dir in CHAMPS:
                player_status = "World Champion"
            elif dir in MASTERS:
                player_status = "Grandmaster"
            else:
                exit(dir)

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
                        if white_elo == "N/A" or white_elo == "0":
                            white_elo = "?"
                        if black_elo == "N/A" or black_elo == "0":
                            black_elo = "?"

                        # Parse the chess moves
                        whitespace_clockttime = re.compile(r"(\{\[%clk [0-9:]*\]\}|\s+)")
                        game_string = whitespace_clockttime.sub(' ', game).strip().split(']')[-1]

                        move_string = re.search(f"1.*{result}", game_string)[0]
                        move_inds = re.findall("[0-9]+\.", move_string)
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

                        # if player1 == "Nakamura, Hikaru" and player2 == "Aronian, Levon" and black_elo == "2719":
                            # print(move_inds)
                            # exit()


                        # Add a row to the CSV file with the player names, Elo ratings, and moves
                        for move in moves:
                            player_writer.writerow([player_game_num,
                                                    player_name,
                                                    player_status,
                                                    white_elo,
                                                    player2,
                                                    black_elo,
                                                    result,
                                                    move[0],
                                                    move[1]])
                            all_writer.writerow([all_game_num,
                                                 player_name,
                                                 player_status,
                                                 white_elo,
                                                 player2,
                                                 black_elo,
                                                 result,
                                                 move[0],
                                                 move[1]])
                        all_game_num += 1
                        player_game_num += 1
