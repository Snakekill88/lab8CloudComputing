import sqlite3


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('cards.db')
        self.create_set_table()
        self.create_cards_table()
        # Why are we calling user table before to_do table
        # what happens if we swap them?

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def create_cards_table(self):
        query = """
       CREATE TABLE IF NOT EXISTS "Cards" (
         id INTEGER PRIMARY KEY,
         Card_Name TEXT,
         Card_Id TEXT,
         Description TEXT,
         Game TEXT,
         DateAdded Date DEFAULT CURRENT_DATE,
         Set_Id INTEGER FOREIGNKEY REFERENCES Set_(_id)
       );
       """

        self.conn.execute(query)

    def create_set_table(self):
        query = """
       CREATE TABLE IF NOT EXISTS "Set_" (
       _id INTEGER PRIMARY KEY AUTOINCREMENT,
       Name TEXT NOT NULL,
       Game TEXT,
       CreatedOn Date default CURRENT_DATE
       );
       """
        self.conn.execute(query)


class CardModel:
    TABLENAME = "Cards"

    def __init__(self):
        self.conn = sqlite3.connect('cards.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        where_clause = f"AND id={_id}"
        return self.list_items(where_clause)

    def create(self, params):
        print(params)
        query = f'insert into {self.TABLENAME} ' \
                f'(Card_Name, Card_Id, Description, Game,Set_Id) ' \
                f'values ("{params.get("Card_Name")}","{params.get("Card_Id")}",' \
                f'"{params.get("Description")}","{params.get("Game")}","{params.get("Set_Id")}")'

        """insert into cards (Card_Name, Card_Id, Description, Game,Set_Id) values
         ("Monkey D Luffy", "Op01-001","TEMPLATE CARD DESCRIPTION","One Piece TCG", 1)"""

        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted =  {1} " \
                f"WHERE id = {item_id}"
        print(query)
        self.conn.execute(query)
        return self.list_items()

    def update(self, item_id, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = ", ".join([f'{column} = "{value}"'
                               for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {item_id}"

        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        query = f"SELECT * " \
                f"from {self.TABLENAME}"
        # WHERE _is_deleted != {1} " + where_clause
        print(query)
        result_set = self.conn.execute(query).fetchall()
        print(result_set)
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class User:
    TABLENAME = "Set_"

    def create(self, name, game):
        query = f'insert into {self.TABLENAME} ' \
                f'(Name, Game) ' \
                f'values ({name},{game})'
        result = self.conn.execute(query)
        return result