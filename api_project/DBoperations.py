from connection import Session, User

session = Session()

# #create a user
user = User(name="Muhammad Moiz")

session.add(user)
session.commit()

# Retrieval through id

users = session.query(User).filter_by(id=2).one_or_none()

print("ID= ", users.id)
print("Name= ", users.name)

# Update data
users.name = "Muhammad Ahmed"
session.commit()

users = session.query(User).filter_by(id=2).one_or_none()
if users:
    print("ID= ", users.id)
    print("Name= ", users.name)

# Search by name

users = session.query(User).filter(User.name.like("%ah%"))
for user in users:
    print("ID= ", user.id)
    print("Name= ", user.name)

users = session.query(User).filter(User.name.startswith("M"))
for user in users:
    print("ID= ", user.id)
    print("Name= ", user.name)


# Delete data


users = session.query(User).filter_by(id=1).one_or_none()
if users:
    session.delete(users)
    session.commit()
