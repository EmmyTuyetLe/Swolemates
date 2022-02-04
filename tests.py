import unittest
from model import connect_to_db, db, Location, User, Save
import server
import crud 

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

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()