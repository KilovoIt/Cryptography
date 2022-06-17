import string

# This is an Enigma Machine emulator.
# Enigma Machine is a electromechanical cryptography device engineered
# in Germany and used from 1920s.
# It is a very complex machine with symmetrical encryption mechanism, 
# meaning each party has to know they key in order to exchange messages. 
# Unlike many other cryptography devices of this time, this machine was 
# able to change the key after each press of a button. Thus, the key was 
# changing dynamically and the same letter would come out different each 
# time it is pressed.

# There were two types of this machine: commercial type and later 
# military type. The commercial type had a set of 8 replaceable rotors 
# with 3 of them installed into the machine and each of them scrambling 
# the letter in a certain way. When the key is pressed, an electricity 
# flows through rotors and back, and lights up a light bulb with a 
# certain letter. This is the encrypted letter. Upon key release, the 
# rightmost rotor turns and changes the electrical signal path. just like
# second cogwheel turns minute cogwheel in a clock, rotors rotate one 
# another after certain position. To successfully decrypt a message, 
# the other party had to know what rotors are used, in which order they 
# are inserted, and the starting position of encryption. 
# This would be the 'key'.

# The military version was very much like a commercial, but it had an 
# addition to it: a plugboard. The plugboard is pretty much a commutator,
# that had a piece of wire connecting to sockets, each socket 
# representing a letter. When the final encrypted or decrypted signal 
# traveled back, it would be swapped in accordance with pairs set up on a
# plugboard. Military version was much harder to decrypt. The 'key' would
# be the same as for the commercial version, plus the plugboard setup.

# to better understand, how an Enigma Machine worked, 
# watch the video: https://www.youtube.com/watch?v=ybkkiGtJmkM
# Enigma Machine code was broken by Alan Turing and his team.


