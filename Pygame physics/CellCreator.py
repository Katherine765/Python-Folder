# cells are dictionaries that store attributes of a loc
def getCellCreator(required, optional):
    def cellCreator(*args, **kwargs):
        result = {attr: value for attr, value in zip(required, args)}
        result.update(optional)
        result.update(kwargs) # overrides defaults when applicable
        return result
    return cellCreator