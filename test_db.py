from sqllite_helper import create_table,add_user,update_user,display_all_user,top_user,get_first_place,delete_user, update_all_users_stats
import asyncio

def test_database():
    db_file = "leetcode.db"
    # Display all users
    asyncio.run(update_all_users_stats(db_file))
    top_user(db_file)

if __name__ == "__main__":
    test_database() 