__author__ = 'james'


def prettyStatus(u):
    status="@" + u.handle
    if u.owner:
        status += " is owned by @" + u.owner.handle
    else:
        status += " is not owned"

    status += ". Their price is %s, they have %s credits and own %s players" % (
        u.price, u.balance, len(u.inventory))

    return status
