from flask import current_app, jsonify
from postgrest.exceptions import APIError
from supabase import create_client, Client


SUPABASE_URL = current_app.config.get('SUPABASE_URL')
SUPABASE_API_KEY = current_app.config.get('SUPABASE_API_KEY')


def get_all_feedbacks():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
    try:
        response = (supabase.
                    table('Feedback').
                    select("*").
                    order('created_at', desc=False).
                    execute())
    except APIError as e:
        return [{'message:': {e.message}, 'code': {e.code}, 'details': {e.details}, "status": 500}]
    return response.data


def get_feedback_database():
    feedbacks = get_all_feedbacks()
    if len(feedbacks) > 0:
        if feedbacks[0].get('status'):
            # if an error occurred fetching feedbacks
            return feedbacks[0]
        # Transform into the same shape the frontend expects
        feedbackDatabase = {}
        for f in feedbacks:
            node_id = f.get('node_id')
            if feedbackDatabase.get(node_id):
                feedbackDatabase[node_id]["notes"].append(
                    {"timestamp": f.get("created_at"), "tag": f.get("tag"), "text": f.get("comment")})
            else:
                feedbackDatabase[node_id] = {
                    'classId': f.get("node_id"),
                    'className': f.get("class_name"),
                    'notes': [{
                        "timestamp": f.get("created_at"),
                        "tag": f.get("tag"),
                        "text": f.get("comment")
                    }]
                }
        return feedbackDatabase
    else:
        return {'message:': {e.message}, 'code': {e.code}, 'details': {e.details}, "status": 500}