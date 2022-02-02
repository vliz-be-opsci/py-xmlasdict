""" xmlasdict

.. module:: xmlasdict
    :synopsis: python library to read xml DOM trees as dicts (with iter and gettattribute behaviour)

.. moduleauthor:: Marc Portier <marc.portier@gmail.com>

"""

from .parser import parse
from .wrapper import Wrapper
import logging

__all__ = ['parse', 'Wrapper']

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
