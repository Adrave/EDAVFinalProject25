import re

def remove_date_from_file(file_name):
  # Open the PGN file for reading
  with open(file_name, 'r') as f:
    # Read the entire file as a single string
    pgn_text = f.read()

  # Use a regular expression to remove the `eventdate` field
  # from the file
  pgn_text = re.sub(r'\[EventDate\s".*?"\]\n', '', pgn_text)
  pgn_text = re.sub(r'\[Date\s".*?"\]\n', '', pgn_text)

  # Write the modified PGN text back to the file
  with open(file_name, 'w') as f:
    f.write(pgn_text)

remove_date_from_file("chess-games/alexander-alekhine/page-10.pgn")