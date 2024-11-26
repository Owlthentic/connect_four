from flask import Flask, jsonify, request
from flasgger import Swagger


if __name__ == '__main__':
    app = Flask(__name__)
    swagger = Swagger(app)

    # persons-database (in-memory) with intially two users
    users = [{"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}]
    max_id = len(users)

    # GET: get all users
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """
        Get a list of all users.
        ---
        tags:
           - Information about users
        responses:
            200:
                description: A list of all users
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                example: 1
                            name:
                                type: string
                                example: John Doe
        """
        print( f"GET /api/users/" )
        return jsonify(users)


    # GET: get individual user by id
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """
        Get a user by their ID.
        **Note**: The `id` field is required and has to be passed as part of the URL.
        ---
        tags:
           - Information about users
        parameters:
            - name: user_id
              in: path
              required: true
              description: The ID of the user to retrieve
              type: integer
        responses:
            200:
                description: A single user
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The user Id
                            example: 1
                        name:
                            type: string
                            description: The user name
                            example: John Doe
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        Error:
                            type: string
                            description: Textual desription of the error.
                            example: User with id 123 not found
        """
        print( f"GET /api/users/{user_id}" )
        # user = None
        for user in users:
            if user["id"] == user_id:
                print( "returning user:", user )
                return jsonify(user), 200
        return jsonify({ "Error": f"User with id {user_id} not found" }), 404

    # POST: create new user
    @app.route('/api/users', methods=['POST'])
    def create_user():
        """
        Create a new user.
        **Notes**:
        - The `id` field is optional and will be replaced by the server if provided.
        - The `name` field is required.
        See ''Model'' under Parameters->body
        ---
        tags:
           - User Management
        parameters:
          - name: body
            in: body
            required: true
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        description: |
                            The user Id.
                            Specifying the Id is optional. If provided, the given Id will be ignored
                            an replaced by a server-generated Id.
                        example: 1
                    name:
                        type: string
                        description: The user name
                        example: John Doe
        responses:
            201:
                description: The user has been created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The server-generated user Id
                            example: 1
                        name:
                            type: string
                            description: The user name
                            example: John Doe
            400:
                description: The provided user is missing the required 'name' field.
                schema:
                    type: object
                    properties:
                        Error:
                            type: string
                            description: Textual desription of the error.
                            example: The provided user is missing the required 'name' field.
        """
        print( f"POST /api/users/" )
        new_user = request.json # this is the dictonary containing the new user to be created
        # check if required field "name" is provied
        if not "name" in new_user:
            return jsonify({ "Error": f"The provided user is missing the required 'name' field." }), 400 # "400 Bad request"

        # create a new unique id
        global max_id
        max_id += 1
        new_user["id"] = max_id
        users.append(new_user)
        return jsonify(new_user), 201 # "201 Created"

    # PUT: update user
    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        """
        Update an existing user by id.
        **Request URL**:
        - The `id` field is required and has to be passed as part of the URL.
        **Request Body**: The fields to be updated need to be contained in the request body. These are:
            - The `name` field is required (this is the only field of a user in this implementation :-)
        **Response Body**:
        - If successful, the entire user object is returned.

        ---
        tags:
           - User Management
        parameters:
            - name: user_id
              in: path
              required: true
              description: The ID of the user to update.
              type: integer
              example: 2
            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    name:
                        type: string
                        description: The user name
                        example: John Bob
        responses:
            200:
                description: The user has been updated
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The user Id
                            example: 2
                        name:
                            type: string
                            description: The user's new name
                            example: John Bob
            400:
                description: The provided user is missing the required 'name' field.
                schema:
                    type: object
                    properties:
                        Error:
                            type: string
                            description: Textual desription of the error.
                            example: The paramater is missing the required 'name' field.
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        Error:
                            type: string
                            description: Textual desription of the error.
                            example: User with id 123 not found
        """
        data = request.json # this is a dicionary including the fields (of the user) to be updated
        if not "name" in data:
            return jsonify({ "Error": f"The parameter is missing the required 'name' field." }), 400
        for user in users:
            if user["id"] == user_id:
                user["name"] = data["name"]                
                return jsonify(user), 200
        return jsonify({ "Error": f"User with id {user_id} not found" }), 404

    # DELETE: delete user by id
    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """
        Delete an existing user by id.
        ---
        tags:
           - User Management
        parameters:
          - name: user_id
            in: path
            required: true
            description: The id of the user to delete
            type: integer
        responses:
            204:
                description: User deleted
                schema:
                    type: object
                    properties:
                        Message:
                            type: string
                            description: Textual desription of the performed action.
                            example: User deleted
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        Error:
                            type: string
                            description: Textual desription of the error.
                            example: User with id 123 not found
        """
        print( f"DELETE /api/users/{user_id}" )
        global users # users is a list of dictionaries
        for user in users:
            if user["id"] == user_id:
                users.remove(user) # delete user from list of users
                return jsonify({"Message": "User deleted"}), 200
        return jsonify({ "Error": f"User with id {user_id} not found" }), 404

    print( "Starting REST user-db server" )
    app.run(host="0.0.0.0", debug=True)
