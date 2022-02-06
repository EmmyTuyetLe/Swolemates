import unittest
from model import connect_to_db, db, Location, User, Save
from server import app
import model
import server
import crud 
import seed

class SwolematesTests(unittest.TestCase):
    """Tests for main swolemates site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Welcome! Ready to meet swolemates and get strong?", result.data)
        self.assertNotIn(b"We're so happy you're here!", result.data)
        
    def test_loggedin_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"We're so happy you're here!", result.data)
        self.assertNotIn(b"Welcome! Ready to meet swolemates and get strong?", result.data)

    def test_logout(self):
        result = self.client.get("/logout")
        self.assertIn(b"Please come back soon! Go get swole!", result.data)
        
    def test_profile(self):
        result = self.client.get("/my_profile")
        self.assertIn(b"personal information", result.data)
        self.assertIn(b"Saved Swolemates", result.data)
        self.assertIn(b"View your messages", result.data)
        
    def test_allbuddies(self):
        result = self.client.get("/users")
        self.assertIn(b"Swolemate name:", result.data)
        self.assertIn(b"Save this swolemate as a workout buddy!", result.data)
        self.assertIn(b"a message!", result.data)
        
    def test_searchresults(self):
        result = self.client.get("/search?")
        self.assertIn(b"Website:", result.data)
        self.assertIn(b"Save this location as your preferred gym", result.data)
        self.assertIn(b"Click to see other swolemates who favorited this gym", result.data)
    
    def test_savedbuddies(self):
        result = self.client.get("/buddies")
        self.assertIn(b"Unsave this buddy from your swolemates", result.data)
        self.assertNotIn(b"Save this swolemate as a workout buddy!", result.data)
        self.assertIn(b"a message!", result.data)
    
    def test_messages(self):
        result = self.client.get("/buddies")
        self.assertIn(b"Unsave this buddy from your swolemates", result.data)
        self.assertNotIn(b"Save this swolemate as a workout buddy!", result.data)
        self.assertIn(b"a message!", result.data)
        
class SwolematesTestsDatabase(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        model.connect_to_db(server.app)
        model.db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()