class EnigmaMachine:
    """represents a physical Enigma Machine from WWII.

    Attributes:
        direct (str): regular sequence of latin letters in a usual order.

        rotors (dict): a dictionary {integer: str}, each element 
            represents a rotor from a real Enigma Machine with exact
            sequence of symbols as they follow on this rotor. 
            Comparing value part of the element to the "direct" 
            attribute, each letter has the same index in the
            string with what it would be replaced on after parsing
            through this rotor. For example, if we put "direct" string 
            next to the 1st rotor, letter "A" would change to "E", as 
            they have the same index.

        notches (dict): a dictionary {int, [int, int]}, where key shows
            the rotor number, and the value indicates at which symbol 
            next rotor will turn 1 step. Some rotors have just 1 notch, 
            therefore they have two identical numbers, however,
            the last 3 of them have two notches and reaching either 
            one of them will turn the next rotor.

        reflector (str): reflector is a sequence of letters that is very 
            alike to a rotor with one exception: it does not spin and it 
            doesn't change. Its job to receive a letter, change it to a 
            corresponding letter, and launch it the opposite way.
    """

    direct = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rotors = {
        1: "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        2: "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        3: "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        4: "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        5: "VZBRGITYUPSDNHLXAWMJQOFECK",
        6: "JPGVOUMFYQBENHZRDKASXLICTW",
        7: "NZJHGRCXMYSWBOUFAIVLPEKQDT",
        8: "FKQHTLXOCBJSPDZRAMEWNIUYGV",
    }

    notches = {
        1: [16, 16],
        2: [3, 3],
        3: [20, 20],
        4: [8, 8],
        5: [24, 24],
        6: [11, 24],
        7: [11, 24],
        8: [11, 24],
    }

    reflector = "EJMZALYXVBWFCRQUONTSPIKHGD"

    def __init__(self, rotor_set="111", position=[0, 0, 0], set_plugboard=[], mode=0):
        """Initializing EnigmaMachine object

        Args:
            rotor_set (str, optional): three digits shows what rotors are
                used from the original EnigmaMachine.rotors dictionary. 
                Defaults to '111'.
            position (list, optional): sets rotor position, three numbers
                from 0 to 25. Defaults to [0, 0, 0].
            set_plugboard (list, optional): a list that accepts pairs of 
                letters, for example ['AB', 'DR']. Defaults to []. These 
                pairs will be added to the self.plugboard via 
                plugboardSetter() method as a part of __init__.


        Attributes:
            rotor_set (str): an attribute storing rotor set arg at the 
                beginning of the operation
            wheel1pos (int): an attribute storing 1 rotor position at the
                beginning of the operation
            wheel2pos (int): an attribute storing 2 rotor position at the
                beginning of the operation
            wheel3pos (int): an attribute storing 3 rotor position at the
                beginning of the operation
            plugboard (list): a python list of sets, each containing a 
                couple of letters to be swapped
                in the end of encryption and decryption. If no 
                set_plugboard parameter is passed, defaults to [].
            mode (int, optional): defines whether to retain the original 
                word length or chop the message into blocks with n 
                symbols each. Defaults to 0. when 0, original word length
                is preserved. Only Encrypt method uses this parameter.
        """

        self.rotor_set = rotor_set
        self.wheel1pos = position[0]
        self.wheel2pos = position[1]
        self.wheel3pos = position[2]
        self.plugboard = []
        self.mode = mode
        self.plugboardSetter(set_plugboard)

    def positionSetter(self, pos: list = None):
        """takes list of positions as an argument, sets them as 
        attributes wheel1pos, wheel2pos, wheel3pos of the instance

        Args:
            pos ([list]): [0, 0, 0] format wheel position, where the 
                digits can be from 0 to 25.
            The last condition is not critical, as 54 will mean rotor has
                to do 2 complete revolutions
                plus 2 positions, so 54 % 26 = 2 in this case
        """
        # asserting that input is in valid form
        #assert len(pos) == 3 and all(
        #    isinstance(item, int) for item in pos
        #), "Position format is invalid. Please, enter as [int, int, int]."
        if pos != None:
            self.wheel1pos = pos[0] % 26  # overstep protection
            self.wheel2pos = pos[1] % 26
            self.wheel3pos = pos[2] % 26

    def add_pair(self, pair: str):
        """adds set(pair) to the plugboard of the instance.

        Args:
            pair (str): input couple of letters.
        """
        pair = pair.upper()  # Only capital letters are used
        assert (
            len(pair) == 2 and type(pair) == str
        ), "Entered pair is invalid. Please, pass the pair of letters as 'AB'."
        # checks if pair consists of the same letter. There is no common 
        # sense to swap the letter on itself,
        # so in this case, the method does nothing.
        if pair[0] == pair[1]:
            return
        # checks if the pair set already in self.plugboard
        if set(pair) not in self.plugboard:
            # if neither of pair set elements exist in any of the pair 
            # sets, adds pair as a set() to self.pluigboard
            if all([
                    set(pair[0]).issubset(item) == False
                    for item in self.plugboard
            ]) and all([
                    set(pair[1]).issubset(item) == False
                    for item in self.plugboard
            ]):
                self.plugboard.append(set(pair))
            else:
                # if not, checks each pair element individually. 
                # If it is used in already existing pair set, it removes 
                # that set, and adds a new one with a given pair.
                if any(
                    [set(pair[0]).issubset(item) for item in self.plugboard]):
                    self.plugboard.pop([
                        set(pair[0]).issubset(item) for item in self.plugboard
                    ].index(True))
                if any(
                    [set(pair[1]).issubset(item) for item in self.plugboard]):
                    self.plugboard.pop([
                        set(pair[1]).issubset(item) for item in self.plugboard
                    ].index(True))
                self.plugboard.append(set(pair))

    def unpair_letter(self, letter: str):
        """takes a letter and deletes the pair set with it if that set 
        exists in plugboard

        Args:
            letter (str): a letter which will be unpaired
        """
        assert (len(letter) == 1 and type(letter) == str
                ), "Wrong input value for letter. Please, enter one letter"
        for index, pair in enumerate(self.plugboard):
            # looks if that letter is in any of the pair sets
            if set(letter.upper()).issubset(pair):
                # if it is, that pair set gets removed
                self.plugboard.pop(index)
                break

    def plugboardSetter(self, plugboard_values: list = None):
        """takes a list of letter couples and adds them
        into plugboard as sets

        Args:
            plugboard_values ([list of strings], optional): list in 
                ['AB', 'XY'] format.
        """

        if plugboard_values == None:
            # if nothing is passed
            return
        elif plugboard_values == []:
            # reset plugboard
            self.plugboard = []

        else:
            invalid = "Entered plugboard values are in invalid format. Please, \
                enter them as ['AB', 'CD']"
            assert all([isinstance(item, str)
                        for item in plugboard_values]) and all(
                            [len(item) == 2
                             for item in plugboard_values]), invalid
            for pair in plugboard_values:
                self.add_pair(pair.upper())

    def rotorHandler(self):
        """when called, makes rotor system turn 1 step"""

        def increase(wheel: int) -> int:
            """defines rotor position after 1 step increment"""
            return (wheel + 1) % 26

        # the following portion checks for notches on rotors.
        # if one of two notches match with current 1st rotor position:
        if (self.wheel1pos == EnigmaMachine.notches[int(self.rotor_set[0])][0]
                or self.wheel1pos == EnigmaMachine.notches[int(
                    self.rotor_set[0])][1]):
            # 1st rotors turns 1 step
            self.wheel1pos = increase(self.wheel1pos)
            # checks if 2nd rotor also has a notch 
            # at the current position:
            if (self.wheel2pos == EnigmaMachine.notches[int(
                    self.rotor_set[1])][0] or self.wheel1pos
                    == EnigmaMachine.notches[int(self.rotor_set[1])][1]):
                # 2nd rotor turns 1 step
                self.wheel2pos = increase(self.wheel2pos)
                # 3rd rotor turns 1 step
                self.wheel3pos = increase(self.wheel3pos)
            else:
                # 2nd rotor does not have a notch 
                # at the current position:
                # just 2nd rotor turns 1 step
                self.wheel2pos = increase(self.wheel2pos)
        else:
            # no rotors has notches at the current position
            # 1st rotor turns 1 step anyway
            self.wheel1pos = increase(self.wheel1pos)

    def stringChecker(self, input) -> str:
        """checks if a symbol can be converted to a string

        Args:
            symbol (any): input symbol

        Raises:
            AssertionError: if the symbol cannot be converted to str value

        Returns:
            str: if symbol can be converted to str, returns str(symbol)
        """
        try:
            input = str(input)  # in case of numerical input
            return input
        except:
            raise AssertionError("Input value cannot be converted to string")

    def plugboardHandler(self, symbol) -> str:
        """takes a symbol from encrypted/decrypted final message and 
        swaps it in accordance with plugboard pair sets

        Args:
            symbol (str): current symbol

        Returns:
            swapped symbol (str): if the symbol is a letter that bound to
                another in plugboard, it is replaced and returned
                for example, if plugboard has {'A', 'M'}, calling 
                plugboardHandler('A') will return 'M'. If the symbol is 
                not a letter, or this is a letter that's not in
                plugboard, the symbol will be returned unchanged.
        """
        symbol = self.stringChecker(
            symbol)  # checking if symbol can be a string

        assert (
            len(symbol) == 1
        ), "Invalid symbol input. The length of the resulting string is > than 1"
        for pair in self.plugboard:
            # if this symbol is in a current set, returns the other 
            # element of this set
            if pair.intersection(set(symbol)) != set():
                return list(pair.difference(set(symbol)))[0]
        # else the symbol itself returned
        return symbol

    def parser(self, symbol: str, func) -> str:
        """takes symbol and a function, filters out non-letters

        Args:
            symbol (str): a symbol of the message
                func (function): operating function, keyEncryptor or 
                keyDecryptor

        Returns:
            str: symbol that is changed in accordance with passed
                operating function
        """
        symbol = self.stringChecker(
            symbol)  # checking if symbol can be a string

        letters = list(string.ascii_letters)
        if symbol not in letters:
            # if it's not an encryptable/decryptable letter
            return symbol
        else:
            return func(symbol.upper())

    def keyEncryptor(self, key: str) -> str:
        """encrypts a letter according to the current rotors setup

        Args:
            key (str): a letter that enters

        Returns:
            str: an encrypted letter that exits

        Example of an encryption:
            encryption of a single key on a single rotor works under the 
            following scheme:
            output_letter = EnigmaMachine.rotors[number_of_rotor][
                            (index_of_that_inputted_key_in_rotor_string         
                            + rotor_position_shift) % 26]

            e.g. we are at position '25'(remember, they start at 0!) for 
            the 1st rotor, and the input key is 'G'.so we should get a 
            letter from the first rotor string by index, where index is 
            ord('G') - 65 + 25 = 31.
            But we don't have index 31, it would be out of list. However,
            because we use modulo operator at the end, we get the element
            under index 5 - which is also a letter 'G'! So, it did not 
            change after the first rotor, but there are manymore ahead.
            We subtract 65 from ord(letter) since ord('A') = 65, and 
            letter 'A' should align with the index 0.
        """
        # signal travels forwards, 1-2-3 rotors
        primary = EnigmaMachine.rotors[int(
            self.rotor_set[0])][(ord(key.upper()) - 65 + self.wheel1pos) %
                                26]  # Letter after rotor 1
        secondary = EnigmaMachine.rotors[int(
            self.rotor_set[1])][(ord(primary.upper()) - 65 + self.wheel2pos) %
                                26]  # Letter after rotor 2
        tertiary = EnigmaMachine.rotors[int(
            self.rotor_set[2])][(ord(secondary.upper()) - 65 + self.wheel3pos)
                                % 26]  # Letter after rotor 3

        # Letter after the reflector
        reflected = EnigmaMachine.reflector[ord(tertiary.upper()) - 65]
        # now signal travels backwards, 3-2-1 rotors
        quaternary = EnigmaMachine.rotors[int(
            self.rotor_set[2])][(ord(reflected.upper()) - 65 + self.wheel3pos)
                                % 26]  # Letter after rotor 3
        quinary = EnigmaMachine.rotors[int(
            self.rotor_set[1])][(ord(quaternary.upper()) - 65 + self.wheel2pos)
                                % 26]  # Letter after rotor 2
        senary = EnigmaMachine.rotors[int(
            self.rotor_set[0])][(ord(quinary.upper()) - 65 + self.wheel1pos) %
                                26]  # Letter after rotor 1

        # rotor setup turns 1 step
        self.rotorHandler()
        # final letter is returned
        return senary

    def keyDecryptor(self, key: str) -> str:
        """decrypts a letter according to a current rotor setup

        Args:
            key (str):an encrypted letter that enters

        Returns:
            str: a decrypted letter that exits

        Example of a decryption:
            decryption has a lot in common with how encryption works.
            output_letter = EnigmaMachine.direct[
                            (index_of_the_letter_in that_rotor - 
                            current_rotor_position) % 26]

            e.g. we got a letter 'R', it's the 2nd rotor at position 14.
            'R' has index 6 for the 2nd rotor, (6 - 14) % 26 = 18.
            now, letter in EnigmaMachine.direct with index 18 is 'S'.
            Thus 'R' decrypted into 'S' after the first rotor.
            There are many more to go.
            This time, rotor position gets subtracted since we are moving
            backwards.

            Note, that in order to correctly decrypt a letter, decryption
            rotor setup has to be identical with encryption rotor setup,
            e.g. if you encrypted it with [0, 4, 13] rotor positions, it 
            must be decrypted from [0, 4, 13] as well.
        """
        # Signal travels forwards, 1-2-3 rotors
        primary = EnigmaMachine.direct[(EnigmaMachine.rotors[int(
            self.rotor_set[0])].index(key.upper()) - self.wheel1pos) %
                                       26]  # Letter after rotor 1
        secondary = EnigmaMachine.direct[(EnigmaMachine.rotors[int(
            self.rotor_set[1])].index(primary.upper()) - self.wheel2pos) %
                                         26]  # Letter after rotor 2
        tertiary = EnigmaMachine.direct[(EnigmaMachine.rotors[int(
            self.rotor_set[2])].index(secondary.upper()) - self.wheel3pos) %
                                        26]  # Letter after rotor 3

        reflected = EnigmaMachine.direct[EnigmaMachine.reflector.index(
            tertiary.upper())]  # Letter after the reflector

        quaternary = EnigmaMachine.direct[(EnigmaMachine.rotors[int(
            self.rotor_set[2])].index(reflected.upper()) - self.wheel3pos) %
                                          26]  # Letter after rotor 3
        quinary = EnigmaMachine.direct[(EnigmaMachine.rotors[int(
            self.rotor_set[1])].index(quaternary.upper()) - self.wheel2pos) %
                                       26]  # Letter after rotor 2
        senary = EnigmaMachine.direct[(EnigmaMachine.rotors[int(
            self.rotor_set[0])].index(quinary.upper()) - self.wheel1pos) %
                                      26]  # Letter after rotor 1
        # rotor setup turns 1 step
        self.rotorHandler()
        # final letter is returned
        return senary

    def encrypt(
        self,
        message,
        position: list = None,
        plugboard_values: list = None
    ) -> str:
        """encrypts message

        Args:
            message (str): a message to be encrypted
                position (list, optional): encrypt from [int, int, int] 
                postition. Defaults to None.
            plugboard_values (list, optional): at the end, swap these 
                letters: e.g. ['AB', 'CD', 'EF']. Defaults to None.
        Returns:
            str: encrypted message
        """
        message = self.stringChecker(
            message)  # check if message can be converted to a string

        # set up parsed plugboard pairs if any
        self.plugboardSetter(plugboard_values)
        self.positionSetter(position)  # set up rotor position if any
        encrypted = ""
        if self.mode == 0:  # ordinal word length procedure
            for symbol in message:
                # decrypts message elementwise
                encrypted += self.plugboardHandler(
                    self.parser(symbol, self.keyEncryptor))
            return encrypted
        else:
            ctr = self.mode  # counter
            for symbol in message:
                if symbol != " ":  # if symbol is not a space, proceeds
                    ctr -= 1  # counter decreased by 1
                    encrypted += self.plugboardHandler(
                        self.parser(symbol, self.keyEncryptor))
                    if ctr == 0:
                        encrypted += " "  # adds a space to encr. string
                        ctr = self.mode  # reset
                else:
                    continue  # if symbol is a space, jumps to the next 
            # returns encrypted message
            return encrypted

    def decrypt(self,
                encr_message,
                position: list = None,
                plugboard_values: list = None) -> str:
        """decrypts message

        Args:
            encr_message (str): encrpyted message
            position (list, optional): rotor positions to decrypt from.
                Defaults to None.
            plugboard_values (list, optional): plugboard pairs to swap 
                after decryption, e.g. ['AB', 'CD', 'EF']. 
                Defaults to None.

        Returns:
            str: decrypted message
        """

        # sets up passed plugboard pairs
        self.plugboardSetter(plugboard_values)
        self.positionSetter(position)  # sets up passed rotor positions
        decrypted = ""
        for symbol in encr_message:
            # decrypts message stirng elementwise
            decrypted += self.parser(self.plugboardHandler(symbol),
                                     self.keyDecryptor)
        # returns decrypted message
        return decrypted


if __name__ == "__main__":
    # just an example
    text = "This is a secret message to be encrypted!"
    # creating an instance of a class, 
    # setting some letter pairs on the plugboard
    enigma1 = EnigmaMachine(set_plugboard=["AB", "CT"])
    # encrypting from a certain position, 
    # adding another pair to the plugboard
    encrypted = enigma1.encrypt(text, [3, 21, 6], ["kt"])
    print(encrypted)  # that's how encrypted message looks.
    # it decrypts back to the normal text
    print(enigma1.decrypt(encrypted, [3, 21, 6]))
