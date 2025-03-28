# routes/rewards.py
from flask import Blueprint, request, jsonify, current_app
from models import db, User, RewardType, UserReward, LootBox, LootBoxType
from models.reward_system import RewardSystem

rewards_bp = Blueprint('rewards', __name__)

@rewards_bp.route('/users/<int:user_id>/rewards', methods=['GET'])
def get_user_rewards(user_id):
    """Get all rewards in a user's inventory"""
    # Check if user exists
    user = User.query.get_or_404(user_id)
    
    # Get user's rewards
    user_rewards = UserReward.query.filter_by(user_id=user_id).all()
    
    result = []
    for user_reward in user_rewards:
        reward = RewardType.query.get(user_reward.reward_type_id)
        if reward:
            result.append({
                "id": user_reward.id,
                "reward_id": reward.id,
                "name": reward.name,
                "description": reward.description,
                "image_url": reward.image_url,
                "tier": reward.tier,
                "category": reward.category,
                "theme": reward.theme,
                "is_rare": reward.is_rare,
                "is_equipped": user_reward.is_equipped,
                "acquired_at": user_reward.acquired_at.isoformat(),
                "loot_box_id": user_reward.loot_box_id
            })
    
    return jsonify(result)


@rewards_bp.route('/reward-types', methods=['GET'])
def get_reward_types():
    """Get all possible reward types"""
    # Optional filtering by tier, category, theme
    tier = request.args.get('tier', type=int)
    category = request.args.get('category')
    theme = request.args.get('theme')
    
    query = RewardType.query
    
    if tier:
        query = query.filter_by(tier=tier)
    if category:
        query = query.filter_by(category=category)
    if theme:
        query = query.filter_by(theme=theme)
    
    reward_types = query.all()
    
    result = [
        {
            "id": reward.id,
            "name": reward.name,
            "description": reward.description,
            "image_url": reward.image_url,
            "tier": reward.tier,
            "category": reward.category,
            "theme": reward.theme,
            "is_rare": reward.is_rare
        } for reward in reward_types
    ]
    
    return jsonify(result)


@rewards_bp.route('/users/<int:user_id>/rewards/<int:reward_id>/equip', methods=['POST'])
def equip_reward(user_id, reward_id):
    """Equip a reward as the user's profile image"""
    # Check if user exists
    user = User.query.get_or_404(user_id)
    
    # Check if the reward exists and belongs to the user
    user_reward = UserReward.query.filter_by(id=reward_id, user_id=user_id).first()
    if not user_reward:
        return jsonify({"error": "Reward not found or doesn't belong to this user"}), 404
    
    # Equip the reward
    success = user.equip_reward(reward_id)
    
    if success:
        return jsonify({"message": "Reward equipped successfully"}), 200
    else:
        return jsonify({"error": "Failed to equip reward"}), 500


@rewards_bp.route('/users/<int:user_id>/lootboxes/<int:lootbox_id>/open', methods=['POST'])
def open_lootbox(user_id, lootbox_id):
    """Open a loot box and receive a reward"""
    # Check if user exists
    user = User.query.get_or_404(user_id)
    
    # Check if the loot box exists and belongs to the user
    loot_box = LootBox.query.filter_by(id=lootbox_id, user_id=user_id).first()
    if not loot_box:
        return jsonify({"error": "Loot box not found or doesn't belong to this user"}), 404
    
    # Check if already opened
    if loot_box.is_opened:
        return jsonify({"error": "Loot box already opened"}), 400
    
    # Open the loot box
    success = loot_box.open()
    
    if success:
        # Get the reward that was just awarded
        user_reward = UserReward.query.filter_by(loot_box_id=lootbox_id).first()
        reward_data = None
        
        if user_reward:
            reward = RewardType.query.get(user_reward.reward_type_id)
            if reward:
                reward_data = {
                    "reward_id": user_reward.id,
                    "name": reward.name,
                    "description": reward.description,
                    "image_url": reward.image_url,
                    "tier": reward.tier,
                    "category": reward.category,
                    "theme": reward.theme,
                    "is_rare": reward.is_rare
                }
        
        return jsonify({
            "message": "Loot box opened successfully",
            "reward": reward_data
        }), 200
    else:
        return jsonify({"error": "Failed to open loot box"}), 500


@rewards_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all available reward categories and themes"""
    # Get all unique categories
    categories = db.session.query(RewardType.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    # Get all unique themes
    themes = db.session.query(RewardType.theme).distinct().all()
    themes = [t[0] for t in themes if t[0]]
    
    return jsonify({
        "categories": categories,
        "themes": themes
    })


@rewards_bp.route('/admin/rewards', methods=['POST'])
def create_reward_type():
    """Create a new reward type (admin only)"""
    # This should be protected by admin authentication in a real app
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    required_fields = ['name', 'description', 'image_url', 'tier', 'category', 'theme']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Check for duplicate
    existing = RewardType.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({"error": "A reward with this name already exists"}), 400
    
    # Create the reward type
    new_reward = RewardType(
        name=data['name'],
        description=data['description'],
        image_url=data['image_url'],
        tier=data['tier'],
        category=data['category'],
        theme=data['theme'],
        is_rare=data.get('is_rare', False)
    )
    
    db.session.add(new_reward)
    db.session.commit()
    
    return jsonify({
        "message": "Reward type created successfully",
        "id": new_reward.id
    }), 201