import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import (
    Base,
    engine,
    Player,
    College,
    HighSchool,
    PlayerCollege,
    PlayerHighSchool,
    Team,
    TeamID,
    MVP,
    SeasonTopPlayer,
    Champion,
    TeamPlayers,
    MvpVoteResults,
    PlayerPosition,
    Position
)

# # Create all tables before importing data
# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def to_int(x):
    return int(x) if pd.notna(x) and x != "" else None


def to_float(x):
    return float(x) if pd.notna(x) and x != "" else None


# -------------------- TEAM IDS --------------------
df = pd.read_excel("team_id.xlsx")
for _, r in df.iterrows():
    team_id_val = to_int(r["team_id"])
    existing = session.query(TeamID).filter_by(team_id=team_id_val).first()
    if not existing:
        session.add(
            TeamID(team_id=team_id_val, franchise_name=r["franchise_name"])
        )
session.commit()
print("team_ids imported")


# -------------------- TEAMS --------------------
df = pd.read_excel("teams.xlsx")
df = df.fillna("")

for _, r in df.iterrows():
    team_id_val = to_int(r["team_id"])
    existing = session.query(Team).filter_by(team_id=team_id_val).first()
    if not existing:
        session.add(
            Team(
                team_id=team_id_val,
                franchise_name=r["franchise_name"],
                location=r["location"],
                seasons_played=to_int(r["seasons_played"]),
                seasons_played_ft=r["seasons_played_FT"],
                total_matches=to_int(r["total_matches"]),
                total_wins=to_int(r["total_wins"]),
                total_loss=to_int(r["total_loss"]),
                w_l_ratio=r["w_l_ratio"],
                playoff_appearances=to_int(r["playoff_appearances"]),
                championships=to_int(r["Championships"]),
                coach=r["coach"],
                leageus=r["leageus"],
                hof_count=to_int(r["HOF_count"]),
                asg_count=to_int(r["ASG_count"]),
                arena_name=r["arena_name"],
            )
        )

session.commit()
print("teams imported")


# -------------------- PLAYERS --------------------
df = pd.read_csv("player.csv")

for _, r in df.iterrows():
    player_id_val = to_int(r["Player_Id"])
    existing = session.query(Player).filter_by(player_id=player_id_val).first()
    if not existing:
        session.add(
            Player(
                player_id=player_id_val,
                player=r["Player"],
                from_year=to_int(r["From"]),
                to_year=to_int(r["To"]),
                player_additional=r["Player-additional"],
                shoots=r["shoots"],
                height=to_float(r["height"]),
                weight=to_float(r["weight"]),
                born_date=r["born_date"],
                born_city_country=r["born_city_country"],
                league=r["league"],
                nba_debut=r["nba_debut"],
                career_length=r["career_length"],
                points=to_float(r["points"]),
                death_date=r["death_date"],
                age=to_float(r["age"]),
                team_id=to_float(r["team_id"]),
            )
        )

session.commit()
print("players imported")


# -------------------- COLLEGES --------------------
df = pd.read_csv("colleges.csv")

for _, r in df.iterrows():
    college_id_val = to_int(r["college_id"])
    existing = session.query(College).filter_by(college_id=college_id_val).first()
    if not existing:
        session.add(
            College(
                college_id=college_id_val,
                college_name=r["college_name"] if pd.notna(r["college_name"]) else None,
            )
        )

session.commit()
print("colleges imported")


# -------------------- HIGH SCHOOLS --------------------
df = pd.read_csv("high_schools.csv")

for _, r in df.iterrows():
    high_school_id_val = to_int(r["high_school_id"])
    existing = session.query(HighSchool).filter_by(high_school_id=high_school_id_val).first()
    if not existing:
        session.add(
            HighSchool(
                high_school_id=high_school_id_val,
                high_school_name=(
                    r["high_school_name"] if pd.notna(r["high_school_name"]) else None
                ),
            )
        )

session.commit()
print("high schools imported")


# -------------------- PLAYER - COLLEGE --------------------
df = pd.read_csv("player_college.csv")

for _, r in df.iterrows():
    player_id_val = to_int(r["Player_Id"])
    college_id_val = to_int(r["college_id"])
    existing = session.query(PlayerCollege).filter_by(
        player_id=player_id_val, college_id=college_id_val
    ).first()
    if not existing:
        session.add(
            PlayerCollege(
                player_id=player_id_val, college_id=college_id_val
            )
        )

session.commit()
print("player_college imported")


