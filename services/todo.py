from flask import request, current_app, Response
from bson import json_util, ObjectId
from config.mongodb import mongo

def create_todo_service():
    data = request.get_json()
    title = data.get('title', None)
    description = data.get('description', None)
    
    if title:
        with current_app.app_context():
            response = mongo.db.todos.insert_one({
                'title': title,
                'description': description,
                'done': False
            })
            result = {
                'id': str(response.inserted_id),
                'title': title,
                'description': description,
                'done': False
            }
            return result
    else:
        return 'invalid payload', 400

def get_todos_service():
    with current_app.app_context():
        data = mongo.db.todos.find()
        result = json_util.dumps(data)
        return Response(result, mimetype='application/json')

def get_todo_service(id):
    with current_app.app_context():
        data = mongo.db.todos.find_one({'_id': ObjectId(id)})
        result = json_util.dumps(data)
        return Response(result, mimetype='application/json')

def update_todo_service(id):
    data = request.get_json()
    title = data.get('title', None)
    description = data.get('description', None)
    
    with current_app.app_context():
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
            
        result = mongo.db.todos.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data}
        )
        
        if result.matched_count > 0:
            return Response(
                json_util.dumps({'message': 'Todo updated successfully'}), 
                mimetype='application/json'
            )
        else:
            return Response(
                json_util.dumps({'message': 'todo not found'}), 
                status=404, 
                mimetype='application/json'
            )
def delete_todo_service(id):
    with current_app.app_context():
        result = mongo.db.todos.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count > 0:
            return Response(
                json_util.dumps({'message': 'Todo deleted successfully'}), 
                mimetype='application/json'
            )
        else:
            return Response(
                json_util.dumps({'message': 'todo not found'}), 
                status=404, 
                mimetype='application/json'
            )