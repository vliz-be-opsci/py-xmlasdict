""" xmlasdict

.. module:: xmlasdict
    :synopsis: python library to read xml DOM trees as dicts (with iter and gettattribute behaviour)

.. moduleauthor:: Marc Portier <marc.portier@gmail.com>

"""

from .wrapper import MyModel
import logging

__all__ = ['MyModel']

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