# -------------------- PLAYER - HIGH SCHOOL --------------------
df = pd.read_csv("player_high_school.csv")

for _, r in df.iterrows():
    player_id_val = to_int(r["Player_Id"])
    high_school_id_val = to_int(r["high_school_id"])
    existing = session.query(PlayerHighSchool).filter_by(
        player_id=player_id_val, high_school_id=high_school_id_val
    ).first()
    if not existing:
        session.add(
            PlayerHighSchool(
                player_id=player_id_val, high_school_id=high_school_id_val
            )
        )

session.commit()
print("player_high_school imported")


# -------------------- POSITION --------------------
df = pd.read_csv("positions.csv")

for _, r in df.iterrows():
    position_id_val = to_int(r["position_id"])
    existing = session.query(Position).filter_by(
        position_id=position_id_val
    ).first()
    if not existing:
        session.add(
            Position(
                position_name=r['position_name'], position_id=position_id_val
            )
        )

session.commit()
print("positions imported")


# -------------------- PLAYER - POSITION --------------------
df = pd.read_csv("player_position.csv")

for _, r in df.iterrows():
    player_id_val = to_int(r["Player_Id"])
    position_id_val = to_int(r["position_id"])
    existing = session.query(PlayerPosition).filter_by(
        player_id=player_id_val, position_id=position_id_val
    ).first()
    if not existing:
        session.add(
            PlayerPosition(
                player_id=player_id_val, position_id=position_id_val
            )
        )

session.commit()
print("player_position imported")


#  MVP
mvp_df = pd.read_csv(r"mvp_ids.csv")

for _, row in mvp_df.iterrows():
    existing = (
        session.query(MVP)
        .filter_by(player_id=int(row["Player_Id"]), season=row["Season"])
        .first()
    )

    if existing:
        continue

    mvp = MVP(
        player_id=int(row["Player_Id"]),
        season=row["Season"],
        league=row["Lg"],
        age=row["Age"],
        games=row["G"],
        points=row["PTS"],
        minutes_played=row["MP"],
        total_rebounds=row["TRB"],
        assists=row["AST"],
        steals=row["STL"],
        blocks=row["BLK"],
        field_goal_percentage=row["FG%"],
        three_point_field_goal_percentage=row["3P%"],
        free_throw_percentage=row["FT%"],
        win_shares=row["WS"],
    )
    session.add(mvp)

session.commit()
print("MVPs imported")

#  Season Top Players
season_df = pd.read_csv(r"top_players_ids.csv")

for _, row in season_df.iterrows():
    existing = (
        session.query(SeasonTopPlayer)
        .filter_by(player_id=int(row["Player_Id"]), season=row["Year"])
        .first()
    )

    if existing:
        continue

    stp = SeasonTopPlayer(
        player_id=int(row["Player_Id"]),
        season=row["Year"],
        rank=row["Rk"],
        position=row["Pos"],
        age=row["Age"],
        games=row["G"],
        points=row["PTS"],
        field_goals=row["FG"],
        field_goal_attempts=row["FGA"],
        field_goal_percentage=row["FG%"],
        free_throws=row["FT"],
        free_throw_attempts=row["FTA"],
        free_throw_percentage=row["FT%"],
        assists=row["AST"],
        personal_fouls=row["PF"],
    )
    session.add(stp)


champ_df = pd.read_excel(r"champion.xlsx")

for _, row in champ_df.iterrows():
    existing = session.query(Champion).filter_by(
        season=row["season"], team_id=row["team_id"]
    ).first()
    if not existing:
        cmp = Champion(
            season=row["season"],
            team_id=row["team_id"],
        )
        session.add(cmp)


team_p_df = pd.read_excel(r"team_players.xlsx")

for _, row in team_p_df.iterrows():
    existing = session.query(TeamPlayers).filter_by(
        season=row["season"],
        team_id=row["team_id"],
        player_id=row["Player_Id"],
    ).first()
    if not existing:
        tp = TeamPlayers(
            season=row["season"],
            team_id=row["team_id"],
            player_id=row["Player_Id"],
        )
        session.add(tp)


mvp_votes_df = pd.read_excel(r"MJA.xlsx")

for _, row in mvp_votes_df.iterrows():
    existing = session.query(MvpVoteResults).filter_by(
        season=row["season"],
        player_id=row["Player_Id"],
    ).first()
    if not existing:
        tp = MvpVoteResults(
            season=row["season"],
            player_id=row["Player_Id"],
        )
        session.add(tp)

session.commit()
print("Season top players imported")
