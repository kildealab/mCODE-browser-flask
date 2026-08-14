from flask import jsonify, request, Blueprint, current_app
from datetime import datetime
from pathlib import Path
from postgrest.exceptions import APIError
from supabase import create_client, Client


api = Blueprint(
    'api', __name__,
    url_prefix='/api',
)
SUPABASE_URL = current_app.config.get('SUPABASE_URL')
SUPABASE_API_KEY = current_app.config.get('SUPABASE_API_KEY')

# Health check
@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200



@api.route('/feedback', methods=['GET', 'POST'])
def feedback():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
    # GET /api/feedback  → all feedback (same shape as original frontend feedbackDatabase)
    if request.method == 'GET':
        try:
            response = (supabase.
                        table('Feedback').
                        select("*").
                        order('created_at', desc=False).
                        execute())

        except APIError as e:
            return jsonify({'message:': {e.message}, 'code': {e.code}, 'details': {e.details}}), e.code

        feedbacks = response.data

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
    # POST /api/feedback → add a new note
    elif request.method == 'POST':
        data = request.json
        try:
            response = (
                supabase.table("Feedback")
                .insert({"node_id": data.get('node_id'),
                         "comment": data.get('comment'),
                         "tag": data.get('tag'),
                         "class_name": data.get('class_name'),
                         })
                .execute()
            )
            data = response.data
            if len(data) == 1 and (isinstance(data[0], dict)):
                return jsonify({'timestamp': data[0].get('created_at'),
                                'tag': data[0].get('tag'),
                                'text': data[0].get('comment')}), 201
            else:
                return jsonify({
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred on the server."
                }), 500
        except APIError as e:
            return jsonify({'message:': {e.message}, 'code': {e.code}, 'details': {e.details}}), e.code


@api.route('/export-feedbacks', methods=['GET'])
def export_feedbacks():
    r = feedback()
    return jsonify(r), 200



@api.route('/data', methods=['GET'])
def ontology_data_info():
    ontology_data = Path(current_app.static_folder ,'js' , 'ontology-data.js')
    if ontology_data.is_file():
        return jsonify({'message': 'Ontology data is currently served as static file ontology-data.js',
                        'path': '/static/js/ontology-data.js'}), 200
    else:
        return jsonify({'error': 'ontology-data.js not found. Place the file in the static/js/ folder.'}), 404
