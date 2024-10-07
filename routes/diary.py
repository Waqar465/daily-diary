from flask import Blueprint, request, jsonify
from utils.token import token_required
from models import DiaryEntry
from datetime import datetime

diary_bp = Blueprint('diary', __name__)

@diary_bp.route('/write', methods=['POST'])
@token_required
def write_diary(current_user):
    data = request.json
    title = data.get("title")
    content = data.get("content")

    DiaryEntry.insert_entry(current_user['_id'], title, content, datetime.utcnow())
    return jsonify({"message": "Diary entry added"}), 201

@diary_bp.route('/entries', methods=['GET'])
@token_required
def get_entries(current_user):
    entries = DiaryEntry.get_user_entries(current_user['_id'])
    entries_list = [{"title": entry['title'], "content": entry['content'], "date": entry['date']} for entry in entries]

    return jsonify({"entries": entries_list}), 200
