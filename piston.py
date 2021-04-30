from pistonapi import PistonAPI, PistonError

piston = PistonAPI()

# This a dynamic property, so we save it to make less api calls.
languages = piston.languages

def completeAlias(alias):
    """Completes an alias, example: js -> javascript, returns the same alias if it can not be completed."""
    for name, properties in languages.items():
        if alias in properties["aliases"]:
            alias = name
    return alias

def getVersion(language):
    """Gets the recommended version for a specific language, returns None if the language is unknown."""
    return languages.get(language, {"version" : None})["version"]

@polygon.on(pattern="piston (.*)")
async def pistonfn(e):
    arguments = e.pattern_match.group(1)
    language, code = arguments.split(maxsplit=1)
    language = completeAlias(language)
    version = getVersion(language) or "1.0"
    try:
        result = piston.execute(language, version, code)
    except PistonError as error:
        result = error
    await e.edit(
        f"Language:\n`{language}` v`{version}` \
        \n\nQuery: \n`{code}` \
        \n\nOutput: \n`{result}` \
        "
    )
