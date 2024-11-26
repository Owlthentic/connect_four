from game_logic import GameLogic
from game_state import GameState
from drop_state import DropState
from flask import Flask, request, jsonify
from flasgger import Swagger


if __name__ == "__main__":
    game = GameLogic()
    app = Flask(__name__)
    swagger = Swagger(app)

    @app.route('/api/board', methods=['GET'])
    def get_board():
        """
        Get the current state of the game board.
        ---
        tags:
           - Getting information about the current game 
        description: |
            The response is a dictionary with a single entry:
            - `board`: A 6x7 grid (as a list of lists) representing the game board.

            **Response Details**: 
            The response contains:
            - a dictionary which contains a single key-value pair whose key is `board`.
            - The value represents the current state of the game board. It is a
              list containing 6 lists, each of which contain 7 strings. Each
              string represents a game token:
                - `'X'`: Player token for red.
                - `'0'`: Player token for yellow.
                - `' '`: An empty cell.

            *Example*:
            ```json
            {
                "board": [
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ','0',' ',' '],
                    [' ',' ',' ','0','X',' ',' '],
                    [' ','X','0','X','X','0',' ']
                ]
            }
            ```
        responses:
            200:
                description: The current game board
                schema:
                    type: object
                    properties:
                        board:
                            type: array
                            description: The game board, represented as a list of 6 rows.
                            items:
                                type: array
                                description: A row of the game board, represented as 7 game tokens.
                                items:
                                    type: string
                                    description: A token in the game, represented by one of 'X', 'O', ' '
        """
        # working implementation for GET /api/board
        # get the board from the local GameLogic object
        board = game.get_board()
        # return board to the caller via JSON response
        return jsonify( {"board": board} ), 200 # status code: 200 Ok

    @app.route('/api/state', methods=['GET'])
    def get_state():
        """
        Retrieve the current state of the game.
        ---
        tags:
           - Getting information about the current game 
        description: |
            The response is a dictionary with a single entry:
            - `state`: An integer number indicating the current state of the game. Possible values are:
                - `0` (TURN_RED):    It's Red's turn to play.
                - `1` (TURN_YELLOW): It's Yellow's turn to play.
                - `2` (WON_RED):     Red has won the game.
                - `3` (WON_YELLOW):  Yellow has won the game.
                - `4` (DRAW):        The game ends in a draw.

            *Example*:
            ```json
            { "state": 1 }
            ```
        responses:
            200:
                description: The current game state
                schema:
                    type: object
                    properties:
                        state:
                            type: integer
                            description: The current state of the game, represented as integer number [0..4]
                            example: 1
        """
        # IMPLEMENT GET /api/state HERE
        return jsonify({"game_state": "not implemented!"}), 501 # status code: 501: Not implemented

    @app.route('/api/drop', methods=['POST'])
    def drop_token():
        """
        A player makes their move by dropping their token into the specified column.
        ---
        tags:
           - A player making their move
        description: |
            **Request Details**:
            The request body contains a dictionary containing the player's move details.

            *Example*:
            ```json
            { "column": 3, "player_id": "X" }
            ```
            **Response Details**: 
            The response is a dictionary with a single entry:
            - `drop_state`: An integer number indicating the state of drop. Possible values are:
                - `0` (DROP_OK):        Token dropped successfully
                - `1` (COLUMN_INVALID): The selected column is invalid
                - `2` (COLUMN_FULL):    The selected column is already full
                - `3` (WRONG_PLAYER):   A player made a move that is not theirs
            
            *Example*:
            ```json
            { "drop_state": 1 }
            ```
        parameters:
            - in: body
              name: body
              required: true
              description: The dictionary containing the player's move details.
              schema:
                type: object
                properties:
                    player_id:
                        type: string
                        description: The token of the player making the move, either 'X' or '0'.
                        example: 'X'
                    column:
                        type: integer
                        description: The column in which to drop the token (0-indexed).
                        example: 3
        responses:
            200:
                description: The current game state
                schema:
                    type: object
                    properties:
                        drop_state:
                            type: integer
                            description: A status code describing the result of the drop [0..3]
                            example: 1
            400:
                description: Fields 'player_id' and/or 'column' missing in request body.
                schema:
                    type: object
                    properties:
                        Error:
                            type: string
                            description: Textual desription of the error.
                            example: Fields 'player_id' and/or 'column' missing in request body.
        """
        # IMPLEMENT POST /api/drop HERE!
        return jsonify({"drop_state": "not implemented!"}), 501
    
    
    # starting the server on all interfaces
    print("Game server start")
    app.run(host="0.0.0.0", debug=True)
    print("Game server exit")
