from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, \
    SmallInteger, BigInteger

Base = declarative_base()


class Conf(Base):
    __tablename__ = 'conf'
    conf_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String)
    __table_args__ = (
        UniqueConstraint("name"),
    )

    def __repr__(self):
        return f"<Conf(conf_id={self.conf_id}, name={self.name}, value={self.value})>"


class UserType(Base):
    __tablename__ = 'user_type'
    user_type_id = Column(Integer, unsigned=True, nullable=False, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<UserType(user_type_id={self.user_type_id}, name={self.name})>"


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, Integerunsigned=True, nullable=False, primary_key=True, autoincrement=False)
    user_type_id = Column(Integer, ForeignKey(UserType.user_type_id, ondelete="cascade", onupdate="cascade",
                                              name="fk_user_user_type_id"),
                          Integerunsigned=True, nullable=False)
    # vk_user_id is another field because of SQLAlchemy autoincrementing first primary key in class
    # vk_user_id = Column(Integer, Integerunsigned=True, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, user_type_id={self.user_type_id}, vk_user_id={self.vk_user_id}, " \
               f"first_name={self.last_name}, user_type_id={self.last_name})>"


class CharacterType(Base):
    __tablename__ = 'character_type'
    character_type_id = Column(Integerunsigned=True, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<CharacterType(character_type_id={self.character_type_id}, name={self.name})>"


class Character(Base):
    __tablename__ = 'character'
    character_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    character_type_id = Column(Integer, ForeignKey(CharacterType.character_type_id,
                                                   ondelete="cascade", onupdate="cascade",
                                                   name="fk_character_character_type_id"),
                               nullable=False)
    name = Column(String, nullable=False)
    alive = Column(SmallInteger, nullable=False)
    level = Column(SmallInteger, nullable=False)
    xp = Column(BigInteger, nullable=False)
    money = Column(BigInteger, nullable=False)

    def __repr__(self):
        return f"<Character(character_id={self.character_id}, character_type_id={self.character_type_id}, " \
               f"name={self.name}, alive={self.alive}, level={self.level}, xp={self.xp}, money={self.money})>"


class UserCharacter(Base):
    __tablename__ = 'user_character'
    user_character_id = Column(Integer, Integerunsigned=True, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id,
                                         ondelete="cascade", onupdate="cascade",
                                         name="fk_user_character_user_id"),
                     Integerunsigned=True, nullable=False,)
    character_id = Column(Integer, ForeignKey(Character.character_id,
                                              ondelete="cascade", onupdate="cascade",
                                              name="fk_user_character_character_id"),
                          Integerunsigned=True, nullable=False)
    __table_args__ = (
        UniqueConstraint("user_id", "character_id", name="uk_user_id_character_id"),
    )

    def __repr__(self):
        return f"<UserCharacter(user_character_id={self.user_character_id}, user_id={self.user_id}, " \
               f"character_id={self.character_id})>"


class Attribute(Base):
    __tablename__ = 'attribute'
    attribute_id = Column(Integerunsigned=True, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False,)
    desc = Column(String)

    def __repr__(self):
        return f"<Attribute(attribute_id={self.attribute_id}, name={self.name}, " \
               f"desc={self.desc})>"


class CharacterAttribute(Base):
    __tablename__ = 'character_attribute'
    character_attribute_id = Column(Integer, Integerunsigned=True, nullable=False, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey(Character.character_id, ondelete="cascade", onupdate="cascade",
                                              name="fk_character_attribute_character_id"),
                          Integerunsigned=True, nullable=False)
    attribute_id = Column(Integer, ForeignKey(Attribute.attribute_id, ondelete="cascade", onupdate="cascade",
                                              name="fk_character_attribute_attribute_id"),
                          Integerunsigned=True, nullable=False)
    value = Column(BigInteger, Integerunsigned=True, nullable=False)
    __table_args__ = (
        UniqueConstraint("character_id", "attribute_id", name="uk_character_id_attribute_id"),
    )

    def __repr__(self):
        return f"<CharacterAttribute(character_attribute_id={self.character_attribute_id}, " \
               f"character_id={self.character_id}, attribute_id={self.attribute_id}, value={self.value})>"
