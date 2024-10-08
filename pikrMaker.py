import random


class PikrMaker():
    def __init__(self):
        self.participants = []

    def _validateParticipants(self, participants):

        if len(participants) <= 0:
            raise ParticipantError("No participants")

        if len(participants) == 1:
            raise ParticipantError("Only one participants")

        if len(participants) > 1000:
            raise ParticipantError("Too much participants. Max 1000")

    def _getOneReceiver(self, currentParticipant, pickSameGroup = True):

        if pickSameGroup:
            if len(self.receivers) == 1:
                return self.receivers[0]

            filteredReceivers = [
                receiver for receiver in self.receivers
                if receiver != currentParticipant
            ]
        else:
            filteredReceivers = [
                receiver for receiver in self.receivers
                if receiver != currentParticipant
                and receiver["groupName"] != currentParticipant["groupName"]
            ]

            if len(filteredReceivers) == 0:
                raise NoParticipantAvaillable(
                    "One participant have to pick in is family")

        pickedReceiver = random.choice(filteredReceivers)

        self.receivers.remove(pickedReceiver)
        return pickedReceiver

    def setParticipants(self, participants):

        self._validateParticipants(participants)

        self.participants = []

        for participant in participants:
            self.participants.append({
                "id": participant["id"],
                "groupName": participant["groupName"]
            })

    def getResults(self, pickSameGroup=True):

        self._validateParticipants(self.participants)

        retry = 0
        lastError = None

        while retry < 10:
            try:
                results = []
                self.receivers = self.participants.copy()
                random.shuffle(self.participants)

                for participant in self.participants:

                    receiver = self._getOneReceiver(participant, pickSameGroup)

                    if (participant == receiver):
                        raise UserMustPickItselfError()

                    results.append({
                        "giver": participant,
                        "receiver": receiver
                    })

                return results
            except UserMustPickItselfError as e:
                retry += 1
                lastError = e
            except NoParticipantAvaillable as e:
                retry += 1
                lastError = e

        raise lastError


class UserMustPickItselfError(Exception):
    pass


class NoParticipantAvaillable(Exception):
    pass


class ParticipantError(AssertionError):
    pass
