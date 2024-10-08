import unittest
from pikrMaker import PikrMaker, ParticipantError, NoParticipantAvaillable

class pikrTest(unittest.TestCase):

    def setUp(self):
        self.pikr = PikrMaker()

    def testSetNoParticipant(self):
        participant = []

        with self.assertRaises(ParticipantError):
            self.pikr.setParticipants(participant)
            self.pikr.getResults()

    def testSetOneParticipant(self):
        participant = [{"id": "idVal1", "groupName": "groupVal1"}]

        with self.assertRaises(ParticipantError):
            self.pikr.setParticipants(participant)

    def testSetTooMuchParticipant(self):
        participants = []

        for index in range(1001):
            participants.append({"id": "idVal{}".format(index), "groupName": "groupVal{}".format(index)})

        with self.assertRaises(ParticipantError):
            self.pikr.setParticipants(participants)

    def testSetTwoParticipant(self):
        participants = [
            {"id": "idVal1", "groupName": "groupVal1"},
            {"id": "idVal2", "groupName": "groupVal2"}
            ]

        self.pikr.setParticipants(participants)

        self.assertEqual(participants, self.pikr.participants)

    def testSetMultipleParticipant(self):

        participants = []

        for index in range(1000):
            participants.append({"id": "idVal{}".format(index), "groupName": "groupVal{}".format(index)})

        self.pikr.setParticipants(participants)

        self.assertEqual(participants, self.pikr.participants)
    
    def testResetParticipant(self):

        participants = [
            {"id": "idVal1", "groupName": "groupVal1"},
            {"id": "idVal2", "groupName": "groupVal2"}
            ]
        self.pikr.setParticipants(participants)

        participants = [
            {"id": "idVal3", "groupName": "groupVal4"},
            {"id": "idVal4", "groupName": "groupVal4"},
            {"id": "idVal5", "groupName": "groupVal5"}
            ]
        self.pikr.setParticipants(participants)

        self.assertEqual(3, len(self.pikr.participants))
        self.assertEqual(participants, self.pikr.participants)

    def testGetResults(self):

        participants = []

        for index in range(10):
            participants.append({"id": "idVal{}".format(index), "groupName": "groupVal{}".format(index)})

        self.pikr.setParticipants(participants)

        results = self.pikr.getResults()

        self.assertEqual(len(results), 10)

        for result in results:
            self.assertIn("giver", result)
            self.assertIn("id", result["giver"])
            self.assertIn("groupName", result["giver"])
            self.assertIn("receiver", result)
            self.assertIn("id", result["receiver"])
            self.assertIn("groupName", result["receiver"])
    
    def testCannotPickItself(self):

        participants = []

        for index in range(10):
            participants.append({"id": "idVal{}".format(index), "groupName": "groupVal{}".format(index)})

        self.pikr.setParticipants(participants)

        for iter in range(100):

            with self.subTest("Iteration : {}".format(iter)):

                results = self.pikr.getResults()

                self.assertEqual(len(results), 10)

                for result in results:
                    self.assertNotEqual(result["giver"], result["receiver"])         

    def testCannotHaveTwiceSameReceiver(self):

        participants = []

        for index in range(10):
            participants.append({"id": "idVal{}".format(index), "groupName": "groupVal{}".format(index)})

        self.pikr.setParticipants(participants)

        for iter in range(100):

            with self.subTest("Iteration : {}".format(iter)):

                results = self.pikr.getResults()

                for participant in participants:

                    givers = [result["receiver"] for result in results if result["receiver"] == participant]

                    self.assertEqual(1, len(givers))
    
    def testCannotPickSameGroup(self):

        participants = [
            {"id": "idVal1-1", "groupName": "groupVal1"},
            {"id": "idVal1-2", "groupName": "groupVal1"},
            {"id": "idVal2-1", "groupName": "groupVal2"},
            {"id": "idVal2-2", "groupName": "groupVal2"}
            ]

        for iter in range(10):
            self.pikr.setParticipants(participants)

            results = self.pikr.getResults(pickSameGroup=False)

            for result in results:
                self.assertNotEqual(result["receiver"]["groupName"], result["giver"]["groupName"])

    def testNoParticipantAvailableInOtherGroup(self):

        participants = [
            {"id": "idVal1-1", "groupName": "groupVal1"},
            {"id": "idVal1-2", "groupName": "groupVal1"},
            {"id": "idVal2-1", "groupName": "groupVal2"}
            ]
        
        self.pikr.setParticipants(participants)

        with self.assertRaises(NoParticipantAvaillable):
            self.pikr.getResults(pickSameGroup=False)

if __name__ == '__main__':  
    unittest.main()  