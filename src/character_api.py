CHARACTER_API = "http://0.0.0.0:8080/Character"
CHARACTER_FRONT = "http://localhost:3000"

###############################################################################
#                        url manipulations functions                          #
###############################################################################


def createCharacterURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/CreateCharacter?idPlayer={idPlayer}&idGame={idGame}"


def getCharacterURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/GetCharacter?idPlayer={idPlayer}&idGame={idGame}"


def deleteCharacterURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/DeleteCharacter?idPlayer={idPlayer}&idGame={idGame}"


def takeDamageURL(idPlayer: int, idGame: int, amount: int):
    return f"{CHARACTER_API}/TakeDamage?idPlayer={idPlayer}&idGame={idGame}&amount={amount}"


def rollInitiativeURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/RollInitiative?idPlayer={idPlayer}&idGame={idGame}"


def rollAnyURL(idPlayer: int, idGame: int, abilityName: str):
    return f"{CHARACTER_API}/RollAny?idPlayer={idPlayer}&idGame={idGame}&name={abilityName}"


def rollAttackURL(idPlayer: int, idGame: int, weaponIdx: int):
    return f"{CHARACTER_API}/RollAttack?idPlayer={idPlayer}&idGame={idGame}&index={weaponIdx}"


def rollDamageURL(idPlayer: int, idGame: int, weaponIdx: int):
    return f"{CHARACTER_API}/RollDamage?idPlayer={idPlayer}&idGame={idGame}&index={weaponIdx}"


def modifyCharacterURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_FRONT}?idPlayer={idPlayer}&idGame={idGame}"


def listStatsURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/GetStats?idPlayer={idPlayer}&idGame={idGame}"


def listWeaponsURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/GetWeapons?idPlayer={idPlayer}&idGame={idGame}"


def listSkillsURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/GetSkills?idPlayer={idPlayer}&idGame={idGame}"


def listSavingsThrowsURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/GetSavingThrows?idPlayer={idPlayer}&idGame={idGame}"


def listInfosURL(idPlayer: int, idGame: int):
    return f"{CHARACTER_API}/GetInfo?idPlayer={idPlayer}&idGame={idGame}"
