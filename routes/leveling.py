# routes/leveling.py
from flask import Blueprint, request, jsonify, current_app
from models import db, User, Level, UserActivity, LootBox, LootBoxType, Semester
from models.semester import Semester
from datetime import datetime

leveling_bp = Blueprint('leveling', __name__)

@leveling_bp.route('/users/<int:user_id>/progress', methods=['GET'])
def get_user_progress(user_id):
    """Get a user's level and XP progress"""
    user = User.query.get_or_404(user_id)
    
    # Get current level details
    current_level = Level.query.filter_by(level_number=user.current_level).first()
    
    # Get next level details (if exists and not at max level)
    next_level = None
    if user.current_level < 25:  # Max level is 25
        next_level = Level.query.filter_by(level_number=user.current_level + 1).first()
    
    # Calculate progress to next level
    progress_percent = 0
    xp_for_next_level = 0
    
    if next_level:
        # Determine which XP values to use (new or old system)
        if hasattr(next_level, 'level_xp') and next_level.level_xp is not None:
            # New system
            xp_needed = next_level.level_xp  # XP needed for this specific level
            current_level_total_xp = current_level.total_xp if current_level else 0
            xp_earned_in_level = user.current_xp - current_level_total_xp
            xp_for_next_level = next_level.level_xp - xp_earned_in_level
        else:
            # Old system
            current_xp_required = current_level.xp_required if current_level else 0
            xp_needed = next_level.xp_required - current_xp_required
            xp_earned_in_level = user.current_xp - current_xp_required
            xp_for_next_level = next_level.xp_required - user.current_xp
        
        if xp_needed > 0:
            progress_percent = min(100, int((xp_earned_in_level / xp_needed) * 100))
    else:
        # Max level reached
        progress_percent = 100
        
    # Get recent activities
    recent_activities = UserActivity.query.filter_by(user_id=user_id).order_by(
        UserActivity.timestamp.desc()
    ).limit(10).all()
    
    # Format the response
    result = {
        "user_id": user.id,
        "username": user.username,
        "current_level": user.current_level,
        "current_xp": user.current_xp,
        "total_xp_earned": user.total_xp_earned,
        "current_tier": user.current_tier,
        "active_weeks_streak": user.active_weeks_streak,
        "activity_bonus": f"{user.calculate_activity_bonus():.2f}x",
        "next_level": next_level.level_number if next_level else None,
        "xp_for_next_level": xp_for_next_level,
        "xp_needed_for_level": next_level.level_xp if next_level else 0,
        "progress_percent": progress_percent,
        "max_level_reached": user.current_level == 25,
        "current_semester": user.current_semester,
        "recent_activities": [
            {
                "timestamp": activity.timestamp.isoformat(),
                "activity_type": activity.activity_type,
                "xp_earned": activity.xp_earned,
                "description": activity.description
            } for activity in recent_activities
        ]
    }
    
    return jsonify(result)


@leveling_bp.route('/levels', methods=['GET'])
def get_levels():
    """Get all level definitions"""
    levels = Level.query.order_by(Level.level_number).all()
    
    result = [
        {
            "level_number": level.level_number,
            "level_xp": level.level_xp,
            "total_xp": level.total_xp,
            "tier": level.tier
        } for level in levels
    ]
    
    return jsonify(result)


@leveling_bp.route('/users/<int:user_id>/lootboxes', methods=['GET'])
def get_user_lootboxes(user_id):
    """Get all loot boxes for a user"""
    # Check if user exists
    user = User.query.get_or_404(user_id)
    
    # Get user's loot boxes
    loot_boxes = LootBox.query.filter_by(user_id=user_id).all()
    
    result = []
    for box in loot_boxes:
        box_type = LootBoxType.query.get(box.type_id)
        if box_type:
            result.append({
                "id": box.id,
                "type_name": box_type.name,
                "description": box_type.description,
                "tier": box_type.tier,
                "icon_url": box_type.icon_url,
                "is_opened": box.is_opened,
                "awarded_at": box.awarded_at.isoformat(),
                "opened_at": box.opened_at.isoformat() if box.opened_at else None,
                "awarded_for": box.awarded_for
            })
    
    return jsonify(result)


@leveling_bp.route('/users/<int:user_id>/lootboxes/<int:lootbox_id>/open', methods=['POST'])
def open_lootbox(user_id, lootbox_id):
    """Open a loot box"""
    # Check if user exists
    user = User.query.get_or_404(user_id)
    
    # Check if loot box exists and belongs to user
    loot_box = LootBox.query.filter_by(id=lootbox_id, user_id=user_id).first()
    if not loot_box:
        return jsonify({"error": "Loot box not found or doesn't belong to this user"}), 404
    
    # Try to open the loot box
    if loot_box.is_opened:
        return jsonify({"error": "Loot box has already been opened"}), 400
    
    success = loot_box.open()
    
    if success:
        # In the future, this would return the contents of the loot box
        return jsonify({"message": "Loot box opened successfully"}), 200
    else:
        return jsonify({"error": "Failed to open loot box"}), 500


@leveling_bp.route('/admin/semester', methods=['POST'])
def start_new_semester():
    """Start a new semester (admin only)"""
    # This should be protected by admin authentication in a real app
    
    data = request.json
    if not data or 'name' not in data or 'start_date' not in data or 'end_date' not in data:
        return jsonify({"error": "Missing required fields: name, start_date, end_date"}), 400
    
    try:
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400
    
    # Start new semester
    new_semester = Semester.start_new_semester(
        name=data['name'],
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        "message": "New semester started successfully",
        "semester": {
            "name": new_semester.name,
            "start_date": new_semester.start_date.isoformat(),
            "end_date": new_semester.end_date.isoformat()
        }
    }), 201