from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///nba.db", echo=False)
Base = declarative_base()


# -------------------- PLAYERS --------------------
class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True)
    player = Column(String)

    from_year = Column(Integer)
    to_year = Column(Integer)

    player_additional = Column(String)

    shoots = Column(String)

    height = Column(Float)
    weight = Column(Float)

    born_date = Column(String)
    born_city_country = Column(String)

    league = Column(String)
    nba_debut = Column(String)

    career_length = Column(String)
    points = Column(Float)

    death_date = Column(String)
    age = Column(Float)

    team_id = Column(Integer)


# -------------------- COLLEGES --------------------
class College(Base):
    __tablename__ = "colleges"

    college_id = Column(Integer, primary_key=True)
    college_name = Column(String)


# -------------------- HIGH SCHOOLS --------------------
class HighSchool(Base):
    __tablename__ = "high_schools"

    high_school_id = Column(Integer, primary_key=True)
    high_school_name = Column(String)


# -------------------- PLAYER - COLLEGE --------------------
class PlayerCollege(Base):
    __tablename__ = "player_college"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    college_id = Column(Integer)

    __table_args__ = (UniqueConstraint("player_id", "college_id"),)


# -------------------- PLAYER - HIGH SCHOOL --------------------
class PlayerHighSchool(Base):
    __tablename__ = "player_high_school"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    high_school_id = Column(Integer)

    __table_args__ = (UniqueConstraint("player_id", "high_school_id"),)


# -------------------- POSITION --------------------
class Position(Base):
    __tablename__ = "positions"

    position_id = Column(Integer, primary_key=True)
    position_name = Column(String)


# -------------------- PLAYER - POSITION --------------------
class PlayerPosition(Base):
    __tablename__ = "player_position"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.player_id"))
    position_id = Column(Integer, ForeignKey("positions.position_id"), nullable=True)


class MVP(Base):
    __tablename__ = "mvp"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    season = Column(String, nullable=False)
    league = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    games = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    minutes_played = Column(Float, nullable=True)
    total_rebounds = Column(Float, nullable=True)
    assists = Column(Float, nullable=True)
    steals = Column(Float, nullable=True)
    blocks = Column(Float, nullable=True)
    field_goal_percentage = Column(Float, nullable=True)
    three_point_field_goal_percentage = Column(Float, nullable=True)
    free_throw_percentage = Column(Float, nullable=True)
    win_shares = Column(Float, nullable=True)
    

class SeasonTopPlayer(Base):
    __tablename__ = "season_top_players"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    rank = Column(Integer, nullable=True)
    season = Column(String, nullable=False)
    position = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    games = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    field_goals = Column(Integer, nullable=True)
    field_goal_attempts = Column(Integer, nullable=True)
    field_goal_percentage = Column(Float, nullable=True)
    free_throws = Column(Integer, nullable=True)
    free_throw_attempts = Column(Integer, nullable=True)
    free_throw_percentage = Column(Float, nullable=True)
    assists = Column(Integer, nullable=True)
    personal_fouls = Column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("player_id", "season", name="uq_player_season"),
    )


# -------------------- TEAM IDS --------------------
class TeamID(Base):
    __tablename__ = "team_ids"

    team_id = Column(Integer, primary_key=True)
    franchise_name = Column(String)


# -------------------- TEAMS --------------------
class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True)
    franchise_name = Column(String)
    location = Column(String)

    seasons_played = Column(Integer)
    seasons_played_ft = Column(String)

    total_matches = Column(Integer)
    total_wins = Column(Integer)
    total_loss = Column(Integer)

    w_l_ratio = Column(String)

    playoff_appearances = Column(Integer)
    championships = Column(Integer)

    coach = Column(String)
    leageus = Column(String)

    hof_count = Column(Integer)
    asg_count = Column(Integer)

    arena_name = Column(String)


class Champion(Base):
    __tablename__ = "champion"

    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id"))


class TeamPlayers(Base):
    __tablename__ = "team_players"

    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    player_id = Column(Integer, ForeignKey("players.player_id"))


class MvpVoteResults(Base):
    __tablename__ = "mvp_vote_results"

    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.player_id"))


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
