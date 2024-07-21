from sqlalchemy.orm import sessionmaker
from models import Base, engine, Game, Review, User
from faker import Faker
import random

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Add a console message so we can see output when the seed file runs
print("Seeding games...")

# Clear existing data
session.query(Game).delete()
session.query(Review).delete()
session.query(User).delete()
session.commit()

fake = Faker()

# Generate users
users = [User(name=fake.name()) for _ in range(10)]
session.bulk_save_objects(users)
session.commit()

# Generate games
games = [Game(title=fake.word(), genre=fake.word(), platform=fake.word(), price=random.randint(0, 60)) for _ in range(10)]
session.bulk_save_objects(games)
session.commit()

# Generate reviews and link users and games
for user in users:
    for _ in range(random.randint(1, 5)):
        game = random.choice(games)
        review = Review(score=random.randint(1, 10), comment=fake.sentence(), game_id=game.id, user_id=user.id)
        session.add(review)
session.commit()

print("Seeding complete.")
