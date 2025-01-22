"""Test cases for the console module."""

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand  # Make sure to import your console class

class TestConsole(unittest.TestCase):
    @patch("builtins.input", side_effect=[
        'create State name="California"',
        'create State name="Arizona"',
        'all State',
        'create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297',
        'all Place'
    ])
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_command(self, mock_stdout, mock_input):
        """Test the 'create' command for creating objects with parameters."""

        # Instantiate the HBNBCommand (console)
        console = HBNBCommand()

        # Run the test case
        console.cmdloop()

        # Capture the output
        output = mock_stdout.getvalue().strip()

        # Assert that the correct object IDs are printed
        self.assertTrue("d80e0344-63eb-434a-b1e0-07783522124e" in output)
        self.assertTrue("092c9e5d-6cc0-4eec-aab9-3c1d79cfc2d7" in output)

        # Check that the "State" objects are listed correctly
        self.assertIn("[State] (d80e0344-63eb-434a-b1e0-07783522124e)", output)
        self.assertIn("[State] (092c9e5d-6cc0-4eec-aab9-3c1d79cfc2d7)", output)

        # Check that the "Place" object is created and listed
        self.assertIn("[Place] (76b65327-9e94-4632-b688-aaa22ab8a124)", output)
        self.assertIn('"name": "My little house"', output)

        # Check if the Place object has correct attributes
        self.assertIn("number_rooms", output)
        self.assertIn("price_by_night", output)

if __name__ == "__main__":
    unittest.main()
