from app import db
from datetime import datetime
from sqlalchemy import func
import json

class Player(db.Model):
    """Enhanced model for storing detailed player Bedwars statistics"""
    
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, unique=True)
    kills = db.Column(db.Integer, default=0, nullable=False)
    final_kills = db.Column(db.Integer, default=0, nullable=False)
    deaths = db.Column(db.Integer, default=0, nullable=False)
    beds_broken = db.Column(db.Integer, default=0, nullable=False)
    games_played = db.Column(db.Integer, default=0, nullable=False)
    wins = db.Column(db.Integer, default=0, nullable=False)
    experience = db.Column(db.Integer, default=0, nullable=False)
    role = db.Column(db.String(50), default='Игрок', nullable=False)
    server_ip = db.Column(db.String(100), default='', nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # New fields for enhanced statistics
    iron_collected = db.Column(db.Integer, default=0, nullable=False)
    gold_collected = db.Column(db.Integer, default=0, nullable=False)
    diamond_collected = db.Column(db.Integer, default=0, nullable=False)
    emerald_collected = db.Column(db.Integer, default=0, nullable=False)
    items_purchased = db.Column(db.Integer, default=0, nullable=False)
    
    # Minecraft skin system
    skin_url = db.Column(db.String(255), nullable=True)  # Custom skin URL from NameMC
    skin_type = db.Column(db.String(10), default='auto', nullable=False)  # auto, steve, alex, custom
    is_premium = db.Column(db.Boolean, default=False, nullable=False)  # Licensed Minecraft account
    
    # Personal profile information
    real_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    discord_tag = db.Column(db.String(50), nullable=True)
    youtube_channel = db.Column(db.String(100), nullable=True)
    twitch_channel = db.Column(db.String(100), nullable=True)
    favorite_server = db.Column(db.String(100), nullable=True)
    favorite_map = db.Column(db.String(100), nullable=True)
    preferred_gamemode = db.Column(db.String(50), nullable=True)
    profile_banner_color = db.Column(db.String(7), default='#3498db', nullable=True)
    profile_is_public = db.Column(db.Boolean, default=True, nullable=False)
    custom_status = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    
    # Custom profile customization
    custom_avatar_url = db.Column(db.String(255), nullable=True)
    custom_banner_url = db.Column(db.String(255), nullable=True)
    banner_is_animated = db.Column(db.Boolean, default=False, nullable=False)
    
    # Extended social networks
    social_networks = db.Column(db.Text, nullable=True)  # JSON array of social networks
    
    # Profile section backgrounds
    stats_section_color = db.Column(db.String(7), default='#343a40', nullable=True)
    info_section_color = db.Column(db.String(7), default='#343a40', nullable=True)
    social_section_color = db.Column(db.String(7), default='#343a40', nullable=True)
    prefs_section_color = db.Column(db.String(7), default='#343a40', nullable=True)
    
    # Password system
    password_hash = db.Column(db.String(255), nullable=True)
    has_password = db.Column(db.Boolean, default=False, nullable=False)
    
    # Leaderboard customization
    leaderboard_name_color = db.Column(db.String(7), default='#ffffff', nullable=True)
    leaderboard_stats_color = db.Column(db.String(7), default='#ffffff', nullable=True)
    leaderboard_use_gradient = db.Column(db.Boolean, default=False, nullable=False)
    leaderboard_gradient_start = db.Column(db.String(7), default='#ff6b35', nullable=True)
    leaderboard_gradient_end = db.Column(db.String(7), default='#f7931e', nullable=True)
    leaderboard_gradient_animated = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships for quest system
    player_quests = db.relationship('PlayerQuest', backref='player', lazy=True, cascade='all, delete-orphan')
    player_achievements = db.relationship('PlayerAchievement', backref='player', lazy=True, cascade='all, delete-orphan')
    
    @property
    def active_custom_title(self):
        """Get player's active custom title"""
        player_title = PlayerTitle.query.filter_by(
            player_id=self.id, 
            is_active=True
        ).first()
        return player_title.title if player_title else None
    
    def get_gradient_for_element(self, element_type):
        """Get gradient setting for specific element type"""
        setting = PlayerGradientSetting.query.filter_by(
            player_id=self.id,
            element_type=element_type,
            is_enabled=True
        ).first()
        return setting.css_gradient if setting else None
    
    @property
    def nickname_gradient(self):
        """Get nickname gradient CSS"""
        return self.get_gradient_for_element('nickname')
    
    @property
    def stats_gradient(self):
        """Get stats gradient CSS"""
        return self.get_gradient_for_element('stats')
    
    @property
    def title_gradient(self):
        """Get title gradient CSS"""
        return self.get_gradient_for_element('title')
    
    @property
    def kills_gradient(self):
        """Get kills gradient CSS"""
        return self.get_gradient_for_element('kills')
    
    @property
    def deaths_gradient(self):
        """Get deaths gradient CSS"""
        return self.get_gradient_for_element('deaths')
    
    @property
    def wins_gradient(self):
        """Get wins gradient CSS"""
        return self.get_gradient_for_element('wins')
    
    @property
    def beds_gradient(self):
        """Get beds gradient CSS"""
        return self.get_gradient_for_element('beds')
    
    @property
    def status_gradient(self):
        """Get status gradient CSS"""
        return self.get_gradient_for_element('status')
    
    @property
    def bio_gradient(self):
        """Get bio gradient CSS"""
        return self.get_gradient_for_element('bio')
    
    @property
    def role_gradient(self):
        """Get role gradient CSS"""
        return self.get_gradient_for_element('role')
    
    @property
    def can_use_static_gradients(self):
        """Check if player can use static gradients (level 80+)"""
        return self.level >= 80
    
    @property
    def can_use_animated_gradients(self):
        """Check if player can use animated gradients (level 100+)"""
        return self.level >= 100
    
    @property
    def can_customize_colors(self):
        """Check if player can customize interface colors (level 20+)"""
        return self.level >= 20
    
    @property
    def can_use_custom_avatars(self):
        """Check if player can use custom avatars (level 20+)"""
        return self.level >= 20
    
    @property
    def can_use_animated_banners(self):
        """Check if player can use animated banners (level 50+)"""
        return self.level >= 50
    
    @property
    def can_use_leaderboard_gradients(self):
        """Check if player can use gradients in leaderboard (level 50+)"""
        return self.level >= 50
    
    @property
    def can_use_leaderboard_animated_gradients(self):
        """Check if player can use animated gradients in leaderboard (level 75+)"""
        return self.level >= 75
    
    def get_social_networks_list(self):
        """Get parsed social networks list"""
        if not self.social_networks:
            return []
        try:
            import json
            return json.loads(self.social_networks)
        except:
            return []
    
    def set_social_networks_list(self, networks_list):
        """Set social networks list"""
        import json
        self.social_networks = json.dumps(networks_list) if networks_list else None
    
    def __repr__(self):
        return f'<Player {self.nickname}: Level {self.level} ({self.experience} XP)>'

    @property
    def kd_ratio(self):
        """Calculate kill/death ratio"""
        if self.deaths == 0:
            return self.kills if self.kills > 0 else 0
        return round(self.kills / self.deaths, 2)

    @property
    def fkd_ratio(self):
        """Calculate final kill/death ratio"""
        if self.deaths == 0:
            return self.final_kills if self.final_kills > 0 else 0
        return round(self.final_kills / self.deaths, 2)

    @property
    def win_rate(self):
        """Calculate win rate percentage"""
        if self.games_played == 0:
            return 0
        return round((self.wins / self.games_played) * 100, 1)

    @property
    def level(self):
        """Calculate player level based on Hypixel experience system"""
        # Hypixel level thresholds
        level_thresholds = [
            0, 10000, 22500, 37500, 55000, 75000, 97500, 122500, 150000, 180000,
            212500, 247500, 285000, 325000, 367500, 412500, 460000, 510000, 562500, 617500,
            675000, 735000, 797500, 862500, 930000, 1000000, 1072500, 1147500, 1225000, 1305000,
            1387500, 1472500, 1560000, 1650000, 1742500, 1837500, 1935000, 2035000, 2137500, 2242500,
            2350000, 2460000, 2572500, 2687500, 2805000, 2925000, 3047500, 3172500, 3300000, 3430000,
            3562500, 3697500, 3835000, 3975000, 4117500, 4262500, 4410000, 4560000, 4712500, 4867500,
            5025000, 5185000, 5347500, 5512500, 5680000, 5850000, 6022500, 6197500, 6375000, 6555000,
            6737500, 6922500, 7110000, 7300000, 7492500, 7687500, 7885000, 8085000, 8287500, 8492500,
            8700000, 8910000, 9122500, 9337500, 9555000, 9775000, 9997500, 10222500, 10450000, 10680000,
            10912500, 11147500, 11385000, 11625000, 11867500, 12112500, 12360000, 12610000, 12862500, 13117500
        ]
        
        for level, threshold in enumerate(level_thresholds, 1):
            if self.experience < threshold:
                return max(1, level - 1)
        
        # For levels 100+, each level requires 2500 more XP than the previous
        if self.experience >= 13117500:
            additional_levels = (self.experience - 13117500) // 2500
            return min(1000, 100 + additional_levels)
        
        return 100

    @property
    def level_progress(self):
        """Calculate progress to next level as percentage"""
        current_level = self.level
        if current_level >= 1000:
            return 100
            
        # Hypixel level thresholds
        level_thresholds = [
            0, 10000, 22500, 37500, 55000, 75000, 97500, 122500, 150000, 180000,
            212500, 247500, 285000, 325000, 367500, 412500, 460000, 510000, 562500, 617500,
            675000, 735000, 797500, 862500, 930000, 1000000, 1072500, 1147500, 1225000, 1305000,
            1387500, 1472500, 1560000, 1650000, 1742500, 1837500, 1935000, 2035000, 2137500, 2242500,
            2350000, 2460000, 2572500, 2687500, 2805000, 2925000, 3047500, 3172500, 3300000, 3430000,
            3562500, 3697500, 3835000, 3975000, 4117500, 4262500, 4410000, 4560000, 4712500, 4867500,
            5025000, 5185000, 5347500, 5512500, 5680000, 5850000, 6022500, 6197500, 6375000, 6555000,
            6737500, 6922500, 7110000, 7300000, 7492500, 7687500, 7885000, 8085000, 8287500, 8492500,
            8700000, 8910000, 9122500, 9337500, 9555000, 9775000, 9997500, 10222500, 10450000, 10680000,
            10912500, 11147500, 11385000, 11625000, 11867500, 12112500, 12360000, 12610000, 12862500, 13117500
        ]
        
        if current_level <= 100:
            current_threshold = level_thresholds[current_level - 1] if current_level > 0 else 0
            next_threshold = level_thresholds[current_level] if current_level < len(level_thresholds) else level_thresholds[-1] + 2500
        else:
            # For levels 100+
            current_threshold = 13117500 + (current_level - 100) * 2500
            next_threshold = 13117500 + (current_level - 99) * 2500
            
        if next_threshold == current_threshold:
            return 100
            
        progress = ((self.experience - current_threshold) / (next_threshold - current_threshold)) * 100
        return min(100, max(0, round(progress, 1)))

    @property
    def total_resources(self):
        """Calculate total resources collected"""
        return self.iron_collected + self.gold_collected + self.diamond_collected + self.emerald_collected

    @property
    def star_rating(self):
        """Calculate star rating based on overall performance"""
        # Complex formula considering multiple factors
        base_score = 0
        
        # Level contribution (0-20 points)
        base_score += min(20, self.level * 0.5)
        
        # K/D ratio contribution (0-15 points)
        base_score += min(15, self.kd_ratio * 3)
        
        # Win rate contribution (0-15 points)
        base_score += min(15, self.win_rate * 0.15)
        
        # Bed breaking contribution (0-10 points)
        base_score += min(10, self.beds_broken * 0.1)
        
        # Final kills contribution (0-10 points)
        base_score += min(10, self.final_kills * 0.05)
        
        # Games played bonus (0-5 points for activity)
        base_score += min(5, self.games_played * 0.01)
        
        # Convert to 1-5 star rating
        return min(5, max(1, round(base_score / 13)))
    
    @property
    def minecraft_skin_url(self):
        """Get Minecraft skin URL based on skin type and settings"""
        # Use custom avatar if set
        if self.custom_avatar_url:
            return self.custom_avatar_url
            
        if self.skin_type == 'custom' and self.skin_url:
            return self.skin_url
        elif self.skin_type == 'steve':
            return 'https://mc-heads.net/avatar/steve/128'
        elif self.skin_type == 'alex':
            return 'https://mc-heads.net/avatar/alex/128'
        elif self.is_premium and self.nickname:
            # Try to get premium skin by nickname
            return f'https://mc-heads.net/avatar/{self.nickname}/128'
        else:
            # Default to steve/alex randomly based on nickname hash
            import hashlib
            hash_val = int(hashlib.md5(self.nickname.encode()).hexdigest(), 16)
            default_skin = 'alex' if hash_val % 2 else 'steve'
            return f'https://mc-heads.net/avatar/{default_skin}/128'
    
    def set_custom_skin(self, namemc_url):
        """Set custom skin from NameMC URL"""
        if namemc_url and 'namemc.com' in namemc_url:
            # Extract UUID or username from NameMC URL
            try:
                import re
                # Extract username from NameMC URL
                match = re.search(r'namemc\.com/profile/([^/]+)', namemc_url)
                if match:
                    username = match.group(1)
                    # Use Crafatar to get skin
                    self.skin_url = f'https://crafatar.com/avatars/{username}?size=128'
                    self.skin_type = 'custom'
                    return True
            except:
                pass
        return False

    @classmethod
    def get_leaderboard(cls, sort_by='experience', limit=50):
        """Get top players ordered by specified field"""
        if sort_by == 'experience':
            return cls.query.order_by(cls.experience.desc()).limit(limit).all()
        elif sort_by == 'kills':
            return cls.query.order_by(cls.kills.desc()).limit(limit).all()
        elif sort_by == 'final_kills':
            return cls.query.order_by(cls.final_kills.desc()).limit(limit).all()
        elif sort_by == 'beds_broken':
            return cls.query.order_by(cls.beds_broken.desc()).limit(limit).all()
        elif sort_by == 'wins':
            return cls.query.order_by(cls.wins.desc()).limit(limit).all()
        elif sort_by == 'level':
            return sorted(cls.query.all(), key=lambda p: p.level, reverse=True)[:limit]
        elif sort_by == 'kd_ratio':
            return sorted(cls.query.all(), key=lambda p: p.kd_ratio, reverse=True)[:limit]
        elif sort_by == 'win_rate':
            return sorted(cls.query.all(), key=lambda p: p.win_rate, reverse=True)[:limit]
        else:
            return cls.query.order_by(cls.experience.desc()).limit(limit).all()

    @classmethod
    def search_players(cls, query):
        """Search players by nickname"""
        return cls.query.filter(cls.nickname.ilike(f'%{query}%')).all()

    @classmethod
    def get_statistics(cls):
        """Get overall leaderboard statistics"""
        total_players = cls.query.count()
        if total_players == 0:
            return {
                'total_players': 0,
                'total_kills': 0,
                'total_deaths': 0,
                'total_games': 0,
                'total_wins': 0,
                'total_beds_broken': 0,
                'average_level': 0,
                'top_player': None
            }
            
        stats = db.session.query(
            func.sum(cls.kills).label('total_kills'),
            func.sum(cls.deaths).label('total_deaths'),
            func.sum(cls.games_played).label('total_games'),
            func.sum(cls.wins).label('total_wins'),
            func.sum(cls.beds_broken).label('total_beds_broken'),
            func.avg(cls.experience).label('average_experience')
        ).first()
        
        top_player = cls.query.order_by(cls.experience.desc()).first()
        
        return {
            'total_players': total_players,
            'total_kills': int(stats.total_kills) if stats and stats.total_kills else 0,
            'total_deaths': int(stats.total_deaths) if stats and stats.total_deaths else 0,
            'total_games': int(stats.total_games) if stats and stats.total_games else 0,
            'total_wins': int(stats.total_wins) if stats and stats.total_wins else 0,
            'total_beds_broken': int(stats.total_beds_broken) if stats and stats.total_beds_broken else 0,
            'average_level': round(stats.average_experience / 1000) if stats and stats.average_experience else 0,
            'top_player': top_player
        }

    def calculate_auto_experience(self):
        """Calculate experience based on player statistics"""
        base_xp = 0
        
        # XP from kills (10 XP per kill)
        base_xp += self.kills * 10
        
        # XP from final kills (50 XP per final kill)
        base_xp += self.final_kills * 50
        
        # XP from beds broken (100 XP per bed)
        base_xp += self.beds_broken * 100
        
        # XP from wins (200 XP per win)
        base_xp += self.wins * 200
        
        # XP from games played (25 XP per game)
        base_xp += self.games_played * 25
        
        # XP from resources collected (1 XP per 10 resources)
        base_xp += self.total_resources // 10
        
        # Bonus XP for good performance
        if self.kd_ratio >= 2.0:
            base_xp = int(base_xp * 1.2)  # 20% bonus
        elif self.kd_ratio >= 1.5:
            base_xp = int(base_xp * 1.1)  # 10% bonus
            
        if self.win_rate >= 75:
            base_xp = int(base_xp * 1.3)  # 30% bonus
        elif self.win_rate >= 50:
            base_xp = int(base_xp * 1.15)  # 15% bonus
        
        return base_xp

    def update_stats(self, **kwargs):
        """Update player statistics and auto-calculate experience"""
        old_stats = {
            'kills': self.kills,
            'final_kills': self.final_kills,
            'beds_broken': self.beds_broken,
            'wins': self.wins,
            'games_played': self.games_played
        }
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        # Only auto-update XP if stats changed significantly
        if any(getattr(self, key) != old_stats.get(key, 0) for key in old_stats):
            # Don't override manually set experience, just set a baseline
            calculated_xp = self.calculate_auto_experience()
            if self.experience < calculated_xp:
                self.experience = calculated_xp
                
        self.last_updated = datetime.utcnow()
        db.session.commit()

    @classmethod
    def add_player(cls, nickname, kills=0, final_kills=0, deaths=0, beds_broken=0, 
                   games_played=0, wins=0, experience=0, role='Игрок', server_ip='',
                   iron_collected=0, gold_collected=0, diamond_collected=0, 
                   emerald_collected=0, items_purchased=0):
        """Add a new player to the leaderboard"""
        player = cls(
            nickname=nickname,
            kills=kills,
            final_kills=final_kills,
            deaths=deaths,
            beds_broken=beds_broken,
            games_played=games_played,
            wins=wins,
            experience=experience,
            role=role,
            server_ip=server_ip,
            iron_collected=iron_collected,
            gold_collected=gold_collected,
            diamond_collected=diamond_collected,
            emerald_collected=emerald_collected,
            items_purchased=items_purchased
        )
        db.session.add(player)
        db.session.commit()
        return player


class Quest(db.Model):
    """Quest system for gamification"""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # kills, beds, wins, etc.
    target_value = db.Column(db.Integer, nullable=False)
    reward_xp = db.Column(db.Integer, default=0)
    reward_title = db.Column(db.String(100), nullable=True)
    icon = db.Column(db.String(50), default='fas fa-trophy')
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard, epic
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with player quest progress
    player_quests = db.relationship('PlayerQuest', backref='quest', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quest {self.title}>'
    
    @property
    def completion_rate(self):
        """Calculate overall completion rate"""
        total_attempts = PlayerQuest.query.filter_by(quest_id=self.id).count()
        if total_attempts == 0:
            return 0
        completed = PlayerQuest.query.filter_by(quest_id=self.id, is_completed=True).count()
        return round((completed / total_attempts) * 100, 1)
    
    @classmethod
    def get_active_quests(cls):
        """Get all active quests"""
        return cls.query.filter_by(is_active=True).all()
    
    @classmethod
    def create_default_quests(cls):
        """Create default quests for the game"""
        default_quests = [
            {
                'title': 'Первая кровь',
                'description': 'Убейте 10 игроков в режиме Bedwars',
                'type': 'kills',
                'target_value': 10,
                'reward_xp': 1000,
                'reward_title': 'Воин',
                'icon': 'fas fa-sword',
                'difficulty': 'easy'
            },
            {
                'title': 'Разрушитель кроватей',
                'description': 'Сломайте 5 кроватей противников',
                'type': 'beds_broken',
                'target_value': 5,
                'reward_xp': 1500,
                'reward_title': 'Разрушитель',
                'icon': 'fas fa-bed',
                'difficulty': 'easy'
            },
            {
                'title': 'Победитель',
                'description': 'Выиграйте 10 игр',
                'type': 'wins',
                'target_value': 10,
                'reward_xp': 2000,
                'reward_title': 'Чемпион',
                'icon': 'fas fa-trophy',
                'difficulty': 'medium'
            },
            {
                'title': 'Убийца',
                'description': 'Убейте 100 игроков',
                'type': 'kills',
                'target_value': 100,
                'reward_xp': 5000,
                'reward_title': 'Убийца',
                'icon': 'fas fa-skull',
                'difficulty': 'medium'
            },
            {
                'title': 'Финальный удар',
                'description': 'Совершите 25 финальных убийств',
                'type': 'final_kills',
                'target_value': 25,
                'reward_xp': 3000,
                'reward_title': 'Палач',
                'icon': 'fas fa-lightning-bolt',
                'difficulty': 'medium'
            },
            {
                'title': 'Коллекционер алмазов',
                'description': 'Соберите 1000 алмазов',
                'type': 'diamond_collected',
                'target_value': 1000,
                'reward_xp': 4000,
                'reward_title': 'Кладоискатель',
                'icon': 'fas fa-gem',
                'difficulty': 'hard'
            },
            {
                'title': 'Легенда Bedwars',
                'description': 'Достигните 50 побед',
                'type': 'wins',
                'target_value': 50,
                'reward_xp': 10000,
                'reward_title': 'Легенда',
                'icon': 'fas fa-crown',
                'difficulty': 'epic'
            },
            {
                'title': 'Мастер ресурсов',
                'description': 'Соберите 10000 единиц железа',
                'type': 'iron_collected',
                'target_value': 10000,
                'reward_xp': 6000,
                'reward_title': 'Майнер',
                'icon': 'fas fa-tools',
                'difficulty': 'hard'
            }
        ]
        
        for quest_data in default_quests:
            existing = cls.query.filter_by(title=quest_data['title']).first()
            if not existing:
                quest = cls(**quest_data)
                db.session.add(quest)
        
        db.session.commit()


class PlayerQuest(db.Model):
    """Player progress on quests"""
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    current_progress = db.Column(db.Integer, default=0)
    baseline_value = db.Column(db.Integer, default=0)  # Starting value when quest was accepted
    is_completed = db.Column(db.Boolean, default=False)
    is_accepted = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    accepted_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<PlayerQuest {self.player_id}:{self.quest_id}>'
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        quest_obj = Quest.query.get(self.quest_id)
        if not quest_obj or quest_obj.target_value == 0:
            return 100
        return min(100, round((self.current_progress / quest_obj.target_value) * 100))
    
    def check_completion(self, player_stat_value):
        """Check if quest should be completed"""
        # Calculate progress from baseline
        progress_from_baseline = max(0, player_stat_value - self.baseline_value)
        self.current_progress = progress_from_baseline
        quest_obj = Quest.query.get(self.quest_id)
        
        if not self.is_completed and quest_obj and self.current_progress >= quest_obj.target_value:
            self.is_completed = True
            self.completed_at = datetime.utcnow()
            return True
        return False
    
    @classmethod
    def update_player_quest_progress(cls, player):
        """Update quest progress only for accepted quests"""
        completed_quests = []
        
        # Only update progress for accepted quests
        accepted_quests = cls.query.filter_by(
            player_id=player.id,
            is_accepted=True,
            is_completed=False
        ).all()
        
        for player_quest in accepted_quests:
            quest = player_quest.quest
            
            # Get current stat value
            current_stat_value = getattr(player, quest.type, 0)
            
            # Check completion based on progress from baseline
            if player_quest.check_completion(current_stat_value):
                completed_quests.append(quest)
                
                # Award XP only, don't auto-assign title or role
                player.experience += quest.reward_xp
        
        if completed_quests:
            db.session.commit()
        
        return completed_quests


class Achievement(db.Model):
    """Achievement system for special accomplishments"""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fas fa-medal')
    rarity = db.Column(db.String(20), default='common')  # common, rare, epic, legendary
    unlock_condition = db.Column(db.Text, nullable=False)  # JSON condition
    reward_xp = db.Column(db.Integer, default=0)
    reward_title = db.Column(db.String(100), nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with player achievements
    player_achievements = db.relationship('PlayerAchievement', backref='achievement', lazy=True)
    
    def __repr__(self):
        return f'<Achievement {self.title}>'
    
    def check_unlock_condition(self, player):
        """Check if player meets achievement unlock condition"""
        try:
            import json
            condition = json.loads(self.unlock_condition)
            
            for key, required_value in condition.items():
                if key == 'kd_ratio':
                    if float(player.kd_ratio) < float(required_value):
                        return False
                elif key == 'win_rate':
                    if float(player.win_rate) < float(required_value):
                        return False
                elif key == 'total_resources':
                    if player.total_resources < required_value:
                        return False
                else:
                    player_value = getattr(player, key, 0)
                    if player_value < required_value:
                        return False
                        
            return True
        except Exception as e:
            print(f"Error checking achievement condition: {e}")
            return False
    
    @classmethod
    def check_player_achievements(cls, player):
        """Check and award new achievements for player"""
        new_achievements = []
        
        # Get all achievements not yet earned by player
        earned_achievement_ids = [pa.achievement_id for pa in player.player_achievements]
        unearned_achievements = cls.query.filter(~cls.id.in_(earned_achievement_ids)).all()
        
        for achievement in unearned_achievements:
            if achievement.check_unlock_condition(player):
                # Award achievement
                player_achievement = PlayerAchievement(
                    player_id=player.id,
                    achievement_id=achievement.id
                )
                db.session.add(player_achievement)
                
                # Award XP only, don't auto-assign title
                player.experience += achievement.reward_xp
                
                new_achievements.append(achievement)
        
        if new_achievements:
            db.session.commit()
            
        return new_achievements
    
    @classmethod
    def create_default_achievements(cls):
        """Create default achievements"""
        default_achievements = [
            {
                'title': 'Новичок',
                'description': 'Сыграйте первую игру',
                'icon': 'fas fa-baby',
                'rarity': 'common',
                'unlock_condition': '{"games_played": 1}',
                'reward_xp': 500
            },
            {
                'title': 'Неудержимый',
                'description': 'Убейте 100 игроков',
                'icon': 'fas fa-fire',
                'rarity': 'rare',
                'unlock_condition': '{"kills": 100}',
                'reward_xp': 2500,
                'is_hidden': True
            },
            {
                'title': 'Коллекционер',
                'description': 'Соберите 5000 единиц ресурсов',
                'icon': 'fas fa-coins',
                'rarity': 'epic',
                'unlock_condition': '{"total_resources": 5000}',
                'reward_xp': 5000,
                'is_hidden': True
            },
            {
                'title': 'Мастер Bedwars',
                'description': 'Достигните K/D соотношения 3.0',
                'icon': 'fas fa-crown',
                'rarity': 'legendary',
                'unlock_condition': '{"kd_ratio": 3.0}',
                'reward_xp': 10000
            },
            {
                'title': 'Божество PVP',
                'description': 'Достигните K/D соотношения 5.0 и совершите 1000+ убийств',
                'icon': 'fas fa-bolt',
                'rarity': 'mythic',
                'unlock_condition': '{"kd_ratio": 5.0, "kills": 1000}',
                'reward_xp': 50000,
                'reward_title': 'Божество PVP',
                'is_hidden': True
            },
            {
                'title': 'Разрушитель миров',
                'description': 'Сломайте 500 кроватей противников',
                'icon': 'fas fa-meteor',
                'rarity': 'mythic',
                'unlock_condition': '{"beds_broken": 500}',
                'reward_xp': 75000,
                'reward_title': 'Разрушитель миров',
                'is_hidden': True
            },
            {
                'title': 'Легенда сервера',
                'description': 'Достигните 95% процента побед при 100+ играх',
                'icon': 'fas fa-dragon',
                'rarity': 'mythic',
                'unlock_condition': '{"win_rate": 95.0, "games_played": 100}',
                'reward_xp': 100000,
                'reward_title': 'Легенда сервера',
                'is_hidden': True
            },
            {
                'title': 'Повелитель ресурсов',
                'description': 'Соберите 100,000 единиц ресурсов',
                'icon': 'fas fa-gem',
                'rarity': 'mythic',
                'unlock_condition': '{"total_resources": 100000}',
                'reward_xp': 80000,
                'reward_title': 'Повелитель ресурсов',
                'is_hidden': True
            },
            {
                'title': 'Абсолютный чемпион',
                'description': 'Выиграйте 1000 игр подряд',
                'icon': 'fas fa-infinity',
                'rarity': 'mythic',
                'unlock_condition': '{"wins": 1000, "win_rate": 100.0}',
                'reward_xp': 250000,
                'reward_title': 'Абсолютный чемпион',
                'is_hidden': True
            }
        ]
        
        for achievement_data in default_achievements:
            existing = cls.query.filter_by(title=achievement_data['title']).first()
            if not existing:
                achievement = cls(**achievement_data)
                db.session.add(achievement)
        
        db.session.commit()


class PlayerAchievement(db.Model):
    """Player earned achievements"""
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlayerAchievement {self.player_id}:{self.achievement_id}>'


class CustomTitle(db.Model):
    """Custom titles that admins can assign to players"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(7), default='#ffd700')  # Hex color
    glow_color = db.Column(db.String(7), default='#ffd700')  # Glow effect color
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100), default='admin')
    
    def __repr__(self):
        return f'<CustomTitle {self.name}>'
    
    @classmethod
    def create_default_titles(cls):
        """Create default custom titles"""
        default_titles = [
            {
                'name': 'legend',
                'display_name': '🏆 Легенда',
                'color': '#ffd700',
                'glow_color': '#ffaa00'
            },
            {
                'name': 'champion',
                'display_name': '👑 Чемпион',
                'color': '#ff6b35',
                'glow_color': '#ff4444'
            },
            {
                'name': 'elite',
                'display_name': '⭐ Элита',
                'color': '#9b59b6',
                'glow_color': '#8e44ad'
            },
            {
                'name': 'destroyer',
                'display_name': '💥 Разрушитель',
                'color': '#e74c3c',
                'glow_color': '#c0392b'
            },
            {
                'name': 'master',
                'display_name': '🎯 Мастер',
                'color': '#3498db',
                'glow_color': '#2980b9'
            }
        ]
        
        for title_data in default_titles:
            existing = cls.query.filter_by(name=title_data['name']).first()
            if not existing:
                title = cls(**title_data)
                db.session.add(title)
        
        db.session.commit()


class PlayerTitle(db.Model):
    """Custom titles assigned to players by admins"""
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    title_id = db.Column(db.Integer, db.ForeignKey('custom_title.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_by = db.Column(db.String(100), default='admin')
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    player = db.relationship('Player', backref='custom_titles')
    title = db.relationship('CustomTitle', backref='assigned_players')
    
    def __repr__(self):
        return f'<PlayerTitle {self.player_id}:{self.title_id}>'


class GradientTheme(db.Model):
    """Gradient themes for various UI elements"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    element_type = db.Column(db.String(50), nullable=False)  # nickname, title, stats, kills, etc.
    color1 = db.Column(db.String(7), nullable=False)  # First gradient color
    color2 = db.Column(db.String(7), nullable=False)  # Second gradient color
    color3 = db.Column(db.String(7), nullable=True)   # Optional third color
    gradient_direction = db.Column(db.String(20), default='45deg')  # Gradient direction
    animation_enabled = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GradientTheme {self.name}>'
    
    @property
    def css_gradient(self):
        """Generate CSS gradient string"""
        if self.color3:
            return f"linear-gradient({self.gradient_direction}, {self.color1}, {self.color2}, {self.color3})"
        return f"linear-gradient({self.gradient_direction}, {self.color1}, {self.color2})"
    
    @classmethod
    def create_default_themes(cls):
        """Create default gradient themes"""
        default_themes = [
            # Nickname gradients
            {
                'name': 'fire_nickname',
                'display_name': '🔥 Огненный',
                'element_type': 'nickname',
                'color1': '#ff6b35',
                'color2': '#f7931e',
                'color3': '#ffaa00',
                'gradient_direction': '45deg',
                'animation_enabled': True
            },
            {
                'name': 'ocean_nickname',
                'display_name': '🌊 Океанский',
                'element_type': 'nickname',
                'color1': '#00d2ff',
                'color2': '#3a7bd5',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'purple_nickname',
                'display_name': '🔮 Фиолетовый',
                'element_type': 'nickname',
                'color1': '#667eea',
                'color2': '#764ba2',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'rainbow_nickname',
                'display_name': '🌈 Радужный',
                'element_type': 'nickname',
                'color1': '#ff0000',
                'color2': '#ffff00',
                'color3': '#00ff00',
                'gradient_direction': '90deg',
                'animation_enabled': True
            },
            
            # Stats gradients
            {
                'name': 'gold_stats',
                'display_name': '🥇 Золотая статистика',
                'element_type': 'stats',
                'color1': '#ffd700',
                'color2': '#ffed4e',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'emerald_stats',
                'display_name': '💎 Изумрудная статистика',
                'element_type': 'stats',
                'color1': '#50c878',
                'color2': '#00ff7f',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'blood_stats',
                'display_name': '🩸 Кровавая статистика',
                'element_type': 'stats',
                'color1': '#dc143c',
                'color2': '#ff1744',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            
            # Individual stat gradients
            {
                'name': 'fire_kills',
                'display_name': '🔥 Огненные киллы',
                'element_type': 'kills',
                'color1': '#ff6b35',
                'color2': '#f7931e',
                'gradient_direction': '45deg',
                'animation_enabled': True
            },
            {
                'name': 'ice_deaths',
                'display_name': '❄️ Ледяные смерти',
                'element_type': 'deaths',
                'color1': '#74b9ff',
                'color2': '#0984e3',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'golden_wins',
                'display_name': '🏆 Золотые победы',
                'element_type': 'wins',
                'color1': '#ffd700',
                'color2': '#ffaa00',
                'gradient_direction': '45deg',
                'animation_enabled': True
            },
            {
                'name': 'diamond_beds',
                'display_name': '💎 Алмазные кровати',
                'element_type': 'beds',
                'color1': '#74b9ff',
                'color2': '#0984e3',
                'color3': '#6c5ce7',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            
            # Title gradients
            {
                'name': 'legendary_title',
                'display_name': '👑 Легендарный титул',
                'element_type': 'title',
                'color1': '#ffd700',
                'color2': '#ff6b35',
                'color3': '#8e44ad',
                'gradient_direction': '45deg',
                'animation_enabled': True
            },
            {
                'name': 'crystal_title',
                'display_name': '💎 Кристальный титул',
                'element_type': 'title',
                'color1': '#74b9ff',
                'color2': '#0984e3',
                'color3': '#6c5ce7',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            
            # Status gradients (level 20+)
            {
                'name': 'sunset_status',
                'display_name': '🌅 Закатный статус',
                'element_type': 'status',
                'color1': '#ff6b35',
                'color2': '#f7931e',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'ocean_status',
                'display_name': '🌊 Океанский статус',
                'element_type': 'status',
                'color1': '#00d2ff',
                'color2': '#3a7bd5',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'mystic_status',
                'display_name': '🔮 Мистический статус',
                'element_type': 'status',
                'color1': '#667eea',
                'color2': '#764ba2',
                'gradient_direction': '45deg',
                'animation_enabled': True
            },
            
            # Bio gradients (level 20+)
            {
                'name': 'elegant_bio',
                'display_name': '✨ Элегантное био',
                'element_type': 'bio',
                'color1': '#ffd700',
                'color2': '#ffed4e',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'royal_bio',
                'display_name': '👑 Королевское био',
                'element_type': 'bio',
                'color1': '#8e44ad',
                'color2': '#3498db',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'cosmic_bio',
                'display_name': '🌌 Космическое био',
                'element_type': 'bio',
                'color1': '#667eea',
                'color2': '#764ba2',
                'color3': '#f093fb',
                'gradient_direction': '45deg',
                'animation_enabled': True
            },
            
            # Role gradients
            {
                'name': 'admin_role',
                'display_name': '👑 Администраторская роль',
                'element_type': 'role',
                'color1': '#ff6b35',
                'color2': '#f7931e',
                'gradient_direction': '45deg',
                'animation_enabled': True
            },
            {
                'name': 'vip_role',
                'display_name': '💎 VIP роль',
                'element_type': 'role',
                'color1': '#8e44ad',
                'color2': '#3498db',
                'gradient_direction': '45deg',
                'animation_enabled': False
            },
            {
                'name': 'pro_role',
                'display_name': '⭐ Профессиональная роль',
                'element_type': 'role',
                'color1': '#28a745',
                'color2': '#20c997',
                'gradient_direction': '45deg',
                'animation_enabled': False
            }
        ]
        
        for theme_data in default_themes:
            existing = cls.query.filter_by(name=theme_data['name']).first()
            if not existing:
                theme = cls(**theme_data)
                db.session.add(theme)
        
        db.session.commit()


class PlayerGradientSetting(db.Model):
    """Player's gradient settings"""
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    element_type = db.Column(db.String(50), nullable=False)  # nickname, stats, etc.
    gradient_theme_id = db.Column(db.Integer, db.ForeignKey('gradient_theme.id'), nullable=True)
    custom_color1 = db.Column(db.String(7), nullable=True)
    custom_color2 = db.Column(db.String(7), nullable=True)
    custom_color3 = db.Column(db.String(7), nullable=True)
    is_enabled = db.Column(db.Boolean, default=True)
    assigned_by = db.Column(db.String(100), default='admin')
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    player = db.relationship('Player', backref='gradient_settings')
    gradient_theme = db.relationship('GradientTheme', backref='player_settings')
    
    def __repr__(self):
        return f'<PlayerGradientSetting {self.player_id}:{self.element_type}>'
    
    @property
    def css_gradient(self):
        """Get CSS gradient for this setting"""
        if self.gradient_theme_id and self.gradient_theme:
            return self.gradient_theme.css_gradient
        elif self.custom_color1 and self.custom_color2:
            if self.custom_color3:
                return f"linear-gradient(45deg, {self.custom_color1}, {self.custom_color2}, {self.custom_color3})"
            return f"linear-gradient(45deg, {self.custom_color1}, {self.custom_color2})"
        return None
