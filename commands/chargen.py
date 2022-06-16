from random import choice, random
from textwrap import wrap
from evennia.commands.default.muxcommand import MuxCommand
from world.lifepath import LIFEPATH


class lifepath(MuxCommand):
    """
    Set and edit your basic lifepath chart. This command will also lead
    you through a short @pprogram to lead you through selecting the
    multiple choice options of your profession.

    Usage:
        +lp/roll          - Roll your basic character lifepath.
        +lp/roll/<role>   - Choose a role, and create a lifepath fpr it.
        +lp/reset         - Reset your normal or roll lifepath
        +lp/reset/<role>  - Reset your role based lifepath only.
    """

    key = "lifepath"
    aliases = ["lp, +lp, +lifepath"]

    def generate_path(self):
        self.caller.db.lifepath = {}
        lp = self.caller.db.lifepath

        # Your (General) Cultural Region
        origins = LIFEPATH["CULTURAL ORIGINS"]["Your (General) Cultural Region"]
        region = choice(list(origins.keys()))
        lp["cultural origins"] = {"name": region, "languages": origins[region]}

        # Personality
        lp["personality"] = choice(LIFEPATH["YOUR PERSONALITY"]["What Are You Like?"])

        # Clothing and Style
        style = LIFEPATH["DRESS AND PERSONAL STYLE"]

        lp["dress and personal style"] = {
            "clothing style": choice(style["Clothing Style"]),
            "hairstyle": choice(style["Hairstyle"]),
            "affection you are not without": choice(
                style["Affectation You Are Never Without"]
            ),
        }

        # Motiviation and Relationships
        motivations = LIFEPATH["YOUR MOTIVATIONS AND RELATIONSHIPS"]
        lp["your motiviations and relationships"] = {
            "what do you value most": choice(motivations["What Do You Value Most?"]),
            "how do you feel about most people": choice(
                motivations["How Do You Feel About Most People?"]
            ),
            "most valued person in your life": choice(
                motivations["Most Valued Person in Your Life?"]
            ),
            "most valued possession you own": choice(
                motivations["Most Valued Posession You Own?"]
            ),
        }

        # Original Family Background
        background = choice(
            list(
                LIFEPATH["YOUR ORIGINAL FAMILY BACKGROUND"][
                    "Original Background"
                ].keys()
            )
        )
        history = LIFEPATH["YOUR ORIGINAL FAMILY BACKGROUND"]["Original Background"][
            background
        ]

        lp["original background"] = {"background": background, "history": history}

        # Enviornment
        lp["your environment"] = choice(
            LIFEPATH["YOUR ENVIRONMENT"]["Childhood Environment"]
        )

        # Your Family Crisis
        lp["your family crisis"] = choice(LIFEPATH["YOUR FAMILY CRISIS"]["Background"])

        # Your Friends
        num = int(random() * 10 + 1 - 7)
        friends = []
        if num > 0:
            for x in range(num):
                friends.append(choice(LIFEPATH["YOUR FRIENDS"]["Friend"]))
            lp["friends"] = friends

        # Enemies
        num = int(random() * 10 + 1 - 7)
        enemies = []
        path = LIFEPATH["YOUR ENEMIES"]
        if num > 0:
            for x in range(num):
                enemies.append(
                    {
                        "enemy": choice(path["Enemy"]),
                        "what caused it": choice(path["What Caused It?"]),
                        "what can they throw at you": choice(
                            path["What Can They Throw At You?"]
                        ),
                        "What are you/they gonna do about it": choice(
                            LIFEPATH["SWEET REVENGE"][
                                "What are You/They Gonna do About It?"
                            ]
                        ),
                    }
                )
        lp["enemies"] = enemies

        # The Wrap Up
        lp["life goals"] = choice(LIFEPATH["THE WRAP UP"]["Life Goals"])

    def show_cultural_origins(self):

        lp = self.caller.db.lifepath
        langs = f"|wPotential Languages:|n " + ", ".join(
            lp["cultural origins"]["languages"]
        )
        output = "\nCULTURAL ORIGINS\n"

        output += (
            f"|wYour (general) Cultural Region:|n {lp['cultural origins']['name']}\n"
        )
        output += langs
        return output

    def show_personality(self):
        lp = self.caller.db.lifepath
        output = "\n\nYOUR PERSONALITY\n"

        output += f"|wWhat Are You Like?: |n{lp['personality']}\n"
        output += "\nDRESS AND PERSONAL STYLE\n"

        output += (
            f"|wClothing Style: |n{lp['dress and personal style']['clothing style']}\n"
        )
        output += f"|wHairstyle: |n{lp['dress and personal style']['hairstyle']}\n"
        output += f"|wAffection You're Not Without?: |n{lp['dress and personal style']['affection you are not without']}\n"
        return output

    def show_motivation(self):
        lp = self.caller.db.lifepath
        output = "\nMOTIVATION AND RELATIONSHIPS\n"
        output += f"|wWhat Do You Value Most?: |n{lp['your motiviations and relationships']['what do you value most']}\n"
        output += f"|wHow Do you Feel About Most People?: |n{lp['your motiviations and relationships']['how do you feel about most people']}\n"
        output += f"|wWMost Valued Person in Your Life?: |n{lp['your motiviations and relationships']['most valued person in your life']}\n"
        output += f"|wWMost Valued Possession You Own?: |n{lp['your motiviations and relationships']['most valued possession you own']}\n"
        return output

    def show_background(self):
        lp = self.caller.db.lifepath
        output = "\nYOUR ORIGINAL FAMILY BACKGROUND\n"
        output += f"|wBackground: |n{lp['original background']['background']}\n"
        output += f"|wHistory: |n{lp['original background']['history']}\n"
        return output

    def show_environment(self):
        lp = self.caller.db.lifepath
        output = "\nYOUR ENVIRONMENT\n"
        output += f"|wChildhood environment: |n{lp['your environment']}\n"
        return output

    def show_family_crisis(self):
        lp = self.caller.db.lifepath
        output = "\nYOUR FAMILY CRISIS\n"
        output += f"|wYour Family Crisis: |n{lp['your family crisis']}\n"
        return output

    def show_friends(self):
        lp = self.caller.db.lifepath
        output = "\nYOUR FRIENDS\n"
        output += "\n".join(lp["friends"]) + "\n" if "friends" in lp.keys() else "\n"
        return output

    def show_life_goals(self):
        lp = self.caller.db.lifepath
        output = "\nTHE WRAP UP\n"
        output += f"|wLife Goals: |n{lp['life goals']}\n"
        return output

    def func(self):
        self.generate_path()
        output = "|b>> |w./lifepath.sh|n"
        output += self.show_cultural_origins()
        output += self.show_personality()
        output += self.show_motivation()
        output += self.show_background()
        output += self.show_environment()
        output += self.show_family_crisis()
        output += self.show_friends()
        output += self.show_life_goals()

        self.msg(output)
